"""Generate a grounded answer using retrieved chunks and OpenAI GPT-4o.

Includes confidence scoring: if retrieved chunks are too few or too distant
semantically, the model is instructed to say it doesn't know rather than
risk hallucinating medical information.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config
from openai import AsyncOpenAI

_client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

_SYSTEM = """\
You are MedChat, a careful medical information assistant that only uses information
from verified clinical sources (NIH, CDC, WHO, Mayo Clinic, peer-reviewed journals, etc.).

Rules you must ALWAYS follow:
1. Answer ONLY using the context passages provided. Do NOT add any medical facts from memory.
2. Cite sources inline as [1], [2], etc., matching the passage numbers in the context.
3. If the context does not contain a clear, reliable answer to the question, respond with
   a variation of: "I'm not confident I have reliable information on that from my trusted
   sources. I'd recommend speaking with a healthcare professional or checking resources
   like NIH MedlinePlus (medlineplus.gov) directly."
4. Never speculate, extrapolate, or guess about diagnoses, dosages, or treatments.
5. Always end answers about symptoms, treatments, or medications with:
   "⚕ This information is for educational purposes only. Please consult a qualified
   healthcare professional before making any medical decisions."
"""

_LOW_CONFIDENCE_RESPONSE = (
    "I'm not confident I have reliable information on that from my trusted sources. "
    "The clinical sources I searched didn't return enough relevant material to give you "
    "a well-grounded answer on this topic.\n\n"
    "I'd recommend consulting a qualified healthcare professional, or checking these "
    "authoritative resources directly:\n"
    "- **NIH MedlinePlus**: medlineplus.gov\n"
    "- **CDC**: cdc.gov\n"
    "- **WHO**: who.int\n\n"
    "⚕ Always consult a healthcare professional for personal medical advice."
)


def _assess_confidence(chunks: list[dict]) -> bool:
    """
    Return True (high confidence) if we have enough well-matched chunks.
    chunks may carry an optional 'distance' field from the vector store.
    """
    if len(chunks) < config.MIN_CONFIDENT_CHUNKS:
        return False

    # If distance scores are available, check them
    chunks_with_scores = [c for c in chunks if "distance" in c]
    if chunks_with_scores:
        good = [c for c in chunks_with_scores if c["distance"] < config.CONFIDENCE_DISTANCE_THRESHOLD]
        return len(good) >= config.MIN_CONFIDENT_CHUNKS

    # No distance info – fall back to chunk count alone
    return True


async def generate_answer(question: str, chunks: list[dict]) -> tuple[str, bool]:
    """
    Returns (answer_text, is_confident).
    Callers can use is_confident to set a flag in the API response.
    """
    if not _assess_confidence(chunks):
        return _LOW_CONFIDENCE_RESPONSE, False

    # Build numbered context block
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(f"[{i}] (source: {chunk['source']})\n{chunk['text']}")
    context = "\n\n---\n\n".join(context_parts)

    user_message = f"Context:\n{context}\n\nMedical question: {question}"

    response = await _client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": user_message},
        ],
        temperature=0.1,   # lower temp for medical accuracy
        max_tokens=1024,
    )
    answer = response.choices[0].message.content or _LOW_CONFIDENCE_RESPONSE

    # Heuristic: if the model itself signals uncertainty, mark low-confidence
    uncertainty_signals = [
        "i don't have", "i'm not confident", "i cannot find",
        "not enough information", "consult a", "speak with a",
    ]
    is_confident = not any(s in answer.lower() for s in uncertainty_signals)

    return answer, is_confident
