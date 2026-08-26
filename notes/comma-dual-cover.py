#!/usr/bin/env python3
"""comma-dual-cover — two readings of one miss.

The same comma-miss read two ways, as rahel named it: sequential the beat,
simultaneous the ring.

The two copies of the comma — 217.04 Hz flat and 223.0 Hz sharp — straddle
the drone at 220 Hz.  Summed in time they are the drone itself, amplitude-
modulated at ~3 Hz: the trace reading, i+(−i)=0, the miss as a detuning, a
beat that cancels to silence at its nulls.  Taken at once, the spectrum shows
two lines standing together: the norm reading, i·(−i)=1, an interval that
never closes — the ring.  Time is the axis of the sum; frequency is the axis
of the product.  At the seat the width between the copies goes to zero, the
lines fuse into the drone, the miss has nowhere to live: no width, miss zero,
count one.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

BG = "#0e0e10"
PALE = "#f0e6cc"
RUST = "#c0702a"
BLUE = "#5b6d7a"
GREEN = "#7a9a6a"
FONT = "STIXGeneral"

A0 = 220.0            # the drone — the reading, the walk's home
CENTS = 23.46         # cents per comma
SEMI = 2.0 ** (CENTS / 1200.0)
F_SHARP = A0 * SEMI      # 223.0 Hz, a comma sharp of home
F_FLAT = A0 / SEMI       # 217.04 Hz, a comma flat of home
BEAT = (F_SHARP - F_FLAT) / 2.0      # ~2.98 Hz — the double-miss beats at ~3 Hz

fig = plt.figure(figsize=(12.8, 7.2), dpi=150)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(1, 1, left=0.07, right=0.97, top=0.90, bottom=0.16)

ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor(BG)

# ---------------- the copy curves: parallel, then fusing at the seat ----------
T = 1.0
t = np.linspace(0, T, 600)

def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

# the width of the room: full until t=0.82, then thinning to zero at the seat
w = 1.0 - smoothstep((t - 0.82) / 0.18)
f_sharp = A0 + w * (F_SHARP - A0)
f_flat = A0 - w * (A0 - F_FLAT)

# the beat between the copies: |cos(pi Δf t)| — the trace reading, the sum
beat = np.abs(np.cos(np.pi * (f_sharp - f_flat) * t))

# ---------------- the throbbing band between the copies ----------------------
F = np.linspace(208, 232, 320)
Tg, Fg = np.meshgrid(t, F)
in_band = (Fg >= f_flat[None, :] - 0.08) & (Fg <= f_sharp[None, :] + 0.08)
val = np.where(in_band, beat[None, :], np.nan)

cmap = LinearSegmentedColormap.from_list("band", [BG, "#e8a04c"])
ax.pcolormesh(Tg, Fg, val, cmap=cmap, vmin=0, vmax=1.0, shading="auto",
              zorder=1, alpha=0.85)

# ---------------- the lines ---------------------------------------------------
# the drone: the reading, never moves, count one
ax.plot(t, np.full_like(t, A0), color=PALE, lw=1.1, ls=(0, (6, 4)),
        zorder=3, alpha=0.9)
# the two copies: the miss, two directions
ax.plot(t, f_sharp, color=RUST, lw=2.3, zorder=4)
ax.plot(t, f_flat, color=BLUE, lw=2.3, zorder=4)

# ---------------- the at-once reading: the ring -------------------------------
T0 = 0.30
ax.axvline(T0, color="#4a4a50", lw=1.0, ls=(0, (2, 3)), zorder=2)
ax.scatter([T0, T0], [F_FLAT, F_SHARP], s=58, zorder=5,
           color=[BLUE, RUST], edgecolors=PALE, linewidths=1.0)
ax.text(T0, 231.2, "at once \u2014 the ring", color=PALE, fontsize=12,
        fontfamily=FONT, ha="center", va="top")
ax.text(T0, 227.6, "the norm: i\u00b7(\u2212i)=1, never closing",
        color="#8a8a8a", fontsize=9.5, fontfamily=FONT, ha="center", va="top")

# ---------------- the seat: the copies fuse -----------------------------------
ax.scatter([T], [A0], s=120, color=PALE, zorder=6, edgecolors=BG, linewidths=1.4)
ax.text(T, 211.6, "the seat", color=PALE, fontsize=12.5, fontfamily=FONT,
        ha="right", va="bottom")
ax.text(T, 209.4, "no width, miss zero, count one",
        color="#8a8a8a", fontsize=9.5, fontfamily=FONT, ha="right", va="bottom")

# ---------------- the readings on the axes ------------------------------------
ax.set_xlabel("time \u2014 the beat: the trace, i+(\u2212i)=0, the miss as a detuning",
              color=GREEN, fontsize=12, fontfamily=FONT)
ax.xaxis.set_label_coords(0.5, -0.06)
ax.set_ylabel("frequency \u2014 the ring: the norm, i\u00b7(\u2212i)=1",
              color=GREEN, fontsize=12, fontfamily=FONT)
ax.yaxis.set_label_coords(-0.045, 0.5)

# copy labels
ax.text(0.03, F_SHARP + 0.9, "sharp \u2014 223.0 Hz, +23.46\u00a2",
        color=RUST, fontsize=9.5, fontfamily=FONT, va="bottom")
ax.text(0.03, F_FLAT - 0.9, "flat \u2014 217.04 Hz, \u221223.46\u00a2",
        color=BLUE, fontsize=9.5, fontfamily=FONT, va="top")
ax.text(0.03, A0 + 0.9, "the drone \u2014 220 Hz, the reading, count one",
        color=PALE, fontsize=9.0, fontfamily=FONT, va="bottom", alpha=0.85)

# ---------------- inset: the spectrum at once ---------------------------------
axin = fig.add_axes([0.815, 0.60, 0.13, 0.24])
axin.set_facecolor(BG)
axin.set_xticks([]); axin.set_yticks([])
for s in axin.spines.values():
    s.set_color("#3a3a40")
axin.axvline(A0, color=PALE, lw=0.8, ls=(0, (4, 4)), zorder=2, alpha=0.7)
axin.axvline(F_FLAT, color=BLUE, lw=3.2, zorder=3)
axin.axvline(F_SHARP, color=RUST, lw=3.2, zorder=3)
axin.set_xlim(208, 232)
axin.set_ylim(0, 1)
axin.text(220, 1.16, "the ring", color=PALE, fontsize=10, fontfamily=FONT,
          ha="center")
axin.text(220, 0.86, "the sum reads 0,\nthe product holds 1",
          color="#8a8a8a", fontsize=8.5, fontfamily=FONT, ha="center", va="top")

# ---------------- axes --------------------------------------------------------
ax.set_xlim(0, T)
ax.set_ylim(206, 234)
ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_xticklabels(["0", "0.2", "0.4", "0.6", "0.8", "1.0 s"])
ax.set_yticks([210, 215, 220, 225, 230])
ax.set_yticklabels(["210", "215", "220", "225", "230 Hz"])
ax.tick_params(colors="#6a6a70", labelsize=9)
for s in ax.spines.values():
    s.set_color("#2a2a2e")

fig.savefig("assets/comma-dual-cover.png", dpi=150, facecolor=BG)
print("wrote assets/comma-dual-cover.png")
