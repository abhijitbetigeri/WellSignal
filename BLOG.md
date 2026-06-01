# WellSignal: Building a Real-Time GTM Intelligence Platform for Wellness with Bright Data and Claude AI

![WellSignal Cover](WellSignal_Blog_Cover.png)

💻 **GitHub:** [github.com/abhijitbetigeri/WellSignal](https://github.com/abhijitbetigeri/WellSignal)

---

## The Problem

Wellness is no longer a niche — it spans yoga, meditation, breathwork, pilates, sound healing, nutrition coaching, mental health programs, corporate retreats, fitness, and more. The industry is massive, growing, and deeply fragmented.

Yet despite this scale, both sides of the wellness market operate almost entirely on gut feel:

**On the operator side**, wellness businesses — whether a pilates studio, a retreat center, a mindfulness coach, a breathwork facilitator, or a corporate wellness consultancy — face the same set of unanswered questions every day:

- What are competitors charging across every category and location?
- Which wellness events and formats are actually selling — and which are losing demand?
- Which companies nearby are actively hiring wellness vendors or building employee wellness programs?
- What service bundle should I pitch to land a corporate B2B contract?
- How do I write a cold outreach email that references something real and timely?

There is no single platform that answers these questions. Operators manually browse ClassPass, scroll Eventbrite, and guess. It takes hours, it's incomplete, and the picture is already stale by the time they act on it.

**On the corporate wellness side**, companies increasingly recognise that employee wellbeing directly impacts productivity, retention, and healthcare costs. But building a meaningful wellness program is hard:

- Which wellness formats actually work for employee engagement — yoga, meditation, coaching, retreats, breathwork?
- What does a fair, competitive wellness package look like across different provider types and team sizes?
- How do you evaluate and compare wellness vendors quickly, without spending weeks on calls?
- How do you make a data-backed business case for investing in employee wellness?
- Who are the right local wellness providers to partner with, and how do you approach them?

Companies end up with generic, one-size-fits-all wellness perks that employees don't use — because there was no intelligence behind the selection.

**WellSignal solves both sides simultaneously.** It is a wellness intelligence product — purpose-built to give the wellness ecosystem the real-time market data it has always lacked. It scrapes the live web across all wellness categories and formats, classifies every signal with AI, and delivers a complete GTM intelligence report in under 30 seconds.

---

## What is WellSignal?

WellSignal is a **wellness intelligence product** — a dual-sided GTM (Go-To-Market) platform built for the entire wellness ecosystem. It covers the full spectrum: yoga, meditation, breathwork, pilates, fitness, sound healing, nutrition, life coaching, corporate retreats, and employee wellness programs.

| Mode | Who it's for | What it delivers |
|------|-------------|-----------------|
| 🧘 **Wellness Operator** | Studios, coaches, retreat centers, breathwork facilitators, meditation teachers, fitness instructors, nutrition coaches, wellness consultants | Live competitor pricing across all wellness categories, event demand signals, corporate buyer radar, B2B bundle recommendations, personalized outreach emails |
| 🏢 **Corporate Wellness** | Companies, wellness committees, and People teams building employee wellness programs | Curated wellness provider bundles across all formats, benchmarked pricing, ROI projections, ready-to-send vendor outreach |

---

## System Architecture

Here is the full end-to-end architecture of WellSignal:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                                │
│           Streamlit Dashboard  /  Next.js Dashboard                 │
│     [Mode Toggle: Wellness Operator  |  Corporate HR]               │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ HTTP Request
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        FASTAPI BACKEND                               │
│                                                                      │
│   POST /operator/analyze          POST /corporate/recommend          │
└──────┬─────────────────────────────────────────────┬────────────────┘
       │                                             │
       ▼                                             ▼
┌──────────────────────┐                 ┌──────────────────────────┐
│   SCRAPING LAYER     │                 │      SCRAPING LAYER       │
│  (Bright Data)       │                 │     (Bright Data)         │
│                      │                 │                           │
│  ┌───────────────┐   │                 │  ┌─────────────────────┐  │
│  │  ClassPass    │   │                 │  │  LinkedIn Jobs      │  │
│  │  (pricing &   │   │                 │  │  (corporate buyer   │  │
│  │   listings)   │   │                 │  │   signals)          │  │
│  └───────────────┘   │                 │  └─────────────────────┘  │
│  ┌───────────────┐   │                 │  ┌─────────────────────┐  │
│  │  Eventbrite   │   │                 │  │  Google SERP        │  │
│  │  (demand &    │   │                 │  │  (demand trends,    │  │
│  │   events)     │   │                 │  │   community posts)  │  │
│  └───────────────┘   │                 │  └─────────────────────┘  │
│  ┌───────────────┐   │                 │  ┌─────────────────────┐  │
│  │  Luma         │   │                 │  │  Luma               │  │
│  │  (community   │   │                 │  │  (wellness events   │  │
│  │   events)     │   │                 │  │   & retreats)       │  │
│  └───────────────┘   │                 │  └─────────────────────┘  │
│  ┌───────────────┐   │                 └──────────────────────────┘
│  │  Google SERP  │   │
│  │  (market      │   │
│  │   trends)     │   │
│  └───────────────┘   │
└──────────────────────┘
       │                                             │
       └──────────────────┬──────────────────────────┘
                          │ Raw Signals (65+)
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     AI AGENT PIPELINE                                │
│                   (LangChain + Claude Haiku)                         │
│                                                                      │
│   Step 1: Signal Classifier                                          │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │ Input: Raw scraped data from all sources                     │  │
│   │ Output per signal:                                           │  │
│   │   - signal_type: demand_spike / competitor_move /            │  │
│   │                  corporate_buyer / review_trend              │  │
│   │   - urgency: high / medium / low                             │  │
│   │   - wellness_category: yoga / meditation / breathwork / ...  │  │
│   │   - geography: city/region extracted                         │  │
│   │   - summary: one-line human-readable insight                 │  │
│   └──────────────────────────────────────────────────────────────┘  │
│                          │                                           │
│                          ▼                                           │
│   Step 2: Competitor Tracker                                         │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │ Input: All classified signals                                │  │
│   │ Output:                                                      │  │
│   │   - avg_price & price_range across competitors               │  │
│   │   - market_gaps: what nobody is offering yet                 │  │
│   │   - rising_categories: what's gaining demand                 │  │
│   │   - declining_categories: what's losing relevance           │  │
│   │   - recommendations: 5 actionable strategic moves            │  │
│   │   - executive_summary: paragraph-level market overview       │  │
│   └──────────────────────────────────────────────────────────────┘  │
│                          │                                           │
│                          ▼                                           │
│   Step 3: Bundle Recommender                                         │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │ Input: Classified signals + competitor analysis              │  │
│   │ Output (3 bundles):                                          │  │
│   │   Operator mode:                                             │  │
│   │     - bundle_name, services[], suggested_price               │  │
│   │     - target_segment, competitor_gap, outreach_angle         │  │
│   │   Corporate mode:                                            │  │
│   │     - bundle_name, services[], price_per_employee_monthly    │  │
│   │     - target_segment, projected_roi                          │  │
│   └──────────────────────────────────────────────────────────────┘  │
│                          │                                           │
│                          ▼  (Corporate mode only)                    │
│   Step 4: Outreach Generator                                         │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │ Input: Bundles + signals + target company profile            │  │
│   │ Output (per vendor):                                         │  │
│   │   - subject, body (< 150 words)                              │  │
│   │   - target_role, target_company                              │  │
│   │   - signal_used: which web signal inspired this email        │  │
│   └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        FINAL OUTPUT                                  │
│                                                                      │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────┐  │
│   │  65+ Live    │  │  7 Market    │  │ 3 Bundle │  │ Outreach │  │
│   │  Signals     │  │  Gaps        │  │   Recs   │  │  Drafts  │  │
│   └──────────────┘  └──────────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Deep Dive: Each Component

### 1. The Scraping Layer — Powered by Bright Data

This is the foundation of everything. Without fresh, reliable data, the AI has nothing to work with.

WellSignal uses **Bright Data's Web Unlocker** — a residential proxy network that bypasses bot detection on sites like ClassPass and LinkedIn that aggressively block standard scrapers.

Every scraper follows the same pattern:

```python
def fetch_url(url: str, scraper_name: str) -> str:
    # Check local JSON cache first — never re-scrape same URL in dev
    cache_path = _get_cache_path(scraper_name, url)
    if cache_path.exists():
        return json.loads(cache_path.read_text())["html"]

    # Hit Bright Data Web Unlocker
    response = requests.post(
        "https://api.brightdata.com/request",
        headers={"Authorization": f"Bearer {API_TOKEN}"},
        json={"zone": "wellsignal_unlocker", "url": url, "format": "raw"},
        timeout=30
    )
    html = response.text
    # Cache for next time
    cache_path.write_text(json.dumps({"url": url, "html": html}))
    return html
```

Here's what each scraper collects:

| Scraper | Source | Data Collected | Why it matters |
|---------|--------|---------------|----------------|
| `classpass_scraper.py` | ClassPass | Studio names, ratings, review counts, activity types, locations | Competitor pricing & popularity benchmark |
| `eventbrite_scraper.py` | Eventbrite | Event titles, dates, prices, descriptions | Demand signals — what people are actively paying for |
| `luma_scraper.py` | Luma Discover API | Community events, prices, attendee counts | Grassroots wellness demand trends |
| `linkedin_scraper.py` | LinkedIn Jobs | Job titles, company names, hiring signals | Corporate buyer radar — who is hiring wellness roles |
| `serp_scraper.py` | Google Search | Top results, snippets for wellness queries | Broad market demand trends |
| `reddit_scraper.py` | Google → Reddit | Community discussions about wellness | Sentiment and grassroots interest signals |

Every raw response is stored as a JSON object:

```json
{
  "source": "classpass",
  "url": "https://classpass.com/studios/san-francisco/yoga",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "name": "CorePower Yoga - Mission",
    "rating": 4.8,
    "review_count": 1247,
    "location": "Mission District, SF",
    "activities": ["yoga", "hot yoga", "sculpt"]
  }
}
```

---

### 2. Signal Classifier — Claude AI Agent

Once all raw data is collected, it passes through the Signal Classifier. This is a Claude Haiku agent that reads each scraped item and enriches it with structured intelligence.

**Why classify?** Raw scraped data is noisy and inconsistent. A ClassPass listing looks very different from an Eventbrite event or a LinkedIn job post. The classifier normalizes everything into a common schema and adds meaning.

```python
class SignalClassifier:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-haiku-4-5")

    def classify(self, signals: list[dict]) -> list[dict]:
        results = []
        for signal in signals:
            prompt = f"""
            Analyze this wellness market signal and classify it:
            {json.dumps(signal['data'])}

            Return JSON with:
            - signal_type: demand_spike | competitor_move | corporate_buyer | review_trend | general
            - urgency: high | medium | low
            - wellness_category: yoga | meditation | breathwork | pilates | fitness | coaching | retreat
            - geography: extracted location string
            - summary: one-sentence insight about this signal
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            classified = self._parse_json(response.content)
            results.append({**signal, **classified})
        return results
```

**Example input → output:**

```
Input (raw Eventbrite event):
  title: "Corporate Breathwork Session - Lunch Break"
  date: "2024-02-10"
  price: "$45"
  description: "Join us for a 45-minute guided breathwork session..."

Output (classified signal):
  signal_type: "corporate_buyer"
  urgency: "high"
  wellness_category: "breathwork"
  geography: "San Francisco"
  summary: "High-demand corporate lunch breathwork event at premium price point — strong B2B signal"
```

---

### 3. Competitor Tracker — Market Gap Analysis

After all signals are classified, the Competitor Tracker agent reads the entire dataset and produces a market-level intelligence report.

This agent answers: **"What is the market doing, and where are the gaps?"**

```python
class CompetitorTracker:
    def analyze_competitors(self, signals: list[dict]) -> dict:
        prompt = f"""
        You are a wellness market analyst. Here are {len(signals)} live market signals:
        {json.dumps(signals[:20])}

        Analyze and return:
        - avg_price: average price point across offerings
        - market_gaps: list of 5-7 underserved opportunities nobody is filling
        - rising_categories: wellness categories gaining momentum
        - declining_categories: categories losing relevance
        - recommendations: 5 specific actionable strategies
        - summary: executive paragraph summarizing the market landscape
        """
```

**Example output for SF Yoga market:**

```json
{
  "avg_price": "$32/class",
  "market_gaps": [
    "No hybrid (in-person + digital) yoga offerings in SF — major gap vs national competitors",
    "Corporate lunch-break wellness sessions severely underserved despite high demand",
    "Premium pricing tier ($45-65/class) has no clear market leader in Mission District",
    "Breathwork + yoga combination classes missing from all major studios",
    "No subscription model for corporate teams at 10+ employees"
  ],
  "rising_categories": ["breathwork", "sound healing", "corporate wellness"],
  "recommendations": [
    "Launch a hybrid class model with 30% lower overhead than pure in-person",
    "Target tech companies in SoMa with lunch-break corporate packages",
    "Create a $299/month team subscription for 10-person corporate groups"
  ],
  "summary": "The SF yoga market is saturated at the mid-price tier but wide open for corporate B2B offerings..."
}
```

---

### 4. Bundle Recommender — AI-Generated Service Packages

Using the classified signals and competitor analysis, the Bundle Recommender creates three ready-to-pitch service bundles. Each bundle is grounded in real market gaps — not generic suggestions.

**Operator Mode bundle example:**

```json
{
  "bundle_name": "Corporate Lunch Wellness Sprint",
  "services": ["45-min breathwork", "guided meditation", "nutrition talk"],
  "suggested_price": "$1,200/month",
  "target_segment": "SoMa tech companies, 50-200 employees",
  "competitor_gap": "No SF studio offers a packaged corporate lunch-break program",
  "outreach_angle": "Your team gets 45 minutes back — we handle the recovery"
}
```

**Corporate HR Mode bundle example:**

```json
{
  "bundle_name": "Full Spectrum Employee Wellness",
  "services": ["weekly yoga", "monthly retreat", "1:1 coaching", "digital access"],
  "price_per_employee_monthly": 89,
  "target_segment": "200-person tech company, SF",
  "projected_roi": "Est. $534/employee/year saved in reduced absenteeism and healthcare"
}
```

---

### 5. Outreach Generator — Personalized B2B Emails

The final agent (Corporate HR mode only) writes personalized outreach emails to wellness vendors on behalf of the HR team. Each email is under 150 words and references a specific web signal that made this vendor relevant.

```json
{
  "subject": "Wellness partnership for Stripe's SF team",
  "body": "Hi Sarah,\n\nI came across your breathwork sessions on Luma — your recent corporate lunch event had a 4.9 rating with 80+ attendees.\n\nWe're building a wellness program for 200 engineers at Stripe and believe your format is a strong fit. We're looking for a monthly partner at $45-55/session...",
  "target_role": "Studio Owner",
  "target_company": "Mindful Collective SF",
  "signal_used": "Luma event: Corporate Breathwork Lunch — 82 attendees, sold out"
}
```

---

## How Bright Data Makes This Possible

Bright Data is not just a proxy tool here — it is the entire data foundation of WellSignal. Without it:

- **ClassPass** would block the scraper within 2 requests (they use advanced bot detection)
- **LinkedIn** would serve empty pages without residential IPs
- **Eventbrite** requires JavaScript rendering that standard requests cannot handle
- **Google SERP** throttles and blocks non-residential IP ranges aggressively

The `wellsignal_unlocker` zone in Bright Data's Web Unlocker handles all of this transparently. From the code's perspective, it's just an HTTP POST — Bright Data handles the residential routing, CAPTCHA bypass, and JavaScript rendering under the hood.

```
Your Code → Bright Data Web Unlocker → Residential IP → Target Website
                                     ↑
                        Handles: bot detection, JS rendering,
                                 CAPTCHA, rate limits, geo-routing
```

---

## Project File Structure

```
wellsignal/
├── streamlit_app.py          # Live demo (Streamlit Cloud)
├── requirements.txt
│
├── scrapers/                 # Bright Data scraping layer
│   ├── base_scraper.py       # Core Web Unlocker + caching logic
│   ├── classpass_scraper.py  # Competitor pricing
│   ├── eventbrite_scraper.py # Event demand signals
│   ├── luma_scraper.py       # Community events (public API)
│   ├── linkedin_scraper.py   # Corporate buyer radar
│   ├── reddit_scraper.py     # Community sentiment
│   └── serp_scraper.py       # Google demand trends
│
├── agents/                   # Claude AI agent pipeline
│   ├── signal_classifier.py  # Classifies every signal
│   ├── competitor_tracker.py # Market gap analysis
│   ├── bundle_recommender.py # Service bundle generation
│   └── outreach_generator.py # B2B email drafting
│
├── api/                      # FastAPI backend
│   └── main.py               # /operator/analyze, /corporate/recommend
│
└── frontend/                 # Next.js production dashboard
    ├── app/page.tsx
    └── components/
        ├── SignalCard.tsx
        ├── BundleCard.tsx
        ├── OutreachCard.tsx
        └── SourceBreakdown.tsx
```

---

## The Dashboard — What You See and Why

When the pipeline completes, the WellSignal dashboard surfaces four core intelligence constructs. Each one is the output of a distinct layer of the system. Here is exactly what each one means, how it is generated, and how it is displayed.

---

### 1. 📡 Signals Scraped

**What it is:**
A signal is a single live data point pulled from the web that carries a meaningful wellness market insight. It could be a ClassPass studio listing, an Eventbrite event that sold out, a LinkedIn job post from a company hiring a "Head of Wellness", or a Google search result showing rising demand for breathwork in a city.

**How it is generated:**
Every scraper (ClassPass, Eventbrite, Luma, LinkedIn, SERP, Reddit) returns a list of raw data objects. Each object goes through the Signal Classifier agent, which enriches it with:

| Field | What it means | Example |
|-------|--------------|---------|
| `signal_type` | What kind of market signal this is | `demand_spike`, `competitor_move`, `corporate_buyer`, `review_trend` |
| `urgency` | How time-sensitive this signal is | `high`, `medium`, `low` |
| `wellness_category` | Which wellness format this relates to | `yoga`, `meditation`, `breathwork`, `pilates`, `coaching`, `retreat` |
| `geography` | Where this signal is coming from | `San Francisco, CA` |
| `summary` | One-line human-readable insight | `"Sold-out corporate breathwork lunch — strong B2B demand signal"` |

**How it appears in the dashboard:**
- A **summary stats bar** at the top shows the total signal count at a glance
- A **Source Breakdown panel** shows three charts side by side:
  - *By Source* — a bar chart showing how many signals came from each platform (ClassPass, Eventbrite, Luma, SERP, LinkedIn) with a colour-coded progress bar per source
  - *By Urgency* — signals split into high / medium / low with red / yellow / green indicators
  - *Top Categories* — the most frequently occurring wellness categories across all signals (e.g. yoga × 22, breathwork × 11, meditation × 8)
- Below the breakdown, every signal renders as a **Signal Card** — a compact tile showing the source badge, wellness category, signal type icon, urgency badge, the signal title, location or date, and Claude's one-line summary

```
┌──────────────────────────────────────────────┐
│  [classpass]  [breathwork]          [high]   │
│                                              │
│  📈  CorePower Yoga — Mission District       │
│      San Francisco                           │
│      "High-rated studio with 1,200+ reviews  │
│       — strong competitor at this price pt"  │
└──────────────────────────────────────────────┘
```

**Why it matters:**
Wellness operators can instantly see which competitors are gaining traction, which events are creating demand spikes, and which companies are signalling buying intent — all in one view, sourced from live data scraped minutes ago.

---

### 2. 🎯 Market Gaps

**What it is:**
A market gap is an opportunity that exists in the wellness market but is not currently being served by any competitor. It is not an opinion or a generic suggestion — it is a conclusion drawn by Claude AI after reading all the scraped signals together and identifying what is missing.

**How it is generated:**
The Competitor Tracker agent receives all classified signals and looks at the full market picture. It asks: given what every competitor is offering, what formats are underserved? What price tiers have no leader? What corporate wellness needs are not being met by existing providers?

It returns:
- `market_gaps` — a list of 5–7 specific, actionable gaps
- `rising_categories` — wellness formats gaining momentum in the scraped data
- `declining_categories` — formats losing relevance
- `recommendations` — 5 concrete strategic moves the operator can take
- `summary` — an executive paragraph summarising the competitive landscape

**How it appears in the dashboard:**
The Analysis tab shows four panels:

- **Market Gaps** — each gap is listed with an amber diamond (◆) indicator. These are specific and grounded — not "offer better service" but "no studio in SF Mission offers a hybrid in-person + digital yoga subscription under $100/month"
- **Rising Categories** — emerald upward arrows (▲) showing which wellness formats are growing in the scraped signals
- **Recommendations** — numbered list of prioritised strategic moves, each tied to a real gap observed in the data
- **Executive Summary** — a paragraph Claude wrote synthesising the entire competitive landscape for that market

```
◆  No hybrid (in-person + digital) yoga model exists in SF Mission
◆  Corporate lunch-break sessions underserved — high demand, zero supply
◆  Premium tier ($55–75/class) has no clear market leader
▲  Breathwork rising sharply across Eventbrite and Luma events
▲  Sound healing appearing in corporate wellness job postings
```

**Why it matters:**
This is the core intelligence output of WellSignal. Instead of spending weeks doing manual competitive research, a wellness operator gets a prioritised gap list in seconds — grounded in real, live market data, not assumptions.

---

### 3. 📦 Bundles Ready

**What it is:**
A bundle is a ready-to-pitch service package — a concrete offering a wellness operator can take to a corporate client or a wellness consumer. It is not a generic template. Each bundle is designed around a specific market gap identified in the previous step, with pricing, target audience, and a pitch angle built in.

**How it is generated:**
The Bundle Recommender agent receives the classified signals and the competitor analysis. It knows what competitors are offering, what is missing, and what demand looks like. It generates exactly 3 bundles per run — one for each tier of the market opportunity.

Each bundle contains:

| Field | Operator Mode | Corporate Wellness Mode |
|-------|--------------|------------------------|
| `bundle_name` | "Corporate Lunch Wellness Sprint" | "Full Spectrum Employee Wellness" |
| `services` | List of session types included | List of wellness formats included |
| `suggested_price` | Per-session or monthly price | Per-employee per-month price |
| `target_segment` | Type of corporate client to target | Type of employee population |
| `competitor_gap` | The specific gap this bundle exploits | The unmet need this program addresses |
| `outreach_angle` | The pitch line to open a sales call | — |
| `projected_roi` | — | Expected return per employee per year |

**How it appears in the dashboard:**
Each of the 3 bundles renders as a **Bundle Card** — a full card with gradient colour coding (violet, emerald, amber) showing:
- Bundle name and price at the top
- "Includes" chip list of services
- Target segment description
- Market Gap box explaining what competitor gap this bundle addresses
- For Operator mode: a **Pitch Angle** box with the exact opening line to use in a sales conversation
- For Corporate Wellness mode: a **Projected ROI** box in green showing the expected financial return

```
┌─────────────────────────────────────────┐
│  Bundle 1                               │
│  Corporate Lunch Wellness Sprint        │
│                          $1,200/month   │
│                                         │
│  Includes                               │
│  [45-min breathwork] [meditation]       │
│  [nutrition talk]                       │
│                                         │
│  Target                                 │
│  SoMa tech companies, 50–200 employees  │
│                                         │
│  Market Gap                             │
│  No SF studio offers a packaged         │
│  corporate lunch-break program          │
│                                         │
│  Pitch Angle                            │
│  "Your team gets 45 minutes back —      │
│   we handle the recovery"               │
└─────────────────────────────────────────┘
```

**Why it matters:**
Wellness operators do not need to figure out what to sell or how to price it. WellSignal builds the package for them, based on what is actually missing in the market right now. They walk out of the dashboard ready to make a sales call.

---

### 4. ✉️ Outreach Drafts

**What it is:**
An outreach draft is a personalized B2B email, under 150 words, written by Claude AI and ready to copy and send. It is not a generic cold email template — it references a specific web signal (a Luma event, a LinkedIn job post, a SERP trend) that made this particular vendor or company relevant to contact right now.

**How it is generated:**
The Outreach Generator agent is the final step in the pipeline and runs only in Corporate Wellness mode. It takes:
- The top bundle recommendation
- The classified signals (to find real, specific references)
- A target vendor profile (company name, contact role)

It generates one email per vendor target, with:

| Field | What it contains |
|-------|-----------------|
| `subject` | A specific, non-generic subject line referencing the vendor |
| `body` | < 150 words — intro, context, ask, next step |
| `target_role` | Who the email is addressed to |
| `target_company` | Which wellness provider is being contacted |
| `signal_used` | The exact web signal that inspired this email |

**How it appears in the dashboard:**
Each outreach draft renders as an **Outreach Card** — an expandable panel showing:
- The "To:" field (role + company)
- The subject line
- The full email body, formatted and ready to read
- A signal attribution line at the bottom showing exactly which scraped signal triggered this email
- A **Copy** button — one click copies the full email (subject + body) to clipboard, ready to paste into Gmail

```
┌────────────────────────────────────────────────┐
│  To: Studio Owner @ Mindful Collective SF       │
│  Subject: Wellness partnership for Stripe's     │
│           SF team                               │
│  ─────────────────────────────────────────────  │
│  Hi Sarah,                                      │
│                                                 │
│  I came across your breathwork sessions on      │
│  Luma — your recent corporate lunch event had   │
│  a 4.9 rating with 80+ attendees.               │
│                                                 │
│  We're building a wellness program for 200      │
│  engineers at Stripe...                         │
│                                                 │
│  Signal used: Luma — Corporate Breathwork       │
│  Lunch, 82 attendees, sold out                  │
│                                    [Copy ✉]    │
└────────────────────────────────────────────────┘
```

**Why it matters:**
The hardest part of B2B wellness sales is knowing who to reach out to and what to say. WellSignal eliminates both problems — it identifies which vendors are gaining traction from live web signals, and writes a personalised email that references something real, making it far more likely to get a response than a generic template.

---

A real pipeline run for **yoga in San Francisco** produced:

| Metric | Result |
|--------|--------|
| ClassPass listings scraped | 34 studios |
| Eventbrite events | 20 events |
| Luma community events | 5 events |
| SERP demand signals | 6 results |
| **Total signals** | **65 signals** |
| Market gaps identified | 7 gaps |
| Bundles generated | 3 bundles |
| Pipeline runtime | < 30 seconds |

---

## Try It Yourself

Clone the repo and run it locally — setup takes under 5 minutes:

**Wellness Operator mode:**
1. Select `Wellness Operator`
2. Enter a location (e.g. `san-francisco`) and category (e.g. `yoga`)
3. Click **Analyze Market**
4. See live signals, market gaps, competitor analysis, and service bundles

**Corporate HR mode:**
1. Select `Corporate HR`
2. Enter company name, industry, employee count, location
3. Click **Generate Wellness Recommendations**
4. Get tailored bundles, ROI projections, and ready-to-send outreach emails

---

## What's Next

WellSignal is a hackathon project today, but the architecture maps cleanly to a real product:

- **Signal tracking over time** — trend lines instead of snapshots
- **CRM integration** — one-click push to HubSpot or Salesforce
- **More data sources** — Mindbody, Yelp reviews, Google Maps ratings
- **Automated outreach** — connect to Gmail and send directly from the dashboard

---

*Built for the Bright Data Web Data UNLOCKED Hackathon — GTM Intelligence track.*
*Stack: Bright Data · Anthropic Claude · LangChain · FastAPI · Streamlit · Next.js*
