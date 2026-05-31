"""
partiful_scraper.py — Scrapes Partiful explore pages for wellness/community
event signals. Uses Bright Data Web Unlocker to bypass JS rendering.
City pages: https://partiful.com/explore/{city_code}
"""

import re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

try:
    from scrapers.base_scraper import fetch_url, _city_keywords
except ModuleNotFoundError:
    from base_scraper import fetch_url, _city_keywords

# Map location slugs → Partiful city codes
CITY_MAP = {
    "san-francisco":  "sf",
    "sf":             "sf",
    "new-york":       "nyc",
    "nyc":            "nyc",
    "los-angeles":    "la",
    "la":             "la",
    "austin":         "austin",
    "chicago":        "chicago",
    "seattle":        "seattle",
    "miami":          "miami",
    "boston":         "boston",
    "denver":         "denver",
    "washington-dc":  "dc",
    "atlanta":        "atlanta",
    "portland":       "portland",
    "nashville":      "nashville",
    "san-diego":      "sandiego",
}

# Wellness keywords to filter relevant events
WELLNESS_KEYWORDS = [
    "yoga", "meditation", "breathwork", "wellness", "mindfulness",
    "pilates", "fitness", "retreat", "healing", "sound bath",
    "somatic", "coaching", "movement", "breath", "reiki",
    "acupuncture", "nutrition", "mental health", "spiritual",
    "dance", "stretch", "recovery", "cold plunge", "sauna",
]


def _is_wellness(text: str) -> bool:
    """Return True if event text contains wellness-related keywords."""
    t = text.lower()
    return any(kw in t for kw in WELLNESS_KEYWORDS)


def _strip_html(text: str) -> str:
    """Strip HTML tags from a string using regex."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", str(text))
    text = re.sub(r"&[a-z]+;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def scrape_partiful(location: str, category: str = "wellness", limit: int = 20) -> list[dict]:
    """
    Scrapes Partiful explore page for wellness events in a given city.

    Args:
        location: Location slug e.g. "san-francisco", "new-york", "austin".
        category: Wellness category keyword to filter events (e.g. "yoga").
        limit: Max number of events to return.

    Returns:
        List of Scraped Signal dicts with Partiful event data.
    """
    city_code = CITY_MAP.get(location.lower(), "sf")
    url = f"https://partiful.com/explore/{city_code}"
    html = fetch_url(url, scraper_name="partiful")
    soup = BeautifulSoup(html, "lxml")

    events = []

    # Partiful renders event cards as <a href="/e/..."> links
    # Each card contains title, date, location, and attendance count
    event_links = soup.find_all("a", href=re.compile(r"^/e/"))

    seen = set()
    for link in event_links:
        href = link.get("href", "")
        if href in seen:
            continue
        seen.add(href)

        full_url = f"https://partiful.com{href.split('?')[0]}"
        text_content = _strip_html(link.get_text(separator=" ", strip=True))

        if not text_content or len(text_content) < 3:
            continue

        # Try to extract structured fields from card text
        # Partiful cards typically have: title, date, location, count
        lines = [l.strip() for l in text_content.split("  ") if l.strip()]
        lines = [l for l in " ".join(lines).split("\n") if l.strip()]

        # Flatten and split by common separators
        flat = re.sub(r"\s{2,}", " | ", text_content)
        parts = [p.strip() for p in flat.split("|") if p.strip()]

        title = parts[0] if parts else text_content[:80]
        date_str = ""
        location_str = ""
        count_str = ""

        for part in parts[1:]:
            if re.search(r"\d+(am|pm)|today|tomorrow|mon|tue|wed|thu|fri|sat|sun|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec", part.lower()):
                date_str = part
            elif re.search(r"\d+\s*(interested|going|attending)", part.lower()):
                count_str = part
            elif len(part) > 2 and not date_str:
                location_str = part

        # Filter: only include wellness-relevant events
        full_text = (title + " " + text_content).lower()
        if not _is_wellness(full_text) and category.lower() not in full_text:
            continue

        events.append({
            "name": _strip_html(title),
            "date": _strip_html(date_str) or "N/A",
            "location": _strip_html(location_str) or location,
            "attendance": _strip_html(count_str) or "N/A",
            "url": full_url,
            "description": _strip_html(" ".join(parts[1:]))[:200],
        })

        if len(events) >= limit:
            break

    signals = [
        {
            "source": "partiful",
            "url": event["url"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": event,
        }
        for event in events
    ]

    print(f"[partiful] Found {len(signals)} wellness events in '{city_code}'")
    return signals


if __name__ == "__main__":
    results = scrape_partiful(location="san-francisco", category="yoga")
    for r in results[:5]:
        d = r["data"]
        print(f"  {d['name']} | {d['date']} | {d['location']} | {d['attendance']}")
