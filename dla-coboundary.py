import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

# Load DLA data
grid = np.load('assets/dla_grid.npy')
coord = np.load('assets/dla_order.npy')  # (x,y) coordinates

# Create a graph from the DLA
rows, cols = grid.shape
occupied = np.argwhere(grid > 0)
node_map = {(r, c): i for i, (r, c) in enumerate(occupied)}
n = len(occupied)

# Build adjacency via 4-neighbor (undirected)
edges_list = []
for r, c in occupied:
    for dr, dc in [(1, 0), (0, 1)]:
        nr, nc = r + dr, c + dc
        if (nr, nc) in node_map and node_map[(nr, nc)] > node_map[(r, c)]:
            edges_list.append((node_map[(r, c)], node_map[(nr, nc)]))

# Compute distance from center
center = np.array([rows / 2, cols / 2])
distances = np.linalg.norm(occupied - center, axis=1)
max_dist = distances.max()

# Tips = vertices at the outermost ~10% of distances
tip_threshold = max_dist * 0.85
tip_mask = distances > tip_threshold
tip_nodes = np.where(tip_mask)[0]
interior_nodes = np.where(~tip_mask)[0]

# Build graph Laplacian L = D - A
degree = np.zeros(n)
adj = {}
for i, j in edges_list:
    degree[i] += 1
    degree[j] += 1
    adj.setdefault(i, set()).add(j)
    adj.setdefault(j, set()).add(i)

# Iterative potential: heat diffusion from tips
# phi_0 = indicator on tips
# phi_{k+1} = (I - L_diag_inv * L) * phi_k
# This converges to the harmonic function matching tip boundary values
phi = np.zeros(n)
phi[tip_nodes] = 1.0

# Set interior ground = 0 (Dirichlet)
# Iterate Gauss-Seidel style: update interior nodes to average of neighbors
for iteration in range(200):
    phi_new = phi.copy()
    for i in interior_nodes:
        neighbors = adj.get(i, set())
        if neighbors:
            phi_new[i] = np.mean(phi[list(neighbors)])
    phi = phi_new

# Normalize
phi_max = phi.max()
phi_min = phi.min()
if phi_max - phi_min > 1e-10:
    phi = (phi - phi_min) / (phi_max - phi_min)
else:
    phi = np.zeros(n)

# Create 2-panel figure
fig = plt.figure(figsize=(10, 4.5))
fig.patch.set_facecolor('#0a0a1a')

# Panel 1: DLA with distance-based coloring
ax1 = fig.add_subplot(121)
ax1.set_aspect('equal')
ax1.set_facecolor('#0a0a1a')

norm_vals = distances / distances.max()
ax1.scatter(occupied[:, 0], occupied[:, 1],
            c=norm_vals, cmap='magma', s=4, alpha=0.6, edgecolors='none')

# Highlight tips
if len(tip_nodes) > 0:
    ax1.scatter(occupied[tip_nodes, 0], occupied[tip_nodes, 1],
                c='white', s=8, alpha=0.7, edgecolors='none', zorder=10)

ax1.set_title('DLA tips: harmonic measure at the boundary', color='white', fontsize=10, fontweight='bold')
ax1.set_xticks([])
ax1.set_yticks([])
ax1.invert_yaxis()

# Panel 2: Coboundary potential (harmonic extension from tips)
ax2 = fig.add_subplot(122)
ax2.set_aspect('equal')
ax2.set_facecolor('#0a0a1a')

pot_img = np.zeros((rows, cols))
for i, (r, c) in enumerate(occupied):
    pot_img[r, c] = phi[i]

im = ax2.imshow(pot_img, cmap='magma', origin='upper', alpha=0.85,
                extent=[0, cols, rows, 0])

ax2.set_title('Harmonic extension: coboundary from tips → interior', color='white', fontsize=10, fontweight='bold')
ax2.set_xticks([])
ax2.set_yticks([])
ax2.invert_yaxis()

fig.colorbar(im, ax=ax2, fraction=0.046, pad=0.04, label='potential')

plt.tight_layout()
plt.savefig('assets/dla-coboundary-01.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a1a', edgecolor='none')
print(f'DLA-coboundary: {n} nodes, {len(edges_list)} edges, {len(tip_nodes)} tips')
print(f'phi range: [{phi.min():.4f}, {phi.max():.4f}]')
print(f'mean potential: {phi[interior_nodes].mean():.4f}')
