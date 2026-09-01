#!/usr/bin/env python3
"""Cover: the count as the side of a square, the tritone as its diagonal.

lelia's triangle: right isoceles, legs = count 110, hypotenuse = tritone
110*sqrt(2) = 155.6, excess (hyp - leg) = toll 45.6 = 110(sqrt(2)-1).
diagonal + side = 265.6 = upper = 110(sqrt(2)+1).

The constellation verified numerically:
  toll + count = tritone       (45.6 + 110 = 155.6)   the ladder
  tritone + count = upper      (155.6 + 110 = 265.6)   step = count
  toll * upper = count^2       (mirror: GM of the ends is the count)
  tritone = AM(toll, upper)    (the arithmetic center)
  tritone = GM(count, octave)  (110*sqrt(2) = sqrt(110*220))

The count is NOT a rung of the ladder {toll, tritone, upper}: it is the
step between them, and the mirror point that pairs the ends.

Left:  the square and its diagonal. side=count, diagonal=tritone,
       diagonal-side = toll, diagonal+side = upper.
Right: the three rungs on a line (step = count) and the mirror across the
       count.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

K = 12100.0
c = np.sqrt(K)          # 110 count
s2 = np.sqrt(2)
t = c / (1 + s2)        # 45.56 toll
T = c * s2              # 155.56 tritone
U = c * (1 + s2)        # 265.56 upper

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(13.5, 6.0), gridspec_kw={"width_ratios": [1, 1.25]},
)

INK = "#1a1a1a"
FAINT = "#888888"
ACC = "#b03a2e"   # toll / excess
BLU = "#2a5d8f"   # count
GRN = "#2f6b3a"   # tritone / diagonal

# ---------------------------------------------------------------------------
# left panel: the square and its diagonal
# ---------------------------------------------------------------------------
ax1.set_xlim(0, 300)
ax1.set_ylim(-40, 135)
ax1.set_aspect("equal")
ax1.axis("off")

sq = 110.0
ax1.add_patch(plt.Rectangle((20, 20), sq, sq, fill=False, ec=INK, lw=1.6))
ax1.plot([20, 20 + sq], [20, 20 + sq], color=GRN, lw=2.2)
# right-angle corner marks
ax1.plot([20, 20 + 15], [20, 20], color=INK, lw=1.0)
ax1.plot([20, 20], [20, 20 + 15], color=INK, lw=1.0)
ax1.plot([20 + 15, 20 + 15], [20, 20 + 15], color=INK, lw=1.0, ls=":")
ax1.plot([20, 20 + 15], [20 + 15, 20 + 15], color=INK, lw=1.0, ls=":")

ax1.text(20 + sq / 2, 11, "count 110", ha="center", va="center",
         color=BLU, fontsize=15, fontweight="bold")
ax1.text(13, 20 + sq / 2, "110", ha="right", va="center",
         color=BLU, fontsize=13)
ax1.text(20 + sq / 2 + 22, 20 + sq / 2 + 9, "tritone\n110\u221a2 = 155.6",
         ha="left", va="center", color=GRN, fontsize=13)

# the diagonal, straightened on the floor at y = -8
yl = -8
ax1.plot([20, 20 + T], [yl, yl], color=GRN, lw=5.0, solid_capstyle="butt")
ax1.plot([20, 20 + sq], [yl, yl], color=BLU, lw=2.4, solid_capstyle="butt")
ax1.plot([20 + sq, 20 + T], [yl, yl], color=ACC, lw=5.0,
         solid_capstyle="butt")
ax1.plot([20 + T, 20 + T + sq], [yl, yl], color=INK, lw=5.0,
         solid_capstyle="butt")

# row 1 labels: side, upper
ax1.text(20 + sq / 2, yl - 8, "side 110", ha="center", va="top",
         color=BLU, fontsize=12)
ax1.text(20 + T + sq / 2, yl - 8, "upper 265.6", ha="center", va="top",
         color=INK, fontsize=12)
# row 2 labels: diagonal, toll
ax1.text(20 + T / 2, yl - 21, "diagonal 155.6", ha="center", va="top",
         color=GRN, fontsize=12)
ax1.text(20 + (sq + T) / 2, yl - 21, "toll 45.6", ha="center", va="top",
         color=ACC, fontsize=12)

# toll arrow from the red segment up into the panel
ax1.annotate(
    "", xy=(20 + (sq + T) / 2, yl + 4), xytext=(20 + (sq + T) / 2 + 18, 46),
    arrowprops=dict(arrowstyle="-", color=ACC, lw=1.2, ls="--"),
)
ax1.text(20 + (sq + T) / 2 + 22, 48,
         "toll =\ndiagonal \u2212 side", ha="left", va="center",
         fontsize=11.5, color=ACC)

ax1.set_title("the count is the side; the tritone is the diagonal",
              fontsize=13.5, color=INK, pad=12)

# ---------------------------------------------------------------------------
# right panel: the ladder and the mirror
# ---------------------------------------------------------------------------
ax2.set_xlim(-25, 305)
ax2.set_ylim(-52, 78)
ax2.axis("off")

yline = 0.0
xs = [t, c, T, U]
labels = ["toll 45.6", "count 110", "tritone 155.6", "upper 265.6"]
cols = [ACC, BLU, GRN, INK]
markers = ["o", "s", "o", "o"]

ax2.plot([0, 285], [yline, yline], color=INK, lw=1.2)
for x, lab, col, mk in zip(xs, labels, cols, markers):
    ax2.plot([x, x], [yline - 5, yline + 5], color=col, lw=1.8)
    ax2.plot([x], [yline], marker=mk, ms=8, color=col, mec=col)
    ax2.text(x, yline - 11, lab, ha="center", va="top", color=col,
             fontsize=12, fontweight="bold")

# the ladder: rungs {toll, tritone, upper}, step = count  (two +110 arrows)
for x0 in (t, T):
    ax2.annotate(
        "", xy=(x0 + c - 6, yline + 7), xytext=(x0 + 6, yline + 7),
        arrowprops=dict(arrowstyle="->", color=BLU, lw=1.7),
    )
ax2.text((t + T) / 2, yline + 13, "+110", ha="center", va="bottom",
         color=BLU, fontsize=11)
ax2.text((T + U) / 2, yline + 13, "+110", ha="center", va="bottom",
         color=BLU, fontsize=11)

# the count is the step, not a rung: bracket the gap it lives in
ax2.plot([c, c], [yline - 7, yline + 7], color=BLU, lw=2.4)
ax2.text(c, yline - 33, "the count is the step,\nnot a rung",
         ha="center", va="top", color=BLU, fontsize=11)

# the mirror: toll * upper = count^2, across the count
ax2.annotate(
    "", xy=(U, yline + 40), xytext=(t, yline + 40),
    arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4,
                    connectionstyle="arc3,rad=0.30"),
)
ax2.plot([(t + U) / 2], [yline + 36], marker="o", ms=7, color=GRN)
ax2.text((t + U) / 2, yline + 51,
         "mirror: toll \u00d7 upper = 110\u00b2", ha="center", va="bottom",
         color=INK, fontsize=12.5)
ax2.text((t + U) / 2, yline + 22,
         "AM of the ends = the tritone; GM = the count",
         ha="center", va="center", color=GRN, fontsize=11)

ax2.set_title("one ladder, one mirror", fontsize=13.5, color=INK, pad=12)

fig.suptitle("the count as the unit of the fold's own diagonal",
             fontsize=14.5, color=INK, y=0.97)
fig.tight_layout(rect=[0, 0, 1, 0.93])
out = "assets/triangle-ladder-cover.png"
fig.savefig(out, dpi=170, facecolor="white")
print("wrote", out)
