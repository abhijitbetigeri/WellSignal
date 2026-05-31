"""
reddit_scraper.py — Fetches wellness community signals via Google SERP targeting
wellness forums and communities (Reddit blocked on trial zones).
Falls back to searching wellness discussion forums and communities.
"""

import json
import time
import hashlib
import urllib.parse
import requests
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")
ZONE = os.getenv("BRIGHTDATA_ZONE", "wellsignal_unlocker")
CACHE_DIR = Path("cache")

# Community signal queries — wellness forums, blogs, discussions
COMMUNITY_QUERIES = [
    "corporate breathwork program employee feedback forum 2026",
    "yoga meditation employee wellness benefit review discussion",
    "corporate wellness retreat ROI employee experience 2026",
    "breathwork mindfulness team building discussion",
]


def _get_cache_path(key: str) -> Path:
    key_hash = hashlib.md5(key.encode()).hexdigest()
    path = CACHE_DIR / "reddit"
    path.mkdir(parents=True, exist_ok=True)
    return path / f"{key_hash}.json"


def scrape_reddit(subreddit: str, query: str) -> list[dict]:
    """
    Fetches community wellness signals via Google SERP (Reddit blocked on trial).
    Searches wellness forums and discussion communities instead.

    Args:
        subreddit: Used as context tag for the signal (not directly scraped).
        query: Search term e.g. "corporate wellness", "breathwork benefits".

    Returns:
        List of Scraped Signal dicts with community discussion data.
    """
    cache_key = f"{subreddit}:{query}"
    cache_path = _get_cache_path(cache_key)

    if cache_path.exists():
        print(f"[cache hit] community signals: {query}")
        posts = json.loads(cache_path.read_text()).get("posts", [])
    else:
        print(f"[community searching] {query}")
        # Search Google for wellness community discussions
        search_q = f"{query} wellness community discussion experience"
        google_url = f"https://www.google.com/search?q={urllib.parse.quote(search_q)}&num=10"

        time.sleep(1)
        response = requests.post(
            "https://api.brightdata.com/request",
            headers={"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"},
            json={"zone": ZONE, "url": google_url, "format": "raw"},
            timeout=60
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        posts = []
        for a in soup.find_all("a", href=re.compile(r"^https?://")):
            h3 = a.find("h3")
            if h3:
                href = a["href"]
                if any(skip in href for skip in ["google.com", "accounts.google", "support.google"]):
                    continue
                posts.append({
                    "title": h3.get_text(strip=True),
                    "url": href,
                    "snippet": "",
                    "subreddit": subreddit,
                    "upvotes": "N/A",
                    "comment_count": "N/A",
                })

        cache_path.write_text(json.dumps({"posts": posts}))

    signals = [
        {
            "source": "reddit",
            "url": post.get("url", ""),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": post
        }
        for post in posts
    ]
    print(f"[community] Found {len(signals)} signals for '{query}'")
    return signals


def scrape_reddit_multi(query: str, subreddits: list[str] = None) -> list[dict]:
    """
    Searches community signals across multiple wellness topics.

    Args:
        query: Search term.
        subreddits: Used as context tags. Defaults to wellness categories.

    Returns:
        Combined list of Scraped Signal dicts.
    """
    categories = subreddits or ["yoga", "meditation", "wellness"]
    all_signals = []
    for cat in categories[:2]:  # limit to 2 to save credits
        try:
            signals = scrape_reddit(cat, query)
            all_signals.extend(signals)
        except Exception as e:
            print(f"[community] Skipping {cat}: {e}")
    return all_signals


if __name__ == "__main__":
    results = scrape_reddit(subreddit="wellness", query="corporate wellness program employee feedback")
    for r in results[:5]:
        print(r)
