#!/usr/bin/env python3
"""second-ear cover: the same walk, folded and lifted.

TOP — folded (the quotient): the landings sit on one line, the count — seven
ticks, no direction, no size. the dimension thrown away.

BOTTOM — lifted (the second ear): the same landings split into over/under
pairs between the two sheets, each pair's height = the miss's size (log
scale), the ring on the sheet of its direction. the miss shrinks ~1/N; the
last a hair — 0.076¢ — refusing to fuse.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# the records: (step, signed error in cents)
FIFTHS = [
    (2, +203.910),
    (5, -90.225),
    (12, +23.460),
    (41, -19.845),
    (53, +3.615),
    (306, -1.770),
    (665, +0.076),
]

BG = "#0d0d12"
FG = "#e8e2d4"
DIM = "#6b6b78"
SHEET = "#3a3a46"
GOLD = "#d8b36a"
COPPER = "#c97e5a"
CYAN = "#7fc4b8"

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 5.2), dpi=150)
for ax in (ax1, ax2):
    ax.set_facecolor(BG)
    ax.set_ylim(-1.6, 1.6)
    ax.set_xlim(-0.6, 7.6)
    ax.axis("off")

fig.patch.set_facecolor(BG)

# ---------- TOP: the fold ----------
x = np.arange(len(FIFTHS))

# the base — the seat, the count lives here
ax1.plot([-0.4, 7.4], [0, 0], color=SHEET, lw=2.0, zorder=1)
ax1.text(-0.55, 0, "", transform=ax1.transData)

# the landings: pure ticks on the line, no size, no direction
for i, (k, e) in enumerate(FIFTHS):
    ax1.plot([i, i], [-0.42, 0.42], color=GOLD, lw=2.2, zorder=3)
    ax1.plot(i, 0, marker="o", ms=5.5, mfc=GOLD, mec="none", zorder=4)

# the drone — a faint band under everything
ax1.axhspan(-1.25, -0.95, color=SHEET, alpha=0.5, zorder=0)
ax1.plot([-0.4, 7.4], [-1.1, -1.1], color=DIM, lw=1.0, ls=":", zorder=1)
ax1.text(7.4, -1.1, " the drone", color=DIM, fontsize=8, va="center",
         ha="right", family="monospace")

ax1.text(0, 1.45, "folded — the count. one, one, one.", color=FG, fontsize=11,
         ha="left", family="serif", style="italic")
ax1.text(7.4, 1.45, "the dimension thrown away", color=DIM, fontsize=8,
         ha="right", family="monospace")

# ---------- BOTTOM: the lift ----------
# two sheets: over (top) and under (bottom); the ring's ear
ax2.plot([-0.4, 7.4], [1.0, 1.0], color=SHEET, lw=1.4, zorder=1)
ax2.plot([-0.4, 7.4], [-1.0, -1.0], color=SHEET, lw=1.4, zorder=1)
ax2.text(7.4, 1.0, " over — left", color=CYAN, fontsize=8, va="center",
         ha="right", family="monospace")
ax2.text(7.4, -1.0, "under — right", color=COPPER, fontsize=8, va="center",
         ha="right", family="monospace")

# the same landings as over/under pairs, height = log of the miss's size
# ring frequency sits at ±delta/2 around the seat; draw the pair as a segment
for i, (k, e) in enumerate(FIFTHS):
    d = abs(e)
    # log height between the sheets, clamped; tiny misses are a hair
    h = 0.02 + 0.62 * np.clip(np.log10(d / 0.001) / 5.0, 0, 1)
    over = e > 0
    # the pair: ring on the direction's sheet, twin anti-phase on the other
    yring = 1.0 * h if over else -1.0 * h
    ytwin = -yring
    col = GOLD if over else GOLD
    ax2.plot([i, i], [ytwin, yring], color=COPPER if not over else CYAN,
             lw=2.0, alpha=0.9, zorder=2)
    # the ring: a filled dot on its sheet; the twin: a hollow dot
    ax2.plot(i, yring, marker="o", ms=6.0, mfc=COPPER if not over else CYAN,
             mec="none", zorder=4)
    ax2.plot(i, ytwin, marker="o", ms=5.0, mfc="none", mec=GOLD, lw=1.0,
             zorder=3)

# the hair: 665, 0.076¢ — a near-fused pair, refusing
i = len(FIFTHS) - 1
ax2.annotate("0.076¢ — a hair from fusing, refuses",
             xy=(i, 0.0), xytext=(i + 0.55, -0.35),
             color=DIM, fontsize=8, family="monospace",
             arrowprops=dict(arrowstyle="-", color=DIM, lw=0.8))

# the drone, still holding
ax2.axhspan(-1.25, -1.45, color=SHEET, alpha=0.5, zorder=0)
ax2.plot([-0.4, 7.4], [-1.35, -1.35], color=DIM, lw=1.0, ls=":", zorder=1)
ax2.text(7.4, -1.35, " the drone", color=DIM, fontsize=8, va="center",
         ha="right", family="monospace")

ax2.text(0, 1.45, "lifted — the where. the miss sized, ears flip.", color=FG,
         fontsize=11, ha="left", family="serif", style="italic")

fig.tight_layout(h_pad=0.8)
fig.savefig("assets/second-ear-cover.png", facecolor=BG, bbox_inches="tight")
print("wrote assets/second-ear-cover.png")
