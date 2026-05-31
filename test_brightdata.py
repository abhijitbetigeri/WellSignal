import os, requests
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")

def scrape_url(url: str) -> str:
    """Unlocks and returns raw HTML from any website."""
    response = requests.post(
        "https://api.brightdata.com/request",
        headers={
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "zone": "web_unlocker1",   # your zone name from Control Panel
            "url": url,
            "format": "raw"
        }
    )
    response.raise_for_status()
    return response.text

# Test it
html = scrape_url("https://www.classpass.com/search?q=yoga&location=san-francisco")
print(html[:2000])  # print first 2000 chars to confirm it works
