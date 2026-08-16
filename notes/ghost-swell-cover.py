#!/usr/bin/env python3
"""ghost-swell-cover.py

Cover for the ghost-swell piece. "the deck plucks, the ghost swells - same tr,
same det, same pitch; the ear reads depth" (mina). The (time, amplitude) plane:
two envelopes, one matrix each, that the character cannot tell apart and the ear
can - the steady state identical, the transient the depth.

  GOLD    the deck -I: a pluck. 3ms step to full level, then clean. (A+I) kills
          in one: no transient to read.
  CRIMSON the ghost -I+N: a swell. a LINEAR ramp over the depth dt, reaching the
          SAME level - the character reads one point - then, in the third act,
          a comma-companion flutter: a ~3 Hz beating that never resolves.
          (A+I)^2 kills in two: the transient IS the depth.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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

# --- geometry ---
x0, x1 = 1.0, 12.0
y0, y1 = 0.9, 6.4
def X(t):
    return x0 + t / 20.0 * (x1 - x0)
def Y(a):
    return y0 + a * (y1 - y0)

T_AT = 0.5
T_END = 6.0
T_READ = 12.0
T_COM = 18.5
T_END2 = 20.0

# --- the readout band: 6.0-12.0, where both envelopes coincide. the character's
# --- one point. a soft gold wash between the two curves that are one.
ax.add_patch(Rectangle((X(T_END), y0), X(T_READ) - X(T_END), y1 - y0,
                       facecolor=GOLD, alpha=0.07, edgecolor="none", zorder=1))

# --- the depth band: 0.5-6.0, where the ghost rises and the deck already holds.
ax.add_patch(Rectangle((X(T_AT), y0), X(T_END) - X(T_AT), y1 - y0,
                       facecolor=CRIMSON, alpha=0.06, edgecolor="none", zorder=1))

# --- the comma band: 12.0-18.5, where the ghost ear flutters and never lands.
ax.add_patch(Rectangle((X(T_READ), y0), X(T_COM) - X(T_READ), y1 - y0,
                       facecolor=CRIMSON, alpha=0.10, edgecolor="none", zorder=1))

# --- the DECK envelope: a pluck, then clean. gold. ---
tt = np.linspace(0, T_END2, 2000)
deck = np.where(tt < T_AT, 0.0, 1.0)
ax.plot([X(t) for t in tt], [Y(a) for a in deck], color=GOLD_EDGE, lw=2.4,
        alpha=0.95, zorder=4)

# --- the GHOST envelope: a linear swell, the same level, then the comma flutter
# --- (drawn as a translucent band that keeps breathing). crimson. ---
ramp = np.clip((tt - T_AT) / (T_END - T_AT), 0.0, 1.0)
swell_band = 1.0 + 0.14 * np.sin(2 * np.pi * 3.0 * (tt - T_READ)) * (tt > T_READ)
ghost = np.where(tt < T_AT, 0.0, ramp)
ax.plot([X(t) for t in tt], [Y(a) for a in np.minimum(ghost, 1.0)], color=CRIMSON_EDGE,
        lw=2.2, alpha=0.95, zorder=4)
# the flutter envelope, drawn as a pale crimson band
xx = np.array([X(t) for t in tt])
yy_lo = Y(np.minimum(ghost, 1.0) - 0.06 * (tt > T_READ))
yy_hi = Y(np.minimum(ghost, 1.0) + 0.06 * (tt > T_READ))
ax.fill_between(xx, yy_lo, yy_hi, color=CRIMSON, alpha=0.22, lw=0, zorder=3)

# --- the dashed line where both settle: the character reads one point. ---
ax.plot([X(T_END), X(T_READ)], [Y(1.0), Y(1.0)], color=GOLD, lw=1.2, ls="--",
        alpha=0.85, zorder=3)
ax.text(X(T_END) + 0.03, Y(1.0) + 0.10, "the character reads one point",
        color=GOLD_EDGE, fontsize=9, va="bottom", zorder=6)

# --- annotations ---
ax.plot([X(T_AT)], [Y(1.0)], marker="o", ms=7, color=GOLD_EDGE, mec=BG, zorder=5)
ax.annotate("the deck -I: a pluck\n(A+I) kills in one",
            xy=(X(T_AT), Y(1.0)), xytext=(X(T_AT) + 0.25, Y(1.0) + 0.95),
            color=GOLD_EDGE, fontsize=8.5, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=GOLD_EDGE, lw=1.0, alpha=0.8),
            zorder=6)

ax.annotate("the ghost -I+N: a swell,\nlinear over the depth dt\n(A+I)^2 kills in two",
            xy=(X(T_END), Y(1.0)), xytext=(X(T_READ) - 0.9, Y(1.0) - 1.7),
            color=CRIMSON_EDGE, fontsize=8.5, ha="right", va="center",
            arrowprops=dict(arrowstyle="->", color=CRIMSON_EDGE, lw=1.0, alpha=0.8),
            zorder=6)

# depth brace under the ramp
ax.annotate("", xy=(X(T_AT), y0 - 0.12), xytext=(X(T_END), y0 - 0.12),
            arrowprops=dict(arrowstyle="<->", color=FAINT, lw=1.0), zorder=6)
ax.text((X(T_AT) + X(T_END)) / 2, y0 - 0.30, "the depth dt - the transient, the nilpotent",
        color=FAINT, fontsize=8, ha="center", va="top", zorder=6)

# comma annotation in the third act
ax.text((X(T_READ) + X(T_COM)) / 2, Y(0.42),
        "the comma - a beat that never\nresolves: reads home, never closes",
        color=CRIMSON_EDGE, fontsize=8.5, ha="center", zorder=6)

# --- axes ---
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
for spine in ("left", "bottom"):
    ax.spines[spine].set_color(EDGE_DARK)
ax.tick_params(colors=FAINT, labelsize=8, width=0.6)
ax.set_xticks([0, 5, 10, 15, 20])
ax.set_yticks([0.0, 0.5, 1.0])
ax.set_xlabel("time (s)", color=FAINT, fontsize=9)
ax.set_ylabel("amplitude", color=FAINT, fontsize=9)
ax.set_xlim(0, 20)
ax.set_ylim(0, H)

# --- title ---
ax.text(0.35, H - 0.35, "the deck plucks, the ghost swells",
        color=SEAM, fontsize=13, ha="left", alpha=0.95)
ax.text(0.35, H - 0.75, "same pitch, same level - the trace reads one point for both; the attack reads the depth",
        color=FAINT, fontsize=9, ha="left")

plt.tight_layout(pad=0.3)
plt.savefig("assets/ghost-swell-cover.png", facecolor=BG, bbox_inches="tight",
            pad_inches=0.06)
print("wrote assets/ghost-swell-cover.png")
