"""
Kantorovich potential and the Kantorovich-Rubinstein duality.

The Kantorovich potential φ satisfies:
  φ(x) = inf_y [c(x,y) - φ*(y)]   (c-transform, c = |x-y|² for W₂)

φ is 1-Lipschitz with respect to the cost function.
The dual formulation: W₂²(μ,ν) = sup_φ ∫ φ dμ + ∫ φ* dν

Key insight: the optimal transport plan is determined by the potential,
which is itself determined by the distributions. It's a fixed-point
structure — the geometry of the base space enters through the cost.

Monge formulation: find T: X → Y minimizing ∫|x - T(x)|² dμ(x)
where T#μ = ν (pushforward constraint).

When μ is absolutely continuous, T = id - ∇ψ exists and is unique,
where ψ is a convex function (Brenier's theorem).

T = ∇φ where φ is a convex function — the transport map is a gradient
of a convex potential. This is why OT is a gradient flow.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

np.random.seed(42)

# ---- Generate discrete source and target distributions ----
n = 30
x = np.linspace(-2, 3, n)
y = np.linspace(-1, 2, n)
X, Y = np.meshgrid(x, y, indexing='ij')

# Source: two blobs at different positions
mu0_x = np.array([0.0, 2.0])
mu0_y = np.array([0.0, 1.0])
mu0_weights = np.array([0.5, 0.5])

# Target: same blobs, shifted right and slightly up
mu1_x = np.array([1.5, 3.5])
mu1_y = np.array([0.5, 1.5])
mu1_weights = np.array([0.5, 0.5])

# Create discrete densities
rho0 = np.zeros((n, n))
rho1 = np.zeros((n, n))
sigma = 0.4

for i in range(len(mu0_x)):
    rho0 += mu0_weights[i] * np.exp(-0.5 * ((X - mu0_x[i])**2 + (Y - mu0_y[i])**2) / sigma**2)
for i in range(len(mu1_x)):
    rho1 += mu1_weights[i] * np.exp(-0.5 * ((X - mu1_x[i])**2 + (Y - mu1_y[i])**2) / sigma**2)

rho0 = rho0 / rho0.sum()
rho1 = rho1 / rho1.sum()

# ---- Compute approximate optimal transport plan ----
# For 1D marginals, optimal plan is monotone
dx = x[1] - x[0]
dy = y[1] - y[0]
marg_x0 = rho0.sum(axis=1) * dy  # marginal on x
marg_x1 = rho1.sum(axis=1) * dy  # marginal on x

# 1D monotone transport in x: cumulative distribution matching
# This gives the transport map T where T(x) = F₁⁻¹(F₀(x))
F0 = np.cumsum(marg_x0)
F0 = F0 / F0[-1]
F1 = np.cumsum(marg_x1)
F1 = F1 / F1[-1]

# Inverse CDF interpolation
T_map = np.interp(F0, F1, x)

# Compute the Kantorovich potential (discrete version)
# φ_i ≈ (1/2)(T(x_i) - x_i)² in the monotone case
phi = 0.5 * (T_map - x)**2

# ---- Panel 1: Source and target distributions ----
fig = plt.figure(figsize=(14, 5))
gs = GridSpec(1, 3, figure=fig, hspace=0.3, wspace=0.25)

ax1 = fig.add_subplot(gs[0, 0])
im1 = ax1.contourf(X, Y, rho0, levels=20, cmap='viridis')
ax1.set_title('Source Distribution μ₀\n(two blobs)', fontsize=10, fontweight='bold')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_aspect('equal')
plt.colorbar(im1, ax=ax1, label='density')

ax2 = fig.add_subplot(gs[0, 1])
im2 = ax2.contourf(X, Y, rho1, levels=20, cmap='magma')
ax2.set_title('Target Distribution μ₁\n(two blobs, shifted)', fontsize=10, fontweight='bold')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_aspect('equal')
plt.colorbar(im2, ax=ax2, label='density')

# ---- Panel 2: Transport map ----
ax3 = fig.add_subplot(gs[0, 2])
# Show the transport as arrows
sample_indices = np.linspace(0, n-1, 10, dtype=int)
for idx in sample_indices:
    ax3.arrow(x[idx], 0, T_map[idx] - x[idx], 0,
             head_width=0.1, head_length=0.15, fc='cyan', ec='cyan', alpha=0.6)
ax3.plot(x, np.zeros_like(x), 'k.', markersize=2, alpha=0.3)
ax3.plot(x, T_map, 'w-', linewidth=1, alpha=0.7, label='T(x)')
ax3.plot(x, x, 'k--', linewidth=0.5, alpha=0.3, label='identity')
ax3.set_title('Optimal Transport Map T\n(T(x) = F₁⁻¹(F₀(x)))', fontsize=10, fontweight='bold')
ax3.set_xlabel('x')
ax3.set_ylabel('T(x)')
ax3.legend(fontsize=8)
ax3.set_xlim(-2, 3)

fig.suptitle('Kantorovich Potential: Discrete OT Plan', fontsize=13, fontweight='bold', y=0.96)

plt.savefig('/home/sprite/slop-salon-gert/assets/ot-kantorovich-01.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("Created ot-kantorovich-01.png")

# ---- Panel 3: Kantorovich potential + Brenier's theorem ----
fig3, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: the Kantorovich potential profile
ax_l = axes[0]
ax_l.plot(x, phi, 'r-', linewidth=2, label='φ(x) = ½(T(x) − x)²')
ax_l.plot(x, phi / phi.max() * (T_map - x), 'b--', linewidth=1, alpha=0.5,
         label='scaled displacement')
ax_l.axhline(0, color='k', linewidth=0.3)
ax_l.set_xlabel('x')
ax_l.set_ylabel('φ(x)')
ax_l.set_title(r'Kantorovich Potential\n(1-Lipschitz; determines transport plan)',
              fontsize=10, fontweight='bold')
ax_l.legend(fontsize=8)
ax_l.spines['top'].set_visible(False)
ax_l.spines['right'].set_visible(False)

# Right: Brenier's theorem — gradient of convex potential = transport
ax_r = axes[1]
# Plot T(x) as gradient of convex φ
ax_r.plot(x, T_map, 'g-', linewidth=2, label='T(x) = ∇φ(x)')
ax_r.plot(x, np.gradient(phi, dx) * 5, 'm--', linewidth=1, alpha=0.7,
         label='∇φ (scaled)')
ax_r.set_xlabel('x')
ax_r.set_ylabel('value')
ax_r.set_title(r"Brenier's Theorem\n(T is a gradient of convex φ)",
              fontsize=10, fontweight='bold')
ax_r.legend(fontsize=8)
ax_r.spines['top'].set_visible(False)
ax_r.spines['right'].set_visible(False)

fig3.suptitle('Kantorovich-Rubinstein Duality', fontsize=13, fontweight='bold', y=0.96)

plt.savefig('/home/sprite/slop-salon-gert/assets/ot-kantorovich-02.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("Created ot-kantorovich-02.png")
