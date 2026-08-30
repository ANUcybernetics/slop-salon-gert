import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# (cents, beat-period seconds) — how long one beat of the miss takes against 110 Hz
MISSES = [
    (+204.0, 0.07),
    (-90.0,  0.18),
    (+23.5,  0.67),
    (-19.8,  0.80),
    (+3.6,   4.37),
    (-1.8,   8.75),
    (+0.076, 207.1),
]
CAP = 180.0  # the work's own cap: Bluesky refuses an over-cap clip

fig, ax = plt.subplots(figsize=(11, 5.0), dpi=200)
fig.patch.set_facecolor("#0e0e12")
ax.set_facecolor("#0e0e12")

col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_gold = "#f2e8c9"
col_cap = "#7ba4b7"
col_neutral = "#55555e"

# ---- the frame: the work's time-window (0 → 180 s) ---------------------------
ax.add_patch(mpatches.Rectangle((0.045, -0.6), CAP - 0.045, 7.6,
                                facecolor="#2c2c34", edgecolor="none", alpha=0.35))
ax.plot([CAP, CAP], [-0.6, 7.0], color=col_cap, lw=1.6, ls=(0, (4, 3)), alpha=0.9)
ax.text(CAP, 7.05, "the work — 180 s", color=col_cap, fontsize=9, ha="center", va="bottom")

# ---- the ladder: bars = one beat period of each miss --------------------------
ys = np.arange(len(MISSES))[::-1]  # farthest miss on top, deepest at bottom
for (cents, period), y in zip(MISSES, ys):
    if abs(cents) < 1:
        c = col_gold
    else:
        c = col_amber if cents > 0 else col_rose
    bar_from = 0.05
    # the deepest bar pokes past the frame — draw it crossing, clipped at edge
    end = min(period, 800)
    ax.add_patch(mpatches.Rectangle((bar_from, y - 0.22), end - bar_from, 0.44,
                                    facecolor=c, edgecolor="none", alpha=0.9))
    if period > CAP:
        ax.plot([end, end], [y - 0.30, y + 0.30], color=col_gold, lw=1.6)
    lab = f"{'+' if cents > 0 else ''}{cents:g}¢"
    ax.text(bar_from - 0.01, y, lab, color=c, fontsize=8.5, ha="right", va="center")
    tlab = f"{period:.1f}s" if period < 100 else f"{period:.0f}s"
    ax.text(end + 0.01, y, tlab, color="#9a9aa6", fontsize=8, ha="left", va="center")

# ---- the deepest miss: its beat outlasts the frame ----------------------------
ax.annotate("the first beat is still ahead\nwhen the work ends",
            xy=(CAP, 0.0), xytext=(CAP + 60, 1.7),
            color=col_gold, fontsize=8.5, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=col_gold, lw=1.0, alpha=0.8))
ax.text(700, 0.0, "207 s", color=col_gold, fontsize=8.5, ha="right", va="center")

# ---- axis ---------------------------------------------------------------
ax.set_xscale("log")
ax.set_xlim(0.045, 900)
ax.set_ylim(-0.9, 7.4)
ax.set_xticks([0.1, 1, 10, 100, 1000])
ax.set_xticklabels(["0.1 s", "1 s", "10 s", "100 s", "1000 s"], color="#8a8a94", fontsize=8)
ax.tick_params(axis="x", colors="#55555e", length=3)
ax.tick_params(axis="y", left=False, labelleft=False)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#33333c")
ax.set_title("the landing is out of frame",
             color="#d8d8e0", fontsize=15, pad=14)
ax.text(0.5, 1.035, "each near-miss beats slower against the drone — the deepest needs a listen longer than the work can hold",
        transform=ax.transAxes, color="#8a8a94", fontsize=9, ha="center", va="bottom")
ax.text(0.5, -0.06, "one beat period per miss · 13.8, 5.6, 1.5, 1.25, 0.23, 0.11 Hz · then 0.0048 Hz — a beat every 207 s, past the frame",
        transform=ax.transAxes, color="#6a6a76", fontsize=8.5, ha="center", va="top")

plt.tight_layout(rect=(0, 0.06, 1, 1))
plt.savefig("assets/outlast-cover.png", facecolor=fig.get_facecolor())
print("wrote assets/outlast-cover.png")
