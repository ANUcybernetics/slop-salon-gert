"""Halting boundary: undecidability as boundary.

A visualization of the boundary between halting and non-halting computation.
The key insight: we can draw near the boundary, but never cross it with certainty.
Cells near the boundary look the same whether they halt or not.

We use a simple model: pairs of integers (p,q) representing configurations,
coloring them by how long their "computation" takes before we decide to stop.
The boundary is where time → ∞ — we never decide.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Simple "computation" model: Collatz-like iteration
# For each cell (i,j), we simulate and track how long until we "halt"
# (reach a simple state). Near the boundary, iterations explode.
# This isn't the halting problem itself, but a visual metaphor:
# the boundary between halting and non-halting is undecidable.

def compute_time(p, q, max_iter=256):
    """Simulate a pair (p,q) evolving. Time is how long until stable."""
    # Map (p,q) to a 2D dynamics: each step, the pair evolves
    x, y = float(p), float(q)
    for t in range(1, max_iter + 1):
        # Simple chaotic map
        x_new = abs(x) / (1 + abs(y)) + 0.3 * np.sin(y * t * 0.01)
        y_new = abs(y) / (1 + abs(x)) + 0.3 * np.cos(x * t * 0.01)
        # Check convergence
        if abs(x_new - x) < 1e-10 and abs(y_new - y) < 1e-10:
            return t
        x, y = x_new, y_new
    return max_iter  # "non-halting" — boundary

# Grid
N = 256
X = np.linspace(-2, 2, N)
Y = np.linspace(-2, 2, N)
gx, gy = np.meshgrid(X, Y)

# Compute iteration counts (vectorized-ish)
max_iter = 256
times = np.zeros((N, N), dtype=np.float64)
xs = gx.copy()
ys = gy.copy()

for step in range(1, max_iter + 1):
    x_new = np.abs(xs) / (1 + np.abs(ys)) + 0.3 * np.sin(ys * step * 0.01)
    y_new = np.abs(ys) / (1 + np.abs(xs)) + 0.3 * np.cos(xs * step * 0.01)
    converged = (np.abs(x_new - xs) < 1e-10) & (np.abs(y_new - ys) < 1e-10)
    # Set converged cells
    mask = converged & (times == 0)
    times[mask] = step
    xs, ys = x_new, y_new

# Cells that never converged = boundary (time → ∞)
times[times == 0] = max_iter

# Threshold: "halting" vs "non-halting"
# Halting: converged quickly (< some threshold)
# Non-halting: took very long or never
threshold = max_iter * 0.5
halting = (times <= threshold).astype(float)

# Create visualization
fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
fig.patch.set_facecolor('#1a1a2e')

# Panel 1: Convergence time (log scale)
im0 = axes[0].imshow(times, cmap='inferno', extent=[-2, 2, -2, 2],
                      origin='lower',
                      norm=matplotlib.colors.LogNorm(vmin=1, vmax=int(max_iter * 0.9)))
axes[0].set_title('Iteration count to convergence', color='#e0e0e0', fontsize=10)
axes[0].set_xlabel('x')
axes[0].set_ylabel('y')
axes[0].tick_params(colors='#e0e0e0')
# Add a thin line at the undecidable boundary
axes[0].axhline(0, color='white', linewidth=0.5, alpha=0.3)
cbar = plt.colorbar(im0, ax=axes[0], pad=0.01, fraction=0.046)
cbar.set_label('Iterations', color='#e0e0e0', fontsize=8)
cbar.ax.tick_params(colors='#e0e0e0', size=6)

# Panel 2: Halting (binary view) — we can see the decidability gap
im1 = axes[1].imshow(halting, cmap='bwr', extent=[-2, 2, -2, 2],
                      origin='lower', vmin=-0.5, vmax=0.5)
axes[1].set_title('Decidable: halt (white) vs non-halt (blue)',
                   color='#e0e0e0', fontsize=10)
axes[1].set_xlabel('x')
axes[1].set_ylabel('y')
axes[1].tick_params(colors='#e0e0e0')
# Show boundary cells as ambiguous (gray)
boundary_mask = (times > threshold) & (times < max_iter)
axes[1].contour(gx, gy, boundary_mask.astype(float), levels=[0.5],
                colors='gray', linewidths=1)
# Annotate
axes[1].text(-1.8, 1.8, 'halting region', fontsize=7, color='white')
axes[1].text(-1.8, -1.8, 'non-halting', fontsize=7, color='lightblue')

# Panel 3: Phase portrait of a single trajectory near boundary
ax3 = axes[2]
ax3.set_facecolor('#1a1a2e')
ax3.set_title('Trajectories approaching the boundary', color='#e0e0e0', fontsize=10)

n_trajs = 30
theta = np.linspace(0, 2*np.pi, n_trajs)
colors_traj = plt.cm.coolwarm(np.linspace(0, 1, n_trajs))
for i, (th, col) in enumerate(zip(theta, colors_traj)):
    x, y = 1.8 * np.cos(th), 1.8 * np.sin(th)
    traj_x, traj_y = [x], [y]
    for _ in range(80):
        x_new = abs(x) / (1 + abs(y)) + 0.3 * np.sin(y * 0.01)
        y_new = abs(y) / (1 + abs(x)) + 0.3 * np.cos(x * 0.01)
        if abs(x_new - x) < 1e-10 and abs(y_new - y) < 1e-10:
            break
        x, y = x_new, y_new
        traj_x.append(x)
        traj_y.append(y)
    ax3.plot(traj_x, traj_y, color=col, linewidth=0.5, alpha=0.7)

ax3.plot(0, 0, 'o', color='red', markersize=6, label='fixed point')
ax3.set_xlim(-0.5, 0.5)
ax3.set_ylim(-0.5, 0.5)
ax3.set_aspect('equal')
ax3.spines['bottom'].set_color('#e0e0e0')
ax3.spines['top'].set_color('#e0e0e0')
ax3.spines['left'].set_color('#e0e0e0')
ax3.spines['right'].set_color('#e0e0e0')
ax3.tick_params(colors='#e0e0e0', axis='both', labelsize=7)
ax3.legend(fontsize=6, facecolor='#1a1a2e', edgecolor='#444', labelcolor='#e0e0e0')
ax3.set_xlabel('x')
ax3.set_ylabel('y')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('/home/sprite/slop-salon-gert/assets/halting-01.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
