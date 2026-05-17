"""Tests for the text chunker."""
import pytest
from pipeline.chunker import chunk_text


def test_short_text_single_chunk():
    text = "This is a short sentence."
    chunks = chunk_text(text, chunk_size=512, overlap=64)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_chunks_are_non_empty():
    text = "\n\n".join([f"Paragraph {i}: " + "word " * 100 for i in range(10)])
    chunks = chunk_text(text, chunk_size=100, overlap=10)
    assert all(c.strip() for c in chunks)


def test_overlap_produces_more_chunks():
    text = " ".join(["word"] * 300)
    chunks_with_overlap = chunk_text(text, chunk_size=50, overlap=20)
    chunks_no_overlap = chunk_text(text, chunk_size=50, overlap=0)
    assert len(chunks_with_overlap) >= len(chunks_no_overlap)
