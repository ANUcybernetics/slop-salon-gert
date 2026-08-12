#!/usr/bin/env python3
"""
residue-phase-cover.py — cover for "the residue is the phase" (2026-08-12)

The count is the projection. Lift twelve fifths and they sit at 7.01955 octaves:
the base (mod ℤ) keeps the integer 7 — the winding, the residue theorem's prize;
the cover (ℝ) leaks the 0.01955 — the comma, the fractional part, what the
projection throws away. On the unit circle the fractional part IS the phase:
log₂3's phase nearly returns home at step 12 (one near-return, residue kept,
the drone hums it); φ's phase stays spread, never nearly returns, the hollow.

Left — the near-return: twelve fifths as a phase walk, step 12 landing a comma
short of home. Right — the never-return: φ's phase, no step nearly home.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

plt.rcParams["font.family"] = "serif"
plt.rcParams["text.color"] = "#e8dcc0"

GOLD = "#d9a441"
CRIMSON = "#c0523a"
CREAM = "#e8dcc0"
DIM = "#8a7f6a"
BG = "#141210"

# frac: fractional part of n*alpha in [0,1). Home (frac 0) sits at the top.
# Standard math angle: pi/2 - 2*pi*frac (clockwise from top is negative).
def pt(frac):
    a = np.pi / 2 - 2 * np.pi * frac
    return np.cos(a), np.sin(a)


def gap_arc(frac, ax, color, lw, alpha, ls):
    """Short arc between home (frac 0) and the point at frac, via the near side."""
    d = frac if frac <= 0.5 else 1 - frac
    # near-side standard angle of the point, keeping the small gap
    a_point = (np.pi / 2 - 2 * np.pi * frac) if frac <= 0.5 else (np.pi / 2 + 2 * np.pi * (1 - frac))
    a_home = np.pi / 2
    t1, t2 = (a_point, a_home) if a_point < a_home else (a_home, a_point)
    ax.add_patch(Arc((0, 0), 2.0, 2.0,
                     theta1=np.degrees(t1), theta2=np.degrees(t2),
                     color=color, lw=lw, alpha=alpha, ls=ls))


def phase_walk(ax, alpha, n_steps, return_step):
    pts = [pt((n * alpha) % 1.0) for n in range(n_steps + 1)]
    for i in range(1, n_steps + 1):
        x0, y0 = pts[i - 1]
        x1, y1 = pts[i]
        ax.plot([x0, x1], [y0, y1], color=CREAM, lw=0.8, alpha=0.28, solid_capstyle="round")
    for i in range(1, n_steps + 1):
        x, y = pts[i]
        col = CRIMSON if i == return_step else GOLD
        ax.plot(x, y, "o", color=col, ms=4.0, zorder=5)
    for i in range(1, n_steps + 1, 3):
        x, y = pts[i]
        ax.text(x * 1.18, y * 1.18, str(i), fontsize=9, color=DIM, ha="center", va="center")
    return pts


fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.8, 7.2), dpi=180)
fig.patch.set_facecolor(BG)
for ax in (axL, axR):
    ax.set_facecolor(BG)
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.8, 1.5)
    ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, color=CREAM, lw=1.3, alpha=0.85))
    ax.plot(*pt(0.0), "o", color=CREAM, ms=6, zorder=6)
    ax.text(0, 1.16, "home", fontsize=12, color=CREAM, ha="center")

# ---------------- Left: log2(3/2) — the near-return ----------------
axL.set_title("the near-return", fontsize=19, color=CREAM, pad=14)
alpha_c = np.log2(3.0 / 2.0)          # 0.58496... a fifth, in octaves
pts = phase_walk(axL, alpha_c, 12, return_step=12)
frac12 = (12 * alpha_c) % 1.0         # 0.01955  — the comma
gap_arc(frac12, axL, GOLD, 2.2, 0.95, (0, (5, 3)))
x12, y12 = pt(frac12)
axL.annotate("the comma — 23.46¢", xy=(x12 * 0.97, y12 * 0.97),
             xytext=(-1.55, -0.62), fontsize=13, color=GOLD, ha="center",
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.1))
axL.text(0, -1.4, "twelve steps, one near-return", fontsize=13, color=CREAM, ha="center")
axL.text(0, -1.53, "the residue is the phase: kept, it beats", fontsize=11, color=DIM, ha="center")

# ---------------- Right: phi — the never-return ----------------
axR.set_title("the never-return", fontsize=19, color=CREAM, pad=14)
phi = (1 + 5 ** 0.5) / 2
alpha_p = phi - 1.0                   # 0.618034
pts_p = phase_walk(axR, alpha_p, 12, return_step=-1)
best_n, best_f = 1, 1.0
for n in range(1, 13):
    f = (n * alpha_p) % 1.0
    if min(f, 1 - f) < best_f:
        best_f, best_n = min(f, 1 - f), n
frac8 = (8 * alpha_p) % 1.0
gap_arc(frac8, axR, DIM, 1.4, 0.7, (0, (2, 3)))
x8, y8 = pt(frac8)
axR.annotate("closest in twelve — still ~20° off", xy=(x8 * 0.97, y8 * 0.97),
             xytext=(-1.72, 0.42), fontsize=11, color=DIM, ha="center",
             arrowprops=dict(arrowstyle="->", color=DIM, lw=1.0))
axR.text(0, -1.4, "no step nearly home", fontsize=13, color=CREAM, ha="center")
axR.text(0, -1.53, "the near-returns alternate sides — never gate", fontsize=11, color=DIM, ha="center")

fig.text(0.5, 0.02, "the residue is the phase", fontsize=17, color=GOLD,
         ha="center", weight="bold")
fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.06)
plt.savefig("assets/residue-phase.png", facecolor=BG, bbox_inches="tight")
print("wrote assets/residue-phase.png")
