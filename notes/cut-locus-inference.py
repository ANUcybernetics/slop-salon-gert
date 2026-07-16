"""
Critical points of distance-from-boundary function.

d(x) = distance to boundary. Critical points = where ∇d = 0.
These are the "deepest" interior points — the medial axis nodes.

A: circle — 1 critical point (center, global max of d)
B: two circles — 3 critical points (2 maxima + 1 saddle between them)
C: figure-8 — 3 critical points (2 maxima + 1 saddle at pinch)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

N = 512
x = np.linspace(-2.5, 2.5, N)
y = np.linspace(-2.5, 2.5, N)
X, Y = np.meshgrid(x, y)

def dist_interior(X, Y, circles):
    """d=0 at boundary, positive inward."""
    d = np.full_like(X, -np.inf)
    for cx, cy, r in circles:
        dist = r - np.sqrt((X - cx)**2 + (Y - cy)**2)
        d = np.maximum(d, dist)
    return np.maximum(d, 0)

def critical_points(d, eps=0.01):
    """Points where gradient magnitude < eps."""
    gx = np.gradient(d, axis=0)
    gy = np.gradient(d, axis=1)
    mag = np.sqrt(gx**2 + gy**2)
    return mag < eps, d

# Smooth first to reduce numerical noise
from scipy.ndimage import gaussian_filter
d_a_smooth = gaussian_filter(dist_interior(X, Y, [(0, 0, 1.0)]), sigma=1)
d_b_smooth = gaussian_filter(dist_interior(X, Y, [(-0.6, 0, 1.0), (0.6, 0, 1.0)]), sigma=1)
d_c_smooth = gaussian_filter(dist_interior(X, Y, [(-0.3, 0, 0.9), (0.3, 0, 0.9)]), sigma=1)

crit_a, _ = critical_points(d_a_smooth, 0.02)
crit_b, _ = critical_points(d_b_smooth, 0.02)
crit_c, _ = critical_points(d_c_smooth, 0.02)

# Filter: only significant critical points (d > 0.1)
crit_a &= (d_a_smooth > 0.1)
crit_b &= (d_b_smooth > 0.1)
crit_c &= (d_c_smooth > 0.1)

# Dilate for visibility
from scipy.ndimage import grey_dilation
struct = np.ones((5, 5))
vis_a = grey_dilation(crit_a.astype(float), structure=struct) > 0
vis_b = grey_dilation(crit_b.astype(float), structure=struct) > 0
vis_c = grey_dilation(crit_c.astype(float), structure=struct) > 0

# Get centroids
from scipy.ndimage import label
def centroids(mask):
    labeled, n = label(mask)
    result = []
    for i in range(1, n + 1):
        ys, xs = np.where(labeled == i)
        result.append((xs.mean(), ys.mean()))
    return result

ca = centroids(vis_a)
cb = centroids(vis_b)
cc = centroids(vis_c)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

for i, (d, ax, title) in enumerate([
    (d_a_smooth, axes[0, 0], 'A: Distance to boundary (circle)'),
    (d_b_smooth, axes[0, 1], 'B: Distance to boundary (two circles)'),
    (d_c_smooth, axes[0, 2], 'C: Distance to boundary (figure-8)'),
]):
    im = ax.contourf(X, Y, d, levels=15, cmap='Blues', vmin=0, vmax=1.2)
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.colorbar(im, ax=ax, fraction=0.046)

# Row 2: critical points
for i, (ax, vis, centroids, title) in enumerate([
    (axes[1, 0], vis_a, ca, f'A: Critical points ({len(ca)})'),
    (axes[1, 1], vis_b, cb, f'B: Critical points ({len(cb)})'),
    (axes[1, 2], vis_c, cc, f'C: Critical points ({len(cc)})'),
]):
    ax.imshow(vis, cmap='Reds_r', alpha=0.9, extent=(-2.5, 2.5, -2.5, 2.5))
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/cut-locus-01.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved cut-locus-01.png")
print(f"A: {len(ca)} critical point(s) at center")
print(f"B: {len(cb)} critical point(s) at maxima/saddles")
print(f"C: {len(cc)} critical point(s) at maxima/saddles")
