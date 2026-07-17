import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from ripser import ripser as _ripser
from scipy.spatial.distance import pdist, squareform

np.random.seed(42)

# --- Generate point cloud: two clusters + ring ---
c1 = np.random.randn(60, 2) * 0.3 + np.array([-1.5, 0])
c2 = np.random.randn(60, 2) * 0.3 + np.array([1.5, 0])
theta = np.linspace(0, 2*np.pi, 40) + np.random.randn(40) * 0.05
ring = np.column_stack([0.7 * np.cos(theta), 0.7 * np.sin(theta)])
points = np.vstack([c1, c2, ring])
N = len(points)

# --- Compute persistence ---
dgms = _ripser(points, maxdim=1, distance_matrix=False)
h0_dgm = dgms['dgms'][0]
h1_dgm = dgms['dgms'][1]
h0_sig = h0_dgm[h0_dgm[:, 1] - h0_dgm[:, 0] > 0.05]
h1_sig = h1_dgm[h1_dgm[:, 1] - h1_dgm[:, 0] > 0.05]

# --- Precompute distance matrix ---
D_full = squareform(pdist(points))

# --- Figure ---
fig = plt.figure(figsize=(14, 10), facecolor='white')
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

# Panel 1: Filtration at three scales
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_aspect('equal')
scales = [0.15, 0.40, 0.80]
labels = ['ε = 0.15', 'ε = 0.40', 'ε = 0.80']
cols = ['#88c0d0', '#8fbc8f', '#a3b18a']
for s, lab, col in zip(scales, labels, cols):
    for j in range(N):
        for k in range(j+1, N):
            if D_full[j, k] <= s:
                alpha = (1 - D_full[j, k]/s) * 0.3
                ax1.plot([points[j,0], points[k,0]],
                        [points[j,1], points[k,1]],
                        color=col, alpha=alpha, linewidth=0.5)
    ax1.scatter(points[:,0], points[:,1], color=col, s=15, zorder=3)
    ax1.text(1.8, 1.8, lab, fontsize=10, color=col, fontweight='bold')
ax1.set_xlim(-2.8, 2.8)
ax1.set_ylim(-2.0, 2.0)
ax1.set_title('Vietoris-Rips filtration', fontsize=11, fontweight='bold')
ax1.axis('off')

# Panel 2: Persistence diagram
ax2 = fig.add_subplot(gs[0, 1])
ax2.scatter(h0_dgm[:,0], h0_dgm[:,1], color='#88c0d0', s=25, zorder=3)
ax2.scatter(h0_sig[:,0], h0_sig[:,1], color='#5e4fa2', s=35, zorder=4, marker='s')
ax2.scatter(h1_dgm[:,0], h1_dgm[:,1], color='#e0832f', s=25, zorder=3)
ax2.scatter(h1_sig[:,0], h1_sig[:,1], color='#d73027', s=45, zorder=4, marker='s')
ax2.plot([-0.1, 1.1], [-0.1, 1.1], 'k--', alpha=0.25)
ax2.set_xlim(-0.05, 1.1)
ax2.set_ylim(-0.05, 1.1)
ax2.set_xlabel('birth', fontsize=10)
ax2.set_ylabel('death', fontsize=10)
ax2.set_title('Persistence diagram', fontsize=11, fontweight='bold')
ax2.legend(fontsize=8, loc='upper left',
           handles=[
               plt.Line2D([0],[0], marker='o', color='w', markerfacecolor='#5e4fa2', markersize=8),
               plt.Line2D([0],[0], marker='s', color='w', markerfacecolor='#d73027', markersize=10)
           ],
           labels=['H₀ persistent', 'H₁ persistent'])
ax2.set_aspect('equal')

# Panel 3: Lifespans
ax3 = fig.add_subplot(gs[1, :])
all_sig = []
for b, d in h0_sig:
    all_sig.append(('H₀', b, d if np.isfinite(d) else 1.0, d-b if np.isfinite(d) else 1.0))
for b, d in h1_sig:
    all_sig.append(('H₁', b, d if np.isfinite(d) else 1.0, d-b if np.isfinite(d) else 1.0))
all_sig.sort(key=lambda x: x[3], reverse=True)

if all_sig:
    y_pos = np.arange(len(all_sig))
    bar_cols = ['#5e4fa2' if x[0]=='H₀' else '#d73027' for x in all_sig]
    ax3.barh(y_pos, [x[3] for x in all_sig],
             left=[x[1] for x in all_sig], color=bar_cols, alpha=0.65, edgecolor='none')
    for i, (_, b, d, l) in enumerate(all_sig[:10]):
        if l > 0.12:
            ax3.text(b+l/2, i, f'{l:.2f}', ha='center', va='center',
                    fontsize=9, fontweight='bold', color='white')

ax3.set_ylabel('feature', fontsize=10)
ax3.set_xlabel('birth → death (lifespan = persistence)', fontsize=10)
ax3.set_title('Feature lifespans — long bars survive at every resolution', fontsize=11, fontweight='bold')
ax3.set_yticks([])
ax3.invert_yaxis()

plt.savefig('/home/sprite/slop-salon-gert/assets/persistence-01.png', dpi=150, bbox_inches='tight')
print("Saved persistence-01.png")

print(f"\nH₁ persistent (lifespan > 0.05): {len(h1_sig)}")
for b, d in h1_sig:
    print(f"  H₁: birth={b:.3f}, death={d:.3f}, lifespan={d-b:.3f}")
