"""
classpass_scraper.py — Scrapes ClassPass listings for competitor pricing
and wellness bundle intelligence.
"""

from datetime import datetime, timezone
from bs4 import BeautifulSoup
try:
    from scrapers.base_scraper import fetch_url, _city_keywords
except ModuleNotFoundError:
    from base_scraper import fetch_url, _city_keywords


def scrape_classpass(location: str, category: str) -> list[dict]:
    """
    Scrapes ClassPass search results for a given location and wellness category.

    Args:
        location: City or area slug e.g. "san-francisco", "new-york".
        category: Wellness category e.g. "yoga", "meditation", "pilates".

    Returns:
        List of Scraped Signal dicts with ClassPass listing data.
    """
    url = f"https://classpass.com/search?q={category}&location={location}"
    html = fetch_url(url, scraper_name="classpass")
    soup = BeautifulSoup(html, "lxml")

    listings = []

    # Try multiple selector patterns — ClassPass updates its HTML frequently
    # ClassPass uses data-testid="VenueItem" and data-qa="VenueItem.*" attributes
    cards = soup.select("[data-testid='VenueItem']")

    for card in cards:
        name_el = card.select_one("[data-qa='VenueItem.name']")
        rating_el = card.select_one("[data-qa='VenueItem.rating'], [data-testid='StarRating']")
        review_el = card.select_one("[data-qa='VenueItem.review'], [data-qa='VenueItem.inline-review']")
        location_el = card.select_one("[data-qa='VenueItem.location']")
        activities_el = card.select_one("[data-qa='VenueItem.activities']")
        link_el = card.select_one("a[href]")

        # Extract clean star rating (e.g. "4.9") from rating block
        rating_text = rating_el.get_text(strip=True) if rating_el else ""
        import re
        rating_match = re.search(r"\b([45]\.\d)\b", rating_text)
        review_match = re.search(r"([\d,]+\+?)\s*\)", rating_text)

        listing = {
            "name": name_el.get_text(strip=True) if name_el else "Unknown",
            "rating": rating_match.group(1) if rating_match else "N/A",
            "review_count": review_match.group(1) if review_match else "N/A",
            "location": location_el.get_text(strip=True) if location_el else "N/A",
            "activities": activities_el.get_text(strip=True) if activities_el else "N/A",
            "price": "N/A",  # ClassPass hides exact pricing behind login
            "url": "https://classpass.com" + link_el["href"] if link_el and link_el.get("href", "").startswith("/") else (link_el["href"] if link_el else url),
        }
        listings.append(listing)

    # Location filter — drop results whose location doesn't match the requested city
    city_keywords = _city_keywords(location)
    if city_keywords:
        listings = [
            l for l in listings
            if any(kw in (l.get("location") or "").lower() for kw in city_keywords)
            or l.get("location") in ("N/A", "", None)  # keep if no location data
        ]

    signals = [
        {
            "source": "classpass",
            "url": url,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": listing
        }
        for listing in listings
    ]

    print(f"[classpass] Found {len(signals)} listings for '{category}' in '{location}'")
    return signals


if __name__ == "__main__":
    results = scrape_classpass(location="san-francisco", category="yoga")
    for r in results[:5]:
        print(r)
