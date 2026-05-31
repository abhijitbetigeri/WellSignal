"""
main.py — FastAPI backend for WellSignal.
Two core routes: /operator/analyze and /corporate/recommend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scrapers.classpass_scraper import scrape_classpass
from scrapers.eventbrite_scraper import scrape_eventbrite
from scrapers.luma_scraper import scrape_luma_wellness, scrape_luma_query
from scrapers.reddit_scraper import scrape_reddit_multi
from scrapers.linkedin_scraper import scan_corporate_buyers
from scrapers.serp_scraper import search_wellness_demand

from agents.signal_classifier import SignalClassifier
from agents.competitor_tracker import CompetitorTracker
from agents.bundle_recommender import BundleRecommender
from agents.outreach_generator import OutreachGenerator

app = FastAPI(
    title="WellSignal API",
    description="GTM Intelligence Platform for Wellness Operators and Corporate HR Teams",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared agent instances
classifier = SignalClassifier()
tracker = CompetitorTracker()
recommender = BundleRecommender()
generator = OutreachGenerator()


# ── Request / Response Models ────────────────────────────────────────────────

class OperatorRequest(BaseModel):
    location: str = "san-francisco"
    category: str = "yoga"
    competitors: list[str] = []

class CorporateRequest(BaseModel):
    company_name: str
    industry: str = "technology"
    employee_count: int = 100
    location: str = "San Francisco"


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "WellSignal API"}


@app.post("/operator/analyze")
def operator_analyze(req: OperatorRequest):
    """
    Full GTM intelligence pipeline for wellness operators.

    Scrapes competitor listings, demand signals, and corporate buyer radar.
    Returns classified signals, competitor analysis, and 3 bundle recommendations.

    Args:
        req: OperatorRequest with location, category, optional competitors list.

    Returns:
        Dict with signals, competitor_analysis, and bundles.
    """
    try:
        # 1. Scrape
        print(f"[/operator/analyze] Starting scrape for {req.category} in {req.location}")
        listings = scrape_classpass(req.location, req.category)
        events = scrape_eventbrite(req.location, req.category)
        luma_events = scrape_luma_query(req.category, limit=15, location=req.location)
        demand = search_wellness_demand(f"corporate {req.category} wellness program {req.location}")

        all_signals = listings + events + luma_events + demand

        # 2. Classify
        classified = classifier.classify(all_signals)

        # 3. Competitor analysis
        competitor_signals = listings + events
        analysis = tracker.analyze_competitors(competitor_signals)

        # 4. Bundle recommendations
        bundles = recommender.recommend(classified, analysis, target="operator")

        return {
            "signals": classified,
            "competitor_analysis": analysis,
            "bundles": bundles,
            "meta": {
                "location": req.location,
                "category": req.category,
                "total_signals": len(classified)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/corporate/recommend")
def corporate_recommend(req: CorporateRequest):
    """
    Full wellness recommendation pipeline for corporate HR teams.

    Scrapes wellness providers, demand trends, and benchmarks peer companies.
    Returns bundle recommendations, ROI projections, and draft outreach emails
    to shortlisted wellness vendors.

    Args:
        req: CorporateRequest with company_name, industry, employee_count, location.

    Returns:
        Dict with signals, bundles, outreach_drafts, and roi_summary.
    """
    try:
        print(f"[/corporate/recommend] Starting analysis for {req.company_name}")

        # 1. Scrape
        buyer_signals = scan_corporate_buyers(req.location)
        reddit_signals = scrape_reddit_multi(f"corporate wellness {req.industry}")
        demand_signals = search_wellness_demand(f"employee wellness program {req.industry} {req.location} 2026")
        luma_signals = scrape_luma_wellness(queries=["wellness retreat", "breathwork", "meditation", "coaching"], limit_per_query=8)

        all_signals = buyer_signals + reddit_signals + demand_signals + luma_signals

        # 2. Classify
        classified = classifier.classify(all_signals)

        # 3. Competitor analysis (use demand signals as proxy for market landscape)
        analysis = tracker.analyze_competitors(demand_signals[:10])

        # 4. Bundle recommendations (corporate mode)
        bundles = recommender.recommend(classified, analysis, target="corporate")

        # 5. Outreach drafts to potential wellness vendors (top bundle as basis)
        outreach_targets = [
            {"company_name": "Local Yoga Studio", "role": "Studio Owner"},
            {"company_name": "Mindful Coaching Co", "role": "Lead Coach"},
        ]
        outreach_drafts = []
        if bundles:
            outreach_drafts = generator.generate_batch(outreach_targets, classified, bundles[0])

        # 6. ROI summary
        monthly_investment = bundles[0].get("price_per_employee_monthly", 50) if bundles else 50
        annual_per_employee = monthly_investment * 12
        roi_summary = (
            f"At ${monthly_investment}/employee/month (${annual_per_employee:.0f}/year), "
            f"with {req.employee_count} employees, total annual investment = "
            f"${annual_per_employee * req.employee_count:,.0f}. "
            f"Based on industry benchmarks ($3.27 medical savings + $2.73 absenteeism "
            f"reduction per $1 invested), projected annual return = "
            f"${annual_per_employee * req.employee_count * 6:,.0f}."
        )

        return {
            "signals": classified,
            "bundles": bundles,
            "outreach_drafts": outreach_drafts,
            "roi_summary": roi_summary,
            "meta": {
                "company_name": req.company_name,
                "employee_count": req.employee_count,
                "location": req.location,
                "total_signals": len(classified)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
