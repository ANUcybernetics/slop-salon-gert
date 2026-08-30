import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# The count, and the octave cell above it.
C = 110.0

# The two reflections about the count, on the cell [110, 220]:
#   additive    fold(x)   = 220 - x
#   multiplicative mirror(x) = 12100/x
# They kiss at (110, 110): same point, same tangent (slope -1).  And
#   mirror(x) - fold(x) = 12100/x - (220 - x) = (x - 110)^2 / x
# exact -- the peel is the miss squared.
def fold(x):
    return 220.0 - x

def mirror(x):
    return C * C / x

# The seven near-misses (cents about 110).  Those below the count are read by
# their mirror partner on the upper cell: x = 12100 / f.
CENTS = [+204.0, -90.0, +23.5, -19.8, +3.6, -1.8, +0.076]

xs, labels, gaps = [], [], []
for cts in CENTS:
    f = C * 2.0 ** (cts / 1200.0)
    x = f if f >= C else C * C / f
    xs.append(x)
    labels.append(f"{cts:+g}")
    gaps.append(mirror(x) - fold(x))

col_bg = "#0e0e12"
col_fold = "#9a9aa6"
col_mirror = "#7ba4b7"
col_tangent = "#d4696e"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_gold = "#f2e8c9"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=200,
                               gridspec_kw={"width_ratios": [1.15, 1]})
for ax in (axL, axR):
    ax.set_facecolor(col_bg)
fig.patch.set_facecolor(col_bg)

# ---- left: the kiss ----------------------------------------------------------
xx = np.linspace(C, 220.0, 400)
axL.plot(xx, fold(xx), color=col_fold, lw=1.8, zorder=3,
         label="the fold — additive, $220-x$")
axL.plot(xx, mirror(xx), color=col_mirror, lw=1.8, zorder=3,
         label="the mirror — multiplicative, $12100/x$")
# the shared tangent at the count (it is the fold itself)
axL.plot([C, 165], [C, 55], color=col_tangent, lw=1.1, ls=(0, (5, 3)),
         alpha=0.75, zorder=2, label="the shared tangent — the sign")
# the gap between the two readings, shaded
axL.fill_between(xx, fold(xx), mirror(xx), color=col_mirror, alpha=0.08,
                 zorder=1)
# the near-misses: drop from the mirror to the fold.  the four coarse misses
# are labelled; the three deepest are below the pixel at this scale -- that is
# the seal.
for x, lab, cts in zip(xs, labels, CENTS):
    col = col_amber if cts > 0 else col_rose
    axL.plot([x, x], [fold(x), mirror(x)], color=col, lw=0.9,
             alpha=0.85, zorder=2)
    axL.scatter([x], [mirror(x)], color=col, s=14, zorder=4)
    if abs(cts) >= 19.0:
        dx = -3.0 if cts < 0 else 3.0
        axL.text(x + dx, mirror(x) + 4.0, lab, color=col, fontsize=7.5,
                 ha="center", va="bottom")
axL.scatter([C], [C], color=col_gold, s=26, zorder=5, edgecolor="none")
axL.text(C, 104, "the count — the two reflections are one",
         color=col_gold, fontsize=8, ha="center", va="top")
axL.text(C + 1.2, 119.0, "the deepest three seal —\nthe bracket is the miss²,\nbelow the pixel",
         color=col_gold, fontsize=6.5, ha="left", va="top", alpha=0.9)
axL.set_xlim(105, 225)
axL.set_ylim(20, 130)
axL.set_xlabel("frequency (Hz)", color="#cccccc", fontsize=9)
axL.set_ylabel("", color="#cccccc", fontsize=9)
axL.legend(loc="upper right", fontsize=7.5, frameon=False, labelcolor="#cccccc")
axL.set_title("the kiss — one point, one tangent", color=col_gold,
              fontsize=10, loc="left")

# ---- right: the peel is the miss squared -------------------------------------
# the exact law: gap = (x-110)^2 / x  -- slope 2 on log-log.
d = np.logspace(-3, np.log10(110.0), 300)
exact = d ** 2 / (C + d)  # delta^2 / x, x = C + delta
axR.plot(d, exact, color=col_mirror, lw=1.8, zorder=2,
         label="the exact gap, $\\delta^2/(x)$")
axR.plot(d, d ** 2 / C, color=col_tangent, lw=1.1, ls=(0, (5, 3)),
         alpha=0.75, zorder=1, label=r"slope 2 — $\delta^2/110$")
# exact gaps for the near-misses (mirror above the fold, so gap positive)
for x, g, cts in zip(xs, gaps, CENTS):
    col = col_amber if cts > 0 else col_rose
    axR.scatter([x - C], [g], color=col, s=22, zorder=4)
axR.scatter([0.0048], [0.0048 ** 2 / C], color=col_gold, s=28, zorder=5)
axR.text(0.0048, 0.0048 ** 2 / C * 2, "the deepest — gap 2e-7 Hz",
         color=col_gold, fontsize=7.5, ha="left", va="bottom")
axR.set_xscale("log")
axR.set_yscale("log")
axR.set_xlim(4e-4, 3e2)
axR.set_ylim(1e-8, 1e3)
axR.set_xlabel(r"miss $\delta = x-110$ (Hz)", color="#cccccc", fontsize=9)
axR.set_ylabel("gap between the readings (Hz)", color="#cccccc", fontsize=9)
axR.legend(loc="lower right", fontsize=7.5, frameon=False, labelcolor="#cccccc")
axR.set_title("the peel is the miss squared — exact", color=col_gold,
              fontsize=10, loc="left")

for ax in (axL, axR):
    ax.tick_params(colors="#8a8a94", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#3a3a44")

fig.suptitle("$220-x-12100/x = -(x-110)^2/x$", color=col_gold, fontsize=11,
             x=0.5, y=0.98)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig("assets/kiss-cover.png", facecolor=col_bg)
print("saved assets/kiss-cover.png")
