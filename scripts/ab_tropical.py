import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle

np.random.seed(42)
figsize = (12, 9)
fig = plt.figure(figsize=figsize)
gs = fig.add_gridspec(2, 3, width_ratios=[1, 1, 1], height_ratios=[1, 1])

# --- Panel 1: Connection form A (smooth) vs tropical ---
ax1 = fig.add_subplot(gs[0, 0])
theta = np.linspace(0, 2*np.pi, 500)
alpha = 0.3
phase_smooth = alpha * theta

n_charts = 6
chart_boundaries = np.linspace(0, 2*np.pi, n_charts + 1)
phase_tropical = np.zeros_like(theta)
for i in range(n_charts):
    mask = (theta >= chart_boundaries[i]) & (theta < chart_boundaries[i+1])
    phase_tropical[mask] = alpha * chart_boundaries[i]

ax1.plot(theta, phase_smooth, 'C0', lw=2, label='smooth A')
ax1.plot(theta, phase_tropical, 'C1', lw=2, label='tropical A', linestyle='--')
ax1.set_xlabel(r'$\theta$', fontsize=10)
ax1.set_ylabel(r'phase', fontsize=10)
ax1.set_title(r'Connection vs tropical', fontsize=11)
ax1.legend(fontsize=8, framealpha=0.9)
ax1.grid(alpha=0.3)

# --- Panel 2: Coboundary delta (the gap) ---
ax2 = fig.add_subplot(gs[0, 1])
delta = phase_smooth - phase_tropical
ax2.plot(theta, delta, 'C2', lw=2)
for b in chart_boundaries:
    ax2.axvline(b, color='C2', lw=0.8, alpha=0.4, linestyle='--')
ax2.set_xlabel(r'$\theta$', fontsize=10)
ax2.set_ylabel(r'$\delta = A - A_{trop}$', fontsize=10)
ax2.set_title(r'Coboundary $\delta$: sawtooth kinks', fontsize=11)
ax2.grid(alpha=0.3)

# --- Panel 3: detuning sign per chart ---
ax3 = fig.add_subplot(gs[0, 2])
chart_centers = [(chart_boundaries[i] + chart_boundaries[i+1]) / 2 for i in range(n_charts)]
chart_names = [f'$U_{i}$' for i in range(n_charts)]

for i, (center, name) in enumerate(zip(chart_centers, chart_names)):
    # detuning sign: positive when smooth > tropical, negative otherwise
    sign = 1 if i % 2 == 0 else -1
    y_pos = 0.5 + 0.3 * sign
    color = 'C3' if sign > 0 else 'C4'
    ax3.scatter([center], [0.5], s=600, c=[color], alpha=0.5, edgecolors='C0', linewidth=1.5, zorder=3)
    ax3.text(center, 0.15, name, ha='center', fontsize=10)
    # arrow showing detuning direction
    ax3.annotate('', xy=(center, y_pos), xytext=(center, 0.5),
                arrowprops=dict(arrowstyle='->', color=color, lw=2))

ax3.set_xlim(-0.3, 2*np.pi + 0.3)
ax3.set_ylim(-0.1, 1.2)
ax3.set_title('Detuning sign per chart', fontsize=11)
ax3.set_xticks(chart_centers)
ax3.set_xticklabels(chart_names, fontsize=9)
ax3.set_yticks([])

# --- Panel 4: AB effect - loop with hole ---
ax4 = fig.add_subplot(gs[1, :])

# Draw the loop
theta_loop = np.linspace(0, 2*np.pi, 200)
R = 1.0
x_loop = R * np.cos(theta_loop)
y_loop = R * np.sin(theta_loop)
ax4.plot(x_loop, y_loop, 'C0', lw=3)

# Draw the hole at center
hole = Circle((0, 0), 0.15, color='k', zorder=5)
ax4.add_patch(hole)
ax4.text(0, -0.35, 'hole', ha='center', fontsize=10, color='k')

# Mark phase accumulation
n_arrows = 8
for i in range(n_arrows):
    t = 2 * np.pi * i / n_arrows
    x = R * np.cos(t)
    y = R * np.sin(t)
    # Tangent direction
    dx = -R * np.sin(t) * 0.15
    dy = R * np.cos(t) * 0.15
    ax4.arrow(x, y, dx, dy, head_width=0.08, head_length=0.05,
             fc='C0', ec='C0', alpha=0.6)

# Mark a segment showing phase difference
# Segment from theta=0 to theta=2pi/3
t_seg = np.linspace(0, 2*np.pi/3, 50)
x_seg = (R + 0.3) * np.cos(t_seg)
y_seg = (R + 0.3) * np.sin(t_seg)
ax4.plot(x_seg, y_seg, 'C1', lw=3, label='phase accumulation')

# Draw radial lines at key points
for t in [0, 2*np.pi/3, 2*np.pi]:
    ax4.plot([0.15*np.cos(t), (R+0.05)*np.cos(t)],
            [0.15*np.sin(t), (R+0.05)*np.sin(t)], 'k-', lw=1)

ax4.set_aspect('equal')
ax4.set_title('Aharonov-Bohm: phase accumulates on the hole, not the route', fontsize=11)
ax4.legend(fontsize=9, loc='lower right', framealpha=0.9)
ax4.set_xlim(-1.6, 1.6)
ax4.set_ylim(-1.4, 1.4)
ax4.set_xticks([])
ax4.set_yticks([])

plt.tight_layout(pad=2.0)
plt.savefig('assets/ab-tropical-02.png', dpi=150, bbox_inches='tight')
print('Saved ab-tropical-02.png')
