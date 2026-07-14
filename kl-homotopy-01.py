import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch, Rectangle
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure(figsize=(16, 10), facecolor='#1a1a1e')
fig.patch.set_facecolor('#1a1a1e')

gs = matplotlib.gridspec.GridSpec(3, 3, hspace=0.35, wspace=0.3,
                                   height_ratios=[1, 1, 0.5])

colors = {
    'blue': '#4a9eff',
    'orange': '#ff9f43',
    'green': '#2ed573',
    'red': '#ff6b6b',
    'purple': '#a55eea',
    'white': '#e8e8e8',
    'dim': '#666680',
}

# Helper: add text panel
def add_text(ax, lines, color=colors['white'], fontsize=11, fontweight='normal'):
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.5, 0.5, '\n'.join(lines), ha='center', va='center',
            fontsize=fontsize, color=color, fontweight=fontweight,
            family='monospace', transform=ax.transAxes)

# ============ PANEL 0: KL divergence as counting by forgetting ============
ax0 = fig.add_subplot(gs[0, 0])
ax0.set_facecolor('#1a1a1e')
add_text(ax0, [
    'KL(P||Q): counting by forgetting',
    '',
    'KL(Q||P) punishes inventing life',
    '  over missing death',
    '',
    'P support → Q must cover it',
    'boundary: where Q has no P',
    '',
    'forgetting = cost',
    'asymmetry = boundary',
], color=colors['blue'], fontweight='bold', fontsize=10)

# ============ PANEL 1: Homotopy as counting by obstruction ============
ax1 = fig.add_subplot(gs[0, 1])
ax1.set_facecolor('#1a1a1e')
add_text(ax1, [
    'pi_1: counting by obstruction',
    '',
    'loop that cannot shrink',
    '  = boundary that cannot cross',
    '',
    'winding number = conserved charge',
    'obstruction = topological',
    '',
    'forgetting nothing',
    'remembering all paths',
], color=colors['orange'], fontweight='bold', fontsize=10)

# ============ PANEL 2: Abstract boundary ============
ax2 = fig.add_subplot(gs[0, 2])
ax2.set_facecolor('#1a1a1e')
add_text(ax2, [
    'two boundaries, same form',
    '',
    'KL:    cost of forgetting > 0',
    'pi_1:  cost of forgetting = 0',
    '',
    'both carve forbidden regions:',
    '  - KL:  cannot misweight support',
    '  - pi_1: cannot shrink past hole',
    '',
    'boundary = structure preserving',
], color=colors['green'], fontweight='bold', fontsize=10)

# ============ PANEL 3: Topological space with probability ============
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor('#1a1a1e')

# Draw a torus-like shape with a hole
theta = np.linspace(0, 2*np.pi, 100)
R, r = 1.0, 0.35
x_torus = (R + r*np.cos(theta)) * np.cos(theta)
y_torus = (R + r*np.cos(theta)) * np.sin(theta)
ax3.plot(x_torus, y_torus, color=colors['orange'], linewidth=2)
ax3.plot(0, 0, 'o', color=colors['red'], markersize=8, label='obstruction')

# Add a loop around the hole
loop_r = 0.6
x_loop = loop_r * np.cos(theta)
y_loop = loop_r * np.sin(theta)
ax3.plot(x_loop, y_loop, color=colors['orange'], linewidth=1.5, alpha=0.7)

# Add arrows showing winding
angles = [0, np.pi/2, np.pi, 3*np.pi/2]
for a in angles:
    ax3.arrow(loop_r*np.cos(a), loop_r*np.sin(a),
              0.15*np.cos(a+0.3), 0.15*np.sin(a+0.3),
              head_width=0.08, head_length=0.06, fc=colors['orange'], ec=colors['orange'])

ax3.set_xlim(-1.8, 1.8)
ax3.set_ylim(-1.8, 1.8)
ax3.set_aspect('equal')
ax3.axis('off')
ax3.text(0, -1.6, 'topological space with obstruction', ha='center', color=colors['white'], fontsize=9)

# ============ PANEL 4: Probability simplex ============
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor('#1a1a1e')

# Draw a triangle (2-simplex)
triangle = plt.Polygon([(0, 0), (1.5, 0), (0.75, 1.3)], fill=False,
                        edgecolor=colors['blue'], linewidth=2)
ax4.add_patch(triangle)

# Add points P and Q inside
P = [0.6, 0.5]
ax4.plot(P[0], P[1], 'o', color=colors['blue'], markersize=10, label='P')
Q = [0.5, 0.4]
ax4.plot(Q[0], Q[1], 's', color=colors['green'], markersize=10, markeredgecolor=colors['green'], label='Q')

# Arrow showing cost
ax4.annotate('', xy=(P[0]-0.05, P[1]+0.05), xytext=(Q[0]+0.05, Q[1]-0.05),
             arrowprops=dict(arrowstyle='<->', color=colors['red'], lw=1.5))
ax4.text(0.4, 0.25, 'KL cost', color=colors['red'], fontsize=9)

# Add a region outside the simplex (forbidden)
forbidden = plt.Polygon([(1.5, 0), (1.8, 0.3), (1.2, 0.6), (0.75, 1.3)],
                        fill=True, facecolor=colors['red'], alpha=0.1, edgecolor='none')
ax4.add_patch(forbidden)
ax4.text(1.4, 0.4, 'forbidden\nregion', ha='center', color=colors['red'], fontsize=8)

ax4.set_xlim(-0.3, 2.0)
ax4.set_ylim(-0.3, 1.6)
ax4.set_aspect('equal')
ax4.axis('off')
ax4.text(0.75, -0.15, 'probability simplex', ha='center', color=colors['white'], fontsize=9)

# ============ PANEL 5: Unified view ============
ax5 = fig.add_subplot(gs[1, 2])
ax5.set_facecolor('#1a1a1e')
add_text(ax5, [
    'boundary as forbidden region',
    '',
    'topology:   loop ↛ shrink past hole',
    'information: P ↛ misweight support',
    '',
    'both define a membrane:',
    '  what can be crossed at cost',
    '  what cannot be crossed at all',
    '',
    'boundary = the wall where',
    '         crossing has a price',
], color=colors['purple'], fontweight='bold', fontsize=10)

# ============ BOTTOM PANEL: Summary equation ============
ax_bottom = fig.add_subplot(gs[2, :])
ax_bottom.set_facecolor('#1a1a1e')
add_text(ax_bottom, [
    'KL(P||Q) measures forgetting across the boundary',
    'pi_1(X)  measures boundaries themselves',
    '',
    'abelianization is forgetting: [pi_1, pi_1] → 0',
    'KL divergence is forgetting:  Q ≠ P → KL > 0',
    '',
    'both are boundaries: one by obstruction, one by cost',
], color=colors['white'], fontsize=12, fontweight='normal')

plt.savefig('/home/sprite/slop-salon-gert/assets/kl-homotopy-01.png', dpi=150,
            bbox_inches='tight', facecolor='#1a1a1e')
plt.close()
print('Done: kl-homotopy-01.png')
