"""
Lorenz attractor: structurally unoccupiable.

Two layers:
1. The attractor itself — dim, grey-white, the limit set traced by a very long trajectory
2. A short trajectory segment — bright, colored — showing the orbit near but never on it

The gap between the two is the point: the structure is real, the dynamics forbid landing.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# Lorenz parameters
sigma, rho, beta = 10.0, 28.0, 8/3

def lorenz_step(x, y, z, dt=0.001):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return x + dx*dt, y + dy*dt, z + dz*dt

def integrate(x0, y0, z0, n_steps, dt=0.001):
    xs, ys, zs = [x0], [y0], [z0]
    x, y, z = x0, y0, z0
    for _ in range(n_steps):
        x, y, z = lorenz_step(x, y, z, dt)
        xs.append(x); ys.append(y); zs.append(z)
    return np.array(xs), np.array(ys), np.array(zs)

# Long trajectory for the attractor structure (ghosted)
xa, ya, za = integrate(0.1, 0.0, 0.0, 200_000)

# Short trajectory segment showing the orbit (bright)
# Start slightly off the attractor
xo, yo, zo = integrate(1.0, 1.0, 1.0, 20_000)
# Use the latter portion (after transient)
skip = 5000
xo, yo, zo = xo[skip:], yo[skip:], zo[skip:]

fig, ax = plt.subplots(figsize=(10, 8), facecolor='black')
ax.set_facecolor('black')

# Draw the attractor structure — faint, ghosted
ax.plot(xa[::4], za[::4], color='#1a1a2e', linewidth=0.2, alpha=0.15, rasterized=True)
ax.plot(xa[::2], za[::2], color='#2d2d4e', linewidth=0.3, alpha=0.25, rasterized=True)
ax.plot(xa, za, color='#3a3a5c', linewidth=0.4, alpha=0.4, rasterized=True)

# Draw the orbit — bright segment, colored by time
n = len(xo)
# Color: orbit colored by progression through time, copper/amber tones
points = np.array([xo, zo]).T.reshape(-1, 1, 2)
segs = np.concatenate([points[:-1], points[1:]], axis=1)
t = np.linspace(0, 1, len(segs))
# Map time to color: deep amber → bright white-gold
colors = plt.cm.YlOrBr(0.3 + 0.7 * t)
lc = mc.LineCollection(segs, colors=colors, linewidth=0.8, alpha=0.9, rasterized=True)
ax.add_collection(lc)

# Mark a specific moment on the orbit — a single point, showing "here, now, not on the structure"
mid = len(xo) // 2
ax.scatter([xo[mid]], [zo[mid]], color='white', s=12, zorder=10, alpha=0.9)

ax.set_xlim(xa.min() - 2, xa.max() + 2)
ax.set_ylim(za.min() - 2, za.max() + 2)
ax.axis('off')

# Minimal label
ax.text(0.02, 0.02,
    "the attractor exists — fractal dimension, measure\nno trajectory is ever on it",
    transform=ax.transAxes,
    color='#888888', fontsize=8, fontfamily='monospace',
    va='bottom')

plt.tight_layout(pad=0.5)
outpath = "./assets/lorenz-unoccupiable-2026-05-20.png"
plt.savefig(outpath, dpi=180, bbox_inches='tight', facecolor='black')
print(f"saved: {outpath}")
plt.close()
