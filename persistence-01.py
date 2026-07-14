import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import scipy
import scipy.spatial
from ripser import ripser as _ripser

# Three panels: point cloud with VR triangulation, persistence diagram,
# Betti curves across the filtration

np.random.seed(42)

# Point cloud on a circle + noise
theta = np.linspace(0, 2*np.pi, 30, endpoint=False)
radius = 1.5
x = radius * np.cos(theta) + np.random.normal(0, 0.08, 30)
y = radius * np.sin(theta) + np.random.normal(0, 0.08, 30)
pts = np.column_stack([x, y])

n_noise = 15
noise_pts = np.column_stack([
    np.random.uniform(-1.5, 1.5, n_noise),
    np.random.uniform(-1.5, 1.5, n_noise),
])
all_pts = np.vstack([pts, noise_pts])

# Distance matrix
D = scipy.spatial.distance.cdist(all_pts, all_pts, metric='euclidean')
n = len(all_pts)

# Full persistence across all scales
vr = _ripser(D, maxdim=1, distance_matrix=True)
dgms = vr['dgms']

# --- Panel 1: Point cloud with VR triangulation at a specific scale ---
fig = plt.figure(figsize=(12, 11), facecolor='#1a1a2e')
gs = GridSpec(2, 2, figure=fig, wspace=0.40, hspace=0.35)

scale = 1.8
mask = D <= scale

ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor('#1a1a2e')

for i in range(n):
    for j in range(i+1, n):
        if mask[i, j]:
            ax1.plot([all_pts[i, 0], all_pts[j, 0]],
                    [all_pts[i, 1], all_pts[j, 1]],
                    color='#4a4a6a', linewidth=0.4, alpha=0.5)

circle_mask = np.array([np.linalg.norm(p) > 1.0 for p in all_pts])
circle_pts = all_pts[circle_mask]

ax1.scatter(circle_pts[:, 0], circle_pts[:, 1], s=30, c='#e6c84a',
          edgecolors='#c9a832', linewidths=0.5, zorder=5)
ax1.scatter(all_pts[~circle_mask, 0], all_pts[~circle_mask, 1],
          s=20, c='#6a6a8a', zorder=4)

ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-2.5, 2.5)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('Vietoris-Rips complex at scale r=1.8',
             color='#c8c8e0', fontsize=11, pad=12)

# --- Panel 2: Persistence diagram ---
ax2 = fig.add_subplot(gs[1, 0])
ax2.set_facecolor('#1a1a2e')

if len(dgms[1]) > 0:
    h1 = dgms[1]
    ax2.scatter(h1[:, 0], h1[:, 1], s=80, c='#e6c84a', edgecolors='#c9a832',
               linewidths=1.5, zorder=3)
    ax2.plot([-0.5, 3.5], [-0.5, 3.5], color='#4a4a6a', linewidth=1, linestyle='--')
    for bx, by in h1:
        ax2.plot([bx, bx, by, by], [bx, by, by, bx],
                color='#e6c84a', linewidth=1.5, alpha=0.8)

ax2.set_xlim(-0.5, 3.5)
ax2.set_ylim(-0.5, 3.5)
ax2.set_xlabel('Birth', color='#c8c8e0', fontsize=9)
ax2.set_ylabel('Death', color='#c8c8e0', fontsize=9)
ax2.tick_params(colors='#8a8aa0', labelsize=8)
ax2.set_title('Persistence diagram (H₁)', color='#c8c8e0', fontsize=11)

# --- Panel 3: Betti numbers vs filtration ---
ax3 = fig.add_subplot(gs[1, 1])
ax3.set_facecolor('#1a1a2e')

# Betti number βᵢ(f) = number of bars (b, d) with b ≤ f < d
scales = np.linspace(0.2, 4.0, 200)
h1_betti = []
for f in scales:
    count = 0
    for bar in dgms[1]:
        if bar[0] <= f < bar[1]:
            count += 1
    h1_betti.append(count)

scales_arr = np.array(scales)
ax3.fill_between(scales_arr, h1_betti, alpha=0.4, color='#e6c84a')
ax3.plot(scales_arr, h1_betti, color='#e6c84a', linewidth=1.5)

ax3.axvline(scale, color='#ff6b6b', linewidth=1, linestyle='--', alpha=0.6,
           label=f'r=1.8 (panel 1)')
ax3.legend(fontsize=8, frameon=False, labelcolor='#c8c8e0')

ax3.set_xlabel('Filtration parameter r', color='#c8c8e0', fontsize=9)
ax3.set_ylabel('β₁(r)', color='#c8c8e0', fontsize=9)
ax3.tick_params(colors='#8a8aa0', labelsize=8)
ax3.set_title('Persistent H₁ cycle', color='#c8c8e0', fontsize=11)

# --- Panel 4: Euler characteristic across filtration ---
ax4 = fig.add_subplot(gs[0, 1])
ax4.set_facecolor('#1a1a2e')

h0_betti = []
h1_betti_full = []
for f in scales:
    b0 = 0
    b1 = 0
    for bar in dgms[0]:
        if bar[0] <= f < bar[1]:
            b0 += 1
    for bar in dgms[1]:
        if bar[0] <= f < bar[1]:
            b1 += 1
    h0_betti.append(b0)
    h1_betti_full.append(b1)

h0_betti = np.array(h0_betti)
h1_betti_full = np.array(h1_betti_full)
chi = h0_betti - h1_betti_full

ax4.plot(scales_arr, h0_betti, color='#4a8af0', linewidth=1.2, label='β₀')
ax4.plot(scales_arr, h1_betti_full, color='#e6c84a', linewidth=1.2, label='β₁')
ax4.plot(scales_arr, chi, color='#6ae', linewidth=1.5, label='χ = β₀ − β₁')

ax4.set_xlabel('Filtration r', color='#c8c8e0', fontsize=9)
ax4.set_ylabel('Betti numbers', color='#c8c8e0', fontsize=9)
ax4.tick_params(colors='#8a8aa0', labelsize=8)
ax4.legend(fontsize=8, frameon=False, labelcolor='#c8c8e0')
ax4.set_title('Euler characteristic χ(r)', color='#c8c8e0', fontsize=11)

fig.suptitle('Persistent homology on a Vietoris-Rips complex',
            color='#e0e0f0', fontsize=13, y=0.98)

plt.savefig('persistence-01.png', dpi=150, bbox_inches='tight',
           facecolor='#1a1a2e', edgecolor='none')
print("Done — saved persistence-01.png")
