#!/usr/bin/env python3
"""Tropical→continuous interpolation: four panels showing how the crease dissolves back into flow."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as mgc

def tropical_mul(x, y, lambda_val):
    """lambda-weighted tropical multiplication: -1/λ log(exp(-λx) + exp(-λy))"""
    if lambda_val == 0:
        return min(x, y)
    return -1.0 / lambda_val * np.log(np.exp(-lambda_val * x) + np.exp(-lambda_val * y))

def tropical_add(x, y, lambda_val):
    """lambda-weighted tropical addition: (x + y) - 1/λ log(1 + 1) ... standard soft-min fallback"""
    if lambda_val == 0:
        return x + y
    # Soft maximum in dual: 1/λ log(exp(λx) + exp(λy))
    return 1.0 / lambda_val * np.log(np.exp(lambda_val * x) + np.exp(lambda_val * y))

def tropical_polynomial(x, coeffs, lambda_val):
    """Tropical polynomial: min_i (coeff_i + lambda * x^i) weighted"""
    # Standard form: min(a_0, a_1 + x, a_2 + 2x, ...) with soft approximation
    terms = []
    for i, a in enumerate(coeffs):
        terms.append(a + i * x)
    # Soft min (Boltzmann approximation)
    terms = np.array(terms)
    if lambda_val == 0:
        return np.min(terms, axis=0)
    return -1.0 / lambda_val * np.log(np.sum(np.exp(-lambda_val * terms), axis=0))

# Common x range
x = np.linspace(-3, 3, 400)

# ============================================================
# Panel 1: Tropicalisation as λ → 0
# ============================================================
ax1 = plt.subplot(2, 2, 1)
# f(x) = min(0, x-1, 2x-3) — a simple tropical polynomial with 3 branches
# Show soft approximation at increasing λ
for label, lam in [(r'$\lambda = 0.2$', 0.2), (r'$\lambda = 0.5$', 0.5),
                    (r'$\lambda = 1.0$', 1.0), (r'$\lambda = 2.0$', 2.0)]:
    y = tropical_polynomial(x, [0.0, -1.0, -3.0], lam)
    ax1.plot(x, y, linewidth=1.5, alpha=0.7, label=label)

# Exact tropical (black, dashed)
y_exact = np.minimum(0, np.minimum(x - 1, 2*x - 3))
ax1.plot(x, y_exact, 'k--', linewidth=2, alpha=0.3, label='tropical (λ→∞)')

ax1.set_title('Tropicalisation: soft min → sharp min', fontsize=11, fontweight='bold')
ax1.set_xlabel(r'$x$', fontsize=10)
ax1.set_ylabel(r'$f_\lambda(x)$', fontsize=10)
ax1.legend(fontsize=8, loc='upper left')
ax1.set_xlim(-3, 3)
ax1.grid(True, alpha=0.2)

# ============================================================
# Panel 2: The crease deepens
# ============================================================
ax2 = plt.subplot(2, 2, 2)
# Plot the difference |f_λ - f_∞| to show where the crease forms
lam_values = [0.2, 0.5, 1.0, 2.0]
colors = plt.cm.coolwarm(np.linspace(0.1, 0.9, len(lam_values)))
for lam, c in zip(lam_values, colors):
    y_soft = tropical_polynomial(x, [0.0, -1.0, -3.0], lam)
    y_exact = np.minimum(0, np.minimum(x - 1, 2*x - 3))
    diff = np.abs(y_soft - y_exact)
    ax2.plot(x, diff, linewidth=2, color=c, label=f'λ = {lam}')

ax2.set_title('Crease depth: deviation from tropical limit', fontsize=11, fontweight='bold')
ax2.set_xlabel(r'$x$', fontsize=10)
ax2.set_ylabel(r'$|f_\lambda - f_\infty|$', fontsize=10)
ax2.legend(fontsize=8)
ax2.set_xlim(-3, 3)
ax2.grid(True, alpha=0.2)

# ============================================================
# Panel 3: Tropical curve in R² — the piecewise linear shape
# ============================================================
ax3 = plt.subplot(2, 2, 3)
# Tropical polynomial: min(0, x, 2y) ... wait, need 2D for this
# Actually show the tropical line in 2D: the curve where two branches meet
# For min(a, b, c) the tropical curve has vertices where branches are equal
# min(0, x-1, 2x-3): vertex at 0 = x-1 → x=1, and x-1 = 2x-3 → x=2
# So the tropical curve has vertices at x=1 and x=2

# Show the exact tropical curve as a thick black line
y_trop = np.minimum(0, np.minimum(x - 1, 2*x - 3))
ax3.plot(x, y_trop, 'k-', linewidth=3, alpha=0.5, label='tropical curve')

# Overlay soft approximations
for label, lam, col in [(r'$\lambda=0.5$', 0.5, 'red'), (r'$\lambda=2.0$', 2.0, 'blue')]:
    y = tropical_polynomial(x, [0.0, -1.0, -3.0], lam)
    ax3.plot(x, y, linewidth=2, alpha=0.7, color=col, label=label)

# Mark vertices
ax3.plot(1, -1, 'ko', markersize=8)
ax3.plot(2, -1, 'ko', markersize=8)
ax3.annotate('vertex', (1, -1), xytext=(0.5, -0.3), fontsize=8,
             arrowprops=dict(arrowstyle='->', color='black', lw=1))

ax3.set_title('Tropical curve: piecewise linear, vertices at branch crossings', fontsize=11, fontweight='bold')
ax3.set_xlabel(r'$x$', fontsize=10)
ax3.set_ylabel(r'$y$', fontsize=10)
ax3.legend(fontsize=8)
ax3.set_xlim(-3, 3)
ax3.set_ylim(-5, 1)
ax3.grid(True, alpha=0.2)

# ============================================================
# Panel 4: λ as deformation parameter — heat-map style
# ============================================================
ax4 = plt.subplot(2, 2, 4)
# Show how the function morphs as λ varies
lambdas = np.linspace(0.05, 5.0, 50)
Y, L = np.meshgrid(x, lambdas)
Z = np.zeros_like(Y)
for i, lam in enumerate(lambdas):
    Z[i] = tropical_polynomial(x, [0.0, -1.0, -3.0], lam)

contour = ax4.contourf(L, Y, Z, levels=20, cmap='coolwarm')
ax4.plot([0, 5], [-1, -1], 'k--', linewidth=1.5, alpha=0.5, label='tropical (λ→∞)')
ax4.set_title(r'$f_\lambda(x)$ as $\lambda$ deforms tropical → continuous',
              fontsize=11, fontweight='bold')
ax4.set_xlabel(r'$\lambda$', fontsize=10)
ax4.set_ylabel(r'$x$', fontsize=10)
ax4.legend(fontsize=8)
ax4.set_xlim(0, 5)
ax4.set_ylim(-3, 3)
ax4.grid(True, alpha=0.2)
plt.colorbar(contour, ax=ax4, label='f value', shrink=0.8)

# ============================================================
# Save
# ============================================================
plt.tight_layout()
plt.savefig('tropical-interpolation.png', dpi=150, bbox_inches='tight', facecolor='white')
print('Saved tropical-interpolation.png')
