#!/usr/bin/env python3
"""seam-end-on — the seam seen end-on is a point.

The comma register's residue: the drone is the seam. A field of dashed
approaches — each a count climbing, winding, never landing — stops at the
boundary of a solid dot. The approaches end AT the dot's edge: the seam is the
dot's circumference, the drone is the dot. One object, two ears. Between the
rays, where the miss is loudest, a faint mid-gap stroke.

Code-made still. No model. matplotlib.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 8), dpi=200)
fig.patch.set_facecolor("#05060a")
ax.set_facecolor("#05060a")

n_rays = 72
theta = np.linspace(0, 2 * np.pi, n_rays, endpoint=False)

# ---- the approaches: dashed rays, stopping at the dot's horizon ----
r = np.linspace(1.0, 2.15, 80)
dashes = (2.4, 2.6)
for i, th in enumerate(theta):
    ang = th + 0.05 * np.sin(3 * th + 0.7) * (r - 1.0)  # gentle wind
    x = r * np.cos(ang)
    y = r * np.sin(ang)
    if i % 2 == 0:
        ax.plot(x, y, color="#d8b84a", lw=1.0, alpha=0.6, dashes=dashes,
                solid_capstyle="round")
    else:
        ax.plot(x, y, color="#c9a83e", lw=0.55, alpha=0.34, dashes=dashes,
                solid_capstyle="round")

# ---- the between: faint mid-gap strokes, loudest at the annulus middle ----
mid = (theta[:-1] + theta[1:]) / 2
gap = np.linspace(-0.5, 0.5, 3) * (2 * np.pi / n_rays) * 0.5
for th in mid:
    for g, a in zip(gap, (0.20, 0.30, 0.20)):
        ang = th + g
        x0, y0 = 1.30 * np.cos(ang), 1.30 * np.sin(ang)
        x1, y1 = 1.42 * np.cos(ang), 1.42 * np.sin(ang)
        ax.plot([x0, x1], [y0, y1], color="#8a7a3a", lw=1.6, alpha=a,
                solid_capstyle="round")
        x0, y0 = 1.68 * np.cos(ang), 1.68 * np.sin(ang)
        x1, y1 = 1.80 * np.cos(ang), 1.80 * np.sin(ang)
        ax.plot([x0, x1], [y0, y1], color="#8a7a3a", lw=1.6, alpha=a * 0.8,
                solid_capstyle="round")

# ---- the drone: the solid dot ----
dot = plt.Circle((0, 0), 0.42, color="#f2e3b0", zorder=5)
ax.add_artist(dot)
core = plt.Circle((0, 0), 0.20, color="#f7eecf", zorder=6)
ax.add_artist(core)

# ---- the seam: the dot's horizon, where every approach ends ----
seam = plt.Circle((0, 0), 1.0, color="none", edgecolor="#d8b84a",
                  lw=0.7, linestyle=(0, (1, 3)), alpha=0.45, zorder=3)
ax.add_artist(seam)

ax.set_xlim(-2.45, 2.45)
ax.set_ylim(-2.45, 2.45)
ax.set_aspect("equal")
ax.axis("off")
plt.tight_layout(pad=0)
plt.savefig("assets/seam-end-on.png", facecolor=fig.get_facecolor(), bbox_inches="tight")
print("wrote assets/seam-end-on.png")
