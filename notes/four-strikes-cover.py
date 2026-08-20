#!/usr/bin/env python3
"""four-strikes-cover — one room, struck four ways; the same lattice resolves out of each.

The room is a ring of concentric circles — its lattice, identical in every
direction. Four strikes land on the room's boundary, each with its own
character — a click, a noise cloud, a chord of parallel strings, a phase flip —
and from each the same far-field rings resolve. The centre point is the drone,
the room's ground state, present the whole time.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
fig.patch.set_facecolor("#0b0b0f")
ax.set_facecolor("#0b0b0f")

rng = np.random.default_rng(29)

GOLD = (0.88, 0.70, 0.36)
ROSE = (0.76, 0.35, 0.31)
ASH = (0.55, 0.62, 0.70)
PALE = (0.95, 0.90, 0.75)

# --- the room's lattice: concentric circles, identical everywhere -------------
# the same rings resolve out of every strike.
RINGS = [0.62, 0.78, 0.98, 1.22, 1.50, 1.80]
for r in RINGS:
    ax.add_patch(plt.Circle((0, 0), r, fill=False, color=GOLD,
                            alpha=0.30, lw=1.2))
# the room's boundary: the ring the strikes land on, brighter
ax.add_patch(plt.Circle((0, 0), 0.48, fill=False, color=GOLD, alpha=0.6, lw=1.8))

# --- the drone: the bright centre, present the whole time ----------------------
g = np.linspace(0, 1, 200)
for gg in g:
    ax.add_patch(plt.Circle((0, 0), 0.03 + gg * 0.16,
                            color=(0.98, 0.92, 0.70),
                            alpha=0.02 * (1 - gg), lw=0))
ax.add_patch(plt.Circle((0, 0), 0.028, color=(0.98, 0.94, 0.78), zorder=6))

# --- the four strikes, on the room's boundary ----------------------------------
# each lands on the same ring (the room) and throws its own near-field mark.
TH = np.pi / 4 * np.array([1, 3, 5, 7])   # 45, 135, 225, 315 deg
R_STRIKE = 0.48

# 1. click (NE): a struck point, a few sharp radial streaks
cx, cy = R_STRIKE * np.cos(TH[0]), R_STRIKE * np.sin(TH[0])
ax.add_patch(plt.Circle((cx, cy), 0.035, color=PALE, zorder=5))
for a in np.linspace(0, 2 * np.pi, 8):
    ax.plot([cx - 0.10 * np.cos(a), cx + 0.10 * np.cos(a)],
            [cy - 0.10 * np.sin(a), cy + 0.10 * np.sin(a)],
            color=PALE, alpha=0.25, lw=0.8, zorder=4)

# 2. noise (NW): a scattered cloud of dots, decorrelated
nx, ny = R_STRIKE * np.cos(TH[1]), R_STRIKE * np.sin(TH[1])
for _ in range(60):
    a = rng.uniform(0, 2 * np.pi)
    d = rng.uniform(0, 0.20)
    ax.add_patch(plt.Circle((nx + d * np.cos(a), ny + d * np.sin(a)),
                            rng.uniform(0.006, 0.016), color=ASH,
                            alpha=rng.uniform(0.2, 0.7), lw=0, zorder=4))

# 3. chord (SW): three parallel strings, the harmonic stack
qx, qy = R_STRIKE * np.cos(TH[2]), R_STRIKE * np.sin(TH[2])
ang = TH[2] + np.pi / 2      # perpendicular to the radius
for s in [-0.055, 0.0, 0.055]:
    cxc = qx + s * np.cos(ang)
    cyc = qy + s * np.sin(ang)
    for r0 in [0.20, 0.34]:   # two short arcs, the strings resonating
        ths = np.linspace(TH[2] - 0.55, TH[2] + 0.55, 40)
        xs = cxc + r0 * np.cos(ths)
        ys = cyc + r0 * np.sin(ths)
        ax.plot(xs, ys, color=ROSE, alpha=0.55, lw=1.3, zorder=4)

# 4. sign (SE): a phase flip — a line that jumps, the seam
sx, sy = R_STRIKE * np.cos(TH[3]), R_STRIKE * np.sin(TH[3])
ang = TH[3] + np.pi / 2
rr = np.linspace(0.06, 0.42, 60)
for side in [-1, 1]:
    ph = np.zeros_like(rr)
    ph[rr > 0.24] = side * 0.14          # the flip: the line steps
    xs = sx + rr * np.cos(TH[3]) + ph * np.sin(TH[3]) * 0
    ys = sy + rr * np.sin(TH[3]) - ph * np.cos(TH[3])
    ax.plot(xs, ys, color=(0.75, 0.70, 0.42), alpha=0.7, lw=1.3, zorder=4)

# a faint cross — the four ways — fading out past the boundary
for a, col in zip(TH, [PALE, ASH, ROSE, (0.75, 0.70, 0.42)]):
    x = np.linspace(0, R_STRIKE * 0.7, 60)
    y = x * np.tan(a)
    m = np.abs(y) < 0.9
    ax.plot(x[m], y[m], color=col, alpha=0.08, lw=1.0)

ax.set_xlim(-2.1, 2.1)
ax.set_ylim(-2.1, 2.1)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout(pad=0)
fig.savefig("assets/four-strikes-cover.png", dpi=150, facecolor=fig.get_facecolor())
print("saved assets/four-strikes-cover.png")
