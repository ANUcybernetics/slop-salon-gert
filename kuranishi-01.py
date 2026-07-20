import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

np.random.seed(42)

# Kuranishi map: quadratic obstruction in deformation theory
# κ: U → Ob, where U is the deformation space, κ(ξ) = Q(ξ,ξ) + higher
# ker(κ) = unobstructed directions (survive to all orders)
# im(κ) = first obstruction locus

fig, axes = plt.subplots(1, 4, figsize=(14, 3.2), dpi=150)

# Panel A: Kuranishi map as quadratic cone in 2D deformation space
ax = axes[0]
u = np.linspace(-3, 3, 200)
v = np.linspace(-3, 3, 200)
U, V = np.meshgrid(u, v)
Q = U**2 - 2 * V**2

im0 = ax.contourf(U, V, Q, levels=30, cmap='coolwarm', alpha=0.8)
ax.contour(U, V, Q, levels=[0], colors='white', linewidths=2.5, linestyles='-')
ax.plot(0, 0, 'ko', markersize=6, zorder=5)
for angle in [0.3, 0.5, 0.7, 1.0, 1.4]:
    t = np.linspace(0, 2.5, 100)
    x = t * np.cos(angle)
    y = t * np.sin(angle)
    inside_ker = np.abs(x**2 - 2*y**2) < 0.3
    color = 'gold' if inside_ker.mean() > 0.5 else 'teal'
    alpha = 0.7 if inside_ker.mean() > 0.5 else 0.4
    ax.plot(x, y, color=color, linewidth=1.5, alpha=alpha, zorder=3)
ax.set_xlabel(r'$\xi_1$')
ax.set_ylabel(r'$\xi_2$')
ax.set_title('κ(ξ) = Q(ξ, ξ)', fontsize=10)
ax.set_aspect('equal')
fig.colorbar(im0, ax=ax, label='Q(u,v)')

# Panel B: Exact sequence 0 → ker → U → im → 0
ax = axes[1]
U_rect = matplotlib.patches.FancyBboxPatch((0.5, 0.5), 2.5, 2.0,
                                           boxstyle="round,pad=0.05",
                                           edgecolor='steelblue',
                                           facecolor='lightblue',
                                           alpha=0.3, linewidth=2)
ax.add_patch(U_rect)
ker_path = matplotlib.patches.FancyBboxPatch((0.5, 1.2), 2.5, 0.6,
                                             boxstyle="round,pad=0.02",
                                             edgecolor='gold',
                                             facecolor='gold',
                                             alpha=0.4, linewidth=2)
ax.add_patch(ker_path)

ax.annotate('', xy=(0.7, 1.5), xytext=(0.05, 1.5),
            arrowprops=dict(arrowstyle='->', lw=2, color='black'))
ax.text(0.05, 1.65, '0', fontsize=11, ha='left', va='bottom')
ax.text(0.4, 1.7, 'ker', fontsize=11, ha='center', va='bottom',
        color='gold', weight='bold')

ax.annotate('', xy=(3.5, 0.5), xytext=(3.0, 0.7),
            arrowprops=dict(arrowstyle='->', lw=2, color='black'))
ax.text(3.2, 0.6, 'U ↠ im', fontsize=10, ha='left', va='bottom')

ax.text(4.2, 0.65, 'im', fontsize=11, ha='center', va='bottom',
        color='teal', weight='bold')

ax.text(1.75, 1.5, 'ker\n(what survives)', fontsize=8, ha='center',
        va='center', weight='bold')
ax.text(1.75, 0.8, 'U / ker', fontsize=8, ha='center', va='center',
        color='teal', weight='bold')
ax.text(3.0, 1.5, 'im\n(first obstructions)', fontsize=8, ha='center',
        va='center', color='teal', weight='bold')
ax.annotate('κ(ξ) = Q(ξ,ξ)', xy=(3.0, 2.0), fontsize=10, ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='teal', alpha=0.9))
ax.set_xlim(-0.2, 5.0)
ax.set_ylim(0, 3)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('0 → ker → U → im → 0', fontsize=10, pad=10)

# Panel C: 3D obstruction surface
ax = axes[2]
ax3d = fig.add_subplot(1, 4, 3, projection='3d')
s2 = np.linspace(-2, 2, 60)
t2 = np.linspace(-2, 2, 60)
S2, T2 = np.meshgrid(s2, t2)
Z2 = S2**2 - 2 * T2
color2 = np.zeros(Z2.shape + (3,))
color2[np.abs(Z2) < 0.5, :] = [0.9, 0.8, 0.1]
color2[Z2 > 0.5, :] = [0.2, 0.6, 0.6]
color2[Z2 < -0.5, :] = [0.6, 0.2, 0.4]
ax3d.plot_surface(S2, T2, Z2, facecolors=color2, alpha=0.8, edgecolor='none')
cone_u2 = np.linspace(-2, 2, 50)
cone_v1_2 = cone_u2 / np.sqrt(2)
cone_v2_2 = -cone_u2 / np.sqrt(2)
ax3d.plot(cone_u2, cone_v1_2, cone_u2**2 - 2*(cone_v1_2**2), 'w-', linewidth=3)
ax3d.plot(cone_u2, cone_v2_2, cone_u2**2 - 2*(cone_v2_2**2), 'w-', linewidth=3)
ax3d.set_xlabel(r'$\xi_1$')
ax3d.set_ylabel(r'$\xi_2$')
ax3d.set_zlabel('Q')
ax3d.set_title('Obstruction surface', fontsize=10)
ax3d.view_init(elev=25, azim=60)
# Replace axes[2] with the 3D axis reference
axes[2] = ax3d

# Panel D: H²=0 vs obstructed — unobstructed directions vs first obstruction
ax = axes[3]
# Left half: H²=0, all paths survive
for i in range(4):
    angle = 2 * np.pi * i / 8
    r = np.linspace(0, 1.0, 50)
    x = r * np.cos(angle)
    y = r * np.sin(angle)
    ax.plot(x, y + 0.5, 'gold', linewidth=1.5, alpha=0.7)

# Right half: H²≠0, some paths terminate at obstructions
for i in range(4, 8):
    angle = 2 * np.pi * i / 8
    r = np.linspace(0, 1.0, 50)
    x = r * np.cos(angle)
    y = r * np.sin(angle)
    if abs(angle - np.pi/4) < np.pi/6:
        ax.plot(x, y - 0.5, 'ros', linewidth=1.5, alpha=0.4,
                marker='o', markersize=3)
        ax.plot(0.6 * np.cos(angle), 0.6 * np.sin(angle) - 0.5,
                'r.', markersize=10)
    else:
        ax.plot(x, y - 0.5, 'gold', linewidth=1.5, alpha=0.7)

# Labels
ax.text(-1.0, 1.8, 'H² = 0', fontsize=10, ha='center', weight='bold')
ax.text(-1.0, 1.5, 'all paths survive', fontsize=8, ha='center')
ax.text(1.0, 1.8, 'H² ≠ 0', fontsize=10, ha='center', weight='bold')
ax.text(1.0, 1.5, 'paths terminate', fontsize=8, ha='center')
# Divide line
ax.axvline(0, color='black', linestyle='--', alpha=0.3)

ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.8, 2.0)
ax.set_aspect('equal')
ax.set_title('Unobstructed vs obstructed\npaths through deformation space',
             fontsize=10, pad=10)

plt.tight_layout()
fig.savefig('kuranishi-01.png', dpi=150, bbox_inches='tight')
print("Done: kuranishi-01.png (4-panel)")
