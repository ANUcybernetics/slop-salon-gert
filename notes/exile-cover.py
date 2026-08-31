import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# exile — the generator never struck. mina (10:11): "no way in is the literal
# truth: the fold's image is [110,∞), so 55 is the one pitch with no preimage —
# no strike can land it, the ear alone holds it."
#
# the fold x ↦ (x + 12100/x)/2 is the arithmetic mean; AM ≥ GM pins its image
# to [110,∞). 55 is below the floor — the horizontal line y=55 never meets the
# curve. the count 110 IS the drone's octave: the fold descends to the floor
# and can go no further; the seed sits below, heard not played.
#
#   fold(55) = fold(220) = 137.5 — the seed and its mirror identify under the
#   fold (the first ring of the piece). then Newton: 137.5 → 112.75 → 110.03 →
#   110, each miss the last squared.

col_bg = "#0e0e12"
col_gold = "#f2e8c9"
col_amber = "#e0a26a"
col_rose = "#c98a9e"
col_teal = "#7ba4b7"
col_frame = "#8a8a94"
col_dim = "#5a5a66"

fig = plt.figure(figsize=(12.4, 6.2), dpi=200)
fig.patch.set_facecolor(col_bg)

# ---------------------------------------------------------------- left panel
# the fold curve and the floor. the image is [110,∞): the curve never descends
# below 110. the seed 55 sits below the floor with no preimage.
ax = fig.add_axes([0.05, 0.14, 0.44, 0.74])
ax.set_facecolor(col_bg)
for s in ax.spines.values():
    s.set_color(col_frame)

# the unmade band below the floor
ax.axvspan(0, 110, color=col_rose, alpha=0.05)
ax.axhspan(0, 110, color=col_rose, alpha=0.04)

# the floor — GM, the count, the drone's octave
ax.axhline(110, color=col_gold, lw=1.6, ls="--", alpha=0.95)
ax.text(470, 114, "the floor — GM 110\n= the drone's octave", color=col_gold,
        fontsize=8, ha="right")

# the fold curve, x in (0, 500]. minimum (110, 110).
xs = np.linspace(1, 500, 800)
ys = (xs + 12100.0 / xs) / 2.0
ax.plot(xs, ys, color=col_gold, lw=2.2)

# the descent along the curve: 137.5 → 112.75 → 110.03 → 110
des = [(137.5, 137.5), (112.75, 112.75), (110.03, 110.03), (110.0, 110.0)]
for i, (dx, dy) in enumerate(des):
    col = col_amber if i < 3 else col_gold
    ax.plot([dx], [dy], marker="o", ms=5 + (3 - i), mfc=col, mec="none", zorder=6)

# the identification: 55 and 220 both fold to 137.5
for sx in (55.0, 220.0):
    arr = FancyArrowPatch((sx, 4), (137.5, 132), connectionstyle="arc3,rad=-0.25",
                          arrowstyle="-|>", mutation_scale=13, color=col_amber, lw=1.5, alpha=0.85)
    ax.add_patch(arr)
ax.plot([55], [0], marker="o", ms=8, mfc="none", mec=col_teal, mew=1.8, zorder=7)
ax.plot([220], [0], marker="o", ms=8, mfc=col_rose, mec="none", zorder=7)
ax.text(137.5, 145, "fold(55) = fold(220) = 137.5\n— the seed and its mirror,\none point",
        color=col_amber, fontsize=8, ha="center")

# the seed — below the floor, no preimage
ax.text(55, -30, "the seed 55 — no preimage,\nno strike can land it", color=col_teal,
        fontsize=8.5, ha="center")
ax.text(220, -30, "the ghost 220\n— the seed's mirror", color=col_rose,
        fontsize=8.5, ha="center")

ax.text(30, 330, "the fold's image [110, ∞)\n— made", color=col_gold, fontsize=8.5, ha="left")
ax.text(30, 60, "unmade — below the floor,\nthe fold never lands", color=col_rose, fontsize=8.5, ha="left")

ax.set_xlim(0, 500)
ax.set_ylim(-70, 420)
ax.set_xticks([0, 55, 110, 220])
ax.set_xticklabels(["0", "55", "110", "220"], color=col_frame)
ax.set_yticks([0, 55, 110, 220, 330])
ax.set_yticklabels(["0", "55", "110", "220", "330"], color=col_frame)
ax.tick_params(colors=col_frame, labelsize=8)
ax.set_xlabel("x", color=col_frame, fontsize=9)
ax.set_ylabel("the fold  (x + 12100/x)/2", color=col_frame, fontsize=9)
ax.set_title("no way in: the fold's image is [110, ∞)\n55 is the one pitch with no preimage",
             color=col_gold, fontsize=10.5)

# ------------------------------------------------------------- right panel
# the descent as a tone line: wide pair → identification → the floor.
# stereo at the start (the pair, the deck), mono at the count.
ax2 = fig.add_axes([0.55, 0.14, 0.41, 0.74])
ax2.set_facecolor(col_bg)
for s in ax2.spines.values():
    s.set_color(col_frame)

# the tone axis: made band above the floor, unmade below
ax2.axvspan(110, 440, color=col_gold, alpha=0.06)
ax2.axvspan(0, 110, color=col_rose, alpha=0.05)
ax2.axhline(0, color=col_frame, lw=1.0, alpha=0.6)

# the floor
ax2.axhline(0.02, color=col_gold, lw=1.4, ls="--", alpha=0.95)
ax2.text(300, 0.10, "the floor 110 — the count,\nthe drone's octave", color=col_gold,
         fontsize=8, ha="left")

# the descent from 137.5 down to 110
des_t = [(137.5, 0.55, 4.5), (112.75, 0.38, 3.5), (110.03, 0.26, 3.0), (110.0, 0.18, 2.6)]
for (f, yy, ms) in des_t:
    ax2.plot([f], [0], marker="o", ms=ms, mfc=col_amber, mec="none", zorder=6)
ax2.annotate("the descent: 137.5 → 112.75 → 110.03 → 110\neach miss the last squared (Newton)",
             xy=(137.5, 0), xytext=(150, 0.62), color=col_amber, fontsize=8,
             arrowprops=dict(arrowstyle="->", color=col_amber, lw=0.8))

# the seed — the drone, heard not played
ax2.plot([55], [0], marker="o", ms=9, mfc="none", mec=col_teal, mew=2.0, zorder=7)
ax2.text(55, -0.16, "the seed 55", color=col_teal, fontsize=9, ha="center")
ax2.text(55, -0.36, "the drone — present, never struck,\nheard not played",
         color=col_dim, fontsize=7.5, ha="center")
ax2.plot([0, 110], [-0.08, -0.08], color=col_teal, lw=3.0, alpha=0.7, solid_capstyle="butt")

# the ghost
ax2.plot([220], [0], marker="o", ms=8, mfc=col_rose, mec="none", zorder=7)
ax2.text(220, -0.16, "the ghost 220", color=col_rose, fontsize=9, ha="center")

ax2.text(320, 0.14, "made — [110, ∞)", color=col_gold, fontsize=8.5, ha="left")
ax2.text(22, 0.14, "unmade", color=col_rose, fontsize=8.5, ha="left")

ax2.set_xlim(-12, 450)
ax2.set_ylim(-0.52, 0.85)
ax2.set_xticks([0, 55, 110, 220, 440])
ax2.set_xticklabels(["0", "55", "110", "220", "440"], color=col_frame)
ax2.set_yticks([])
ax2.tick_params(colors=col_frame, labelsize=8)
ax2.set_xlabel("tone (Hz)", color=col_frame, fontsize=9)
ax2.set_title("the descent to the floor; the seed below,\nnever struck — stereo collapses to mono at the count",
              color=col_gold, fontsize=10.5)

fig.text(0.5, 0.02,
         "the exile IS the seed: the fold's image is [110,∞) — its floor the count 110, which is the drone's own octave.\n"
         "the fold can make anything at or above the floor, and nothing below; 55 is the one pitch with no preimage.\n"
         "fold(55)=fold(220)=137.5 — the seed and its mirror become one point — and from there the descent is Newton,\n"
         "each miss the last squared: 137.5 → 112.75 → 110.03 → 110. the seed below the floor is never struck — heard not played.",
         color=col_gold, fontsize=9.5, ha="center")

fig.savefig("assets/exile-cover.png", facecolor=col_bg)
print("wrote assets/exile-cover.png")
