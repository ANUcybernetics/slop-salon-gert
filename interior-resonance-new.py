#!/usr/bin/env python3
"""Interior resonance: harmonic forms on closed vs bounded manifolds.

On a closed manifold, harmonic forms = cohomology classes — pure topology,
no boundary conditions needed. On a manifold with boundary, there's an extra
degree of freedom: things can resonate without being topological.

Three panels:
1. Closed surface: harmonic 1-form on a torus (topological, no boundary)
2. Bounded surface: harmonic on annulus (boundary conditions matter)
3. The gap: what resonates on bounded but not closed — non-topological modes
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.gridspec import GridSpec

def torus_field(u, v, R=2, r=0.7):
    """Parametric torus, compute toroidal/axial harmonic 1-forms."""
    x = (R + r*np.cos(v)) * np.cos(u)
    y = (R + r*np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    return x, y, z

def closed_torus_quiver(ax, N=15):
    """Harmonic 1-form on torus — two directions, neither needs a boundary."""
    u = np.linspace(0, 2*np.pi, N, endpoint=False)
    v = np.linspace(0, 2*np.pi, N, endpoint=False)
    U, V = np.meshgrid(u, v, indexing='ij')

    x, y, z = torus_field(U, V)

    # Harmonic form: constant in (u,v) coordinates — topological, not geometric
    du = np.ones_like(U) * 0.4
    dv = np.ones_like(V) * 0.4

    # Convert to 3D vector components
    dx = (-np.sin(U)*(2+0.7*np.cos(V))*du - 0.7*np.sin(V)*np.cos(U)*dv)
    dy = ( np.cos(U)*(2+0.7*np.cos(V))*du - 0.7*np.sin(V)*np.sin(U)*dv)
    dz =                        0.7*np.cos(V)*dv

    # Show every other arrow — readable density on torus
    skip = slice(0, None, 2)
    ax.quiver(x[skip,skip], y[skip,skip], z[skip,skip],
              dx[skip,skip], dy[skip,skip], dz[skip,skip],
              length=0.35, alpha=0.8, color='#4a9eff')

    # Thin wireframe so torus shape reads clearly
    u_wire = np.linspace(0, 2*np.pi, 30)
    v_wire = np.linspace(0, 2*np.pi, 30)
    UW, VW = np.meshgrid(u_wire, v_wire)
    XW, YW, ZW = torus_field(UW, VW)
    ax.plot_surface(XW, YW, ZW, color='#1a1a2e', alpha=0.5, linewidth=0)

    ax.set_title("Closed: every harmonic is topological", fontsize=10, color='#ccc')
    ax.set_axis_off()
    ax.view_init(elev=25, azim=45)
    ax.set_box_aspect([1,1,0.6])

def bounded_annulus_quiver(ax):
    """Harmonic on annulus — boundary conditions create non-topological modes."""
    theta = np.linspace(0, 2*np.pi, 40, endpoint=False)
    r = np.linspace(0.8, 2.0, 15)
    Rgrid, Tgrid = np.meshgrid(r, theta, indexing='ij')

    x = Rgrid * np.cos(Tgrid)
    y = Rgrid * np.sin(Tgrid)

    # Harmonic on annulus: combination of radial (non-topological) and angular (topological)
    dr = np.ones_like(Rgrid) * 0.15
    dtheta = 0.5 / Rgrid * np.ones_like(Rgrid)

    dx = np.cos(Tgrid)*dr - Rgrid*np.sin(Tgrid)*dtheta
    dy = np.sin(Tgrid)*dr + Rgrid*np.cos(Tgrid)*dtheta

    skip = slice(0, None, 2)
    ax.quiver(x[skip,skip], y[skip,skip],
              dx[skip,skip], dy[skip,skip],
              scale=8, scale_units='inches', alpha=0.7, color='#ff6a4a')

    ax.set_title("Bounded: resonance needs a boundary condition", fontsize=10, color='#ccc')
    ax.set_axis_off()
    ax.set_facecolor('#0a0a0f')

def gap_comparison(ax):
    """What exists in one space but not the other — the gap between closed and bounded."""
    N = 50
    k = np.linspace(-2, 2, N)
    l = np.linspace(-2, 2, N)
    K, L = np.meshgrid(k, l)

    # On an annulus: continuous spectrum modulated by boundary — radial modes add
    annulus_eigen = np.exp(-(K**2 + L**2) * 0.5) * (1 + 0.5 * np.cos(2*K))

    ax.imshow(annulus_eigen, origin='lower', extent=[-2, 2, -2, 2],
              cmap='viridis', alpha=0.8, aspect='equal')

    for i in range(-2, 3):
        for j in range(-2, 3):
            if i*i + j*j < 10:
                ax.plot(i, j, 'wo', markersize=6, alpha=0.9)

    ax.set_xlabel(r'$k_r$ (radial)', fontsize=9, color='#999')
    ax.set_ylabel(r'$k_\theta$ (angular)', fontsize=9, color='#999')
    ax.set_title("Spectral gap: radial modes exist only with boundary", fontsize=10)
    ax.set_facecolor('#0a0a0f')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color('#999')

fig = plt.figure(figsize=(14, 3.5), dpi=120)
fig.patch.set_facecolor('#0a0a0f')

gs = GridSpec(1, 3, figure=fig, width_ratios=[1.2, 1, 1], wspace=0.3)

ax1 = fig.add_subplot(gs[0], projection='3d')
ax1.set_facecolor('#0a0a0f')
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])

closed_torus_quiver(ax1)
bounded_annulus_quiver(ax2)
gap_comparison(ax3)

plt.savefig('interior-resonance-new.png', dpi=120, facecolor=fig.get_facecolor(),
            bbox_inches='tight')
print("Saved interior-resonance-new.png")
