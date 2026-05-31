"""
signal_classifier.py — LangChain agent that classifies and scores scraped
wellness signals by type, urgency, geography, and wellness category.
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

SYSTEM_PROMPT = """You are a GTM intelligence analyst specializing in the wellness industry.

You will receive a list of web signals scraped from sources like ClassPass, Eventbrite,
Reddit, LinkedIn, and Google. For each signal, classify it and return enriched JSON.

For each signal, add these fields:
- signal_type: one of "demand_spike" | "competitor_move" | "corporate_buyer" | "review_trend" | "general"
- urgency: one of "high" | "medium" | "low"
- geography: extracted city/region or "remote" or "unknown"
- wellness_category: one of "yoga" | "meditation" | "coaching" | "retreat" | "dance" | "fitness" | "breathwork" | "travel_wellness" | "other"
- summary: one sentence describing why this signal matters for a wellness operator or HR team

Return ONLY a valid JSON array. No explanation, no markdown, just the JSON array.
"""



def _strip_html(text: str) -> str:
    """Strip HTML tags from a string."""
    if not text or "<" not in str(text):
        return text
    try:
        from bs4 import BeautifulSoup
        return BeautifulSoup(str(text), "lxml").get_text(separator=" ", strip=True)
    except Exception:
        import re
        return re.sub(r"<[^>]+>", " ", str(text)).strip()


def _clean_signal_data(data: dict) -> dict:
    """Recursively strip HTML from all string values in a signal data dict."""
    cleaned = {}
    for k, v in data.items():
        if isinstance(v, str):
            cleaned[k] = _strip_html(v)
        elif isinstance(v, dict):
            cleaned[k] = _clean_signal_data(v)
        elif isinstance(v, list):
            cleaned[k] = [_strip_html(i) if isinstance(i, str) else i for i in v]
        else:
            cleaned[k] = v
    return cleaned


def _parse_json(text: str):
    """Strip markdown code fences and parse JSON."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text.strip())

class SignalClassifier:
    """Classifies raw scraped signals using Claude LLM."""

    def classify(self, signals: list[dict]) -> list[dict]:
        """
        Enriches a list of scraped signals with classification metadata.

        Args:
            signals: List of Scraped Signal dicts from any scraper.

        Returns:
            List of signals enriched with signal_type, urgency, geography,
            wellness_category, and summary fields.
        """
        if not signals:
            return []

        # Trim signals to just the data payload for LLM efficiency
        # Strip HTML from all string fields before sending to Claude
        trimmed = [
            {
                "source": s.get("source"),
                "url": s.get("url"),
                "data": _clean_signal_data(s.get("data", {}))
            }
            for s in signals
        ]

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Classify these {len(trimmed)} signals:\n\n{json.dumps(trimmed, indent=2)}")
        ]

        try:
            response = llm.invoke(messages)
            classified = _parse_json(response.content)

            # Merge classification back into original signals
            enriched = []
            for i, original in enumerate(signals):
                merged = {**original}
                if i < len(classified):
                    merged.update({
                        "signal_type": classified[i].get("signal_type", "general"),
                        "urgency": classified[i].get("urgency", "low"),
                        "geography": classified[i].get("geography", "unknown"),
                        "wellness_category": classified[i].get("wellness_category", "other"),
                        "summary": classified[i].get("summary", ""),
                    })
                enriched.append(merged)

            print(f"[classifier] Classified {len(enriched)} signals")
            return enriched

        except (json.JSONDecodeError, Exception) as e:
            print(f"[classifier] Error: {e}")
            return signals  # return unclassified on failure


if __name__ == "__main__":
    mock_signals = [
        {
            "source": "reddit",
            "url": "https://reddit.com/r/wellness/post/abc",
            "timestamp": "2026-05-30T10:00:00Z",
            "data": {
                "title": "Anyone tried bundling breathwork + cold plunge for corporate teams?",
                "upvotes": "342",
                "comment_count": "87",
                "subreddit": "wellness"
            }
        },
        {
            "source": "linkedin",
            "url": "https://linkedin.com/jobs/view/123",
            "timestamp": "2026-05-30T10:00:00Z",
            "data": {
                "job_title": "Head of Employee Wellbeing",
                "company_name": "Stripe",
                "location": "San Francisco, CA",
                "posted_date": "2026-05-28"
            }
        },
        {
            "source": "classpass",
            "url": "https://classpass.com/search?q=yoga&location=san-francisco",
            "timestamp": "2026-05-30T10:00:00Z",
            "data": {
                "name": "The Breathing Room SF",
                "price": "18 credits",
                "rating": "4.9",
                "review_count": "312 reviews"
            }
        }
    ]

    classifier = SignalClassifier()
    results = classifier.classify(mock_signals)
    for r in results:
        print(json.dumps(r, indent=2))
