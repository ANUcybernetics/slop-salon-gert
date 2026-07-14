import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(14, 7))
fig.patch.set_facecolor('#1a1a1a')
gs = GridSpec(1, 3, figure=fig, wspace=0.15)

DARK_BG = '#1a1a1a'
TEXT_LIGHT = '#e0e0e0'
TEXT_DIM = '#888888'
EXACT = '#4fc3f7'       # cyan — exact (gradient)
COEXACT = '#ff8a65'     # orange — coexact (curl)
HARMONIC = '#aed581'    # green — harmonic
GRID_COLOR = '#2a2a2a'

def torus(u, v, R=2.0, r=0.7):
    """Parametric torus."""
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    return x, y, z

# Generate grid on torus surface
u = np.linspace(0, 2*np.pi, 40)
v = np.linspace(0, 2*np.pi, 30)
U, V = np.meshgrid(u, v)
X, Y, Z = torus(U, V)

# Viewpoint parameters
elev = 25
azim = -55

colors = [EXACT, COEXACT, HARMONIC]
titles = [
    'Exact:  ω = dφ  (gradient of scalar)',
    'Coexact: ω = δψ  (codifferential of 2-form)',
    'Harmonic: Δω = 0  (closed and co-closed)',
]
captions = [
    'coboundary — locally a gradient,\nalways exact, always zero in cohomology',
    'codifferential — locally a curl,\nnever exact (unless trivial),\nnever closed',
    'both closed and co-closed:\nω = dφ and ω = δψ simultaneously.\nrepresents a non-trivial cohomology class',
]

for i, ax_idx in enumerate([0, 1, 2]):
    ax = fig.add_subplot(gs[i], projection='3d', computed_zorder=False)
    ax.set_facecolor(DARK_BG)

    # Draw torus wireframe (subtle)
    ax.plot_wireframe(X, Y, Z, color=GRID_COLOR, rstride=5, cstride=5,
                      linewidth=0.3, alpha=0.3)

    # Compute tangent vectors on the torus for the 1-form field
    du = 2 * np.pi / 40
    dv = 2 * np.pi / 30

    # Partial derivatives of the parametrization
    # X_u, Y_u, Z_u = tangent in u direction
    # X_v, Y_v, Z_v = tangent in v direction

    R, r = 2.0, 0.7
    Xu = -((R + r*np.cos(V)) * np.sin(U))
    Yu =  ((R + r*np.cos(V)) * np.cos(U))
    Zu =  np.zeros_like(U)

    Xv = -r * np.sin(V) * np.cos(U)
    Yv = -r * np.sin(V) * np.sin(U)
    Zv =  r * np.cos(V)

    # Normal vector (cross product of tangents)
    Nx = Yu * Zv - Zu * Yv
    Ny = Zu * Xv - Xu * Zv
    Nz = Xu * Yv - Yu * Xv

    # Normalize to get unit vectors
    norm_u = np.sqrt(Xu**2 + Yu**2 + Zu**2)
    norm_v = np.sqrt(Xv**2 + Yv**2 + Zv**2)
    norm_n = np.sqrt(Nx**2 + Ny**2 + Nz**2)

    # Choose field components based on decomposition type
    if i == 0:
        # EXACT: gradient of a scalar function on the torus
        # φ(u,v) = cos(u) + 0.5*cos(2u)*sin(v)
        # dφ = (−sin(u) − sin(2u)*sin(v)) du + (0.5*cos(2u)*cos(v)) dv
        phi_u = -np.sin(U) - np.sin(2*U)*np.sin(V)
        phi_v = 0.5 * np.cos(2*U) * np.cos(V)
        # Scale by metric factors
        F1 = phi_u / (norm_u + 1e-10)
        F2 = phi_v / (norm_v + 1e-10)
        # Field = F1 * e_u + F2 * e_v (unit tangent frame)
        dx = F1 * Xu + F2 * Xv
        dy = F1 * Yu + F2 * Yv
        dz = F1 * Zu + F2 * Zv
    elif i == 1:
        # COEXACT: curl of a 2-form (in 3D, curl is codifferential of 1-form)
        # Use a 2-form ψ = sin(u)*sin(v) du∧dv
        # δψ gives a vector field tangential to the torus
        # In the tangent frame: the "curl" part has zero divergence
        # Use sin/cos fields that are divergence-free on the torus
        curl_phi_u = np.cos(U) * np.sin(V)
        curl_phi_v = -np.sin(U) * np.cos(V)
        dx = curl_phi_u * Xu / (norm_u + 1e-10) + curl_phi_v * Xv / (norm_v + 1e-10)
        dy = curl_phi_u * Yu / (norm_u + 1e-10) + curl_phi_v * Yv / (norm_v + 1e-10)
        dz = curl_phi_u * Zu / (norm_u + 1e-10) + curl_phi_v * Zv / (norm_v + 1e-10)
    else:
        # HARMONIC: two independent harmonic 1-forms on genus-1 surface
        # For torus: H^1(T²) = ℝ², spanned by du and dv (constant in flat metric)
        # These are closed (d=0) and co-closed (δ=0)
        # Use the flat harmonic forms: one along the "big" circle, one along the "small"
        harmonic_u = np.ones_like(U)  # constant along u direction
        harmonic_v = 0.3 * np.ones_like(U)  # constant along v direction (smaller amplitude)
        dx = harmonic_u * Xu / (norm_u + 1e-10) + harmonic_v * Xv / (norm_v + 1e-10)
        dy = harmonic_u * Yu / (norm_u + 1e-10) + harmonic_v * Yv / (norm_v + 1e-10)
        dz = harmonic_u * Zu / (norm_u + 1e-10) + harmonic_v * Zv / (norm_v + 1e-10)

    # Downsample for arrow plot
    step_u, step_v = 6, 6
    quiver_u = U[::step_v, ::step_u]
    quiver_v = V[::step_v, ::step_u]
    quiver_x = X[::step_v, ::step_u]
    quiver_y = Y[::step_v, ::step_u]
    quiver_z = Z[::step_v, ::step_u]
    quiver_dx = dx[::step_v, ::step_u]
    quiver_dy = dy[::step_v, ::step_u]
    quiver_dz = dz[::step_v, ::step_u]

    # Normalize arrow lengths
    arrow_len = np.sqrt(quiver_dx**2 + quiver_dy**2 + quiver_dz**2)
    max_len = np.percentile(arrow_len[arrow_len > 0], 90)
    quiver_dx = quiver_dx / (arrow_len + 1e-10) * 0.4
    quiver_dy = quiver_dy / (arrow_len + 1e-10) * 0.4
    quiver_dz = quiver_dz / (arrow_len + 1e-10) * 0.4

    # Color arrows by field strength
    magnitudes = np.sqrt(dx[::step_v, ::step_u]**2 + dy[::step_v, ::step_u]**2 + dz[::step_v, ::step_u]**2)

    ax.quiver(quiver_x, quiver_y, quiver_z, quiver_dx, quiver_dy, quiver_dz,
              length=0.3, color=colors[i], alpha=0.85, linewidths=1.2)

    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-2, 2])
    ax.set_title(titles[i], fontsize=12, color=TEXT_LIGHT, pad=15)

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.xaxis.set_tick_params(color=TEXT_DIM, labelcolor=TEXT_DIM)
    ax.yaxis.set_tick_params(color=TEXT_DIM, labelcolor=TEXT_DIM)
    ax.zaxis.set_tick_params(color=TEXT_DIM, labelcolor=TEXT_DIM)
    ax.tick_params(axis='both', colors=TEXT_DIM)

    # Set the viewing angle
    ax.view_init(elev=elev, azim=azim)

    # Remove grid
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor(GRID_COLOR)
    ax.yaxis.pane.set_edgecolor(GRID_COLOR)
    ax.zaxis.pane.set_edgecolor(GRID_COLOR)
    ax.xaxis.pane.set_alpha(0.0)
    ax.yaxis.pane.set_alpha(0.0)
    ax.zaxis.pane.set_alpha(0.0)

# Add equation row at the bottom
eqax = fig.add_axes([0.05, 0.06, 0.9, 0.06])
eqax.set_facecolor(DARK_BG)
eqax.axis('off')
eqax.text(0.5, 0.85, r'Hodge Decomposition:  ω = dφ + δψ + h',
          ha='center', va='top', fontsize=14, color=TEXT_LIGHT,
          transform=eqax.transAxes, fontweight='bold')
eqax.text(0.5, 0.15, 'Every 1-form splits into exact + coexact + harmonic. Uniquely, once the metric is chosen.',
          ha='center', va='bottom', fontsize=10, color=TEXT_DIM,
          transform=eqax.transAxes, style='italic')

plt.savefig('/home/sprite/slop-salon-gert/assets/hodge-decomposition-01.png',
            dpi=150, bbox_inches='tight', facecolor='#1a1a1a')
plt.close()

print("Done: hodge-decomposition-01.png")
