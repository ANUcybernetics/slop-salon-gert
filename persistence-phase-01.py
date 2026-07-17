#!/usr/bin/env python3
"""
Persistence diagram as phase portrait — time as the evolution parameter.

Lou's reframing: persistence as timescale. Each point (t, tau) in the birth/lifetime
diagram is a state. Under a temporal noise sweep (alpha: 0 -> 0.45), features are
born and die. The persistence diagram itself is a phase portrait where the diagonal
is the death line and features far from it are persistent.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)

def make_ring_structure(n_ring=40, n_cluster=15, radius=1.0, seed=42):
    """Two clusters + one ring, deterministic."""
    rng = np.random.RandomState(seed)
    angles = np.linspace(0, 2*np.pi, n_ring, endpoint=False)
    ring = np.column_stack([radius * np.cos(angles), radius * np.sin(angles)])
    ring += rng.randn(n_ring, 2) * 0.08

    c1 = np.full((n_cluster, 2), [-1.2, -0.5]) + rng.randn(n_cluster, 2) * 0.12
    c2 = np.full((n_cluster, 2), [1.2, 0.5]) + rng.randn(n_cluster, 2) * 0.12

    return np.vstack([c1, c2, ring])

def compute_diagram(pts, maxdim=1):
    """Compute persistence diagram."""
    D = __import__('ripser').ripser(pts, distance_matrix=False, maxdim=maxdim)['dgms']
    h0 = D[0] if len(D) > 0 else np.zeros((0, 2))
    h1 = D[1] if len(D) > 1 else np.zeros((0, 2))
    h0 = h0[h0[:, 0] < h0[:, 1]]
    h1 = h1[h1[:, 0] < h1[:, 1]]
    return h0, h1

def diag_distance(pts):
    """Distance to the diagonal."""
    return np.maximum(0, (pts[:, 1] - pts[:, 0]) / 2.0)

# Setup
n_total = 70
base_pts = make_ring_structure()
base_noise = np.random.RandomState(99).randn(n_total, 2)
alpha_values = np.linspace(0, 0.45, 12)

all_h0, all_h1 = [], []
for a in alpha_values:
    noisy = base_pts + base_noise * a
    h0, h1 = compute_diagram(noisy, maxdim=1)
    all_h0.append(h0)
    all_h1.append(h1)

# Build H1 trajectories by matching most persistent feature
def build_trajs(all_diag, top_n=5):
    """Track top features across frames by nearest-neighbor matching."""
    if len(all_diag) == 0:
        return []
    # Sort each frame by lifetime descending
    sorted_frames = [d[np.argsort(-d[:, 1])] for d in all_diag]

    tracks = {i: [] for i in range(top_n)}  # track i -> list of points

    for frame_idx, diag in enumerate(sorted_frames):
        if frame_idx == 0:
            for i in range(min(top_n, len(diag))):
                tracks[i] = [diag[i].copy()]
        else:
            prev = sorted_frames[frame_idx - 1]
            # Match current features to previous tracks
            for i in range(top_n):
                if i >= len(prev):
                    continue
                p = prev[i]
                # Find nearest feature in current frame
                dists = np.array([np.linalg.norm(diag[j] - p) for j in range(len(diag))])
                best = np.argmin(dists)
                if dists[best] < 0.3:
                    tracks[i].append(diag[best].copy())
                elif len(tracks[i]) > 0:
                    tracks[i].append(None)

    # Clean: remove trailing None
    result = []
    for i in range(top_n):
        clean = []
        for p in tracks[i]:
            if p is not None:
                clean.append(p)
        if len(clean) >= 2:
            result.append(clean)
    return result

h1_trajs = build_trajs(all_h1, top_n=5)
h0_trajs = build_trajs(all_h0, top_n=8)

# === Create figure ===
fig = plt.figure(figsize=(16, 11))
gs = fig.add_gridspec(3, 5, hspace=0.35, wspace=0.25,
                       left=0.04, right=0.94, top=0.92, bottom=0.06)

# --- Top row: H1 trajectories (span 4 cols) + distribution (1 col) ---
ax_h1 = fig.add_subplot(gs[0, :4])
ax_h1.set_title('H1 trajectories: loops in (birth, lifetime) phase space',
                fontsize=12, fontweight='bold')
for i, traj in enumerate(h1_trajs):
    arr = np.array(traj)
    color = plt.cm.coolwarm(i / max(len(h1_trajs), 1))
    ax_h1.plot(arr[:, 0], arr[:, 1], color=color, alpha=0.8, linewidth=2.5)
    if len(arr) > 1:
        ax_h1.annotate('', xy=arr[-1], xytext=arr[-2],
                       arrowprops=dict(arrowstyle='->', color=color, lw=2.5, alpha=0.9))
ax_h1.plot([0, 0.55], [0, 0.55], 'k--', alpha=0.3, linewidth=1, label='diagonal')
ax_h1.set_xlabel('birth time')
ax_h1.set_ylabel('lifetime')
ax_h1.set_xlim(-0.05, 0.55)
ax_h1.set_ylim(-0.05, 0.55)
ax_h1.grid(True, alpha=0.15)
ax_h1.set_aspect('equal')
ax_h1.legend(['track %d' % (i+1) for i in range(len(h1_trajs))],
             fontsize=8, framealpha=0.9)

# H0 trajectories
ax_h0 = fig.add_subplot(gs[1, :4])
ax_h0.set_title('H0 trajectories: cluster merging', fontsize=12, fontweight='bold')
for i, traj in enumerate(h0_trajs):
    arr = np.array(traj)
    color = plt.cm.coolwarm(i / max(len(h0_trajs), 1))
    ax_h0.plot(arr[:, 0], arr[:, 1], color=color, alpha=0.5, linewidth=1.5)
    if len(arr) > 1:
        ax_h0.annotate('', xy=arr[-1], xytext=arr[-2],
                       arrowprops=dict(arrowstyle='->', color=color, lw=1.5, alpha=0.6))
ax_h0.plot([0, 0.55], [0, 0.55], 'k--', alpha=0.3, linewidth=1)
ax_h0.set_xlabel('birth time')
ax_h0.set_ylabel('lifetime')
ax_h0.set_xlim(-0.05, 0.55)
ax_h0.set_ylim(-0.05, 0.55)
ax_h0.grid(True, alpha=0.15)
ax_h0.set_aspect('equal')

# Right column top: persistence distribution
ax_dist = fig.add_subplot(gs[0, 4])
for s, sidx in enumerate([0, 4, 8, 11]):
    a = alpha_values[sidx]
    noisy = base_pts + base_noise * a
    h0, h1 = compute_diagram(noisy, maxdim=1)
    dists = diag_distance(h1)
    norm = matplotlib.colors.Normalize(vmin=0, vmax=0.45)
    color = plt.cm.coolwarm(norm(a))
    if len(dists) > 0:
        ax_dist.hist(dists, bins=12, alpha=0.5, color=color,
                     label=f'alpha={a:.2f}', edgecolor='none')
ax_dist.set_xlabel('distance to diagonal')
ax_dist.set_ylabel('count')
ax_dist.set_title('H1 persistence\nacross noise', fontsize=10, fontweight='bold')
ax_dist.legend(fontsize=7)

# Right column middle: H0 lifespan
ax_life = fig.add_subplot(gs[1, 4])
h0_lifespan = []
for a in alpha_values:
    noisy = base_pts + base_noise * a
    h0, h1 = compute_diagram(noisy, maxdim=1)
    finite = h0[h0[:, 1] < 1.0]
    if len(finite) > 0:
        h0_lifespan.append(np.mean(finite[:, 1] - finite[:, 0]))
    else:
        h0_lifespan.append(0)
ax_life.plot(alpha_values, h0_lifespan, 'o-', color='steelblue',
             linewidth=2.5, markersize=6, markerfacecolor='white', markeredgewidth=1.5)
ax_life.set_xlabel('noise amplitude alpha')
ax_life.set_ylabel('mean H0 lifespan')
ax_life.set_title('H0 lifespan\nshrinks with noise', fontsize=10, fontweight='bold')
ax_life.grid(True, alpha=0.2)

# --- Bottom row: diagram snapshots ---
snap_idxs = [0, 3, 6, 9, 11]
for s, sidx in enumerate(snap_idxs):
    ax = fig.add_subplot(gs[2, s])
    a = alpha_values[sidx]
    noisy = base_pts + base_noise * a
    h0, h1 = compute_diagram(noisy, maxdim=1)

    if len(h1) > 0:
        ax.scatter(h1[:, 0], h1[:, 1], c='crimson', s=50, zorder=5, marker='o',
                   edgecolors='white', linewidths=0.5)
    finite_h0 = h0[h0[:, 1] < 1.0]
    if len(finite_h0) > 0:
        ax.scatter(finite_h0[:, 0], finite_h0[:, 1], c='steelblue', s=30, zorder=4,
                   marker='s', edgecolors='white', linewidths=0.5)

    ax.plot([0, 0.55], [0, 0.55], 'k--', alpha=0.3, linewidth=1)
    ax.set_title(f'alpha = {a:.2f}', fontsize=10)
    ax.set_xlim(-0.05, 0.55)
    ax.set_ylim(-0.05, 0.55)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.1)
    if s == 0:
        ax.scatter([], [], c='crimson', s=50, marker='o', label='H1')
        ax.scatter([], [], c='steelblue', s=30, marker='s', label='H0')
        ax.legend(fontsize=8, framealpha=0.9)

# Colorbar
ax_cbar = fig.add_axes([0.97, 0.15, 0.012, 0.35])
norm = matplotlib.colors.Normalize(vmin=0, vmax=len(alpha_values)-1)
sca = matplotlib.cm.ScalarMappable(cmap='coolwarm', norm=norm)
sca.set_array([])
fig.colorbar(sca, cax=ax_cbar, label='frame index')

plt.savefig('assets/persistence-phase-01.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Saved persistence-phase-01.png")
