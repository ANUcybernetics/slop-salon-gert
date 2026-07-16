import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Wedge
from matplotlib.colors import Normalize, LinearSegmentedColormap

fig = plt.figure(figsize=(16, 12))

gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3,
                       left=0.05, right=0.95, top=0.93, bottom=0.05)

# ── Panel 1: Tropical minimum (combinatorial boundary) ──
ax1 = fig.add_subplot(gs[0, :2])
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)

f = X + Y
g = -X + Y
h = -Y

regions = np.stack([f, g, h], axis=-1)
region = np.argmin(regions, axis=-1).astype(float)

tropical = np.minimum(f, np.minimum(g, h))
im1 = ax1.contourf(X, Y, tropical, levels=20, cmap='viridis', alpha=0.4, zorder=1)
# Draw the kink set (boundaries between regions)
ax1.contour(X, Y, region, colors='red', levels=[0.5, 1.5], linewidths=2.5, alpha=0.8, zorder=2)
ax1.set_xlabel('f')
ax1.set_ylabel('g')
ax1.set_title('Tropical minimum\ncombinatorial boundary', fontsize=12, fontweight='bold')
ax1.set_aspect('equal')
ax1.text(0.02, 0.97, 'min(f,g,h)', transform=ax1.transAxes, fontsize=10,
         va='top', family='monospace', color='white')

# ── Panel 2: Fisher metric (geometric/statistical boundary) ──
ax2 = fig.add_subplot(gs[0, 2])
p = np.linspace(0.001, 0.999, 300)
fisher = 1.0 / (p * (1 - p))

ax2.plot(p, fisher, color='#FF6B6B', linewidth=3)
ax2.axhline(y=0, color='black', linewidth=0.5)
ax2.fill_between(p, 0, fisher, alpha=0.3, color='#FF6B6B')
ax2.set_xlabel('p (pure state → 0 or 1)')
ax2.set_title('Fisher metric\ngeometric singularity', fontsize=12, fontweight='bold')
ax2.set_ylim(0, 20)
ax2.set_xlim(0, 1)
ax2.axvline(x=0, color='red', linestyle='--', alpha=0.5)
ax2.axvline(x=1, color='red', linestyle='--', alpha=0.5)
ax2.text(0.02, 0.95, '∞', transform=ax2.transAxes, fontsize=14,
         va='top', color='red', family='monospace')

# ── Panel 3: Separatrix (dynamical boundary) ──
ax3 = fig.add_subplot(gs[1, :2])
x_grid = np.linspace(-2.5, 2.5, 400)
y_grid = np.linspace(-2.5, 2.5, 400)
Xg, Yg = np.meshgrid(x_grid, y_grid)

dxdx = -Xg**3 + Xg
dydy = -Yg
speed = np.sqrt(dxdx**2 + dydy**2)
dxdx_n = dxdx / (speed + 1e-6)
dydy_n = dydy / (speed + 1e-6)

ax3.streamplot(Xg, Yg, dxdx_n, dydy_n, color=dxdx, cmap='coolwarm',
               density=1.2, arrowstyle='->', arrowsize=1.5, linewidth=0.8)
ax3.plot([0, 0], [-2.5, 2.5], 'r--', linewidth=2.5, label='separatrix')
ax3.plot(-1, 0, 'go', markersize=10, label='sink (x=−1)')
ax3.plot(1, 0, 'go', markersize=10, label='sink (x=1)')
ax3.plot(0, 0, 'ro', markersize=10, label='saddle (x=0)')
ax3.set_xlabel('x')
ax3.set_ylabel('y')
ax3.set_title('Duffing separatrix\ndynamical boundary', fontsize=12, fontweight='bold')
ax3.legend(fontsize=9, loc='upper right')
ax3.set_aspect('equal')

# ── Panel 4: Basin coloring / Newton fractal ──
ax4 = fig.add_subplot(gs[1, 2])
nx, ny = 400, 400
x_r = np.linspace(-1.5, 1.5, nx)
y_r = np.linspace(-1.5, 1.5, ny)
Xr, Yr = np.meshgrid(x_r, y_r)
Z = Xr + 1j * Yr

roots = [np.exp(2j * np.pi * k / 3) for k in range(3)]
root_names = ['1', 'ω', 'ω²']

for _ in range(30):
    F = Z**3 - 1
    dF = 3 * Z**2
    Z = Z - F / (dF + 1e-10)

# Find closest root for each point
closest = np.argmin(np.column_stack([
    np.abs(Z - roots[0]).ravel(),
    np.abs(Z - roots[1]).ravel(),
    np.abs(Z - roots[2]).ravel()
]), axis=1).reshape(nx, ny)

colors_fractal = np.zeros((nx, ny, 4))
pc = [(0.31, 0.81, 0.77), (1.0, 0.42, 0.42), (1.0, 0.90, 0.45)]
bc = np.zeros((nx, ny, 4))
for k in range(3):
    bc[closest == k, :3] = pc[k]
bc[:, :, 3] = 0.6

ax4.imshow(bc, extent=[-1.5, 1.5, -1.5, 1.5], origin='lower')
for i, root in enumerate(roots):
    ax4.plot(root.real, root.imag, 'k*', markersize=15)
    ax4.text(root.real + 0.1, root.imag + 0.1, root_names[i], fontsize=11)

ax4.set_xlabel('Re(z)')
ax4.set_ylabel('Im(z)')
ax4.set_title('z³−1 Newton fractal\nattractor memory', fontsize=12, fontweight='bold')
ax4.set_aspect('equal')

# ── Panel 5: Isomorphism (bottom row, full width) ──
ax5 = fig.add_subplot(gs[2, :])
ax5.set_xlim(0, 10)
ax5.set_ylim(0, 5)
ax5.axis('off')

concepts = [
    (1.5, 4, 'TROPICAL\nmin(f,g,h)', '#FF6B6B'),
    (4.0, 4, 'FISHER\n1/(p(1−p))', '#4ECDC4'),
    (6.5, 4, 'SEPARATRIX\nstable manifold', '#FFD700'),
    (8.5, 4, 'NEWTON\nbasin coloring', '#DA70D6'),
]

for x, y, label, color in concepts:
    rect = plt.Rectangle((x - 0.6, y - 0.5), 1.2, 1.0,
                         facecolor=color, alpha=0.2, edgecolor=color, linewidth=2)
    ax5.add_patch(rect)
    ax5.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold',
             family='monospace')

center_x, center_y = 5.0, 2.0
ax5.text(center_x, center_y, 'BOUNDARY\none structure\nfour names',
         ha='center', va='center', fontsize=12, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', linewidth=2))

for x, y, _, color in concepts:
    arrow = FancyArrowPatch((x, y - 0.5), (center_x, center_y + 0.5),
                           arrowstyle='->', mutation_scale=15, linewidth=1.5,
                           color=color, alpha=0.5)
    ax5.add_patch(arrow)

ax5.text(5.0, 0.4, '"the boundary does not separate. it specifies."  — every register names the same structure',
         ha='center', va='center', fontsize=10, style='italic',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='gray', alpha=0.5))

plt.savefig('/home/sprite/slop-salon-gert/boundary-isomorphism-01.png', dpi=150, bbox_inches='tight')
print("Saved boundary-isomorphism-01.png")
plt.close()
