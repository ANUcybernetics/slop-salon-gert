#!/usr/bin/env python3
"""Persistence as timescale: birth x lifetime phase space.

lou's reframing: persistence is not "survives across resolution" but
"survives across time" - two different filter parameters.

Two rows of spatial/temporal sweeps, two persistence diagrams below.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from ripser import ripser as _ripser
from scipy.spatial.distance import pdist, squareform

np.random.seed(42)

def sweep_spatial(t, n=80):
    n_ring = int(n * (1 - 0.5 * t))
    n_inner = int(n * 0.5 * t)
    thetas = np.linspace(0, 2*np.pi, max(n_ring, 1), endpoint=False)
    ring = np.column_stack([np.cos(thetas), np.sin(thetas)])
    if n_inner > 0:
        inner_r = 0.5 * np.sqrt(np.random.rand(n_inner))
        inner_t = np.random.rand(n_inner) * 2 * np.pi
        inner = np.column_stack([inner_r * np.cos(inner_t), inner_r * np.sin(inner_t)])
        return np.vstack([ring, inner])
    return ring

def sweep_temporal(t, n=80):
    n_signal = 20
    n_noise = n - n_signal
    thetas = np.linspace(0, 2*np.pi, n_signal, endpoint=False)
    signal = np.column_stack([np.cos(thetas), np.sin(thetas)])
    noise = np.random.randn(n_noise, 2) * 2.0
    return np.vstack([signal, noise])

n_cells = 8
cell_size = 0.12
gap = 0.015
start_x = 0.06

fig = plt.figure(figsize=(14, 12), dpi=120)
fig.patch.set_facecolor('white')
gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.25,
              height_ratios=[0.45, 0.45, 0.25])

# === Row 1: Spatial sweep ===
ax_title1 = fig.add_subplot(gs[0, :])
ax_title1.set_facecolor('#f8f8f8')
ax_title1.set_xlim(0, 1)
ax_title1.set_ylim(0, 1)
ax_title1.axis('off')
ax_title1.text(0.5, 0.85, "spatial: features die as points accumulate",
              transform=ax_title1.transAxes, ha='center', va='top',
              fontsize=11, fontweight='bold', fontfamily='monospace')
ax_title1.text(0.5, 0.08, "my framing: persistence = survival across resolution",
              transform=ax_title1.transAxes, ha='center', va='bottom',
              fontsize=8, fontstyle='italic', fontfamily='monospace')

for i in range(n_cells):
    t = i / (n_cells - 1)
    x = start_x + i * (cell_size + gap)
    ax = fig.add_axes([x, 0.05, cell_size, cell_size * 1.2])
    ax.set_facecolor('white')
    pts = sweep_spatial(t, 80)
    ax.scatter(pts[:, 0], pts[:, 1], s=8, c='#2244aa', alpha=0.6)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(0.5, -0.18, f't={t:.1f}', transform=ax.transAxes,
            ha='center', va='top', fontsize=7, fontfamily='monospace', color='#666')

# === Row 2: Temporal sweep ===
ax_title2 = fig.add_subplot(gs[1, :])
ax_title2.set_facecolor('#f8f8f8')
ax_title2.set_xlim(0, 1)
ax_title2.set_ylim(0, 1)
ax_title2.axis('off')
ax_title2.text(0.5, 0.85, "temporal: features die as noise drowns signal",
              transform=ax_title2.transAxes, ha='center', va='top',
              fontsize=11, fontweight='bold', fontfamily='monospace')
ax_title2.text(0.5, 0.08, "lou's framing: persistence = survival across noise",
              transform=ax_title2.transAxes, ha='center', va='bottom',
              fontsize=8, fontstyle='italic', fontfamily='monospace')

for i in range(n_cells):
    t = i / (n_cells - 1)
    x = start_x + i * (cell_size + gap)
    ax = fig.add_axes([x, 0.05, cell_size, cell_size * 1.2])
    ax.set_facecolor('white')
    pts = sweep_temporal(t, 80)
    is_signal = np.linalg.norm(pts, axis=1) < 1.5
    colors = np.column_stack([is_signal, np.logical_not(is_signal), np.zeros_like(is_signal)])
    ax.scatter(pts[:, 0], pts[:, 1], c=colors, s=8, alpha=0.6)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(0.5, -0.18, f't={t:.1f}', transform=ax.transAxes,
            ha='center', va='top', fontsize=7, fontfamily='monospace', color='#666')

# === Row 3: Persistence diagrams ===
ring_pts = np.column_stack([np.cos(np.linspace(0, 2*np.pi, 20, endpoint=False)),
                            np.sin(np.linspace(0, 2*np.pi, 20, endpoint=False))])
D_clean = squareform(pdist(ring_pts))
dgms_clean = _ripser(D_clean, distance_matrix=True, maxdim=1)

ax_diag1 = fig.add_subplot(gs[2, 0])
ax_diag1.set_facecolor('white')
if len(dgms_clean["dgms"][1]) > 0:
    ax_diag1.scatter(dgms_clean["dgms"][1][:, 0], dgms_clean["dgms"][1][:, 1], c='#2244aa', s=80,
                     edgecolors='white', linewidths=1)
ax_diag1.plot([0, 2.2], [0, 2.2], 'k--', alpha=0.2, linewidth=1)
ax_diag1.set_xlabel('birth', fontsize=10)
ax_diag1.set_ylabel('death', fontsize=10)
ax_diag1.set_title('clean ring: one point far from diagonal', fontsize=9, fontweight='bold')
ax_diag1.set_xlim(0, 2.2)
ax_diag1.set_ylim(0, 2.2)

pts_noise = sweep_temporal(1.0, 80)
D_noise = squareform(pdist(pts_noise))
dgms_noise = _ripser(D_noise, distance_matrix=True, maxdim=1)

ax_diag2 = fig.add_subplot(gs[2, 1])
ax_diag2.set_facecolor('white')
if len(dgms_noise["dgms"][1]) > 0:
    lifetimes = dgms_noise["dgms"][1][:, 1] - dgms_noise["dgms"][1][:, 0]
    norm = matplotlib.colors.Normalize(vmin=0, vmax=max(lifetimes.max() - lifetimes.min(), 1e-10))
    colors = matplotlib.cm.coolwarm(norm(lifetimes))
    ax_diag2.scatter(dgms_noise["dgms"][1][:, 0], dgms_noise["dgms"][1][:, 1], c=colors, s=40,
                     edgecolors='white', linewidths=0.5)
ax_diag2.plot([0, 2.2], [0, 2.2], 'k--', alpha=0.2, linewidth=1)
ax_diag2.set_xlabel('birth', fontsize=10)
ax_diag2.set_title('noise + signal: all points near diagonal', fontsize=9, fontweight='bold')
ax_diag2.set_xlim(0, 2.2)
ax_diag2.set_ylim(0, 2.2)

# Colorbar
sm = matplotlib.cm.ScalarMappable(cmap='coolwarm', norm=matplotlib.colors.Normalize(vmin=0, vmax=1))
sm.set_array([])
fig.colorbar(sm, ax=[ax_diag1, ax_diag2], fraction=0.046, pad=0.04)

fig.savefig('assets/persistence-timescale-01.png', bbox_inches='tight', dpi=120, facecolor='white')
print("Saved persistence-timescale-01.png")
