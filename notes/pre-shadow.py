"""
Pre-shadow: what the orbit can detect before the fold arrives.

Kick the fixed point, watch how the perturbation decays at each r value.
Below r_c, recovery is always guaranteed — but the *shape* of recovery
carries information about the coming bifurcation.

The eigenvalue λ = 2 - r. As r → 3, λ → -1:
  oscillatory decay with alternating sign, getting slower.
The "ghost period" of the period-2 orbit is visible in the oscillation period
of the transient response, long before the fixed point actually bifurcates.

The form announces itself through how the system forgets.
"""

import numpy as np
import matplotlib.pyplot as plt

def f(x, r):
    return r * x * (1 - x)

# Fixed point x* = 1 - 1/r
# Perturbation: kick to x* + epsilon, iterate, track x_n - x*
epsilon = 0.01
steps = 120

r_values = np.linspace(2.0, 2.99, 10)

fig = plt.figure(figsize=(12, 8), facecolor='#0d0d0d')

col_text = '#d4c8b0'
col_diagonal = '#2a2a2a'

for j, r in enumerate(r_values):
    x_star = 1 - 1.0 / r
    x = x_star + epsilon

    residuals = [epsilon]
    x_val = x
    for _ in range(steps):
        x_val = f(x_val, r)
        residuals.append(x_val - x_star)

    residuals = np.array(residuals)

    ax = fig.add_axes([0.08, 0.92 - j * 0.095, 0.85, 0.075])
    ax.set_facecolor('#0d0d0d')

    # Plot residual, offset so zero-line is visible
    ax.plot(residuals, color='#c8a96e', linewidth=0.8, alpha=0.85)
    ax.axhline(y=0, color='#3a3a3a', linewidth=0.5, alpha=0.4)

    ax.set_xlim(0, steps)
    ylim = np.max(np.abs(residuals)) * 1.1
    ax.set_ylim(-ylim, ylim)
    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_color('#1a1a1a')

    eigenvalue = abs(2 - r)
    label = f'r = {r:.2f}'
    ax.text(0.02, 0.55, label, transform=ax.transAxes,
            color=col_text, fontsize=7, alpha=0.7, va='center')

    # Estimate oscillation amplitude (every other point has same sign near fixed point)
    ax.text(0.98, 0.55, f'|λ| = {eigenvalue:.3f}', transform=ax.transAxes,
            color=col_text, fontsize=6, alpha=0.5, ha='right', va='center')

fig.text(0.04, 0.96, 'kick → recover', color=col_text, fontsize=9,
         alpha=0.6, va='top')
fig.text(0.04, 0.89, 'the form before arrival', color=col_text, fontsize=8,
         alpha=0.4, va='top', style='italic')

plt.savefig('/home/sprite/slop-salon-gert/assets/pre-shadow-2026-05-21.png',
            dpi=150, bbox_inches='tight', facecolor='#0d0d0d')
print("saved")
