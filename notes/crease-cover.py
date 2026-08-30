import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# The kiss, read as a paper fold.  fold(x) = 220 - x is a reflection about the
# count 110; mirror(x) = 12100/x is an inversion about it.  At x=110 both pass
# through (110,110) with slope -1 -- first order agree, second order part.
# That shared tangent is the crease: the invariant neither diagonal carries.

C = 110.0
xs = np.linspace(40, 200, 600)
fold = 220.0 - xs
mirror = 12100.0 / xs

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_mirror = "#7ba4b7"
col_frame = "#8a8a94"
col_rose = "#c98a9e"

fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=200)
ax.set_facecolor(col_bg)
fig.patch.set_facecolor(col_bg)

# the crease: a vertical fold line at the count, soft shadow either side
ax.axvline(C, color=col_gold, lw=1.4, zorder=5, alpha=0.9)
for x0 in (C - 5, C + 5):
    ax.axvline(x0, color=col_gold, lw=10, alpha=0.045, zorder=1)
ax.axvline(C, color=col_gold, lw=34, alpha=0.06, zorder=1)

# left half of the sheet: the fold (reflection)
mask_l = xs <= C
ax.plot(xs[mask_l], fold[mask_l], color=col_gold, lw=2.2, zorder=4)
# right half of the sheet: the mirror (inversion)
mask_r = xs >= C
ax.plot(xs[mask_r], mirror[mask_r], color=col_amber, lw=2.2, zorder=4)

# the shared tangent at the kiss: both agree to first order, slope -1
tt = np.linspace(70, 150, 2)
ax.plot(tt, 220.0 - tt, color=col_frame, lw=0.9, ls=(0, (3, 3)), alpha=0.8,
        zorder=3)

# the kiss point
ax.scatter([C], [C], s=60, facecolor="none", edgecolor=col_rose, lw=1.8,
           zorder=6)

# labels
ax.text(C + 2, 168, "the crease — the count, 110", color=col_gold,
        fontsize=9, ha="left", va="center", rotation=90)
ax.text(78, 120, "fold: 220 − x", color=col_gold, fontsize=10, ha="center",
        va="bottom")
ax.text(143, 96, "mirror: 12100/x", color=col_amber, fontsize=10, ha="center",
        va="bottom")
ax.text(120, 158, "the kiss — first order agree", color=col_rose, fontsize=8,
        ha="center", va="bottom")
ax.text(120, 148, "(both slope −1 at 110)", color=col_frame, fontsize=7.5,
        ha="center", va="bottom")
ax.text(120, 196, "second order part", color=col_frame, fontsize=7.5,
        ha="center", va="bottom")
ax.text(C, 40, "the sign lives on the crease —\nno diagonal carries it",
        color=col_gold, fontsize=8.5, ha="center", va="top")

ax.set_xlim(40, 200)
ax.set_ylim(40, 200)
ax.set_xlabel("pitch (Hz)", color="#cccccc", fontsize=9)
ax.set_ylabel("pitch (Hz)", color="#cccccc", fontsize=9)
ax.set_title("the kiss is a fold — the crease knows what the diagonal was for",
             color=col_gold, fontsize=10.5, loc="left")
ax.tick_params(colors="#8a8a94", labelsize=8)
for spine in ax.spines.values():
    spine.set_color("#3a3a44")

fig.tight_layout()
fig.savefig("assets/crease-cover.png", facecolor=col_bg)
print("saved assets/crease-cover.png")
