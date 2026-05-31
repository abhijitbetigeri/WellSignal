"""
luma_scraper.py — Fetches wellness events from Luma (lu.ma) via their
public Discover API. No scraping needed — clean structured JSON responses.
"""

import json
import time
import hashlib
import requests
from datetime import datetime, timezone
from pathlib import Path

CACHE_DIR = Path("cache")
LUMA_API = "https://api.lu.ma/discover/get-paginated-events"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "WellSignal/1.0 (hackathon project)"
}

# Wellness keyword queries to run against Luma's API
WELLNESS_QUERIES = [
    "yoga",
    "meditation",
    "breathwork",
    "wellness retreat",
    "mindfulness",
    "sound healing",
    "somatic",
    "coaching wellness",
]


def _get_cache_path(key: str) -> Path:
    key_hash = hashlib.md5(key.encode()).hexdigest()
    path = CACHE_DIR / "luma"
    path.mkdir(parents=True, exist_ok=True)
    return path / f"{key_hash}.json"


def _parse_event(item: dict) -> dict:
    """Parse a Luma API event entry into a clean dict."""
    ev = item.get("event", {})
    ticket_info = item.get("ticket_info", {}) or {}
    calendar = item.get("calendar", {}) or {}
    hosts = item.get("hosts", []) or []

    host_names = [h.get("name", "") for h in hosts if h.get("name")]
    is_free = ticket_info.get("is_free", True)
    price_cents = ticket_info.get("price")
    # price_cents can be a dict or int depending on API version
    if isinstance(price_cents, dict):
        price_cents = price_cents.get("cents") or price_cents.get("amount")
    price_str = "Free" if is_free or not price_cents else f"${int(price_cents) / 100:.0f}"

    return {
        "name": ev.get("name", "Unknown"),
        "start_at": item.get("start_at", ev.get("start_at", "N/A")),
        "end_at": ev.get("end_at", "N/A"),
        "location_type": ev.get("location_type", "N/A"),   # offline / online
        "price": price_str,
        "guest_count": item.get("guest_count", 0),
        "organizer": calendar.get("name") or (host_names[0] if host_names else "N/A"),
        "description": (ev.get("description_short") or "")[:300],
        "url": f"https://lu.ma/{ev.get('url', item.get('api_id', ''))}",
        "tags": ev.get("tags", []),
    }


def scrape_luma_query(query: str, limit: int = 20) -> list[dict]:
    """
    Fetches Luma events matching a keyword query via the Discover API.

    Args:
        query: Wellness keyword e.g. "yoga", "breathwork", "wellness retreat".
        limit: Max events to fetch.

    Returns:
        List of Scraped Signal dicts with Luma event data.
    """
    cache_path = _get_cache_path(f"query:{query}")

    if cache_path.exists():
        print(f"[cache hit] luma query: {query}")
        events = json.loads(cache_path.read_text()).get("events", [])
    else:
        print(f"[luma fetching] query: {query}")
        time.sleep(0.5)

        try:
            resp = requests.get(
                LUMA_API,
                params={"query": query, "pagination_limit": limit},
                headers=HEADERS,
                timeout=20
            )
            resp.raise_for_status()
            entries = resp.json().get("entries", [])
            events = [_parse_event(e) for e in entries]
            cache_path.write_text(json.dumps({"events": events}))

        except Exception as e:
            print(f"[luma] API error for '{query}': {e}")
            return []

    signals = [
        {
            "source": "luma",
            "url": event.get("url", "https://lu.ma"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": event
        }
        for event in events
    ]

    print(f"[luma] Found {len(signals)} events for query='{query}'")
    return signals


def scrape_luma_wellness(queries: list[str] = None, limit_per_query: int = 10) -> list[dict]:
    """
    Fetches wellness events from Luma across multiple keyword queries.
    Deduplicates by event URL.

    Args:
        queries: List of keyword queries. Defaults to WELLNESS_QUERIES.
        limit_per_query: Max events per query (keep low to save API calls).

    Returns:
        Deduplicated list of Scraped Signal dicts.
    """
    if queries is None:
        queries = WELLNESS_QUERIES

    all_signals = []
    seen_urls = set()

    for query in queries:
        try:
            signals = scrape_luma_query(query, limit=limit_per_query)
            for s in signals:
                if s["url"] not in seen_urls:
                    seen_urls.add(s["url"])
                    all_signals.append(s)
        except Exception as e:
            print(f"[luma] Skipping query '{query}': {e}")

    print(f"[luma] Total unique wellness events: {len(all_signals)}")
    return all_signals


# Alias for backward compatibility with api/main.py
def scrape_luma(location_slug: str = "sf", keyword: str = None) -> list[dict]:
    """
    Convenience wrapper — fetches wellness events from Luma.
    location_slug is accepted for interface consistency but Luma API
    uses keyword search, not location filtering.

    Args:
        location_slug: Ignored (kept for interface parity with other scrapers).
        keyword: Wellness keyword to search. Defaults to broad wellness queries.

    Returns:
        List of Scraped Signal dicts.
    """
    if keyword:
        return scrape_luma_query(keyword)
    return scrape_luma_wellness()


if __name__ == "__main__":
    print("=== Luma: yoga ===")
    yoga = scrape_luma_query("yoga", limit=5)
    for s in yoga:
        d = s["data"]
        print(f"  {d['name']} | {d['start_at'][:10]} | {d['price']} | guests: {d['guest_count']}")

    print("\n=== Luma: breathwork ===")
    bw = scrape_luma_query("breathwork", limit=5)
    for s in bw:
        d = s["data"]
        print(f"  {d['name']} | {d['start_at'][:10]} | {d['price']} | {d['location_type']}")

    print("\n=== Luma: wellness retreat ===")
    wr = scrape_luma_query("wellness retreat", limit=5)
    for s in wr:
        d = s["data"]
        print(f"  {d['name']} | {d['start_at'][:10]} | {d['price']} | organizer: {d['organizer']}")
