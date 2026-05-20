"""
two fates.
left: limit cycle — approach converges, orbit closes.
right: lorenz — approach converges, orbit never closes.

same ending for approach. different ending for what you find there.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.integrate import odeint

# ── Stuart-Landau / Hopf limit cycle ─────────────────────────────────────────
# ẋ = μx - ωy - (x²+y²)x
# ẏ = ωx + μy - (x²+y²)y
# steady-state orbit: circle of radius √μ

def stuart_landau(state, t, mu=1.0, omega=1.5):
    x, y = state
    r2 = x**2 + y**2
    dx = mu * x - omega * y - r2 * x
    dy = omega * x + mu * y - r2 * y
    return [dx, dy]

# ── Lorenz ────────────────────────────────────────────────────────────────────
def lorenz(state, t, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    return [sigma*(y - x), x*(rho - z) - y, x*y - beta*z]

t_approach = np.linspace(0, 6, 3000)
t_orbit    = np.linspace(6, 30, 8000)   # long orbit phase after approach settles
t_lorenz_warmup = np.linspace(0, 5, 2000)
t_lorenz_orbit  = np.linspace(5, 55, 20000)

fig, axes = plt.subplots(1, 2, figsize=(12, 6), facecolor='#0a0a0a')

# ── LEFT: limit cycle ─────────────────────────────────────────────────────────
ax = axes[0]
ax.set_facecolor('#0a0a0a')
ax.set_aspect('equal')

# several initial conditions at different distances from origin
np.random.seed(42)
ics = [(r * np.cos(theta), r * np.sin(theta))
       for r, theta in [(0.15, 0.3), (0.3, 1.8), (0.5, 3.5),
                        (1.8, 0.8), (2.1, 2.4), (2.3, 4.2),
                        (0.08, 5.0), (1.95, 1.1)]]

for i, ic in enumerate(ics):
    # approach phase
    sol_a = odeint(stuart_landau, ic, t_approach)
    # orbit phase
    sol_o = odeint(stuart_landau, sol_a[-1], t_orbit)

    # approach: muted blue-grey fading in
    n_a = len(sol_a)
    alphas = np.linspace(0.15, 0.55, n_a)
    for j in range(0, n_a - 1, 8):
        ax.plot(sol_a[j:j+9, 0], sol_a[j:j+9, 1],
                color='#4a8fa8', alpha=alphas[j], lw=0.8)

    # orbit: bright — show it closes (periodic, same path)
    ax.plot(sol_o[:, 0], sol_o[:, 1],
            color='#a8d8ea', alpha=0.7, lw=1.1)

# the limit circle itself, bold
theta = np.linspace(0, 2*np.pi, 500)
ax.plot(np.cos(theta), np.sin(theta), color='#e8f4f8', lw=1.8, alpha=0.9)

ax.set_xlim(-2.6, 2.6)
ax.set_ylim(-2.6, 2.6)
ax.axis('off')
ax.set_title('limit cycle\napproach converges. orbit closes.',
             color='#c8d8e0', fontsize=10, pad=10, linespacing=1.6,
             fontfamily='monospace')

# ── RIGHT: lorenz ─────────────────────────────────────────────────────────────
ax = axes[1]
ax.set_facecolor('#0a0a0a')

# single long trajectory after warmup — project to x-z plane
ic_l = [1.0, 0.0, 0.0]
warmup = odeint(lorenz, ic_l, t_lorenz_warmup)
orbit_l = odeint(lorenz, warmup[-1], t_lorenz_orbit)

x, z = orbit_l[:, 0], orbit_l[:, 2]

# color by z-position to show the aperiodic wandering
z_norm = (z - z.min()) / (z.max() - z.min())
cmap = plt.cm.get_cmap('cool')
n = len(x)
step = 3
for j in range(0, n - step, step):
    c = cmap(z_norm[j])
    ax.plot(x[j:j+step+1], z[j:j+step+1],
            color=c, alpha=0.35, lw=0.5)

ax.set_xlim(-25, 25)
ax.set_ylim(0, 50)
ax.axis('off')
ax.set_title('lorenz\napproach converges. orbit never closes.',
             color='#c8d8e0', fontsize=10, pad=10, linespacing=1.6,
             fontfamily='monospace')

plt.suptitle('same ending for approach. different ending for what you find there.',
             color='#8a9aa8', fontsize=9, fontfamily='monospace', y=0.04)

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig('./assets/approach-orbit-fate-2026-05-20.png',
            dpi=180, bbox_inches='tight',
            facecolor='#0a0a0a')
plt.close()
print("saved.")
