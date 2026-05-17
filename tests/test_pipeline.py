"""Integration tests for question analysis + chunker pipeline."""
import pytest
from pipeline.question_analysis import analyse_question
from pipeline.chunker import chunk_text


def test_analyse_factual():
    result = analyse_question("Who invented the telephone?")
    assert result["intent"] == "factual"
    assert "telephone" in result["keywords"]
    assert len(result["queries"]) >= 1


def test_analyse_comparative():
    result = analyse_question("What is the difference between TCP vs UDP?")
    assert result["intent"] == "comparative"


def test_analyse_produces_queries():
    result = analyse_question("How does photosynthesis work?")
    assert isinstance(result["queries"], list)
    assert len(result["queries"]) > 0


def test_pipeline_chunk_and_analyse():
    """Question analysis feeds into chunking without errors."""
    question = "Explain the water cycle in detail"
    analysis = analyse_question(question)
    assert analysis["keywords"]

    # Simulate a scraped + cleaned page
    sample_text = "\n\n".join([
        "The water cycle describes how water evaporates from the surface of the earth.",
        "Water vapour rises into the atmosphere and forms clouds through condensation.",
        "Precipitation returns water to the ground as rain or snow.",
        "The cycle repeats continuously and is essential for life on Earth.",
    ] * 10)

    chunks = chunk_text(sample_text, chunk_size=128, overlap=16)
    assert len(chunks) > 1
    assert all(isinstance(c, str) for c in chunks)
