#!/usr/bin/env python3
"""residue-cover — the ring, held. Radius is time.

A single point is struck once. The rings it throws are perturbed near the
strike — the sign flutters, the twin beats, the where smears — and settle into
perfect circles at the far radius. Deform the room; the seam stays.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
fig.patch.set_facecolor("#0b0b0f")
ax.set_facecolor("#0b0b0f")

cx, cy = 0.0, 0.0
rng = np.random.default_rng(11)

# radial glow at the struck point
g = np.linspace(0, 1, 256)
for gg in g:
    ax.add_patch(plt.Circle((cx, cy), 0.08 + gg * 0.30,
                            color=(0.88, 0.70, 0.36),
                            alpha=0.012 * (1 - gg), lw=0))
ax.add_patch(plt.Circle((cx, cy), 0.045, color=(0.95, 0.85, 0.55), zorder=5))

theta = np.linspace(0, 2 * np.pi, 2000)

# perturbed rings: near the strike, the deformations live
# (radius-as-time: early = wavy, late = clean)
perturbed = [
    (0.30, 0.045, 5, 0.8, (0.76, 0.35, 0.31)),   # the sign, fluttering
    (0.48, 0.032, 4, 1.7, (0.60, 0.47, 0.24)),   # the twin, beating
    (0.68, 0.022, 6, 2.5, (0.76, 0.35, 0.31)),   # the where, smearing
    (0.88, 0.012, 3, 3.4, (0.60, 0.47, 0.24)),   # thinning out
]
for r, amp, k, ph, col in perturbed:
    rr = r + amp * np.sin(k * theta + ph)
    xs = cx + rr * np.cos(theta)
    ys = cy + rr * np.sin(theta)
    ax.plot(xs, ys, color=col, alpha=0.55, lw=1.2)

# the residue: perfect circles at the far radius — invariant under deformation
clean = [(1.10, 0.85), (1.32, 0.60), (1.52, 0.35)]
for r, alpha in clean:
    ax.add_patch(plt.Circle((cx, cy), r, fill=False,
                            color=(0.88, 0.70, 0.36), alpha=alpha, lw=1.6))

# one faint clean circle farther out still, the held ring
ax.add_patch(plt.Circle((cx, cy), 1.72, fill=False,
                        color=(0.88, 0.70, 0.36), alpha=0.18, lw=1.0))

ax.set_xlim(-1.95, 1.95)
ax.set_ylim(-1.95, 1.95)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout(pad=0)
fig.savefig("assets/residue-cover.png", dpi=150, facecolor=fig.get_facecolor())
print("saved assets/residue-cover.png")
