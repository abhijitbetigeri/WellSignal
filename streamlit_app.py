"""
WellSignal — Streamlit Demo
GTM Intelligence Platform for Wellness Operators & Corporate HR Teams
"""

import streamlit as st
import sys
import os

# ── Path setup ───────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WellSignal — GTM Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Dark background */
  .stApp { background-color: #0a0a0f; color: #ffffff; }
  section[data-testid="stSidebar"] { background-color: #0d0d14; }

  /* Hide Streamlit branding */
  #MainMenu, footer, header { visibility: hidden; }

  /* Metric cards */
  div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 16px;
  }
  div[data-testid="metric-container"] label { color: rgba(255,255,255,0.5) !important; }
  div[data-testid="metric-container"] div { color: #ffffff !important; }

  /* Inputs */
  .stTextInput input, .stSelectbox select {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #fff !important;
  }

  /* Buttons */
  .stButton > button {
    background: linear-gradient(135deg, #8b5cf6, #10b981);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    padding: 10px 28px;
    width: 100%;
    font-size: 15px;
  }
  .stButton > button:hover { opacity: 0.88; }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: rgba(255,255,255,0.5);
    font-weight: 600;
  }
  .stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.12) !important;
    color: white !important;
  }

  /* Cards */
  .ws-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
  }
  .ws-signal-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 8px;
  }
  .badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 99px;
    font-size: 11px;
    font-weight: 700;
    margin-right: 4px;
  }
  .badge-violet  { background: rgba(139,92,246,0.2);  color: #a78bfa; }
  .badge-emerald { background: rgba(16,185,129,0.2);  color: #34d399; }
  .badge-amber   { background: rgba(245,158,11,0.2);  color: #fbbf24; }
  .badge-red     { background: rgba(239,68,68,0.2);   color: #f87171; }
  .badge-blue    { background: rgba(59,130,246,0.2);  color: #60a5fa; }
  .badge-pink    { background: rgba(236,72,153,0.2);  color: #f472b6; }
  .badge-cyan    { background: rgba(6,182,212,0.2);   color: #22d3ee; }
  .badge-orange  { background: rgba(249,115,22,0.2);  color: #fb923c; }

  .urgency-high   { background: rgba(239,68,68,0.15);   color: #f87171; border: 1px solid rgba(239,68,68,0.35); }
  .urgency-medium { background: rgba(234,179,8,0.15);   color: #fbbf24; border: 1px solid rgba(234,179,8,0.35); }
  .urgency-low    { background: rgba(34,197,94,0.15);   color: #4ade80; border: 1px solid rgba(34,197,94,0.35); }

  h1, h2, h3 { color: #ffffff !important; }
  p, li { color: rgba(255,255,255,0.75); }
  hr { border-color: rgba(255,255,255,0.08); }
</style>
""", unsafe_allow_html=True)

# ── Source / urgency color maps ───────────────────────────────────────────────
SOURCE_BADGE = {
    "classpass":  "badge-violet",
    "eventbrite": "badge-orange",
    "luma":       "badge-pink",
    "partiful":   "badge-amber",
    "reddit":     "badge-red",
    "linkedin":   "badge-blue",
    "serp":       "badge-cyan",
}
TYPE_ICONS = {
    "demand_spike": "📈", "competitor_move": "🎯",
    "corporate_buyer": "🏢", "review_trend": "⭐", "general": "📡",
}

# ── Header ────────────────────────────────────────────────────────────────────
col_logo, col_live = st.columns([6, 1])
with col_logo:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:4px;">
      <div style="width:40px;height:40px;border-radius:10px;
                  background:linear-gradient(135deg,#8b5cf6,#10b981);
                  display:flex;align-items:center;justify-content:center;
                  font-size:18px;font-weight:900;color:white;">W</div>
      <div>
        <div style="font-size:22px;font-weight:800;color:white;line-height:1.1;">WellSignal</div>
        <div style="font-size:11px;color:rgba(255,255,255,0.4);">
          GTM Intelligence · Bright Data + Claude AI
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
with col_live:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:6px;padding-top:8px;justify-content:flex-end;">
      <div style="width:8px;height:8px;border-radius:50%;background:#10b981;
                  animation:pulse 2s infinite;"></div>
      <span style="font-size:12px;color:rgba(255,255,255,0.4);">Live data</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin:8px 0 20px 0;'>", unsafe_allow_html=True)

# ── Mode toggle ───────────────────────────────────────────────────────────────
mode = st.radio(
    "Mode",
    ["🧘 Wellness Operator", "🏢 Corporate HR"],
    horizontal=True,
    label_visibility="collapsed",
)
is_operator = mode.startswith("🧘")

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Input form ────────────────────────────────────────────────────────────────
LOCATIONS = {
    "San Francisco, CA":  "san-francisco",
    "New York, NY":       "new-york",
    "Los Angeles, CA":    "los-angeles",
    "Austin, TX":         "austin",
    "Chicago, IL":        "chicago",
    "Seattle, WA":        "seattle",
    "Miami, FL":          "miami",
    "Denver, CO":         "denver",
    "Boston, MA":         "boston",
    "Washington, DC":     "washington-dc",
    "Atlanta, GA":        "atlanta",
    "Portland, OR":       "portland",
    "Nashville, TN":      "nashville",
    "San Diego, CA":      "san-diego",
}

CORP_LOCATIONS = [
    "San Francisco, CA", "New York, NY", "Los Angeles, CA", "Austin, TX",
    "Chicago, IL", "Seattle, WA", "Miami, FL", "Denver, CO", "Boston, MA",
    "Washington, DC", "Atlanta, GA", "Portland, OR", "Nashville, TN", "San Diego, CA",
]

with st.container():
    if is_operator:
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            location_label = st.selectbox("Location", list(LOCATIONS.keys()), index=0)
            location = LOCATIONS[location_label]
        with c2:
            category = st.selectbox("Wellness Category",
                ["yoga", "meditation", "breathwork", "pilates", "dance", "coaching", "retreat", "fitness"])
        with c3:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            run = st.button("🔍 Analyze Market")
    else:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            company = st.text_input("Company Name", value="Stripe", placeholder="Stripe")
        with c2:
            industry = st.text_input("Industry", value="technology", placeholder="technology")
        with c3:
            employees = st.text_input("Employees", value="200", placeholder="200")
        with c4:
            corp_location = st.selectbox("Location", CORP_LOCATIONS, index=0)
        run = st.button("🏢 Generate Wellness Recommendations")

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run:
    with st.spinner("⏳ Scraping live data via Bright Data..."):
        try:
            from scrapers.classpass_scraper import scrape_classpass
            from scrapers.eventbrite_scraper import scrape_eventbrite
            from scrapers.luma_scraper import scrape_luma_wellness, scrape_luma_query
            from scrapers.partiful_scraper import scrape_partiful
            from scrapers.reddit_scraper import scrape_reddit_multi
            from scrapers.linkedin_scraper import scan_corporate_buyers
            from scrapers.serp_scraper import search_wellness_demand
            from agents.signal_classifier import SignalClassifier
            from agents.competitor_tracker import CompetitorTracker
            from agents.bundle_recommender import BundleRecommender
            from agents.outreach_generator import OutreachGenerator

            classifier  = SignalClassifier()
            tracker     = CompetitorTracker()
            recommender = BundleRecommender()
            generator   = OutreachGenerator()

            if is_operator:
                st.toast("Scraping ClassPass, Eventbrite, Luma, SERP...", icon="🌐")
                listings    = scrape_classpass(location, category)
                events      = scrape_eventbrite(location, category)
                luma_events = scrape_luma_query(category, limit=15, location=location)
                demand      = search_wellness_demand(f"corporate {category} wellness program {location}")
                partiful_events = scrape_partiful(location, category)
                all_signals = listings + events + luma_events + partiful_events + demand

                st.toast("Classifying signals with Claude AI...", icon="🤖")
                classified  = classifier.classify(all_signals)
                analysis    = tracker.analyze_competitors(listings + events)
                bundles     = recommender.recommend(classified, analysis, target="operator")

                st.session_state["result"] = {
                    "mode": "operator", "signals": classified,
                    "analysis": analysis, "bundles": bundles, "outreach": [],
                    "roi_summary": None,
                }
            else:
                st.toast("Scraping LinkedIn, SERP, Luma wellness signals...", icon="🌐")
                buyer_signals  = scan_corporate_buyers(corp_location)
                reddit_signals = scrape_reddit_multi(f"corporate wellness {industry}")
                demand_signals = search_wellness_demand(f"employee wellness program {industry} {corp_location} 2026")
                luma_signals   = scrape_luma_wellness(
                    queries=["wellness retreat", "breathwork", "meditation", "coaching"],
                    limit_per_query=8)
                all_signals    = buyer_signals + reddit_signals + demand_signals + luma_signals

                st.toast("Classifying signals & generating bundles...", icon="🤖")
                classified = classifier.classify(all_signals)
                analysis   = tracker.analyze_competitors(demand_signals[:10])
                bundles    = recommender.recommend(classified, analysis, target="corporate")

                outreach_targets = [
                    {"company_name": "Local Yoga Studio",  "role": "Studio Owner"},
                    {"company_name": "Mindful Coaching Co", "role": "Lead Coach"},
                ]
                outreach_drafts = generator.generate_batch(outreach_targets, classified, bundles[0]) if bundles else []

                emp = int(employees) if employees.isdigit() else 100
                monthly = bundles[0].get("price_per_employee_monthly", 50) if bundles else 50
                annual  = monthly * 12
                roi_summary = (
                    f"At ${monthly}/employee/month (${annual}/year), "
                    f"with {emp} employees, total annual investment = ${annual * emp:,.0f}. "
                    f"Projected annual return (6× ROI benchmark) = ${annual * emp * 6:,.0f}."
                )

                st.session_state["result"] = {
                    "mode": "corporate", "signals": classified,
                    "analysis": analysis, "bundles": bundles,
                    "outreach": outreach_drafts, "roi_summary": roi_summary,
                }

        except Exception as e:
            st.error(f"❌ {e}")
            st.stop()

# ── Results ───────────────────────────────────────────────────────────────────
if "result" in st.session_state:
    res      = st.session_state["result"]
    signals  = res["signals"]
    analysis = res["analysis"]
    bundles  = res["bundles"]
    outreach = res["outreach"]
    roi      = res["roi_summary"]
    r_mode   = res["mode"]

    # Summary stats
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📡 Signals Scraped",   len(signals))
    m2.metric("🎯 Market Gaps",       len(analysis.get("market_gaps", [])))
    m3.metric("📦 Bundles Ready",     len(bundles))
    m4.metric("✉️ Outreach Drafts",   len(outreach))

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Tabs
    tab_signals, tab_analysis, tab_bundles, tab_outreach = st.tabs([
        f"📡 Signals ({len(signals)})",
        f"🎯 Analysis",
        f"📦 Bundles ({len(bundles)})",
        f"✉️ Outreach ({len(outreach)})",
    ])

    # ── TAB: Signals ──────────────────────────────────────────────────────────
    with tab_signals:
        # Source breakdown
        from collections import Counter
        src_counts = Counter(s["source"] for s in signals)
        urg_counts = Counter(s.get("urgency", "low") for s in signals)

        sb1, sb2, sb3 = st.columns(3)
        with sb1:
            st.markdown("**By Source**")
            for src, cnt in src_counts.most_common():
                pct = int(cnt / len(signals) * 100)
                badge_cls = SOURCE_BADGE.get(src, "badge-violet")
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                  <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                    <span class="badge {badge_cls}">{src}</span>
                    <span style="color:white;font-weight:600;font-size:13px;">{cnt}</span>
                  </div>
                  <div style="height:4px;background:rgba(255,255,255,0.08);border-radius:99px;">
                    <div style="width:{pct}%;height:4px;background:#8b5cf6;border-radius:99px;"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        with sb2:
            st.markdown("**By Urgency**")
            for urg, color in [("high","#ef4444"),("medium","#eab308"),("low","#22c55e")]:
                cnt = urg_counts.get(urg, 0)
                pct = int(cnt / max(len(signals),1) * 100)
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                  <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                    <span style="color:rgba(255,255,255,0.7);font-size:13px;text-transform:capitalize;">{urg}</span>
                    <span style="color:white;font-weight:600;font-size:13px;">{cnt}</span>
                  </div>
                  <div style="height:4px;background:rgba(255,255,255,0.08);border-radius:99px;">
                    <div style="width:{pct}%;height:4px;background:{color};border-radius:99px;"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        with sb3:
            st.markdown("**Top Categories**")
            cat_counts = Counter(s.get("wellness_category","general") for s in signals if s.get("wellness_category"))
            top5 = cat_counts.most_common(5)
            max_cnt = top5[0][1] if top5 else 1
            for cat, cnt in top5:
                pct = int(cnt / max_cnt * 100)
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                  <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                    <span style="color:rgba(255,255,255,0.7);font-size:13px;text-transform:capitalize;">{cat}</span>
                    <span style="color:white;font-weight:600;font-size:13px;">{cnt}</span>
                  </div>
                  <div style="height:4px;background:rgba(255,255,255,0.08);border-radius:99px;">
                    <div style="width:{pct}%;height:4px;background:#10b981;border-radius:99px;"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        import re as _re
        import html as _html
        def _strip(t):
            """Aggressively strip all HTML tags, decode entities, then re-escape for safe HTML injection."""
            if not t:
                return ""
            t = _re.sub(r"<[^>]+>", " ", str(t))
            t = _re.sub(r"&[a-z0-9]+;", " ", t)
            t = _re.sub(r"&#\d+;", " ", t)
            t = _re.sub(r"\s+", " ", t).strip()
            return _html.escape(t)

        # ── Source filter ─────────────────────────────────────────────────────
        available_sources = sorted(set(s.get("source", "") for s in signals if s.get("source")))
        SOURCE_COLORS_MAP = {
            "classpass":  "#8b5cf6", "eventbrite": "#f97316", "luma":      "#ec4899",
            "partiful":   "#f59e0b", "reddit":     "#ef4444", "linkedin":  "#3b82f6",
            "serp":       "#06b6d4",
        }

        st.markdown("**Filter by Source**")
        filter_cols = st.columns(len(available_sources) + 1)
        selected_sources = []

        with filter_cols[0]:
            all_selected = st.checkbox("All", value=True, key="src_all")

        for idx, src in enumerate(available_sources):
            color = SOURCE_COLORS_MAP.get(src, "#6b7280")
            with filter_cols[idx + 1]:
                checked = st.checkbox(src.capitalize(), value=True, key=f"src_{src}")
                if checked:
                    selected_sources.append(src)

        # If "All" is checked or nothing selected, show everything
        if all_selected or not selected_sources:
            filtered_signals = signals
        else:
            filtered_signals = [s for s in signals if s.get("source") in selected_sources]

        st.markdown(
            f"<div style='font-size:12px;color:rgba(255,255,255,0.4);margin-bottom:12px;'>"
            f"Showing {len(filtered_signals)} of {len(signals)} signals</div>",
            unsafe_allow_html=True
        )
        st.markdown("<hr>", unsafe_allow_html=True)

        # Signal cards — 3-column grid
        cols = st.columns(3)
        for i, s in enumerate(filtered_signals):
            d       = s.get("data", {})
            label   = _strip(d.get("name") or d.get("title") or d.get("job_title") or d.get("query") or "Signal")
            sub     = _strip(d.get("location") or d.get("date") or d.get("company_name") or "")
            summ    = _strip(s.get("summary", ""))
            icon    = TYPE_ICONS.get(s.get("signal_type","general"), "📡")
            src_b   = SOURCE_BADGE.get(s.get("source",""), "badge-violet")
            urg     = s.get("urgency","")
            urg_cls = f"urgency-{urg}" if urg else ""
            cat     = s.get("wellness_category","")

            with cols[i % 3]:
                st.markdown(f"""
                <div class="ws-signal-card">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                    <div>
                      <span class="badge {src_b}">{s.get('source','')}</span>
                      {f'<span class="badge badge-emerald">{cat}</span>' if cat else ''}
                    </div>
                    {f'<span class="badge {urg_cls}" style="font-size:10px;">{urg}</span>' if urg else ''}
                  </div>
                  <div style="display:flex;gap:8px;align-items:flex-start;">
                    <span style="font-size:18px;">{icon}</span>
                    <div>
                      <p style="font-size:13px;font-weight:600;color:white;margin:0;line-height:1.35;
                                 display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">
                        {label}
                      </p>
                      {f'<p style="font-size:11px;color:rgba(255,255,255,0.4);margin:3px 0 0 0;">{sub}</p>' if sub else ''}
                      {f'<p style="font-size:11px;color:rgba(255,255,255,0.55);margin:5px 0 0 0;line-height:1.4;">{summ[:120]}...</p>' if summ else ''}
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB: Analysis ─────────────────────────────────────────────────────────
    with tab_analysis:
        if analysis.get("error"):
            st.error(analysis["error"])
        else:
            a1, a2 = st.columns(2)
            with a1:
                st.markdown("#### 🎯 Market Gaps")
                for g in analysis.get("market_gaps", []):
                    st.markdown(f"""
                    <div style="display:flex;gap:8px;align-items:flex-start;margin-bottom:8px;">
                      <span style="color:#fbbf24;margin-top:2px;">◆</span>
                      <span style="font-size:13px;color:rgba(255,255,255,0.8);">{g}</span>
                    </div>""", unsafe_allow_html=True)

            with a2:
                st.markdown("#### 📈 Rising Categories")
                for c in analysis.get("rising_categories", []):
                    st.markdown(f"""
                    <div style="display:flex;gap:8px;align-items:flex-start;margin-bottom:8px;">
                      <span style="color:#10b981;margin-top:2px;">▲</span>
                      <span style="font-size:13px;color:rgba(255,255,255,0.8);">{c}</span>
                    </div>""", unsafe_allow_html=True)

            st.markdown("#### 💡 Recommendations")
            for i, r in enumerate(analysis.get("recommendations", []), 1):
                st.markdown(f"""
                <div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:10px;">
                  <span style="background:rgba(139,92,246,0.2);color:#a78bfa;
                               font-size:11px;padding:2px 8px;border-radius:99px;
                               white-space:nowrap;margin-top:1px;">{i}</span>
                  <span style="font-size:13px;color:rgba(255,255,255,0.8);">{r}</span>
                </div>""", unsafe_allow_html=True)

            if analysis.get("summary"):
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,rgba(139,92,246,0.1),rgba(16,185,129,0.1));
                             border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:20px;margin-top:16px;">
                  <div style="font-size:11px;font-weight:700;color:rgba(255,255,255,0.4);
                               text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">
                    Executive Summary
                  </div>
                  <p style="font-size:14px;line-height:1.7;color:rgba(255,255,255,0.8);margin:0;">
                    {analysis['summary']}
                  </p>
                </div>""", unsafe_allow_html=True)

    # ── TAB: Bundles ──────────────────────────────────────────────────────────
    with tab_bundles:
        if not bundles:
            st.info("No bundles generated.")
        else:
            BUNDLE_COLORS = [
                ("rgba(139,92,246,0.15)", "#8b5cf6"),
                ("rgba(16,185,129,0.15)", "#10b981"),
                ("rgba(245,158,11,0.15)", "#f59e0b"),
            ]
            b_cols = st.columns(len(bundles))
            for i, (b, col) in enumerate(zip(bundles, b_cols)):
                bg, accent = BUNDLE_COLORS[i % 3]
                price = b.get("suggested_price") or b.get("price_per_employee_monthly")
                price_str = f"${price}/employee/mo" if isinstance(price, (int, float)) else (price or "")
                services = b.get("services", [])
                with col:
                    st.markdown(f"""
                    <div style="background:{bg};border:1px solid {accent}44;
                                border-radius:20px;padding:22px;height:100%;">
                      <div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.4);
                                   text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px;">
                        Bundle {i+1}
                      </div>
                      <div style="font-size:16px;font-weight:800;color:white;margin-bottom:12px;
                                   line-height:1.3;">{b.get('bundle_name','')}</div>
                      {f'<div style="background:rgba(255,255,255,0.08);display:inline-block;padding:4px 12px;border-radius:8px;font-size:12px;font-weight:700;color:white;margin-bottom:14px;">{price_str}</div>' if price_str else ''}
                      <div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.4);
                                   text-transform:uppercase;margin-bottom:6px;">Includes</div>
                      <div style="margin-bottom:14px;">
                        {''.join(f'<span style="display:inline-block;background:rgba(255,255,255,0.08);color:rgba(255,255,255,0.8);font-size:11px;padding:3px 10px;border-radius:99px;margin:2px;">{s}</span>' for s in services)}
                      </div>
                      {f'<div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.4);text-transform:uppercase;margin-bottom:4px;">Target</div><p style="font-size:12px;color:rgba(255,255,255,0.7);margin-bottom:12px;">{b.get("target_segment","")}</p>' if b.get("target_segment") else ''}
                      {f'<div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px;margin-bottom:10px;"><div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.4);text-transform:uppercase;margin-bottom:4px;">Market Gap</div><p style="font-size:12px;color:rgba(255,255,255,0.75);margin:0;">{b.get("competitor_gap","")}</p></div>' if b.get("competitor_gap") else ''}
                      {f'<div style="background:rgba(139,92,246,0.1);border-radius:10px;padding:10px;"><div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.4);text-transform:uppercase;margin-bottom:4px;">Pitch Angle</div><p style="font-size:12px;color:rgba(255,255,255,0.75);margin:0;font-style:italic;">"{b.get("outreach_angle","")}"</p></div>' if r_mode == "operator" and b.get("outreach_angle") else ''}
                      {f'<div style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.2);border-radius:10px;padding:10px;"><div style="font-size:10px;font-weight:700;color:#10b981;text-transform:uppercase;margin-bottom:4px;">Projected ROI</div><p style="font-size:12px;color:#34d399;margin:0;">{b.get("projected_roi","")}</p></div>' if r_mode == "corporate" and b.get("projected_roi") else ''}
                    </div>
                    """, unsafe_allow_html=True)

    # ── TAB: Outreach ─────────────────────────────────────────────────────────
    with tab_outreach:
        if not outreach:
            st.info("Outreach drafts are generated in Corporate HR mode only.")
        else:
            for i, e in enumerate(outreach):
                with st.expander(f"✉️ {e.get('subject','Email')}  —  {e.get('target_role','')} @ {e.get('target_company','')}"):
                    st.markdown(f"**To:** {e.get('target_role','')} @ {e.get('target_company','')}")
                    st.markdown(f"**Subject:** {e.get('subject','')}")
                    st.markdown("---")
                    st.markdown(e.get("body",""))
                    if e.get("signal_used"):
                        st.caption(f"Signal used: {e['signal_used']}")
                    st.code(f"Subject: {e.get('subject','')}\n\n{e.get('body','')}", language=None)

    # ── ROI summary (corporate) ───────────────────────────────────────────────
    if r_mode == "corporate" and roi:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(16,185,129,0.12),rgba(20,184,166,0.08));
                     border:1px solid rgba(16,185,129,0.3);border-radius:16px;padding:20px;margin-top:16px;">
          <div style="font-size:11px;font-weight:700;color:#10b981;
                       text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">
            💰 ROI Summary
          </div>
          <p style="font-size:14px;line-height:1.7;color:rgba(255,255,255,0.8);margin:0;">{roi}</p>
        </div>""", unsafe_allow_html=True)
