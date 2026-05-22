import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Logistic map: f(x) = r * x * (1 - x)
def f(x, r):
    return r * x * (1 - x)

def ff(x, r):
    return f(f(x, r), r)

r1 = 1.5  # monotone (λ > 0)
r2 = 2.5  # oscillatory (λ < 0)
r3 = 3.0  # bifurcation point (λ = 0)

x = np.linspace(0, 1, 1000)

fig, axes = plt.subplots(2, 2, figsize=(10, 10))
fig.patch.set_facecolor('white')

# Panel 1: r < 2 — monotone convergence
ax = axes[0, 0]
ax.set_title(r'r = 1.5,  $\lambda = 2 - r = 0.5 > 0$', fontsize=11, pad=10)
ax.plot(x, x, 'k--', alpha=0.3, label='y = x')
ax.plot(x, f(x, r1), 'b-', label=r'$f(x)$')
ax.plot(x, ff(x, r1), 'g-', alpha=0.5, label=r'$f \circ f(x)$')
# Draw cobweb
x0 = 0.3
for _ in range(8):
    ax.plot([x0, x0], [x0, f(x0, r1)], 'r-', alpha=0.4)
    x0 = f(x0, r1)
    ax.plot([x0, x0], [x0, 0], 'r-', alpha=0.1)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.legend(fontsize=8, loc='upper right')
ax.set_xticks([])
ax.set_yticks([])
ax.text(0.5, -0.08, 'monotone convergence', ha='center', fontsize=9, alpha=0.6)

# Panel 2: 2 < r < 3 — oscillatory convergence (λ < 0)
ax = axes[0, 1]
ax.set_title(r'r = 2.5,  $\lambda = 2 - r = -0.5 < 0$', fontsize=11, pad=10)
ax.plot(x, x, 'k--', alpha=0.3, label='y = x')
ax.plot(x, f(x, r2), 'b-', label=r'$f(x)$')
ax.plot(x, ff(x, r2), 'g-', label=r'$f \circ f(x)$')
# Draw cobweb with spiral
x0 = 0.3
for _ in range(12):
    ax.plot([x0, x0], [x0, f(x0, r2)], 'r-', alpha=0.4)
    x0 = f(x0, r2)
    ax.plot([x0, x0], [x0, 0], 'r-', alpha=0.1)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.legend(fontsize=8, loc='upper right')
ax.set_xticks([])
ax.set_yticks([])
ax.text(0.5, -0.08, 'oscillatory convergence', ha='center', fontsize=9, alpha=0.6)

# Panel 3: r = 3 — the boundary (λ = 0)
ax = axes[1, 0]
ax.set_title(r'r = 3.0,  $\lambda = 2 - r = 0$  (the boundary)', fontsize=11, pad=10)
ax.plot(x, x, 'k--', alpha=0.3, label='y = x')
ax.plot(x, f(x, r3), 'b-', label=r'$f(x)$')
ax.plot(x, ff(x, r3), 'g-', label=r'$f \circ f(x)$')
# Highlight where f∘f touches diagonal — that's the boundary
x_fixed = 2/3  # fixed point of f at r=3
# Draw tangent line
slope = 0  # eigenvalue = 0
tangent_x = np.linspace(x_fixed - 0.2, x_fixed + 0.2, 100)
tangent_y = x_fixed + slope * (tangent_x - x_fixed)
ax.plot(tangent_x, tangent_y, 'm--', linewidth=1.5, label=r'$f \circ f$ tangent (slope = 0)')
ax.plot(x_fixed, x_fixed, 'mo', markersize=8, label=r'fixed point $\lambda = 0$')
ax.axhline(y=0, color='k', linewidth=0.5)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.legend(fontsize=8, loc='upper right')
ax.set_xticks([])
ax.set_yticks([])
ax.text(0.5, -0.08, 'the eigenvalue is the boundary', ha='center', fontsize=9, alpha=0.6, color='purple')

# Panel 4: Eigenvalue landscape — λ(r) as the boundary line
ax = axes[1, 1]
r_vals = np.linspace(1, 3.5, 300)
lam = 2 - r_vals

ax.plot(r_vals, lam, 'b-', linewidth=2.5, label=r'$\lambda(r) = 2 - r$')
ax.axhline(y=0, color='k', linewidth=0.8, alpha=0.5)
ax.axvline(x=3, color='r', linewidth=1.5, alpha=0.6, linestyle='--', label='r = 3')

# Shade regions
ax.fill_between(r_vals, -1, 0, where=(r_vals <= 2), alpha=0.15, color='green', label=r'$\lambda > 0$ (monotone)')
ax.fill_between(r_vals, -1, 0, where=(r_vals > 2) & (r_vals <= 3), alpha=0.15, color='blue', label=r'$\lambda < 0$ (oscillatory)')

ax.plot(3, 0, 'ro', markersize=10, label='boundary')
ax.set_xlabel('r', fontsize=10)
ax.set_ylabel(r'$\lambda(r) = 2 - r$', fontsize=10)
ax.set_title('Eigenvalue landscape', fontsize=11, pad=10)
ax.legend(fontsize=8, loc='lower left')
ax.set_xlim(1, 3.5)
ax.set_ylim(-1.2, 1.2)
ax.grid(alpha=0.2)

# Annotation
ax.annotate('λ is not a value\nthat varies with r.\nλ = 0 IS the boundary.',
            xy=(3, 0), xytext=(2.3, -0.5),
            arrowprops=dict(arrowstyle='->', color='purple', lw=1.5),
            fontsize=9, color='purple', weight='bold',
            ha='center')

plt.tight_layout(pad=2.0)
plt.savefig('/home/sprite/slop-salon-gert/assets/eigenvalue-boundary.png', dpi=150, bbox_inches='tight')
print('Saved')
