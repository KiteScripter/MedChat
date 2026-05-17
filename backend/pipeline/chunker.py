"""Recursive character-based text chunker with token-aware sizing."""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config

try:
    import tiktoken
    _enc = tiktoken.get_encoding("cl100k_base")

    def _token_len(text: str) -> int:
        return len(_enc.encode(text))
except ImportError:
    def _token_len(text: str) -> int:  # type: ignore[misc]
        return len(text) // 4  # rough fallback


_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]


def _split(text: str, separators: list[str], chunk_size: int, overlap: int) -> list[str]:
    if not text.strip():
        return []

    sep = ""
    remaining = list(separators)
    while remaining:
        sep = remaining.pop(0)
        if sep in text or not remaining:
            break

    splits = text.split(sep) if sep else list(text)
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for s in splits:
        s_len = _token_len(s)
        if current_len + s_len > chunk_size and current:
            chunks.append(sep.join(current).strip())
            # keep overlap
            while current and current_len > overlap:
                removed = current.pop(0)
                current_len -= _token_len(removed)
        current.append(s)
        current_len += s_len

    if current:
        chunks.append(sep.join(current).strip())

    return [c for c in chunks if c]


def chunk_text(
    text: str,
    chunk_size: int = config.CHUNK_SIZE,
    overlap: int = config.CHUNK_OVERLAP,
) -> list[str]:
    """Split *text* into overlapping chunks of ≤chunk_size tokens."""
    return _split(text, list(_SEPARATORS), chunk_size, overlap)
