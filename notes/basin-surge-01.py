"""
Basin surge: perturb the polynomial and watch basins deform.

z^3 - 1 has three basins of attraction. Perturb with a small term:
z^3 - 1 + epsilon * z (or other perturbations).

Watch how basin boundaries respond — do they deform smoothly,
or do they undergo topological transitions (basin flipping)?

This is the dynamical complement to the boundary condition arc.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def newton_step(z, poly_coeffs, deriv_coeffs):
    """One Newton step: z -> z - p(z)/p'(z)"""
    p = np.polyval(poly_coeffs, z)
    dp = np.polyval(deriv_coeffs, z)
    mask = np.abs(dp) < 1e-14
    z = z - p / dp
    z[mask] = z[mask] + 1e-6j  # regularize
    return z

def basin_attractor(z, poly_coeffs, deriv_coeffs, max_iter=30):
    """Find which root z converges to via Newton's method."""
    for _ in range(max_iter):
        z = newton_step(z, poly_coeffs, deriv_coeffs)
    roots = np.roots(poly_coeffs)
    dists = np.abs(z[:, :, None] - roots[None, None, :])
    return np.argmin(dists, axis=2), roots

def color_basins(attractors, roots, ax, extent):
    """Color each basin differently based on root angle."""
    n = len(roots)
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    colors = []
    for a in angles:
        r = 0.5 + 0.5 * np.cos(a)
        g = 0.5 + 0.5 * np.cos(a + 2*np.pi/3)
        b = 0.5 + 0.5 * np.cos(a + 4*np.pi/3)
        colors.append((r, g, b))

    cmap = LinearSegmentedColormap.from_list(f"basins_{n}", colors, N=n)
    im = ax.imshow(attractors, cmap=cmap, extent=extent, vmin=0, vmax=n-1,
                   origin='lower', interpolation='nearest')
    for i, root in enumerate(roots):
        ax.scatter(root.real, root.imag, c='white', s=40, edgecolors='black',
                   linewidths=1, zorder=5, marker='o')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    return im

# Grid
x = np.linspace(-1.5, 1.5, 600)
y = np.linspace(-1.5, 1.5, 600)
xx, yy = np.meshgrid(x, y)
z = xx + 1j * yy
extent = [-1.5, 1.5, -1.5, 1.5]

# Perturbation strengths
epsilons = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5]
perturb_types = [
    ("unperturbed", None),
    ("+ ε·z", "epsilon_z"),
    ("+ ε·z²", "epsilon_z2"),
]

# Layout: 3 perturbations x 6 epsilons
fig, axes = plt.subplots(3, 6, figsize=(24, 10.5))

for row, (name, ptype) in enumerate(perturb_types):
    for col, eps in enumerate(epsilons):
        ax = axes[row, col]
        if ptype is None:
            coeffs = [1, 0, 0, -1]
        else:
            coeffs = [1, 0, 0, -1]
            if eps > 0.01:
                if ptype == "epsilon_z":
                    coeffs[1] += eps
                elif ptype == "epsilon_z2":
                    coeffs[2] += eps

        deriv_coeffs = np.polyder(coeffs)
        attractors, roots = basin_attractor(z, coeffs, deriv_coeffs)
        color_basins(attractors, roots, ax, extent)
        ax.set_title(f"{name}  ε={eps:.2f}", fontsize=9)

# Hide last row if needed (we only need 3 rows)
# Add titles on left
for row, (name, _) in enumerate(perturb_types):
    axes[row, 0].text(-0.05, 0.5, name, fontsize=10, fontweight='bold',
                      va='center', ha='center', rotation=90,
                      transform=axes[row, 0].transAxes)

plt.suptitle("Basin surge: perturbation responses to z³-1", fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('/tmp/basin-surge-01.png', dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("Done")
