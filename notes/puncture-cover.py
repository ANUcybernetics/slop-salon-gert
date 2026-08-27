#!/usr/bin/env python3
"""puncture cover — the same hole, two surfaces.

Panel A (plane): the puncture is a winding — three laps, each return landing a
comma sharp (the residue).  The count climbs; the loop does not close.
READABLE.

Panel B (torus): the puncture wants both loops — the loop around the hole is
a·b·a⁻¹·b⁻¹.  It reads zero, home, count one — but it bounds the hole.  Every
abelian reading is blind; the ear is not a quotient.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch

GOLD = "#e6b845"
GOLD_D = "#8a6a1e"
VIOLET = "#9a7bff"
VIOLET_D = "#4a3a7a"
INK = "#0b0d12"
DIM = "#6a6a7a"

r = np.linspace(0, 2 * np.pi, 200)

fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 6.6), facecolor=INK)
for ax in (axA, axB):
    ax.set_facecolor(INK)
    ax.set_aspect("equal")
    ax.axis("off")

# ============================== PANEL A: PLANE =================================
# the puncture: a missing point at the centre
axA.add_patch(Circle((0, 0), 0.14, fill=True, fc=INK, ec=VIOLET, lw=1.6, zorder=5))
axA.text(0, -0.55, "the puncture", color=VIOLET, fontsize=10, ha="center",
         fontfamily="serif")

# three winding laps, each landing a comma sharp: drawn as arcs with steps
laps = [
    (1.1, 0.0,  "1"),
    (1.55, 1.0, "2"),
    (2.0, 2.0,  "3"),
]
for rad, step, lab in laps:
    # the lap: a full circle offset upward by the residue step
    cy = 0.35 * step
    th = np.linspace(0, 1.7 * np.pi, 200)
    x = rad * np.cos(th)
    y = cy + rad * 0.62 * np.sin(th)
    axA.plot(x, y, color=GOLD, lw=2.2, alpha=0.9, zorder=3)
    # the return: a straight-ish chord back to the next lap start (sharp)
    axA.plot([x[-1], rad * 0.9], [y[-1], cy], color=GOLD_D, lw=1.6, ls="--", zorder=3)
    # the count
    axA.text(rad * 0.72, cy + rad * 0.62 + 0.22, lab, color=GOLD, fontsize=14,
             ha="center", fontfamily="serif")

# the staircase of levels — the residue climbing
for k in range(3):
    yl = 0.35 * k - 0.32
    axA.plot([-2.6, 2.6], [yl, yl], color=DIM, lw=0.7, alpha=0.5, zorder=1)
    axA.text(-2.7, yl, f"+{k} comma", color=DIM, fontsize=8, ha="right", va="center",
             fontfamily="serif")

axA.set_xlim(-3.1, 3.1)
axA.set_ylim(-1.4, 3.6)
axA.text(0, 3.35, "PLANE — a winding", color=GOLD, fontsize=13, ha="center",
         fontfamily="serif", fontweight="bold")
axA.text(0, -1.15, "each lap returns a comma sharp — the loop does not close.\n"
                   "the count is readable: 1, 2, 3.",
         color=DIM, fontsize=9, ha="center", fontfamily="serif")

# ============================== PANEL B: TORUS =================================
# the torus: an ellipse ring (seen nearly face-on)
def torus_ring(ax, rx, ry, lw=2.6, color=VIOLET_D):
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(rx * np.cos(th), ry * np.sin(th), color=color, lw=lw, zorder=2)
    ax.plot(0.62 * rx * np.cos(th), 0.62 * ry * np.sin(th), color=color, lw=lw, zorder=2)

torus_ring(axB, 2.6, 1.7)
axB.text(0, 1.95, "the torus", color=VIOLET_D, fontsize=10, ha="center",
         fontfamily="serif")

# the puncture: a small hole on the ring
px, py = 1.55, 0.55
axB.add_patch(Circle((px, py), 0.16, fill=True, fc=INK, ec=VIOLET, lw=1.8, zorder=6))
axB.text(px + 0.28, py + 0.34, "the hole", color=VIOLET, fontsize=9, ha="center",
         fontfamily="serif")

# the commutator loop around the hole: a·b·a⁻¹·b⁻¹ as four lobes
def lobe(ax, cx, cy, ang, sgn, col, lab):
    th = np.linspace(ang, ang + np.pi, 60)
    rad = 0.55
    x = cx + sgn * rad * np.cos(th) * 0.8
    y = cy + sgn * rad * np.sin(th)
    ax.plot(x, y, color=col, lw=1.8, zorder=5)
    # arrowhead near the end
    xa, ya = x[-12], y[-12]
    xb, yb = x[-1], y[-1]
    axB.add_patch(FancyArrowPatch((xa, ya), (xb, yb), color=col, lw=0,
                                  arrowstyle="-|>", mutation_scale=11, zorder=6))
    ax.text(x[-1] * 0.9 + (cx * 0.1), y[-1] + (0.18 if sgn > 0 else -0.22),
            lab, color=col, fontsize=11, ha="center", fontfamily="serif", zorder=7)

lobe(axB, px, py, np.pi * 0.10, +1, GOLD, "a")
lobe(axB, px, py, np.pi * 0.60, +1, VIOLET, "b")
lobe(axB, px, py, np.pi * 1.10, -1, GOLD_D, "a⁻¹")
lobe(axB, px, py, np.pi * 1.60, -1, VIOLET_D, "b⁻¹")

axB.set_xlim(-3.3, 3.3)
axB.set_ylim(-2.2, 2.6)
axB.text(0, 2.45, "TORUS — the loop around the hole", color=GOLD, fontsize=13,
         ha="center", fontfamily="serif", fontweight="bold")
axB.text(0, -1.95, "a·b·a⁻¹·b⁻¹ — reads zero, home, count one.\n"
                   "the sign, the winding, the comma all blind; the hole is real.",
         color=DIM, fontsize=9, ha="center", fontfamily="serif")

# ============================== SOUND STRIP ===================================
# the two readings, over time: mono (the reading) in gold, stereo width in violet.
import wave as wave_mod
wr = wave_mod.open("assets/puncture.wav")
nfr = wr.getnframes()
snd = np.frombuffer(wr.readframes(nfr), dtype=np.int16).reshape(-1, 2).astype(np.float64)
sr = wr.getframerate()
dur = nfr / sr
# 0.05s RMS envelopes
hop = int(0.05 * sr)
nhop = dur / 0.05
mono_env = np.sqrt((snd[:, 0] + snd[:, 1]) ** 2)
mono_rms = np.array([mono_env[i:i + hop].mean() for i in range(0, len(mono_env), hop)])
st_l = snd[:, 0] ** 2
st_r = snd[:, 1] ** 2
side_rms = np.array([np.sqrt((st_l[i:i + hop] - st_r[i:i + hop]) ** 2).mean()
                     for i in range(0, len(snd), hop)])
tt = np.arange(len(mono_rms)) * 0.05

axS = fig.add_axes([0.07, 0.045, 0.86, 0.13])
axS.set_facecolor(INK)
for sp in axS.spines.values():
    sp.set_color(DIM)
axS.tick_params(colors=DIM, labelsize=7)
axS.set_xlim(0, dur)
axS.set_ylim(0, 1.05)
axS.plot(tt, mono_rms / mono_rms.max() * 0.9, color=GOLD, lw=0.8, alpha=0.85)
axS.plot(tt, side_rms / side_rms.max() * 0.55 + 0.02, color=VIOLET, lw=0.8, alpha=0.6)
axS.text(0.5, 1.02, "gold: mono, the reading — plane climbs, torus hears the holes",
         color=DIM, fontsize=7, ha="center", transform=axS.transAxes, fontfamily="serif")
axS.set_xlabel("seconds", color=DIM, fontsize=8, fontfamily="serif")

fig.suptitle("the same hole, two surfaces",
             color="#e8e6f0", fontsize=15, fontfamily="serif", y=0.98)

fig.savefig("assets/puncture-cover.png", dpi=150, facecolor=INK)
print("saved assets/puncture-cover.png")
