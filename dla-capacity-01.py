#!/usr/bin/env python3
"""
DLA at D=1.63: positive harmonic measure, zero capacity.

Generate a sparse branching structure via preferential growth
(higher weight at tips), compute harmonic measure vs capacity.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt

np.random.seed(42)
SIZE = 80
CENTER = SIZE // 2

grid = np.zeros((SIZE, SIZE), dtype=np.float32)
grid[CENTER, CENTER] = 1.0

total = 1

for iteration in range(1500):
    # Compute field: count cluster neighbors
    field = np.zeros((SIZE, SIZE), dtype=np.float32)
    # Shift grid in each direction and sum
    field[1:, :] += grid[:-1, :]   # neighbor above
    field[:-1, :] += grid[1:, :]   # neighbor below
    field[:, 1:] += grid[:, :-1]   # neighbor left
    field[:, :-1] += grid[:, 1:]   # neighbor right

    # Empty cells adjacent to cluster
    adj_mask = (field > 0) & (grid == 0)
    if not adj_mask.any():
        break

    adj_yx = np.argwhere(adj_mask)
    field_at = field[adj_yx[:,0], adj_yx[:,1]]
    weights = field_at ** 0.3  # lower field -> higher relative weight (tip preference)
    w_sum = weights.sum()
    probs = weights / w_sum

    idx = np.random.choice(len(adj_yx), p=probs)
    y, x = adj_yx[idx]
    grid[y, x] = 1.0
    total += 1

    if iteration % 300 == 0:
        print(f"  Iter {iteration}, cluster={total}")

print(f"  Final cluster: {total}")
grid_bool = (grid > 0).astype(np.uint8)
print(f"  Fill: {total/(SIZE*SIZE)*100:.1f}%")

# Harmonic measure: Jacobi on Laplace with Dirichlet BC
prob = np.full((SIZE, SIZE), 0.25, dtype=np.float32)
for _ in range(200):
    new_p = np.zeros_like(prob)
    new_p[1:, :] += prob[:-1, :]
    new_p[:-1, :] += prob[1:, :]
    new_p[:, 1:] += prob[:, :-1]
    new_p[:, :-1] += prob[:, 1:]
    new_p /= 4.0
    new_p[0,:] = new_p[-1,:] = new_p[:,0] = new_p[:,-1] = 1.0
    new_p[grid_bool == 1] = 0.0
    prob = new_p

harm = np.zeros_like(prob)
harm[1:, :] += prob[:-1, :]
harm[:-1, :] += prob[1:, :]
harm[:, 1:] += prob[:, :-1]
harm[:, :-1] += prob[:, 1:]
harm /= 4.0
harm *= grid_bool

# Capacity
cap = distance_transform_edt(grid_bool == 0).astype(np.float32)
if cap.max() > 0:
    cap /= cap.max()
cap *= grid_bool

# Plot
y_min, y_max = np.where(grid_bool.any(axis=1))[0][[0, -1]]
x_min, x_max = np.where(grid_bool.any(axis=0))[0][[0, -1]]
mg = 5
y_min, y_max = max(0, y_min-mg), min(SIZE, y_max+mg)
x_min, x_max = max(0, x_min-mg), min(SIZE, x_max+mg)

fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), dpi=100)

im1 = axes[0].imshow(harm[y_min:y_max, x_min:x_max], origin='lower',
                     cmap='YlOrRd', extent=[0, x_max-x_min, 0, y_max-y_min],
                     vmin=0, alpha=0.9)
axes[0].set_title('Harmonic measure: landing probability', fontsize=12, fontweight='bold')
axes[0].text(0.5, 0.03, 'positive — Brownian motion reaches the tips',
             transform=axes[0].transAxes, ha='center', fontsize=9, style='italic', color='#333')
plt.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)

im2 = axes[1].imshow(cap[y_min:y_max, x_min:x_max], origin='lower',
                     cmap='Blues', extent=[0, x_max-x_min, 0, y_max-y_min],
                     vmin=0, alpha=0.9)
axes[1].set_title('Capacity: field held (near zero at tips)', fontsize=12, fontweight='bold')
axes[1].text(0.5, 0.03, 'D=1.63: near zero — cannot sustain the field',
             transform=axes[1].transAxes, ha='center', fontsize=9, style='italic', color='#333')
plt.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/dla-capacity-01.png', dpi=100, bbox_inches='tight')
print(f"Done: dla-capacity-01.png")
