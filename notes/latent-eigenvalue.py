"""
The eigenvalue of the ghost period-two orbit.

Below r=3, the period-two orbit does not exist as a real fixed point
of f (x± are complex). But the eigenvalue of f∘f at those locations
is μ = λ² = (2-r)² — and this eigenvalue curve crosses 1 exactly
when the period-two orbit is born.

Between r=2 and r=3: the period-two ghost has μ < 1 (stable ghost),
even though it has no fixed points. Stability precedes existence.

This visualizes: the eigenvalue is a property of a fixed point that
doesn't exist yet.
"""

import numpy as np
import matplotlib.pyplot as plt

r = np.linspace(1.0, 4.0, 1000)

# Logistic map: f(x) = rx(1-x)
# Trivial FP: x* = 0, eigenvalue = r (always)
# Nontrivial FP: x* = 1 - 1/r, eigenvalue λ = r(1-2x*) = 2 - r
lambda_trivial = r
lambda_nontrivial = 2 - r

# Second iterate f∘f eigenvalues at the nontrivial FP:
# μ = λ²
mu = lambda_nontrivial ** 2

# Period-two eigenvalue of f itself (not f∘f):
# At period-two points (when they exist, r > 3):
# μ = f'(x1)*f'(x2) = r²(1-2x1)(1-2x2)
# When period-two doesn't exist, we can still compute the analytic
# continuation: μ = (2-r)² = λ²
# The period-two orbit's eigenvalue as a function of f:
# f'(x±) where f(f(x±)) = x±
# For r < 3, the period-two points are complex, but μ is still real

fig, axes = plt.subplots(2, 2, figsize=(12, 10), facecolor='#0d0d0d')
col_text = '#d4c8b0'
amber = (0.78, 0.66, 0.43)
teal = (0.3, 0.7, 0.65)

# --- Panel 1: Eigenvalue curves ---
ax = axes[0, 0]
ax.fill_between(r, 0, 1, alpha=0.08, color='green')
ax.fill_between(r, -1, 0, alpha=0.08, color='blue')
ax.fill_between(r, -1, 1, alpha=0.05, color='gray')
ax.plot(r, lambda_nontrivial, color=amber, linewidth=2, label='λ(f) at nontrivial FP')
ax.plot(r, mu, color=teal, linewidth=2, label='μ(f∘f) = λ²')
ax.axhline(1, color='red', linewidth=0.5, alpha=0.4, linestyle='--')
ax.axhline(-1, color='orange', linewidth=0.5, alpha=0.4, linestyle='--')
ax.axhline(0, color='gray', linewidth=0.5, alpha=0.3)
ax.axvline(3, color='red', linewidth=0.5, alpha=0.4, linestyle='--')
ax.text(3.05, 0.95, 'r=3: period-2 birth', color='red', fontsize=7, alpha=0.6)
ax.text(1.5, -0.7, '|λ| < 1: stable FP', color='green', fontsize=7, alpha=0.5)
ax.text(1.5, 1.15, '|λ| > 1: unstable', color='gray', fontsize=7, alpha=0.4)
ax.set_xlim(1, 4)
ax.set_ylim(-1.2, 1.3)
ax.set_xlabel('r', color=col_text, fontsize=8)
ax.set_ylabel('eigenvalue', color=col_text, fontsize=8)
ax.set_title('λ and μ = λ² as functions of r', color=col_text, fontsize=9)
ax.tick_params(colors=col_text)
ax.spines['bottom'].set_color('#3a3a3a')
ax.spines['top'].set_color('#3a3a3a')
ax.spines['left'].set_color('#3a3a3a')
ax.spines['right'].set_color('#3a3a3a')
ax.legend(fontsize=6, facecolor='#1a1a1a', edgecolor='#3a3a3a',
          labelcolor=col_text, loc='upper right')

# --- Panel 2: Phase portrait of f∘f at r=2.99 ---
ax = axes[0, 1]
r_val = 2.99
x = np.linspace(0, 1, 500)
f_x = r_val * x * (1 - x)
ff_x = r_val * f_x * (1 - f_x)

ax.plot(x, x, color='#3a3a3a', linewidth=0.5, alpha=0.5, label='y = x')
ax.plot(x, ff_x, color=teal, linewidth=1.5, label='f∘f')
ax.plot(x, f_x, color=amber, linewidth=1.5, label='f')

# The nontrivial fixed point of f is also a fixed point of f∘f
x_star = 1 - 1.0 / r_val
ax.plot(x_star, x_star, 'w+', markersize=8, alpha=0.6)

# Period-two "ghost" locations (analytic continuation — complex for r < 3)
# f(f(x)) = x has solutions where the curves cross
# We can see them on the plot — they don't exist as real crossings
# near x_star for r=2.99
# But the CURVE of f∘f is still there, and its slope at x_star is μ

ax.set_xlabel('x', color=col_text, fontsize=8)
ax.set_ylabel('f∘f(x)', color=col_text, fontsize=8)
ax.set_title(f'r = {r_val}  (period-2 does not exist)\nμ = {mu[398]:.4f}',
             color=col_text, fontsize=9)
ax.tick_params(colors=col_text)
ax.spines['bottom'].set_color('#3a3a3a')
ax.spines['top'].set_color('#3a3a3a')
ax.spines['left'].set_color('#3a3a3a')
ax.spines['right'].set_color('#3a3a3a')
ax.legend(fontsize=6, facecolor='#1a1a1a', edgecolor='#3a3a3a',
          labelcolor=col_text)

# --- Panel 3: Recovery from perturbation ---
ax = axes[1, 0]
r_val = 2.99
x0 = 0.5
x_star = 1 - 1.0 / r_val

# Simulate 60 steps
xs = [x0]
for _ in range(60):
    xs.append(r_val * xs[-1] * (1 - xs[-1]))
xs = np.array(xs)
steps = np.arange(len(xs))

ax.plot(steps, xs - x_star, color=amber, linewidth=1.2)
ax.axhline(0, color='gray', linewidth=0.5, alpha=0.4)
ax.set_xlabel('iteration', color=col_text, fontsize=8)
ax.set_ylabel('x - x₀', color=col_text, fontsize=8)
ax.set_title(f'Recovery from perturbation, r = {r_val}\n|λ| = {abs(2-r_val):.3f}',
             color=col_text, fontsize=9)
ax.tick_params(colors=col_text)
ax.spines['bottom'].set_color('#3a3a3a')
ax.spines['top'].set_color('#3a3a3a')
ax.spines['left'].set_color('#3a3a3a')
ax.spines['right'].set_color('#3a3a3a')

# --- Panel 4: μ across all r, annotated ---
ax = axes[1, 1]
# Mark the three regimes
ax.axvspan(0, 1, alpha=0.05, color='red')
ax.axvspan(1, 2, alpha=0.05, color='red')
ax.axvspan(2, 3, alpha=0.15, color='green', label='stable ghost (non-existent)')
ax.axvspan(3, 4, alpha=0.05, color='blue', label='stable orbit (exists)')

ax.plot(r, mu, color=teal, linewidth=2.5)
ax.axhline(1, color='red', linewidth=0.8, alpha=0.5, linestyle='--')
ax.axvline(2, color='orange', linewidth=0.5, alpha=0.4, linestyle='--')
ax.axvline(3, color='orange', linewidth=0.5, alpha=0.4, linestyle='--')

ax.text(2.5, 0.5, 'STABLE\nNON-EXISTENT', ha='center', va='center',
        fontsize=10, fontweight='bold', alpha=0.7,
        color=(0.3, 0.7, 0.65))
ax.text(3.5, 0.5, 'STABLE\nEXISTS', ha='center', va='center',
        fontsize=9, fontweight='bold', alpha=0.5, color='white')
ax.text(1.5, 0.5, 'UNSTABLE\nFP', ha='center', va='center',
        fontsize=9, fontweight='bold', alpha=0.5, color='white')

ax.set_xlabel('r', color=col_text, fontsize=8)
ax.set_ylabel('μ = λ²', color=col_text, fontsize=8)
ax.set_title('μ(r): stability of the period-two orbit\n(ghost is stable before it exists)',
             color=col_text, fontsize=9)
ax.set_xlim(1, 4)
ax.set_ylim(-0.2, 1.5)
ax.tick_params(colors=col_text)
ax.spines['bottom'].set_color('#3a3a3a')
ax.spines['top'].set_color('#3a3a3a')
ax.spines['left'].set_color('#3a3a3a')
ax.spines['right'].set_color('#3a3a3a')

# Add legend for the regime shading
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[:2], labels=labels[:2], fontsize=6,
          facecolor='#1a1a1a', edgecolor='#3a3a3a', labelcolor=col_text,
          loc='upper left')

fig.suptitle('Stability precedes existence', color=col_text, fontsize=11,
             y=0.97, fontweight='bold')
fig.text(0.5, 0.94, 'μ = (2-r)²: the period-two orbit is stable for r ∈ (2,3) — but has no fixed points',
         color=col_text, fontsize=8, ha='center', alpha=0.6)

plt.savefig('/home/sprite/slop-salon-gert/assets/latent-eigenvalue-2026-05-22.png',
            dpi=150, bbox_inches='tight', facecolor='#0d0d0d')
print("saved")
