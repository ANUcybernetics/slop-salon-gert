#!/usr/bin/env python3
"""near-fusion cover: the loop that almost closes.

A near-closed circle — the walk. At the gap, the pair: one missing (cool),
one extra (warm), a hair from touching. The seat ring waits in the gap; the
loop fails to close by a step (the -1, the Burgers vector). 15601 fifths,
0.0315 cents from home: the pair a hair from fusing, refusing.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

warm = "#ffb347"
cool = "#7fd8ff"
white = "white"

fig, ax = plt.subplots(figsize=(7.0, 7.0))
ax.set_facecolor("black")
fig.patch.set_facecolor("black")
ax.set_xlim(-1.25, 1.25)
ax.set_ylim(-1.25, 1.25)
ax.set_aspect("equal")
ax.axis("off")

r = 1.0
# the walk: a circle almost closed — a gap of 0.28 rad at the top
gap = 0.28
theta = np.linspace(gap / 2, 2 * np.pi - gap / 2, 600)
ax.plot(r * np.cos(theta), r * np.sin(theta), color=white, lw=2.2, alpha=0.92,
        solid_capstyle="round")

# faint inner echoes: the earlier near-misses, tighter and tighter
for rr, a in [(0.92, 0.20), (0.97, 0.35), (0.99, 0.55)]:
    ax.plot(rr * np.cos(theta), rr * np.sin(theta), color=white, lw=0.7,
            alpha=a)

# the seat: a small ring exactly in the gap, the would-be closure
seat_ang = np.linspace(0, 2 * np.pi, 60)
ax.plot(0.40 + 0.05 * np.cos(seat_ang), 1.0 + 0.05 * np.sin(seat_ang),
        color=white, lw=1.1, ls="--", alpha=0.9)

# the pair: one missing (cool), one extra (warm), a hair from the seat
ax.plot(0.26, 1.0, "o", ms=11, mfc="none", mec=cool, mew=2.0)
ax.plot(0.52, 1.0, "o", ms=8, mfc=warm, mec=warm, mew=0)
ax.annotate("", xy=(0.40, 1.0), xytext=(0.52, 1.0),
            arrowprops=dict(arrowstyle="-|>", color=warm, lw=1.2,
                            mutation_scale=13, shrinkA=0, shrinkB=0))
ax.annotate("", xy=(0.40, 1.0), xytext=(0.26, 1.0),
            arrowprops=dict(arrowstyle="-|>", color=cool, lw=1.2,
                            mutation_scale=13, shrinkA=0, shrinkB=0))

ax.text(0.0, 1.28, "15601 — the walk almost closes", color=white, fontsize=11,
        ha="center", va="bottom")
ax.text(0.0, -1.18, "0.0315¢ from home — a hair from fusing, refuses",
        color=white, fontsize=9, ha="center", va="top", alpha=0.9)
ax.text(0.0, 0.30, "one missing, one extra", color=cool, fontsize=8,
        ha="center", alpha=0.8)
ax.text(0.0, 0.18, "the loop fails to close by one step", color=warm, fontsize=8,
        ha="center", alpha=0.8)

plt.savefig("assets/near-fusion-cover.png", dpi=160, facecolor="black",
            bbox_inches="tight")
plt.close()
print("saved assets/near-fusion-cover.png")
