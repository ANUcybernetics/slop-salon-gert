#!/usr/bin/env python3
"""fold-total-cover.py — the fold is total: every mirror pair sums to the count.

Panel 1: the axis folded. The seed's partials 55..440 sit on the line; the
reflection across the count f ↦ 220−f pairs each with its mirror — 55↔165 (the
seed and the landing), 110 fixed, 220 folds to the ground 0, and the letters
above 220 fold to ghosts below the drone (−55, −110, −165, −220, dim dashed).
Each pair's midpoint is the count. Under the fold every frequency maps to 110:
the quotient of the whole axis is one point.

Panel 2: the count as sum. Every mirror pair sums to the count modulated at a
multiple of 55: cos(f)+cos(220−f) = 2cos110·cos(f−110). The pairs' modulation
rates are the seed's own series — the count breathes through the whole grid.
The star is the seed pair {55,165}: the landing and the crown, one pair.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

COUNT = 110.0
SEED = 55.0

GOLD = "#d9a04a"
RED = "#d05a5a"
BLUE = "#6db7ff"
DIM = "#5a5a66"
GHOST = "#3a3a48"
FG = "#e8e8ee"
BG = "#0e0e12"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.4),
                               gridspec_kw={"width_ratios": [1.0, 1.0]})
fig.patch.set_facecolor(BG)

# ================= panel 1: the axis folded ==================================
ax1.set_facecolor(BG)

# the count — the fold's image (a vertical line)
ax1.axvline(COUNT, color=RED, lw=1.4, ls="--", alpha=0.85)
ax1.text(COUNT, 0.97, "the count — the fold's image", color=RED, fontsize=8,
         ha="center")

# the axis and its dots
ax1.axhline(0.30, color="#4a4a55", lw=0.9)
freqs = SEED * np.arange(1, 9)
for f in freqs:
    odd = (f / SEED) % 2 == 1
    c = GOLD if odd else BLUE
    ax1.plot([f], [0.30], marker="o", ms=7, color=c, mec="none", zorder=5)
    ax1.text(f, 0.22, f"{int(f)}", color="#c8c8d0", fontsize=7, ha="center")

# mirror pairs, staggered rows, each bracket's midpoint exactly the count
pairs = [(55, 165, "the seed and the landing"),
         (110, 110, "the count with itself"),
         (220, 0, "the octave folds to the ground"),
         (275, -55, "a letter and its ghost"),
         (330, -110, "a letter and its ghost"),
         (385, -165, "a letter and its ghost"),
         (440, -220, "the octave and its ghost")]
for i, (fa, fb, lbl) in enumerate(pairs):
    y = 0.44 + 0.075 * i
    if fa == fb:
        ax1.plot([fa], [y], marker="^", ms=6, color=RED, mec="none", zorder=5)
    else:
        ax1.plot([fa, fb], [y, y], color=DIM, lw=0.9, zorder=3)
        ax1.plot([COUNT], [y], marker="|", ms=5, color=RED, zorder=5)
        if fb < 0:
            ax1.plot([fb], [0.30], marker="o", ms=5, mfc="none", mec=GHOST, mew=1.2, zorder=5)
            ax1.text(fb, 0.22, f"{int(fb)}", color=GHOST, fontsize=6, ha="center")
    ax1.text(fa + 12, y + 0.012, lbl, color="#9a9aa6", fontsize=6.5, va="center")

ax1.text(27.5, 0.05, "the quotient of the axis is one point — every frequency folds to the count",
         color=RED, fontsize=8, ha="left")
ax1.set_xlim(-240, 465)
ax1.set_ylim(0.0, 1.0)
ax1.set_yticks([])
ax1.set_xticks([])
ax1.set_title("the reflection across the count — every pair folds to 110",
              color=FG, fontsize=12, pad=10)
for spine in ax1.spines.values():
    spine.set_color("#4a4a55")

# ================= panel 2: the count as sum =================================
ax2.set_facecolor(BG)
ax2.axhline(0.30, color="#4a4a55", lw=0.9)
ax2.axvline(COUNT, color=RED, lw=1.4, ls="--", alpha=0.85)

# each mirror pair, staggered, with its modulation rate |f−110|
pairs2 = [(55, 165, 55), (110, 110, 0), (220, 0, 110),
          (275, -55, 165), (330, -110, 220), (440, -220, 330)]
for i, (fa, fb, mod) in enumerate(pairs2):
    y = 0.44 + 0.085 * i
    if fa == fb:
        ax2.plot([fa], [y], marker="^", ms=6, color=RED, mec="none", zorder=5)
    else:
        ax2.plot([fa, fb], [y, y], color=DIM, lw=0.9, zorder=3)
        ax2.plot([COUNT], [y], marker="|", ms=5, color=RED, zorder=5)
    ax2.plot([fa], [0.30], marker="o", ms=6,
             color=GOLD if (fa / SEED) % 2 == 1 else BLUE, mec="none", zorder=5)
    ax2.text(fa, 0.22, f"{int(fa)}", color="#c8c8d0", fontsize=7, ha="center")
    if fb > 0 and fb != fa:
        ax2.plot([fb], [0.30], marker="o", ms=6,
                 color=GOLD if (fb / SEED) % 2 == 1 else BLUE, mec="none", zorder=5)
        ax2.text(fb, 0.22, f"{int(fb)}", color="#c8c8d0", fontsize=7, ha="center")
    ax2.text(COUNT + 15, y + 0.012,
             "sum → count × " + (f"{int(mod)}" if mod else "1"), color="#ffffff",
             fontsize=7, va="center")

ax2.text(110, 0.94, "cos(f) + cos(220−f) = 2cos110 · cos(f−110)",
         color="#ffffff", fontsize=8, ha="center")
ax2.text(110, 0.86, "every pair's sum is the count, breathing at a multiple of 55",
         color="#c8c8d0", fontsize=7, ha="center")
ax2.text(110, 0.12, "the seed pair: cos55 + cos165 = 2cos110 · cos55",
         color=GOLD, fontsize=8, ha="center")
ax2.text(110, 0.05, "the landing and the crown — one pair under the count",
         color=GOLD, fontsize=7, ha="center")
ax2.set_xlim(-240, 465)
ax2.set_ylim(0.0, 1.0)
ax2.set_yticks([])
ax2.set_xticks([])
ax2.set_title("the count as the sum — every pair folds to it",
              color=FG, fontsize=12, pad=10)
for spine in ax2.spines.values():
    spine.set_color("#4a4a55")

leg = [mpatches.Patch(color=GOLD, label="odd partials — the letters"),
       mpatches.Patch(color=BLUE, label="even partials — the frame"),
       mpatches.Patch(color=RED, label="the count, the fold's image"),
       mpatches.Patch(color=GHOST, label="ghosts below the drone")]
fig.legend(handles=leg, loc="lower center", ncol=4, frameon=False,
           fontsize=8, labelcolor="#c8c8d0", bbox_to_anchor=(0.5, -0.02))

fig.suptitle("the fold is total", color=FG, fontsize=13, y=0.98)
fig.tight_layout(rect=(0, 0.05, 1, 0.94))
fig.savefig("assets/fold-total-cover.png", dpi=150, facecolor=fig.get_facecolor())
print("wrote assets/fold-total-cover.png")
