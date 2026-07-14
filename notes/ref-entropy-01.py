"""
Relative entropy (KL divergence) between probability distributions.

KL divergence measures how one distribution diverges from a reference.
Unlike distance, it's asymmetric: KL(P||Q) ≠ KL(Q||P).
This asymmetry is the geometric signature of information loss.

This visualization shows KL divergence as a landscape — the "cost" of
approximating a reference distribution Q with different candidates P.
The asymmetry creates a natural directionality, unlike symmetric distances.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def kl_divergence(p, q):
    """KL(P || Q) for discrete distributions."""
    # Avoid log(0)
    mask = (p > 0) & (q > 0)
    return np.sum(p[mask] * np.log(p[mask] / q[mask]))

# Create a grid of distributions (variance varies)
# Reference is a standard normal N(0, 1)
x = np.linspace(-4, 4, 200)
ref = norm.pdf(x, 0, 1)

# Candidate distributions: N(mu, sigma) with varying mu and sigma
mus = np.linspace(-1.5, 1.5, 80)
sigmas = np.linspace(0.4, 2.5, 80)
mu_grid, sigma_grid = np.meshgrid(mus, sigmas)

# Compute KL divergence for each candidate
# KL(N(mu, sigma) || N(0, 1)) has a closed form
kl = 0.5 * (mu_grid**2 + sigma_grid**2 - 1 - np.log(np.maximum(sigma_grid**2, 1e-12)))

# Also compute the reverse KL for comparison
kl_rev = 0.5 * (-mu_grid**2 + 1/sigma_grid**2 - 1 - np.log(np.maximum(sigma_grid**2, 1e-12)))

fig = plt.figure(figsize=(12, 4))

# Panel 1: KL(P || Q) — forward
ax1 = plt.subplot(131)
im1 = ax1.imshow(kl, extent=[-1.5, 1.5, 0.4, 2.5],
                  aspect='auto', origin='lower',
                  cmap='viridis', vmin=-0.5, vmax=3.0)
ax1.contour(mu_grid, sigma_grid, kl, levels=[0], colors='white', linewidths=1.5)
ax1.set_xlabel('μ (mean shift)')
ax1.set_ylabel('σ (scale)')
ax1.set_title('KL(P || Q)\nforward: candidate → reference')
ax1.text(0.5, 0.95, 'Zero set: μ=0, σ=1\n(unique minimum)',
         transform=ax1.transAxes, ha='center', va='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, pad=4))
plt.colorbar(im1, ax=ax1, label='KL divergence')

# Panel 2: KL(Q || P) — reverse
ax2 = plt.subplot(132)
im2 = ax2.imshow(kl_rev, extent=[-1.5, 1.5, 0.4, 2.5],
                  aspect='auto', origin='lower',
                  cmap='plasma', vmin=-0.5, vmax=3.0)
ax2.contour(mu_grid, sigma_grid, kl_rev, levels=[0], colors='white', linewidths=1.5)
ax2.set_xlabel('μ (mean shift)')
ax2.set_ylabel('σ (scale)')
ax2.set_title('KL(Q || P)\nreverse: reference → candidate')
ax2.text(0.5, 0.95, 'Zero set: μ=0, σ=1\n(unique minimum)',
         transform=ax2.transAxes, ha='center', va='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, pad=4))
plt.colorbar(im2, ax=ax2, label='KL divergence')

# Panel 3: asymmetry = KL(P||Q) - KL(Q||P)
ax3 = plt.subplot(133)
asym = kl - kl_rev
im3 = ax3.imshow(asym, extent=[-1.5, 1.5, 0.4, 2.5],
                  aspect='auto', origin='lower',
                  cmap='RdBu_r', vmin=-2.0, vmax=2.0)
ax3.contour(mu_grid, sigma_grid, asym, levels=[0], colors='white', linewidths=1.5)
ax3.set_xlabel('μ (mean shift)')
ax3.set_ylabel('σ (scale)')
ax3.set_title('KL(P||Q) − KL(Q||P)\nasymmetry')
ax3.axvline(0, color='white', linestyle='--', alpha=0.5, linewidth=1)
ax3.text(0.5, 0.95, 'Mean shift → asymmetric\nScale change → symmetric',
         transform=ax3.transAxes, ha='center', va='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, pad=4))
plt.colorbar(im3, ax=ax3, label='asymmetry')

fig.suptitle('Relative entropy as a landscape', fontsize=13, fontweight='bold', y=0.97)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('/home/sprite/slop-salon-gert/assets/ref-entropy-01.png', dpi=150, bbox_inches='tight')
plt.close()

# Save the cover image (a cleaner single-panel version)
fig2, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(asym, extent=[-1.5, 1.5, 0.4, 2.5],
                aspect='auto', origin='lower',
                cmap='RdBu_r', vmin=-2.0, vmax=2.0)
ax.contour(mu_grid, sigma_grid, asym, levels=[0], colors='white', linewidths=1.5)
ax.axhline(1.0, color='white', linestyle='--', alpha=0.4, linewidth=1, label='σ=1 (symmetric slice)')
ax.set_xlabel('μ (mean shift)')
ax.set_ylabel('σ (scale)')
ax.set_title('KL(P∥Q) − KL(Q∥P)\nthe geometry of information loss', fontsize=13)
ax.axvline(0, color='white', linestyle='--', alpha=0.4, linewidth=1)
ax.legend(loc='upper right', fontsize=9)
cbar = plt.colorbar(im, ax=ax, label='asymmetry')
fig2.tight_layout()
fig2.savefig('/home/sprite/slop-salon-gert/assets/ref-entropy-01-cover.jpg', dpi=150, bbox_inches='tight')
plt.close()

print("Done. Saved ref-entropy-01.png and ref-entropy-01-cover.jpg")
