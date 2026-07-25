#!/usr/bin/env python3
"""Regular rep of S3: clean 2-panel showing decomposition."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# S3
elems = [
    (0, 1, 2), (1, 0, 2), (2, 1, 0),
    (0, 2, 1), (1, 2, 0), (2, 0, 1),
]

def mult(a, b):
    return tuple(a[i] for i in b)

# Regular rep character
regular_char = np.array([6, 0, 0])

# Character table
irreps = ['triv', 'sign', 'std']
chi = np.array([
    [1,  1,  1],
    [1, -1,  1],
    [2,  0, -1],
])
class_sizes = np.array([1, 3, 2])

print("Decomposition of regular rep:")
for i, r in enumerate(irreps):
    n_r = sum(class_sizes[j] * regular_char[j] * chi[i, j] for j in range(3)) / 6
    print(f"  ρ_reg = ... ⊕ {n_r:.0f} · {r}  (dim = {chi[i, 0]:.0f})")

# Layout
elem_labels = ['e', '(12)', '(13)', '(23)', '(123)', '(132)']
angles = np.linspace(0, 2*np.pi, 7)[:-1] + np.pi/6
positions = np.column_stack([np.cos(angles), np.sin(angles)])

s_gen = (1, 0, 2)  # (12)
t_gen = (1, 2, 0)  # (123)

swap_color = '#e76f51'
cycle_color = '#2a9d8f'

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

# Panel 1: Directed Cayley graph
ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-1.6, 1.4)
ax1.set_aspect('equal')

for j in range(6):
    src = positions[j]
    tgt_s = mult(s_gen, elems[j])
    tgt_t = mult(t_gen, elems[j])
    i_s = elems.index(tgt_s)
    i_t = elems.index(tgt_t)

    dx_s = positions[i_s, 0] - src[0]
    dy_s = positions[i_s, 1] - src[1]
    ax1.annotate('', xy=(positions[i_s, 0] + 0.1*dx_s, positions[i_s, 1] + 0.1*dy_s),
                xytext=(src[0] + 0.1*dx_s, src[1] + 0.1*dy_s),
                arrowprops=dict(arrowstyle='->', color=swap_color, lw=2, alpha=0.45,
                               connectionstyle='arc3,rad=0.15'))

    dx_t = positions[i_t, 0] - src[0]
    dy_t = positions[i_t, 1] - src[1]
    ax1.annotate('', xy=(positions[i_t, 0] + 0.1*dx_t, positions[i_t, 1] + 0.1*dy_t),
                xytext=(src[0] + 0.1*dx_t, src[1] + 0.1*dy_t),
                arrowprops=dict(arrowstyle='->', color=cycle_color, lw=2, alpha=0.45,
                               connectionstyle='arc3,rad=-0.15'))

for i, (x, y) in enumerate(positions):
    ax1.scatter([x], [y], s=280, c='white', edgecolors='#264653', linewidths=2.5, zorder=5)
    ax1.text(x, y, elem_labels[i], ha='center', va='center', fontsize=11, fontweight='bold', zorder=6)

# Legend
ax1.text(-1.5, -1.45, 's=(12)  ', transform=ax1.transAxes,
        ha='left', fontsize=11, color=swap_color, fontweight='bold')
ax1.text(-1.5, -1.58, 't=(123)  ', transform=ax1.transAxes,
        ha='left', fontsize=11, color=cycle_color, fontweight='bold')

ax1.set_title('Left regular action: S₃ on itself\nf ↦ f(g⁻¹x) — generators act by translation',
             fontsize=12, pad=10)
ax1.axis('off')

# Panel 2: Decomposition
ax2.axis('off')

lines = [
    'Regular rep: ρ_reg(g) permutes',
    'basis vectors indexed by group elements.',
    '',
    'Decomposition:',
    '',
    '  ρ_reg = triv ⊕ sign ⊕ std ⊕ std',
    '',
    '  dim:     1      +   1    +   2    +   2',
    '',
    '  χ_reg(x) = |G| if x=e',
    '           = 0   if x≠e',
    '',
    '  — δ-function on the group',
    '  — trace "forgets" everything',
    '    except whether g = e',
    '',
    '  The trace IS coarse-graining:',
    '  every group element apart from',
    '  the identity becomes indistinguishable.',
]
ax2.text(0.06, 0.95, '\n'.join(lines), fontsize=11.5, family='monospace',
        verticalalignment='top', transform=ax2.transAxes)
ax2.set_title('χ_reg = δₑ·|G| — coarse-graining on the group',
             fontsize=12, pad=10)

fig.savefig('assets/regular-rep-01.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: assets/regular-rep-01.png")
