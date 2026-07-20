import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# Burgers circuit: walk around a screw dislocation and compute the closure failure.
#
# A screw dislocation has a Burgers vector parallel to the dislocation line.
# The displacement field is u_theta = b * theta / (2*pi), so walking a circuit
# of radius R gives a closure failure of exactly b in the azimuthal direction.
#
# We embed this in a 2D grid, place a dislocation at center, and compute:
# 1. The displacement field
# 2. A Burgers circuit (small square) showing closure failure
# 3. The strain field (|grad u|) to show concentration near the core

fig = plt.figure(figsize=(14, 5))

# --- Panel 1: Displacement field ---
ax1 = fig.add_subplot(131)
L = 20
x = np.linspace(-L, L, 200)
y = np.linspace(-L, L, 200)
X, Y = np.meshgrid(x, y)

# Core at origin. Displacement in z-direction (out of plane).
# u(r, theta) = b * theta / (2*pi)
b = 2.0
R = np.sqrt(X**2 + Y**2)
Theta = np.arctan2(Y, X)

u = b * Theta / (2 * np.pi)
# Wrap to [-1, 1] for visualization
u_wrapped = np.arctan(np.sin(Theta), np.cos(Theta)) * b / np.pi

img1 = ax1.contourf(X, Y, u_wrapped, levels=30, cmap='coolwarm')
ax1.set_title('Displacement field: u_θ = b·θ/(2π)\n(wrapped for visualization)', fontsize=10)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_aspect('equal')
plt.colorbar(img1, ax=ax1, label='u (wrapped)')

# --- Panel 2: Burgers circuit ---
ax2 = fig.add_subplot(132)

# Pick a square circuit around the origin
circuit_size = 3.0
n_steps = 50
# Top, right, bottom, left
top_y = np.linspace(-circuit_size, circuit_size, n_steps)
right_x = np.full(n_steps, circuit_size)
bottom_y = np.linspace(circuit_size, -circuit_size, n_steps)
left_x = np.full(n_steps, -circuit_size)

# Build the circuit as a parametric path
t_top = np.linspace(-1, 1, n_steps)
t_right = np.linspace(-1, 1, n_steps)
t_bottom = np.linspace(1, -1, n_steps)
t_left = np.linspace(1, -1, n_steps)

path_x = np.concatenate([
    t_top * circuit_size,    # top: x from -s to s, y = s
    right_x,                 # right: x = s, y from s to -s...
])
path_y = np.concatenate([
    np.full(n_steps, circuit_size),
    t_right * circuit_size,
])

# Better: explicit circuit
n_s = 40
cx, cy = [], []
# Top edge: left to right
cx.extend(np.linspace(-circuit_size, circuit_size, n_s))
cy.extend(np.full(n_s, circuit_size))
# Right edge: top to bottom
cx.extend(np.full(n_s, circuit_size))
cy.extend(np.linspace(circuit_size, -circuit_size, n_s))
# Bottom edge: right to left
cx.extend(np.linspace(circuit_size, -circuit_size, n_s))
cy.extend(np.full(n_s, -circuit_size))
# Left edge: bottom to top
cx.extend(np.full(n_s, -circuit_size))
cy.extend(np.linspace(-circuit_size, circuit_size, n_s))
# Close loop
cx.append(cx[0])
cy.append(cy[0])

ax2.plot(cx, cy, 'b-', lw=1.5, label='Burgers circuit')

# Compute displacement at each point
disp_x = b * np.arctan2(np.array(cy), np.array(cx)) / (2 * np.pi)

# Show closure failure: the displacement at end != displacement at start
end_disp = b * np.arctan2(cy[-1], cx[-1]) / (2 * np.pi)
start_disp = b * np.arctan2(cy[0], cx[0]) / (2 * np.pi)
closure_failure = end_disp - start_disp

# Annotate
ax2.axhline(0, color='k', lw=0.5)
ax2.axvline(0, color='k', lw=0.5)
ax2.scatter([0], [0], c='red', s=50, zorder=5, label='dislocation core')
ax2.text(0, 0, '×', color='red', fontsize=20, ha='center', va='center', fontweight='bold')

# Show the failure as a vector at the corner
corner_idx = n_s  # end of top edge
ax2.annotate('', xy=(cx[corner_idx], cy[corner_idx] + closure_failure),
             xytext=(cx[corner_idx], cy[corner_idx]),
             arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax2.text(cx[corner_idx]+1, cy[corner_idx] + closure_failure/2,
         f'B = {closure_failure:.2f}', color='red', fontweight='bold')

ax2.set_title(f'Burgers circuit: closure failure\nB = ∮ du = {closure_failure:.2f}', fontsize=10)
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_aspect('equal')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# --- Panel 3: Strain concentration ---
ax3 = fig.add_subplot(133)

# Strain: du/dr = 0 for screw (purely azimuthal), but |grad u|² = (b/2πr)²
# This diverges at r=0.
strain = np.where(R > 0.5, np.abs(b / (2 * np.pi * R)), np.nan)

# Smooth near core for visualization
R_core = R.copy()
R_core[R_core < 1.0] = 1.0
strain_core = np.abs(b / (2 * np.pi * R_core))

img3 = ax3.contourf(X, Y, strain_core, levels=30, cmap='inferno',
                     norm=Normalize(vmin=0, vmax=np.max(strain_core)*0.9))
ax3.set_title('Strain: |∇u| = b/(2πr)\nconcentrated at core', fontsize=10)
ax3.set_xlabel('x')
ax3.set_ylabel('y')
ax3.set_aspect('equal')
plt.colorbar(img3, ax=ax3, label='|∇u|')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/burgers-circuit-01.png', dpi=120, bbox_inches='tight')
print("Saved burgers-circuit-01.png")
print(f"Panel dimensions: {fig.get_size_inches()}")
print(f"Figure size: {fig.get_figwidth()}x{fig.get_figheight()}")
