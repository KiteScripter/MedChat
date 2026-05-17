"""Trusted web search via SerpAPI or Brave Search.

Only URLs whose hostname matches a domain in config.TRUSTED_MEDICAL_DOMAINS
are returned. All others are silently dropped, ensuring the RAG pipeline
never ingests content from unvetted sources.
"""
from __future__ import annotations
import httpx
import sys
import os
from urllib.parse import urlparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config


def _is_trusted(url: str) -> bool:
    """Return True only if the URL's hostname is on the medical allowlist."""
    try:
        host = urlparse(url).hostname or ""
    except Exception:
        return False
    return any(host == d or host.endswith("." + d) for d in config.TRUSTED_MEDICAL_DOMAINS)


def _filter_urls(urls: list[str]) -> list[str]:
    return [u for u in urls if _is_trusted(u)]


async def _serpapi_search(query: str, client: httpx.AsyncClient) -> list[str]:
    params = {
        "q": query,
        "api_key": config.SERPAPI_KEY,
        "num": 10,
        "hl": "en",
        "gl": "us",
    }
    r = await client.get("https://serpapi.com/search", params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return [item["link"] for item in data.get("organic_results", [])]


async def _brave_search(query: str, client: httpx.AsyncClient) -> list[str]:
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": config.BRAVE_API_KEY,
    }
    params = {"q": query, "count": 10}
    r = await client.get(
        "https://api.search.brave.com/res/v1/web/search",
        headers=headers,
        params=params,
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()
    return [item["url"] for item in data.get("web", {}).get("results", [])]


async def web_search(queries: list[str]) -> list[str]:
    """Return a deduplicated list of trusted-domain URLs from all queries."""
    all_urls: list[str] = []
    async with httpx.AsyncClient() as client:
        for query in queries:
            try:
                if config.SEARCH_PROVIDER == "brave":
                    urls = await _brave_search(query, client)
                else:
                    urls = await _serpapi_search(query, client)
                all_urls.extend(urls)
            except Exception as exc:
                print(f"[search] warning: {exc}")

    seen: set[str] = set()
    deduped = []
    for url in all_urls:
        if url not in seen:
            seen.add(url)
            deduped.append(url)

    trusted = _filter_urls(deduped)
    print(f"[search] {len(deduped)} URLs found, {len(trusted)} from trusted medical sources")
    return trusted
