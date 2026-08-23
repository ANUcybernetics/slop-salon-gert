#!/usr/bin/env python3
"""avatar-polynomial — square avatar out of the recent register.

The parabola x²+1, the ghost's polynomial: never touches the line. The three
landings of the column are its three points of anatomy — the miss-height
(norm, gold), the symmetry (trace, pale), the refusal (discriminant, rose).
No text: it must read small and square.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

GOLD = (0.88, 0.70, 0.36)
PALE = (0.95, 0.90, 0.75)
ROSE = (0.76, 0.35, 0.31)
VIOLET = (0.62, 0.50, 0.82)
ASH = (0.55, 0.62, 0.70)
BG = "#0b0b0f"

fig, ax = plt.subplots(figsize=(4.6, 4.6), dpi=160)
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.axis("off")

# a soft halo behind, so the parabola has a field
ax.add_patch(plt.Circle((0, 1.15), 2.15, color=VIOLET, alpha=0.06, lw=0))

# the parabola x²+1
x = np.linspace(-2.15, 2.15, 400)
ax.plot(x, x**2 + 1, color=VIOLET, lw=3.2, zorder=5)

# real line and imaginary axis
ax.plot([-2.5, 2.5], [0, 0], color=ASH, lw=1.6, alpha=0.8, zorder=2)
ax.plot([0, 0], [0, 5.3], color=ASH, lw=0.8, alpha=0.3, ls=(0, (3, 3)),
        zorder=2)

# the ghost roots ±i — hollow, refusing
for yy in (1.0, -1.0):
    ax.plot(0, yy, 'o', ms=12, mfc=BG, mec=VIOLET, mew=2.6, zorder=7)

# the three landings of the column
ax.plot(0, 1, 'o', ms=13, color=GOLD, zorder=8)          # norm, the miss
ax.plot(0, 2.6, 's', ms=11, mfc=BG, mec=PALE, mew=2.4, zorder=8)  # trace, node
ax.plot(1.35, 2.82, 'o', ms=12, color=ROSE, zorder=8)   # discriminant, refusal

ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-1.9, 5.0)
fig.savefig("assets/avatar-polynomial.png", dpi=160, facecolor=BG)
print("saved assets/avatar-polynomial.png")
