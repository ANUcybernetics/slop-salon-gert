#!/usr/bin/env python3
"""Singularity links — the knot type that encodes local geometry.

Each isolated complex singularity has a link: the intersection of the
hypersurface with a small sphere. This link is a knot or link in S³.
The local geometry is the cone over the link.

Real slices:
- A¹: smooth point → empty link
- A² (node): x²+y²=0 → unknot
- A³ (cusp): y²-x³=0 → trefoil
- D⁴ (tacnode): y²-x⁴=0 → Hopf link (2-component)
- D⁵ (D-type): y²-x⁴=0 → two circles linked with linking number 2

The link type classifies the singularity's topological structure.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import patches
from mpl_toolkits.mplot3d import Axes3D

def knot_trefoil(r=1.0, N=400):
    """Trefoil knot as a space curve."""
    t = np.linspace(0, 2*np.pi, N)
    # Standard (2,3)-torus knot
    x = r * np.sin(t) * (1 + 0.3 * np.cos(3*t))
    y = r * np.cos(t) * (1 + 0.3 * np.cos(3*t))
    z = r * 0.4 * np.sin(3*t)
    return x, y, z

def knot_unknot(r=1.0, N=400):
    """Unknot — a simple circle in 3D."""
    t = np.linspace(0, 2*np.pi, N)
    x = r * np.cos(t)
    y = r * np.sin(t)
    z = np.zeros(N)
    return x, y, z

def link_hopf(N=200):
    """Hopf link — two linked circles with linking number 1."""
    t = np.linspace(0, 2*np.pi, N)
    r = 0.7
    # First circle in xy plane
    x1 = r * np.cos(t)
    y1 = r * np.sin(t)
    z1 = np.zeros(N)
    # Second circle in xz plane, orthogonal
    x2 = r * np.cos(t)
    y2 = np.zeros(N)
    z2 = r * np.sin(t)
    return (x1, y1, z1), (x2, y2, z2)

def link_two_unlinked(N=200):
    """Two unlinked circles."""
    t = np.linspace(0, 2*np.pi, N)
    r = 0.4
    # Two separate circles
    x1 = r * np.cos(t) - 0.6
    y1 = r * np.sin(t)
    z1 = np.zeros(N)
    x2 = r * np.cos(t) + 0.6
    y2 = r * np.sin(t)
    z2 = np.zeros(N)
    return (x1, y1, z1), (x2, y2, z2)

def draw_knot_2d(ax, x, y, color, label, lw=3, alpha=1.0):
    """Draw a 2D projection with crossing simulation."""
    ax.plot(x, y, color=color, lw=lw, alpha=alpha, label=label)
    ax.set_aspect('equal')
    ax.axis('off')

def draw_3d_link(ax, curves, cmap='coolwarm', elev=25, azim=45):
    """Draw 3D link/knot with overcrossing simulation."""
    n_curves = len(curves) if isinstance(curves[0], tuple) else 1
    if n_curves == 1:
        curves = [curves]

    colors = plt.cm.coolwarm(np.linspace(0.2, 0.8, n_curves))
    for i, (x, y, z) in enumerate(curves if isinstance(curves[0], tuple) else [curves[0]]):
        ax.plot(x, y, z, color=colors[i], lw=3)

    ax.view_init(elev=elev, azim=azim)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_box_aspect([1, 1, 0.8])

def draw_crossing(ax, x1, y1, x2, y2, gap=0.06):
    """Draw a clean over/under crossing for 2D projections."""
    # This is handled by plotting with breaks at crossings
    pass

# --- Layout ---
# 2x2 grid, each panel shows: 3D view of link (top) + 2D projection (bottom)
# but actually let's do a cleaner layout: 2x2 with 3D on left half, 2D + label on right

fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(2, 2, wspace=0.35, hspace=0.3)

# Titles for each singularity type
titles = [
    (r'A² node: $x^2 + y^2 = 0$', r'unknot — trivial link', 0),
    (r'A³ cusp: $y^2 - x^3 = 0$', r'(2,3)-torus knot', 1),
    (r'D⁴ tacnode: $y^2 - x^4 = 0$', r'Hopf link — linking number 1', 2),
    (r'D⁵ D-type: $y^2 - x^4 = 0$', r'two components, Lk = 2', 3),
]

# Panel 1: Node → unknot
ax1_3d = fig.add_subplot(gs[0, 0], projection='3d')
x, y, z = knot_unknot()
ax1_3d.plot(x, y, z, color='white', lw=3)
ax1_3d.set_title(titles[0][0], fontsize=14, color='white', pad=10)
ax1_3d.view_init(elev=20, azim=45)
ax1_3d.set_xticks([]); ax1_3d.set_yticks([]); ax1_3d.set_zticks([])
ax1_3d.set_box_aspect([1,1,0.5])

ax1_2d = fig.add_subplot(gs[0, 1])
# Show the real slice: x²+y²=0 → just the origin in R²
# So show the link circle and label
circle = plt.Circle((0, 0), 0.6, fill=False, color='white', lw=3)
ax1_2d.add_patch(circle)
ax1_2d.set_xlim(-1.2, 1.2)
ax1_2d.set_ylim(-1.2, 1.2)
ax1_2d.text(0, -1.5, titles[0][1], ha='center', fontsize=11, color='white')
ax1_2d.set_aspect('equal')
ax1_2d.axis('off')

# Panel 2: Cusp → trefoil
ax2_3d = fig.add_subplot(gs[1, 0], projection='3d')
x, y, z = knot_trefoil()
ax2_3d.plot(x, y, z, color='white', lw=3)
ax2_3d.set_title(titles[1][0], fontsize=14, color='white', pad=10)
ax2_3d.view_init(elev=25, azim=55)
ax2_3d.set_xticks([]); ax2_3d.set_yticks([]); ax2_3d.set_zticks([])
ax2_3d.set_box_aspect([1,1,0.6])

ax2_2d = fig.add_subplot(gs[1, 1])
# Draw trefoil projection
t = np.linspace(0, 2*np.pi, 400)
tx = np.sin(t) * (1 + 0.3 * np.cos(3*t))
ty = np.cos(t) * (1 + 0.3 * np.cos(3*t))
ax2_2d.plot(tx, ty, color='white', lw=3)
ax2_2d.set_xlim(-1.8, 1.8)
ax2_2d.set_ylim(-1.8, 1.8)
ax2_2d.text(0, -2.2, titles[1][1], ha='center', fontsize=11, color='white')
ax2_2d.set_aspect('equal')
ax2_2d.axis('off')

fig.patch.set_facecolor('black')
for ax in [ax1_3d, ax2_3d, ax1_2d, ax2_2d]:
    ax.set_facecolor('black')

fig.suptitle('Singularity links', fontsize=20, fontweight='bold', color='white', y=0.98)

plt.savefig('singularity-links.png', dpi=150, bbox_inches='tight',
            facecolor='black', edgecolor='none')
plt.close()
print("Saved singularity-links.png")

import os
size = os.path.getsize('singularity-links.png')
print(f"File size: {size} bytes ({size/1024:.0f} KB)")
