"""WellSignal Hackathon Slide Deck Generator"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.font_manager as fm

# Register Apple Color Emoji for emoji rendering
try:
    fm.fontManager.addfont('/System/Library/Fonts/Apple Color Emoji.ttc')
except Exception:
    pass

# Replace emojis with text alternatives for reliability
ICONS = {
    "yoga": "[W]", "building": "[HR]", "chart": "[--]",
    "globe": "[BD]", "robot": "[AI]", "target": "[>>]", "package": "[PKG]",
}

BG      = "#0a0a0f"
VIOLET  = "#8b5cf6"
EMERALD = "#10b981"
WHITE   = "#ffffff"
DIM     = "#ffffff66"
CARD    = "#ffffff0d"
AMBER   = "#f59e0b"
BLUE    = "#3b82f6"

def fig(w=16, h=9):
    f, ax = plt.subplots(figsize=(w, h))
    f.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 16); ax.set_ylim(0, 9)
    ax.axis("off")
    return f, ax

def grad_text(ax, x, y, text, size, weight="bold", ha="center", va="center"):
    """Gradient violet→emerald text via two overlapping labels."""
    ax.text(x, y, text, fontsize=size, fontweight=weight, ha=ha, va=va,
            color=VIOLET, alpha=0.0)  # invisible anchor
    # Use a gradient via image trick — just use violet for left, emerald for right
    # Simpler: render in white with glow, accent in violet
    t = ax.text(x, y, text, fontsize=size, fontweight=weight, ha=ha, va=va,
                color=WHITE, zorder=5)
    t.set_path_effects([pe.withStroke(linewidth=6, foreground=VIOLET+"44")])
    return t

def pill(ax, x, y, w, h, color, alpha=0.15, radius=0.3):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                           boxstyle=f"round,pad=0,rounding_size={radius}",
                           facecolor=color, alpha=alpha, edgecolor=color,
                           linewidth=1.5, zorder=3)
    ax.add_patch(rect)
    return rect

def dot_grid(ax, color=VIOLET, alpha=0.08):
    for x in np.arange(0.5, 16, 1.2):
        for y in np.arange(0.5, 9, 1.2):
            ax.plot(x, y, "o", color=color, markersize=1.8, alpha=alpha, zorder=0)

def gradient_bar(ax, y=0.35, h=0.35):
    for i, t in enumerate(np.linspace(0, 1, 300)):
        c = plt.cm.ScalarMappable(cmap=LinearSegmentedColormap.from_list("vg",[VIOLET,EMERALD]))
        c.set_clim(0, 1)
        color = c.to_rgba(t)
        ax.add_patch(plt.Rectangle((i * 16/300, y - h/2), 16/300, h,
                                    facecolor=color, edgecolor="none", zorder=1))

def header_logo(ax):
    pill(ax, 0.7, 8.5, 0.6, 0.5, VIOLET, alpha=0.3)
    ax.text(0.7, 8.5, "W", fontsize=14, fontweight="bold", ha="center", va="center",
            color=WHITE, zorder=5)
    ax.text(1.3, 8.55, "WellSignal", fontsize=11, fontweight="bold", ha="left",
            va="center", color=WHITE, zorder=5)
    ax.text(1.3, 8.38, "GTM Intelligence · Bright Data + Claude", fontsize=7,
            ha="left", va="center", color=DIM, zorder=5)

# ─────────────────────────────────────────────
# SLIDE 1 — TITLE
# ─────────────────────────────────────────────
def slide_title():
    f, ax = fig()
    dot_grid(ax)
    gradient_bar(ax)

    # Glow circle
    for r, a in [(3.5, 0.04), (2.5, 0.07), (1.5, 0.12)]:
        c = plt.Circle((8, 4.8), r, color=VIOLET, alpha=a, zorder=0)
        ax.add_patch(c)

    ax.text(8, 5.9, "WellSignal", fontsize=72, fontweight="bold", ha="center",
            va="center", color=WHITE, zorder=5,
            path_effects=[pe.withStroke(linewidth=12, foreground=VIOLET+"33")])

    # Gradient underline
    for i, t in enumerate(np.linspace(0, 1, 200)):
        cm = LinearSegmentedColormap.from_list("vg", [VIOLET, EMERALD])
        ax.add_patch(plt.Rectangle((4 + i*8/200, 5.12), 8/200, 0.055,
                                    facecolor=cm(t), edgecolor="none", zorder=4))

    ax.text(8, 4.65, "GTM Intelligence for Wellness", fontsize=22, ha="center",
            va="center", color=DIM, zorder=5)
    ax.text(8, 4.1, "Live web scraping → AI insights → B2B revenue", fontsize=13,
            ha="center", va="center", color="#ffffff44", zorder=5)

    # Tech pills
    techs = ["Bright Data", "Claude AI", "FastAPI", "Next.js"]
    colors = [VIOLET, EMERALD, AMBER, BLUE]
    for i, (t, c) in enumerate(zip(techs, colors)):
        x = 5.5 + i * 1.7
        pill(ax, x, 3.2, 1.4, 0.42, c, alpha=0.2, radius=0.2)
        ax.text(x, 3.2, t, fontsize=9, ha="center", va="center",
                color=c, fontweight="bold", zorder=5)

    ax.text(8, 0.75, "Bright Data Web Data UNLOCKED Hackathon  ·  2024",
            fontsize=9, ha="center", va="center", color="#ffffff30", zorder=5)
    return f

# ─────────────────────────────────────────────
# SLIDE 2 — PROBLEM
# ─────────────────────────────────────────────
def slide_problem():
    f, ax = fig()
    dot_grid(ax, VIOLET, 0.05)
    gradient_bar(ax)
    header_logo(ax)

    ax.text(8, 7.8, "The Problem", fontsize=34, fontweight="bold", ha="center",
            va="center", color=WHITE, zorder=5)

    problems = [
        ("◉", "Wellness operators", "fly blind — no idea what competitors charge\nor which corporate buyers are hiring"),
        ("▣", "Corporate HR teams", "spend weeks researching wellness vendors\nwith zero market benchmarks"),
        ("▼", "Missed revenue", "millions in B2B wellness contracts lost\nbecause operators can't find the right buyers"),
    ]
    for i, (icon, title, desc) in enumerate(problems):
        x = 2.2 + i * 4.0
        pill(ax, x, 4.5, 3.6, 3.2, VIOLET if i != 1 else EMERALD, alpha=0.08, radius=0.4)
        ax.text(x, 5.7, icon, fontsize=26, ha="center", va="center", zorder=5)
        ax.text(x, 5.15, title, fontsize=12, fontweight="bold", ha="center",
                va="center", color=WHITE, zorder=5)
        ax.text(x, 4.35, desc, fontsize=9.5, ha="center", va="center",
                color=DIM, zorder=5, linespacing=1.6)

    return f

# ─────────────────────────────────────────────
# SLIDE 3 — SOLUTION
# ─────────────────────────────────────────────
def slide_solution():
    f, ax = fig()
    dot_grid(ax, EMERALD, 0.05)
    gradient_bar(ax)
    header_logo(ax)

    ax.text(8, 7.8, "The Solution", fontsize=34, fontweight="bold", ha="center",
            va="center", color=WHITE, zorder=5)

    ax.text(8, 7.1, "WellSignal scrapes the live web, classifies signals with Claude AI,\nand delivers actionable GTM intelligence in seconds.",
            fontsize=12, ha="center", va="center", color=DIM, linespacing=1.6, zorder=5)

    # Two mode boxes
    for xi, (icon, title, pts, c) in enumerate([
        ("◉", "Wellness Operator Mode", [
            "Real-time competitor pricing",
            "Event demand signals",
            "Corporate buyer radar",
            "Bundle recommendations",
            "Auto-drafted B2B emails",
        ], VIOLET),
        ("▣", "Corporate HR Mode", [
            "Curated vendor bundles",
            "Employee wellness programs",
            "ROI projections",
            "Benchmarked pricing",
            "Outreach-ready content",
        ], EMERALD),
    ]):
        x = 3.5 + xi * 6.5
        pill(ax, x, 4.0, 5.8, 4.8, c, alpha=0.1, radius=0.4)
        ax.plot([x - 2.5, x + 2.5], [6.15, 6.15], color=c, alpha=0.3, linewidth=0.8, zorder=3)
        ax.text(x, 6.55, icon + "  " + title, fontsize=13, fontweight="bold",
                ha="center", va="center", color=c, zorder=5)
        for j, pt in enumerate(pts):
            ax.text(x - 2.2, 5.65 - j * 0.68, f"◆  {pt}", fontsize=10,
                    ha="left", va="center", color=DIM, zorder=5)
    return f

# ─────────────────────────────────────────────
# SLIDE 4 — HOW IT WORKS
# ─────────────────────────────────────────────
def slide_architecture():
    f, ax = fig()
    dot_grid(ax, BLUE, 0.05)
    gradient_bar(ax)
    header_logo(ax)

    ax.text(8, 7.8, "How It Works", fontsize=34, fontweight="bold", ha="center",
            va="center", color=WHITE, zorder=5)

    steps = [
        ("◈", "Bright Data\nScraping", "ClassPass · Eventbrite\nLuma · LinkedIn · SERP", VIOLET),
        ("⊛", "Claude AI\nClassification", "Signal type · Urgency\nCategory · Geography", EMERALD),
        ("◎", "Competitor\nAnalysis", "Market gaps · Pricing\nRising categories", AMBER),
        ("▤", "Bundle &\nOutreach", "B2B packages\nPersonalized emails", BLUE),
    ]

    for i, (icon, title, sub, c) in enumerate(steps):
        x = 1.8 + i * 3.8
        pill(ax, x, 4.5, 3.2, 3.8, c, alpha=0.12, radius=0.4)
        ax.text(x, 5.8, icon, fontsize=28, ha="center", va="center", zorder=5)
        ax.text(x, 5.05, title, fontsize=12, fontweight="bold", ha="center",
                va="center", color=c, zorder=5, linespacing=1.4)
        ax.text(x, 4.1, sub, fontsize=9, ha="center", va="center",
                color=DIM, zorder=5, linespacing=1.5)

        # Arrow
        if i < 3:
            ax.annotate("", xy=(x + 2.1, 4.5), xytext=(x + 1.6, 4.5),
                        arrowprops=dict(arrowstyle="->", color=c, lw=1.8), zorder=6)

    ax.text(8, 1.8, "65+ live signals scraped  ·  Claude classifies each signal  ·  Full pipeline in < 30 seconds",
            fontsize=10, ha="center", va="center", color="#ffffff40", zorder=5)
    return f

# ─────────────────────────────────────────────
# SLIDE 5 — BRIGHT DATA USAGE
# ─────────────────────────────────────────────
def slide_brightdata():
    f, ax = fig()
    dot_grid(ax, VIOLET, 0.05)
    gradient_bar(ax)
    header_logo(ax)

    ax.text(8, 7.8, "Bright Data Integration", fontsize=34, fontweight="bold",
            ha="center", va="center", color=WHITE, zorder=5)

    sources = [
        ("ClassPass", "34 listings", "Competitor pricing & wellness bundles", VIOLET),
        ("Eventbrite", "20 events", "Demand signals by category & location", EMERALD),
        ("Luma", "5+ events", "Community wellness events via Discover API", BLUE),
        ("SERP", "6+ results", "Google demand trends & community signals", AMBER),
        ("LinkedIn", "Live feed", "Corporate buyer radar — hiring signals", "#ec4899"),
    ]

    for i, (src, count, desc, c) in enumerate(sources):
        y = 6.5 - i * 1.1
        pill(ax, 8, y, 13, 0.82, c, alpha=0.08, radius=0.2)
        ax.text(1.8, y, src, fontsize=11, fontweight="bold", ha="left",
                va="center", color=c, zorder=5)
        pill(ax, 5.0, y, 1.5, 0.44, c, alpha=0.2, radius=0.15)
        ax.text(5.0, y, count, fontsize=10, fontweight="bold", ha="center",
                va="center", color=WHITE, zorder=5)
        ax.text(7.0, y, desc, fontsize=10, ha="left", va="center",
                color=DIM, zorder=5)

    ax.text(8, 1.15, "Web Unlocker zone: wellsignal_unlocker  ·  SERP API  ·  Local JSON caching for dev efficiency",
            fontsize=9, ha="center", va="center", color="#ffffff30", zorder=5)
    return f

# ─────────────────────────────────────────────
# SLIDE 6 — DEMO RESULTS
# ─────────────────────────────────────────────
def slide_results():
    f, ax = fig()
    dot_grid(ax, EMERALD, 0.05)
    gradient_bar(ax)
    header_logo(ax)

    ax.text(8, 7.8, "Live Demo Results", fontsize=34, fontweight="bold",
            ha="center", va="center", color=WHITE, zorder=5)

    stats = [
        ("65+", "Live Signals\nScraped", VIOLET),
        ("7", "Market Gaps\nIdentified", AMBER),
        ("3", "Bundle\nRecommendations", EMERALD),
        ("<30s", "Full Pipeline\nRuntime", BLUE),
    ]

    for i, (val, label, c) in enumerate(stats):
        x = 2.0 + i * 3.8
        pill(ax, x, 5.8, 3.2, 2.4, c, alpha=0.15, radius=0.4)
        ax.text(x, 6.3, val, fontsize=32, fontweight="bold", ha="center",
                va="center", color=c, zorder=5)
        ax.text(x, 5.4, label, fontsize=10, ha="center", va="center",
                color=DIM, zorder=5, linespacing=1.5)

    # Sample output box
    pill(ax, 8, 3.1, 13.5, 2.6, VIOLET, alpha=0.07, radius=0.4)
    ax.text(1.5, 4.1, "Sample Market Gap (SF Yoga):", fontsize=10, fontweight="bold",
            ha="left", va="center", color=VIOLET, zorder=5)
    gaps = [
        "◆  No hybrid (in-person + digital) yoga offerings in SF — major gap vs competitors",
        "◆  Corporate lunch-break wellness sessions underserved — strong B2B demand signal",
        "◆  Premium pricing tier ($45-65/class) has no clear market leader in Mission District",
    ]
    for j, g in enumerate(gaps):
        ax.text(1.5, 3.65 - j * 0.52, g, fontsize=9.5, ha="left", va="center",
                color=DIM, zorder=5)
    return f

# ─────────────────────────────────────────────
# SLIDE 7 — TECH STACK
# ─────────────────────────────────────────────
def slide_stack():
    f, ax = fig()
    dot_grid(ax, BLUE, 0.05)
    gradient_bar(ax)
    header_logo(ax)

    ax.text(8, 7.8, "Tech Stack", fontsize=34, fontweight="bold", ha="center",
            va="center", color=WHITE, zorder=5)

    layers = [
        ("Frontend", "Next.js 15  ·  Tailwind CSS  ·  React", BLUE),
        ("Backend", "FastAPI  ·  Python 3.11  ·  Uvicorn", EMERALD),
        ("AI Agents", "LangChain  ·  Claude Haiku 4.5  ·  Multi-agent pipeline", VIOLET),
        ("Data Layer", "Bright Data Web Unlocker  ·  SERP API  ·  BeautifulSoup", AMBER),
    ]

    for i, (layer, tech, c) in enumerate(layers):
        y = 5.9 - i * 1.3
        pill(ax, 8, y, 13.5, 0.9, c, alpha=0.1, radius=0.25)
        ax.text(2.0, y, layer, fontsize=12, fontweight="bold", ha="left",
                va="center", color=c, zorder=5)
        ax.plot([4.5, 4.5], [y - 0.3, y + 0.3], color=c, alpha=0.3, linewidth=1, zorder=3)
        ax.text(5.0, y, tech, fontsize=11, ha="left", va="center",
                color=DIM, zorder=5)

    ax.text(8, 1.2, "All data ingestion through Bright Data APIs  ·  AI synthesis by Anthropic Claude",
            fontsize=10, ha="center", va="center", color="#ffffff30", zorder=5)
    return f

# ─────────────────────────────────────────────
# SLIDE 8 — CLOSING
# ─────────────────────────────────────────────
def slide_closing():
    f, ax = fig()
    dot_grid(ax)
    gradient_bar(ax)

    for r, a in [(4, 0.03), (3, 0.06), (2, 0.1), (1, 0.15)]:
        c1 = plt.Circle((8, 4.8), r, color=EMERALD, alpha=a, zorder=0)
        ax.add_patch(c1)

    ax.text(8, 6.2, "WellSignal", fontsize=58, fontweight="bold", ha="center",
            va="center", color=WHITE, zorder=5,
            path_effects=[pe.withStroke(linewidth=10, foreground=EMERALD+"33")])

    for i, t in enumerate(np.linspace(0, 1, 200)):
        cm = LinearSegmentedColormap.from_list("vg", [VIOLET, EMERALD])
        ax.add_patch(plt.Rectangle((4 + i*8/200, 5.6), 8/200, 0.06,
                                    facecolor=cm(t), edgecolor="none", zorder=4))

    ax.text(8, 5.15, "Live web data → AI intelligence → Wellness revenue", fontsize=14,
            ha="center", va="center", color=DIM, zorder=5)

    pills = [
        ("65+ live signals", VIOLET), ("7 market gaps", AMBER),
        ("3 bundles", EMERALD), ("<30s pipeline", BLUE),
    ]
    for i, (label, c) in enumerate(pills):
        x = 3.5 + i * 3.0
        pill(ax, x, 3.9, 2.6, 0.55, c, alpha=0.2, radius=0.25)
        ax.text(x, 3.9, label, fontsize=10, fontweight="bold", ha="center",
                va="center", color=c, zorder=5)

    ax.text(8, 2.8, "Built for the Bright Data Web Data UNLOCKED Hackathon",
            fontsize=11, ha="center", va="center", color="#ffffff40", zorder=5)
    ax.text(8, 2.35, "GTM Intelligence Track", fontsize=10, ha="center",
            va="center", color=EMERALD, zorder=5)
    return f


if __name__ == "__main__":
    slides = [
        slide_title(),
        slide_problem(),
        slide_solution(),
        slide_architecture(),
        slide_brightdata(),
        slide_results(),
        slide_stack(),
        slide_closing(),
    ]

    out = "/Users/abhijitbetigeri/projects/wellsignal/WellSignal_Pitch_Deck.pdf"
    with PdfPages(out) as pdf:
        for s in slides:
            pdf.savefig(s, bbox_inches="tight", facecolor=BG, dpi=150)
            plt.close(s)

    print(f"Saved: {out}")
