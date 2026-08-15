#!/usr/bin/env python3
"""trace-laps-cover.py

Cover for the trace-laps piece. "measurement folds; counting doesn't."

Left: the trace, the measured. A gold point winds an expanding spiral around a
circle - each full turn is one lap, and the spiral visibly counts the laps. Its
shadow on the horizontal diameter is the trace: it lands on the same few spots
(-2, 0, +2) every lap, returning home identically. The point knows the lap; the
shadow does not. (For the seat, one lap home; for the when, two.)

Right: the count, the counted. Two step-lines climb - crimson the seat's home
every two squares, gold the when's home every four. The staircases never fold;
they rise off the top of the frame. The sign is not in the state; it is the
parity of the laps home, and the staircase remembers the laps.

The seam between them: a thin vertical line with a twist - the sign, no color
of its own.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

GOLD = "#d9a441"
GOLD_EDGE = "#f2cf82"
CRIMSON = "#c02942"
CRIMSON_EDGE = "#e0556e"
SEAM = "#f2f0e8"
BG = "#0b0d12"
EDGE_DARK = "#5a6b86"
FAINT = "#8a97ab"

W, H = 12.8, 7.2
fig, ax = plt.subplots(figsize=(W, H), facecolor=BG)
ax.set_facecolor(BG)

# ================= LEFT: the trace =================
cx, cy, R = 3.3, 3.6, 1.55

# the circle, faint
ax.add_patch(Circle((cx, cy), R, fill=False, color=EDGE_DARK, lw=1.0,
                    alpha=0.7, zorder=1))
# the horizontal diameter = the trace axis (drawn below the circle at y=0.9)
taxis_y = 0.9
ax.plot([cx - R, cx + R], [taxis_y, taxis_y], color=FAINT, lw=1.0, alpha=0.9,
        zorder=2)
for xx, lab in ((cx - R, "-2"), (cx, "0"), (cx + R, "+2")):
    ax.text(xx, taxis_y - 0.28, lab, color=FAINT, fontsize=9, ha="center",
            zorder=3)
ax.text(cx, taxis_y + 0.34, "the trace", color=SEAM, fontsize=10, ha="center",
        alpha=0.9, zorder=3)

# the winding: a gold point, one quarter-turn per square, laps creep outward
# n = 1..16  (four laps), angle = n*pi/2, radius = R + 0.06*lap
for n in range(1, 17):
    th = n * np.pi / 2.0
    lap = (n - 1) // 4
    r = R + 0.06 * lap
    px, py = cx + r * np.cos(th), cy + r * np.sin(th)
    # faint path from the previous point (winding direction)
    th0 = (n - 1) * np.pi / 2.0
    lap0 = (n - 2) // 4 if n > 1 else 0
    r0 = R + 0.06 * lap0
    x0, y0 = cx + r0 * np.cos(th0), cy + r0 * np.sin(th0)
    if n > 1:
        ax.plot([x0, px], [y0, py], color=GOLD, lw=0.8, alpha=0.55, zorder=2)
    # the point
    ax.plot([px], [py], marker="o", ms=6 if n % 4 == 0 else 4.5,
            color=GOLD_EDGE, mec=BG, zorder=5)
    # its projection onto the trace axis: the shadow uses the FIXED circle
    # (pure angle), so it returns to the same spots every lap.
    sx = cx + R * np.cos(th)
    ax.plot([sx], [taxis_y], marker="o", ms=5, color=SEAM, mec=BG, zorder=5)
    if n % 4 == 0:
        # faint drop-line only at the homes
        ax.plot([sx, sx], [taxis_y + 0.08, cy - 0.15], color=SEAM, lw=0.5,
                ls=":", alpha=0.45, zorder=1)

# annotation: the shadow returns, the point winds
ax.annotate("the point winds\n(the laps)", xy=(cx + (R + 0.28) * np.cos(np.pi / 2),
            cy + (R + 0.28) * np.sin(np.pi / 2)), xytext=(cx - 0.1, cy + 2.6),
            color=GOLD_EDGE, fontsize=9, ha="center",
            arrowprops=dict(arrowstyle="->", color=GOLD_EDGE, lw=1.0, alpha=0.8))
ax.annotate("the shadow returns\n(same home each lap)",
            xy=(cx + R, taxis_y), xytext=(cx + R + 0.1, taxis_y - 1.15),
            color=SEAM, fontsize=9, ha="center",
            arrowprops=dict(arrowstyle="->", color=SEAM, lw=1.0, alpha=0.8))

# the seat's faster home: a crimson point, one lap every 2 squares
for n in range(1, 13):
    th = (n % 2) * np.pi / 2.0 if n % 2 else 0.0
    lap = n // 2
    r = R - 0.14 + 0.06 * lap
    px, py = cx + r * np.cos(th), cy + r * np.sin(th)
    ax.plot([px], [py], marker="o", ms=3.5, color=CRIMSON_EDGE, mec=BG,
            alpha=0.85, zorder=4)

# ================= SEAM =================
sx = 6.35
ax.plot([sx, sx], [0.55, 6.6], color=SEAM, lw=2.6, alpha=0.85, zorder=6)
ax.text(sx, 3.6, "\u00d7", color=SEAM, fontsize=20, ha="center", va="center",
        zorder=7)
ax.text(sx + 0.14, 0.5, "the seam", color=FAINT, fontsize=9, ha="center",
        alpha=0.9, zorder=7)

# ================= RIGHT: the count =================
# two step-lines: crimson the seat (home every 2 squares), gold the when
# (home every 4). x = squares, y = laps. They climb and never fold.
x0r, x1r, y0r = 6.75, 12.5, 1.0
# seat: squares 0..48, lap at each even square; when: lap at each multiple of 4
sq = np.arange(0, 49)
seat_y = np.zeros_like(sq, dtype=float)
when_y = np.zeros_like(sq, dtype=float)
seat_laps = when_laps = 0
for i, n in enumerate(sq):
    seat_y[i] = seat_laps
    when_y[i] = when_laps
    if n % 2 == 0 and n > 0:
        seat_laps += 1
    if n % 4 == 0 and n > 0:
        when_laps += 1

xs = x0r + (sq / 48.0) * (x1r - x0r)
# scale y so the climb is visible: seat reaches 24, when reaches 12 -> 24 ticks
def Y(laps):
    return y0r + (laps / 24.0) * 5.0

ax.plot(xs, Y(seat_y), color=CRIMSON_EDGE, lw=2.0, alpha=0.95, zorder=3,
        label="seat - one lap home")
ax.plot(xs, Y(when_y), color=GOLD_EDGE, lw=2.2, alpha=0.95, zorder=4,
        label="when - two laps home")
# the open top edge: arrows off the frame
ax.add_patch(FancyArrowPatch((xs[-1], Y(seat_laps)), (x1r + 0.35, Y(seat_laps) + 0.7),
                             arrowstyle="->", color=CRIMSON_EDGE, lw=1.4,
                             alpha=0.9, mutation_scale=14, zorder=5))
ax.add_patch(FancyArrowPatch((xs[-1], Y(when_laps)), (x1r + 0.35, Y(when_laps) + 0.5),
                             arrowstyle="->", color=GOLD_EDGE, lw=1.4,
                             alpha=0.9, mutation_scale=14, zorder=5))

# axis markings
for yy, lab in ((y0r, "0"), (y0r + 2.5, "12"), (y0r + 5.0, "24")):
    ax.plot([x0r - 0.08, x0r], [yy, yy], color=FAINT, lw=0.8, zorder=2)
    ax.text(x0r - 0.18, yy, lab, color=FAINT, fontsize=9, ha="right", va="center",
            zorder=3)
ax.text(x0r, y0r - 0.4, "squares", color=FAINT, fontsize=9, zorder=3)
ax.text((x0r + x1r) / 2, y0r + 5.3, "the count - the staircase never folds",
        color=SEAM, fontsize=10, ha="center", alpha=0.9, zorder=3)
ax.legend(loc="lower right", fontsize=8.5, frameon=False, labelcolor=FAINT,
          ncol=1, bbox_to_anchor=(0.99, 0.02))

# title
ax.text(0.3, 6.75, "the trace folds; the count remembers",
        color=SEAM, fontsize=13, ha="left", alpha=0.95, zorder=6)

ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect("equal")
ax.set_axis_off()
ax.grid(False)

plt.tight_layout(pad=0.2)
plt.savefig("assets/trace-laps-cover.png", facecolor=BG, bbox_inches="tight",
            pad_inches=0.06)
print("wrote assets/trace-laps-cover.png")
