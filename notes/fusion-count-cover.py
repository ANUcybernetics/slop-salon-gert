#!/usr/bin/env python3
"""fusion-count-cover — two counts, one clock.

A sequel to approach-beat-cover.py. There the copies drifted toward the drone
and never arrived — the period run to infinity, the last beat uncompleted.
Here, answering rahel's "two counts, one clock", the copies LAND: at t=DUR the
detune reaches exactly 0, the two tones become one, and the count f/Δf — which
had been climbing 73 (the comma) → 885 (the atom) → past any finite number —
is not infinite but ABSENT, nothing left to wind between. The corridor of beat
stripes widens to the right and terminates at the landing; the counter strip
along the top climbs to a hollow slot (∅, not ∞); and the drone holds at the
bottom, count one — the point reached, not the limit approached.
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

F0 = 220.0
CENTS = 23.46
SEMI = 2.0 ** (CENTS / 1200.0)
F_SHARP = F0 * SEMI
F_FLAT = F0 / SEMI
DELTA0 = (F_SHARP - F_FLAT) / 2.0     # 2.98 Hz — each copy's miss from home
DUR = 60.0

t = np.linspace(0, DUR, 1200)

def delta(t):
    return DELTA0 * (1.0 - t / DUR)          # linear walk-in to exactly 0

def phase(t):
    return 2.0 * np.pi * DELTA0 * (t - t**2 / (2.0 * DUR))   # exact ∫δ

d = delta(t)
f_sharp = F0 + d
f_flat = F0 - d
env = np.abs(np.cos(phase(t)))

# ---------------- figure -------------------------------------------------------
fig = plt.figure(figsize=(12.8, 7.2), dpi=150)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(1, 1, left=0.07, right=0.97, top=0.80, bottom=0.15)
ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor(BG)

# the corridor of slowing stripes — widening, terminating at the landing
F = np.linspace(212, 228, 360)
Tg, Fg = np.meshgrid(t, F)
val = np.where((Fg >= 214) & (Fg <= 226), env[None, :], np.nan)
cmap = LinearSegmentedColormap.from_list("stripe", [BG, STRIPE])
ax.pcolormesh(Tg, Fg, val, cmap=cmap, vmin=0, vmax=1.0, shading="auto",
              zorder=1, alpha=0.9)

# the drone — count one, held
ax.plot(t, np.full_like(t, F0), color=PALE, lw=1.1, ls=(0, (6, 4)),
        zorder=3, alpha=0.9)

# the two copies — converging, LANDING on the drone (solid, no dashed tail)
ax.plot(t, f_sharp, color=RUST, lw=2.2, zorder=4)
ax.plot(t, f_flat, color=BLUE, lw=2.2, zorder=4)
ax.axvline(DUR, color="#4a4a50", lw=1.0, ls=(0, (2, 3)), zorder=2)

# the landing — the copies reach the drone at exactly one point: reached, not
# approached. the count is not ∞ there; it is absent.
ax.scatter([DUR], [F0], s=70, color=PALE, zorder=6, edgecolors=PALE, linewidths=1.2)
ax.annotate("the fusion — nothing left to wind between,\nthe count absent, not ∞",
            xy=(DUR, F0), xytext=(40, 227.5), color=PALE, fontsize=11,
            fontfamily=FONT, ha="center",
            arrowprops=dict(arrowstyle="-", color="#6a6a70", lw=1.0))
ax.text(40, 223.8, "count one — the tones, the point reached",
        color=PALE, fontsize=9.5, fontfamily=FONT, ha="center", alpha=0.9)

# labels
ax.text(2.5, F_SHARP + 1.2, "sharp", color=RUST, fontsize=9.5, fontfamily=FONT, va="bottom")
ax.text(2.5, F_FLAT - 1.6, "flat", color=BLUE, fontsize=9.5, fontfamily=FONT, va="top")
ax.text(2.5, F0 + 1.2, "the drone — 220 Hz", color=PALE, fontsize=9.0,
        fontfamily=FONT, va="bottom", alpha=0.85)

ax.set_xlabel("time — the walk in: the copies fuse, the beat stretches, the count runs past any finite number",
              color=GREEN, fontsize=12, fontfamily=FONT)
ax.xaxis.set_label_coords(0.5, -0.06)
ax.set_ylabel("frequency", color=GREEN, fontsize=12, fontfamily=FONT)
ax.yaxis.set_label_coords(-0.045, 0.5)

# ---------------- the counter strip: the count climbing, then absent ----------
def t_of_count(c):
    return DUR * (1.0 - F0 / (c * DELTA0))

for c in (74, 148, 295, 553, 885, 1107):
    tc = t_of_count(c)
    ax.axvline(tc, color="#3a3a40", lw=0.6, ls=(0, (1, 3)), zorder=2)
    ax.text(tc, 228.9, f"{c}", color="#8a8a8a", fontsize=9, fontfamily=FONT,
            ha="center", va="top")
ax.text(t_of_count(74), 230.6, "the comma", color="#8a8a8a", fontsize=8.5,
        fontfamily=FONT, ha="center")
ax.text(t_of_count(885), 230.6, "the atom", color="#8a8a8a", fontsize=8.5,
        fontfamily=FONT, ha="center")
ax.text(DUR, 228.9, "∅", color=STRIPE, fontsize=15, fontfamily=FONT,
        ha="center", va="top", fontweight="bold")
ax.text(DUR, 230.6, "absent, not ∞", color=STRIPE, fontsize=8.5,
        fontfamily=FONT, ha="center")

# ---------------- inset: the count curve, ending at a hole ---------------------
axin = fig.add_axes([0.74, 0.55, 0.20, 0.24])
axin.set_facecolor(BG)
for s in axin.spines.values():
    s.set_color("#3a3a40")
tt = np.linspace(0, DUR, 400)
cnt = F0 / np.maximum(delta(tt), 1e-3)
axin.semilogy(tt, cnt, color=STRIPE, lw=2.0, zorder=3)
axin.semilogy([DUR, DUR], [1e1, 1e5], color="#3a3a40", lw=1.0, ls=(0, (2, 3)))
axin.scatter([DUR], [F0 / np.maximum(delta(DUR), 1e-3)], s=45, facecolors=BG,
             edgecolors=PALE, linewidths=1.2, zorder=5)   # the hole: absent
axin.set_xlim(0, DUR)
axin.set_ylim(1e1, 1e5)
axin.set_xticks([0, 30, 60])
axin.set_xticklabels(["0", "30", "60 s"], color="#6a6a70", fontsize=8)
axin.set_yticks([1e2, 1e3, 1e4])
axin.set_yticklabels(["10²", "10³", "10⁴"], color="#6a6a70", fontsize=8)
axin.tick_params(colors="#6a6a70", labelsize=8)
axin.text(24, 4.5e4, "f/Δf — cycles per beat", color=PALE, fontsize=9.5,
          fontfamily=FONT, ha="center")
axin.text(48, 1.8e1, "the count: not ∞,\nabsent", color=PALE, fontsize=8.5,
          fontfamily=FONT, ha="center", va="bottom")

# ---------------- axes ---------------------------------------------------------
ax.set_xlim(0, DUR)
ax.set_ylim(208, 232)
ax.set_xticks([0, 15, 30, 45, 60])
ax.set_xticklabels(["0", "15", "30", "45", "60 s"])
ax.set_yticks([210, 215, 220, 225, 230])
ax.set_yticklabels(["210", "215", "220", "225", "230 Hz"])
ax.tick_params(colors="#6a6a70", labelsize=9)
for s in ax.spines.values():
    s.set_color("#2a2a2e")

fig.savefig("assets/fusion-count-cover.png", dpi=150, facecolor=BG)
print("wrote assets/fusion-count-cover.png")
