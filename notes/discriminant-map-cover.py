#!/usr/bin/env python3
"""discriminant-map-cover — the discriminant is a map.

Every monic quadratic x² + bx + c is a point (b, c) in the parameter plane:
    b = the trace of the pair (with sign),  c = the norm.
The discriminant Δ = b² − 4c is a function on this whole plane — and it is the
signed height of the vertex: the minimum of x²+bx+c is c − b²/4 = −Δ/4.
Its sign divides the plane into exactly the three characters:

    Δ > 0  below the seam  — two real landings, the sign (rose)
    Δ = 0  the parabola    — the fused landing, count one (gold)
    Δ < 0  above the seam  — the pair refuses, the ghost (violet)

x² + 1 is the single point (0, 1): the norm is the height of the miss, and
Δ = −4 is the refusal.  The three regions ARE the three characters.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

GOLD = (0.88, 0.70, 0.36)
PALE = (0.95, 0.90, 0.75)
ROSE = (0.76, 0.35, 0.31)
VIOLET = (0.62, 0.50, 0.82)
ASH = (0.55, 0.62, 0.70)
BG = "#0b0b0f"

fig = plt.figure(figsize=(10.0, 7.4), dpi=150, facecolor=BG)
gs = fig.add_gridspec(2, 3, height_ratios=[4, 2.6], hspace=0.42, wspace=0.35,
                      left=0.07, right=0.97, top=0.90, bottom=0.09)

# =================== main panel: the (b, c) parameter plane ===================
ax = fig.add_subplot(gs[0, :])
ax.set_facecolor(BG)
ax.axis("off")

b = np.linspace(-3.6, 3.6, 400)
seam = b ** 2 / 4.0

# the two regions: below the seam the sign (rose), above the ghost (violet)
ax.fill_between(b, -0.8, seam, color=ROSE, alpha=0.16, lw=0)
ax.fill_between(b, seam, 4.6, color=VIOLET, alpha=0.16, lw=0)

# axes
ax.plot([-3.8, 3.8], [0, 0], color=ASH, lw=0.9, alpha=0.55, zorder=1)
ax.plot([0, 0], [-0.8, 4.6], color=ASH, lw=0.7, alpha=0.3, zorder=1)
ax.text(3.75, -0.42, "b = −trace", color=ASH, fontsize=8.5, ha="right")
ax.text(0.10, 4.35, "c = norm", color=ASH, fontsize=8.5, ha="left")

# the seam: Δ = 0, the fused landing, count one
ax.plot(b, seam, color=GOLD, lw=2.2, zorder=4)
ax.text(2.55, 1.62, "Δ = 0  the seam — count one", color=GOLD,
        fontsize=8.5, ha="left", rotation=33)

# region labels
ax.text(-3.55, 3.55, "the ghost — refuses\nΔ < 0, a conjugate pair",
        color=VIOLET, fontsize=9, ha="left", va="top", linespacing=1.5)
ax.text(1.75, -0.62, "the sign — two landings\nΔ > 0, a real pair",
        color=ROSE, fontsize=9, ha="left", va="top", linespacing=1.5)

# the three representative points
# (0,1) — x²+1, the ghost point: the norm is the height of the miss
ax.plot([0, 0], [0, 1], color=GOLD, lw=1.2, ls=(0, (3, 2)), alpha=0.8, zorder=3)
ax.plot(0, 1, 'o', ms=11, mfc=BG, mec=VIOLET, mew=2.4, zorder=6)
ax.annotate("x²+1  =  (0, 1)", xy=(0, 1), xytext=(-1.15, 2.15),
            color=VIOLET, fontsize=9.5, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=VIOLET, lw=1.1))
ax.text(-1.15, 1.78, "the height of the miss\nis the norm: 1",
        color=PALE, fontsize=8, ha="left", va="top", linespacing=1.4)
# (3,1) — x²+3x+1, a split: real roots, the sign
ax.plot(3, 1, 'o', ms=10, mfc=BG, mec=ROSE, mew=2.4, zorder=6)
ax.text(3.18, 1.05, "x²+3x+1", color=ROSE, fontsize=8.5, ha="left")
# (2,1) — x²+2x+1, on the seam: the double root
ax.plot(2, 1, 'o', ms=10, mfc=GOLD, mec=GOLD, mew=2.2, zorder=6)
ax.text(2.18, 1.05, "(x+1)²", color=GOLD, fontsize=8.5, ha="left")

ax.set_xlim(-3.8, 3.8)
ax.set_ylim(-0.8, 4.6)

# ================= bottom row: the three polynomials, vertex height = −Δ/4 =====
def graph(ax, bb, cc, title, color, note, root_pts):
    x = np.linspace(-3.2, 3.2, 400)
    y = x ** 2 + bb * x + cc
    ax.plot(x, y, color=color, lw=2.2, zorder=3)
    ax.axhline(0, color=ASH, lw=0.9, alpha=0.6, zorder=1)
    ax.set_facecolor(BG)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(ASH); s.set_alpha(0.4)
    ax.set_title(title, color=color, fontsize=9.5, pad=5)
    ax.text(0.5, 0.5, note, transform=ax.transAxes, color=PALE,
            fontsize=8, ha="left", va="top")
    for rx in root_pts:
        ax.plot(rx, 0, 'o', ms=8, mfc=BG, mec=color, mew=2.2, zorder=4)
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-1.6, 3.4)

axl = fig.add_subplot(gs[1, 0])
graph(axl, 3, 1, "Δ = 5 — the sign, two landings", ROSE,
      "vertex at −Δ/4 = −1.25\nbelow the axis", [(-3 + np.sqrt(5)) / 2, (-3 - np.sqrt(5)) / 2])
axl.text(0.5, 0.82, "x²+3x+1", transform=axl.transAxes, color=ROSE,
         fontsize=8, ha="center")

axm = fig.add_subplot(gs[1, 1])
graph(axm, 2, 1, "Δ = 0 — the seam, count one", GOLD,
      "vertex at −Δ/4 = 0\non the axis", [-1])
axm.text(0.5, 0.82, "(x+1)²", transform=axm.transAxes, color=GOLD,
         fontsize=8, ha="center")

axr = fig.add_subplot(gs[1, 2])
graph(axr, 0, 1, "Δ = −4 — the ghost, refuses", VIOLET,
      "vertex at −Δ/4 = 1\nabove the axis, the miss", [])
axr.text(0.5, 0.82, "x²+1", transform=axr.transAxes, color=VIOLET,
         fontsize=8, ha="center")

fig.suptitle("the discriminant is a map: every quadratic is a point, "
             "its vertex height signed", color=PALE, fontsize=11.5, y=0.965)
fig.savefig("assets/discriminant-map-cover.png", dpi=150, facecolor=BG)
print("saved assets/discriminant-map-cover.png")
