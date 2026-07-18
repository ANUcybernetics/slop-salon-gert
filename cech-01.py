#!/usr/bin/env python3
"""Cech cocycle visualization — local-to-global problem."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

def make_circles(ax, alpha=1.0):
    """Make three overlapping circles on given axes."""
    c1 = Circle((0.35, 0.5), 0.4, fill=False, edgecolor='#4488cc', linewidth=2.5 * alpha)
    c2 = Circle((0.65, 0.5), 0.4, fill=False, edgecolor='#44bb66', linewidth=2.5 * alpha)
    c3 = Circle((0.5, 0.72), 0.35, fill=False, edgecolor='#dd8844', linewidth=2.5 * alpha)
    ax.add_patch(c1)
    ax.add_patch(c2)
    ax.add_patch(c3)
    return c1, c2, c3

fig = plt.figure(figsize=(15, 10))

# ── Panel 1: Open cover with local sections ──
ax1 = fig.add_subplot(2, 3, 1)
ax1.set_xlim(-0.1, 1.1)
ax1.set_ylim(-0.1, 1.1)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title(r'Open cover $\{U_i\}$ — local sections $s_i \in \mathcal{F}(U_i)$',
              fontsize=11, fontweight='bold')

make_circles(ax1)
ax1.text(0.22, 0.45, 'U$_1$', fontsize=14, color='#4488cc', fontweight='bold')
ax1.text(0.78, 0.45, 'U$_2$', fontsize=14, color='#44bb66', fontweight='bold')
ax1.text(0.5, 0.88, 'U$_3$', fontsize=14, color='#dd8844', fontweight='bold')

# Local section values (represented as concentric rings inside each region)
for cx, cy, color in [(0.35, 0.5, '#4488cc'), (0.65, 0.5, '#44bb66'), (0.5, 0.6, '#dd8844')]:
    for r in np.linspace(0.05, 0.25, 5):
        theta = np.linspace(0, 2*np.pi, 20)
        x = cx + r * np.cos(theta) * 0.5
        y = cy + r * np.sin(theta) * 0.5
        ax1.plot(x, y, color=color, alpha=0.15, linewidth=0.8)

ax1.text(0.5, 0.05, 's$_1$, s$_2$, s$_3$ defined separately on each U$_i$',
         fontsize=9, ha='center', style='italic')

# ── Panel 2: Overlaps and cocycle condition ──
ax2 = fig.add_subplot(2, 3, 2)
ax2.set_xlim(-0.1, 1.1)
ax2.set_ylim(-0.1, 1.1)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('Restrictions to overlaps — cocycle condition', fontsize=11, fontweight='bold')

make_circles(ax2)

# Highlight overlaps
ov12 = Circle((0.5, 0.5), 0.15, fill=True, facecolor='#88cc88', alpha=0.3, edgecolor='none')
ov23 = Circle((0.58, 0.62), 0.13, fill=True, facecolor='#ccaa66', alpha=0.3, edgecolor='none')
ov13 = Circle((0.42, 0.62), 0.13, fill=True, facecolor='#88aacc', alpha=0.3, edgecolor='none')
ax2.add_patch(ov12)
ax2.add_patch(ov23)
ax2.add_patch(ov13)

ax2.text(0.5, 0.48, 'U$_1$$\cap$U$_2$', fontsize=9, ha='center', fontweight='bold')
ax2.text(0.6, 0.76, 'U$_2$$\cap$U$_3$', fontsize=9, ha='center', fontweight='bold')
ax2.text(0.38, 0.76, 'U$_1$$\cap$U$_3$', fontsize=9, ha='center', fontweight='bold')

# Cocycle condition
ax2.text(0.5, 0.65, r's$_1$|$_{U_{12}}$ = s$_2$|$_{U_{12}}$', fontsize=9,
         color='red', fontweight='bold')

ax2.text(0.5, 0.08, r'On $U_i \cap U_j$:  $s_i - s_j = 0$  (the cocycle condition)',
         fontsize=9, ha='center', style='italic',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.4))

# ── Panel 3: Gluing attempt — global section ──
ax3 = fig.add_subplot(2, 3, 3)
ax3.set_xlim(-0.1, 1.1)
ax3.set_ylim(-0.1, 1.1)
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_title('Attempt to glue — global section?', fontsize=11, fontweight='bold')

make_circles(ax3)

# Show attempted global section as a continuous field
x = np.linspace(0, 1, 50)
y = np.linspace(0, 1, 50)
X, Y = np.meshgrid(x, y)

R = np.sqrt((X - 0.5)**2 + (Y - 0.5)**2)
theta = np.arctan2(Y - 0.5, X - 0.5)
Z = np.sin(3 * theta) * np.exp(-2 * R)

# Show a ring (annulus) where the field is continuous
mask = (R < 0.35) & (R > 0.15)
Z[~mask] = np.nan

ax3.contourf(X, Y, Z, levels=15, cmap='coolwarm', alpha=0.7)
ax3.contour(X, Y, Z, levels=5, colors='black', linewidths=0.5, alpha=0.3)

# Show the "hole" or obstruction
hole = Circle((0.5, 0.5), 0.08, fill=True, facecolor='black', edgecolor='white', linewidth=2)
ax3.add_patch(hole)

# Red X through the center
ax3.plot([0.45, 0.55], [0.45, 0.55], 'r-', linewidth=2)
ax3.plot([0.45, 0.55], [0.55, 0.45], 'r-', linewidth=2)

ax3.text(0.5, 0.02, 'Continuous field defined piecewise, but cannot extend globally',
         fontsize=9, ha='center', style='italic')

# ── Panel 4: Cech 1-cocycle as coboundary ──
ax4 = fig.add_subplot(2, 3, 4)
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)
ax4.axis('off')
ax4.set_title(r'$\check{C}^1(\{U_i\}, \mathcal{F})$ — Cech cochains',
              fontsize=11, fontweight='bold')

y_start = 8.5
ax4.text(5, y_start, r'A Cech 1-cocycle $\lambda = \{\lambda_{ij}\}$ satisfies:',
         fontsize=10, ha='center')

y_start -= 1.2
ax4.text(5, y_start, r'$\lambda_{ij} = s_i|_{U_i \cap U_j} - s_j|_{U_i \cap U_j}$',
         fontsize=12, ha='center',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#ddeeff', edgecolor='#4488cc', linewidth=2))

y_start -= 1.3
ax4.text(5, y_start, r'If every cocycle is a coboundary,  $\check{H}^1 = 0$',
         fontsize=10, ha='center', style='italic')

y_start -= 1.2
ax4.text(5, y_start, r'This means: local sections ALWAYS patch globally.',
         fontsize=9, ha='center', color='#228844')

y_start -= 1.5
ax4.text(5, y_start, r'On a Stein manifold or contractible space — true.',
         fontsize=8, ha='center', style='italic', color='gray')

y_start -= 1.5
ax4.text(5, y_start, r'$\delta: \check{C}^0 \to \check{C}^1$', fontsize=10, ha='center')
y_start -= 0.8
ax4.text(5, y_start, r'$(\delta s)_{ij} = s_i - s_j$', fontsize=10, ha='center',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffcc', edgecolor='orange', linewidth=1.5))

# ── Panel 5: H¹ as obstruction ──
ax5 = fig.add_subplot(2, 3, 5)
ax5.set_xlim(0, 10)
ax5.set_ylim(0, 10)
ax5.axis('off')
ax5.set_title(r'$\check{H}^1(X, \mathcal{F}) = \check{Z}^1 / \check{B}^1$ — the obstruction',
              fontsize=10, fontweight='bold')

y_start = 8.5
ax5.text(5, y_start, r'$\check{Z}^1$: cocycles (patching data on overlaps)',
         fontsize=9.5, ha='center')
y_start -= 1.0
ax5.text(5, y_start, r'$\check{B}^1$: coboundaries (trivial patching)',
         fontsize=9.5, ha='center')
y_start -= 1.0
ax5.text(5, y_start, r'$\check{H}^1 \neq 0$  $\Leftrightarrow$  some cocycles are not coboundaries',
         fontsize=10, ha='center', fontweight='bold', color='red')
y_start -= 1.2
ax5.text(5, y_start, 'The local sections satisfy compatibility\nbut no global section exists.',
         fontsize=9, ha='center', style='italic',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffcccc', alpha=0.5))

y_start -= 1.8
ax5.text(5, y_start, 'Example: tangent bundle of S$^2$',
         fontsize=9, ha='center', color='gray')
y_start -= 0.8
ax5.text(5, y_start, '(hairy ball theorem)',
         fontsize=9, ha='center', style='italic', color='gray')

# ── Panel 6: Sheaf of compressible strings ──
ax6 = fig.add_subplot(2, 3, 6)
ax6.set_xlim(0, 10)
ax6.set_ylim(0, 10)
ax6.axis('off')
ax6.set_title(r'$\mathcal{K}$: sheaf of compressible strings',
              fontsize=11, fontweight='bold')

y_start = 8.5
ax6.text(5, y_start, r'Stalk at x: $\mathcal{K}_x = \lim_{\ni x} \{s \in \mathcal{F}(U) : K(s) < |s|\}$',
         fontsize=9, ha='center')

y_start -= 1.3
ax6.text(5, y_start, r'$|x| - K(x)$ = "distance" from stalk to global section',
         fontsize=9.5, ha='center',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#ddeeff', edgecolor='#4488cc', linewidth=2))

y_start -= 1.4
ax6.text(5, y_start, 'Periodic strings $\to$ local sections $\to$ patch at x',
         fontsize=8.5, ha='center', color='#4488cc')
y_start -= 0.7
ax6.text(5, y_start, 'Random strings $\to$ refuse to close $\to$ no local section',
         fontsize=8.5, ha='center', color='#cc4444')
y_start -= 1.2
ax6.text(5, y_start, r'$\check{H}^1(X, \mathcal{K}) \neq 0$  $\Leftrightarrow$  compression is local, not global',
         fontsize=9, ha='center', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffcc', edgecolor='red', linewidth=2))

y_start -= 1.4
ax6.text(5, y_start, 'H$^1$ measures the gap between local compression\nand global computability.',
         fontsize=8.5, ha='center', style='italic')

plt.tight_layout()
plt.savefig('cech-01.png', dpi=150, bbox_inches='tight', facecolor='black', edgecolor='none')
plt.close()

print("Done: cech-01.png")
