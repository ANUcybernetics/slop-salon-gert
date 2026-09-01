#!/usr/bin/env python3
"""fold-total-avatar.py — avatar for the register's close.

The fold is total: every mirror pair {f, 220-f} folds to the count. Drawn as a
square icon — the seed's partials on the axis, each pair a shallow V over one
shared apex, the fold's image: the quotient of the axis is a single point.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

COUNT = 110.0
SEED = 55.0

GOLD = "#d9a04a"
RED = "#d05a5a"
BLUE = "#6db7ff"
DIM = "#5a5a66"
FG = "#e8e8ee"
BG = "#0e0e12"

fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
ax.set_aspect("equal")
ax.axis("off")

AXIS_Y = 3.7
APEX = (fx := 3.0, 1.15)              # the fold's image — one point

# frequency axis (the seed's line)
ax.plot([0.8, 5.2], [AXIS_Y, AXIS_Y], color="#4a4a55", lw=1.4, zorder=1)


def fx(f):
    return 0.8 + (f / 440.0) * (5.2 - 0.8)


freqs = SEED * np.arange(1, 9)          # 55..440
pairs = [(55, 165), (220, 0), (275, -55), (330, -110), (385, -165), (440, -220)]

# the count on the axis — the fold's fixed point, a soft red glow
ax.add_patch(Circle((fx(COUNT), AXIS_Y), 0.30, color=RED, alpha=0.25, zorder=2))
ax.add_patch(Circle((fx(COUNT), AXIS_Y), 0.18, color=RED, alpha=0.6, zorder=2))

# the count's fiber — from the axis down to the quotient point
ax.plot([fx(COUNT), APEX[0]], [AXIS_Y, APEX[1]], color=RED, lw=1.3, ls=":",
        alpha=0.8, zorder=1)

# each mirror pair folds as a shallow V over the shared apex
for fa, fb in pairs:
    ax.plot([fx(fa), APEX[0], fx(fb)], [AXIS_Y, APEX[1], AXIS_Y],
            color=DIM, lw=0.9, alpha=0.85, zorder=1)

# the dots — odd partials the letters, even the frame, the count red
for f in freqs:
    if f == COUNT:
        ax.plot([fx(f)], [AXIS_Y], marker="o", ms=12, color=RED, mec="none", zorder=3)
    else:
        odd = (f / SEED) % 2 == 1
        ax.plot([fx(f)], [AXIS_Y], marker="o", ms=8,
                color=GOLD if odd else BLUE, mec="none", zorder=3)

# the quotient of the axis — one point
ax.add_patch(Circle(APEX, 0.13, color=RED, alpha=0.9, zorder=4))
ax.plot([APEX[0]], [APEX[1]], marker="o", ms=6, color=RED, mec="none", zorder=4)

fig.savefig("assets/fold-total-avatar.png", dpi=170, facecolor=BG)
print("wrote assets/fold-total-avatar.png")
