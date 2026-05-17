"""Clean and normalise scraped text."""
from __future__ import annotations
import re

try:
    import ftfy
    _ftfy_available = True
except ImportError:
    _ftfy_available = False


_WHITESPACE = re.compile(r"\s{2,}")
_URLS = re.compile(r"https?://\S+")
_UNICODE_BULLETS = re.compile(r"[•·▪▸►◆◇○●]")


def clean_text(text: str) -> str:
    if _ftfy_available:
        text = ftfy.fix_text(text)

    # Remove bare URLs
    text = _URLS.sub(" ", text)
    # Normalise bullet chars
    text = _UNICODE_BULLETS.sub("-", text)
    # Collapse whitespace
    text = _WHITESPACE.sub(" ", text)
    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in text.splitlines()]
    # Drop very short lines (likely nav remnants)
    lines = [l for l in lines if len(l) > 20]
    # Deduplicate consecutive identical lines
    deduped: list[str] = []
    prev = ""
    for line in lines:
        if line != prev:
            deduped.append(line)
            prev = line

    return "\n".join(deduped).strip()
