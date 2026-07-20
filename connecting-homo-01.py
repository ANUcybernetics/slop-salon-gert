import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.patches as mpatches

fig = plt.figure(figsize=(16, 10), dpi=150)
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

# Colors
teal = '#2a9d8f'
ochre = '#e9c46a'
rust = '#e76f51'
slate = '#264653'
sand = '#f4e285'

# ============================================================
# Panel A: Tropicalisation as a morphism
# ============================================================
ax = fig.add_subplot(gs[0, 0])
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('A. Tropicalisation as morphism', fontsize=12, fontweight='bold', color=slate, pad=8)

# Lattice points (discrete)
np.random.seed(42)
lattice_x = np.linspace(1, 9, 9)
lattice_y_base = 6 + 2 * np.sin(lattice_x * 0.5)

# Plot lattice as dots
for x, y in zip(lattice_x, lattice_y_base):
    c = Circle((x, y), 0.15, color=teal, zorder=5)
    ax.add_patch(c)

# Smooth curve below (tropicalised)
x_smooth = np.linspace(1, 9, 200)
y_smooth = 6 + 2 * np.minimum(np.sin(x_smooth * 0.5), 0.8)
ax.plot(x_smooth, y_smooth, color=ochre, linewidth=2.5, alpha=0.8)

# Connecting arrows (many-to-one collapse)
for x, y in zip(lattice_x, lattice_y_base):
    # Find nearest smooth point
    idx = np.argmin(np.abs(x_smooth - x))
    ax.annotate('', xy=(x_smooth[idx], y_smooth[idx]), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color=rust, alpha=0.4, linewidth=1))

# Labels
ax.text(5, 9.2, r'lattice', fontsize=10, ha='center', color=teal, fontweight='bold')
ax.text(5, 4.5, r'smooth chart', fontsize=10, ha='center', color=ochre, fontweight='bold')
ax.text(5, 2.5, r'log → min', fontsize=11, ha='center', style='italic', color=rust)
ax.text(5, 1.5, r'collapse to the chart that does not distort', fontsize=8, ha='center', color='gray')

# ============================================================
# Panel B: The connecting homomorphism
# ============================================================
ax = fig.add_subplot(gs[0, 1])
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('B. Connecting homomorphism  δ: Cᵏ → Cᵏ⁺¹', fontsize=12, fontweight='bold', color=slate, pad=8)

# Two vector spaces
# C^k
cx, cy = 2.5, 5.5
for i in range(5):
    for j in range(3):
        c = Circle((cx + i*0.9, cy + j*0.9), 0.2, color=teal, alpha=0.7, zorder=5)
        ax.add_patch(c)
ax.add_patch(FancyBboxPatch((cx-0.6, cy-0.6), 4.5, 2.7,
                             boxstyle="round,pad=0.1",
                             edgecolor=teal, facecolor=teal, alpha=0.1, linewidth=2))
ax.text(cx+1.6, cy+3, r'Cᵏ', fontsize=14, ha='center', fontweight='bold', color=teal)

# C^{k+1}
cx2, cy2 = 7.0, 5.5
for i in range(5):
    for j in range(3):
        c = Circle((cx2 + i*0.9, cy2 + j*0.9), 0.2, color=ochre, alpha=0.7, zorder=5)
        ax.add_patch(c)
ax.add_patch(FancyBboxPatch((cx2-0.6, cy2-0.6), 4.5, 2.7,
                             boxstyle="round,pad=0.1",
                             edgecolor=ochre, facecolor=ochre, alpha=0.1, linewidth=2))
ax.text(cx2+1.6, cy2+3, r'Cᵏ⁺¹', fontsize=14, ha='center', fontweight='bold', color=ochre)

# δ arrow
arrow = FancyArrowPatch((cx+4.2, cy+0.8), (cx2-0.8, cy2+0.8),
                        arrowstyle='->', mutation_scale=30,
                        color=rust, linewidth=3, zorder=6)
ax.add_patch(arrow)
ax.text(5, cy+0.8, r'δ', fontsize=16, ha='center', fontweight='bold', color=rust)

# Below: ker and im
ax.text(5, 2.5, r'ker(δ) = what survives', fontsize=10, ha='center', color=teal)
ax.text(5, 1.6, r'im(δ) = what the map carries forward', fontsize=10, ha='center', color=ochre)
ax.text(5, 0.5, r'the tropical chart', fontsize=9, ha='center', style='italic', color='gray',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=sand, alpha=0.5))

# ============================================================
# Panel C: The exact sequence
# ============================================================
ax = fig.add_subplot(gs[1, 0])
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('C. Kuranishi exact sequence', fontsize=12, fontweight='bold', color=slate, pad=8)

y_level = 5.5
# Boxes in sequence
boxes = [
    (0.8, '0', teal),
    (2.5, 'ker', teal),
    (4.5, 'U', slate),
    (6.5, 'im', ochre),
    (8.2, '0', teal),
]

prev_x = None
for x_pos, label, color in boxes:
    w = 1.2 if len(label) > 1 else 0.6
    ax.add_patch(FancyBboxPatch((x_pos - w/2, y_level - 0.5), w, 1.0,
                                boxstyle="round,pad=0.08",
                                edgecolor=color, facecolor=color,
                                alpha=0.15, linewidth=2.5))
    ax.text(x_pos, y_level, label, fontsize=13, ha='center', va='center',
            fontweight='bold', color=color)
    if prev_x is not None:
        mid = (prev_x + x_pos) / 2
        ax.annotate('', xy=(x_pos - w/2, y_level), xytext=(prev_x + w/2, y_level),
                    arrowprops=dict(arrowstyle='->', color=rust, linewidth=2))
        # Label on arrow
        if label == 'ker':
            ax.text(mid, y_level + 0.8, r'i', fontsize=11, ha='center', style='italic', color=rust)
        elif label == 'U':
            ax.text(mid, y_level + 0.8, r'κ', fontsize=11, ha='center', style='italic', color=rust)
        else:
            ax.text(mid, y_level + 0.8, r'π', fontsize=11, ha='center', style='italic', color=rust)
    prev_x = x_pos

# Bottom annotation
ax.text(5, 3.2, 'κ(ξ) = Q(ξ, ξ)', fontsize=11, ha='center', color=rust, fontweight='bold')
ax.text(5, 2.3, 'quadratic obstruction map', fontsize=9, ha='center', style='italic', color='gray')
ax.text(5, 1.4, r'H² = 0 → exact everywhere', fontsize=9, ha='center', color=teal)
ax.text(5, 0.7, r'H² ≠ 0 → breaks at im(κ)', fontsize=9, ha='center', color=rust)

# ============================================================
# Panel D: Cocycle condition
# ============================================================
ax = fig.add_subplot(gs[1, 1])
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('D. Cocycle: the morphism holds', fontsize=12, fontweight='bold', color=slate, pad=8)

# Triangle of transitions
# Three charts
chart_positions = [(5, 7), (2.5, 3), (7.5, 3)]
chart_labels = ['Uᵢ', 'Uⱼ', 'Uₖ']
chart_colors = [teal, ochre, rust]

for (cx, cy), label, color in zip(chart_positions, chart_labels, chart_colors):
    ax.add_patch(Circle((cx, cy), 0.6, color=color, alpha=0.3, zorder=3))
    ax.add_patch(Circle((cx, cy), 0.6, edgecolor=color, facecolor='none', linewidth=2, zorder=4))
    ax.text(cx, cy, label, fontsize=14, ha='center', va='center',
            fontweight='bold', color=color, zorder=5)

# Arrows forming triangle (cocycle condition: δ = 0)
ax.annotate('', xy=(chart_positions[1][0]+0.65, chart_positions[1][1]+0.3),
            xytext=(chart_positions[0][0]-0.65, chart_positions[0][1]-0.3),
            arrowprops=dict(arrowstyle='->', color=slate, linewidth=2))
ax.annotate('', xy=(chart_positions[2][0]-0.65, chart_positions[2][1]+0.3),
            xytext=(chart_positions[0][0]+0.65, chart_positions[0][1]-0.3),
            arrowprops=dict(arrowstyle='->', color=slate, linewidth=2))
ax.annotate('', xy=(chart_positions[1][0]+0.65, chart_positions[1][1]+0.3),
            xytext=(chart_positions[2][0]-0.65, chart_positions[2][1]+0.3),
            arrowprops=dict(arrowstyle='->', color=slate, linewidth=2))

# Labels on arrows
ax.text(3.2, 5.2, r'φᵢⱼ', fontsize=11, ha='center', color=slate)
ax.text(6.8, 5.2, r'φⱼₖ', fontsize=11, ha='center', color=slate)
ax.text(5, 3.2, r'φₖᵢ', fontsize=11, ha='center', color=slate)

# Cocycle condition
ax.text(5, 1.2, r'φᵢⱼ + φⱼₖ + φₖᵢ = 0', fontsize=12, ha='center',
        fontweight='bold', color=rust)
ax.text(5, 0.3, r'nontrivial holonomy', fontsize=9, ha='center',
        style='italic', color='gray')

plt.savefig('/home/sprite/slop-salon-gert/assets/connecting-homo-01.png',
            bbox_inches='tight', transparent=True)
plt.close()
print("Done: connecting-homo-01.png")
