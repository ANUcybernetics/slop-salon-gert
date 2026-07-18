#!/usr/bin/env python3
"""deformation-04: integrability theorem — when do first-order deformations extend?"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(14, 10))
fig.patch.set_facecolor('#0a0a0f')

gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

# Color palette
h1_color = '#4fc3f7'  # light blue for H¹
h2_color = '#ef5350'  # red for H²
kernel_color = '#66bb6a'  # green for kernel / extendable
null_color = '#78909c'  # grey for H²=0 case
extend_color = '#29b6f6'  # cyan for extending paths

# ---- Panel 0: Filtration by integrability ----
ax0 = fig.add_subplot(gs[0, 0])
ax0.set_facecolor('#0a0a0f')

# H¹ as a large circle
circle_h1 = Circle((0.5, 0.5), 0.35, fill=True, facecolor=h1_color,
                    edgecolor='white', linewidth=1.5, alpha=0.3, label='H¹')
ax0.add_patch(circle_h1)

# Nested kernels: ker(θ) ⊃ ker(θ²) ⊃ ker(θ³)
for i, (r, label, color) in enumerate([
    (0.28, r'$\ker \theta$', kernel_color),
    (0.19, r'$\ker \theta^2$', '#42a5f5'),
    (0.10, r'$\ker \theta^3$', '#80deea'),
]):
    circle = Circle((0.5, 0.5), r, fill=True, facecolor=color,
                    edgecolor='white', linewidth=1.0, alpha=0.4)
    ax0.add_patch(circle)
    ax0.text(0.5, 0.5 - r - 0.03, label, ha='center', va='top',
             fontsize=10, color=color, fontweight='bold')

# Center point
ax0.plot(0.5, 0.5, 'o', color='white', markersize=4)
ax0.text(0.5, 0.5, '0', ha='center', va='center', fontsize=8, color='white')

# Labels
ax0.text(0.5, 0.02, 'filtration by integrability', ha='center', va='bottom',
         fontsize=10, color='white', fontweight='bold')
ax0.text(0.5, 0.96, 'A', ha='center', va='top', fontsize=12, color=null_color,
         fontweight='bold')
ax0.set_xlim(0, 1)
ax0.set_ylim(0, 1)
ax0.axis('off')

# ---- Panel 1: Obstruction map ----
ax1 = fig.add_subplot(gs[0, 1])
ax1.set_facecolor('#0a0a0f')

# H¹ as rectangle on left
rect_h1 = Rectangle((0.05, 0.25), 0.2, 0.5, fill=True, facecolor=h1_color,
                     edgecolor='white', linewidth=1.5, alpha=0.3)
ax1.add_patch(rect_h1)
ax1.text(0.15, 0.78, r'$H^1$', ha='center', va='top', fontsize=12,
         color=h1_color, fontweight='bold')

# H² as rectangle on right
rect_h2 = Rectangle((0.75, 0.25), 0.2, 0.5, fill=True, facecolor=h2_color,
                     edgecolor='white', linewidth=1.5, alpha=0.3)
ax1.add_patch(rect_h2)
ax1.text(0.85, 0.78, r'$H^2$', ha='center', va='top', fontsize=12,
         color=h2_color, fontweight='bold')

# Quadratic obstruction map: θ: H¹ → Sym²(H¹)* ⊗ H²
# Draw several arrows, most hitting non-zero, a few hitting zero
np.random.seed(42)
for i in range(12):
    y_in = 0.3 + 0.4 * np.random.random()
    if i < 3:
        # hitting kernel (zero obstruction)
        y_out = 0.5
        color = kernel_color
        alpha = 0.8
    else:
        y_out = 0.25 + 0.5 * np.random.random()
        color = h2_color
        alpha = 0.4
    ax1.annotate('', xy=(0.76, y_out), xytext=(0.25, y_in),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5, alpha=alpha))

# Arrow label
ax1.text(0.5, 0.92, r'$\theta_2: H^1 \to \mathrm{Sym}^2(H^1)^* \otimes H^2$',
         ha='center', va='bottom', fontsize=9, color='white')

ax1.text(0.5, 0.02, 'quadratic obstruction map', ha='center', va='bottom',
         fontsize=10, color='white', fontweight='bold')
ax1.text(0.5, 0.96, 'B', ha='center', va='top', fontsize=12, color=null_color,
         fontweight='bold')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')

# ---- Panel 2: K3 (unobstructed) vs general ----
ax2 = fig.add_subplot(gs[1, 0])
ax2.set_facecolor('#0a0a0f')

# Left: H² = 0 (K3, Calabi-Yau)
ax2.text(0.25, 0.93, r'$H^2 = 0$', ha='center', va='top', fontsize=11,
         color=extend_color, fontweight='bold')

# H¹ circle — all extend
circle_all = Circle((0.25, 0.55), 0.22, fill=True, facecolor=extend_color,
                    edgecolor='white', linewidth=1.5, alpha=0.3)
ax2.add_patch(circle_all)
ax2.text(0.25, 0.55, r'all extend', ha='center', va='center', fontsize=9,
         color='white')

# Arrow to "deformations = H¹"
ax2.annotate('', xy=(0.48, 0.55), xytext=(0.38, 0.55),
            arrowprops=dict(arrowstyle='->', color=extend_color, lw=2))
ax2.text(0.43, 0.58, 'unobstructed', ha='center', va='bottom',
         fontsize=8, color=extend_color)

ax2.text(0.48, 0.55, r'$\Rightarrow \dim \mathcal{M} = \dim H^1$',
         ha='left', va='center', fontsize=9, color=extend_color)

ax2.text(0.25, 0.25, r'K3 / Calabi–Yau', ha='center', va='center',
         fontsize=9, color=null_color)

# Right: H² ≠ 0 (general)
ax2.text(0.78, 0.93, r'$H^2 \neq 0$', ha='center', va='top',
         fontsize=11, color=h2_color, fontweight='bold')

# H¹ circle — some extend
circle_h1_r = Circle((0.78, 0.55), 0.22, fill=True, facecolor=h1_color,
                     edgecolor='white', linewidth=1.5, alpha=0.3)
ax2.add_patch(circle_h1_r)

# Mark a kernel subspace
circle_kern = Circle((0.78, 0.55), 0.10, fill=True, facecolor=kernel_color,
                     edgecolor='white', linewidth=1.0, alpha=0.5)
ax2.add_patch(circle_kern)
ax2.text(0.78, 0.40, r'$\ker \theta_2$', ha='center', va='top',
         fontsize=8, color=kernel_color)

ax2.annotate('', xy=(0.95, 0.55), xytext=(0.88, 0.55),
            arrowprops=dict(arrowstyle='->', color=h2_color, lw=2))
ax2.text(0.92, 0.58, 'obstructed', ha='center', va='bottom',
         fontsize=8, color=h2_color)

ax2.text(0.95, 0.55, r'$\dim \mathcal{M}_{\mathrm{Kuranishi}} = \dim \ker \theta_2$',
         ha='left', va='center', fontsize=8, color=h2_color)

ax2.text(0.78, 0.25, 'general', ha='center', va='center',
         fontsize=9, color=null_color)

ax2.text(0.5, 0.02, 'integrability = H² = 0 (sufficient, not necessary)',
         ha='center', va='bottom', fontsize=10, color='white', fontweight='bold')
ax2.text(0.5, 0.96, 'C', ha='center', va='top', fontsize=12, color=null_color,
         fontweight='bold')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')

# ---- Panel 3: Deformation curve + obstruction locus ----
ax3 = fig.add_subplot(gs[1, 1])
ax3.set_facecolor('#0a0a0f')

# H¹ as a 2D space (x₁, x₂ representing coordinates in H¹)
theta = np.linspace(0, 2*np.pi, 200)
# Obstruction locus: a curve in H¹ where θ vanishes (kernel curve)
# Simulate a conic section (quadratic constraint)
u = np.linspace(-0.4, 0.4, 100)
v_obst = np.sqrt(0.16 - u**2) * np.sign(u + 0.3)  # approximate circle-ish
x_kern = 0.5 + u
y_kern = 0.5 + v_obst

# Plot kernel curve (green)
ax3.plot(x_kern, y_kern, color=kernel_color, linewidth=2.5, alpha=0.8,
         label=r'$\ker \theta_2$')

# Fill H¹ region
circle_full = Circle((0.5, 0.5), 0.42, fill=True, facecolor=h1_color,
                     edgecolor='white', linewidth=1.0, alpha=0.15)
ax3.add_patch(circle_full)
ax3.text(0.08, 0.92, r'$H^1$', ha='left', va='top', fontsize=12,
         color=h1_color, fontweight='bold')

# Several deformation paths
# Path that avoids obstruction (extends — green)
t = np.linspace(0, 1, 50)
x1 = 0.5 + 0.3 * t
y1 = 0.3 + 0.3 * t * (1 - 0.5 * t)
ax3.plot(x1, y1, color=kernel_color, linewidth=2, alpha=0.9)
ax3.plot(x1[0], y1[0], 'o', color=kernel_color, markersize=6)
ax3.plot(x1[-1], y1[-1], '^', color=kernel_color, markersize=8)

# Path that hits obstruction (breaks — red)
x2 = 0.3 + 0.4 * t
y2 = 0.3 + 0.5 * t
ax3.plot(x2, y2, color=h2_color, linewidth=2, alpha=0.7)
ax3.plot(x2[0], y2[0], 'o', color=h2_color, markersize=6)
hit_idx = 30
ax3.plot(x2[hit_idx], y2[hit_idx], 'x', color='white', markersize=10,
         markeredgewidth=2)
# remainder dashed (doesn't extend)
ax3.plot(x2[hit_idx:], y2[hit_idx:], color=h2_color, linewidth=2,
         alpha=0.4, linestyle='--')

# Another path that grazes and extends
x3 = 0.4 + 0.1 * np.sin(3 * t)
y3 = 0.3 + 0.4 * t
ax3.plot(x3, y3, color=extend_color, linewidth=1.5, alpha=0.6)
ax3.plot(x3[0], y3[0], 'o', color=extend_color, markersize=5)
ax3.plot(x3[-1], y3[-1], '^', color=extend_color, markersize=7)

# Labels
ax3.text(0.5, 0.02, 'paths through H¹ — obstruction locus as boundary',
         ha='center', va='bottom', fontsize=10, color='white', fontweight='bold')
ax3.text(0.5, 0.96, 'D', ha='center', va='top', fontsize=12, color=null_color,
         fontweight='bold')
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.set_aspect('equal')
ax3.axis('off')

plt.savefig('/home/sprite/slop-salon-gert/assets/deformation-04.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
print("deformation-04.png written")
