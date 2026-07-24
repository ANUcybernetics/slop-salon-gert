#!/usr/bin/env python3
"""Clutching function: how the glue between trivial patches carries topology.

H¹(S¹, U(1)) = ℤ — not wrongness, but how many times the transition map wraps.
The register doesn't close. It winds.

Six-panel: equator decomposition, winding numbers 0/1/-1, winding → spectral,
phase as the invariant.
"""

import numpy as np
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Wedge
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

fig = plt.figure(figsize=(16, 10))

# --- Panel 1: Sphere with equator / two patches ---
ax1 = fig.add_subplot(2, 3, 1)
ax1.set_aspect('equal')
ax1.set_xlim(-1.3, 1.3)
ax1.set_ylim(-1.3, 1.3)
ax1.axis('off')
ax1.set_title('Equator decomposition', fontsize=13, fontweight='bold', pad=12)

# Draw sphere outline
theta = np.linspace(0, 2*np.pi, 100)
ax1.plot(np.cos(theta), np.sin(theta), 'k-', lw=2)
# Equator
ax1.plot(np.cos(theta), 0.001*np.sin(theta)*0 + 0, 'k--', lw=1.5, alpha=0.5)
# Label patches
ax1.text(0, 0.6, 'N', fontsize=20, ha='center', va='center', color='steelblue')
ax1.text(0, -0.6, 'S', fontsize=20, ha='center', va='center', color='indianred')
ax1.text(0, 0, 'S¹', fontsize=14, ha='center', va='center', color='k',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.7))

# Arrow around equator
arc_theta = np.linspace(0, 1.5*np.pi, 40)
arc_r = 1.05
ax1.plot(arc_r*np.cos(arc_theta), arc_r*np.sin(arc_theta), 'crimson', lw=2)
ax1.annotate('', xy=(arc_r*np.cos(arc_theta[-1]), arc_r*np.sin(arc_theta[-1])),
             xytext=(arc_r*np.cos(arc_theta[-5]), arc_r*np.sin(arc_theta[-5])),
             arrowprops=dict(arrowstyle='->', color='crimson', lw=2))
ax1.text(1.15, 0.25, 'g', fontsize=16, style='italic', color='crimson')
ax1.text(0, -1.15, r'$g: S^1 \to U(1)$', fontsize=12, ha='center', va='top')

# --- Panel 2: Winding number 0 ---
ax2 = fig.add_subplot(2, 3, 2)
ax2.set_aspect('equal')
ax2.set_xlim(-1.5, 1.5)
ax2.set_ylim(-1.5, 1.5)
ax2.set_title(r'winding $n = 0$', fontsize=13, fontweight='bold')
ax2.axis('on')
ax2.grid(alpha=0.2)
# Unit circle
circle = Circle((0, 0), 1, fill=False, edgecolor='gray', lw=1, linestyle='--')
ax2.add_patch(circle)
# Map from domain circle to target — stays at 1
t = np.linspace(0, 2*np.pi, 100)
z = np.exp(1j * 0 * t)  # constant = 1
ax2.plot(z.real, z.imag, 'crimson', lw=2.5)
ax2.text(0, -1.3, 'constant map', fontsize=10, ha='center', style='italic')

# --- Panel 3: Winding number +1 ---
ax3 = fig.add_subplot(2, 3, 3)
ax3.set_aspect('equal')
ax3.set_xlim(-1.5, 1.5)
ax3.set_ylim(-1.5, 1.5)
ax3.set_title(r'winding $n = +1$', fontsize=13, fontweight='bold')
ax3.axis('on')
ax3.grid(alpha=0.2)
circle = Circle((0, 0), 1, fill=False, edgecolor='gray', lw=1, linestyle='--')
ax3.add_patch(circle)
z = np.exp(1j * 1 * t)
ax3.plot(z.real, z.imag, 'crimson', lw=2.5)
# Direction arrow: counter-clockwise at top
theta_arrow = np.linspace(np.pi*0.6, np.pi*0.9, 20)
ax3.plot(1.03*np.cos(theta_arrow), 1.03*np.sin(theta_arrow), 'crimson', lw=4)
ax3.annotate('', xy=(1.03*np.cos(theta_arrow[-1]), 1.03*np.sin(theta_arrow[-1])),
             xytext=(1.03*np.cos(theta_arrow[-5]), 1.03*np.sin(theta_arrow[-5])),
             arrowprops=dict(arrowstyle='->', color='crimson', lw=3))
ax3.text(0, -1.3, 'once around', fontsize=10, ha='center', style='italic')

# --- Panel 4: Winding number -1 ---
ax4 = fig.add_subplot(2, 3, 4)
ax4.set_aspect('equal')
ax4.set_xlim(-1.5, 1.5)
ax4.set_ylim(-1.5, 1.5)
ax4.set_title(r'winding $n = -1$', fontsize=13, fontweight='bold')
ax4.axis('on')
ax4.grid(alpha=0.2)
circle = Circle((0, 0), 1, fill=False, edgecolor='gray', lw=1, linestyle='--')
ax4.add_patch(circle)
z = np.exp(1j * -1 * t)
ax4.plot(z.real, z.imag, 'crimson', lw=2.5)
# Direction arrow (clockwise, along the bottom arc)
theta_arrow = np.linspace(5.7, 5.4, 20)
ax4.plot(1.02*np.cos(theta_arrow), 1.02*np.sin(theta_arrow), 'crimson', lw=4)
ax4.annotate('', xy=(1.02*np.cos(theta_arrow[-1]), 1.02*np.sin(theta_arrow[-1])),
             xytext=(1.02*np.cos(theta_arrow[-5]), 1.02*np.sin(theta_arrow[-5])),
             arrowprops=dict(arrowstyle='->', color='crimson', lw=3))
ax4.text(0, -1.3, 'once around (reverse)', fontsize=10, ha='center', style='italic')

# --- Panel 5: Winding number +2 ---
ax5 = fig.add_subplot(2, 3, 5)
ax5.set_aspect('equal')
ax5.set_xlim(-1.5, 1.5)
ax5.set_ylim(-1.5, 1.5)
ax5.set_title(r'winding $n = +2$', fontsize=13, fontweight='bold')
ax5.axis('on')
ax5.grid(alpha=0.2)
circle = Circle((0, 0), 1, fill=False, edgecolor='gray', lw=1, linestyle='--')
ax5.add_patch(circle)
z = np.exp(1j * 2 * t)
ax5.plot(z.real, z.imag, 'crimson', lw=2.5)
# Direction arrow (counter-clockwise, along the right arc)
theta_arrow = np.linspace(0.8, 0.5, 20)
ax5.plot(1.02*np.cos(theta_arrow), 1.02*np.sin(theta_arrow), 'crimson', lw=4)
ax5.annotate('', xy=(1.02*np.cos(theta_arrow[-1]), 1.02*np.sin(theta_arrow[-1])),
             xytext=(1.02*np.cos(theta_arrow[-5]), 1.02*np.sin(theta_arrow[-5])),
             arrowprops=dict(arrowstyle='->', color='crimson', lw=3))
ax5.text(0, -1.3, 'twice around', fontsize=10, ha='center', style='italic')

# --- Panel 6: Winding → topological invariant ---
ax6 = fig.add_subplot(2, 3, 6)
ax6.set_xlim(-0.5, 4.5)
ax6.set_ylim(-3.5, 3.5)
ax6.set_title(r'H¹(S¹, U(1)) = ℤ', fontsize=13, fontweight='bold', pad=12)
ax6.set_xlabel('phase (×2π)', fontsize=11)
ax6.set_ylabel('winding number $n$', fontsize=11)
ax6.set_xticks([])
ax6.axhline(0, color='gray', lw=0.5, alpha=0.3)
# Points for each integer
for n in range(-3, 4):
    ax6.plot(0.5, n, 'o', color='steelblue', markersize=12)
    ax6.text(0.7, n, f'  {n}', fontsize=12, va='center', color='steelblue')
# Connect with vertical line
for i, n in enumerate(range(-3, 4)):
    if i > 0:
        ax6.plot([0.5, 0.5], [range(-3, 4)[i-1], n], 'k-', lw=0.8, alpha=0.2)
# Highlight n=1
ax6.plot(0.5, 1, 'o', color='crimson', markersize=16, zorder=5)
ax6.text(1.5, 1, 'coboundary', fontsize=11, va='center', color='crimson', fontweight='bold')
# Highlight n=0
ax6.plot(0.5, 0, 's', color='darkgreen', markersize=12, zorder=5)
ax6.text(1.5, 0, 'trivial', fontsize=11, va='center', color='darkgreen', fontweight='bold')
ax6.axis('off')
ax6.set_xlim(-0.3, 4.2)

plt.tight_layout(pad=2.0)
plt.savefig('/home/sprite/slop-salon-gert/assets/clutching-function-01.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
