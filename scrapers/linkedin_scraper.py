"""
linkedin_scraper.py — Scrapes LinkedIn job listings to identify corporate
buyers actively hiring for HR/wellness roles (corporate buyer radar).
"""

from datetime import datetime, timezone
from bs4 import BeautifulSoup
try:
    from scrapers.base_scraper import fetch_url
except ModuleNotFoundError:
    from base_scraper import fetch_url

# Keywords that signal a company is actively investing in employee wellness
BUYER_SIGNAL_KEYWORDS = [
    "HR Director wellness",
    "Chief People Officer wellbeing",
    "Employee Benefits Manager",
    "Corporate Wellness Program",
    "Head of People wellness",
]


def scrape_linkedin_jobs(keyword: str, location: str) -> list[dict]:
    """
    Scrapes LinkedIn public job search results for corporate buyer signals.

    Args:
        keyword: Job title/keyword e.g. "HR Director wellness".
        location: Location to search e.g. "San Francisco", "New York".

    Returns:
        List of Scraped Signal dicts with job listing data.
    """
    keyword_slug = keyword.replace(" ", "%20")
    location_slug = location.replace(" ", "%20")
    url = f"https://www.linkedin.com/jobs/search/?keywords={keyword_slug}&location={location_slug}"

    html = fetch_url(url, scraper_name="linkedin")
    soup = BeautifulSoup(html, "lxml")

    jobs = []

    cards = (
        soup.select(".jobs-search__results-list li") or
        soup.select(".job-search-card") or
        soup.select("li[data-occludable-job-id]") or
        soup.select(".base-card")
    )

    for card in cards:
        title_el = card.select_one("h3, .base-search-card__title, [data-testid='job-title']")
        company_el = card.select_one("h4, .base-search-card__subtitle, .job-card-container__company-name")
        location_el = card.select_one(".job-search-card__location, .base-search-card__metadata")
        date_el = card.select_one("time, .job-search-card__listdate")
        link_el = card.select_one("a[href]")

        job = {
            "job_title": title_el.get_text(strip=True) if title_el else "Unknown",
            "company_name": company_el.get_text(strip=True) if company_el else "Unknown",
            "location": location_el.get_text(strip=True) if location_el else location,
            "posted_date": date_el.get("datetime", date_el.get_text(strip=True)) if date_el else "N/A",
            "job_url": link_el["href"].split("?")[0] if link_el else url,
            "search_keyword": keyword,
        }
        jobs.append(job)

    signals = [
        {
            "source": "linkedin",
            "url": url,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": job
        }
        for job in jobs
    ]

    print(f"[linkedin] Found {len(signals)} jobs for '{keyword}' in '{location}'")
    return signals


def scan_corporate_buyers(location: str) -> list[dict]:
    """
    Scans LinkedIn across all buyer signal keywords to build a corporate buyer radar.

    Args:
        location: City to scan e.g. "San Francisco".

    Returns:
        Combined list of Scraped Signal dicts from all keyword searches.
    """
    all_signals = []
    for keyword in BUYER_SIGNAL_KEYWORDS:
        try:
            signals = scrape_linkedin_jobs(keyword, location)
            all_signals.extend(signals)
        except Exception as e:
            print(f"[linkedin] Skipping keyword '{keyword}': {e}")
    return all_signals


if __name__ == "__main__":
    results = scrape_linkedin_jobs(
        keyword="Employee Benefits Manager wellness",
        location="San Francisco"
    )
    for r in results[:5]:
        print(r)
