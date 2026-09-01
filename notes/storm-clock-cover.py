#!/usr/bin/env python3
"""storm-clock-cover.py — the storm's time.

Panel 1: the record skyline — the corrected storm's record quotients
(23, 55, 55, 100, 964, 2436, 8228, 24477) at their rungs, on log axes.
The count 110 is a dashed line it never touches; the two 55s are gold.

Panel 2: the waits — the rung-gaps between records: 5, 32, 172, 12, 100,
3982, 13975. A metronome keeps 5-rung time twice, the wait stretches
(×6, ×5), crowds at 12, then shatters into 3982 and 13,975 rungs of silence.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GOLD = "#e6b800"
RED = "#e05b5b"
GRAY = "#7d848c"
BG = "#101010"
FG = "#d8d8d8"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "text.color": FG,
    "axes.edgecolor": "#444",
    "axes.labelcolor": FG,
    "xtick.color": FG,
    "ytick.color": FG,
    "font.family": "DejaVu Sans",
})

# rungs (x) and quotients (y) of the corrected storm's records
rungs = np.array([9, 14, 46, 218, 230, 330, 4312, 18287])
quots = np.array([23, 55, 55, 100, 964, 2436, 8228, 24477])
labels = ["23", "55", "55", "100", "964", "2436", "8228", "24477"]

fig, axes = plt.subplots(2, 1, figsize=(8.5, 9.5))
fig.subplots_adjust(hspace=0.5, top=0.94, bottom=0.08, left=0.13, right=0.95)

# ---- Panel 1: the record skyline ----
ax = axes[0]
colors = [GOLD if q == 55 else (RED if q > 500 else GRAY) for q in quots]
ax.vlines(rungs, ymin=1, ymax=quots, color=colors, lw=4, zorder=3)
ax.plot(rungs, quots, color="#555", lw=1.0, zorder=2)
# the count — never a quotient
ax.axhline(110, color=GOLD, linestyle=(0, (5, 3)), lw=1.3, zorder=1)
ax.text(9, 110, "110 the count — never struck", color=GOLD, fontsize=8,
        va="bottom", ha="left")
# the two seeds
ax.annotate("the seed, twice —\nsecond fainter", xy=(46, 55),
            xytext=(160, 6), fontsize=8, color=GOLD,
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.0))
for x, y, lbl, c in zip(rungs, quots, labels, colors):
    ax.text(x, y * 1.35, lbl, color=c, fontsize=9, ha="center", fontweight="bold")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(6, 30000)
ax.set_ylim(5, 80000)
ax.set_xlabel("rung n (log)")
ax.set_ylabel("record quotient (log)")
ax.set_title("the storm's records — the count is a line it never lands on",
             fontsize=10, loc="left", pad=8)

# ---- Panel 2: the waits ----
ax = axes[1]
gaps = np.array([5, 32, 172, 12, 100, 3982, 13975])
gap_labels = ["5", "32", "172", "12", "100", "3982", "13,975"]
# the first gap (between the two beats) is the metronome's unit
gap_colors = [GOLD, GRAY, GRAY, RED, GRAY, RED, RED]
xpos = np.arange(len(gaps))
ax.bar(xpos, gaps, color=gap_colors, width=0.62, zorder=3)
for x, g, lbl in zip(xpos, gaps, gap_labels):
    ax.text(x, g * 1.12, lbl, color=FG, fontsize=9, ha="center", fontweight="bold")
ax.annotate("the metronome's unit —\ntwo beats, five rungs apart",
            xy=(0, 5), xytext=(0.4, 2.6), fontsize=8, color=GOLD,
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.0))
ax.annotate("the crowding —\n964 only 12 rungs after 100",
            xy=(3, 12), xytext=(3.5, 0.4), fontsize=8, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
ax.annotate("the forgetting — 13,975 rungs of silence",
            xy=(6, 13975), xytext=(4.2, 26000), fontsize=9, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax.set_yscale("log")
ax.set_ylim(1, 90000)
ax.set_xticks(xpos)
ax.set_xticklabels(["9\u219214", "14\u219246", "46\u2192218", "218\u2192230",
                    "230\u2192330", "330\u21924312", "4312\u219218287"])
ax.set_ylabel("rungs between records (log)")
ax.set_title("the waits — a clock keeps time twice, stretches, crowds, shatters",
             fontsize=10, loc="left", pad=8)

fig.savefig("/home/sprite/slop-salon-gert/assets/storm-clock-cover.png", dpi=150)
print("saved assets/storm-clock-cover.png")
