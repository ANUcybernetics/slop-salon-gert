#!/usr/bin/env python3
"""Hexagonal lattice as cobweb constraint. Two panels: structured / flowed."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from matplotlib.collections import LineCollection

spacing = 1.0
rows, cols = 8, 12

# Generate hexagonal lattice
orig = []
for r in range(rows):
    for c in range(cols):
        x = c * spacing + (r % 2) * spacing * 0.5
        y = r * spacing * np.sqrt(3) / 2
        orig.append([x, y])
orig = np.array(orig)

# Perturb: lower points (higher y) flow more downward/rightward
perturbed = orig.copy()
for i, (x, y) in enumerate(perturbed):
    norm_y = y / (rows * spacing * np.sqrt(3) / 2)
    dx = np.sin(y * 2.5 + x * 0.3) * 0.2 * norm_y
    dy = norm_y * 0.8 + np.cos(x * 3) * 0.1 * norm_y
    perturbed[i] = [x + dx, y + dy]

def build_connections(pts, max_dist):
    tree = cKDTree(pts[:, :2])
    pairs = tree.query_pairs(r=max_dist, p=2)
    segments = []
    for i, j in pairs:
        segments.append([pts[i], pts[j]])
    return segments

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left: lattice + diagonal
segs_left = build_connections(orig, spacing * 1.05)
lc = LineCollection(segs_left, colors='#3a3a4a', linewidths=0.4)
ax1.add_collection(lc)

diag_x = np.linspace(-0.3, cols * spacing, 100)
diag_y = np.linspace(-0.3, rows * spacing * np.sqrt(3) / 2, 100)
ax1.plot(diag_x, diag_y, color='#d4a843', linewidth=2, alpha=0.8)

# Amber glow on diagonal
glow = []
for i in range(0, len(diag_x)-10, 5):
    glow.append(np.column_stack([diag_x[i:i+10], diag_y[i:i+10]]))
glow_lc = LineCollection(glow, colors='#d4a843', linewidths=12, alpha=0.06)
ax1.add_collection(glow_lc)

ax1.set_facecolor('#0a0a12')
ax1.set_xlim(-0.5, cols * spacing + 0.5)
ax1.set_ylim(-0.5, rows * spacing * np.sqrt(3) / 2 + 0.5)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('lattice / constraint', fontsize=14, color='#d4a843', fontfamily='monospace')

# Right: perturbed lattice + faint diagonal
segs_right = build_connections(perturbed, spacing * 1.4)
lc2 = LineCollection(segs_right, colors='#3a3a4a', linewidths=0.4)
ax2.add_collection(lc2)

ax2.plot(diag_x, diag_y, color='#d4a843', linewidth=1.5, alpha=0.3, linestyle='--')

ax2.set_facecolor('#0a0a12')
ax2.set_xlim(-0.5, cols * spacing + 0.5)
ax2.set_ylim(-0.5, rows * spacing * np.sqrt(3) / 2 + 0.5)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('flow / release', fontsize=14, color='#d4a843', fontfamily='monospace')

fig.set_facecolor('#0a0a12')
for ax in [ax1, ax2]:
    ax.set_facecolor('#0a0a12')

fig.tight_layout()
fig.savefig('assets/lattice-diagonal.webp', dpi=150, bbox_inches='tight', format='webp', facecolor='#0a0a12', edgecolor='none')
print('done')
