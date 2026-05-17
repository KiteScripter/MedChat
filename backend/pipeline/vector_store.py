"""Vector database abstraction – ChromaDB (local) or Pinecone (cloud).

ChromaDB results now include distance scores so the LLM layer can perform
confidence assessment.
"""
from __future__ import annotations
import uuid
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config
from pipeline.embedder import embed_query


class VectorStore:
    def __init__(self) -> None:
        if config.PINECONE_API_KEY:
            self._backend = _PineconeBackend()
        else:
            self._backend = _ChromaBackend()

    def upsert(self, chunks: list[dict]) -> None:
        self._backend.upsert(chunks)

    def query(self, question: str, top_k: int = config.TOP_K_RESULTS) -> list[dict]:
        import asyncio
        vec = asyncio.get_event_loop().run_until_complete(embed_query(question))
        return self._backend.query(vec, top_k)


# ── ChromaDB ──────────────────────────────────────────────────────────────

class _ChromaBackend:
    def __init__(self) -> None:
        import chromadb
        self._client = chromadb.PersistentClient(path=config.CHROMA_PERSIST_DIR)
        self._col = self._client.get_or_create_collection(
            name="medchat_chunks",
            metadata={"hnsw:space": "cosine"},
        )

    def upsert(self, chunks: list[dict]) -> None:
        if not chunks:
            return
        ids = [str(uuid.uuid4()) for _ in chunks]
        self._col.upsert(
            ids=ids,
            embeddings=[c["embedding"] for c in chunks],
            documents=[c["text"] for c in chunks],
            metadatas=[{"source": c["source"]} for c in chunks],
        )

    def query(self, vector: list[float], top_k: int) -> list[dict]:
        res = self._col.query(query_embeddings=[vector], n_results=top_k)
        results = []
        docs = res["documents"][0]
        metas = res["metadatas"][0]
        distances = res.get("distances", [[]])[0]
        for i, (doc, meta) in enumerate(zip(docs, metas)):
            entry = {"text": doc, "source": meta["source"]}
            if distances and i < len(distances):
                entry["distance"] = distances[i]
            results.append(entry)
        return results


# ── Pinecone ──────────────────────────────────────────────────────────────

class _PineconeBackend:
    def __init__(self) -> None:
        from pinecone import Pinecone
        pc = Pinecone(api_key=config.PINECONE_API_KEY)
        self._index = pc.Index(config.PINECONE_INDEX)

    def upsert(self, chunks: list[dict]) -> None:
        vectors = [
            {
                "id": str(uuid.uuid4()),
                "values": c["embedding"],
                "metadata": {"text": c["text"], "source": c["source"]},
            }
            for c in chunks
        ]
        self._index.upsert(vectors=vectors)

    def query(self, vector: list[float], top_k: int) -> list[dict]:
        res = self._index.query(vector=vector, top_k=top_k, include_metadata=True)
        return [
            {
                "text": m.metadata["text"],
                "source": m.metadata["source"],
                "distance": 1.0 - m.score,  # convert similarity → distance
            }
            for m in res.matches
        ]
