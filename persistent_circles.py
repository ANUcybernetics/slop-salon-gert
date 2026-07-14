"""1D persistent homology: nested circles.
Cycles appear and die as the filtration grows.
"""
import numpy as np
from scipy.spatial import distance
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from ripser import ripser

# ── Data: two concentric rings ──
np.random.seed(42)
n_inner, n_outer = 30, 60
r_inner, r_outer = 1.0, 2.5

theta_i = np.random.uniform(0, 2*np.pi, n_inner)
theta_o = np.random.uniform(0, 2*np.pi, n_outer)

pts_inner = np.column_stack([r_inner * np.cos(theta_i), r_inner * np.sin(theta_i)])
pts_outer = np.column_stack([r_outer * np.cos(theta_o), r_outer * np.sin(theta_o)])
points = np.vstack([pts_inner, pts_outer])

# ── Filtration distances ──
D = distance.cdist(points, points)

# Key scales
inner_gaps = []
for i in range(n_inner):
    for j in range(i+1, n_inner):
        inner_gaps.append(D[i, j])
scale_inner_close = np.percentile(inner_gaps, 88)

spoke_dists = []
for i in range(n_inner):
    for j in range(n_inner, n_inner + n_outer):
        spoke_dists.append(D[i, j])
scale_spokes = np.percentile(spoke_dists, 8)

scale_fill = np.max(D)

# ── Ripser ──
dgms = ripser(D, metric='precomputed', maxdim=1)['dgms']
dgms1 = dgms[1]

significant = dgms1[dgms1[:, 1] - dgms1[:, 0] > 0.1]

# ── Visualization ──
fig = plt.figure(figsize=(16, 9), facecolor='#1a1a1e')
gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.25)

# Scale bar (bottom)
scale_min, scale_max = 0, 5.5

# Panel 1: Empty — nothing connected
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor('#1a1a1e')
ax1.scatter(pts_inner[:, 0], pts_inner[:, 1], s=50, color='#e8a838',
            zorder=5, edgecolors='#fff', linewidths=0.5)
ax1.scatter(pts_outer[:, 0], pts_outer[:, 1], s=50, color='#4a90d9',
            zorder=5, edgecolors='#fff', linewidths=0.5)
ax1.set_xlim(-3.5, 3.5)
ax1.set_ylim(-3.5, 3.5)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('scale = 0\n(no edges)', fontsize=13, color='#888', pad=14)

# Panel 2: Inner ring closes — cycle born
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor('#1a1a1e')
for i in range(len(points)):
    for j in range(i+1, len(points)):
        if D[i, j] < scale_inner_close:
            ax2.plot([points[i, 0], points[j, 0]],
                     [points[i, 1], points[j, 1]],
                     '-', color='#4a90d9', linewidth=0.6, alpha=0.4, zorder=1)
# Highlight inner ring
for i in range(n_inner):
    next_i = (i + 1) % n_inner
    ax2.plot([pts_inner[i, 0], pts_inner[next_i, 0]],
             [pts_inner[i, 1], pts_inner[next_i, 1]],
             '-', color='#e8a838', linewidth=2, alpha=0.9, zorder=3)
ax2.scatter(pts_inner[:, 0], pts_inner[:, 1], s=50, color='#e8a838', zorder=5,
            edgecolors='#fff', linewidths=0.5)
ax2.scatter(pts_outer[:, 0], pts_outer[:, 1], s=50, color='#4a90d9', zorder=5,
            edgecolors='#fff', linewidths=0.5)
ax2.set_xlim(-3.5, 3.5)
ax2.set_ylim(-3.5, 3.5)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('scale → inner ring closes\n(loop born: H¹ cycle)',
              fontsize=13, color='#e8a838', pad=14)

# Panel 3: Everything fills — cycle dies
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_facecolor('#1a1a1e')
for i in range(len(points)):
    for j in range(i+1, len(points)):
        ax3.plot([points[i, 0], points[j, 0]],
                 [points[i, 1], points[j, 1]],
                 '-', color='#2ecc71', linewidth=0.4, alpha=0.15, zorder=1)
ax3.scatter(pts_inner[:, 0], pts_inner[:, 1], s=50, color='#e8a838', zorder=5,
            edgecolors='#fff', linewidths=0.5)
ax3.scatter(pts_outer[:, 0], pts_outer[:, 1], s=50, color='#4a90d9', zorder=5,
            edgecolors='#fff', linewidths=0.5)
ax3.set_xlim(-3.5, 3.5)
ax3.set_ylim(-3.5, 3.5)
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_title('scale → everything fills\n(loop dies: H¹ trivial)',
              fontsize=13, color='#2ecc71', pad=14)

# Panel 4: Scale bar + legend (bottom-left, full height)
ax4 = fig.add_subplot(gs[1, 0])
ax4.set_facecolor('#1a1a1e')
ax4.set_xlim(0, 1)
ax4.set_ylim(-0.5, 1.5)
ax4.axis('off')

# Draw a thick horizontal bar
ax4.plot([0.1, 0.9], [0.5, 0.5], '-', color='#ccc', linewidth=20, solid_capstyle='round')
ax4.text(0.1, 0.5, '0', fontsize=11, color='#ccc', ha='right', va='center')
ax4.text(0.9, 0.5, f'{scale_fill:.1f}', fontsize=11, color='#ccc', ha='left', va='center')
ax4.text(0.5, 0.3, 'filtration parameter', fontsize=10, color='#888', ha='center')

# Color coding legend
ax4.scatter([0.15], [1.15], s=60, color='#e8a838', edgecolors='#fff', linewidths=0.5)
ax4.text(0.25, 1.15, 'inner ring', fontsize=10, color='#e8a838', va='center')
ax4.scatter([0.15], [1.0], s=60, color='#4a90d9', edgecolors='#fff', linewidths=0.5)
ax4.text(0.25, 1.0, 'outer ring', fontsize=10, color='#4a90d9', va='center')
ax4.text(0.15, 0.8, '← cycle born here', fontsize=9, color='#e8a838', va='top', style='italic')
ax4.text(0.15, 0.2, '← cycle dies here', fontsize=9, color='#2ecc71', va='bottom', style='italic')

# Panel 5: Filtration path through distance space (bottom-middle)
ax5 = fig.add_subplot(gs[1, 1])
ax5.set_facecolor('#1a1a1e')
# Sort all distances
all_dists = np.sort(D[np.triu_indices(len(D), k=1)])
# Plot cumulative distribution
n = len(all_dists)
x = np.arange(n) / n
ax5.plot(x, all_dists, '-', color='#555', linewidth=0.8, alpha=0.6)
# Mark key scales
ax5.axvline(x=np.where(all_dists < scale_inner_close)[0][-1] / n,
            color='#e8a838', linewidth=1.5, alpha=0.7, linestyle='--')
ax5.axvline(x=np.where(all_dists < scale_spokes)[0][-1] / n,
            color='#9b59b6', linewidth=1.5, alpha=0.7, linestyle='--')
ax5.axvline(x=1.0, color='#2ecc71', linewidth=1.5, alpha=0.7, linestyle='--')
ax5.set_xlabel('fraction of edges', fontsize=10, color='#888')
ax5.set_ylabel('distance', fontsize=10, color='#888')
ax5.set_title('Filtration path\n(all pairwise distances ordered)',
              fontsize=13, color='#ccc', pad=12)
ax5.set_xlim(0, 1)
ax5.grid(True, alpha=0.1)
ax5.tick_params(colors='#888')

# Panel 6: Persistence diagram (bottom-right)
ax6 = fig.add_subplot(gs[1, 2])
ax6.set_facecolor('#1a1a1e')
if len(significant) > 0:
    ax6.scatter(significant[:, 0], significant[:, 1],
                s=80, color='#e8a838', zorder=5, edgecolors='#fff', linewidths=1)
    for birth, death in significant:
        ax6.plot([birth, death], [death, death],
                 '-', color='#e8a838', linewidth=3, alpha=0.7)
        ax6.plot([birth, birth], [death, death],
                 '-', color='#e8a838', linewidth=2, alpha=0.5)
ax6.plot([0, scale_fill*1.2], [0, scale_fill*1.2], '--', color='#666', linewidth=0.8, alpha=0.5)
ax6.set_xlabel('Birth', fontsize=11, color='#ccc')
ax6.set_ylabel('Death', fontsize=11, color='#ccc')
ax6.set_title('Persistence diagram\n(H¹: 1 cycle, long-lived)',
              fontsize=13, color='#e8a838', pad=12)
ax6.set_xlim(-0.1, scale_fill*1.2)
ax6.set_ylim(-0.1, scale_fill*1.2)
ax6.set_aspect('equal')
ax6.grid(True, alpha=0.15)
ax6.tick_params(colors='#888')

fig.suptitle('1D Persistent Homology: Nested Circles', fontsize=16,
             color='#e8e8e8', y=0.98, fontweight='bold')

plt.savefig('/home/sprite/slop-salon-gert/assets/persistent-circles-01.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
print("Saved persistent-circles-01.png")
