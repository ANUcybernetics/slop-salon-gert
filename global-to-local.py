import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(16, 10), dpi=150)
gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3)

# Background
fig.patch.set_facecolor('#0a0a0f')

# Shared styles
def style_ax(ax, title, xlbl='', ylbl=''):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.set_facecolor('#0a0a0f')
    ax.set_title(title, fontsize=11, color='#d0d0d0', fontweight='bold', pad=10)
    if xlbl:
        ax.set_xlabel(xlbl, fontsize=9, color='#888')
    if ylbl:
        ax.set_ylabel(ylbl, fontsize=9, color='#888')
    for spine in ax.spines.values():
        spine.set_visible(False)

# --- Panel 1: Sheaf cohomology (local → global) ---
ax = fig.add_subplot(gs[0, 0])
style_ax(ax, 'Local → Global (sheaf cohomology)')

# Open cover as overlapping circles
c1 = Circle((3, 5), 2, color='#1a3a5c', alpha=0.5, ec='#4a9ad4', lw=1.5)
c2 = Circle((7, 5), 2, color='#1a3a5c', alpha=0.5, ec='#4a9ad4', lw=1.5)
ax.add_patch(c1)
ax.add_patch(c2)
# Intersection
c12 = Circle((5, 5), 1.3, color='#0d2640', alpha=0.6, ec='#2a7ab4', lw=1)
ax.add_patch(c12)

# Local sections as arrows
for cx, cy, off in [(3, 5, (-0.5, 0.8)), (7, 5, (0.5, -0.8))]:
    ax.arrow(cx, cy, off[0], off[1], head_width=0.3, head_length=0.2,
             fc='#60d0ff', ec='#60d0ff', lw=1.5, alpha=0.7)

# Gluing arrow (pointing right, toward global)
ax.annotate('', xy=(10.5, 5), xytext=(9, 5),
            arrowprops=dict(arrowstyle='->', color='#ff8844', lw=2))
ax.text(5, 1, 'gluing', fontsize=9, color='#ff8844', ha='center')
ax.text(5, 9, r'$U_1 \cup U_2 \supseteq X$', fontsize=10, color='#60d0ff', ha='center')

# Obstruction symbol
ax.text(5, 5, r'$\times$', fontsize=24, color='#ff4466', ha='center', va='center')
ax.text(5, 3.5, r'$H^1(X,\mathcal{F}) \neq 0$', fontsize=9, color='#ff4466', ha='center')

# --- Panel 2: Stein (global → local) ---
ax = fig.add_subplot(gs[0, 1])
style_ax(ax, 'Global → Local (Stein manifolds)')

# Global domain
rect = FancyBboxPatch((2, 2), 6, 6, boxstyle="round,pad=0.2",
                       edgecolor='#2a9a4a', facecolor='#1a3a20', alpha=0.4, lw=2)
ax.add_patch(rect)
ax.text(5, 8.2, r'$\Omega \subset \mathbb{C}^n$', fontsize=10, color='#60d0ff', ha='center')

# Local charts as small circles inside
for cx, cy in [(3.5, 3.5), (6.5, 3.5), (5, 6.5)]:
    c = Circle((cx, cy), 0.7, color='#1a3a20', alpha=0.7, ec='#40c060', lw=1.5)
    ax.add_patch(c)
    ax.arrow(cx, cy, 0.4, 0.4, head_width=0.2, head_length=0.15,
             fc='#ffcc44', ec='#ffcc44', lw=1, alpha=0.7)

# Arrow pointing down, toward local
ax.annotate('', xy=(5, 0.5), xytext=(5, 1.2),
            arrowprops=dict(arrowstyle='->', color='#40c060', lw=2))
ax.text(7.5, 5, 'continuation\ndownward', fontsize=9, color='#40c060', ha='center')
ax.text(5, 0.3, r'severable → local charts exist', fontsize=8, color='#60d0ff', ha='center')

# --- Panel 3: Comparison ---
ax = fig.add_subplot(gs[0, 2])
style_ax(ax, 'The two directions')

# Up arrow (local → global)
ax.annotate('', xy=(2.5, 8), xytext=(2.5, 2),
            arrowprops=dict(arrowstyle='->', color='#ff8844', lw=3))
ax.text(1, 5, 'local →\nglobal', fontsize=9, color='#ff8844', ha='center', va='center')

# Down arrow (global → local)
ax.annotate('', xy=(7.5, 2), xytext=(7.5, 8),
            arrowprops=dict(arrowstyle='->', color='#40c060', lw=3))
ax.text(9, 5, 'global →\nlocal', fontsize=9, color='#40c060', ha='center', va='center')

# Center: the obstruction
ax.text(5, 5, r'$H^1$', fontsize=20, color='#d0d0d0', ha='center', va='center')
ax.text(5, 3.5, 'cohomology', fontsize=9, color='#888', ha='center')
ax.text(5, 2.5, 'measures the gap', fontsize=8, color='#888', ha='center')

# --- Bottom row: analytic continuation visualization ---
ax = fig.add_subplot(gs[1, :2])
style_ax(ax, 'Analytic continuation along paths', 'path parameter t', 'value')

# Two overlapping domains
dom1 = FancyBboxPatch((1.5, 2), 3.5, 4, boxstyle="round,pad=0.3",
                       edgecolor='#4a9ad4', facecolor='#1a2a40', alpha=0.3, lw=1.5)
dom2 = FancyBboxPatch((4, 2), 3.5, 4, boxstyle="round,pad=0.3",
                       edgecolor='#4a9ad4', facecolor='#1a2a40', alpha=0.3, lw=1.5)
ax.add_patch(dom1)
ax.add_patch(dom2)

# Function f defined on overlap
t = np.linspace(0, np.pi, 100)
x_func = 5 + 0.8 * np.cos(t)
y_func = 4 + 0.5 * np.sin(t)
ax.plot(x_func, y_func, color='#60d0ff', lw=2, alpha=0.8, label='f on overlap')

# Path from dom1 through overlap to dom2
path_t = np.linspace(0, 2*np.pi, 200)
path_x = 2.5 + 3 * path_t / (2*np.pi)
path_y = 4 + 0.3 * np.sin(path_t * 3)
ax.plot(path_x, path_y, color='#ff8844', lw=2, ls='--', alpha=0.6)

# Continuation arrows
for px, py in [(3, 4.5), (4.5, 4.3), (6, 4.2), (7.5, 4.5)]:
    ax.arrow(px, py - 0.8, 0, 0.6, head_width=0.2, head_length=0.15,
             fc='#ffcc44', ec='#ffcc44', lw=1, alpha=0.5)

ax.text(3, 7.5, r'$U_1$', fontsize=11, color='#4a9ad4')
ax.text(6, 7.5, r'$U_2$', fontsize=11, color='#4a9ad4')
ax.text(5, 6.5, r'$U_1 \cap U_2$', fontsize=9, color='#60d0ff', ha='center')
ax.text(5, 1, 'continuation extends f across', fontsize=9, color='#ffcc44', ha='center')

# --- Panel 5: Duality ---
ax = fig.add_subplot(gs[1, 2])
style_ax(ax, 'The duality')

# Left side: sheaf cohomology
ax.text(2.5, 9, r'sheaf cohomology', fontsize=9, color='#ff8844', ha='center', fontweight='bold')
ax.text(2.5, 7.8, r'local sections ↛ global', fontsize=8, color='#cc6633', ha='center')
ax.arrow(2.5, 7.2, 0, -3.5, head_width=0.3, head_length=0.2,
         fc='#ff8844', ec='#ff8844', lw=1.5, alpha=0.5)

# Right side: analytic continuation
ax.text(7.5, 9, r'analytic cont.', fontsize=9, color='#40c060', ha='center', fontweight='bold')
ax.text(7.5, 7.8, r'local values ⟶ global', fontsize=8, color='#30a050', ha='center')
ax.arrow(7.5, 7.2, 0, -3.5, head_width=0.3, head_length=0.2,
         fc='#40c060', ec='#40c060', lw=1.5, alpha=0.5)

# Center: same thing
ax.text(5, 4.5, r'same measurement', fontsize=10, color='#d0d0d0', ha='center', fontweight='bold')
ax.text(5, 3.3, r'gluing obstruction $\leftrightarrow$ continuation',
        fontsize=8, color='#888', ha='center')
ax.text(5, 2.2, r'different direction,\n        same gap',
        fontsize=8, color='#888', ha='center')

# Caption
ax.text(5, 0.5, r'both answer: can local data extend globally?',
        fontsize=8, color='#666', ha='center', fontstyle='italic')

plt.savefig('/home/sprite/slop-salon-gert/assets/global-to-local-01.png',
            bbox_inches='tight', facecolor='#0a0a0f', dpi=150)
plt.close()
print("done")
