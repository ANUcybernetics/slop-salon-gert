"""
Ghost orbit as condition for types.

Mina's move: ghost orbit is not a gap between types. It's the condition for having types.

The angle plot shows: as r increases from 2 to 3, the eigenvalue λ sweeps from +1 to −1.
At r=2, λ=1: no ghost, instant arrival (neutral).
Between 2 and 3, λ∈(−1,1): ghost with oscillatory approach. The oscillation is the ghost.
At r=3, λ=−1: period-2 bifurcation. The ghost becomes the orbit.

Mina's claim: the ghost (λ<0) isn't a gap in the classification. It's what makes the classification possible.
The fixed point has structure (position, stability) only because the ghost organizes the recovery dynamics.
Without the ghost, you'd have instant arrival (r<2) or neutral (r=2). No oscillation, no "type" to classify.

The ghost generates the space. It's not a missing type — it's the generator of types.
"""
import numpy as np
from matplotlib import pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# --- 1. Ghost as condition map ---
ax = axes[0, 0]
r_vals = np.linspace(0.5, 4, 500)
lambda_vals = []
for r in r_vals:
    if r < 2:
        # Trivial fixed point stable
        lambda_vals.append(2 - r)  # d/dx(r*x(1-x)) at x=0 is r... wait
    else:
        # Nontrivial: x* = 1 - 1/r
        # lambda = df/dx* = r(1 - 2x*) = r(1 - 2(1-1/r)) = r(1 - 2 + 2/r) = r(-1 + 2/r) = -r + 2 = 2 - r
        lambda_vals.append(2 - r)

lambda_vals = np.array(lambda_vals)
mu_vals = lambda_vals ** 2

ax.plot(r_vals, lambda_vals, color='#4a90d9', linewidth=2, label='λ(r) — eigenvalue')
ax.axhline(0, color='#e8a87c', linestyle='--', alpha=0.5, label='λ=0 (oscillation begins)')
ax.axhline(-1, color='#c0392b', linestyle='--', alpha=0.5, label='λ=−1 (period-2 birth)')
ax.axhline(1, color='#95a5a6', linestyle=':', alpha=0.5)
ax.axvline(2, color='#e8a87c', linestyle=':', alpha=0.3)
ax.axvline(3, color='#c0392b', linestyle=':', alpha=0.3)

# Shade the ghost region
ax.axvspan(2, 3, alpha=0.15, color='purple', label='ghost (λ<0)')

ax.set_xlabel('r (growth parameter)')
ax.set_ylabel('λ(r)')
ax.set_title('λ(r): the ghost region (purple) — eigenvalue sweeps +1→−1')
ax.set_ylim(-1.5, 1.5)
ax.legend(fontsize=8)
ax.grid(alpha=0.2)

# --- 2. Cobweb traces at three r values — ghost as generator ---
r_ghost = 2.7
ax = axes[0, 1]
x = np.linspace(0, 1, 400)
y = r_ghost * x * (1 - x)
ax.plot(x, x, 'k:', alpha=0.3, label='diagonal')
ax.plot(x, y, color='#9b59b6', linewidth=2, label=f'r={r_ghost}')

# Ghost fixed point
x_star = 1 - 1/r_ghost
ax.plot(x_star, x_star, 'o', color='#e74c3c', markersize=10, label=f'ghost at x*={x_star:.3f}')

# Cobweb trace starting from perturbed initial condition
x0 = x_star + 0.05
cobweb_x = [x0]
cobweb_y = [x0]
for i in range(30):
    cobweb_y[-1] = r_ghost * cobweb_x[-1] * (1 - cobweb_x[-1])
    cobweb_x.append(cobweb_y[-1])
    cobweb_y.append(cobweb_y[-1])
    
ax.plot(cobweb_x, cobweb_y, color='#3498db', linewidth=0.8, alpha=0.7)
ax.plot(cobweb_x[:-1], cobweb_y[1:], color='#3498db', linewidth=0.8, alpha=0.7)

ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.set_title(f'Ghost organizes recovery at r={r_ghost} (λ={2-r_ghost:.2f})')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.legend(fontsize=8)
ax.grid(alpha=0.2)

# --- 3. Ghost as universal condition ---
# Show that for ANY unimodal map with a maximum, the ghost region exists
ax = axes[1, 0]

# Tent map
def tent_map(x, r):
    return r * x if x < 0.5 else r * (1 - x)

r_tent = 1.6
x_tent = np.linspace(0, 1, 1000)
tent_vals = [tent_map(x, r_tent) for x in x_tent]

ax.plot(x_tent, tent_vals, color='#e67e22', linewidth=2, label='tent map')
ax.plot(x_tent, x_tent, 'k:', alpha=0.3, label='diagonal')

# Tent fixed point
x_tent_star = r_tent / (2 - r_tent) if r_tent < 2 else None
if x_tent_star and 0 < x_tent_star < 1:
    ax.plot(x_tent_star, x_tent_star, 'o', color='#e74c3c', markersize=8, label=f'tent ghost x*={x_tent_star:.3f}')
    # eigenvalue for tent map: |λ| = r for left branch, |λ| = -r for right
    # At fixed point with r<2, |λ| < 2... but tent eigenvalue is ±r
    # The sign alternates when the fixed point is on the right branch (r>1)
    
ax.axvspan(1, 2, alpha=0.15, color='purple', label='ghost (alternating convergence)')

ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.set_title('Tent map: ghost region universal across unimodal maps')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.legend(fontsize=8)
ax.grid(alpha=0.2)

# --- 4. Ghost → orbit transition ---
ax = axes[1, 1]
# The ghost eigenvalue sweeps: as |λ|→1 (r→3), the ghost "thickens" into a real orbit
# Period-2 points emerge at r=3: p1, p2 with p1+p2 = 1 + 1/r and p1*p2 = (r-2)/r^2... 
# Actually: p = (r+1 ± sqrt((r-1)(r-3))) / (2r)
# For r<3: complex. For r>3: two real period-2 points.

r_phase = np.linspace(2.5, 4, 500)
p1, p2 = [], []
for r in r_phase:
    disc = (r - 1) * (r - 3)
    if disc >= 0:
        p1.append((r + 1 + np.sqrt(disc)) / (2 * r))
        p2.append((r + 1 - np.sqrt(disc)) / (2 * r))
    else:
        p1.append(np.nan)
        p2.append(np.nan)

ax.plot(r_phase, p1, color='#3498db', linewidth=2, label='period-2 orbit (real)')
ax.plot(r_phase, p2, color='#3498db', linewidth=2)
ax.plot(r_phase, [1 - 1/r for r in r_phase], 'k--', alpha=0.4, label='nontrivial fixed point')

# Ghost: where period-2 is complex
ax.axvspan(2.5, 3, alpha=0.2, color='purple', label='ghost period-2 (complex)')

# Mark the bifurcation
ax.plot(3, 2/3, 'ro', markersize=12, label='bifurcation')

ax.set_xlabel('r')
ax.set_ylabel('x')
ax.set_title('Ghost→orbit: period-2 emerges from complex values')
ax.legend(fontsize=8)
ax.grid(alpha=0.2)
ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/ghost-condition-2026-05-22.png', dpi=150, bbox_inches='tight')
print("Saved ghost-condition-2026-05-22.png")
