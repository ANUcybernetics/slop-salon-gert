#!/usr/bin/env python3
"""Persistent spectral theory: eigenvalue trajectories across a filtration.

The graph Laplacian's zero-eigenvalue multiplicity equals the number of connected
components. As the VR filtration grows, eigenvalue trajectories carry information
about how topology forms — eigenvalues approaching zero signal imminent merges.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.spatial.distance import cdist
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import laplacian, connected_components as cc
from scipy.sparse.linalg import eigsh

np.random.seed(42)


def dlakm(n=120):
    """DLA-like point cloud with branches and voids."""
    points = [[0.0, 0.0]]
    angles = np.array([0, 60, 120, 180, 240, 300]) * np.pi / 180
    for b in angles:
        x, y = 0.0, 0.0
        for _ in range(15 + np.random.randint(0, 10)):
            x += np.cos(b) * 1.5 + np.random.uniform(-0.5, 0.5)
            y += np.sin(b) * 1.5 + np.random.uniform(-0.5, 0.5)
            points.append([x, y])
            if np.random.random() < 0.3:
                sa = b + np.pi/2 * np.random.choice([-1, 1])
                sx, sy = x, y
                for _ in range(np.random.randint(2, 5)):
                    sx += np.cos(sa) * np.random.uniform(0.5, 1.0)
                    sy += np.sin(sa) * np.random.uniform(0.5, 1.0)
                    points.append([sx, sy])
    for _ in range(15):
        a, r = np.random.uniform(0, 2*np.pi), np.random.uniform(5, 12)
        points.append([r*np.cos(a), r*np.sin(a)])
    return np.array(points[:n])


# --- Generate ---
coords = dlakm(120)
n = len(coords)
print(f"points: {n}")

D = cdist(coords, coords, 'euclidean')
max_r = D.max()
print(f"max dist: {max_r:.2f}")

N = 250
r_vals = np.linspace(0.005 * max_r, 0.88 * max_r, N)
ne = 6

traj = np.zeros((N, ne))
comp_count = np.zeros(N, dtype=int)

print("sweeping...")
for i, r in enumerate(r_vals):
    if i % 40 == 0:
        print(f"  {i}/{N}")

    adj = (D < r).astype(float)
    np.fill_diagonal(adj, 0)
    L = laplacian(csr_matrix(adj))

    try:
        k = min(ne + 1, n - 1)
        eigs = eigsh(L, k=k, which='SM', sigma=0.01,
                    return_eigenvectors=False, maxiter=200)
        traj[i] = np.sort(eigs)[:ne]
    except Exception:
        if i > 0:
            traj[i] = traj[i-1]

    # Connected components
    nc, _ = cc(csr_matrix(adj), directed=False)
    comp_count[i] = nc


def smooth(arr, w=7):
    return np.convolve(arr, np.ones(w)/w, mode='same')

# --- Plot: 2-panel ---
fig = plt.figure(figsize=(14, 6))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.5, 1])

ax1 = fig.add_subplot(gs[0])
cmap = plt.cm.viridis(np.linspace(0, 0.9, ne))
for j in range(ne):
    y = smooth(traj[:, j], w=7)
    ax1.plot(r_vals, y, color=cmap[j], linewidth=1.5, alpha=0.8,
             label=f'$\\lambda_{{{j+1}}}$' if j < 4 else None)
ax1.axhline(y=0, color='grey', linestyle='--', linewidth=0.8, alpha=0.5)
ax1.set_xlabel('filtration radius $r$')
ax1.set_ylabel('eigenvalue')
ax1.set_title('eigenvalue trajectories across the VR filtration', fontsize=12)
ax1.set_ylim(bottom=-1)
ax1.legend(fontsize=8, ncol=2)

ax2 = fig.add_subplot(gs[1])
ax2.plot(r_vals, smooth(comp_count, w=10), 'b-', linewidth=1.8,
         label='# components')
gap = np.array([max(traj[i, 1], 0) for i in range(N)])
ax2.plot(r_vals, smooth(gap, w=10), 'r-', linewidth=1.8,
         label='$\\lambda_2(r)$')
ax2.axhline(y=0, color='grey', linestyle='--', linewidth=0.5, alpha=0.3)
ax2.set_xlabel('filtration radius $r$')
ax2.set_title('components + spectral gap', fontsize=12)
ax2.legend(fontsize=9)

fig.tight_layout()
out = '/home/sprite/slop-salon-gert/notes/persistent-spectral-01.png'
fig.savefig(out, dpi=150)
print(f'saved persistent-spectral-01.png')
print(f"Start: {comp_count[0]} components, End: {comp_count[-1]} components")
