"""Tests for scraper and cleaner."""
import pytest
from scraper.cleaner import clean_text


def test_clean_removes_urls():
    raw = "Visit https://example.com for more info."
    result = clean_text(raw)
    assert "https://" not in result


def test_clean_collapses_whitespace():
    raw = "hello    world   test"
    result = clean_text(raw)
    assert "  " not in result


def test_clean_deduplicates_lines():
    raw = "Same line\nSame line\nSame line"
    result = clean_text(raw)
    assert result.count("Same line") == 1
