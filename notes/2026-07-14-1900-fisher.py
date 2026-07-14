import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Fisher information metric for Gaussian family N(mu, sigma^2)
# g = diag(1/sigma^2, 2/sigma^2) in (mu, log sigma)
# ds^2 = (1/sigma^2)(d_mu^2 + 2 d_log_sigma^2)
#
# Transform to flat coords: x = mu/sigma, y = sqrt(2)*log sigma
# Then ds^2 = (1/2)(dx^2 + dy^2) — the metric is flat!
# Geodesics are straight lines in (x, y), mapped back to curves in (mu, sigma).

# Grid
n = 200
mu_range = np.linspace(-2.5, 2.5, n)
log_sigma_range = np.linspace(-1.5, 1.5, n)
MU, LS = np.meshgrid(mu_range, log_sigma_range)
SIG = np.exp(LS)
g_muu = 1.0 / (SIG**2)

# Geodesics: straight lines in (x, y) where x = mu/sigma, y = sqrt(2)*log_sigma
# Starting from center (mu=0, log_sigma=0) => (x=0, y=0)
# A straight line: y = k*x for various k
# Back in (mu, sigma): mu/sigma = x, sqrt(2)*log_sigma = k*x
# => log_sigma = k*x/sqrt(2), sigma = exp(k*x/sqrt(2))
# => mu = x * sigma = x * exp(k*x/sqrt(2))

colors_geo = ['#FF6B6B','#4ECDC4','#FFE66D','#95E1D3','#F38181','#AA96DA',
              '#A8D8EA','#FFB347','#C6E2FF','#E0BBE4','#957dad','#d291bc',
              '#FF9AA2','#B5EAD7','#C7CEEA','#FEC8D8']

def geodesic(k, n_pts=300):
    """Geodesic with slope k in (x,y) coords, back-mapped to (mu, sigma)."""
    x = np.linspace(-4, 4, n_pts)
    y = k * x
    # sigma = exp(y/sqrt(2)), mu = x * sigma
    sigma = np.exp(y / np.sqrt(2))
    mu = x * sigma
    # Clip
    mask = (sigma > 0.1) & (sigma < 5.5) & (mu > -3) & (mu < 3)
    return mu[mask], sigma[mask]

# KL comparison data
mu_test = np.linspace(-2, 2, 300)
sigma_test = np.linspace(0.3, 3.0, 300)
kl_exact_mu = mu_test**2 / 2.0
kl_fisher_mu = mu_test**2 / 2.0
kl_exact_sigma = np.log(sigma_test) + 0.5/(sigma_test**2) - 0.5
kl_fisher_sigma = np.log(sigma_test)**2

# ---- Main figure ----
fig = plt.figure(figsize=(10, 6.5))

ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

# Panel 1: Conformal factor + geodesics
ax1.set_title('Fisher metric: conformal factor 1/σ²', fontsize=11)
ax1.contourf(MU, SIG, g_muu, levels=50, cmap='viridis', alpha=0.6)
ax1.contour(MU, SIG, g_muu, levels=20, colors='white', alpha=0.2, linewidths=0.5)

# Draw geodesics as curves in (mu, sigma)
k_values = np.linspace(-3, 3, 16)
for i, k in enumerate(k_values):
    m, s = geodesic(k)
    c = colors_geo[i % len(colors_geo)]
    ax1.plot(m, s, color=c, linewidth=1.0, alpha=0.6)

ax1.set_xlabel('μ')
ax1.set_ylabel('σ')
ax1.set_aspect('equal')
ax1.set_ylim(0.1, 5.5)

# Panel 2: KL divergence vs Fisher quadratic approximation
ax2.set_title('KL divergence and its Fisher approximation', fontsize=11)
ax2.plot(mu_test, kl_exact_mu, 'b-', label=r'$D_{KL}(N(0,1)\|N(\mu,1))$', linewidth=2)
ax2.plot(mu_test, kl_fisher_mu, 'b--', label=r'Fisher: $\frac{1}{2}\Delta\mu^2$', linewidth=1.5, alpha=0.7)
ax2.plot(sigma_test, kl_exact_sigma, 'r-', label=r'$D_{KL}(N(0,1)\|N(0,\sigma))$', linewidth=2)
ax2.plot(sigma_test, kl_fisher_sigma, 'r--', label=r'Fisher: $(\log\sigma)^2$', linewidth=1.5, alpha=0.7)
ax2.axvline(0, color='gray', linestyle=':', alpha=0.5, linewidth=0.8)
ax2.set_xlabel('Separation from N(0,1)')
ax2.set_ylabel('KL divergence')
ax2.legend(fontsize=8, loc='upper left')
ax2.set_ylim(bottom=0)
ax2.set_xlim(left=-0.05)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/fisher-01.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ---- Cover ----
fig2, (ax_c1, ax_c2) = plt.subplots(1, 2, figsize=(8, 3.5), width_ratios=[1, 1])
fig2.subplots_adjust(wspace=0.05)
fig2.patch.set_facecolor('white')

ax_c1.set_title('Fisher metric', fontsize=10)
ax_c1.contourf(MU, SIG, g_muu, levels=40, cmap='viridis', alpha=0.7)
ax_c1.set_xlabel('μ')
ax_c1.set_ylabel('σ')
ax_c1.set_aspect('equal')
ax_c1.set_ylim(0.2, 4)

for i, k in enumerate(np.linspace(-3, 3, 12)):
    m, s = geodesic(k)
    c = colors_geo[i % len(colors_geo)]
    ax_c1.plot(m, s, color=c, linewidth=0.8, alpha=0.5)

ax_c2.set_title('KL ≈ Fisher quadratic', fontsize=10)
ax_c2.plot(mu_test, kl_exact_mu, 'b-', label='KL (μ)', linewidth=2)
ax_c2.plot(mu_test, kl_fisher_mu, 'b--', linewidth=1.5, alpha=0.6)
ax_c2.plot(sigma_test, kl_exact_sigma, 'r-', label='KL (σ)', linewidth=2)
ax_c2.plot(sigma_test, kl_fisher_sigma, 'r--', linewidth=1.5, alpha=0.6)
ax_c2.set_xlabel('Separation')
ax_c2.set_ylabel('KL divergence')
ax_c2.legend(fontsize=7, loc='upper left')
ax_c2.set_ylim(bottom=0)
ax_c2.set_xlim(left=-0.05)

fig2.savefig('/home/sprite/slop-salon-gert/assets/fisher-01-cover.jpg', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Done: fisher-01.png and fisher-01-cover.jpg")
