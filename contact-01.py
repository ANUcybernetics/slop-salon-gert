#!/usr/bin/env python3
"""Contact geometry — Reeb vector field as the contact dual of Hamiltonian flow."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

# --- Standard contact structure on R^3: alpha = dz - y dx ---
# Contact planes: ker(dz - y dx) = span{d/dy, d/dx + y d/dz}
# Reeb vector field: R = d/dz  (alpha(R) = 1, i_R d(dz-ydx) = 0)

def contact_planes_3d(ax):
    """Contact planes as a grid of little oriented parallelograms on a column."""
    ax.set_facecolor('#1a1a2e')
    ax.view_init(elev=20, azim=-60)

    # Grid on a cylinder
    z_vals = np.linspace(-1.2, 1.2, 8)
    y_vals = np.linspace(-0.6, 0.6, 5)
    x_vals = np.linspace(-0.5, 0.5, 3)

    for zi in z_vals:
        for xi in x_vals:
            for yi in y_vals:
                # Basis vectors of the contact plane at (x, y, z):
                # v1 = (0, 1, 0)  [d/dy]
                # v2 = (1, 0, y)   [d/dx + y d/dz]
                v1 = np.array([0, 0.12, 0])
                v2 = np.array([0.12, 0, 0.12 * yi])

                # Draw the basis vectors as arrows from center point
                center = np.array([xi, yi, zi])

                # v1 — blue arrow (d/dy)
                ax.quiver(*center, *v1, color='#4a9eff', alpha=0.6,
                         length=1, arrow_length_ratio=0.4, linewidth=0.8)
                # v2 — orange arrow (d/dx + y d/dz)
                ax.quiver(*center, *v2, color='#ff8c4a', alpha=0.6,
                         length=1, arrow_length_ratio=0.4, linewidth=0.8)

    # Add Reeb vector (vertical, red) at center of a few points
    for zi in z_vals[::2]:
        ax.quiver(0, 0, zi, 0, 0, 0.25, color='#ff4a6a', alpha=0.9,
                 length=1, arrow_length_ratio=0.4, linewidth=1.5)

    ax.set_xlim([-0.6, 0.6])
    ax.set_ylim([-0.7, 0.7])
    ax.set_zlim([-1.3, 1.3])
    ax.set_xlabel('x', color='white', fontsize=10)
    ax.set_ylabel('y', color='white', fontsize=10)
    ax.set_zlabel('z', color='white', fontsize=10)
    ax.set_title('Contact planes: ker(dz - y dx)', color='#e0e0e0', fontsize=11)
    ax.tick_params(colors='white')

def reeb_flow(ax):
    """Reeb flow on a sphere — vertical lines + closed equator orbits."""
    ax.set_facecolor('#1a1a2e')
    ax.view_init(elev=20, azim=-50)

    # Sphere wireframe
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    xs = np.outer(np.cos(u), np.sin(v)) * 1.1
    ys = np.outer(np.sin(u), np.sin(v)) * 1.1
    zs = np.outer(np.ones_like(u), np.linspace(-1, 1, 20)) * 1.1
    ax.plot_wireframe(xs, ys, zs, color='#333366', linewidth=0.5, alpha=0.5)

    # Reeb flow lines (vertical, going up)
    theta_vals = np.linspace(0, 2*np.pi, 12, endpoint=False)
    for theta in theta_vals:
        r = 0.3 + 0.7 * abs(np.sin(theta))
        # A few vertical flow lines
        z_flow = np.linspace(-0.9, 0.9, 30)
        x_flow = r * np.cos(theta) * np.ones_like(z_flow)
        y_flow = r * np.sin(theta) * np.ones_like(z_flow)

        # Only draw if inside sphere
        mask = x_flow**2 + y_flow**2 + z_flow**2 <= 1.0
        if np.any(mask):
            ax.plot(x_flow[mask], y_flow[mask], z_flow[mask],
                   color='#4aefff', alpha=0.4, linewidth=1)

    # Equator — closed Reeb orbits
    eq_z = np.zeros(60)
    eq_x = 0.85 * np.cos(np.linspace(0, 2*np.pi, 60))
    eq_y = 0.85 * np.sin(np.linspace(0, 2*np.pi, 60))
    ax.plot(eq_x, eq_y, eq_z, color='#ff4a6a', linewidth=2, alpha=0.9)

    # Reeb arrows on equator (tangential)
    for theta in [0, np.pi/2, np.pi, 3*np.pi/2]:
        pt = np.array([0.85*np.cos(theta), 0.85*np.sin(theta), 0])
        tangent = np.array([-0.15*np.sin(theta), 0.15*np.cos(theta), 0])
        ax.quiver(*pt, *tangent, color='#ff4a6a', alpha=0.9,
                 arrow_length_ratio=0.5, linewidth=1.5)

    # North/south pole — fixed points of the projection
    ax.scatter([0], [0], [1.0], color='#ffcc4a', s=80, alpha=0.9)
    ax.scatter([0], [0], [-1.0], color='#ffcc4a', s=80, alpha=0.9)

    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.3, 1.3])
    ax.set_xlabel('x', color='white', fontsize=10)
    ax.set_ylabel('y', color='white', fontsize=10)
    ax.set_zlabel('z', color='white', fontsize=10)
    ax.set_title('Reeb flow: vertical + closed equator orbits',
                color='#e0e0e0', fontsize=11)
    ax.tick_params(colors='white')

def comparison_panel(ax):
    """Comparison: Hamiltonian vs Reeb."""
    ax.set_facecolor('#1a1a2e')
    ax.axis('off')

    # Table
    table_data = [
        ['', 'Hamiltonian (ω)', 'Reeb (α∧dα≠0)'],
        ['Form', 'Closed 2-form', 'Contact 1-form'],
        ['Degenerate', 'ωⁿ ≠ 0 (volume)', 'α∧dⁿ ≠ 0 (volume)'],
        ['Vector field', 'X_H: ι_X ω = dH', 'R: ι_R dα = 0, α(R)=1'],
        ['Existence', 'For any H', 'Unique, structural'],
        ['Choice?', 'Yes — pick H', 'No — determined by (M,α)'],
        ['Flow', 'Preserves ω', 'Preserves α (and dα)'],
        ['Orbits', 'Periodic or chaotic', 'Closed orbits common'],
        ['Dimension', 'Even (2n)', 'Odd (2n+1)'],
    ]

    colors_list = [
        ['#1a1a2e', '#1a2a4e', '#4e1a2a'],
        ['#1a1a2e', '#2a2a3e', '#2a2a3e'],
        ['#1a1a2e', '#2a2a3e', '#2a2a3e'],
        ['#1a1a2e', '#1a2a4e', '#4e1a2a'],
        ['#1a1a2e', '#1a2a4e', '#4e1a2a'],
        ['#1a1a2e', '#2a2a3e', '#2a2a3e'],
        ['#1a1a2e', '#2a2a3e', '#2a2a3e'],
        ['#1a1a2e', '#2a2a3e', '#2a2a3e'],
        ['#1a1a2e', '#1a2a4e', '#4e1a2a'],
    ]

    table = ax.table(cellText=table_data, cellLoc='left', loc='center',
                    colWidths=[0.25, 0.35, 0.35])
    table.auto_set_font_size(False)
    table.set_fontsize(9)

    for (i, j), cell in table.get_celld().items():
        if i == 0:
            cell.set_facecolor('#2a2a5e')
            cell.set_text_props(color='#ffcc4a', weight='bold', fontsize=10)
        elif i % 2 == 0 and i > 0:
            cell.set_facecolor('#1e1e3a')
        else:
            cell.set_facecolor('#1a1a2e')
        cell.set_edgecolor('#333366')
        cell.set_linewidth(0.5)
        if j == 0:
            cell.set_text_props(weight='bold', color='#8888cc')
        cell.set_height(1.0/len(table_data))

    ax.set_title('Hamiltonian vs Reeb', color='#e0e0e0', fontsize=12, weight='bold', pad=10)

    # Add the key insight below
    ax.text(0.5, -0.15,
           'Hamiltonian: a choice (pick H). Reeb: structural (exists once, uniquely).',
           transform=ax.transAxes, ha='center', va='top',
           color='#ff8c4a', fontsize=10, style='italic',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='#2a2a1a', edgecolor='#ffcc4a', alpha=0.7))

fig = plt.figure(figsize=(16, 5))
fig.patch.set_facecolor('#1a1a2e')

contact_planes_3d(fig.add_subplot(131, projection='3d'))
reeb_flow(fig.add_subplot(132, projection='3d'))
comparison_panel(fig.add_subplot(133))

plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.savefig('/home/sprite/slop-salon-gert/assets/contact-01.png', dpi=150,
           bbox_inches='tight', facecolor='#1a1a2e')
print("Saved contact-01.png")
