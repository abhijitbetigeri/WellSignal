"""
bundle_recommender.py — LangChain agent that synthesizes classified signals
and competitor analysis into concrete wellness bundle recommendations.
Supports both operator mode and corporate HR mode.
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

OPERATOR_SYSTEM_PROMPT = """You are a GTM strategy advisor for wellness operators (yoga studios,
retreat organizers, coaches, fitness instructors).

Based on classified market signals and competitor analysis, recommend 3 wellness bundles
the operator should create and offer to corporate clients.

Return a JSON array of exactly 3 bundle objects with this structure:
[
  {
    "bundle_name": "string",
    "services": ["list of wellness services included"],
    "suggested_price": "string e.g. $299/month per team or $45/session",
    "target_segment": "string describing ideal corporate buyer",
    "timing_rationale": "string — why launch this NOW based on signals",
    "competitor_gap": "string — what gap in the market this fills",
    "outreach_angle": "string — the hook to use when pitching this bundle"
  }
]

Return ONLY valid JSON. No markdown, no explanation.
"""

CORPORATE_SYSTEM_PROMPT = """You are an employee wellness benefits advisor for HR teams.

Based on market signals and available wellness providers, recommend 3 wellness bundles
that the company should offer their employees to improve productivity and wellbeing.

Return a JSON array of exactly 3 bundle objects with this structure:
[
  {
    "bundle_name": "string",
    "services": ["list of wellness services included"],
    "price_per_employee_monthly": 0.0,
    "target_segment": "string describing which employees benefit most",
    "rationale": "string — why this bundle improves productivity/retention",
    "competitor_gap": "string — what peer companies are NOT offering that you should",
    "projected_roi": "string — estimated ROI based on $3.27 savings per $1 invested benchmark",
    "implementation_ease": "easy | medium | complex"
  }
]

Return ONLY valid JSON. No markdown, no explanation.
"""



def _parse_json(text: str):
    """Strip markdown code fences and parse JSON."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text.strip())

class BundleRecommender:
    """Generates wellness bundle recommendations for operators or corporate HR teams."""

    def recommend(
        self,
        classified_signals: list[dict],
        competitor_analysis: dict,
        target: str = "operator"
    ) -> list[dict]:
        """
        Synthesises signals into 3 actionable bundle recommendations.

        Args:
            classified_signals: Enriched signals from SignalClassifier.
            competitor_analysis: Output dict from CompetitorTracker.
            target: "operator" for wellness business owners, "corporate" for HR teams.

        Returns:
            List of 3 Bundle Recommendation dicts.
        """
        if target not in ("operator", "corporate"):
            raise ValueError("target must be 'operator' or 'corporate'")

        system_prompt = OPERATOR_SYSTEM_PROMPT if target == "operator" else CORPORATE_SYSTEM_PROMPT

        # Summarise signals for LLM context (top 10 by urgency)
        high_urgency = [s for s in classified_signals if s.get("urgency") == "high"]
        medium_urgency = [s for s in classified_signals if s.get("urgency") == "medium"]
        top_signals = (high_urgency + medium_urgency)[:10]

        signal_summaries = [
            {
                "source": s.get("source"),
                "signal_type": s.get("signal_type"),
                "wellness_category": s.get("wellness_category"),
                "geography": s.get("geography"),
                "summary": s.get("summary"),
                "urgency": s.get("urgency"),
            }
            for s in top_signals
        ]

        context = {
            "signals": signal_summaries,
            "competitor_analysis": competitor_analysis
        }

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Generate 3 bundle recommendations based on:\n\n{json.dumps(context, indent=2)}")
        ]

        try:
            response = llm.invoke(messages)
            bundles = _parse_json(response.content)
            print(f"[bundle_recommender] Generated {len(bundles)} bundles for target='{target}'")
            return bundles

        except (json.JSONDecodeError, Exception) as e:
            print(f"[bundle_recommender] Error: {e}")
            return []


if __name__ == "__main__":
    mock_signals = [
        {
            "source": "reddit", "signal_type": "demand_spike", "urgency": "high",
            "wellness_category": "breathwork", "geography": "San Francisco",
            "summary": "High community interest in corporate breathwork bundles spiking this week."
        },
        {
            "source": "linkedin", "signal_type": "corporate_buyer", "urgency": "high",
            "wellness_category": "coaching", "geography": "San Francisco",
            "summary": "Stripe posted Head of Employee Wellbeing role — active buyer signal."
        },
    ]

    mock_analysis = {
        "avg_price": "15-20 ClassPass credits",
        "market_gaps": ["No corporate-specific breathwork packages", "Lack of bundled retreat + coaching offers"],
        "rising_categories": ["breathwork", "personalized coaching"],
        "recommendations": ["Launch corporate breathwork package", "Bundle coaching with retreats"]
    }

    recommender = BundleRecommender()

    print("\n=== OPERATOR BUNDLES ===")
    operator_bundles = recommender.recommend(mock_signals, mock_analysis, target="operator")
    print(json.dumps(operator_bundles, indent=2))

    print("\n=== CORPORATE HR BUNDLES ===")
    corporate_bundles = recommender.recommend(mock_signals, mock_analysis, target="corporate")
    print(json.dumps(corporate_bundles, indent=2))
