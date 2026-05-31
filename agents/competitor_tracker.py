"""
competitor_tracker.py — LangChain agent that analyses scraped competitor listings
to identify price trends, popular bundles, and market gaps.
"""

import os
import json
import re
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

llm = ChatAnthropic(
    model="claude-haiku-4-5",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

SYSTEM_PROMPT = """You are a competitive intelligence analyst for the wellness industry.

You will receive scraped listings from platforms like ClassPass and Eventbrite.
Analyse them and return a JSON object with this exact structure:

{
  "avg_price": "string describing average price/credit range",
  "price_range": {"min": "string", "max": "string"},
  "top_bundles": ["list of popular service combinations you notice"],
  "market_gaps": ["list of underserved niches or missing offerings"],
  "rising_categories": ["wellness categories showing high demand signals"],
  "declining_categories": ["categories with low engagement or reviews"],
  "recommendations": ["3-5 actionable recommendations for a wellness operator"],
  "summary": "2-3 sentence executive summary of the competitive landscape"
}

Return ONLY valid JSON. No markdown, no explanation.
"""



def _parse_json(text: str):
    """Strip markdown code fences and parse JSON."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text.strip())

class CompetitorTracker:
    """Analyses competitor listings to surface pricing intelligence and market gaps."""

    def analyze_competitors(self, listings: list[dict]) -> dict:
        """
        Takes scraped ClassPass/Eventbrite listings and returns competitive analysis.

        Args:
            listings: List of Scraped Signal dicts from classpass or eventbrite scrapers.

        Returns:
            Dict with avg_price, price_range, top_bundles, market_gaps,
            rising_categories, declining_categories, recommendations, summary.
        """
        if not listings:
            return {"error": "No listings provided"}

        # Extract just the data payloads
        data_points = [s.get("data", {}) for s in listings]

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Analyse these {len(data_points)} competitor listings:\n\n{json.dumps(data_points, indent=2)}")
        ]

        try:
            response = llm.invoke(messages)
            analysis = _parse_json(response.content)
            print(f"[competitor_tracker] Analysis complete. Found {len(analysis.get('market_gaps', []))} market gaps.")
            return analysis

        except (json.JSONDecodeError, Exception) as e:
            print(f"[competitor_tracker] Error: {e}")
            return {"error": str(e), "raw_response": response.content if 'response' in dir() else ""}


if __name__ == "__main__":
    mock_listings = [
        {
            "source": "classpass",
            "url": "https://classpass.com",
            "timestamp": "2026-05-30T10:00:00Z",
            "data": {"name": "Zen Yoga SF", "price": "12 credits", "rating": "4.8", "review_count": "220 reviews"}
        },
        {
            "source": "classpass",
            "url": "https://classpass.com",
            "timestamp": "2026-05-30T10:00:00Z",
            "data": {"name": "Breathwork Collective", "price": "20 credits", "rating": "4.9", "review_count": "98 reviews"}
        },
        {
            "source": "eventbrite",
            "url": "https://eventbrite.com",
            "timestamp": "2026-05-30T10:00:00Z",
            "data": {"title": "Corporate Mindfulness Half-Day Retreat", "price": "$85", "organizer": "MindfulWork"}
        },
        {
            "source": "eventbrite",
            "url": "https://eventbrite.com",
            "timestamp": "2026-05-30T10:00:00Z",
            "data": {"title": "Sound Bath + Meditation Evening", "price": "$35", "organizer": "Sound Sanctuary"}
        },
    ]

    tracker = CompetitorTracker()
    result = tracker.analyze_competitors(mock_listings)
    print(json.dumps(result, indent=2))
