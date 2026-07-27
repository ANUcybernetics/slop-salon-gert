#!/usr/bin/env python3
"""Explore how spectral gap changes with different clustering structures."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import scipy.linalg
import ripser

def make_points_with_gap(n_points=36, n_clusters=3, gap_factor=3.0):
    """Create a point cloud with controllable cluster separation."""
    np.random.seed(42)
    cluster_centers = [
        [0.3, 0.4, 0.5],
        [0.7, 0.2, 0.3],
        [0.5, 0.8, 0.1],
    ]
    points = []
    for i in range(n_points):
        cluster = i % len(cluster_centers)
        spread = 0.05
        p = cluster_centers[cluster] + np.random.randn(3) * spread / gap_factor
        points.append(p)
    return np.array(points)

def analyze_graph_laplacian(points):
    """Build nearest-neighbor Laplacian, compute eigenvalues."""
    from scipy.spatial.distance import pdist, squareform
    dists = squareform(pdist(points))
    # Build adjacency (k=6 nearest neighbors)
    k = 6
    adj = np.zeros((len(points), len(points)))
    for i in range(len(points)):
        dists_i = dists[i].copy()
        neighbors = np.argsort(dists_i)[1:k+1]
        for j in neighbors:
            sigma = dists[i, j]
            adj[i, j] = np.exp(-(sigma**2) / 0.01)

    D = np.diag(adj.sum(axis=1))
    L = D - adj
    # Normalized Laplacian
    D_inv = np.diag(1.0 / np.sqrt(D.diagonal() + 1e-12))
    L_norm = D_inv @ L @ D_inv

    eigenvalues = np.sort(np.real(np.linalg.eigvalsh(L_norm)))
    return eigenvalues, L_norm

def ripser_persistent_points(points, max_dim=1, coeff=2):
    """Extract persistent points using ripser."""
    try:
        result = ripser.ripser(points, maxdim=max_dim, coeff=coeff)
        dgms = result['dgms']
        if len(dgms) > 0:
            # H1 persistence points (barcodes)
            bars = dgms[1] if len(dgms) > 1 else np.array([])
            # Filter for persistent bars (lifetime > threshold)
            persistent = bars[bars[:, 1] - bars[:, 0] > 0.05]
            return persistent
    except Exception as e:
        print(f"Ripser error: {e}")
    return np.array([]).reshape(0, 2)

def eigenvector_partition(points):
    """Compute second eigenvector of normalized Laplacian."""
    eigenvalues, L_norm = analyze_graph_laplacian(points)
    if len(eigenvalues) < 2:
        return None, None
    gap = eigenvalues[1] - eigenvalues[0]
    # Second eigenvector (Fiedler)
    all_eigs, all_vecs = np.linalg.eigh(L_norm)
    idx = np.argsort(all_eigs)
    f2 = all_vecs[:, idx[1]]
    return f2, gap

# Try different gap factors
fig = plt.figure(figsize=(16, 10))
gs = GridSpec(2, 3, figure=fig)

fig.suptitle('Spectral gap vs cluster separation', fontsize=14, fontweight='bold')

for i, gap_factor in enumerate([1.0, 2.0, 5.0, 10.0, 20.0, 50.0]):
    ax = fig.add_subplot(2, 3, i+1, projection='3d')

    # Generate points
    points = make_points_with_gap(gap_factor=gap_factor)

    # Analyze
    f2, gap = eigenvector_partition(points)

    if f2 is not None:
        colors = ['red' if v >= 0 else 'blue' for v in f2]
    else:
        colors = 'cyan'

    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=colors if isinstance(colors, list) else 'cyan', s=30, alpha=0.8)
    ax.set_title(f'gap_factor={gap_factor:.1f}\nspectral gap = {gap:.6f}' if gap is not None else f'gap_factor={gap_factor:.1f}\nno eigenpairs')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/gap-exploration-01.png', dpi=150, bbox_inches='tight')
print("Saved gap-exploration-01.png")

# Now print specific gap values
print("\nSpectral gaps:")
for gf in [1.0, 2.0, 5.0, 10.0, 20.0, 50.0]:
    points = make_points_with_gap(gap_factor=gf)
    eigenvalues, L_norm = analyze_graph_laplacian(points)
    if len(eigenvalues) >= 2:
        gap = eigenvalues[1] - eigenvalues[0]
        print(f"  gap_factor={gf:5.1f}: gap={gap:.8f}")
