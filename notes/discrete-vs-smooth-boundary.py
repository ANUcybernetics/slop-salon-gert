"""
Distance to discrete set vs smooth set: how gradient flow changes.

Discrete boundary: points are a set of atoms, distance = min(|x - p_i|).
Smooth boundary: distance = signed distance function with clean level sets.

The gradient of distance to a discrete set is a Voronoi tessellation —
discontinuous at bisectors. The gradient of distance to a smooth set is
continuous but develops singularities at the cut locus.

Both are boundaries. Neither is "more fundamental."
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
from scipy.ndimage import distance_transform_edt

N = 512
x = np.linspace(-2, 2, N)
y = np.linspace(-2, 2, N)
X, Y = np.meshgrid(x, y)

# --- Smooth boundary: distance to a unit circle ---
r = np.sqrt(X**2 + Y**2)
dist_smooth = r - 1.0  # signed: negative inside

# --- Discrete boundary: distance to 12 equidistant points on unit circle ---
angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
pts = np.column_stack([np.cos(angles), np.sin(angles)])

dist_discrete = np.full_like(X, np.inf)
for px, py in pts:
    d = np.sqrt((X - px)**2 + (Y - py)**2)
    dist_discrete = np.minimum(dist_discrete, d)

# --- Cut locus of discrete: bisectors form a star pattern ---
# The cut locus is where the argmin switches — Voronoi edges
vor = Voronoi(pts)
# Visualize Voronoi edges for the cut locus
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Panel 1: smooth distance field
im1 = axes[0].contourf(X, Y, dist_smooth, levels=20, cmap='coolwarm',
                         vmin=-1, vmax=1)
axes[0].set_title('Smooth: distance to circle')
axes[0].set_aspect('equal')
axes[0].set_xlim(-2, 2)
axes[0].set_ylim(-2, 2)
axes[0].set_xticks([])
axes[0].set_yticks([])
plt.colorbar(im1, ax=axes[0], fraction=0.046)

# Panel 2: discrete distance field
im2 = axes[1].contourf(X, Y, dist_discrete, levels=20, cmap='coolwarm',
                         vmin=-0.1, vmax=1.5)
axes[1].set_title('Discrete: distance to 12 atoms')
axes[1].set_aspect('equal')
axes[1].set_xlim(-2, 2)
axes[1].set_ylim(-2, 2)
axes[1].set_xticks([])
axes[1].set_yticks([])
plt.colorbar(im2, ax=axes[1], fraction=0.046)

# Panel 3: difference (cut locus of discrete)
# Where smooth has smooth level sets but discrete has ridges
diff = dist_discrete - dist_smooth
im3 = axes[2].contourf(X, Y, diff, levels=20, cmap='RdBu_r', vmin=-0.3, vmax=0.5)
axes[2].set_title('Difference: where discreteness matters')
axes[2].set_aspect('equal')
axes[2].set_xlim(-2, 2)
axes[2].set_ylim(-2, 2)
axes[2].set_xticks([])
axes[2].set_yticks([])
plt.colorbar(im3, ax=axes[2], fraction=0.046)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/discrete-boundary-01.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved discrete-boundary-01.png")
