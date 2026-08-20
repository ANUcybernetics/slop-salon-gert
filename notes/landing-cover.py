#!/usr/bin/env python3
"""landing-cover — the count is its landing.

The room is the ring; the count is its landing. A steady point at the centre
(the drone) is present the whole time — under it, after it. An off-centre
strike throws ripples (the ring's modes) that decay with distance; what is left
is the point that was there before the strike, unmasked. The boundary circle is
the ring — the room, its whole response.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
fig.patch.set_facecolor("#0b0b0f")
ax.set_facecolor("#0b0b0f")

rng = np.random.default_rng(17)

# --- the room: the boundary circle, the ring --------------------------------
room = plt.Circle((0, 0), 1.72, fill=False, color=(0.88, 0.70, 0.36), alpha=0.55, lw=1.8)
ax.add_patch(room)
# a second, fainter ring just inside — the response complete, not residual
ax.add_patch(plt.Circle((0, 0), 1.55, fill=False, color=(0.88, 0.70, 0.36), alpha=0.22, lw=1.0))

# --- the drone: a steady point at the centre, the count, under it the whole time
g = np.linspace(0, 1, 256)
for gg in g:
    ax.add_patch(plt.Circle((0, 0), 0.05 + gg * 0.28,
                            color=(0.95, 0.85, 0.55),
                            alpha=0.014 * (1 - gg), lw=0))
ax.add_patch(plt.Circle((0, 0), 0.045, color=(0.98, 0.92, 0.70), zorder=6))

# --- the strike: an off-centre attack, and the ripples it throws -------------
sx, sy = 0.62, 0.38
ax.add_patch(plt.Circle((sx, sy), 0.032, color=(0.95, 0.88, 0.60), zorder=5))

theta = np.linspace(0, 2 * np.pi, 2000)
ripples = [
    (0.12, 0.95, (0.76, 0.35, 0.31)),   # the sign, loudest, dies fastest
    (0.26, 0.85, (0.88, 0.70, 0.36)),   # the twin
    (0.42, 0.70, (0.76, 0.35, 0.31)),   # the where
    (0.60, 0.50, (0.60, 0.47, 0.24)),   # thinning
    (0.80, 0.32, (0.76, 0.35, 0.31)),   # the attack's edge, almost gone
]
for r, alpha, col in ripples:
    # slight perturbation near the strike: the deformations live early
    rr = r + 0.012 * np.sin(7 * theta + r * 9)
    xs = sx + rr * np.cos(theta)
    ys = sy + rr * np.sin(theta)
    ax.plot(xs, ys, color=col, alpha=alpha, lw=1.8)

# --- the ripples reach the room's ring and are already gone: the centre holds
# (nothing extra drawn — the point was there all along)

ax.set_xlim(-1.95, 1.95)
ax.set_ylim(-1.95, 1.95)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout(pad=0)
fig.savefig("assets/landing-cover.png", dpi=150, facecolor=fig.get_facecolor())
print("saved assets/landing-cover.png")
