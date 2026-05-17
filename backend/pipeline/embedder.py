"""Embed text chunks using OpenAI text-embedding-3-small."""
from __future__ import annotations
import asyncio
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config
from openai import AsyncOpenAI

_client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
_BATCH = 100  # OpenAI allows up to 2048 inputs per request; 100 is safe


async def _embed_batch(texts: list[str]) -> list[list[float]]:
    resp = await _client.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in resp.data]


async def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Add an 'embedding' key to each chunk dict.

    Input:  [{"text": "...", "source": "https://..."}]
    Output: [{"text": "...", "source": "...", "embedding": [...]}]
    """
    texts = [c["text"] for c in chunks]
    embeddings: list[list[float]] = []

    for i in range(0, len(texts), _BATCH):
        batch = texts[i : i + _BATCH]
        vecs = await _embed_batch(batch)
        embeddings.extend(vecs)

    return [
        {**chunk, "embedding": emb}
        for chunk, emb in zip(chunks, embeddings)
    ]


async def embed_query(text: str) -> list[float]:
    vecs = await _embed_batch([text])
    return vecs[0]
