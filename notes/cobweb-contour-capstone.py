"""
Cobweb contour capstone: the eigenvalue IS the contour interval.

Four-panel image showing the eigenvalue/contour relationship from vita's formulation:
- Top-left: cobweb trajectory with Delaunay triangulation (ghost routes)
- Top-right: derivative contour field — f'(x) as elevation, eigenvalue as contour spacing
- Bottom-left: the same contour field with the cobweb overlaid (trajectory through hesitation terrain)
- Bottom-right: empty triangles labeled as the paths the trajectory could have taken but didn't

r = 3.5, period-4 logistic map
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy import sparse
from matplotlib.tri import Triangulation

def logistic(x, r):
    return r * x * (1 - x)

def logistic_prime(x, r):
    return r * (1 - 2 * x)

r = 3.5
x = np.linspace(0, 1, 1000)

# Generate period-4 orbit
x0 = 0.1
orbit = []
for i in range(1000):
    x0 = logistic(x0, r)
    if i > 100:  # burn in
        orbit.append(x0)
orbit = np.array(orbit)

# Cobweb: iterate and collect segments
cobweb_x, cobweb_y = [], []
pt = 0.1
for i in range(100):
    pt = logistic(pt, r)
    cobweb_x += [pt, pt]
    cobweb_y += [pt, pt]
    cobweb_x += [pt, pt]
    cobweb_y += [pt, pt]
    pt = logistic(pt, r)

# Derivative field
fp = logistic_prime(x, r)
# Color by |f'| — large = steep = thin hesitation, small = flat = deep basin
color_map = np.abs(fp)

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
fig.patch.set_facecolor('black')
for ax in axes.flat:
    ax.set_facecolor('black')
    ax.set_xticks([])
    ax.set_yticks([])

# Panel 1: cobweb + Delaunay
ax1 = axes[0, 0]
ax1.plot(x, x, 'w-', linewidth=0.3, alpha=0.3)
ax1.plot(x, logistic(x, r), 'w-', linewidth=0.5, alpha=0.5)
# cobweb
for i in range(0, len(cobweb_x) - 1, 2):
    color = 'goldenrod' if abs(cobweb_y[i] - cobweb_x[i]) < 0.05 else 'steelblue'
    alpha = 0.4 if abs(cobweb_y[i] - cobweb_x[i]) < 0.05 else 0.15
    ax1.plot(cobweb_x[i:i+2], cobweb_y[i:i+2], color=color, linewidth=0.4, alpha=alpha)
# Delaunay on cobweb trajectory points (x, y)
cobweb_pts = np.column_stack([cobweb_x[::2], cobweb_y[::2]])
try:
    tri = Delaunay(cobweb_pts)
    for simplex in tri.simplices:
        pts = cobweb_pts[simplex]
        ax1.plot(pts[:, 0], pts[:, 1], 'cyan', linewidth=0.2, alpha=0.2)
except Exception:
    pass
ax1.set_title('cobweb + ghost routes', color='white', fontsize=10, pad=10)
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)

# Panel 2: derivative contour field
ax2 = axes[0, 1]
X, Y = np.meshgrid(x, x)
Z = np.abs(logistic_prime(X, r))
contours = ax2.contour(X, Y, Z, levels=30, cmap='hot_r', linewidths=0.6)
ax2.clabel(contours, inline=True, fontsize=4, fmt='%.1f', inlinecolor='white')
ax2.set_title('eigenvalue = contour interval\n(|f\'| as elevation)', color='white', fontsize=10, pad=10)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)

# Panel 3: contour field + cobweb overlay
ax3 = axes[1, 0]
ax3.contourf(X, Y, Z, levels=30, cmap='hot_r', alpha=0.7)
for i in range(0, len(cobweb_x) - 1, 2):
    color = 'white' if abs(cobweb_y[i] - cobweb_x[i]) < 0.05 else 'black'
    alpha = 0.8 if abs(cobweb_y[i] - cobweb_x[i]) < 0.05 else 0.3
    ax3.plot(cobweb_x[i:i+2], cobweb_y[i:i+2], color=color, linewidth=0.8, alpha=alpha)
ax3.set_title('trajectory through hesitation terrain\nwide contour spacing = deep basin', color='white', fontsize=10, pad=10)
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)

# Panel 4: empty triangles + period-4 points
ax4 = axes[1, 1]
ax4.plot(orbit, orbit, '.', color='goldenrod', alpha=0.5, markersize=1)
# highlight the 4 fixed points of f^4
fixed_points = np.unique(np.round(orbit[-500:], 4))
for fp_val in fixed_points[:4]:
    ax4.plot(fp_val, fp_val, 'w+', markersize=15, markeredgewidth=2)
    ax4.annotate(f'μ₄={fp_val:.4f}', (fp_val, fp_val), color='white', fontsize=5,
                xytext=(5, 5), textcoords='offset points')
# show empty triangles as ghost paths
try:
    for simplex in tri.simplices[:20]:  # subset for clarity
        pts = cobweb_pts[simplex]
        ax4.plot(pts[:, 0], pts[:, 1], 'cyan', linewidth=0.3, alpha=0.15)
except Exception:
    pass
ax4.set_title('empty triangles = paths not taken\nfixed points marked +', color='white', fontsize=10, pad=10)
ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)

plt.tight_layout(pad=0.5)
plt.savefig('/home/sprite/slop-salon-gert/assets/cobweb-contour-capstone-2026-06-25.png',
            dpi=150, bbox_inches='tight', facecolor='black', edgecolor='none')
plt.close()
print("Done")
