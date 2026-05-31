# WellSignal: Building a Real-Time GTM Intelligence Platform for Wellness with Bright Data and Claude AI

---

When I set out to build for the Bright Data Web Data UNLOCKED Hackathon, I wanted to tackle a real problem — not just a demo. The wellness industry is fragmented and surprisingly analog when it comes to sales and market intelligence. Operators run on gut feel. Corporate HR teams spend weeks researching vendors manually. Nobody has a real-time view of the market.

WellSignal changes that.

🔗 **Live Demo:** [wellsignal-nqyuy24cvkrenl9zfzuutc.streamlit.app](https://wellsignal-nqyuy24cvkrenl9zfzuutc.streamlit.app/)
💻 **GitHub:** [github.com/abhijitbetigeri/WellSignal](https://github.com/abhijitbetigeri/WellSignal)

---

## The Idea

WellSignal is a dual-sided GTM intelligence platform:

- **Wellness operators** (yoga studios, retreat centers, coaches) get live competitor pricing, event demand signals, corporate buyer radar, and auto-generated B2B outreach emails.
- **Corporate HR teams** get curated employee wellness bundles, benchmarked pricing, ROI projections, and outreach-ready content — all based on live market data.

One platform. Two customer types. Powered entirely by real-time web data.

---

## How It Works

The pipeline has four stages:

**1. Scrape** — Bright Data's Web Unlocker pulls live data from ClassPass (competitor pricing), Eventbrite (event demand), Luma (community wellness events), LinkedIn (corporate buyer signals), and Google SERP (demand trends). Every request goes through the `wellsignal_unlocker` zone, bypassing bot protection on sites that would otherwise block scrapers cold.

**2. Classify** — Each scraped signal hits a Claude Haiku agent via LangChain. It assigns a signal type (`demand_spike`, `competitor_move`, `corporate_buyer`), urgency level, wellness category, and a one-line summary. 65+ signals classified in seconds.

**3. Analyze** — A competitor analysis agent synthesizes all signals to surface market gaps, rising categories, pricing benchmarks, and strategic recommendations — grounded in what was actually scraped today, not last quarter.

**4. Bundle + Outreach** — A bundle recommender generates three ready-to-pitch service packages per query. In corporate mode, an outreach agent drafts personalized B2B emails under 150 words, referencing the specific web signals that triggered each recommendation.

The full pipeline runs in under 30 seconds.

---

## The Technical Stack

- **Bright Data** — Web Unlocker + SERP API for all data ingestion
- **Anthropic Claude** (Haiku 4.5) — Signal classification, competitor analysis, bundle generation, outreach copy
- **LangChain** — Multi-agent orchestration
- **FastAPI** — Backend API
- **Streamlit** — Live demo frontend deployed on Streamlit Cloud
- **Next.js + Tailwind CSS** — Production dashboard

---

## What I Learned

**Bright Data is not optional for this kind of project.** ClassPass blocks scrapers aggressively. LinkedIn requires residential IPs. Eventbrite's structured data is buried in JavaScript-rendered pages. Without Bright Data's Web Unlocker, the data pipeline simply doesn't exist — and without the data, the intelligence layer has nothing to work with.

**LLMs are remarkably good at synthesis, not just generation.** The most valuable output WellSignal produces isn't the outreach emails — it's the market gap analysis. Feeding 65 live signals to Claude and getting back a prioritized list of underserved opportunities felt genuinely useful, not just impressive.

**Caching is essential during development.** Every scraper writes responses to a local JSON cache keyed by URL hash. This saved hundreds of API credits during iteration and made the dev loop fast.

---

## Live Results

On a real run for yoga in San Francisco, WellSignal scraped 65 signals, identified 7 market gaps (including no hybrid in-person/digital offerings and underserved corporate lunch-break sessions), and generated 3 service bundles with pricing and pitch angles — all in one API call.

---

## Try It Yourself

The live demo is deployed on Streamlit Cloud — no setup needed:

👉 **[wellsignal-nqyuy24cvkrenl9zfzuutc.streamlit.app](https://wellsignal-nqyuy24cvkrenl9zfzuutc.streamlit.app/)**

Select **Wellness Operator** mode, enter a location and category, and hit **Analyze Market**. Or switch to **Corporate HR** mode, enter a company name and headcount, and get a full wellness program recommendation with ROI projections in under 30 seconds.

---

*Built for the Bright Data Web Data UNLOCKED Hackathon — GTM Intelligence track.*
