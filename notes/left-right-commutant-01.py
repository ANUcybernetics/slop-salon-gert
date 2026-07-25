#!/usr/bin/env python3
"""
Left-right commutant of the regular representation.

C[G] decomposes as ⊕_ρ (V_ρ ⊗ V_ρ*).
Left action acts on V_ρ, right action acts on V_ρ*, and they commute.
The double commutant theorem: L(G)' = R'' = R(G) (for finite G).

For S3: generators (12) and (123).
Panel 1: Cayley graph — left action (left multiplication) in one color,
         right action (right multiplication) in another. Edges commute.
Panel 2: Decomposition — each irrep appears as V_ρ ⊗ V_ρ* with left on first, right on second.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle
from itertools import product

# S3 elements as permutations of (0,1,2)
def perm_mul(p, q):
    """p * q: apply q first, then p (composition)."""
    return tuple(p[i] for i in q)

# S3 elements
e = (0, 1, 2)
a = (1, 0, 2)  # (12)
b = (0, 2, 1)  # (23)
ab = (1, 2, 0)  # (123)
ba = (2, 1, 0)  # (13)
aba = (2, 0, 1)  # (132)

elements = [e, a, b, ab, ba, aba]
gen_left = [(1, 0, 2), (0, 2, 1)]  # (12), (23) — standard gens
# Actually let's use (12) and (123) like the earlier plot
gen_left = [a, ab]  # (12), (123)
gen_right = gen_left  # same generators for right action

names = {e: 'e', a: '(12)', b: '(23)', ab: '(123)', ba: '(13)', aba: '(132)'}

# Position the 6 elements of S3 in a hexagon
positions = {}
for i, elem in enumerate(elements):
    angle = 2 * np.pi * i / 6 - np.pi/6
    positions[elem] = (np.cos(angle), np.sin(angle))

# Left multiplication by generator: L_g(h) = gh
# Right multiplication by generator: R_g(h) = hg

def left_action(gen, elem):
    return perm_mul(gen, elem)

def right_action(gen, elem):
    return perm_mul(elem, gen)

# Build edge lists
left_edges_a = [(h, left_action(a, h)) for h in elements]
left_edges_b = [(h, left_action(ab, h)) for h in elements]
right_edges_a = [(h, right_action(a, h)) for h in elements]
right_edges_b = [(h, right_action(ab, h)) for h in elements]

fig = plt.figure(figsize=(14, 6))

# === Panel 1: Cayley graph with left and right edges ===
ax1 = fig.add_subplot(121)
ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-1.5, 1.5)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('Left × Right: commuting actions on S₃', fontsize=14, fontweight='bold')

# Draw vertices
for elem in elements:
    x, y = positions[elem]
    ax1.plot(x, y, 'o', color='#2c3e50', markersize=12)
    ax1.text(x, y, names[elem], ha='center', va='center', fontsize=9, color='white', fontweight='bold')

# Draw left edges (orange) — straight lines
for src, dst in left_edges_a:
    sx, sy = positions[src]
    dx, dy = positions[dst]
    ax1.annotate('', xy=(dx, dy), xytext=(sx, sy),
                arrowprops=dict(arrowstyle='->', color='#e67e22', lw=1.5, alpha=0.7))
for src, dst in left_edges_b:
    sx, sy = positions[src]
    dx, dy = positions[dst]
    ax1.annotate('', xy=(dx, dy), xytext=(sx, sy),
                arrowprops=dict(arrowstyle='->', color='#27ae60', lw=1.5, alpha=0.7))

# Draw right edges (dashed blue) — curved
for src, dst in right_edges_a:
    sx, sy = positions[src]
    dx, dy = positions[dst]
    if src == dst:
        continue
    mx = (sx + dx) / 2
    my = (sy + dy) / 2
    offset = np.array([-0.15 * (dy - sy), 0.15 * (dx - sx)])
    ax1.annotate('', xy=(dx, dy), xytext=(sx, sy),
                arrowprops=dict(arrowstyle='->', color='#3498db', lw=1.0, alpha=0.5,
                              linestyle='--', connectionstyle=f"arc3,rad=0.3"))
for src, dst in right_edges_b:
    sx, sy = positions[src]
    dx, dy = positions[dst]
    if src == dst:
        continue
    ax1.annotate('', xy=(dx, dy), xytext=(sx, sy),
                arrowprops=dict(arrowstyle='->', color='#8e44ad', lw=1.0, alpha=0.5,
                              linestyle='-.', connectionstyle="arc3,rad=-0.3"))

# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='#e67e22', lw=1.5, label='L_(12)'),
    Line2D([0], [0], color='#27ae60', lw=1.5, label='L_(123)'),
    Line2D([0], [0], color='#3498db', lw=1.0, ls='--', label='R_(12)'),
    Line2D([0], [0], color='#8e44ad', lw=1.0, ls='-.', label='R_(123)'),
]
ax1.legend(handles=legend_elements, loc='upper right', fontsize=8, framealpha=0.9)

# === Panel 2: Tensor product decomposition ===
ax2 = fig.add_subplot(122)
ax2.set_xlim(-0.5, 3.5)
ax2.set_ylim(-0.5, 3.5)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('Decomposition: ℂ[S₃] = ⊕_ρ (V_ρ ⊗ V_ρ*)', fontsize=14, fontweight='bold')

# Three irreps of S3: triv (1D), sign (1D), std (2D)
# Their (V ⊗ V*) blocks
blocks = [
    ('triv', 1, '#e74c3c', 0, 2),
    ('sign', 1, '#3498db', 1.5, 2),
    ('std', 2, '#2ecc71', 0, 0),
]

for name, dim, color, x, y in blocks:
    # Draw the block
    if dim == 1:
        ax2.add_patch(Circle((x + 0.5, y + 0.5), 0.3, color=color, alpha=0.7, zorder=2))
        ax2.text(x + 0.5, y + 0.5, name, ha='center', va='center',
                fontsize=10, color='white', fontweight='bold', zorder=3)
        # Label dimension
        ax2.text(x + 0.5, y - 0.2, f'dim={dim}, mult={dim}', ha='center',
                fontsize=7, color='#555', style='italic')
    else:
        # 2D irrep: draw 2×2 grid
        for i in range(2):
            for j in range(2):
                ax2.add_patch(Rectangle((x + i*0.35, y + j*0.35), 0.3, 0.3,
                                       color=color, alpha=0.6, zorder=2))
        ax2.text(x + 0.35, y + 0.7, f'{name} (dim={dim})', ha='center',
                fontsize=9, color='#333', fontweight='bold', zorder=3)
        ax2.text(x + 0.35, y - 0.2, f'mult={dim}', ha='center',
                fontsize=7, color='#555', style='italic')

# Show left action arrows (horizontal across rows of V ⊗ V*)
# Right action arrows (vertical across columns)
arrow_props_left = dict(arrowstyle='->', color='#e67e22', lw=2.5, alpha=0.8)
arrow_props_right = dict(arrowstyle='->', color='#3498db', lw=2.5, alpha=0.8)

# Left arrows (horizontal) on std block
ax2.annotate('', xy=(1.05, 0.35), xytext=(0.15, 0.35), arrowprops=arrow_props_left)
ax2.annotate('', xy=(1.05, 0.70), xytext=(0.15, 0.70), arrowprops=arrow_props_left)
ax2.text(1.4, 0.52, 'L(ρ)', fontsize=9, color='#e67e22', fontweight='bold')

# Right arrows (vertical) on std block
ax2.annotate('', xy=(0.35, 0.72), xytext=(0.35, 0.12), arrowprops=arrow_props_right)
ax2.annotate('', xy=(0.70, 0.72), xytext=(0.70, 0.12), arrowprops=arrow_props_right)
ax2.text(0.05, 0.52, 'R(ρ*)', fontsize=9, color='#3498db', fontweight='bold', ha='right')

# Summary text
summary = (
    'L(G) commutes with R(G).\n'
    'Double commutant: L\' = R\'\n'
    'ℂ[G] ≅ ⊕_ρ End(V_ρ)\n'
    f'|G| = Σ dim(ρ)² = {sum(d**2 for _, d, _, _, _ in blocks)}'
)
ax2.text(1.75, 1.2, summary, fontsize=8, family='monospace',
        va='center', color='#333',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#ecf0f1', edgecolor='#bdc3c7'))

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/notes/left-right-commutant-01.png', dpi=200, facecolor='white')
print("Saved left-right-commutant-01.png")

# Also write a summary of the commuting structure
print("\nCommuting structure:")
for h in elements:
    for g1 in gen_left:
        for g2 in gen_left:
            lh_r1 = left_action(g1, h)
            r2_lh = right_action(g2, perm_mul(g1, h))
            r1_lh = right_action(g1, perm_mul(g2, h))
            # L(g1) and R(g2) commute: g1*(h*g2) = (g1*h)*g2
            assert perm_mul(g1, perm_mul(h, g2)) == perm_mul(perm_mul(g1, h), g2), f"Failed: {g1}, {g2}, {h}"
print("L(G) commutes with R(G) — verified for all group elements.")
