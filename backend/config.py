"""Central configuration loaded from environment variables."""
from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "MedChat"
APP_TAGLINE = "Medical information from trusted clinical sources only."

OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
SERPAPI_KEY: str = os.getenv("SERPAPI_KEY", "")
BRAVE_API_KEY: str = os.getenv("BRAVE_API_KEY", "")
SEARCH_PROVIDER: str = os.getenv("SEARCH_PROVIDER", "serpapi")  # serpapi | brave

CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX: str = os.getenv("PINECONE_INDEX", "medchat-index")
PINECONE_ENV: str = os.getenv("PINECONE_ENV", "us-east-1")

TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "6"))
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "64"))
MAX_SCRAPE_WORKERS: int = int(os.getenv("MAX_SCRAPE_WORKERS", "8"))

# Cosine similarity threshold below which the answer is considered low-confidence.
# ChromaDB distances are in [0, 2]; lower = more similar.
CONFIDENCE_DISTANCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_DISTANCE_THRESHOLD", "0.45"))
# If fewer than this many chunks are retrieved above threshold, flag as low-confidence.
MIN_CONFIDENT_CHUNKS: int = int(os.getenv("MIN_CONFIDENT_CHUNKS", "2"))

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o"

# ── Trusted medical domains (allowlist) ──────────────────────────────────────
# Only URLs from these domains are scraped. Everything else is dropped.
TRUSTED_MEDICAL_DOMAINS: list[str] = [
    "nih.gov",
    "pubmed.ncbi.nlm.nih.gov",
    "ncbi.nlm.nih.gov",
    "medlineplus.gov",
    "cdc.gov",
    "who.int",
    "mayoclinic.org",
    "clevelandclinic.org",
    "hopkinsmedicine.org",
    "webmd.com",
    "healthline.com",
    "medicalnewstoday.com",
    "bmj.com",
    "thelancet.com",
    "nejm.org",
    "jamanetwork.com",
    "acpjournals.org",
    "uptodate.com",
    "emedicine.medscape.com",
    "merckmanuals.com",
    "drugs.com",
    "rxlist.com",
    "fda.gov",
    "nhs.uk",
    "nice.org.uk",
]
