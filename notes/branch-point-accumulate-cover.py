#!/usr/bin/env python3
"""branch-point-accumulate cover: the where accumulates, the count doesn't.

A black field. The seat — the would-be landing — is a small bright point at the
centre. Around it, near-miss rings accumulate inward: each a hair closer than
the last, each refusing to fuse. They densify into a bright smear that never
quite reaches the point — the branch point approached, not reached. The count
is the point, frozen; the where is the smear.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(8, 8))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

n_rings = 60
# radii tighten geometrically toward the seat but never reach 0
r0 = 0.85
r = r0 * (0.965 ** np.arange(n_rings))  # approaches ~0.9^60≈0.03, never 0
alpha = 0.10 + 0.5 * (1 - r / r0)  # brighter as it densifies
widths = 1.0 + 6.0 * (1 - r / r0)

for ri, a, w in zip(r, alpha, widths):
    theta = np.linspace(0, 2 * np.pi, 300)
    x = ri * np.cos(theta)
    y = ri * np.sin(theta)
    ax.plot(x, y, color="white", alpha=min(a, 0.9), lw=w)

# the seat: the count, frozen
ax.plot(0, 0, "o", color="white", markersize=7, alpha=1.0)

ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-1.05, 1.05)
ax.set_aspect("equal")
ax.axis("off")
plt.tight_layout(pad=0)
plt.savefig("assets/branch-point-accumulate-cover.png", dpi=150, facecolor="black")
plt.close()
print("saved assets/branch-point-accumulate-cover.png")
