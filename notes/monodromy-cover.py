#!/usr/bin/env python3
"""monodromy-cover — the loop around the gate, seen.

Left panel:  the b-plane of the inverse-pair x²+bx+1.  The gates (the branch
             points of √(b²−4)) sit at b=±2, the fused landings; between them
             the ghost (|b|<2, the pair rides the unit circle), outside the
             sign (|b|>2, a real pair).  A loop circles the gate at b=−2 —
             and comes back to the same place with the sheets exchanged.
Right panel: the roots in the complex plane, one lap of the loop.  Two strands,
             the bright root and the pure root, start on the real axis (1.72
             and 0.58), swing onto the unit circle at the ghost (e^{±iθ}), and
             return — swapped.  The braid is the monodromy.
Bottom:      the two voices' pitch over two laps: they cross at the ghost,
             and after one lap the high and low have exchanged; after two, home.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch

GOLD = (0.88, 0.70, 0.36)
PALE = (0.95, 0.90, 0.75)
ROSE = (0.76, 0.35, 0.31)
VIOLET = (0.62, 0.50, 0.82)
ASH = (0.55, 0.62, 0.70)
BG = "#0b0b0f"

UNIT = 220.0
R = 0.3
GATE = -2.0
LAP = 20.0
T0 = 2.0

fig = plt.figure(figsize=(10.2, 7.8), dpi=150, facecolor=BG)
gs = fig.add_gridspec(2, 2, height_ratios=[3.6, 1.8], hspace=0.5, wspace=0.28,
                      left=0.06, right=0.97, top=0.86, bottom=0.08)

# =================== left: the b-plane with the loop ===========================
ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor(BG)
ax.axis("off")

# the two regions along the real axis: ghost inside |b|<2, sign outside
ax.axhspan(-0.02, 0.02, xmin=0.5 - 0.14, xmax=0.5 + 0.14, color=VIOLET, alpha=0.10)
ax.axhspan(-0.02, 0.02, xmin=0.5 - 0.34, xmax=0.5 - 0.14, color=ROSE, alpha=0.10)
ax.axhspan(-0.02, 0.02, xmin=0.5 + 0.14, xmax=0.5 + 0.34, color=ROSE, alpha=0.10)

# real axis
ax.plot([-4.2, 4.2], [0, 0], color=ASH, lw=1.1, alpha=0.75, zorder=1)
ax.text(4.1, -0.30, "the b-plane of x²+bx+1", color=PALE, fontsize=8.5, ha="right")
ax.text(0, -0.55, "b = 0", color=ASH, fontsize=7.5, ha="center")

# the two gates (branch points)
for gx, lab in ((2.0, "b = +2"), (-2.0, "b = −2")):
    ax.plot(gx, 0, 'D', ms=9, mfc=GOLD, mec=GOLD, zorder=6)
ax.text(2.0, 0.32, "b = +2", color=GOLD, fontsize=8, ha="center")
ax.text(-2.0, 0.32, "b = −2", color=GOLD, fontsize=8, ha="center")
ax.text(-2.0, 0.66, "the gate —\nthe fused landing", color=GOLD, fontsize=7.5,
        ha="center", linespacing=1.3)

# the branch cut between the gates
ax.plot([-2.0, 2.0], [0, 0], color=ASH, lw=1.4, ls=(0, (2, 2)), alpha=0.8, zorder=2)
ax.text(0, -0.32, "the ghost: |b| < 2", color=VIOLET, fontsize=8, ha="center")
ax.text(3.1, -0.32, "the sign: |b| > 2", color=ROSE, fontsize=8, ha="center")

# the loop around the gate at b=−2
loop = Circle((-2.0, 0), R, fill=False, ec=GOLD, lw=2.4, zorder=5)
ax.add_patch(loop)
# direction arrow
ang = 60 * np.pi / 180
ax.add_patch(FancyArrowPatch((-2.0 + R * np.cos(ang), R * np.sin(ang) * 0.9),
                             (-2.0 + R * np.cos(ang + 0.7), R * np.sin(ang + 0.7) * 0.9),
                             arrowstyle="->", mutation_scale=11, color=GOLD, lw=1.4))
# where the loop crosses the real axis
ax.plot(-2.0 + R, 0, 'o', ms=7, mfc=ROSE, mec=ROSE, zorder=7)
ax.plot(-2.0 - R, 0, 'o', ms=7, mfc=ROSE, mec=ROSE, zorder=7)
ax.text(-2.0 + R, -0.30, "the pair,\nexchanged", color=ROSE, fontsize=7,
        ha="center", va="top", linespacing=1.2)
ax.annotate("", xy=(-2.0 - R, 0.05), xytext=(-2.0 + R, 0.05),
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.2))
ax.text(-1.3, 1.0, "one lap around the gate\n— never crossing it —", color=GOLD,
        fontsize=9, ha="center", linespacing=1.5)

ax.set_xlim(-4.4, 4.4)
ax.set_ylim(-1.35, 1.85)
ax.set_title("circle the landing, don't land", color=GOLD, fontsize=10.5,
             pad=6, loc="left")

# =================== right: the roots, one lap — the braid =====================
ax = fig.add_subplot(gs[0, 1])
ax.set_facecolor(BG)
ax.axis("off")

# the unit circle and real axis
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color=GOLD, lw=1.6, alpha=0.85, zorder=2)
ax.plot([-3.0, 3.0], [0, 0], color=ASH, lw=0.9, alpha=0.55, zorder=1)
ax.text(2.9, -0.25, "the unit circle |r| = 1", color=PALE, fontsize=7.5,
        ha="right", va="top")

# the two roots' paths over one lap (continuous sqrt, as in the audio)
phi = np.linspace(0, 2 * np.pi, 3000)
b = GATE - R * np.exp(1j * phi)
Delta = b * b - 4.0
argD = np.unwrap(np.angle(Delta))
sq = np.sqrt(np.abs(Delta)) * np.exp(0.5j * argD)
r1 = (-b + sq) / 2.0
r2 = (-b - sq) / 2.0

ax.plot(r1.real, r1.imag, color=ROSE, lw=2.4, zorder=5)
ax.plot(r2.real, r2.imag, color=VIOLET, lw=2.4, zorder=5)

# start points (diamonds) and end points (circles) — the swap
ax.plot(r1.real[0], r1.imag[0], 'D', ms=9, mfc=ROSE, mec=BG, mew=1.2, zorder=7)
ax.plot(r2.real[0], r2.imag[0], 'D', ms=9, mfc=VIOLET, mec=BG, mew=1.2, zorder=7)
ax.plot(r1.real[-1], r1.imag[-1], 'o', ms=10, mfc=BG, mec=ROSE, mew=2.2, zorder=7)
ax.plot(r2.real[-1], r2.imag[-1], 'o', ms=10, mfc=BG, mec=VIOLET, mew=2.2, zorder=7)

# the ghost points where the pair sits on the circle
gth = np.arccos(0.85)  # e^{±iθ} for the crossing at b = −1.7
for sg, col in ((1, ROSE), (-1, VIOLET)):
    ax.plot(np.cos(sg * gth), np.sin(sg * gth), '*', ms=12, mfc=GOLD, mec=GOLD,
            zorder=8)

ax.text(0, 1.55, "the ghost: the pair on the circle", color=GOLD, fontsize=8.5,
        ha="center")
ax.text(2.1, -0.55, "start: bright high", color=ROSE, fontsize=7.5, ha="right")
ax.text(2.1, -0.85, "end:   bright low", color=ROSE, fontsize=7.5, ha="right")
ax.text(-1.9, 1.35, "one lap —\nthe sheets exchange", color=PALE, fontsize=9,
        ha="center", linespacing=1.5)

ax.set_xlim(-2.6, 2.6)
ax.set_ylim(-1.45, 2.0)
ax.set_aspect("equal")
ax.set_title("one lap: the transposition", color=PALE, fontsize=10.5, pad=6,
             loc="left")

# =================== bottom: the two voices' pitch over two laps ================
ax = fig.add_subplot(gs[1, :])
ax.set_facecolor(BG)
tfull = np.linspace(0, 2 * 2 * np.pi, 4000)
bf = GATE - R * np.exp(1j * tfull)
Df = bf * bf - 4.0
adf = np.unwrap(np.angle(Df))
sqf = np.sqrt(np.abs(Df)) * np.exp(0.5j * adf)
f1f = UNIT * np.abs((-bf + sqf) / 2.0)
f2f = UNIT * np.abs((-bf - sqf) / 2.0)
tlap = T0 + np.linspace(0, 2 * LAP, len(tfull))

ax.plot(tlap, f1f, color=ROSE, lw=2.2)
ax.plot(tlap, f2f, color=VIOLET, lw=2.2)
ax.axhline(UNIT, color=GOLD, lw=1.1, ls=(0, (3, 2)), alpha=0.8)
ax.text(43.5, UNIT + 14, "the norm's pitch 220", color=GOLD, fontsize=7.5,
        ha="right")
# lap ends
for le in (T0 + LAP, T0 + 2 * LAP):
    ax.plot([le, le], [60, 460], color=ASH, lw=0.9, alpha=0.5)
ax.text(T0 + LAP / 2, 470, "lap 1 — the exchange", color=PALE, fontsize=8.5,
        ha="center")
ax.text(T0 + 3 * LAP / 2, 470, "lap 2 — home", color=PALE, fontsize=8.5,
        ha="center")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color(ASH); s.set_alpha(0.45)
ax.set_xlim(T0 - 0.5, T0 + 2 * LAP + 1.5)
ax.set_ylim(55, 500)
ax.set_title("the two voices: bright and pure, crossing at the ghost — "
             "after one lap the high and the low have exchanged", color=PALE,
             fontsize=9.5, pad=5, loc="left")

fig.suptitle("the monodromy around the gate: one lap, the sheets exchange; "
             "two, home", color=PALE, fontsize=12, y=0.955)
fig.savefig("assets/monodromy-cover.png", dpi=150, facecolor=BG)
print("saved assets/monodromy-cover.png")
