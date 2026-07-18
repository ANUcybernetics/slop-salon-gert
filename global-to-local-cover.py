import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(8, 8), dpi=150)
fig.patch.set_facecolor('#0a0a0f')

gs = GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

def style(ax, title):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.set_facecolor('#0a0a0f')
    ax.set_title(title, fontsize=13, color='#d0d0d0', fontweight='bold', pad=15)
    for s in ax.spines.values():
        s.set_visible(False)

# Top-left: local -> global (obstruction)
ax = fig.add_subplot(gs[0, 0])
style(ax, 'local $\to$ global')
c1 = Circle((3.5, 5), 1.8, color='#1a3a3a5c', alpha=0.5, ec='#4a9ad4', lw=2)
c2 = Circle((6.5, 5), 1.8, color='#1a3a5c', alpha=0.5, ec='#4a9ad4', lw=2)
ax.add_patch(c1)
ax.add_patch(c2)
ax.arrow(3.5, 5, 0, 1.2, head_width=0.35, head_length=0.2,
         fc='#60d0ff', ec='#60d0ff', lw=2, alpha=0.8)
ax.arrow(6.5, 5, 0, -1.2, head_width=0.35, head_length=0.2,
         fc='#60d0ff', ec='#60d0ff', lw=2, alpha=0.8)
ax.text(5, 5, r'$\times$', fontsize=36, color='#ff4466', ha='center', va='center')
ax.text(5, 2.5, r'$H^1 \neq 0$', fontsize=10, color='#ff4466', ha='center')

# Top-right: global -> local (continuation)
ax = fig.add_subplot(gs[0, 1])
style(ax, 'global $\to$ local')
rect = plt.Rectangle((2, 2), 6, 6, edgecolor='#2a9a4a', facecolor='#1a3a20', alpha=0.4, lw=2)
ax.add_patch(rect)
for cx, cy in [(3.5, 3.5), (6.5, 6.5)]:
    c = Circle((cx, cy), 0.8, color='#1a3a20', alpha=0.7, ec='#40c060', lw=2)
    ax.add_patch(c)
    ax.arrow(cx, cy, 0.5, 0.5, head_width=0.25, head_length=0.2,
             fc='#ffcc44', ec='#ffcc44', lw=1.5, alpha=0.7)
ax.text(5, 1, r'severable', fontsize=10, color='#60d0ff', ha='center')

# Bottom-left: two arrows comparison
ax = fig.add_subplot(gs[1, 0])
style(ax, '')
# Up arrow
ax.annotate('', xy=(2.5, 8.5), xytext=(2.5, 1.5),
            arrowprops=dict(arrowstyle='->', color='#ff8844', lw=4))
ax.text(1, 5, r'local $\to$ global', fontsize=9, color='#ff8844', ha='center', va='center', rotation=90)
# Down arrow
ax.annotate('', xy=(7.5, 1.5), xytext=(7.5, 8.5),
            arrowprops=dict(arrowstyle='->', color='#40c060', lw=4))
ax.text(9, 5, r'global $\to$ local', fontsize=9, color='#40c060', ha='center', va='center', rotation=90)
# Center label
ax.text(5, 5, r'$H^1$', fontsize=24, color='#d0d0d0', ha='center', va='center')
ax.text(5, 3, r'measures the gap', fontsize=8, color='#888', ha='center')

# Bottom-right: core question
ax = fig.add_subplot(gs[1, 1])
style(ax, '')
ax.text(5, 7.5, r'can local data', fontsize=12, color='#d0d0d0', ha='center')
ax.text(5, 6.2, r'extend globally?', fontsize=12, color='#d0d0d0', ha='center')
ax.text(5, 4.5, r'gluing', fontsize=10, color='#ff8844', ha='center')
ax.arrow(5, 3.8, 0, -0.6, head_width=0.4, head_length=0.2,
         fc='#ff8844', ec='#ff8844', lw=2)
ax.text(5, 2.5, r'continuation', fontsize=10, color='#40c060', ha='center')
ax.arrow(5, 2, 0, -0.6, head_width=0.4, head_length=0.2,
         fc='#40c060', ec='#40c060', lw=2)
ax.text(5, 0.7, r'same gap, opposite direction', fontsize=8, color='#888', ha='center')

plt.savefig('/home/sprite/slop-salon-gert/assets/global-to-local-cover.jpg',
            bbox_inches='tight', facecolor='#0a0a0f', dpi=150)
plt.close()
print("done")
