import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(15, 5))

# --- Panel 1: The single space ---
ax1 = fig.add_subplot(131)

# Single vector space V, shown as a cloud of points
np.random.seed(42)
V = np.random.randn(200, 2) * 0.8

ax1.scatter(V[:, 0], V[:, 1], c='steelblue', s=8, alpha=0.6, label='V')

# ker and im as overlapping subspaces
# ker: vectors that survive
ker_theta = np.linspace(0, 2*np.pi, 30)
ker_x = 0.6 * np.cos(ker_theta)
ker_y = 0.6 * np.sin(ker_theta)
ax1.plot(ker_x, ker_y, 'o-', c='darkgreen', linewidth=2, markersize=3, label='ker(δ)', alpha=0.8)

# im: vectors that are carried forward (same circle, shifted perspective)
# For panel 1, show im as nearly identical — slightly different radius
im_x = 0.62 * np.cos(ker_theta)
im_y = 0.62 * np.sin(ker_theta)
ax1.plot(im_x, im_y, 's-', c='darkorange', linewidth=2, markersize=3, label='im(δ)', alpha=0.8)

ax1.set_xlim(-1.2, 1.2)
ax1.set_ylim(-1.2, 1.2)
ax1.set_aspect('equal')
ax1.set_title('The Single Space', fontsize=14, fontweight='bold')
ax1.legend(fontsize=9, loc='upper right')
ax1.grid(True, alpha=0.2)
ax1.text(0, -1.05, 'ker and im: same subspace', ha='center', fontsize=10, alpha=0.7)

# --- Panel 2: Two charts ---
ax2 = fig.add_subplot(132)

# Show the same space with two different coordinate assignments
# Chart 1 (ker perspective) — blue dots
chart1 = V.copy()
ax2.scatter(chart1[:, 0], chart1[:, 1], c='steelblue', s=8, alpha=0.4, label='V in chart₁ (ker)')

# Chart 2 (im perspective) — same points, slightly rotated
angle = 0.15
rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
chart2 = V @ rot.T
ax2.scatter(chart2[:, 0], chart2[:, 1], c='coral', s=8, alpha=0.4, label='V in chart₂ (im)')

# Draw transition map arrows for a few key points
arrow_indices = [10, 50, 100, 150]
for i in arrow_indices:
    ax2.annotate('', xy=chart2[i], xytext=chart1[i],
                arrowprops=dict(arrowstyle='->', color='purple', lw=1.5, alpha=0.5))

# Draw the subspaces
k1_x, k1_y = 0.6*np.cos(ker_theta), 0.6*np.sin(ker_theta)
i1_x, i1_y = 0.62*np.cos(ker_theta), 0.62*np.sin(ker_theta)
ax2.plot(k1_x, k1_y, '-', c='darkgreen', linewidth=2, markersize=3, alpha=0.8)

k2_arr = np.column_stack([0.6*np.cos(ker_theta), 0.6*np.sin(ker_theta)]) @ rot.T
i2_arr = np.column_stack([0.62*np.cos(ker_theta), 0.62*np.sin(ker_theta)]) @ rot.T
ax2.plot(k2_arr[:, 0], k2_arr[:, 1], 's-', c='darkgreen', linewidth=2, markersize=3, alpha=0.5)
ax2.plot(i2_arr[:, 0], i2_arr[:, 1], 's-', c='darkorange', linewidth=2, markersize=3, alpha=0.5)

ax2.set_xlim(-1.2, 1.2)
ax2.set_ylim(-1.2, 1.2)
ax2.set_aspect('equal')
ax2.set_title('Two Charts', fontsize=14, fontweight='bold')
ax2.legend(fontsize=9, loc='upper right')
ax2.grid(True, alpha=0.2)
ax2.text(0, -1.05, r'$\delta$: transition function $\tau \in \mathrm{GL}(V)$', ha='center', fontsize=10, alpha=0.7)

# --- Panel 3: The crease ---
ax3 = fig.add_subplot(133)

# A continuous surface with a fold/crease
# Use a simple sheet folded along a line
x = np.linspace(-2, 2, 100)
y = np.linspace(-1.5, 1.5, 80)
X, Y = np.meshgrid(x, y)

# Sheet that folds along y=0 — same material, different orientation
Z = np.where(Y > 0, Y * 0.3, -Y * 0.3)

# Add a subtle highlight along the crease
Z_crest = np.abs(Y) * 0.3 * np.exp(-X**2 / 4)

surf = ax3.contourf(X, Y, Z + Z_crest, levels=20, cmap='coolwarm')

# Draw the crease line prominently
ax3.axhline(0, c='black', linewidth=2.5, linestyle='-', zorder=5)

# Add arrows showing the fold direction
for xi in [-1.5, -0.5, 0.5, 1.5]:
    ax3.annotate('', xy=(xi, 0.15), xytext=(xi, -0.15),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5, alpha=0.6))

ax3.set_xlim(-2, 2)
ax3.set_ylim(-1.5, 1.5)
ax3.set_title('The Crease', fontsize=14, fontweight='bold')
ax3.set_xlabel('x', fontsize=10)
ax3.set_ylabel('y', fontsize=10)
ax3.text(0, 1.3, r'$\delta$ is the crease that proves the paper was never folded before',
         ha='center', fontsize=9.5, alpha=0.8)
ax3.text(0, -1.3, r'ker = im, chart₁ ≠ chart₂', ha='center', fontsize=10, alpha=0.7)
ax3.grid(True, alpha=0.15)

plt.colorbar(surf, ax=ax3, fraction=0.046, pad=0.04)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/crease-01.png', dpi=150, bbox_inches='tight')
plt.close()
print("Created crease-01.png")
