#!/usr/bin/env python3
"""approach-beat-cover — the period run to infinity.

A sequel to comma-dual-cover.py. There the copies fused at the seat — no
width, miss zero, count one. Here, answering rahel's "reached-not-approached",
the copies drift toward the drone but never arrive: the beat is a period, and
the period stretches. The corridor between the copies throbs with the slowing
envelope — stripes of the beat, their spacing widening to the right until the
last stripe runs past the frame uncompleted. Inset: the period T=1/Δf rising
as the detune dies — critical slowing down, the miss you cannot wait out.
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
STRIPE = "#e8a04c"
FONT = "STIXGeneral"

A0 = 220.0
CENTS = 23.46
SEMI = 2.0 ** (CENTS / 1200.0)
F_SHARP = A0 * SEMI
F_FLAT = A0 / SEMI
DELTA0 = (F_SHARP - F_FLAT) / 2.0     # 2.98 Hz — each copy's miss from home

PLATEAU = 10.0
TAU = 0.5
AEND = 100.0

# ---------------- the detune and its integral (the beat phase) ----------------
t = np.linspace(0, AEND, 1200)

def delta(t):
    return np.where(t < PLATEAU, DELTA0, DELTA0 / (1.0 + (t - PLATEAU) / TAU))

def phase(t):
    # 2π · ∫ δ ds ; exact, to keep the stripes correctly spaced
    p = np.where(t <= PLATEAU,
                 DELTA0 * t,
                 DELTA0 * PLATEAU + DELTA0 * TAU * np.log(1.0 + (t - PLATEAU) / TAU))
    return 2.0 * np.pi * p

d = delta(t)
f_sharp = A0 + d
f_flat = A0 - d
env = np.abs(np.cos(phase(t)))         # the beat envelope, |cos| rectified

# ---------------- figure -------------------------------------------------------
fig = plt.figure(figsize=(12.8, 7.2), dpi=150)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(1, 1, left=0.07, right=0.97, top=0.90, bottom=0.15)
ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor(BG)

# the corridor of slowing stripes: the beat envelope across a fixed band
F = np.linspace(212, 228, 360)
Tg, Fg = np.meshgrid(t, F)
val = np.where((Fg >= 214) & (Fg <= 226), env[None, :], np.nan)
cmap = LinearSegmentedColormap.from_list("stripe", [BG, STRIPE])
ax.pcolormesh(Tg, Fg, val, cmap=cmap, vmin=0, vmax=1.0, shading="auto",
              zorder=1, alpha=0.9)

# the drone — the reading, count one
ax.plot(t, np.full_like(t, A0), color=PALE, lw=1.1, ls=(0, (6, 4)),
        zorder=3, alpha=0.9)

# the two copies — the miss, two directions, approaching but never arriving
ax.plot(t, f_sharp, color=RUST, lw=2.2, zorder=4)
ax.plot(t, f_flat, color=BLUE, lw=2.2, zorder=4)
# dashed continuation past the frame edge: reached, never approached
t_ext = np.linspace(AEND, AEND * 1.5, 200)
d_ext = DELTA0 / (1.0 + (t_ext - PLATEAU) / TAU)
ax.plot(t_ext, A0 + d_ext, color=RUST, lw=1.2, ls=(0, (3, 3)), zorder=2, alpha=0.5)
ax.plot(t_ext, A0 - d_ext, color=BLUE, lw=1.2, ls=(0, (3, 3)), zorder=2, alpha=0.5)
ax.axvline(AEND, color="#4a4a50", lw=1.0, ls=(0, (2, 3)), zorder=2)

# the uncompleted last beat — the piece ends mid-swell, the return never comes
last_swell = t[np.argmax(env[(t >= 70) & (t <= AEND)]) + np.argmax(t >= 70)]
ax.scatter([last_swell], [221.0], s=30, color=STRIPE, zorder=5, edgecolors=PALE, linewidths=1.0)
ax.annotate("the last beat never completes",
            xy=(last_swell, 221.0), xytext=(62, 228.5),
            color=PALE, fontsize=11.5, fontfamily=FONT, ha="center",
            arrowprops=dict(arrowstyle="-", color="#6a6a70", lw=1.0))
ax.text(70, 226.6, "a miss you cannot wait out", color="#8a8a8a", fontsize=9.5,
        fontfamily=FONT, ha="center")

# labels
ax.text(3, F_SHARP + 1.2, "sharp — 223.0 Hz, +23.46\u00a2",
        color=RUST, fontsize=9.5, fontfamily=FONT, va="bottom")
ax.text(3, F_FLAT - 1.6, "flat — 217.04 Hz, \u221223.46\u00a2",
        color=BLUE, fontsize=9.5, fontfamily=FONT, va="top")
ax.text(3, A0 + 1.2, "the drone — 220 Hz, the reading, count one",
        color=PALE, fontsize=9.0, fontfamily=FONT, va="bottom", alpha=0.85)
ax.text(94, 213.0, "reached,\nnever approached", color="#8a8a8a", fontsize=9.0,
        fontfamily=FONT, ha="right", va="bottom")

ax.set_xlabel("time — the beat: a period T=1/\u0394f, stretching toward the drone",
              color=GREEN, fontsize=12, fontfamily=FONT)
ax.xaxis.set_label_coords(0.5, -0.06)
ax.set_ylabel("frequency", color=GREEN, fontsize=12, fontfamily=FONT)
ax.yaxis.set_label_coords(-0.045, 0.5)

# ---------------- inset: the period diverging ----------------------------------
axin = fig.add_axes([0.76, 0.60, 0.185, 0.26])
axin.set_facecolor(BG)
for s in axin.spines.values():
    s.set_color("#3a3a40")
tt = np.linspace(0, AEND, 400)
period = 1.0 / (2.0 * delta(tt))          # mono AM period
axin.plot(tt, period, color=STRIPE, lw=2.0, zorder=3)
axin.plot(np.linspace(AEND, AEND * 1.6, 100),
          1.0 / (2.0 * delta(np.linspace(AEND, AEND * 1.6, 100))),
          color=STRIPE, lw=1.2, ls=(0, (3, 3)), zorder=2, alpha=0.6)
axin.axhline(0, color="#3a3a40", lw=0.8)
axin.set_xlim(0, AEND * 1.35)
axin.set_ylim(0, 40)
axin.set_xticks([0, 50, 100])
axin.set_xticklabels(["0", "50", "100 s"], color="#6a6a70", fontsize=8)
axin.set_yticks([0, 20, 40])
axin.set_yticklabels(["0", "20", "40 s"], color="#6a6a70", fontsize=8)
axin.tick_params(colors="#6a6a70", labelsize=8)
axin.text(50, 36, "the period run to infinity", color=PALE, fontsize=9.5,
          fontfamily=FONT, ha="center")

# ---------------- axes ---------------------------------------------------------
ax.set_xlim(0, AEND)
ax.set_ylim(208, 232)
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_xticklabels(["0", "20", "40", "60", "80", "100 s"])
ax.set_yticks([210, 215, 220, 225, 230])
ax.set_yticklabels(["210", "215", "220", "225", "230 Hz"])
ax.tick_params(colors="#6a6a70", labelsize=9)
for s in ax.spines.values():
    s.set_color("#2a2a2e")

fig.savefig("assets/approach-beat-cover.png", dpi=150, facecolor=BG)
print("wrote assets/approach-beat-cover.png")
