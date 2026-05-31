"""
base_scraper.py — Shared Bright Data request logic with local caching.
Uses Bright Data Web Unlocker REST API directly with zone name.
All scrapers import fetch_url() and fetch_serp() from here.
"""

import os
import json
import time
import hashlib
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")
ZONE = os.getenv("BRIGHTDATA_ZONE", "wellsignal_unlocker")
CACHE_DIR = Path("cache")
BD_ENDPOINT = "https://api.brightdata.com/request"


def _get_cache_path(scraper_name: str, key: str) -> Path:
    """
    Returns a cache file path for a given scraper and URL/query key.

    Args:
        scraper_name: Name of the scraper (used as subfolder).
        key: URL or query string to hash.

    Returns:
        Path object pointing to the cache file.
    """
    key_hash = hashlib.md5(key.encode()).hexdigest()
    path = CACHE_DIR / scraper_name
    path.mkdir(parents=True, exist_ok=True)
    return path / f"{key_hash}.json"


def fetch_url(url: str, scraper_name: str = "default") -> str:
    """
    Fetches raw HTML from any URL via Bright Data Web Unlocker.
    Returns cached result if available — never re-fetches same URL during dev.

    Args:
        url: The URL to scrape.
        scraper_name: Used to namespace the cache folder.

    Returns:
        Raw HTML string of the page.
    """
    cache_path = _get_cache_path(scraper_name, url)

    if cache_path.exists():
        print(f"[cache hit] {url}")
        return json.loads(cache_path.read_text())["html"]

    print(f"[fetching] {url}")
    time.sleep(1)  # protect credits

    try:
        response = requests.post(
            BD_ENDPOINT,
            headers={
                "Authorization": f"Bearer {API_TOKEN}",
                "Content-Type": "application/json"
            },
            json={"zone": ZONE, "url": url, "format": "raw"},
            timeout=60
        )
        response.raise_for_status()
        html = response.text
        cache_path.write_text(json.dumps({"url": url, "html": html}))
        print(f"[fetched] {len(html)} chars from {url}")
        return html

    except requests.RequestException as e:
        print(f"[error] Failed to fetch {url}: {e}")
        raise


def fetch_serp(query: str, num_results: int = 10) -> list[dict]:
    """
    Queries Google via Bright Data SERP API (Unlocker zone).
    Caches results locally to avoid repeat credit usage.

    Args:
        query: Search query string.
        num_results: Number of results to return.

    Returns:
        List of dicts with keys: title, url, snippet.
    """
    cache_path = _get_cache_path("serp", query)

    if cache_path.exists():
        print(f"[cache hit] serp: {query}")
        return json.loads(cache_path.read_text())["results"]

    print(f"[serp fetching] {query}")
    time.sleep(1)

    serp_url = f"https://www.google.com/search?q={requests.utils.quote(query)}&num={num_results}"

    try:
        response = requests.post(
            BD_ENDPOINT,
            headers={
                "Authorization": f"Bearer {API_TOKEN}",
                "Content-Type": "application/json"
            },
            json={"zone": ZONE, "url": serp_url, "format": "raw"},
            timeout=60
        )
        response.raise_for_status()
        html = response.text

        # Parse Google results — try multiple selector patterns
        from bs4 import BeautifulSoup
        import re
        soup = BeautifulSoup(html, "lxml")
        results = []

        # Pattern 1: standard div.g blocks
        for g in soup.select("div.g, div[data-sokoban-container], div.Gx5Zad")[:num_results]:
            title_el = g.select_one("h3")
            link_el = g.select_one("a[href]")
            snippet_el = g.select_one("[data-sncf], .VwiC3b, .yXK7lf, .s3v9rd, span.aCOpRe")
            if title_el and link_el and link_el.get("href", "").startswith("http"):
                results.append({
                    "title": title_el.get_text(strip=True),
                    "url": link_el["href"],
                    "snippet": snippet_el.get_text(strip=True) if snippet_el else "",
                })

        # Pattern 2: extract all hrefs + h3 text if pattern 1 fails
        if not results:
            links = soup.find_all("a", href=re.compile(r"^https?://(?!www\.google)"))
            for a in links[:num_results]:
                h3 = a.find("h3")
                if h3:
                    results.append({
                        "title": h3.get_text(strip=True),
                        "url": a["href"],
                        "snippet": "",
                    })

        cache_path.write_text(json.dumps({"query": query, "results": results}))
        print(f"[serp] {len(results)} results for '{query}'")
        return results

    except Exception as e:
        print(f"[error] SERP query failed for '{query}': {e}")
        raise


if __name__ == "__main__":
    print("=== Testing fetch_url ===")
    html = fetch_url("https://example.com", scraper_name="test")
    print(f"✅ Got {len(html)} chars\nFirst 300:\n{html[:300]}\n")

    print("\n=== Testing fetch_serp ===")
    results = fetch_serp("corporate yoga wellness San Francisco 2026", num_results=5)
    for r in results:
        print(f"  - {r['title']} | {r['url']}")
