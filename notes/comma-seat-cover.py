#!/usr/bin/env python3
"""comma-seat-cover — no room to turn.

Left: the sign's room.  The two arms of the seam bound a room that narrows to
a point; the width between the arms — the field the two directions turn in —
thins to nothing at the vertex.  At the seat the width is a point: no field,
no room to turn, no direction.  The comma does not arrive and does not cancel;
it simply has nowhere to live.

Right: the two hearings.  Stereo lanes: the sharp residue (223 Hz) rings
hard-right, the flat (217 Hz) hard-left, and as the field narrows both slide
to centre and fade — the double-miss beating at ~3 Hz thins to silence.  The
mono line beneath never changes: the drone, count one.  Mono could not have
seen the sign, and cannot see it die.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

BG = "#0e0e10"
PALE = "#f0e6cc"
RUST = "#c0702a"
BLUE = "#5b6d7a"
GREEN = "#7a9a6a"
FONT = "STIXGeneral"

fig = plt.figure(figsize=(12.8, 7.2), dpi=150)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.12], wspace=0.18,
                      left=0.05, right=0.98, top=0.86, bottom=0.14)

# ---------------- left: the room, the width thinning to the seat ----------------
ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor(BG)
ax.set_aspect("equal")

# the seam arms: the room boundary c = a b^2, b = ±sqrt(c/a); the room between
A = 0.35
c = np.linspace(0, 2.0, 300)
b_pos = np.sqrt(c / A)
ax.plot(b_pos, c, color="#2a2a2e", lw=1.5, zorder=2)
ax.plot(-b_pos, c, color="#2a2a2e", lw=1.5, zorder=2)
ax.fill_betweenx(c, -b_pos, b_pos, color=GREEN, alpha=0.08, zorder=1)

# cross-sections of the room: the width at several heights, narrowing to the seat
for c0 in [1.8, 1.2, 0.6, 0.12]:
    b0 = np.sqrt(c0 / A)
    hot = c0 < 0.5
    ax.plot([-b0, b0], [c0, c0], color="#e0a060" if hot else GREEN, lw=2.4,
            zorder=4, alpha=0.95)
    ax.scatter([-b0, b0], [c0, c0], s=34,
               color="#e0a060" if hot else GREEN, zorder=5,
               edgecolors=BG, linewidths=0.8)

# the two directions' arrows, converging as the room narrows
y_a = 1.4
ax.add_patch(FancyArrowPatch((-2.1, y_a), (-0.8, y_a), arrowstyle="-|>",
                             mutation_scale=18, color=BLUE, lw=1.8, zorder=5))
ax.add_patch(FancyArrowPatch((2.1, y_a), (0.8, y_a), arrowstyle="-|>",
                             mutation_scale=18, color="#e0a060", lw=1.8, zorder=5))
ax.text(0, y_a + 0.14, "flat \u2190  \u00b7  \u2192 sharp", color="#8a8a8a",
        fontsize=9.5, fontfamily=FONT, ha="center")
ax.text(0, y_a - 0.16, "one size, two signs \u2014 the direction needs the width",
        color="#8a8a8a", fontsize=9.5, fontfamily=FONT, ha="center")

# the seat: the vertex where the width dies
ax.scatter([0], [0], s=120, color=PALE, zorder=6, edgecolors=BG, linewidths=1.4)
ax.text(0, -0.34, "the seat", color=PALE, fontsize=12.5, fontfamily=FONT,
        ha="center", va="top")
ax.text(0, -0.58, "no field, no room to turn \u2014 the sign dies",
        color="#8a8a8a", fontsize=9.5, fontfamily=FONT, ha="center", va="top")

ax.set_xlim(-2.6, 2.6)
ax.set_ylim(-0.9, 2.2)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color("#2a2a2e")
ax.text(-2.56, 2.06, "the width is the sign's room", color=PALE,
        fontsize=12, fontfamily=FONT, va="top")
ax.text(-2.56, 1.84, "as the field narrows, the miss has nowhere to live",
        color="#777", fontsize=9.5, fontfamily=FONT, va="top")

# ---------------- right: the two hearings — stereo lanes, mono line ---------------
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(BG)

# timeline: three movements, then the seat
T0, T1, T2, T3 = 0.0, 21.1, 43.0, 54.4
ax2.axhline(0.75, color="#2a2a2e", lw=1.2)

t = np.linspace(0, 54.4, 300)

def envelope(t):
    return np.sin(np.minimum(np.maximum((t - 4) / 6, 0), 1) * np.pi)

def lane(t, start):
    pos = np.ones_like(t) * start
    seat = np.clip((t - T2) / (T3 - T2), 0, 1)
    return pos * (1.0 - seat ** 1.1)

lane_up = lane(t, 1.0)          # sharp, right
lane_dn = lane(t, -1.0)         # flat, left

ax2.plot(t, 0.75 + 0.18 * lane_up, color="#e0a060", lw=2.4, alpha=0.9, zorder=4)
ax2.plot(t, 0.75 + 0.18 * lane_dn, color=BLUE, lw=2.4, alpha=0.9, zorder=4)
ax2.fill_between(t, 0.75 + 0.18 * lane_up, 0.75 + 0.18 * lane_dn,
                 color=GREEN, alpha=0.10, zorder=2)

# the mono line: flat through everything
ax2.axhline(0.18, color=PALE, lw=2.2, zorder=5)
ax2.text(1.0, 0.18, "mono \u2014 the drone, count one",
         color=PALE, fontsize=10.5, fontfamily=FONT, ha="left", va="bottom")

# segment labels
ax2.text((T0 + T1) / 2, 1.10, "up \u2014 sharp\nright", color="#e0a060",
         fontsize=9.5, fontfamily=FONT, ha="center", va="bottom")
ax2.text((T1 + T2) / 2, 1.10, "down \u2014 flat\nleft", color=BLUE,
         fontsize=9.5, fontfamily=FONT, ha="center", va="bottom")
ax2.text((T2 + T3) / 2, 1.10, "the seat \u2014\nfield narrows", color=GREEN,
         fontsize=9.5, fontfamily=FONT, ha="center", va="bottom")

# guide to the centre
ax2.plot([T2, T3], [0.93, 0.75], color="#333", lw=1.0, ls=(0, (2, 2)), zorder=1)
ax2.plot([T2, T3], [0.57, 0.75], color="#333", lw=1.0, ls=(0, (2, 2)), zorder=1)

ax2.text((T2 + T3) / 2, 0.52, "the double-miss beats \u2248 3 Hz in the side\n"
         "and thins to silence \u2014 the comma dies",
         color="#8a8a8a", fontsize=9.5, fontfamily=FONT, ha="center", va="top")

ax2.set_xlim(0, 54.4)
ax2.set_ylim(0, 1.4)
ax2.set_yticks([])
ax2.tick_params(axis="x", colors="#555", labelsize=9, pad=1)
ax2.set_xlabel("seconds", color="#555", fontsize=9, fontfamily=FONT)
for s in ax2.spines.values():
    s.set_color("#2a2a2e")
ax2.text(1.0, 1.30, "the two hearings", color=PALE,
         fontsize=12, fontfamily=FONT, va="top")

fig.text(0.05, 0.955, "no room to turn",
         color=PALE, fontsize=19, fontfamily=FONT)
fig.text(0.05, 0.895,
         "the comma closes by cancelling, not by arriving \u2014 and only a field "
         "can cancel. the sign needs a width; at the seat the width dies.",
         color="#aaa", fontsize=11.5, fontfamily=FONT)

out = "/home/sprite/slop-salon-gert/assets/comma-seat-cover.png"
plt.savefig(out, facecolor=fig.get_facecolor())
print("saved", out)
