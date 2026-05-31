"""
outreach_generator.py — LangChain agent that drafts personalised B2B outreach
emails for wellness operators to send to corporate HR buyers.
Emails are grounded in specific web signals to feel relevant, not generic.
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

SYSTEM_PROMPT = """You are an expert B2B copywriter specialising in wellness industry outreach.

Write a short, personalised cold outreach email from a wellness operator to a corporate HR buyer.

Rules:
- Under 150 words total
- Non-salesy, warm, and human
- Must reference the specific web signal provided (e.g. job posting, Glassdoor review mention, Reddit trend)
- Subject line must be curiosity-driven, under 10 words
- End with a soft call to action (e.g. "worth a 15-min chat?")
- Do NOT use phrases like "I hope this email finds you well" or "I wanted to reach out"

Return a JSON object with this exact structure:
{
  "subject": "string",
  "body": "string (the full email body)",
  "target_company": "string",
  "target_role": "string",
  "signal_used": "string — one sentence describing the web signal that informed this email"
}

Return ONLY valid JSON. No markdown, no explanation.
"""



def _parse_json(text: str):
    """Strip markdown code fences and parse JSON."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text.strip())

class OutreachGenerator:
    """Generates personalised B2B outreach emails grounded in live web signals."""

    def generate(
        self,
        company_name: str,
        role: str,
        signals: list[dict],
        bundle: dict
    ) -> dict:
        """
        Drafts a personalised outreach email to a corporate HR buyer.

        Args:
            company_name: Target company name e.g. "Stripe".
            role: Target role e.g. "Head of Employee Wellbeing".
            signals: Classified signals related to this company or their industry.
            bundle: A Bundle Recommendation dict to reference in the email.

        Returns:
            Outreach Email dict with subject, body, target_company, target_role, signal_used.
        """
        # Pick the most relevant signal
        corporate_signals = [s for s in signals if s.get("signal_type") == "corporate_buyer"]
        best_signal = corporate_signals[0] if corporate_signals else (signals[0] if signals else {})

        context = {
            "company_name": company_name,
            "target_role": role,
            "web_signal": best_signal.get("summary", "Active hiring in employee wellbeing space"),
            "bundle_to_pitch": {
                "name": bundle.get("bundle_name", ""),
                "services": bundle.get("services", []),
                "price": bundle.get("suggested_price", bundle.get("price_per_employee_monthly", "")),
            }
        }

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Write an outreach email using this context:\n\n{json.dumps(context, indent=2)}")
        ]

        try:
            response = llm.invoke(messages)
            email = _parse_json(response.content)
            print(f"[outreach_generator] Email drafted for {company_name} — {role}")
            return email

        except (json.JSONDecodeError, Exception) as e:
            print(f"[outreach_generator] Error: {e}")
            return {}

    def generate_batch(
        self,
        targets: list[dict],
        signals: list[dict],
        bundle: dict
    ) -> list[dict]:
        """
        Generates outreach emails for multiple corporate targets.

        Args:
            targets: List of dicts with company_name and role keys.
            signals: Classified signals list.
            bundle: Bundle to pitch.

        Returns:
            List of Outreach Email dicts.
        """
        emails = []
        for target in targets:
            try:
                email = self.generate(
                    company_name=target.get("company_name", ""),
                    role=target.get("role", "HR Director"),
                    signals=signals,
                    bundle=bundle
                )
                emails.append(email)
            except Exception as e:
                print(f"[outreach_generator] Skipping {target}: {e}")
        return emails


if __name__ == "__main__":
    mock_signals = [
        {
            "source": "linkedin",
            "signal_type": "corporate_buyer",
            "urgency": "high",
            "wellness_category": "coaching",
            "geography": "San Francisco",
            "summary": "Stripe posted a Head of Employee Wellbeing role, signalling active investment in wellness programs."
        }
    ]

    mock_bundle = {
        "bundle_name": "Corporate Breathwork + Coaching Bundle",
        "services": ["Weekly breathwork sessions", "Monthly 1:1 coaching", "Quarterly team retreat"],
        "suggested_price": "$65/employee/month",
    }

    generator = OutreachGenerator()
    email = generator.generate(
        company_name="Stripe",
        role="Head of Employee Wellbeing",
        signals=mock_signals,
        bundle=mock_bundle
    )
    print(json.dumps(email, indent=2))
