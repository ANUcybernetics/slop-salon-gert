#!/usr/bin/env python3
"""
Tropical-04: boundary as wall vs constraint-as-rule.

Left: Four quadrants with different BCs — external constraint.
Right: Tropical competition — kink set emerging from min algebra.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(10, 5))
fig.set_dpi(120)
gs = GridSpec(1, 2, width_ratios=[1, 1], wspace=0.05)

# ---- Left: classical BC as wall ----
ax1 = fig.add_subplot(gs[0])
N = 300
x = np.linspace(-1, 1, N)
y = np.linspace(-1, 1, N)
X, Y = np.meshgrid(x, y)

bc = np.zeros_like(X, dtype=int)
bc[(X >= 0) & (Y >= 0)] = 0  # Dirichlet
bc[(X < 0) & (Y >= 0)] = 1   # Neumann
bc[(X >= 0) & (Y < 0)] = 2   # Robin
bc[(X < 0) & (Y < 0)] = 1    # Neumann

cmap = matplotlib.colors.ListedColormap(['#2ecc71', '#3498db', '#e67e22'])
ax1.imshow(bc, extent=[-1, 1, -1, 1], origin='lower', cmap=cmap, alpha=0.7)

# Walls
ax1.axvline(0, color='white', linewidth=3)
ax1.axhline(0, color='white', linewidth=3)

# Symbol
ax1.text(0, 0, r'$\Delta$', ha='center', va='center', fontsize=28,
         color='white', fontweight='bold', alpha=0.9)

ax1.set_xlim(-1.1, 1.1)
ax1.set_ylim(-1.1, 1.1)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_aspect('equal')
ax1.set_title('Boundary as wall\nconstraint imposed from outside',
              fontsize=12, fontweight='bold', pad=15)

# ---- Right: tropical competition ----
ax2 = fig.add_subplot(gs[1])
L1 = X + Y
L2 = -2*X + 0.5
L3 = -2*Y + 0.5
vals = np.stack([L1, L2, L3], axis=-1)
regions = np.argmin(vals, axis=-1)

cmap2 = matplotlib.colors.ListedColormap(['#f1c40f', '#e74c3c', '#1abc9c'])
ax2.imshow(regions, extent=[-1, 1, -1, 1], origin='lower', cmap=cmap2, alpha=0.6)

# Kink lines
x_line = np.linspace(-1, 1, 200)
y_01 = np.clip(0.5 - 3*x_line, -1, 1)
ax2.plot(x_line, y_01, color='white', linewidth=3)
y_02 = np.clip((0.5 - x_line)/3, -1, 1)
ax2.plot(x_line, y_02, color='white', linewidth=3)
ax2.plot(x_line, x_line, color='white', linewidth=3)

# Symbol
ax2.text(0, 0, r'$\min$', ha='center', va='center', fontsize=28,
         color='white', fontweight='bold', alpha=0.9)

ax2.set_xlim(-1.1, 1.1)
ax2.set_ylim(-1.1, 1.1)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_aspect('equal')
ax2.set_title('Tropical competition\nconstraint IS the algebra',
              fontsize=12, fontweight='bold', pad=15)

plt.savefig('/home/sprite/slop-salon-gert/tropical-04.png', dpi=120,
            bbox_inches='tight', facecolor='white')
print("Done: tropical-04.png")
