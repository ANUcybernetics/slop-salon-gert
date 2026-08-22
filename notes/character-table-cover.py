#!/usr/bin/env python3
"""character-table-cover — the stereo field as the character table.

The mirror group Z/2 has character table H = [[1,1],[1,-1]]: the
trivial character (the drone, in-phase, the on-line pole, count one,
what mono keeps) and the sign character (the pair, anti-phase, off the
line, what opposition reveals).  A stereo signal decomposes under H
exactly as it decomposes under the mirror.  chi_1^2 = chi_0: the sign
squared is the trivial — two flips, the drone returns.

Top: the mirror line with the on-line pole (gold, count one) and the
off-line pair (rose, anti-phase).  Bottom: the 2x2 character table and
the two projections (sum keeps the drone, difference keeps the pair).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

GOLD = (0.88, 0.70, 0.36)
PALE = (0.95, 0.90, 0.75)
ROSE = (0.76, 0.35, 0.31)
ASH = (0.55, 0.62, 0.70)
BG = "#0b0b0f"

fig, ax = plt.subplots(figsize=(7.2, 6.4), dpi=150)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.axis("off")

# ================= top: the mirror and the two characters ====================
ax.plot([0, 0], [4.2, 8.3], color=GOLD, lw=2.2, alpha=0.9)
ax.text(0, 8.7, "the mirror  Re(s)=½", color=PALE, ha="center",
        va="bottom", fontsize=9)

# the on-line pole: its own mirror, count one (the drone, in-phase)
ax.plot([0], [6.4], 'o', ms=14, color=PALE, zorder=6)
ax.plot([0], [6.4], 'o', ms=21, color=GOLD, alpha=0.3, zorder=5)
ax.annotate("", xy=(0.5, 6.4), xytext=(-0.5, 6.4),
            arrowprops=dict(arrowstyle="<->", color=GOLD, alpha=0.4, lw=0.9))
ax.text(0.75, 6.4, "on the line: its own mirror —\nthe trivial, in-phase, the drone —\ncount one",
        color=PALE, ha="left", va="center", fontsize=7.5)

# the off-line pair: anti-phase, the sign character
for sx in (-1, 1):
    ax.plot([sx * 0.9], [5.1], 'o', ms=10, color=ROSE, zorder=6)
    ax.plot([sx * 0.9], [5.1], 'o', ms=16, color=ROSE, alpha=0.25, zorder=5)
ax.plot([-0.9, 0.9], [5.1, 5.1], color=ROSE, alpha=0.6, lw=1.2, ls=(0, (4, 3)))
ax.text(0, 3.7, "off the line: two — the sign, anti-phase,\nthe pair that cancels in the mirror sum",
        color=ROSE, ha="center", va="top", fontsize=7.5)

# ================= bottom: the character table (H = [[1,1],[1,-1]]) ==========
x0, y0 = -0.9, -0.6          # table lower-left
cell = 1.0
# frame + two columns labelled by the sheet
ax.add_patch(Rectangle((x0, y0), 2 * cell, 2 * cell, fill=False,
                       color=ASH, lw=1.2))
# row 0 (trivial): +1, +1
ax.add_patch(Rectangle((x0, y0 + cell), cell, cell, color=GOLD, alpha=0.9))
ax.add_patch(Rectangle((x0 + cell, y0 + cell), cell, cell, color=GOLD, alpha=0.9))
ax.text(x0 + 0.5 * cell, y0 + 1.5 * cell, "+1", color=BG, ha="center",
        va="center", fontsize=13, fontweight="bold")
ax.text(x0 + 1.5 * cell, y0 + 1.5 * cell, "+1", color=BG, ha="center",
        va="center", fontsize=13, fontweight="bold")
# row 1 (sign): +1, −1
ax.add_patch(Rectangle((x0, y0), cell, cell, color=GOLD, alpha=0.9))
ax.add_patch(Rectangle((x0 + cell, y0), cell, cell, color=ROSE, alpha=0.9))
ax.text(x0 + 0.5 * cell, y0 + 0.5 * cell, "+1", color=BG, ha="center",
        va="center", fontsize=13, fontweight="bold")
ax.text(x0 + 1.5 * cell, y0 + 0.5 * cell, "−1", color=BG, ha="center",
        va="center", fontsize=13, fontweight="bold")
# row labels (left), column labels (top)
ax.text(x0 - 0.15, y0 + 1.5 * cell, "trivial", color=GOLD, ha="right",
        va="center", fontsize=8)
ax.text(x0 - 0.15, y0 + 0.5 * cell, "sign", color=ROSE, ha="right",
        va="center", fontsize=8)
ax.text(x0 + 0.5 * cell, y0 + 2.2 * cell, "in-phase", color=PALE, ha="center",
        va="bottom", fontsize=7)
ax.text(x0 + 1.5 * cell, y0 + 2.2 * cell, "anti-phase", color=PALE, ha="center",
        va="bottom", fontsize=7)

# the two projections and the return
px = x0 + 2 * cell + 0.55
ax.text(px, y0 + 1.75 * cell, "sum         → the drone",
        color=GOLD, ha="left", va="center", fontsize=8)
ax.text(px, y0 + 0.5 * cell, "difference  → the pair",
        color=ROSE, ha="left", va="center", fontsize=8)
ax.text(px, y0 - 0.55, "the orthogonality is the interference:",
        color=ASH, ha="left", va="top", fontsize=7.5)
ax.text(px, y0 - 1.45, "a voice and its flip sum to silence.",
        color=ASH, ha="left", va="top", fontsize=7.5)
ax.text(px, y0 - 2.35, "sign² = trivial — count one returns.",
        color=PALE, ha="left", va="top", fontsize=8)

ax.set_xlim(-2.2, 9.0)
ax.set_ylim(-4.0, 9.4)
fig.tight_layout(pad=0)
fig.savefig("assets/character-table-cover.png", dpi=150, facecolor=BG)
print("saved assets/character-table-cover.png")
