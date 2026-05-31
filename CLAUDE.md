# WellSignal — GTM Intelligence Platform for Wellness Operators

## Project Purpose
Dual-sided GTM intelligence agent powered by Bright Data live web scraping:

- **Operator Mode**: Wellness studio/retreat operators get real-time competitor
  pricing intel, demand signals, corporate buyer radar, bundle recommendations
  and auto-drafted B2B outreach emails.

- **Corporate HR Mode**: HR teams get curated wellness provider bundles for
  employees, benchmarked against competitors, with ROI projections.

## Core Tech Stack
- **Bright Data** — Web Unlocker, SERP API, Web Scraper API (all data ingestion)
- **Python 3.11+** — Primary language
- **FastAPI** — Backend API server
- **LangChain** — Multi-agent orchestration
- **Anthropic Claude API** — LLM synthesis, recommendations, outreach copy
- **BeautifulSoup4** — HTML parsing from Web Unlocker responses
- **Next.js** — Frontend (scaffold later)

## Environment Variables
All secrets go in .env only — never hardcode:
- BRIGHTDATA_API_TOKEN=
- BRIGHTDATA_ZONE=web_unlocker1
- ANTHROPIC_API_KEY=

## Project Folder Structure
```
wellsignal/
├── .env                        # Real secrets — never commit
├── .env.example                # Placeholder keys — safe to commit
├── .gitignore
├── requirements.txt
├── CLAUDE.md                   # This file
│
├── scrapers/                   # Bright Data scraping layer
│   ├── __init__.py
│   ├── base_scraper.py         # Shared Bright Data request logic + caching
│   ├── classpass_scraper.py    # Competitor pricing & wellness bundles
│   ├── eventbrite_scraper.py   # Event demand signals by category/location
│   ├── reddit_scraper.py       # Community wellness interest signals
│   ├── linkedin_scraper.py     # Corporate buyer radar (company pages)
│   └── serp_scraper.py         # Google demand trends via SERP API
│
├── agents/                     # AI intelligence layer
│   ├── __init__.py
│   ├── signal_classifier.py    # Scores & classifies scraped signals
│   ├── competitor_tracker.py   # Detects price/bundle changes over time
│   ├── bundle_recommender.py   # Recommends what to offer + at what price
│   └── outreach_generator.py   # Drafts personalized B2B outreach emails
│
├── api/                        # FastAPI backend
│   ├── __init__.py
│   └── main.py                 # Two routes: /operator/analyze, /corporate/recommend
│
└── cache/                      # Local JSON cache — never re-scrape same URL in dev
    └── .gitkeep
```

## Coding Rules — Follow These Always
1. **Cache everything**: All scraper responses must be saved to cache/{scraper_name}/{url_hash}.json
   before returning. Check cache first on every call. Never re-scrape same URL during dev.
2. **Protect credits**: Add time.sleep(1) between every Bright Data API request.
3. **Docstrings required**: Every function needs a docstring with Args and Returns.
4. **Env vars only**: Use python-dotenv. Never hardcode API keys or zone names.
5. **Error handling**: All scrapers wrap requests in try/except with clear error messages.
6. **Type hints**: Use Python type hints on all function signatures.

## Bright Data API Pattern (use this in every scraper)
```python
import os, requests, hashlib, json, time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")
ZONE = os.getenv("BRIGHTDATA_ZONE", "web_unlocker1")
CACHE_DIR = Path("cache")

def _get_cache_path(scraper_name: str, url: str) -> Path:
    url_hash = hashlib.md5(url.encode()).hexdigest()
    path = CACHE_DIR / scraper_name
    path.mkdir(parents=True, exist_ok=True)
    return path / f"{url_hash}.json"

def fetch_url(url: str, scraper_name: str = "default") -> str:
    cache_path = _get_cache_path(scraper_name, url)
    if cache_path.exists():
        return json.loads(cache_path.read_text())["html"]

    time.sleep(1)
    response = requests.post(
        "https://api.brightdata.com/request",
        headers={"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"},
        json={"zone": ZONE, "url": url, "format": "raw"},
        timeout=30
    )
    response.raise_for_status()
    html = response.text
    cache_path.write_text(json.dumps({"url": url, "html": html}))
    return html
```

## LangChain Agent Pattern (use this in every agent)
```python
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", api_key=os.getenv("ANTHROPIC_API_KEY"))
```

## Data Contracts

### Scraped Signal (output of all scrapers)
```python
{
  "source": str,        # "classpass" | "reddit" | "eventbrite" | "linkedin" | "serp"
  "url": str,
  "timestamp": str,     # ISO 8601
  "data": dict          # source-specific payload
}
```

### Bundle Recommendation (output of bundle_recommender)
```python
{
  "bundle_name": str,
  "services": list[str],
  "price_per_employee_monthly": float,
  "target_segment": str,
  "rationale": str,
  "competitor_gap": str,
  "projected_roi": str
}
```

### Outreach Email (output of outreach_generator)
```python
{
  "subject": str,
  "body": str,
  "target_company": str,
  "target_role": str,
  "signal_used": str    # what web signal triggered this
}
```

## Existing Files
- test_brightdata.py — early API connection test, keep for reference
- venv/ — Python virtual environment, always activate before running
