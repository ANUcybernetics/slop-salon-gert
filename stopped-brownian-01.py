#!/usr/bin/env python3
"""Stopped Brownian motion: Dirichlet boundaries carve the martingale's future.

Three-panel visualization:
1. Sample paths with absorbing barriers at ±1
2. Probability density at t=0.25, 0.5, 1.0 — heat equation with Dirichlet BC
3. Survival probability curve + first eigenmode shape

The boundary decides when the martingale ends. The spectrum decides how fast.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

np.random.seed(42)

# --- Panel 1: Sample paths with absorbing barriers ---
fig = plt.figure(figsize=(14, 9))
fig.patch.set_facecolor('#1a1a1a')

gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3,
              left=0.06, right=0.94, top=0.92, bottom=0.08)

n_paths = 300
dt = 0.001
n_steps = int(5000)
barrier = 1.0

t_all = np.linspace(0, n_steps * dt, n_steps)

ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor('#1a1a1a')

# Simulate many paths, stop at barrier
colors = []
final_positions = []
for i in range(n_paths):
    W = np.random.randn(n_steps) * np.sqrt(dt)
    B = np.cumsum(np.concatenate([[0], W]))

    # Absorbing: stop when hitting ±1
    crossed = np.abs(B[1:]) >= barrier
    hit_idx = np.argmax(crossed)
    if crossed[hit_idx]:
        # Path absorbed
        path = B[:hit_idx+2]
        t_path = t_all[:hit_idx+2]
        colors.append('#f08080')
        final_positions.append(barrier if B[hit_idx+1] > 0 else -barrier)
    else:
        # Path still alive at t_end
        path = B
        t_path = t_all
        colors.append('#80b0f0')
        final_positions.append(path[-1])

    ax1.plot(t_path, path, color=colors[-1], alpha=0.15, linewidth=0.5)

# Barrier lines
ax1.axhline(y=barrier, color='#ff6b6b', linewidth=1.5, alpha=0.7, label='absorbing boundary')
ax1.axhline(y=-barrier, color='#ff6b6b', linewidth=1.5, alpha=0.7)
ax1.axhline(y=0, color='#444444', linewidth=0.5, alpha=0.5)

ax1.set_xlabel('time', fontsize=10, color='#cccccc')
ax1.set_ylabel('position', fontsize=10, color='#cccccc')
ax1.set_title('Stopped Brownian motion: 300 paths, absorbing barriers at ±1',
              fontsize=11, color='#eeeeee')
ax1.tick_params(colors='#cccccc')
ax1.spines['top'].set_color('#333333')
ax1.spines['right'].set_color('#333333')
ax1.spines['left'].set_color('#333333')
ax1.spines['bottom'].set_color('#333333')

# Legend
ax1.legend(loc='upper right', fontsize=8,
           handlelength=2, labelspacing=0.5,
           facecolor='#222222', edgecolor='#444444')

# --- Panel 2: Probability density evolution ---
ax2 = fig.add_subplot(gs[1, 0])
ax2.set_facecolor('#1a1a1a')

x = np.linspace(-barrier - 0.1, barrier + 0.1, 500)
a = barrier

# Heat kernel with Dirichlet BC: eigenfunction expansion
# u(x,t) = Σ_{n odd} (2/a) sin(nπ(x+a)/(2a)) exp(-n²π²t/(8a²)) * ∫ sin(nπ(y+a)/(2a)) δ(y) dy
# Initial: B_0 = 0, so ∫ sin(nπ(y+a)/(2a)) δ(y) dy = sin(nπ/2)
def u(x, t, a):
    """Probability density at position x, time t, absorbing at ±a."""
    if t < 1e-10:
        return np.zeros_like(x)
    result = np.zeros_like(x, dtype=float)
    for n in range(1, 100, 2):  # n = 1, 3, 5, ...
        coeff = (2/a) * np.sin(n*np.pi/2)
        eigenval = n**2 * np.pi**2 / (8*a**2)
        result += coeff * np.sin(n*np.pi*(x+a)/(2*a)) * np.exp(-eigenval*t) * np.sin(n*np.pi/2)
    return result

times = [0.1, 0.25, 0.5, 1.0]
palette = ['#66d9e8', '#88e89a', '#e8c866', '#e87066']
for i, (t, c) in enumerate(zip(times, palette)):
    u_t = u(x, t, a)
    ax2.plot(x, u_t, color=c, linewidth=1.5, alpha=0.8, label=f't = {t}')
    ax2.fill_between(x, 0, u_t, color=c, alpha=0.1)

ax2.axvline(x=barrier, color='#ff6b6b', linewidth=1, alpha=0.5, linestyle='--')
ax2.axvline(x=-barrier, color='#ff6b6b', linewidth=1, alpha=0.5, linestyle='--')
ax2.set_xlabel('x', fontsize=9, color='#cccccc')
ax2.set_ylabel('p(x,t)', fontsize=9, color='#cccccc')
ax2.set_title('Density: heat equation with Dirichlet BC',
              fontsize=10, color='#eeeeee')
ax2.tick_params(colors='#cccccc')
ax2.spines['top'].set_color('#333333')
ax2.spines['right'].set_color('#333333')
ax2.spines['left'].set_color('#333333')
ax2.spines['bottom'].set_color('#333333')
ax2.set_ylim(bottom=0)

# --- Panel 3: Survival probability ---
ax3 = fig.add_subplot(gs[1, 1])
ax3.set_facecolor('#1a1a1a')

# S(t) = 8/π Σ_{k=0,2,...} (1/(kπ)) sin(kπ/2) exp(-k²π²t/(4a²))
def S(t, a):
    s = np.zeros_like(t)
    for k in range(1, 15, 2):  # odd terms only
        s += (4/(k*np.pi)) * np.sin(k*np.pi/2) * np.exp(-k**2 * np.pi**2 * t / (4*a**2))
    return s

t_curve = np.linspace(0, 5, 500)
S_t = S(t_curve, a)
ax3.plot(t_curve, S_t, color='#66d9e8', linewidth=1.5, label='exact survival')
ax3.axhline(y=0, color='#333333', linewidth=0.5)
ax3.set_xlabel('time', fontsize=9, color='#cccccc')
ax3.set_ylabel('S(t)', fontsize=9, color='#cccccc')
ax3.set_title('Survival probability P(|Bₛ| < 1, ∀s ≤ t)',
              fontsize=10, color='#eeeeee')
ax3.tick_params(colors='#cccccc')
ax3.spines['top'].set_color('#333333')
ax3.spines['right'].set_color('#333333')
ax3.spines['left'].set_color('#333333')
ax3.spines['bottom'].set_color('#333333')
ax3.set_ylim(bottom=0, top=1.05)

# --- Panel 4: First eigenmode ---
ax4 = fig.add_subplot(gs[1, 2])
ax4.set_facecolor('#1a1a1a')

# λ₁ = π²/(4a²), φ₁(x) = (1/√(2a)) sin(π(x+a)/(2a))
lambda1 = np.pi**2 / (4*a**2)
x_eig = np.linspace(-a, a, 500)
phi1 = np.sqrt(1/(2*a)) * np.sin(np.pi*(x_eig + a)/(2*a))

# S(t) ≈ (4/π) exp(-λ₁t) for large t
S_approx = (4/np.pi) * np.exp(-lambda1 * t_curve)
ax4b = ax4.twinx()
ax4.plot(x_eig, phi1**2, color='#e8c866', linewidth=2, label='φ₁²(x)')
ax4.set_xlabel('x', fontsize=9, color='#cccccc')
ax4.set_ylabel('φ₁²(x)', fontsize=9, color='#cccccc')
ax4.tick_params(colors='#cccccc')
ax4.set_title('First eigenmode: λ₁ = π²/4', fontsize=10, color='#eeeeee')
ax4.spines['top'].set_color('#333333')
ax4.spines['right'].set_color('#333333')
ax4.spines['left'].set_color('#333333')
ax4.spines['bottom'].set_color('#333333')
ax4.set_ylim(bottom=0)
ax4b.plot(t_curve, S_approx, color='#e87066', linewidth=1.5, linestyle='--',
          alpha=0.7, label='exp(-λ₁t) tail')
ax4b.set_ylabel('exp(-λ₁t)', fontsize=9, color='#e87066')
ax4b.tick_params(colors='#e87066')
ax4b.set_ylim(bottom=0, top=1.05)

# Save
plt.savefig('/home/sprite/slop-salon-gert/assets/stopped-brownian-01.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
print("Saved stopped-brownian-01.png")

# --- Print some numbers for notes ---
print(f"λ₁ = π²/4 = {lambda1:.4f}")
print(f"S(1) = {S(np.array([1.0]), a)[0]:.4f}")
print(f"Half-life ≈ t where S(t)=0.5: {np.interp(0.5, S(t_curve, a), t_curve):.3f}")
print(f"φ₁ peaks at x = 0, height = {np.sqrt(1/(2*a)):.4f}")
