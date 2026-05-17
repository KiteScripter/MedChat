"""Analyse the user question to produce optimised search queries."""
from __future__ import annotations
import re


_STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been",
    "do", "does", "did", "will", "would", "could", "should", "may",
    "can", "in", "on", "at", "to", "for", "of", "and", "or", "but",
    "what", "how", "why", "when", "where", "who", "which",
}


def _extract_keywords(question: str) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9']+", question.lower())
    return [w for w in words if w not in _STOP_WORDS and len(w) > 2]


def _detect_intent(question: str) -> str:
    q = question.lower()
    if any(q.startswith(p) for p in ("how", "what is", "explain", "describe")):
        return "explanatory"
    if any(p in q for p in ("vs", "versus", "compare", "difference between")):
        return "comparative"
    if any(p in q for p in ("best", "top", "recommend", "should i")):
        return "advisory"
    if any(p in q for p in ("when", "who", "where", "which year")):
        return "factual"
    return "general"


def analyse_question(question: str) -> dict:
    keywords = _extract_keywords(question)
    intent = _detect_intent(question)

    # Build 2 complementary search queries
    base_query = " ".join(keywords[:8])
    queries = [question, base_query] if base_query != question else [question]

    return {
        "original": question,
        "intent": intent,
        "keywords": keywords,
        "queries": queries,
    }
