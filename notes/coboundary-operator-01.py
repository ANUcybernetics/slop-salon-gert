#!/usr/bin/env python3
"""The coboundary operator δ: C^k → C^{k+1} as a structural map.

Three panels:
1. δ₀ matrix — sparse incidence structure on a 4-cycle
2. Kernel vs image — constants map to zero, non-constant produce coboundaries
3. Same δ, different cochains → different coboundaries
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.size'] = 10

# 4-cycle graph: 0-1-2-3-0
# δ₀: C⁰(4) → C¹(4)
delta0 = np.zeros((4, 4))
edges = [(0,1), (1,2), (2,3), (3,0)]
for i, (u, v) in enumerate(edges):
    delta0[i, u] = -1
    delta0[i, v] = 1

fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
dark_bg = '#1a1a2e'
grid_color = '#333'
tick_color = '#aaa'
text_color = '#ddd'

# ============================================================
# Panel 1: The δ matrix
# ============================================================
ax1 = axes[0]
ax1.set_facecolor(dark_bg)
for s in ax1.spines.values():
    s.set_edgecolor(grid_color); s.set_linewidth(0.5)

im1 = ax1.imshow(delta0, cmap='RdBu_r', vmin=-1.5, vmax=1.5, aspect='auto')

ax1.set_xticks(range(4))
ax1.set_yticks(range(4))
ax1.set_xticklabels([r'$c_0$', r'$c_1$', r'$c_2$', r'$c_3$'], color=tick_color)
ax1.set_yticklabels([r'$e_{01}$', r'$e_{12}$', r'$e_{23}$', r'$e_{30}$'], color=tick_color)
ax1.set_title(r'$\delta_0$: 0-cochains $\to$ 1-cochains', color=text_color, fontsize=11)

# Fill in matrix values
for i in range(4):
    for j in range(4):
        if abs(delta0[i,j]) > 0:
            ax1.text(j, i, str(int(delta0[i,j])), ha='center', va='center',
                    color='white', fontsize=12, fontweight='bold')

cbar = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
cbar.ax.tick_params(colors=tick_color, labelsize=7)

# ============================================================
# Panel 2: Kernel vs Image decomposition
# ============================================================
ax2 = axes[1]
ax2.set_facecolor(dark_bg)
for s in ax2.spines.values():
    s.set_edgecolor(grid_color); s.set_linewidth(0.5)

# Two horizontal bands: kernel (top) and image (bottom)
# Kernel: constants → 0
# Image: non-constant cochains → coboundaries

y_kern = 0.7
y_img = 0.3

# Kernel region
rect_k = FancyBboxPatch((0.05, y_kern-0.08), 0.9, 0.12,
                         boxstyle="round,pad=0.02",
                         edgecolor='#e74c3c', facecolor='#e74c3c15', linewidth=1.5)
ax2.add_patch(rect_k)
ax2.text(0.5, y_kern+0.04, r'$\ker(\delta_0)$', ha='center', color='#e74c3c', fontsize=11)
ax2.text(0.5, y_kern-0.02, r'constant cochains $\to$ 0', ha='center', color='#e74c3c', fontsize=8)

# Arrow showing the map
ax2.annotate('', xy=(0.5, y_kern-0.12), xytext=(0.5, y_kern-0.08),
            arrowprops=dict(arrowstyle='->', color='#888', lw=1.5))
ax2.text(0.65, y_kern-0.1, '0', ha='left', color='#e74c3c', fontsize=10, fontweight='bold')

# Image region
rect_i = FancyBboxPatch((0.05, y_img-0.08), 0.9, 0.12,
                         boxstyle="round,pad=0.02",
                         edgecolor='#2ecc71', facecolor='#2ecc7115', linewidth=1.5)
ax2.add_patch(rect_i)
ax2.text(0.5, y_img+0.04, r'$\operatorname{im}(\delta_0)$', ha='center', color='#2ecc71', fontsize=11)
ax2.text(0.5, y_img-0.02, r'coboundaries $\subset C^1$', ha='center', color='#2ecc71', fontsize=8)

# Example input → output
ax2.text(0.05, 0.1, r'$\delta_0[1,0,-1,0] = [-1,1,-1,0]$', ha='left', color='#f39c12', fontsize=9)
ax2.text(0.05, 0.04, r'$\operatorname{rank}(\delta_0) = 3$', ha='left', color='#888', fontsize=8)
ax2.text(0.05, 0.0, r'$\dim\ker = 1$', ha='left', color='#e74c3c', fontsize=8)
ax2.text(0.05, -0.04, r'$4 - 1 = 3$', ha='left', color='#888', fontsize=8)

ax2.set_xlim(0, 1)
ax2.set_ylim(-0.06, 1)
ax2.set_title('Kernel and image', color=text_color, fontsize=11)
ax2.axis('off')

# ============================================================
# Panel 3: Same δ, different inputs
# ============================================================
ax3 = axes[2]
ax3.set_facecolor(dark_bg)
for s in ax3.spines.values():
    s.set_edgecolor(grid_color); s.set_linewidth(0.5)

# Show: the operator δ is the same, what changes is the cochain
# Three examples flowing through δ

examples = [
    ('[1,1,1,1]', r'$\to\ 0$', '#e74c3c'),     # constant
    ('[1,0,0,0]', r'$\to\ \delta_0$', '#3498db'), # basis vector
    ('[1,-1,1,-1]', r'$\to\ \delta_{\text{osc}}$', '#2ecc71'), # alternating
]

for i, (inp, out, col) in enumerate(examples):
    y = 0.75 - i * 0.25

    # Input label
    ax3.text(0.1, y, inp, ha='left', va='center', color=col, fontsize=9,
            family='monospace')

    # δ operator
    ax3.text(0.35, y, r'$\delta$', ha='center', va='center',
            color='#f39c12', fontsize=14, fontweight='bold')

    # Output label
    ax3.text(0.65, y, out, ha='center', va='center', color=col, fontsize=9)

    # Arrow
    ax3.annotate('', xy=(0.28, y), xytext=(0.18, y),
                arrowprops=dict(arrowstyle='->', color=col, lw=1, alpha=0.5))
    ax3.annotate('', xy=(0.6, y), xytext=(0.42, y),
                arrowprops=dict(arrowstyle='->', color=col, lw=1, alpha=0.5))

# Bottom caption
ax3.text(0.5, 0.05,
        'the coboundary is the choice of boundary\nthe operator never changes — the cochain does',
        ha='center', va='center', color='#aaa', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#222244', edgecolor='#555', linewidth=0.5))

ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.set_title(r'$\delta$ is constant. Cochains vary.', color=text_color, fontsize=11)
ax3.axis('off')

plt.tight_layout(rect=[0, 0.02, 1, 0.95])
plt.savefig('coboundary-operator-01.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"Saved coboundary-operator-01.png")
print(f"δ₀:\n{delta0}")
print(f"rank = {np.linalg.matrix_rank(delta0)}")
print(f"ker(δ₀) · [1,1,1,1] = {delta0 @ np.ones(4)}")
