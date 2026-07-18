import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig = plt.figure(figsize=(16, 10))
gs = matplotlib.gridspec.GridSpec(3, 3, hspace=0.45, wspace=0.35,
                                   height_ratios=[1, 1, 0.6])

# ============================================================
# Panel 1: Morse — gradient flow on S¹ (circle)
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])
theta = np.linspace(0, 2*np.pi, 300)
r = np.cos(theta)
x = r * np.cos(theta)
y = r * np.sin(theta)

ax1.plot(x, y, 'k-', linewidth=1.5)

# Morse function values projected onto circle as color
f = 1 - np.cos(theta)
sc = ax1.scatter(x, y, c=f, cmap='coolwarm', s=2, alpha=0.8)
# Mark critical points
ax1.plot(x[0], y[0], 'ro', markersize=10, label='min')  # θ=0
ax1.plot(x[150], y[150], 'bo', markersize=10, label='max')  # θ=π

# Flow arrows (gradient descent)
n_arrows = 12
for i in range(0, 300, 25):
    dx = -(x[i+1] - x[i])
    dy = -(y[i+1] - y[i])
    norm = np.sqrt(dx**2 + dy**2)
    if norm > 0:
        dx, dy = dx/norm * 0.15, dy/norm * 0.15
        ax1.arrow(x[i], y[i], dx, dy, head_width=0.08, head_length=0.05,
                  fc='steelblue', ec='steelblue', alpha=0.5, linewidth=0.8)

ax1.set_xlim(-1.6, 1.6)
ax1.set_ylim(-1.6, 1.6)
ax1.set_aspect('equal')
ax1.set_title('(a) Morse: ∇f flow on S¹', fontsize=12, fontweight='bold')
ax1.axis('off')
ax1.legend(fontsize=8, loc='upper right')

# ============================================================
# Panel 2: Morse boundary — ∂ counts trajectories
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])

# Two critical points with flow line between them
y_min, y_max = -0.5, 0.5
ax2.plot(0, y_min, 'ro', markersize=14)
ax2.plot(0, y_max, 'bo', markersize=14)
ax2.plot([0, 0], [y_min, y_max], 'k--', linewidth=1.5)

# Arrow showing flow direction
ax2.arrow(0, y_max - 0.15, 0, 0.3, head_width=0.08, head_length=0.08,
          fc='steelblue', ec='steelblue', linewidth=2)

ax2.text(0.15, (y_min + y_max) / 2, r'$\#\widehat{\gamma}(p_-, p_+) = 1$',
         fontsize=14, va='center')
ax2.text(0, -1.0, r'$\partial p_- = \sum_{p_+} \#\widehat{\gamma}(p_-, p_+) \, p_+$',
         fontsize=13, ha='center', fontweight='bold')
ax2.text(0, -1.35, 'finite-dim M', fontsize=10, ha='center', style='italic')
ax2.set_xlim(-1, 1)
ax2.set_ylim(-1.6, 1.2)
ax2.axis('off')
ax2.set_title('(b) Morse ∂: count gradient trajectories', fontsize=12, fontweight='bold')

# ============================================================
# Panel 3: Loop space — ΩS¹ with periodic orbits
# ============================================================
ax3 = fig.add_subplot(gs[0, 2], projection='3d')

# Covering space of S¹ — cylinder
t = np.linspace(0, 4*np.pi, 100)
z = np.linspace(0, 4*np.pi, 2)
T, Z = np.meshgrid(t, z)
R = 0.8
X = R * np.cos(T)
Y = R * np.sin(T)

ax3.plot_surface(X, Y, Z, alpha=0.15, color='gray')
ax3.set_xlim([-1.2, 1.2])
ax3.set_ylim([-1.2, 1.2])
ax3.set_zlim([0, 4])
ax3.set_box_aspect([1, 1, 0.8])

# Periodic orbits as constant sections at critical points
# θ=0 (min): winding number 0 section
orbit_min = np.linspace(0, 4*np.pi, 100)
ax3.plot(R*np.cos(orbit_min), R*np.sin(orbit_min), orbit_min,
         'r-', linewidth=2.5, label=r'$\gamma_-$ (min)')

# θ=π (max): another orbit
orbit_max = np.linspace(0, 4*np.pi, 100)
ax3.plot(R*np.cos(orbit_max + np.pi), R*np.sin(orbit_max + np.pi), orbit_max,
         'b-', linewidth=2.5, label=r'$\gamma_+$ (max)')

# Floer trajectory: a strip connecting them
strip_t = np.linspace(0, 4*np.pi, 100)
strip_z = strip_t
radius_transition = R + 0.15 * np.sin(np.pi * strip_t / (4*np.pi))
x_strip = radius_transition * np.cos(strip_t)
y_strip = radius_transition * np.sin(strip_t)
ax3.plot(x_strip, y_strip, strip_z, 'magenta', linewidth=2.5,
         label=r'$u$ (Floer trajectory)')

ax3.set_title('(c) Loop space ΩS¹: u connects periodic orbits', fontsize=12, fontweight='bold')
ax3.legend(fontsize=7, loc='upper left')
ax3.view_init(elev=25, azim=45)

# ============================================================
# Panel 4: Floer equation — ∂ᵤu + J∇H = 0
# ============================================================
ax4 = fig.add_subplot(gs[1, :2])

# Draw the cylinder R × S¹ (u: ℝ × S¹ → M)
# Represent as a "ribbon" surface
s = np.linspace(0, 4*np.pi, 80)  # ℝ direction (compactified to cylinder)
theta2 = np.linspace(0, 2*np.pi, 80)  # S¹
S, TH = np.meshgrid(s, theta2)

# Base radius
rho = 0.7
X_surf = rho * np.cos(TH)
Y_surf = rho * np.sin(TH)
Z_surf = S % (2*np.pi)

# Create the Floer trajectory as a twisting ribbon between two levels
ribbon_t = np.linspace(0, 6*np.pi, 200)
ribbon_angle = ribbon_t + 0.5 * np.sin(ribbon_t / 2)
ribbon_r = rho + 0.1 * np.exp(-((ribbon_t - 3*np.pi) / (2*np.pi))**2)

ribbon_x = ribbon_r * np.cos(ribbon_angle)
ribbon_y = ribbon_r * np.sin(ribbon_angle)
ribbon_z = ribbon_t % (2*np.pi)

ax4.clear()
ax4 = fig.add_subplot(gs[1, :2], projection='3d')

# Draw base cylinder (loop space)
ax4.plot_surface(X_surf[:, :40], Y_surf[:, :40], Z_surf[:, :40],
                 alpha=0.08, color='lightblue')

# Mark critical orbits at top and bottom
orbit_bottom_x = rho * np.cos(ribbon_t[:50])
orbit_bottom_y = rho * np.sin(ribbon_t[:50])
orbit_bottom_z = np.zeros_like(orbit_bottom_x)
ax4.plot(orbit_bottom_x, orbit_bottom_y, orbit_bottom_z,
         'ro', markersize=3, alpha=0.6)

orbit_top_x = rho * np.cos(ribbon_t[-50:] + np.pi)
orbit_top_y = rho * np.sin(ribbon_t[-50:] + np.pi)
orbit_top_z = (2*np.pi) * np.ones_like(orbit_top_x)
ax4.plot(orbit_top_x, orbit_top_y, orbit_top_z,
         'bo', markersize=3, alpha=0.6)

# Floer trajectory ribbon
ax4.plot(ribbon_x, ribbon_y, ribbon_z, 'magenta', linewidth=2.5)

ax4.set_xlabel('')
ax4.set_ylabel('')
ax4.set_zlabel('')
ax4.set_xlim([-1.2, 1.2])
ax4.set_ylim([-1.2, 1.2])
ax4.set_zlim([-0.5, 7])
ax4.set_box_aspect([1, 1, 0.9])
ax4.view_init(elev=20, azim=50)
ax4.set_title('(d) Floer ∂: count solutions u: ℝ × S¹ → M to ∂ᵤu + J∇H = 0',
              fontsize=12, fontweight='bold')

# ============================================================
# Panel 5: Boundary operator comparison (side by side)
# ============================================================
ax5 = fig.add_subplot(gs[2, :])
ax5.axis('off')

# Left side: Morse
box_left = FancyBboxPatch((0.02, 0.3), 0.43, 0.55,
                          boxstyle="round,pad=0.015",
                          edgecolor='black', facecolor='#f0f4ff', linewidth=2)
ax5.add_patch(box_left)
ax5.text(0.235, 0.78, 'MORSE BOUNDARY', ha='center', fontsize=11,
         fontweight='bold', va='top')
morse_text = (
    r"$\partial: C_n \to C_{n-1}$\n"
    r"$C(M) = \langle$ critical points $\rangle$\n\n"
    r"$\partial p_- = \sum_{p_+} \# \widehat{\gamma}(p_-, p_+) \; p_+$\n\n"
    r"$\widehat{\gamma}$ = gradient flow line\n"
    r"$\subset M$ (finite-dim)\n\n"
    r"$\partial^2 = 0$ via\n"
    r"broken trajectories ($\mathbb{R} \to \mathbb{R} \sqcup \mathbb{R}$)")
ax5.text(0.235, 0.55, morse_text, ha='center', va='top', fontsize=9,
         family='monospace')

# Arrow between
ax5.annotate('', xy=(0.52, 0.58), xytext=(0.48, 0.58),
             arrowprops=dict(arrowstyle='->', lw=2.5, color='darkred'))
ax5.text(0.5, 0.62, 'infinite-dim', ha='center', fontsize=9,
         color='darkred', fontweight='bold')
ax5.text(0.5, 0.55, 'ΩM', ha='center', fontsize=9,
         color='darkred', fontweight='bold', style='italic')

# Right side: Floer
box_right = FancyBboxPatch((0.55, 0.3), 0.43, 0.55,
                           boxstyle="round,pad=0.015",
                           edgecolor='darkred', facecolor='#fff5f5', linewidth=2)
ax5.add_patch(box_right)
ax5.text(0.765, 0.78, 'FLOER BOUNDARY', ha='center', fontsize=11,
         fontweight='bold', va='top', color='darkred')
floer_text = (
    r"$\partial: HF_n \to HF_{n-1}$\n"
    r"$HF_*(H) = \langle$ periodic orbits $\rangle$\n\n"
    r"$\partial \gamma_- = \sum_{\gamma_+} \# \mathcal{M}(u) \; \gamma_+$\n\n"
    r"$\mathcal{M}(u)$ = Floer trajectories\n"
    r"$\subset \Omega M$ (infinite-dim)\n\n"
    r"$\partial^2 = 0$ via\n"
    r"broken strips ($u \to$ two strips $\sqcup$ orbit)")
ax5.text(0.765, 0.55, floer_text, ha='center', va='top', fontsize=9,
         family='monospace')

# Key insight line at bottom
key_y = 0.18
ax5.text(0.5, key_y,
         'KEY:  ∂ counts intersections of stable ∩ unstable manifolds  —  finite dim: flow lines  →  infinite dim: pseudoholomorphic strips',
         ha='center', fontsize=10, fontweight='bold', va='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffcc', edgecolor='gold', linewidth=1.5))

# ============================================================
# Panel 6: Stable/unstable manifolds diagram
# ============================================================
ax6 = fig.add_subplot(gs[1, 2])

# Phase plane with stable/unstable manifolds
t6 = np.linspace(-3, 3, 300)

# Saddle point at origin
ax6.plot(0, 0, 'ko', markersize=8)

# Stable manifold (incoming)
y_stable = np.exp(-t6**2 / 2) * np.sign(t6) * 0.5
ax6.plot(t6, y_stable, 'r-', linewidth=2, alpha=0.7, label='Wˢ(γ₋)')
ax6.plot(t6, -y_stable, 'r-', linewidth=2, alpha=0.7)

# Unstable manifold (outgoing)
y_unstable = t6 * 0.5
ax6.plot(t6, y_unstable, 'b-', linewidth=2, alpha=0.7, label='Wᵘ(γ₊)')
ax6.plot(t6, -y_unstable, 'b-', linewidth=2, alpha=0.7)

# Intersection points
ax6.plot(0, 0, 'mo', markersize=12, markeredgewidth=3, markeredgecolor='white')

# Trajectories flowing through
for angle in [0.3, 0.6, -0.3, -0.6]:
    x_traj = np.linspace(-2.5, 2.5, 100)
    y_traj = angle * np.sinh(x_traj * 0.4)
    ax6.plot(x_traj, y_traj, 'gray', linewidth=0.8, alpha=0.4)

ax6.set_xlim(-2.5, 2.5)
ax6.set_ylim(-2.5, 2.5)
ax6.set_aspect('equal')
ax6.set_title('(e) Wˢ ∩ Wᵘ  =  intersection = ∂ counts', fontsize=12, fontweight='bold')
ax6.legend(fontsize=8, loc='lower right')
ax6.grid(True, alpha=0.2)

# ============================================================
# Panel 7: The grading shift
# ============================================================
ax7 = fig.add_subplot(gs[2, 2])
ax7.axis('off')

ax7.text(0.5, 0.85, 'GRADING', ha='center', fontsize=11,
         fontweight='bold', va='top')

grading_text = (
    r'Morse:  $\deg(p) = \text{index}(p)$\n'
    r'(Morse index = dim Wᵘ)\n\n'
    r'Floer:  $\deg(\gamma) = \mu(\gamma)$\n'
    r'(Conley–Zehnder index)\n\n'
    r'$\deg(\partial) = -1$\n'
    r'$\mu(\gamma_-) - \mu(\gamma_+) = 1$')

ax7.text(0.5, 0.42, grading_text, ha='center', va='top',
         fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#e8f5e9', edgecolor='green', linewidth=1.5))

plt.savefig('floer-03.png', dpi=150, bbox_inches='tight', facecolor='white')
print('Done: floer-03.png')
