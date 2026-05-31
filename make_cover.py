"""WellSignal Blog Cover Image — 1600x900px"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_agg import FigureCanvasAgg

BG      = "#0a0a0f"
VIOLET  = "#8b5cf6"
EMERALD = "#10b981"
WHITE   = "#ffffff"
AMBER   = "#f59e0b"
BLUE    = "#3b82f6"
DIM     = "#ffffff55"

W, H = 16, 9

fig, ax = plt.subplots(figsize=(W, H), dpi=100)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

# ── Background: subtle dot grid ──────────────────────────────────────────────
for x in np.arange(0.4, W, 0.9):
    for y in np.arange(0.4, H, 0.9):
        ax.plot(x, y, "o", color=VIOLET, markersize=1.2, alpha=0.07, zorder=0)

# ── Radial glow — left-center (data source side) ─────────────────────────────
for r, a in [(5.5, 0.025), (4.0, 0.045), (2.8, 0.07), (1.6, 0.10)]:
    ax.add_patch(plt.Circle((3.2, 4.5), r, color=VIOLET, alpha=a, zorder=0))

# ── Radial glow — right-center (output side) ─────────────────────────────────
for r, a in [(5.5, 0.025), (4.0, 0.045), (2.8, 0.07), (1.6, 0.10)]:
    ax.add_patch(plt.Circle((12.8, 4.5), r, color=EMERALD, alpha=a, zorder=0))

# ── Central pipeline line ─────────────────────────────────────────────────────
for i, t in enumerate(np.linspace(0, 1, 400)):
    cm = LinearSegmentedColormap.from_list("vg", [VIOLET, EMERALD])
    x = 3.8 + i * (8.4 / 400)
    ax.plot(x, 4.5, "o", color=cm(t), markersize=2.4, alpha=0.6, zorder=2)

# ── Data source nodes (left cluster) ─────────────────────────────────────────
sources = [
    (2.0, 6.8, "ClassPass",   VIOLET),
    (1.2, 5.5, "Eventbrite",  "#f97316"),
    (1.2, 3.5, "Luma",        "#ec4899"),
    (2.0, 2.2, "LinkedIn",    BLUE),
    (3.2, 1.4, "SERP",        "#06b6d4"),
]
for x, y, label, color in sources:
    # Line to center pipeline
    ax.plot([x, 3.8], [y, 4.5], color=color, alpha=0.25, linewidth=1.2,
            linestyle="--", zorder=1)
    # Node circle
    ax.add_patch(plt.Circle((x, y), 0.52, color=color, alpha=0.18, zorder=3))
    ax.add_patch(plt.Circle((x, y), 0.52, color=color, alpha=0.0,
                              fill=False, edgecolor=color, linewidth=1.5, zorder=3))
    ax.plot(x, y, "o", color=color, markersize=8, alpha=0.9, zorder=4)
    ax.text(x, y - 0.82, label, fontsize=8.5, ha="center", va="center",
            color=color, fontweight="bold", zorder=5)

# ── Output nodes (right cluster) ─────────────────────────────────────────────
outputs = [
    (13.8, 6.8, "Market Gaps",  EMERALD),
    (14.8, 5.4, "Bundles",      EMERALD),
    (14.8, 3.6, "Outreach",     BLUE),
    (13.8, 2.2, "ROI Intel",    AMBER),
]
for x, y, label, color in outputs:
    ax.plot([12.2, x], [4.5, y], color=color, alpha=0.25, linewidth=1.2,
            linestyle="--", zorder=1)
    ax.add_patch(plt.Circle((x, y), 0.52, color=color, alpha=0.18, zorder=3))
    ax.plot(x, y, "o", color=color, markersize=8, alpha=0.9, zorder=4)
    ax.text(x, y - 0.82, label, fontsize=8.5, ha="center", va="center",
            color=color, fontweight="bold", zorder=5)

# ── Central AI processing box ─────────────────────────────────────────────────
rect = FancyBboxPatch((5.5, 3.55), 5.0, 1.9,
                       boxstyle="round,pad=0,rounding_size=0.35",
                       facecolor="#0a0a0f", edgecolor=VIOLET,
                       linewidth=1.8, alpha=1.0, zorder=5)
ax.add_patch(rect)
# Inner gradient fill
for i, t in enumerate(np.linspace(0, 1, 100)):
    cm = LinearSegmentedColormap.from_list("vg", [VIOLET+"22", EMERALD+"22"])
    ax.add_patch(plt.Rectangle((5.52 + i * 4.96/100, 3.57), 4.96/100, 1.86,
                                facecolor=cm(t), edgecolor="none", zorder=5))

ax.text(8.0, 4.88, "AI Agent", fontsize=15, fontweight="bold", ha="center",
        va="center", color=WHITE, zorder=6,
        path_effects=[pe.withStroke(linewidth=4, foreground=VIOLET+"44")])
ax.text(8.0, 4.38, "Signal Classification  ·  Market Analysis", fontsize=9,
        ha="center", va="center", color=DIM, zorder=6)
ax.text(8.0, 3.98, "Bundle Generation  ·  Outreach Drafting", fontsize=9,
        ha="center", va="center", color=DIM, zorder=6)

# ── Bright Data badge ─────────────────────────────────────────────────────────
rect2 = FancyBboxPatch((6.6, 2.55), 2.8, 0.62,
                        boxstyle="round,pad=0,rounding_size=0.15",
                        facecolor=VIOLET, alpha=0.15, edgecolor=VIOLET,
                        linewidth=1.2, zorder=5)
ax.add_patch(rect2)
ax.text(8.0, 2.86, "Powered by Bright Data", fontsize=8.5, ha="center",
        va="center", color=VIOLET, fontweight="bold", zorder=6)

# ── Bottom gradient bar ───────────────────────────────────────────────────────
for i, t in enumerate(np.linspace(0, 1, 400)):
    cm = LinearSegmentedColormap.from_list("vg", [VIOLET, EMERALD])
    ax.add_patch(plt.Rectangle((i * W/400, 0.0), W/400, 0.28,
                                facecolor=cm(t), edgecolor="none", zorder=10))

# ── Main title ────────────────────────────────────────────────────────────────
ax.text(8.0, 7.85, "WellSignal", fontsize=64, fontweight="bold", ha="center",
        va="center", color=WHITE, zorder=8,
        path_effects=[pe.withStroke(linewidth=14, foreground=VIOLET+"2a")])

# Gradient underline beneath title
for i, t in enumerate(np.linspace(0, 1, 300)):
    cm = LinearSegmentedColormap.from_list("vg", [VIOLET, EMERALD])
    ax.add_patch(plt.Rectangle((4.2 + i * 7.6/300, 7.26), 7.6/300, 0.055,
                                facecolor=cm(t), edgecolor="none", zorder=8))

# ── Subtitle ──────────────────────────────────────────────────────────────────
ax.text(8.0, 6.82, "Building Real-Time GTM Intelligence for Wellness",
        fontsize=15, ha="center", va="center", color=DIM, zorder=8)
ax.text(8.0, 6.38, "with Bright Data  ·  Claude AI  ·  LangChain",
        fontsize=11, ha="center", va="center", color="#ffffff33", zorder=8)

# ── Small logo pill ───────────────────────────────────────────────────────────
rect3 = FancyBboxPatch((0.35, 8.45), 0.62, 0.42,
                        boxstyle="round,pad=0,rounding_size=0.1",
                        facecolor=VIOLET, alpha=0.35, edgecolor=VIOLET,
                        linewidth=1.2, zorder=9)
ax.add_patch(rect3)
ax.text(0.66, 8.66, "W", fontsize=13, fontweight="bold", ha="center",
        va="center", color=WHITE, zorder=10)

plt.tight_layout(pad=0)
out = "/Users/abhijitbetigeri/projects/wellsignal/WellSignal_Blog_Cover.png"
plt.savefig(out, dpi=100, bbox_inches="tight",
            facecolor=BG, edgecolor="none")
plt.close()
print(f"Saved: {out}")
