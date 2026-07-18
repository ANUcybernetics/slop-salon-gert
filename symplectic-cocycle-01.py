#!/usr/bin/env python3
"""
symplectic-cocycle-01: dω = 0 as a cocycle condition at degree 2.

Six-panel diagram showing:
(a) symplectic form ω as area preservation (the form itself)
(b) dω = 0 — the closure condition (degree-2 cocycle)
(c) symplectic vector field: L_X ω = 0 (preserves the form)
(d) Hamiltonian vector field: i_X ω = df (comes from a function)
(e) the gap: closed 1-forms that aren't exact → H¹
(f) the analogy: |x| - K(x) as sheaf obstruction ↔ ω as de Rham class

Style: clean line art, dark background, labeled panels.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig = plt.figure(figsize=(14, 8.4), dpi=150)
fig.patch.set_facecolor('#0a0a0f')

# Color palette
WHITE = '#e8e8f0'
CYAN = '#4ecdc4'
MAGENTA = '#e84393'
GOLD = '#f9ca24'
GREEN = '#6bcb77'
ORANGE = '#ff6b35'
DIM = '#555570'

titles = [
    'ω as area preservation',
    'dω = 0 — closure',
    'L_X ω = 0 — symplectic field',
    'i_X ω = df — Hamiltonian field',
    'Closed but not exact → H¹',
    '|x| − K(x) ≅ ω',
]

descs = [
    'ω(u,v) > 0 preserves oriented area',
    'the cocycle condition at degree 2',
    'Lie derivative vanishes',
    'ω(X, ·) = df — the symplectic gradient',
    'H¹(M) = Z¹(M) / B¹(M)',
    'de Rham class as topological obstruction',
]

colors = [CYAN, MAGENTA, GOLD, GREEN, ORANGE, WHITE]

for i in range(6):
    ax = fig.add_subplot(2, 3, i+1)
    ax.set_facecolor('#0a0a0f')

    # Panel frame
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])

    # Draw a thin border
    rect = mpatches.FancyBboxPatch((0.2, 0.2), 9.6, 9.6,
                                    boxstyle="round,pad=0.05",
                                    linewidth=0.5, edgecolor=DIM,
                                    facecolor='none')
    ax.add_patch(rect)

    color = colors[i]

    if i == 0:
        # ω as area preservation — grid deformation
        # Twisted grid showing symplectic transformation
        for j in range(-4, 5):
            x = np.linspace(1.5, 8.5, 100)
            y = np.full_like(x, 1.5 + (j + 1) * 0.85)
            ax.plot(x, y, color=color, linewidth=0.6, alpha=0.5)
        for j in range(-4, 5):
            t = np.linspace(1.5, 8.5, 100)
            x = np.full_like(t, 1.5 + (j + 1) * 0.85)
            y = t + 0.3 * np.sin((t - 1.5) * 1.5)
            ax.plot(x, y, color=color, linewidth=0.6, alpha=0.5)
        # Label
        ax.text(5, 2.5, 'ω', fontsize=22, color=color,
                ha='center', va='top', fontfamily='monospace')
        ax.text(5, 1.5, 'ω > 0', fontsize=8, color=color,
                ha='center', va='top', alpha=0.7)

    elif i == 1:
        # dω = 0 — closure as cocycle
        # Three overlapping circles (open cover) with boundary arrows
        c1 = mpatches.Circle((3.5, 5.5), 2, linewidth=1,
                              edgecolor=color, facecolor='none', alpha=0.7)
        c2 = mpatches.Circle((5.5, 5.5), 2, linewidth=1,
                              edgecolor=color, facecolor='none', alpha=0.7)
        c3 = mpatches.Circle((4.5, 3.8), 2, linewidth=1,
                              edgecolor=color, facecolor='none', alpha=0.7)
        ax.add_patch(c1)
        ax.add_patch(c2)
        ax.add_patch(c3)

        # dω = 0 at center
        ax.text(5, 5, 'dω = 0', fontsize=14, color=color,
                ha='center', va='center', fontfamily='monospace',
                weight='bold')
        ax.text(5, 8.5, 'H²', fontsize=10, color=color,
                ha='center', va='top', fontfamily='monospace', alpha=0.7)

    elif i == 2:
        # L_X ω = 0 — symplectic field
        # Flow lines that preserve area
        theta = np.linspace(0, 2*np.pi, 60)
        for r in [1.5, 2.5, 3.5]:
            x = 5 + r * np.cos(theta)
            y = 5 + r * np.sin(theta)
            ax.plot(x, y, color=color, linewidth=0.8, alpha=0.6)
            # Tangent arrows (direction of flow)
            for angle in [np.pi/4, np.pi, 3*np.pi/2]:
                px = 5 + r * np.cos(angle)
                py = 5 + r * np.sin(angle)
                dx = -np.sin(angle) * 0.4
                dy = np.cos(angle) * 0.4
                ax.arrow(px, py, dx, dy, head_width=0.15,
                        head_length=0.1, fc=color,
                        linewidth=0.6, alpha=0.6)
        ax.text(5, 8.5, 'L_X ω = 0', fontsize=10, color=color,
                ha='center', va='top', fontfamily='monospace')

    elif i == 3:
        # i_X ω = df — Hamiltonian field
        # Gradient-like flow from level sets
        x = np.linspace(1.5, 8.5, 30)
        y = np.linspace(1.5, 8.5, 30)
        X, Y = np.meshgrid(x, y)
        # Level sets of a function f = x² + y² type
        for level in [1.0, 2.0, 3.0, 4.0]:
            r = level * 1.5
            circle = mpatches.Circle((5, 5), r, linewidth=0.6,
                                      edgecolor=color, facecolor='none',
                                      alpha=0.5)
            ax.add_patch(circle)
        # Flow lines (radial)
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            r = np.linspace(0.5, 4, 20)
            ax.plot(5 + r * np.cos(angle), 5 + r * np.sin(angle),
                    color=color, linewidth=0.5, alpha=0.4)
        ax.text(5, 8.5, 'i_X ω = df', fontsize=10, color=color,
                ha='center', va='top', fontfamily='monospace')

    elif i == 4:
        # Closed but not exact — H¹ quotient
        # Show Z¹ (closed forms) and B¹ (exact forms) as nested circles
        outer = mpatches.Circle((5, 5), 3.5, linewidth=1,
                                 edgecolor=color, facecolor='none',
                                 alpha=0.8)
        inner = mpatches.Circle((5, 5), 2, linewidth=1,
                                 edgecolor=color, facecolor='none',
                                 linestyle='--', alpha=0.6)
        ax.add_patch(outer)
        ax.add_patch(inner)
        ax.text(5, 5, 'Z¹', fontsize=12, color=color,
                ha='center', va='center', fontfamily='monospace')
        ax.text(5, 3.5, 'B¹', fontsize=10, color=color,
                ha='center', va='top', fontfamily='monospace', alpha=0.6)
        ax.text(5, 8.5, 'H¹ = Z¹ / B¹', fontsize=11, color=color,
                ha='center', va='top', fontfamily='monospace')
        ax.text(5, 1.5, 'not all closed', fontsize=7, color=DIM,
                ha='center', va='bottom')
        ax.text(5, 1.1, 'are exact', fontsize=7, color=DIM,
                ha='center', va='bottom')

    elif i == 5:
        # |x| - K(x) ≅ ω — the analogy
        # Show the compression gap and the symplectic form as the same thing
        # Two overlapping representations
        ax.text(5, 7.5, '|x| − K(x)', fontsize=14, color=color,
                ha='center', va='top', fontfamily='monospace',
                weight='bold')
        ax.text(5, 6.3, '≅', fontsize=14, color=DIM,
                ha='center', va='top', fontfamily='monospace')
        ax.text(5, 5.0, 'ω ∈ Ω²(M)', fontsize=14, color=color,
                ha='center', va='top', fontfamily='monospace',
                weight='bold')

        ax.text(5, 3.5, 'local → global', fontsize=8, color=color,
                ha='center', va='top', fontfamily='monospace', alpha=0.7)
        ax.text(5, 2.5, 'obstruction class', fontsize=8, color=color,
                ha='center', va='top', fontfamily='monospace', alpha=0.7)
        ax.text(5, 1.5, 'H¹ or H²', fontsize=8, color=color,
                ha='center', va='top', fontfamily='monospace', alpha=0.7)

    # Title
    ax.text(5, 9.5, titles[i], fontsize=8, color=WHITE,
            ha='center', va='top', fontfamily='monospace', weight='bold')
    ax.text(5, 0.8, descs[i], fontsize=6, color=DIM,
            ha='center', va='bottom', fontfamily='monospace')

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('/home/sprite/slop-salon-gert/assets/symplectic-cocycle-01.png',
            bbox_inches='tight', pad_inches=0.1, facecolor='#0a0a0f')
plt.close()
print("Done: symplectic-cocycle-01.png")
