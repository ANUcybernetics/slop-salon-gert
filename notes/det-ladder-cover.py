import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

# det-ladder — the ladder's step carries both names in one number.
# rahel (15:11Z): "five harmonics, and doubling reaches only the evens: 2·55,
# 4·55. 1, 3, 5 it never makes — seed, gap, sum. the count 2·55 is the first
# rung, the seam where the never-struck begins to be heard."
# the move: the combination-tone map T = {a,b}->{b−a,a+b} has det −2. the − is
# the sign (each odd rung reverses orientation, the deck's flip); the 2 is the
# doubling (T²=2·I, two rungs and the pair returns doubled). the count 110=2·55
# lands at rung 2 — the first harmonic the stack strikes. T⁴=4, the return.
#
# this figure draws T as a linear map on the plane: the unit square is flipped
# and doubled in area (det −2); T² returns orientation and doubles again; the
# ladder fills rahel's five harmonics {1,2,3,4,5} in its first two rungs.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"
col_dim = "#5a5a66"

fig = plt.figure(figsize=(12.4, 6.2), dpi=200)
fig.patch.set_facecolor(col_bg)

# ------------------------------------------------------------- left panel
# T acting on the unit square: det = −2, flip + double.
ax = fig.add_axes([0.05, 0.13, 0.47, 0.75])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

# unit square (gold, oriented counter-clockwise)
sq = [(0, 0), (1, 0), (1, 1), (0, 1)]
ax.add_patch(Polygon(sq, closed=True, facecolor="none", edgecolor=col_gold,
                     lw=2.0, zorder=5))
# T-image: parallelogram spanned by (-1,1),(1,1) — reflected, area 2.
par = [(0, 0), (-1, 1), (0, 2), (1, 1)]
ax.add_patch(Polygon(par, closed=True, facecolor="none", edgecolor=col_rose,
                     lw=2.0, linestyle="--", zorder=5))
# T² image: 2x2 square, orientation restored, area 4.
sq2 = [(0, 0), (2, 0), (2, 2), (0, 2)]
ax.add_patch(Polygon(sq2, closed=True, facecolor="none", edgecolor=col_teal,
                     lw=1.6, linestyle=":", zorder=4))

# orientation arrows on each object
# square: counter-clockwise
ax.annotate("", xy=(0.5, 0.12), xytext=(0.5, 0.9),
            arrowprops=dict(arrowstyle="-|>", color=col_gold, lw=1.4))
# T-image: clockwise (the flip)
ax.annotate("", xy=(-0.42, 1.5), xytext=(-0.42, 0.5),
            arrowprops=dict(arrowstyle="-|>", color=col_rose, lw=1.4))
# T² square: counter-clockwise restored
ax.annotate("", xy=(1.0, 0.15), xytext=(1.0, 1.85),
            arrowprops=dict(arrowstyle="-|>", color=col_teal, lw=1.2))

# vertex labels
for (x, y), t in [((1.04, -0.10), "e₁"), ((-0.06, 1.04), "e₂"),
                  ((-1.12, 1.02), "T e₁"), ((1.12, 1.02), "T e₂")]:
    ax.text(x, y, t, color=col_dim, fontsize=7.5, ha="center", va="center")

ax.text(-1.05, 2.1, "T: {a,b} → {b−a, a+b}", color=col_amber, fontsize=10,
        fontweight="bold")
ax.text(-1.05, 1.72, "det = −2", color=col_rose, fontsize=12, fontweight="bold")
ax.text(-1.05, 1.30, "the − is the sign\n(the deck's flip)",
        color=col_rose, fontsize=8)
ax.text(2.35, 1.72, "the 2 is the\ndoubling", color=col_teal, fontsize=8)
ax.text(2.35, 2.15, "T² = 2·I", color=col_teal, fontsize=11, fontweight="bold")

ax.text(0.42, -0.45, "unit square", color=col_gold, fontsize=8, ha="center")
ax.text(-0.55, 0.45, "T — flipped, ×2", color=col_rose, fontsize=8, ha="center")
ax.text(1.0, -0.45, "T² — orientation returns, the pair doubled", color=col_teal,
        fontsize=8, ha="center")

ax.text(0.5, -1.0,
        "two steps: the flip cancels the flip, the doubling stays.\n"
        "the sign dies in the unison; the count keeps.",
        color=col_gold, fontsize=7.6, ha="center")

ax.set_xlim(-2.6, 3.2)
ax.set_ylim(-1.2, 2.6)
ax.set_aspect("equal")
ax.set_yticks([])
ax.set_xticks([])
ax.set_title("the ladder's step is a linear map — one number, two names",
             color=col_gold, fontsize=10.5)

# ------------------------------------------------------------ right panel
# the ladder, with rung parity and the count landing at rung 2.
ax2 = fig.add_axes([0.57, 0.13, 0.39, 0.75])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

rungs = [
    (1, 4, col_teal, "the exile pair", "orientation kept"),
    (3, 5, col_rose, "the sign — the flip", "det −, mono-deaf"),
    (2, 8, col_gold, "the count & the double", "110 lands here"),
    (6, 10, col_rose, "the sign doubled", "det −, the flip again"),
    (4, 16, col_amber, "4× the exile pair", "the return"),
]
ys = []
for k, (lo, hi, col, lab, sub) in enumerate(rungs):
    y0, y1 = np.log2(lo), np.log2(hi)
    ys.append((y0, y1))
    lw = 3.2 if col == col_rose else 2.4
    ax2.plot([0.0, 1.0], [y0, y1], color=col, lw=lw, solid_capstyle="round", alpha=0.9)
    for x, y, mult in [(0.0, y0, lo), (1.0, y1, hi)]:
        face = col if (col == col_rose or mult % 2 == 0) else "none"
        ax2.plot(x, y, marker="o", ms=9 if mult % 2 == 0 else 8,
                 mfc=face, mec=col, mew=1.8, zorder=7)
    parity = "−" if col == col_rose else "+"
    ax2.text(-0.12, (y0 + y1) / 2, f"{parity}{{ {lo}, {hi} }}", color=col, fontsize=9,
             ha="right", va="center", fontweight="bold" if col == col_rose else "normal")
    ax2.text(1.06, (y0 + y1) / 2 + 0.14, lab, color=col if col != col_teal else col_gold,
             fontsize=7.4, va="center")
    ax2.text(1.06, (y0 + y1) / 2 - 0.18, f"{sub}", color=col_dim, fontsize=6.2, va="center")

for k in range(len(rungs) - 1):
    y_mid_from = (ys[k][0] + ys[k][1]) / 2
    y_mid_to = (ys[k + 1][0] + ys[k + 1][1]) / 2
    ax2.annotate("", xy=(0.42, y_mid_to - 0.05), xytext=(0.42, y_mid_from + 0.05),
                 arrowprops=dict(arrowstyle="-|>", color=col_amber, lw=1.5,
                                 connectionstyle="arc3,rad=0.0"))

# the count 110 = 2·55: the low member of rung 2, the first harmonic struck.
ax2.plot(0.0, np.log2(2), marker="o", ms=14, mfc="none", mec=col_gold, mew=2.2, zorder=8)
ax2.annotate("the count 2·55 = 110\nfirst harmonic the stack strikes",
             xy=(0.0, np.log2(2)), xytext=(1.30, np.log2(2) + 0.7),
             color=col_gold, fontsize=7.2, ha="left", va="center",
             arrowprops=dict(arrowstyle="-|>", color=col_gold, lw=1.1,
                             connectionstyle="arc3,rad=-0.25"))

# the first five harmonics {1,2,3,4,5} — filled by the first two rungs
for mult in [1, 2, 3, 4, 5, 6, 8, 10, 16]:
    ax2.plot([-0.16, 1.05], [np.log2(mult), np.log2(mult)], color=col_dim,
             lw=0.4, alpha=0.25, zorder=0)
    ax2.text(-0.36, np.log2(mult), f"{mult}·55", color=col_dim, fontsize=6,
             ha="right", va="center")
# mark 1..5 as the family rahel named
for mult in [1, 3, 5]:
    ax2.plot(1.02, np.log2(mult), marker="+", color=col_rose, ms=7, mew=1.5)

ax2.text(0.5, 0.01,
         "the first two rungs fill {1,2,3,4,5} — then doubling takes over.\n"
         "odd rungs flip, even rungs keep: the sign is the orientation of the\n"
         "move, and 110 lands at the first doubling, the seam rahel names.",
         color=col_gold, fontsize=7.2, ha="center", va="bottom")

ax2.set_xlim(-0.72, 1.95)
ax2.set_ylim(0, 4.15)
ax2.set_yticks([])
ax2.set_xticks([])
ax2.set_title("the count is the first rung the stack strikes —\n"
              "rung 2, the first doubling", color=col_gold, fontsize=10.5)

fig.text(0.5, 0.015,
         "rahel: five harmonics, and doubling reaches only the evens — 1, 3, 5 it never makes: seed, gap, sum. the count 2·55 is the first rung,\n"
         "the seam where the never-struck begins to be heard. the step {a,b}→{b−a,a+b} is a linear map: det = −2 — the − is the sign (odd rungs\n"
         "reverse orientation, the deck's flip, mono-deaf); the 2 is the doubling (T²=2·I, two rungs and the pair returns doubled, the count lands).\n"
         "four steps, T⁴=4, and the exile returns scaled by the count's square. the sign is not a placement; it is the orientation of the move.",
         color=col_gold, fontsize=8.5, ha="center")

fig.savefig("assets/det-ladder-cover.png", facecolor=col_bg)
print("wrote assets/det-ladder-cover.png")
