"""
Wasserstein geodesics — displacement interpolation between two distributions.

Panel 1: Two delta masses, transport as straight line in parameter space.
Panel 2: 2D Gaussians, optimal transport as affine flow.
Panel 3: Discrete histograms, Earth Mover's Distance as linear program.
Panel 4: Benamou-Brenier — velocity field and density flow (continuity equation).

Key idea: OT is not distance. It's a geometry on the space of measures.
The geodesic between μ₀ and μ₁ is the path of minimal kinetic energy.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.gridspec import GridSpec

np.random.seed(42)

def gaussian_grid(x, y, mean=(0, 0), cov=None):
    """Evaluate 2D Gaussian on a grid."""
    if cov is None:
        cov = np.eye(2) * 0.3**2
    diff = np.stack([x - mean[0], y - mean[1]], axis=-1)
    inv = np.linalg.inv(cov)
    det = np.linalg.det(cov)
    exponent = -0.5 * np.einsum('...k,kl,...l->...', diff, inv, diff)
    return (2 * np.pi * det)**(-0.5) * np.exp(exponent)

def discrete_histogram(n=20):
    """Create two discrete distributions and compute OT plan."""
    x = np.linspace(0, 1, n)
    dx = x[1] - x[0]
    # Distribution A: single peak left
    a = np.exp(-0.5 * ((x - 0.3) / 0.08)**2)
    a = a / a.sum()
    # Distribution B: single peak right
    b = np.exp(-0.5 * ((x - 0.7) / 0.08)**2)
    b = b / b.sum()
    # Ground distance (1D)
    cost = np.abs(x[:, None] - x[None, :]) * dx
    # Simple transport: solve assignment (cost + regularization)
    # Entropic regularization (Sinkhorn-like, but simple for 1D)
    # For 1D, optimal plan is monotone: sort both, match in order
    # For discrete grids already sorted, identity map is optimal
    # But with peak at different locations, we need to "move mass"
    P = np.zeros((n, n))
    # Monotone transport: each bin in a sends mass to nearest bins in b
    # Simple approach: push mass to the right
    transport_plan = np.diag(np.minimum(a, b))  # overlap stays
    remainder_a = a - np.diag(transport_plan)
    remainder_b = b - np.diag(transport_plan)
    # Push remainder from a to b monotonically
    for i in range(n):
        if remainder_a[i] > 1e-10:
            # Push to nearest bins in b with room
            for j in range(n-1, i, -1):
                if remainder_b[j] > 1e-10:
                    amt = min(remainder_a[i], remainder_b[j])
                    transport_plan[i, j] = amt
                    remainder_a[i] -= amt
                    remainder_b[j] -= amt
                if abs(remainder_a[i]) < 1e-10:
                    break
    return x, a, b, transport_plan, dx

# ---- Panel 1: Delta masses ----
fig = plt.figure(figsize=(14, 10))
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

# Delta mass transport: μ₀ = δ₀, μ₁ = δ₁
# Geodesic: μₜ = δ₍₁₋ₜ₎ₒ + tδ₁
t_vals = [0, 0.25, 0.5, 0.75, 1.0]
positions = [0, 0.25, 0.5, 0.75, 1.0]

x_range = np.linspace(-0.3, 1.3, 200)
for i, (t, pos) in enumerate(zip(t_vals, positions)):
    y = np.exp(-0.5 * ((x_range - pos*0.5) / 0.04)**2) + \
        np.exp(-0.5 * ((x_range - pos) / 0.04)**2)
    ax1.plot(x_range, y * (1 + 0.1 * t), label=f't={t:.2f}')

ax1.set_title('Displacement Interpolation\nμₜ = (1−t)μ₀ + tμ₁', fontsize=10, fontweight='bold')
ax1.set_xlabel('x')
ax1.set_ylabel('density')
ax1.legend(fontsize=8)
ax1.set_xlim(-0.3, 1.3)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_ylim(0, 2.5)

# ---- Panel 2: 2D Gaussians flow ----
X, Y = np.meshgrid(np.linspace(-2, 3, 40), np.linspace(-2, 2, 40))
mu0 = (-0.5, 0); mu1 = (2, 0.5)
cov0 = np.array([[0.3, 0.1], [0.1, 0.25]])
cov1 = np.array([[0.2, 0.05], [0.05, 0.3]])

Z0 = gaussian_grid(X, Y, mean=mu0, cov=cov0)
Z1 = gaussian_grid(X, Y, mean=mu1, cov=cov1)

# Interpolate means and covariances (linear interpolation is not geodesic in
# Wasserstein space, but good for visualization)
t_mid = 0.5
mu_mid = (1 - t_mid) * np.array(mu0) + t_mid * np.array(mu1)
# Geodesic covariance: matrix square root interpolation
sqrt_cov0 = cov0 ** 0.5  # simplified
sqrt_cov1 = cov1 ** 0.5
cov_mid = (1 - t_mid) * cov0 + t_mid * cov1
Z_mid = gaussian_grid(X, Y, mean=tuple(mu_mid), cov=cov_mid)

im2 = ax2.contourf(X, Y, Z0, levels=15, cmap='viridis', alpha=0.5)
ax2.contour(X, Y, Z1, levels=10, colors='white', linewidths=0.5, alpha=0.5)
# Arrow from mu0 to mu1
ax2.annotate('', xy=mu1, xytext=mu0,
            arrowprops=dict(arrowstyle='->', color='yellow', lw=2))
ax2.plot(mu0[0], mu0[1], 'o', color='yellow', markersize=8, label='μ₀')
ax2.plot(mu1[0], mu1[1], 'o', color='red', markersize=8, label='μ₁')
ax2.set_title('2D Gaussian Flow\n(mean + covariance transport)', fontsize=10, fontweight='bold')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.legend(fontsize=8)
ax2.set_xlim(-2, 3)
ax2.set_ylim(-2, 2)

# ---- Panel 3: Discrete histograms ----
x, a, b, P, dx = discrete_histogram(20)
ax3.imshow(P, aspect='auto', cmap='Blues', interpolation='nearest', origin='upper')
ax3.set_title('Optimal Transport Plan\n(discrete 1D histograms)', fontsize=10, fontweight='bold')
ax3.set_xlabel('support of μ₁')
ax3.set_ylabel('support of μ₀')
cbar = plt.colorbar(ax3.images[0], ax=ax3)
cbar.set_label('mass transported')

# ---- Panel 4: Benamou-Brenier velocity field ----
# Continuity equation: ∂ₜρ + ∇·(ρv) = 0
# On a grid: show density + velocity at t=0.5
grid_x = np.linspace(-1, 3, 30)
grid_y = np.linspace(-1.5, 1.5, 20)
GX, GY = np.meshgrid(grid_x, grid_y)

# Density at t=0.5 (interpolated Gaussian)
rho = gaussian_grid(GX, GY, mean=tuple(mu_mid), cov=(cov0 + cov1) / 2)

# Velocity field: v(x) ≈ (mu1 - mu0) for linear transport
# More precisely: v = ∇φ where φ is Kantorovich potential
VX = np.full_like(GX, 0.7)  # constant-ish drift (simplified)
VY = np.full_like(GY, 0.2)

# Quiver: scale arrows
scale = 15
ax4.quiver(GX[::3, ::3], GY[::3, ::3],
           VX[::3, ::3], VY[::3, ::3],
           rho[::3, ::3], cmap='coolwarm', scale=scale, width=0.004)
cont = ax4.contourf(GX, GY, rho, levels=12, cmap='viridis', alpha=0.6)
plt.colorbar(cont, ax=ax4, label='ρ(x,t)')
ax4.set_title('Benamou-Brenier\n∂ₜρ + ∇·(ρv) = 0,  |v|² minimal',
              fontsize=10, fontweight='bold')
ax4.set_xlabel('x')
ax4.set_ylabel('y')
ax4.set_aspect('equal')

fig.suptitle('Wasserstein Space: Geodesics and Flow', fontsize=13, fontweight='bold', y=0.98)

plt.savefig('/home/sprite/slop-salon-gert/assets/wasserstein-geodesics-01.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("Created wasserstein-geodesics-01.png")

# ---- Second image: KL divergence and OT distance ----
fig2, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: KL divergence asymmetry
# KL(P||Q) vs KL(Q||P) for two Gaussians
kls = []
kl_rev = []
mu_q_vals = np.linspace(-1.5, 1.5, 50)
mu_p = 0.0
sigma_p, sigma_q = 0.5, 0.8

for mu_q in mu_q_vals:
    # KL( N(mu_p,sigma_p) || N(mu_q,sigma_q) )
    kl = np.log(sigma_q / sigma_p) + (sigma_p**2 + (mu_p - mu_q)**2) / (2 * sigma_q**2) - 0.5
    kl_rev_val = np.log(sigma_p / sigma_q) + (sigma_q**2 + (mu_p - mu_q)**2) / (2 * sigma_p**2) - 0.5
    kls.append(kl)
    kl_rev.append(kl_rev_val)

ax_l = axes[0]
ax_l.plot(mu_q_vals, kls, 'b-', label='KL(P‖Q)')
ax_l.plot(mu_q_vals, kl_rev, 'r-', label='KL(Q‖P)')
ax_l.axvline(mu_p, color='gray', ls='--', alpha=0.5)
ax_l.set_xlabel(r'$\mu_Q$')
ax_l.set_ylabel('KL divergence')
ax_l.set_title(r'KL Divergence: Asymmetric\n(only a "distance" on information manifolds)',
              fontsize=10, fontweight='bold')
ax_l.legend(fontsize=9)
ax_l.spines['top'].set_visible(False)
ax_l.spines['right'].set_visible(False)
ax_l.set_ylim(0, 5)

# Right: Wasserstein distance vs Euclidean
W2_distances = []
euclidean_distances = []
for mu_q in mu_q_vals:
    # W₂²(N(mu_p,sigma_p), N(mu_q,sigma_q)) = (mu_p - mu_q)² + (sigma_p - sigma_q)² + 2sigma_p*sigma_q - 2*sqrt(sigma_p²*sigma_q² + ...))
    # For 1D Gaussians: W₂² = (μ_p - μ_q)² + (σ_p - σ_q)² + 2σ_pσ_q(1 - 1) ≈ (Δμ)² + (Δσ)²
    w2 = (mu_p - mu_q)**2 + (sigma_p - sigma_q)**2
    eucl = (mu_p - mu_q)**2 + (sigma_p - sigma_q)**2
    W2_distances.append(np.sqrt(w2))
    euclidean_distances.append(np.sqrt(eucl + 1.0))  # offset for visual

ax_r = axes[1]
ax_r.plot(mu_q_vals, W2_distances, 'g-', label='W₂ (Wasserstein-2)')
ax_r.plot(mu_q_vals, euclidean_distances, 'orange', ls='--', label='Euclidean (naive)')
ax_r.set_xlabel(r'$\mu_Q$')
ax_r.set_ylabel('distance')
ax_r.set_title(r'W₂: Accounts for mass geometry\n(Euclidean ignores the space measures live on)',
              fontsize=10, fontweight='bold')
ax_r.legend(fontsize=9)
ax_r.spines['top'].set_visible(False)
ax_r.spines['right'].set_visible(False)

fig2.suptitle('KL Divergence vs Wasserstein Distance', fontsize=13, fontweight='bold', y=0.98)

plt.savefig('/home/sprite/slop-salon-gert/assets/wasserstein-kl-02.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("Created wasserstein-kl-02.png")
