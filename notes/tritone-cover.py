#!/usr/bin/env python3
"""tritone — the ladder is a fan of right triangles, one isosceles rung.

Each rung n is a right triangle sharing the count leg (110, struck, mono):
legs 55n and 110, hypotenuse 55√(n²+4) — never struck. At n=2 the gap equals
the count (110=110), the isosceles rung, the tritone: hypotenuse 110√2,
off-grid tone, on-grid interval. The toll it pays to the count is
110(√2−1) = 110/σ₂ ≈ 45.6 Hz — the amount the landing sits off the grid.

Figure for the ladder register, 2026-09-01.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Polygon

BG = "#0d0e13"
FG = "#e8e2d0"
DIM = "#4a5166"
GOLD = "#e3b64d"
ROSE = "#cf6a5a"
BLUE = "#9bb3c9"
GRID = "#262b3a"

COUNT = 110.0
NS = [1, 2, 3, 4, 5]

fig, ax = plt.subplots(figsize=(12.6, 7.4), dpi=150)
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)

# ---------------------------------------------------------------- triangles
# all rungs share the count leg (0,0)-(110,0); the gap leg is vertical at x=110.
# draw n=1..5 faint; highlight n=2.
for n in NS:
    v = np.array([[0, 0], [COUNT, 0], [COUNT, 55.0 * n]])
    hi = (n == 2)
    col = GOLD if hi else DIM
    lw = 2.6 if hi else 1.0
    # the gap leg (vertical)
    ax.plot([COUNT, COUNT], [0, 55.0 * n], color=col, lw=lw, alpha=0.9 if hi else 0.55,
            zorder=3 if hi else 2)
    # the hypotenuse (0,0) -> (COUNT, 55n)
    ax.plot([0, COUNT], [0, 55.0 * n], color=col, lw=lw, ls="-" if hi else "--",
            alpha=0.95 if hi else 0.5, zorder=3 if hi else 2)
    if hi:
        ax.fill([0, COUNT, COUNT], [0, 0, 55.0 * n], color=GOLD, alpha=0.08, zorder=1)
    else:
        ax.fill([0, COUNT, COUNT], [0, 0, 55.0 * n], color=DIM, alpha=0.035, zorder=1)
    # n label at the top of each gap leg
    ax.text(COUNT + 7, 55.0 * n + 6, f"n={n}", color=col, fontsize=11 if hi else 9,
            ha="left", va="center", alpha=0.95 if hi else 0.6, zorder=4)

# the count leg — the struck side, mono
ax.plot([0, COUNT], [0, 0], color=GOLD, lw=3.6, solid_capstyle="round", zorder=4)
ax.text(COUNT / 2, -14, "the count — 110 Hz, struck, mono", color=GOLD, fontsize=12,
        ha="center", va="top")

# right-angle marker at (110,0)
ax.plot([COUNT - 16, COUNT], [COUNT - 16, COUNT - 16], color=FG, lw=1.2, zorder=5)
ax.plot([COUNT, COUNT], [COUNT - 16, COUNT], color=FG, lw=1.2, zorder=5)

# the n=2 isosceles annotations
ax.annotate("the gap — 110, never struck\n(equals the count: 110=110)",
            xy=(COUNT, 55.0 * 2), xytext=(COUNT + 60, 150),
            color=ROSE, fontsize=11,
            arrowprops=dict(arrowstyle="-|>", color=ROSE, lw=1.3), zorder=5)
ax.annotate("the tritone — 110√2 ≈ 155.6,\nthe never's one landing",
            xy=(COUNT, 55.0 * 2), xytext=(-4, 210),
            color=BLUE, fontsize=11, ha="left",
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.3), zorder=5)

# ---------------------------------------------------------------- the toll
# arc of radius 110√2 through the n=2 hypotenuse end (110,110), cutting the
# x-axis at 155.6 — the excess over the count leg is the toll 45.6.
HYP = COUNT * np.sqrt(2)
arc = Arc((0, 0), 2 * HYP, 2 * HYP, angle=0, theta1=0,
          theta2=45.0, color=ROSE, lw=1.4, ls=":", zorder=2)
ax.add_patch(arc)
# the toll segment on the x-axis: 110 -> 155.6
ax.annotate("", xy=(HYP, 0), xytext=(COUNT, 0),
            arrowprops=dict(arrowstyle="<->", color=ROSE, lw=1.4, ls="-"))
ax.text((COUNT + HYP) / 2, -26, "the toll — 110(√2−1) = 110/σ₂ ≈ 45.6 Hz",
        color=ROSE, fontsize=11.5, ha="center", va="top")
ax.text(HYP, -8, "155.6", color=ROSE, fontsize=10, ha="center", va="top")
ax.text(COUNT, -8, "110", color=GOLD, fontsize=10, ha="center", va="top")

# the n=0 fusion — the drone, where the triangle degenerates (hyp = count)
ring = Circle((COUNT, 0), 4.0, fill=False, ec=FG, lw=1.4, zorder=6)
ax.add_patch(ring)
ax.text(COUNT + 8, -40, "n=0 fuses — the drone, the seam", color=FG, fontsize=9.5,
        ha="left", va="top", alpha=0.85)

# ---------------------------------------------------------------- frame
ax.set_xlim(-18, 320)
ax.set_ylim(-52, 300)
ax.set_xticks([])
ax.set_yticks([])
for s in ("bottom",):
    ax.spines[s].set_position(("data", -38))
ax.text(0, 296, "the ladder is a fan of right triangles — one isosceles rung",
        color=FG, fontsize=16, ha="left")
ax.text(0, 284, "each shares the count leg; at n=2 the gap equals the count, "
                "and the tritone's toll is silver",
        color=DIM, fontsize=10.5, ha="left")

fig.tight_layout()
fig.savefig("assets/tritone-cover.png", facecolor=BG, bbox_inches="tight")
print("wrote assets/tritone-cover.png")
