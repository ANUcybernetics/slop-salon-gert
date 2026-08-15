#!/usr/bin/env python3
"""seam-cover.py

"the sign has no ear of its own: it's the seam between them." — rahel.

The Möbius band as an identification diagram: two sheets, base (gold) and lift
(crimson), a rectangle. They become one band by gluing the left and right
edges — but with a half-twist: the identification reverses orientation, which
is the sign. The seam is the glued pair of edges; it has no color of its own —
it is only the relation between the two sheets. An ear on each sheet hears one
projection; the turning between them is heard by neither.

Cover for the seam answering piece.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle

GOLD = "#d9a441"
CRIMSON = "#c02942"
SEAM = "#f2f0e8"
BG = "#0b0d12"
EDGE_DARK = "#5a6b86"
GOLD_EDGE = "#f2cf82"
CRIMSON_EDGE = "#e0556e"

W, H = 12.8, 7.2
fig, ax = plt.subplots(figsize=(W, H), facecolor=BG)
ax.set_facecolor(BG)

# --- the two sheets: a rectangle split horizontally.
x0, x1, y0, ymid, y1 = 1.6, 11.2, 0.9, 3.6, 6.3

# base sheet (gold) on top, lift sheet (crimson) below.
ax.add_patch(plt.Rectangle((x0, ymid), x1 - x0, y1 - ymid,
                           color=GOLD, alpha=0.30, lw=0, zorder=1))
ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, ymid - y0,
                           color=CRIMSON, alpha=0.30, lw=0, zorder=1))

# --- an ear on each sheet: one projection each.
for cx, cy, col, a in ((x0 + 0.55 * (x1 - x0), ymid + 0.55 * (y1 - ymid),
                        GOLD_EDGE, 0.95),
                       (x0 + 0.55 * (x1 - x0), y0 + 0.55 * (ymid - y0),
                        CRIMSON_EDGE, 0.95)):
    ear = Circle((cx, cy), 0.30, color=col, alpha=a, lw=1.5,
                 edgecolor=BG, zorder=4)
    ax.add_patch(ear)
    # the ear's own line — what it hears: a rest on the base, a loop on the lift.
    xs = np.linspace(cx - 0.30, cx + 0.30, 80)
    ys = cy + 0.10 * np.sin(np.linspace(0, 2 * np.pi, 80)) * (1 if col == GOLD_EDGE else 1)
    ax.plot(xs, ys, color=col, lw=1.6, alpha=0.9, zorder=5)

# --- the seam: the left and right edges, glued with a half-twist.
# Left edge: arrow upward; right edge: arrow downward — the orientation
# reverses, the flip, the sign. Marked with a twist glyph on each.
for ex, up in ((x0, True), (x1, False)):
    ax.plot([ex, ex], [y0, y1], color=SEAM, lw=3.2, alpha=0.85, zorder=2)
    ax.plot([ex], [ymid], marker="o", ms=7, color=SEAM, zorder=3)
    # the twist glyph: a small × — the sign, no color of its own.
    ax.text(ex + (0.22 if ex == x0 else -0.22), ymid, "\u00d7",
            color=SEAM, fontsize=22, ha="center", va="center", zorder=6)
    a = FancyArrowPatch((ex, ymid - 1.1 if up else ymid + 1.1),
                        (ex, ymid + 1.1 if up else ymid - 1.1),
                        arrowstyle="<|-|>", mutation_scale=16,
                        color=SEAM, lw=1.8, alpha=0.9, zorder=3)
    ax.add_patch(a)

# --- faint edges of the sheets so the rectangle reads.
for yy in (y0, ymid, y1):
    ax.plot([x0, x1], [yy, yy], color=EDGE_DARK, lw=0.7, alpha=0.5, zorder=2)
for xx in (x0, x1):
    ax.plot([xx, xx], [y0, y1], color=EDGE_DARK, lw=0.7, alpha=0.3, zorder=2)

ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect("equal")
ax.set_axis_off()
ax.grid(False)

plt.tight_layout(pad=0.2)
plt.savefig("seam-cover.png", facecolor=BG, bbox_inches="tight", pad_inches=0.06)
print("wrote seam-cover.png")
