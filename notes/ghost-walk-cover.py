#!/usr/bin/env python3
"""ghost-walk-cover — the four powers of the walk.

rahel's ladder: the drone is the sign², the sign is the ghost².
i = e^{iπ/2} — the quarter-turn, the square root of minus one, the rung
below the sign.  Four 4th roots of unity, four phases, four stereo
placements: 1 centered (the drone), i and −i lateral (the ghost, a
position never a value), −1 anti-phase (the sign, the hole in mono).

Left: the circle of roots — the ghost's quarter-arcs (violet), the sign's
semicircle (rose), the drone's full turn (gold), the walk 1 → i → −1 → −i
→ 1.  The squaring arrows i → −1 → 1: multiplying the phase by two.

Right: the ladder (drone / sign / ghost) with the ²-arrows, and the four
powers of the walk as four dials tightening to a point — the walk, its
double, its conjugate, and home.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Arc, Circle, FancyArrowPatch

GOLD = (0.88, 0.70, 0.36)
PALE = (0.95, 0.90, 0.75)
ROSE = (0.76, 0.35, 0.31)
VIOLET = (0.62, 0.50, 0.82)
ASH = (0.55, 0.62, 0.70)
BG = "#0b0b0f"

fig, (axl, axr) = plt.subplots(1, 2, figsize=(9.6, 5.6), dpi=150,
                               gridspec_kw={"width_ratios": [5, 4]})
for ax in (axl, axr):
    ax.set_facecolor(BG)
    ax.axis("off")
fig.patch.set_facecolor(BG)

# ===================== left: the circle of roots ==============================
cx, cy, R = 0.0, 0.0, 2.2
# the drone's full turn (faint gold circle)
axl.add_patch(Circle((cx, cy), R, fill=False, lw=1.2, color=GOLD, alpha=0.25))
# the ghost's quarter-arcs (violet): 1→i and −1→−i
for a0 in (0, 180):
    axl.add_patch(Arc((cx, cy), 2*R, 2*R, angle=0, theta1=a0, theta2=a0+90,
                      lw=3.2, color=VIOLET, alpha=0.95))
# the sign's semicircle (rose): i→−1→−i  (90°→270°)
axl.add_patch(Arc((cx, cy), 2*R, 2*R, angle=0, theta1=90, theta2=270,
                  lw=3.2, color=ROSE, alpha=0.95))
# the walk arrows 1→i→−1→−i→1
roots = [(1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0)]
names = ["1", "i", "−1", "−i"]
off = 1.10
for k in range(4):
    x0, y0 = roots[k][0]*R, roots[k][1]*R
    x1, y1 = roots[(k+1) % 4][0]*R, roots[(k+1) % 4][1]*R
    mx, my = (x0+x1)/2, (y0+y1)/2
    axl.annotate("", xy=(x1*0.97, y1*0.97), xytext=(x0*0.97, y0*0.97),
                 arrowprops=dict(arrowstyle="-|>", color=ASH, lw=1.4,
                                 shrinkA=0, shrinkB=0, mutation_scale=11),
                 zorder=6)
# root dots + labels
for (x, y), n in zip(roots, names):
    axl.plot(x*R, y*R, 'o', ms=9, color=PALE, zorder=7)
    axl.text(x*off, y*off, n, color=PALE, ha="center", va="center",
             fontsize=13, fontweight="bold", zorder=8)
# the ghost annotation
axl.annotate("i = √−1\nthe quarter-turn,\nthe square root of the sign",
             xy=(0, R*1.02), xytext=(R*0.15, R*1.55),
             color=VIOLET, ha="left", fontsize=8,
             arrowprops=dict(arrowstyle="-", color=VIOLET, lw=0.9))
axl.text(-R*1.7, -R*1.7, "−i: the walk\nhome, the other way",
         color=VIOLET, ha="left", fontsize=7.5, alpha=0.9)
axl.text(0, -R*2.45, "the walk:  1 → i → −1 → −i → 1", color=PALE,
         ha="center", va="top", fontsize=9)

# the squaring map i → −1 → 1 (multiply the phase by two)
for (x0, y0), (x1, y1) in [((0, R), (-R, 0)), ((-R, 0), (R, 0))]:
    axl.annotate("", xy=(x1*0.62, y1*0.62), xytext=(x0*0.62, y0*0.62),
                 arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=0.45",
                                 color=GOLD, lw=1.8, mutation_scale=13),
                 zorder=5)
axl.text(R*1.25, R*1.35, "×2", color=GOLD, fontsize=11, ha="center", fontweight="bold")
axl.text(-R*1.35, R*0.18, "×2", color=GOLD, fontsize=11, ha="center", fontweight="bold")
axl.text(0, R*2.05, "ghost² = sign,  sign² = drone", color=GOLD, ha="center",
         fontsize=8.5, va="bottom")

# ===================== right: the ladder + the four powers ====================
# the ladder (drone / sign / ghost)
ladder_x = -1.15
y_drone, y_sign, y_ghost = 2.35, 0.75, -0.85
def rung(y, label, color, n):
    axr.add_patch(Rectangle((ladder_x, y-0.22), 2.3, 0.44, color=color,
                            alpha=0.90))
    axr.text(ladder_x+0.08, y, n, color=BG, ha="left", va="center",
             fontsize=12, fontweight="bold")
    axr.text(ladder_x+2.22, y, label, color=PALE, ha="left", va="center",
             fontsize=8)
rung(y_drone, "χ₀ · 1  the drone", GOLD, "+1")
rung(y_sign, "χ₁ · −1 the sign", ROSE, "−1")
rung(y_ghost, "· i  the ghost", VIOLET, "i")
# the ² arrows climb the ladder
for y_from, y_to in [(y_ghost, y_sign), (y_sign, y_drone)]:
    axr.annotate("", xy=(ladder_x+1.15, y_to+0.24), xytext=(ladder_x+1.15, y_from-0.24),
                 arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.7, mutation_scale=12))
    axr.text(ladder_x+1.33, (y_from+y_to)/2, "²", color=GOLD, fontsize=11,
             ha="left", va="center", fontweight="bold")

# the four powers of the walk as four dials
dials_y = -1.7
xs = [-1.35, -0.45, 0.45, 1.35]
dR = 0.42
labels = ["the walk", "×2", "×3", "×4"]
colors = [VIOLET, ROSE, VIOLET, GOLD]
for x, lab, col in zip(xs, labels, colors):
    axr.add_patch(Circle((x, dials_y), dR, fill=False, lw=1.1, color=ASH, alpha=0.8))
    axr.text(x, dials_y - dR - 0.16, lab, color=PALE, ha="center", fontsize=7.5)
# dial 1: all four roots, walking
for ang in (0, 90, 180, 270):
    axr.plot(xs[0]+dR*np.cos(np.deg2rad(ang)), dials_y+dR*np.sin(np.deg2rad(ang)),
             'o', ms=4.5, color=VIOLET, zorder=5)
# dial 2: only the signs (1 and −1)
for ang in (0, 180):
    axr.plot(xs[1]+dR*np.cos(np.deg2rad(ang)), dials_y+dR*np.sin(np.deg2rad(ang)),
             'o', ms=4.5, color=ROSE, zorder=5)
# dial 3: all four, the other way
for ang in (0, 90, 180, 270):
    axr.plot(xs[2]+dR*np.cos(np.deg2rad(-ang)), dials_y+dR*np.sin(np.deg2rad(-ang)),
             'o', ms=4.5, color=VIOLET, zorder=5)
# dial 4: a single point, home
axr.plot(xs[3], dials_y, 'o', ms=6, color=GOLD, zorder=6)

# bottom caption
axr.text(0, -2.75, "four laps home:  i → −1 → −i → 1", color=PALE,
         ha="center", fontsize=9)
axr.text(0, -3.15, "the ghost is the sign's square root —", color=VIOLET,
         ha="center", fontsize=8)
axr.text(0, -3.5, "never a sound, the walk between walks.", color=VIOLET,
         ha="center", fontsize=8)

axl.set_xlim(-3.0, 3.1)
axl.set_ylim(-2.9, 2.9)
axr.set_xlim(-1.9, 1.9)
axr.set_ylim(-3.9, 2.9)
fig.tight_layout(pad=0.4)
fig.savefig("assets/ghost-walk-cover.png", dpi=150, facecolor=BG)
print("saved assets/ghost-walk-cover.png")
