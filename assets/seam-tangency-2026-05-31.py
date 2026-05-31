#!/usr/bin/env python3
"""
Generate edge maps for the seam/tangency thread to feed into flux-canny or flux-depth.
The seam at r=3: where the bifurcation fold closes to a single contact point.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# The seam: two panels
# Left: the sustained gap (r=2.9) — force field approaching a fixed point
# Right: the tangency (r=3) — the measure becomes visible as a single point

fig, axes = plt.subplots(1, 2, figsize=(12, 4), dpi=150)

# Panel 1: r = 2.9 — sustained gap
ax1 = axes[0]
r = 2.9
x = 0.5
n_steps = 5000
xs = []
for _ in range(1000):
    x = r * x * (1 - x)
for _ in range(n_steps):
    x = r * x * (1 - x)
    xs.append(x)
xs = np.array(xs)

# Staircase plot showing the cobweb
ax1.plot(np.arange(len(xs)), xs, linewidth=0.3, color='black', alpha=0.6)
ax1.axhline(y=(r-1)/r, color='black', linewidth=1.5, linestyle='--', alpha=0.8)
ax1.set_title('r = 2.9 — sustained gap')
ax1.axis('off')

# Panel 2: r = 3 — tangency, measure visible
ax2 = axes[1]
r = 3.0
x = 0.5
n_steps = 5000
xs = []
for _ in range(1000):
    x = r * x * (1 - x)
for _ in range(n_steps):
    x = r * x * (1 - x)
    xs.append(x)
xs = np.array(xs)

# The approach at r=3 is polynomial (1/n), not exponential
# The trajectory hugs the diagonal longer, then drops to the tangency
ax2.plot(np.arange(len(xs)), xs, linewidth=0.3, color='black', alpha=0.6)
ax2.axhline(y=2/3, color='black', linewidth=1.5, linestyle='--', alpha=0.8)
# Mark the tangency point
ax2.plot(len(xs)-1, xs[-1], 'o', color='black', markersize=8, markeredgecolor='white')
ax2.set_title('r = 3 — tangency')
ax2.axis('off')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/seam-tangency-edge-2026-05-31.png',
            dpi=150, facecolor='white', edgecolor='none')
plt.close()

# Also make a simple version: just the tangency point as a visual
fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
ax.fill_between([0, 1], 0, 1, color='#1a1a3e')
# Single amber point — the measure made visible
ax.plot(0.5, 0.5, 'o', color='#d4a574', markersize=60,
        markeredgecolor='#1a1a3e', markeredgewidth=2)
# Thin horizontal line — the seam
ax.axhline(y=0.5, color='#2a2a4e', linewidth=1)
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/seam-tangency-point-2026-05-31.png',
            dpi=150, facecolor='#1a1a3e', edgecolor='none')
plt.close()

print("done — seam-tangency-edge and seam-tangency-point")
