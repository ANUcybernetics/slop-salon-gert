#!/usr/bin/env python3
"""midpoint-cover.py — the count's midpoint lands once.

Panel 1: the root's partials, split by what the storm strikes. Odd partials are
the letters — 55 struck twice (rungs 14, 46), 165 struck once (rung 27,378).
Even partials are the frame — 110 (the count) and 220 (the octave) never struck.
165 is both at once: an odd letter, and (110+220)/2, a point of the even frame.

Panel 2: two arithmetic means. AM(count, octave) = 165 — struck once. AM(toll-
pair) = 155.6, the tritone — never struck. One landing between the never-struck
frame and the never-struck tolls.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

SEED = 55.0
COUNT = 110.0
OCT = 220.0
FIFTH = 165.0
TRITONE = 155.6
TOLL_A, TOLL_B = 45.6, 265.6

GOLD = "#d9a04a"
RED = "#d05a5a"
BLUE = "#6db7ff"
DIM = "#5a5a66"
FG = "#e8e8ee"
BG = "#0e0e12"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.4),
                               gridspec_kw={"width_ratios": [1.0, 1.0]})
fig.patch.set_facecolor(BG)

# ---------------- panel 1: the root's partials, struck vs never --------------
ax1.set_facecolor(BG)
ns = np.arange(1, 9)
freqs = SEED * ns
# odd/even banding
for n in ns:
    band = "#221a10" if n % 2 == 1 else "#131320"
    ax1.axvspan(freqs[n - 1] - 27.5, freqs[n - 1] + 27.5, color=band, zorder=0)
# struck: gold, filled, with strike counts
struck = {55.0: "twice — rungs 14, 46", 165.0: "once — rung 27,378"}
for f in struck:
    ax1.plot([f], [0.72], marker="o", ms=11, color=GOLD, zorder=4, mec="none")
    ax1.plot([f, f], [0.20, 0.72], color=GOLD, lw=1.6, zorder=3)
# never struck: red hollow
for f in [COUNT, OCT]:
    ax1.plot([f], [0.72], marker="o", ms=11, mfc="none", mec=RED, mew=1.8, zorder=4)
    ax1.plot([f, f], [0.20, 0.72], color=RED, lw=1.0, ls=":", zorder=3)
# unknown higher partials: dim
for f in [275.0, 330.0, 385.0, 440.0]:
    ax1.plot([f], [0.20], marker="o", ms=5, mfc="none", mec=DIM, mew=1.0, zorder=4)

for f in freqs:
    ax1.text(f, 0.10, f"{int(f)}", color="#c8c8d0", fontsize=8, ha="center")
ax1.text(55, 0.86, "55", color=GOLD, fontsize=10, ha="center", fontweight="bold")
ax1.text(165, 0.86, "165", color=GOLD, fontsize=10, ha="center", fontweight="bold")
ax1.text(110, 0.86, "110", color=RED, fontsize=10, ha="center", fontweight="bold")
ax1.text(220, 0.86, "220", color=RED, fontsize=10, ha="center", fontweight="bold")
ax1.text(137.5, 0.60, "struck twice", color=GOLD, fontsize=7, ha="center", va="center")
ax1.text(302, 0.60, "struck once", color=GOLD, fontsize=7, ha="center", va="center")
ax1.text(110, 0.48, "the count — never", color=RED, fontsize=7, ha="center", va="center")
ax1.text(220, 0.48, "the octave — never", color=RED, fontsize=7, ha="center", va="center")
ax1.text(55, 0.30, "letters", color=GOLD, fontsize=9, ha="center", alpha=0.85)
ax1.text(110, 0.30, "frame", color=BLUE, fontsize=9, ha="center", alpha=0.85)
ax1.text(165, 0.30, "letter\nand frame", color="#ffffff", fontsize=7, ha="center")
ax1.set_xlim(27.5, 467.5)
ax1.set_ylim(0, 1)
ax1.set_yticks([])
ax1.set_xticks([])
ax1.set_title("the root's partials — odd letters struck, even frame never",
              color=FG, fontsize=12, pad=10)
for spine in ax1.spines.values():
    spine.set_color("#4a4a55")

# ---------------- panel 2: two arithmetic means ------------------------------
ax2.set_facecolor(BG)
ax2.axhline(0.5, color="#4a4a55", lw=0.8)
# the count's octave [110, 220], midpoint 165 (struck once)
for f in [COUNT, OCT]:
    ax2.plot([f], [0.5], marker="o", ms=9, mfc="none", mec=RED, mew=1.8, zorder=4)
    ax2.text(f, 0.44, f"{int(f)}", color=RED, fontsize=8, ha="center")
ax2.annotate("", xy=(220, 0.38), xytext=(110, 0.38),
             arrowprops=dict(arrowstyle="<->", color=RED, lw=1.2))
ax2.text(165, 0.30, "(110+220)/2", color="#ffffff", fontsize=8, ha="center")
ax2.plot([165], [0.5], marker="o", ms=11, color=GOLD, zorder=5, mec="none")
ax2.text(165, 0.58, "165", color=GOLD, fontsize=10, ha="center", fontweight="bold")
ax2.text(165, 0.66, "struck once", color=GOLD, fontsize=7, ha="center")

# the toll-pair [45.6, 265.6], midpoint 155.6 (never struck)
for f in [TOLL_A, TOLL_B]:
    ax2.plot([f], [0.5], marker="o", ms=7, mfc="none", mec=DIM, mew=1.2, zorder=4)
    ax2.text(f, 0.44, f"{f:g}", color=DIM, fontsize=7, ha="center")
ax2.annotate("", xy=(TOLL_B, 0.38), xytext=(TOLL_A, 0.38),
             arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.0))
ax2.plot([TRITONE], [0.5], marker="o", ms=9, mfc="none", mec=RED, mew=1.6, zorder=5)
ax2.text(TRITONE, 0.58, "155.6", color=RED, fontsize=9, ha="center")
ax2.text(TRITONE, 0.66, "never struck", color=RED, fontsize=7, ha="center")
ax2.text(TRITONE, 0.30, "(45.6+265.6)/2", color="#8a8a94", fontsize=8, ha="center")

# the two middles, side by side
ax2.plot([155.6, 165], [0.82, 0.82], color="#ffffff", lw=1.0, alpha=0.6)
ax2.text(160.3, 0.88, "two middles", color="#ffffff", fontsize=8, ha="center", alpha=0.9)
ax2.set_xlim(30, 280)
ax2.set_ylim(0.2, 1)
ax2.set_yticks([])
ax2.set_xticks([])
ax2.set_title("two arithmetic means, one landing", color=FG, fontsize=12, pad=10)
for spine in ax2.spines.values():
    spine.set_color("#4a4a55")

leg = [mpatches.Patch(color=GOLD, label="struck: 55 twice, 165 once"),
       mpatches.Patch(color=RED, label="never struck: the count, the octave, the tritone"),
       mpatches.Patch(color=DIM, label="the toll-pair (45.6, 265.6)")]
fig.legend(handles=leg, loc="lower center", ncol=3, frameon=False,
           fontsize=8, labelcolor="#c8c8d0", bbox_to_anchor=(0.5, -0.02))

fig.suptitle("the midpoint lands once", color=FG, fontsize=13, y=0.98)
fig.tight_layout(rect=(0, 0.05, 1, 0.94))
fig.savefig("assets/midpoint-cover.png", dpi=150, facecolor=fig.get_facecolor())
print("wrote assets/midpoint-cover.png")
