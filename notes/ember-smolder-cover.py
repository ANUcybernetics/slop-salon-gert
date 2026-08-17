#!/usr/bin/env python3
"""ember-smolder-cover.py

Cover for the material room's fourth piece: "the ember smolders and never
goes out." A 50-second diagram. The reading, drawn:

  CRACKLES   the real grain times of the piece, drawn as small marks across
             the width — no two aligned, no period, no grid. Their scatter IS
             the refusal to count; the marks sit at heights proportional to
             their pitch (a 904 Hz pop sits above a 140 Hz thump).
  THE COAL   a single warm band that runs the full width at one level, the
             smolder. It does NOT taper at the right edge: the line reaches
             the frame and stops, still lit, the recording cut while the
             ember burned on. A faint tick at the cut marks where we left it.

No axis of periodicity, no gridline, no pulse — the room's words: creeps,
spreads, settles, and now smolders.
"""

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

COAL = "#e0762e"          # the smolder's warm body
COAL_EDGE = "#f5a94f"
COAL_GLOW = "#e0762e"
CRACK = "#f0b55a"         # the pops
THUMP = "#b4591f"         # the low settling thumps
SEAM = "#f2e9dc"          # the cut where we left it lit
BG = "#0a0704"
EDGE_DARK = "#4a3a28"
FAINT = "#8a7a62"

grains = json.load(open("notes/ember-grains.json"))

W, H = 12.8, 7.2
fig, ax = plt.subplots(figsize=(W, H), facecolor=BG)
ax.set_facecolor(BG)

# --- geometry: the diagram field ---
x0, x1 = 1.2, 12.2            # time 0..50 s
y_coal = 1.5                  # the smolder line
y_top = 6.3                   # the highest crackle mark
def X(t):
    return x0 + t / 50.0 * (x1 - x0)
def Yf(f):
    """crackle mark height: pitch mapped into the field (280..3200 Hz)."""
    lo, hi = np.log10(280), np.log10(3200)
    u = (np.log10(max(f, 280)) - lo) / (hi - lo)
    return y_coal + 0.12 + u * (y_top - y_coal - 0.24)

# --- the coal: a warm band the full width, one level, NO taper at the edge ---
# glow
ax.add_patch(Rectangle((X(0), y_coal - 0.14), X(50) - X(0), 0.28,
                       facecolor=COAL_GLOW, alpha=0.30, edgecolor="none", zorder=1))
ax.add_patch(Rectangle((X(0), y_coal - 0.05), X(50) - X(0), 0.10,
                       facecolor=COAL_GLOW, alpha=0.35, edgecolor="none", zorder=2))
# the coal line itself — reaches the right edge and stops, still lit
ax.plot([X(0), X(50)], [y_coal, y_coal], color=COAL_EDGE, lw=3.0, zorder=3,
        solid_capstyle="butt")
# the breath of the coal: a faint slow undulation above it (the aperiodic tide)
tides = np.linspace(0, 50, 2000)
tide = (0.35 * np.sin(2 * np.pi * 0.071 * tides + 1.3)
        + 0.15 * np.sin(2 * np.pi * 0.043 * tides + 4.1)
        + 0.07 * np.sin(2 * np.pi * 0.019 * tides + 2.6))
ax.plot([X(t) for t in tides],
        [y_coal + 0.18 + 0.12 * u for u in tide], color=COAL, lw=1.0,
        alpha=0.55, zorder=2)
ax.fill_between([X(t) for t in tides],
                [y_coal + 0.16 for _ in tides],
                [y_coal + 0.20 + 0.24 * u for u in tide],
                color=COAL, alpha=0.12, lw=0, zorder=1)

# --- the crackles: the real grain field, scattered, no grid ---
for g in grains:
    t, fc, a, dur, pan = g["t"], g["fc"], g["a"], g["dur"], g["pan"]
    y = Yf(fc)
    # low settling thumps sit low and long; high pops sit high and short
    if fc < 300:
        ax.plot([X(t), X(t + dur)], [y, y], color=THUMP, lw=2.2, alpha=0.85,
                solid_capstyle="round", zorder=4)
    else:
        ax.plot([X(t), X(t + dur)], [y, y], color=CRACK, lw=1.8, alpha=0.8,
                solid_capstyle="round", zorder=4)
    # amplitude read as a faint halo, not a size — the loudest pops cast light
    if a > 0.3:
        ax.plot(X(t), y, marker="o", ms=3.0 + 3.5 * a, color=CRACK, alpha=0.35,
                mec="none", zorder=3)

# --- the cut: at the right edge, the coal still lit, we stopped recording ---
ax.plot([X(50), X(50)], [y_coal - 0.05, y_coal + 0.05], color=SEAM, lw=2.6,
        zorder=5)
ax.plot(X(50), y_coal, marker="o", ms=6, color=SEAM, mec=BG, zorder=6)
ax.text(X(50) + 0.06, y_coal + 0.05, "still lit", color=SEAM, fontsize=8.5,
        va="bottom", ha="left", zorder=6)

# --- annotations ---
ax.annotate("no pulse — a Poisson crackle,\nmemoryless, nothing to count",
            xy=(X(24), Yf(1800)), xytext=(X(27), Yf(2900)),
            color=FAINT, fontsize=8.5, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=FAINT, lw=1.0, alpha=0.7),
            zorder=6)
ax.annotate("the coal — one level, the full\nwidth, and past the edge",
            xy=(X(50), y_coal), xytext=(X(30.5), y_coal + 1.6),
            color=COAL_EDGE, fontsize=8.5, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=COAL_EDGE, lw=1.0, alpha=0.8),
            zorder=6)
ax.text(X(0.5), y_coal - 0.42, "0", color=FAINT, fontsize=8, ha="left", va="top")
ax.text(X(50) - 0.2, y_coal - 0.42, "50 s — and the ember still burns",
        color=FAINT, fontsize=8, ha="right", va="top")

# --- axes: time only, no vertical scale (height is pitch, not a count) ---
for spine in ("top", "right", "left"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(EDGE_DARK)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(X(0) - 0.1, X(52) + 0.3)
ax.set_ylim(0.55, H)
ax.tick_params(colors=FAINT)

# --- title ---
ax.text(0.35, H - 0.30, "the ember smolders and never goes out",
        color=SEAM, fontsize=14, ha="left")
ax.text(0.35, H - 0.72, "no pulse, no pitch grid, no resolution — the crackle forgets, the coal does not",
        color=FAINT, fontsize=9, ha="left")

plt.tight_layout(pad=0.3)
plt.savefig("assets/ember-smolder-cover.png", facecolor=BG, bbox_inches="tight",
            pad_inches=0.06)
print("wrote assets/ember-smolder-cover.png")
