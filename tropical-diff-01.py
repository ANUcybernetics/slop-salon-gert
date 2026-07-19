import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig = plt.figure(figsize=(14, 11))
gs = fig.add_gridspec(4, 2, hspace=0.35, wspace=0.28,
                       height_ratios=[1, 1, 1.1, 0.7])

# --- Panel 1 (top): Sawtooth on the circle ---
ax1 = fig.add_subplot(gs[0, :])
theta = np.linspace(-np.pi, np.pi, 500)
sawtooth = 10 * (theta / (2*np.pi) - np.floor(theta / (2*np.pi) + 0.5))

# Draw as two continuous segments (not jumping)
seg1 = (theta >= -np.pi) & (theta < 0)
seg2 = (theta >= 0) & (theta <= np.pi)
ax1.plot(theta[seg1], sawtooth[seg1], 'teal', linewidth=2.5, zorder=2)
ax1.plot(theta[seg2], sawtooth[seg2], 'teal', linewidth=2.5, zorder=2)

# Mark kinks (transition functions)
kinks = [-np.pi, 0, np.pi]
for kx in kinks:
    ax1.axvline(kx, color='orangered', linestyle='--', alpha=0.5, linewidth=1.5, zorder=1)
    ax1.plot(kx, 0, 'o', color='orangered', markersize=10, zorder=3)

ax1.set_xlim(-np.pi-0.4, np.pi+0.4)
ax1.set_ylim(-7, 7)
ax1.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
ax1.set_xticklabels([r'$-\pi$', r'$-\pi/2$', r'$0$', r'$\pi/2$', r'$\pi$'])
ax1.set_yticks([])
ax1.set_xlabel(r'$\lambda$ (detuning parameter)', fontsize=12)
ax1.text(0, -5.5, 'kink = chart boundary  ·  each reset is a transition function',
         ha='center', fontsize=10.5, color='teal', fontweight='bold')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.set_title('sawtooth: the detuning loop', fontsize=13, fontweight='bold', pad=15)

# --- Panel 2: Smooth coboundary → discrete d_r ---
ax2 = fig.add_subplot(gs[1, :])
x = np.linspace(-3, 3, 400)

# Smooth coboundary: δf with interesting structure
df_smooth = np.sin(x) + 0.3*np.sin(3*x)
ax2.plot(x, df_smooth, 'teal', linewidth=2.5, label=r'smooth $\delta f(\lambda)$')

# Discrete lattice points
lattice_pts = np.array([-2.5, -1.25, 0, 1.25, 2.5])
lattice_vals_actual = np.sin(lattice_pts) + 0.3*np.sin(3*lattice_pts)
ax2.plot(lattice_pts, lattice_vals_actual, 's', color='orangered', markersize=11, zorder=3,
         label='discrete coboundaries (lattice)')

# Draw vertical lines from lattice points to axis
for lx, lv in zip(lattice_pts, lattice_vals_actual):
    ax2.axvline(lx, color='orangered', alpha=0.25, linewidth=1)
    ax2.plot(lx, 0, 'kx', markersize=6, markeredgewidth=1.5)

ax2.set_xlabel(r'$\lambda$', fontsize=12)
ax2.set_ylabel(r'$\delta f(\lambda)$', fontsize=12)
ax2.legend(fontsize=10, loc='upper right', framealpha=0.9)
ax2.set_title(r'tropicalisation: smooth coboundary $\to$ discrete differentials',
              fontsize=13, fontweight='bold', pad=15)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_ylim(-2, 2.5)
ax2.axhline(0, color='gray', linewidth=0.5, alpha=0.5)

# --- Panel 3: E_0 page (all cohomology classes) ---
ax3 = fig.add_subplot(gs[2, 0])
ax3.set_xlim(-0.7, 4.7)
ax3.set_ylim(-0.7, 4.7)
ax3.set_aspect('equal')

for i in range(5):
    ax3.axhline(i, color='gray', linewidth=0.5, alpha=0.5)
    ax3.axvline(i, color='gray', linewidth=0.5, alpha=0.5)

ax3.set_xlabel(r'$p$ (base)', fontsize=10)
ax3.set_ylabel(r'$q$ (fiber)', fontsize=10)
ax3.set_xticks([0, 1, 2, 3, 4])
ax3.set_yticks([0, 1, 2, 3, 4])
ax3.set_xticklabels([0, 1, 2, 3, 4])
ax3.set_yticklabels([0, 1, 2, 3, 4])
ax3.set_title(r'$E_0$: all classes', fontsize=12, fontweight='bold')

# All cells
for p in range(4):
    for q in range(4):
        ax3.plot(p, q, 'o', color='teal', markersize=9, alpha=0.5)

# --- Panel 4: E_∞ page (survivors + deleted arrows) ---
ax4 = fig.add_subplot(gs[2, 1])
ax4.set_xlim(-0.7, 4.7)
ax4.set_ylim(-0.7, 4.7)
ax4.set_aspect('equal')

for i in range(5):
    ax4.axhline(i, color='gray', linewidth=0.5, alpha=0.5)
    ax4.axvline(i, color='gray', linewidth=0.5, alpha=0.5)

ax4.set_xlabel(r'$p$ (base)', fontsize=10)
ax4.set_ylabel(r'$q$ (fiber)', fontsize=10)
ax4.set_xticks([0, 1, 2, 3, 4])
ax4.set_yticks([0, 1, 2, 3, 4])
ax4.set_xticklabels([0, 1, 2, 3, 4])
ax4.set_yticklabels([0, 1, 2, 3, 4])
ax4.set_title(r'$E_\infty$: graded shadow', fontsize=12, fontweight='bold')

# Survivors
survivors = [(0,0), (2,1), (3,0), (1,3)]
for p, q in survivors:
    ax4.plot(p, q, 's', color='gold', markersize=14, zorder=4,
             markeredgewidth=1.5, markeredgecolor='k')

# Deleted (ghost)
deleted = [(1,0), (0,1), (1,1), (2,0), (0,2), (3,1)]
for p, q in deleted:
    ax4.plot(p, q, 'o', color='orangered', markersize=9, alpha=0.4)

# Arrows showing d_r differentials
arrow_props = dict(arrowstyle='->', color='teal', linewidth=2.5, alpha=0.7)
arrows = [(0,0,1,0), (1,0,2,1), (0,1,0,2), (2,0,3,1), (0,2,0,3)]
for p1, q1, p2, q2 in arrows:
    ax4.annotate('', xy=(p2, q2), xytext=(p1, q1),
                 arrowprops=arrow_props)

# Legend
teal_circle = mpatches.Patch(color='teal', alpha=0.5, label='killed by $d_r$')
gold_square = mpatches.Patch(color='gold', label=r'$E_\infty$ survivors')
ax4.legend(handles=[teal_circle, gold_square], loc='upper left', fontsize=9.5,
           framealpha=0.9, handlelength=1.5)

# --- Panel 5 (bottom): Summary statement ---
ax5 = fig.add_subplot(gs[3, :])
ax5.set_xlim(0, 1)
ax5.set_ylim(0, 1)
ax5.axis('off')
ax5.text(0.5, 0.6, 'each $d_r$ is the tropicalisation of the coboundary: $\delta\omega \mapsto d(\delta\omega)$',
         ha='center', va='center', fontsize=14, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                   edgecolor='gold', linewidth=2))
ax5.text(0.5, 0.25, 'tropicalisation makes the coboundary discrete: lattice defects $\to$ $d_r$ differentials $\to$ $E_\infty$',
         ha='center', va='center', fontsize=11.5, style='italic',
         color='teal')

fig.savefig('assets/tropical-diff-01.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('Saved tropical-diff-01.png')
plt.close()
