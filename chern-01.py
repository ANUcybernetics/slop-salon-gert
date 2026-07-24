#!/usr/bin/env python3
"""Chern class visualization: clutching function extends to disk.
The clutching map g: S¹ → U(1) with winding n defines a bundle over S².
The first Chern number equals the winding count.

6-panel: the clutching map on the equator, Chern number as intersection,
        curvature 2-form, holonomy loop.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle
from mpl_toolkits.mplot3d import proj3d

plt.rcParams['axes.facecolor'] = '#1a1a1e'
plt.rcParams['figure.facecolor'] = '#1a1a1e'
plt.rcParams['text.color'] = '#e8e8e8'
plt.rcParams['axes.labelcolor'] = '#e8e8e8'
plt.rcParams['mathtext.fontset'] = 'cm'

fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor('#1a1a1e')

# --- Panel 1: Churiching function as map from equator ---
ax1 = plt.subplot(2, 3, 1)
theta = np.linspace(0, 2*np.pi, 120)
n = 3  # winding number
g = np.exp(1j * n * theta)

# Source circle
src = np.exp(1j * theta)
ax1.plot(src.real, src.imag, color='#6a8fba', linewidth=1.5, alpha=0.8)
# Target circle
tgt = np.exp(1j * theta)
ax1.plot(tgt.real, tgt.imag, color='#d96272', linewidth=1.5, alpha=0.8)

# Arrows from source to target
for i in range(0, 120, 15):
    ax1.annotate('', xy=(tgt[i].real, tgt[i].imag),
                xytext=(src[i].real, src[i].imag),
                arrowprops=dict(arrowstyle='->', color='#f0c060',
                              lw=1.0, alpha=0.5))

ax1.plot([0], [0], 'kx', markersize=8, markeredgewidth=2)
ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-1.5, 1.5)
ax1.set_aspect('equal')
ax1.set_title(r'clutching map: $g: S^1 \to U(1)$, $n=3$', fontsize=11)
ax1.set_xlabel(r'source $S^1$', fontsize=9)
ax1.set_ylabel(r'target $U(1)$', fontsize=9)
ax1.grid(False)
ax1.axhline(0, color='#444', lw=0.5)
ax1.axvline(0, color='#444', lw=0.5)

# --- Panel 2: Winding visualization ---
ax2 = plt.subplot(2, 3, 2)
ax2.set_xlim(-1.5, 1.5)
ax2.set_ylim(-1.5, 1.5)
ax2.set_aspect('equal')

# Multiple windings overlaid
for w in [1, 2, 3]:
    phase = w * theta
    r = 0.5 + 0.5 * np.sin(phase)
    ax2.plot(r * np.cos(theta), r * np.sin(theta),
            color='#6a8fba' if w == 3 else '#d96272',
            linewidth=2.0 if w == 3 else 1.0,
            alpha=0.9 if w == 3 else 0.4)

circle = Circle((0, 0), 1.0, fill=False, color='#666', lw=0.5, linestyle='--')
ax2.add_patch(circle)
ax2.set_title('winding n=1, 2, 3 — n=3 bold', fontsize=11)
ax2.set_xlabel('phase in complex plane', fontsize=9)
ax2.grid(False)
ax2.axhline(0, color='#444', lw=0.5)
ax2.axvline(0, color='#444', lw=0.5)

# --- Panel 3: S² with clutching along equator ---
ax3 = plt.subplot(2, 3, 3, projection='3d')
u = np.linspace(0, np.pi, 40)
v = np.linspace(0, 2*np.pi, 40)
U, V = np.meshgrid(u, v)
X = np.sin(U) * np.cos(V)
Y = np.sin(U) * np.sin(V)
Z = np.cos(U)
ax3.plot_surface(X, Y, Z, alpha=0.15, color='#6a8fba', shade=False)

# Equator
equator_u = np.linspace(0, 2*np.pi, 80)
ax3.plot(np.cos(equator_u), np.sin(equator_u), np.zeros(80),
        color='#d96272', linewidth=2.5)

# Arrows along equator showing the clutching direction
for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
    px = np.cos(angle)
    py = np.sin(angle)
    dx = -np.sin(angle) * 0.15
    dy = np.cos(angle) * 0.15
    ax3.quiver(px, py, 0, dx, dy, 0, color='#f0c060',
              arrow_length_ratio=0.6, linewidth=1.5)

ax3.set_title(r'$S^2$ with clutching along equator', fontsize=11)
ax3.set_zticks([])
ax3.set_xticks([])
ax3.set_yticks([])

# --- Panel 4: Chern number = winding count ---
ax4 = plt.subplot(2, 3, 4)
ax4.axis('off')
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)

# Draw the formula
ax4.text(5, 8.5, 'first Chern class', ha='center', fontsize=13,
        color='#f0c060', weight='bold')
ax4.text(5, 7.0, r'$c_1(E) = \frac{i}{2\pi} \int_{S^2} \text{tr}(F)$',
        ha='center', fontsize=14, color='#e8e8e8',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#2a2a30', edgecolor='#6a8fba'))

ax4.text(5, 5.0, 'clutching number = winding count', ha='center', fontsize=11,
        color='#d96272')
ax4.text(5, 3.8, r'$n = \frac{1}{2\pi i} \oint_{S^1} g^{-1} dg$',
        ha='center', fontsize=13, color='#e8e8e8',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#2a2a30', edgecolor='#d96272'))

ax4.text(5, 2.0, r'$c_1 = n$', ha='center', fontsize=18, color='#f0c060',
        weight='bold')

ax4.text(5, 0.5, 'topological: integer, not continuous', ha='center',
        fontsize=9, color='#888', style='italic')

# --- Panel 5: Curvature 2-form visualization ---
ax5 = plt.subplot(2, 3, 5)
# Create a 2D visualization of the curvature form
x = np.linspace(-2, 2, 60)
y = np.linspace(-2, 2, 60)
X, Y = np.meshgrid(x, y)
r = np.sqrt(X**2 + Y**2)
# Gaussian curvature concentrated at origin
kappa = 3 * np.exp(-r**2)

cf = ax5.contourf(X, Y, kappa, levels=20, cmap='RdYlBu_r', alpha=0.8)
ax5.contour(X, Y, kappa, levels=10, colors='#888', linewidths=0.5, alpha=0.5)
ax5.set_title(r'curvature 2-form: $F = dA + A \wedge A$', fontsize=11)
ax5.set_xlabel('disk coordinate z', fontsize=9)
ax5.set_ylabel(r'disk coordinate \bar{z}', fontsize=9)
ax5.set_aspect('equal')

# --- Panel 6: Bundle visualization — fiber over each point ---
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')
ax6.set_xlim(0, 10)
ax6.set_ylim(0, 10)

ax6.text(5, 9, 'the bundle is the choice', ha='center', fontsize=13,
        color='#f0c060', weight='bold')

# Show two different bundles with same clutching base
# Bundle 1: trivial (n=0)
ax6.plot([1, 1], [7.5, 5.5], color='#6a8fba', linewidth=3, alpha=0.6)
ax6.text(1, 4.8, 'n=0', ha='center', fontsize=10, color='#6a8fba')
ax6.text(1, 4.2, '(trivial)', ha='center', fontsize=8, color='#6a8fba', style='italic')

# Bundle 2: nontrivial (n=3)
path_x = [5]
path_y = [7.5, 6.5, 6.0, 6.2, 5.8, 6.0, 5.5]
for i in range(len(path_y)-1):
    ax6.plot([path_x[-1], path_x[-1]], [path_y[i], path_y[i+1]],
            color='#d96272', linewidth=3, alpha=0.6)
ax6.text(5, 4.8, 'n=3', ha='center', fontsize=10, color='#d96272')
ax6.text(5, 4.2, '(twisted)', ha='center', fontsize=8, color='#d96272', style='italic')

# Arrow between them
ax6.annotate('', xy=(3.5, 6.5), xytext=(2.5, 6.5),
            arrowprops=dict(arrowstyle='<->', color='#f0c060', lw=2))
ax6.text(3, 7.0, 'c₁ = n', ha='center', fontsize=10, color='#f0c060')

ax6.text(5, 3.0, 'same base, different total space', ha='center',
        fontsize=10, color='#888')

ax6.text(5, 1.5, 'the clutching function', ha='center', fontsize=9,
        color='#e8e8e8', style='italic')
ax6.text(5, 0.8, 'picks the bundle', ha='center', fontsize=9,
        color='#e8e8e8', style='italic')

plt.tight_layout(pad=2.0)
plt.savefig('/home/sprite/slop-salon-gert/assets/chern-01.png', dpi=150,
            bbox_inches='tight', facecolor='#1a1a1e')
plt.close()

print('Written: assets/chern-01.png')
