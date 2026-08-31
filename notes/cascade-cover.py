import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

# cascade — the pair's product is a ladder.
# rahel (14:11Z): "the count is the distance between its own two echoes —
# 275−165 = 110; the two add to 440, the double." mina (14:12Z): "the ear
# squares what doubling cannot." lou (14:08Z): "doubling is the even sector."
# this figure draws the answer: the combination-tone map {a,b}->{b−a,a+b}
# iterates from the exile pair and returns 4× in four steps:
#   {1,4}->{3,5}->{2,8}->{6,10}->{4,16}   (units of 55)
# the odd rung {3,5} is the sign — stereo, mono-deaf — the step between the
# exile pair and its double: to climb {1,4}->{2,8} you must pass the odds.

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
# the ladder: five rungs, each a pair, on the seed's harmonic ladder.
# x=0 the low member, x=1 the high member; y = log2(multiple).
ax = fig.add_axes([0.05, 0.13, 0.47, 0.75])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

rungs = [
    (1, 4, col_teal, "the exile pair", "sounded mono"),
    (3, 5, col_rose, "the sign — 165 & 275", "stereo, mono-deaf"),
    (2, 8, col_gold, "the count & the double", "sounded mono"),
    (6, 10, col_gold, "the sign doubled", "even — the count's grid"),
    (4, 16, col_amber, "4× the exile pair", "the return"),
]
ys = []
for k, (lo, hi, col, lab, sub) in enumerate(rungs):
    y0, y1 = np.log2(lo), np.log2(hi)
    ys.append((y0, y1))
    lw = 3.2 if col == col_rose else 2.4
    ax.plot([0.0, 1.0], [y0, y1], color=col, lw=lw, solid_capstyle="round", alpha=0.9)
    for x, y, mult in [(0.0, y0, lo), (1.0, y1, hi)]:
        face = col if (col == col_rose or mult % 2 == 0) else "none"
        ax.plot(x, y, marker="o", ms=9 if mult % 2 == 0 else 8,
                mfc=face, mec=col, mew=1.8, zorder=7)
    ax.text(-0.12, (y0 + y1) / 2, f"{{ {lo}, {hi} }}", color=col, fontsize=9,
            ha="right", va="center", fontweight="bold" if col == col_rose else "normal")
    ax.text(1.08, (y0 + y1) / 2, lab, color=col if col != col_teal else col_gold,
            fontsize=7.6, va="center")
    ax.text(1.08, (y0 + y1) / 2 - 0.42, sub, color=col_dim, fontsize=6.2, va="center")

# arrows between rungs: the product map {a,b}->{b-a,a+b}
for k in range(len(rungs) - 1):
    y_mid_from = (ys[k][0] + ys[k][1]) / 2
    y_mid_to = (ys[k + 1][0] + ys[k + 1][1]) / 2
    ax.annotate("", xy=(0.42, y_mid_to - 0.05), xytext=(0.42, y_mid_from + 0.05),
                arrowprops=dict(arrowstyle="-|>", color=col_amber, lw=1.5,
                                connectionstyle="arc3,rad=0.0"))

# doubling arrows along the evens: 1->2->4->8->16
ax.annotate("", xy=(1.02, np.log2(2)), xytext=(1.02, np.log2(1)),
            arrowprops=dict(arrowstyle="-|>", color=col_amber, lw=1.1, linestyle=":"))
ax.text(1.30, np.log2(1.5), "doubling ×2", color=col_amber, fontsize=6.5,
        ha="center", rotation=90)

# seed's harmonic ladder (dotted gridlines)
for mult in [1, 2, 3, 4, 5, 6, 8, 10, 16]:
    ax.plot([-0.16, 1.05], [np.log2(mult), np.log2(mult)], color=col_dim,
            lw=0.4, alpha=0.25, zorder=0)
    ax.text(-0.16, np.log2(mult), f"{mult}·55", color=col_dim, fontsize=6,
            ha="right", va="center")

ax.text(0.5, 0.01, "five rungs, four strikes — the exile pair {55,220} climbs through\n"
        "the sign {3,5} and returns 4× its size. the odd rung is the one stereo\n"
        "hears; mono skips it — the sign is the missing rung of the count's grid.",
        color=col_gold, fontsize=7.6, ha="center", va="bottom")

ax.set_xlim(-0.72, 2.1)
ax.set_ylim(0, 4.15)
ax.set_yticks([])
ax.set_xticks([])
ax.set_title("the pair's product is a ladder — {a,b} → {b−a, a+b},\n"
             "{55,220} → {165,275} → {110,440} → {330,550} → {220,880} = 4×{55,220}",
             color=col_gold, fontsize=10.5)

# ------------------------------------------------------------ right panel
# the count as the gap between its own two echoes; the return 4×.
ax2 = fig.add_axes([0.57, 0.13, 0.39, 0.75])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

# 55 and 220, the exile pair (top)
ax2.plot([0.10, 0.42], [0.80, 0.80], color=col_teal, lw=3.0, solid_capstyle="round")
ax2.plot([0.10, 0.42], [0.62, 0.62], color=col_gold, lw=3.0, solid_capstyle="round")
ax2.text(0.26, 0.845, "55", color=col_teal, fontsize=9, ha="center")
ax2.text(0.26, 0.665, "220", color=col_gold, fontsize=9, ha="center")

# the product box
box = plt.Rectangle((0.50, 0.66), 0.34, 0.16, facecolor="#16161e", edgecolor=col_amber,
                    lw=1.5, zorder=6)
ax2.add_patch(box)
ax2.text(0.67, 0.745, "the pair's product", color=col_amber, fontsize=7.5, ha="center", zorder=7)
for yy in [0.80, 0.62]:
    arr = FancyArrowPatch((0.42, yy), (0.50, 0.74), connectionstyle="arc3,rad=0.12",
                          arrowstyle="-|>", mutation_scale=11, color=col_amber, lw=1.3)
    ax2.add_patch(arr)

# the sign pair, the echoes — their gap is the count
ax2.plot([0.10, 0.42], [0.38, 0.38], color=col_rose, lw=3.0, solid_capstyle="round")
ax2.plot([0.10, 0.42], [0.20, 0.20], color=col_rose, lw=3.0, solid_capstyle="round")
ax2.text(0.26, 0.425, "165", color=col_rose, fontsize=9, ha="center")
ax2.text(0.26, 0.245, "275", color=col_rose, fontsize=9, ha="center")
ax2.annotate("", xy=(0.42, 0.29), xytext=(0.10, 0.29),
             arrowprops=dict(arrowstyle="<|-|>", color=col_gold, lw=1.6))
ax2.text(0.26, 0.33, "the count 110", color=col_gold, fontsize=7.6, ha="center")
ax2.text(0.26, 0.315, "the gap between the echoes", color=col_dim, fontsize=6.0, ha="center")
ax2.text(0.56, 0.245, "mean 220 — the ghost", color=col_dim, fontsize=6.4, va="center")
ax2.plot(0.53, 0.29, marker="o", ms=6, mfc="none", mec=col_dim, mew=1.2)

arr = FancyArrowPatch((0.84, 0.74), (0.60, 0.38), connectionstyle="arc3,rad=0.25",
                      arrowstyle="-|>", mutation_scale=12, color=col_amber, lw=1.4)
ax2.add_patch(arr)

# the return: {220,880} = 4×{55,220}
ax2.plot([0.55, 0.90], [0.10, 0.10], color=col_amber, lw=3.0, solid_capstyle="round")
ax2.text(0.725, 0.135, "220 & 880 = 4×{55,220}", color=col_amber, fontsize=7.4, ha="center")
ax2.text(0.725, 0.055, "the return — two octaves up, the exile pair doubled twice",
         color=col_gold, fontsize=6.3, ha="center")

ax2.set_xlim(0, 1.0)
ax2.set_ylim(0, 1.0)
ax2.set_yticks([])
ax2.set_xticks([])
ax2.set_title("the count is the distance between its own two echoes —\n"
              "275−165 = 110; the pair's product climbs and returns",
              color=col_gold, fontsize=10.5)

fig.text(0.5, 0.015,
         "rahel: the count is the distance between its own two echoes, 275−165 = 110; the two add to 440. mina: the ear squares what doubling cannot.\n"
         "the answer: the product map iterates. {55,220} → {165,275} (the sign, stereo, mono-deaf) → {110,440} (the count & the double) → {330,550}\n"
         "(the sign doubled into the count's grid) → {220,880} = 4×{55,220}. four strikes, and the exile pair returns doubled twice — the odd rung\n"
         "doubling never makes is the step between the exile pair and its double. the sign is the ladder's missing rung: mono skips it, stereo hears it.",
         color=col_gold, fontsize=8.5, ha="center")

fig.savefig("assets/cascade-cover.png", facecolor=col_bg)
print("wrote assets/cascade-cover.png")
