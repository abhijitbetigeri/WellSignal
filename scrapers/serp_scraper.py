"""
serp_scraper.py — Uses Bright Data SERP API to detect wellness demand signals
via Google search results. Tracks trending topics and rising interest categories.
"""

from datetime import datetime, timezone
try:
    from scrapers.base_scraper import fetch_serp
except ModuleNotFoundError:
    from base_scraper import fetch_serp

DEMAND_QUERIES = [
    "corporate breathwork wellness program 2026",
    "yoga retreat corporate team building",
    "employee meditation program ROI",
    "wellness retreat bundled package",
    "personalized coaching corporate wellness",
    "dance fitness employee wellbeing",
    "travel wellness retreat booking platform",
]


def search_wellness_demand(query: str, num_results: int = 10) -> list[dict]:
    """
    Searches Google via Bright Data SERP API for a wellness demand query.

    Args:
        query: Search query string.
        num_results: Number of search results to return.

    Returns:
        List of Scraped Signal dicts with SERP result data.
    """
    raw_results = fetch_serp(query, num_results=num_results)

    signals = []
    for i, result in enumerate(raw_results):
        signal = {
            "source": "serp",
            "url": result.get("url", result.get("link", "")),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {
                "title": result.get("title", ""),
                "snippet": result.get("description", result.get("snippet", "")),
                "position": i + 1,
                "query": query,
            }
        }
        signals.append(signal)

    print(f"[serp] Found {len(signals)} results for '{query}'")
    return signals


def scan_demand_signals(queries: list[str] = None) -> list[dict]:
    """
    Runs multiple demand queries to build a comprehensive wellness demand picture.

    Args:
        queries: List of query strings. Defaults to DEMAND_QUERIES.

    Returns:
        Combined list of Scraped Signal dicts from all queries.
    """
    if queries is None:
        queries = DEMAND_QUERIES

    all_signals = []
    for query in queries:
        try:
            signals = search_wellness_demand(query)
            all_signals.extend(signals)
        except Exception as e:
            print(f"[serp] Skipping query '{query}': {e}")

    return all_signals


if __name__ == "__main__":
    results = search_wellness_demand("corporate breathwork wellness program 2026")
    for r in results[:5]:
        print(r)
