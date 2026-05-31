"""
eventbrite_scraper.py — Scrapes Eventbrite for wellness event demand signals.
Captures event titles, prices, attendance trends by category and location.
"""

from datetime import datetime, timezone
from bs4 import BeautifulSoup
try:
    from scrapers.base_scraper import fetch_url
except ModuleNotFoundError:
    from base_scraper import fetch_url


def scrape_eventbrite(location: str, keyword: str) -> list[dict]:
    """
    Scrapes Eventbrite search results for wellness events in a given location.

    Args:
        location: City name e.g. "san-francisco", "austin", "new-york".
        keyword: Wellness keyword e.g. "yoga retreat", "breathwork", "meditation".

    Returns:
        List of Scraped Signal dicts with event data.
    """
    keyword_slug = keyword.replace(" ", "%20")
    url = f"https://www.eventbrite.com/d/{location}/{keyword_slug}/"
    html = fetch_url(url, scraper_name="eventbrite")
    soup = BeautifulSoup(html, "lxml")

    events = []
    import json as _json

    # Primary: parse structured ld+json ItemList (most reliable)
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = _json.loads(script.string)
            if data.get("@type") == "ItemList":
                for item in data.get("itemListElement", []):
                    ev = item.get("item", {})
                    events.append({
                        "title": ev.get("name", "Unknown"),
                        "date": ev.get("startDate", "N/A"),
                        "price": ev.get("offers", {}).get("price", "N/A") if isinstance(ev.get("offers"), dict) else "N/A",
                        "organizer": ev.get("organizer", {}).get("name", "N/A") if isinstance(ev.get("organizer"), dict) else "N/A",
                        "description": ev.get("description", "")[:200],
                        "url": ev.get("url", url),
                    })
        except Exception:
            pass

    # Fallback: event card elements
    if not events:
        for card in soup.select("[data-testid='event-card-tracking-layer']"):
            title_el = card.select_one("h2, h3")
            link_el = card.select_one("a[href]")
            if title_el:
                events.append({
                    "title": title_el.get_text(strip=True),
                    "date": "N/A", "price": "N/A", "organizer": "N/A",
                    "description": "",
                    "url": link_el["href"] if link_el else url,
                })

    signals = [
        {
            "source": "eventbrite",
            "url": url,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": event
        }
        for event in events
    ]

    print(f"[eventbrite] Found {len(signals)} events for '{keyword}' in '{location}'")
    return signals


if __name__ == "__main__":
    results = scrape_eventbrite(location="san-francisco", keyword="breathwork")
    for r in results[:5]:
        print(r)
