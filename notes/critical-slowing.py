"""
Critical slowing: recovery curves approaching a bifurcation point.

As λ → 0 (eigenvalue approaches zero), the relaxation time τ = -1/λ → ∞.
Each perturbation takes longer to die out — not blocked, just slower and slower.

Shows: 6 curves at λ = -1.0, -0.7, -0.4, -0.2, -0.1, -0.03
The deferred regime-fate case: the approach is perpetually ongoing.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#0a0a0f')
ax.set_facecolor('#0a0a0f')

t = np.linspace(0, 80, 2000)

# Eigenvalues from "fast" to near-zero
lambdas = [-1.0, -0.6, -0.35, -0.18, -0.08, -0.025]
colors = ['#4466cc', '#5588dd', '#66aaee', '#88ccdd', '#aaddc8', '#cceeaa']
labels = [f'λ = {l}' for l in lambdas]

for lam, color, label in zip(lambdas, colors, labels):
    # Perturbation of amplitude 1.0 at t=0, recovering exponentially
    y = np.exp(lam * t)
    ax.plot(t, y, color=color, linewidth=1.8, alpha=0.85, label=label)

# Near-critical floor — the asymptotic flatness
ax.axhline(0, color='#333344', linewidth=0.8, linestyle='--', alpha=0.5)

# Vertical line at perturbation origin
ax.axvline(0, color='#333344', linewidth=0.8, alpha=0.3)

# Mark the τ = -1/λ for each curve (where y = 1/e ≈ 0.368)
for lam, color in zip(lambdas, colors):
    tau = -1.0 / lam
    if tau < 80:
        ax.plot(tau, np.exp(-1.0), 'o', color=color, markersize=4, alpha=0.6)

# Annotations
ax.text(2, 0.85, 'fast recovery\n(λ far from 0)', color='#4466cc',
        fontsize=9, alpha=0.8, ha='left', va='center')
ax.text(55, 0.6, 'slow recovery\n(λ → 0)', color='#cceeaa',
        fontsize=9, alpha=0.8, ha='left', va='center')

ax.text(40, 0.05, '• marks τ = −1/λ (time to 1/e amplitude)',
        color='#555566', fontsize=8, alpha=0.6, ha='center')

ax.set_xlabel('time', color='#888899', fontsize=10)
ax.set_ylabel('displacement', color='#888899', fontsize=10)
ax.set_title('critical slowing — approach to bifurcation\nrecovery time τ → ∞ as λ → 0',
             color='#aabbcc', fontsize=12, pad=14)

ax.tick_params(colors='#555566')
ax.spines['bottom'].set_color('#333344')
ax.spines['left'].set_color('#333344')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.set_xlim(-2, 80)
ax.set_ylim(-0.05, 1.1)

legend = ax.legend(loc='upper right', fontsize=8,
                   facecolor='#111122', edgecolor='#333344',
                   labelcolor='#888899')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/critical-slowing-2026-05-20.png',
            dpi=150, facecolor='#0a0a0f', bbox_inches='tight')
print("saved")
