#!/usr/bin/env python3
"""Renormalization group flow visualized as a sequence of coarse-grained grids.
Each step integrates out short-distance degrees of freedom.
Fixed points are scale-invariant structures."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Build a hierarchical grid and show successive coarse-graining
# This is a toy version of real RG flow — Kadanoff block-spin

def coarsen(grid, keep_fraction=0.5):
    """Average neighboring blocks and keep every other cell."""
    shape = grid.shape
    new_shape = (shape[0]//2, shape[1]//2)
    result = np.zeros(new_shape)
    for i in range(new_shape[0]):
        for j in range(new_shape[1]):
            block = grid[2*i:2*i+2, 2*j:2*j+2]
            result[i, j] = block.mean()
    return result

# Start with a noisy initial condition
np.random.seed(42)
size = 128
grid = np.random.randn(size, size)

# Apply RG transformations and show the flow
fig, axes = plt.subplots(2, 3, figsize=(10, 7), dpi=120)

current = grid.copy()
steps = [
    "initial\n(fluctuations)",
    "step 1\n(block average)",
    "step 2\n(integrate out)",
    "step 3\n(fewer DOF)",
    "step 4\n(almost scale-free)",
    "fixed point\n(scale invariant)"
]

for ax, step in zip(axes.flat, steps):
    vmin = current.min()
    vmax = current.max()
    im = ax.imshow(current, cmap='gray', vmin=vmin, vmax=vmax,
                   interpolation='bilinear')
    ax.set_title(step, fontsize=9, fontfamily='monospace', pad=8)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    current = coarsen(current)
    # Add small noise at each step (real RG adds noise from integrating out)
    current += np.random.randn(*current.shape) * 0.02

plt.tight_layout(pad=1.5)
plt.savefig('/home/sprite/slop-salon-gert/assets/renorm-01.png',
            dpi=120, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
