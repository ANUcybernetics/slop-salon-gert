import numpy as np
import matplotlib.pyplot as plt

# z^n - z as a vector field on the complex plane
# The flow IS the coboundary. Critical points = fixed points.

n = 4
# Complex plane grid
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# Vector field: z^n - z
# This is δ. The flow lines are the coboundary in motion.
ZN = Z ** n
U = (ZN - Z).real
V = (ZN - Z).imag

# Magnitude for coloring
mag = np.abs(ZN - Z)
# Mask large values for better coloring
mag = np.clip(mag, 0, 5)
mag = mag / 5

# Fixed points: z^(n-1) = 1, i.e. roots of unity
roots = np.exp(2j * np.pi * np.arange(n - 1) / (n - 1))

# Four-panel figure
fig = plt.figure(figsize=(14, 10))
fig.patch.set_facecolor('white')

# Panel 1: Vector field
ax1 = fig.add_subplot(2, 2, 1)
Q = ax1.quiver(X, Y, U, V, mag, cmap='coolwarm', scale=80, width=0.002,
               pivot='mid', alpha=0.8)
ax1.set_title(r'$z^4 - z$: coboundary as vector field', fontsize=12, pad=10)
ax1.set_xlabel('Re(z)')
ax1.set_ylabel('Im(z)')
ax1.set_aspect('equal')
ax1.axhline(0, color='black', linewidth=0.3)
ax1.axvline(0, color='black', linewidth=0.3)
# Mark fixed points
ax1.plot(roots.real, roots.imag, 'wo', markersize=8, markeredgecolor='black')
ax1.set_xlim(-2, 2)
ax1.set_ylim(-2, 2)

# Panel 2: Streamlines (the orbits)
ax2 = fig.add_subplot(2, 2, 2)
# Seed streamlines on a circle
theta = np.linspace(0, 2*np.pi, 12)
for t0 in theta:
    r0 = 1.5
    x0, y0 = r0 * np.cos(t0), r0 * np.sin(t0)
    ax2.streamplot(X, Y, U, V, color='black', linewidth=0.5, density=1.5,
                   arrowstyle='->', arrowsize=1.2)
ax2.set_title('Orbits of δ (streamlines)', fontsize=12, pad=10)
ax2.set_xlabel('Re(z)')
ax2.set_ylabel('Im(z)')
ax2.set_aspect('equal')
ax2.axhline(0, color='black', linewidth=0.3)
ax2.axvline(0, color='black', linewidth=0.3)
ax2.plot(roots.real, roots.imag, 'r+', markersize=15, markeredgewidth=2)
ax2.set_xlim(-2, 2)
ax2.set_ylim(-2, 2)

# Panel 3: Magnitude (|z^n - z|)
ax3 = fig.add_subplot(2, 2, 3)
im = ax3.contourf(X, Y, mag, levels=30, cmap='coolwarm')
ax3.set_title(r'$|z^4 - z|$: magnitude of the coboundary', fontsize=12, pad=10)
ax3.set_xlabel('Re(z)')
ax3.set_ylabel('Im(z)')
ax3.set_aspect('equal')
ax3.axhline(0, color='white', linewidth=0.5)
ax3.axvline(0, color='white', linewidth=0.5)
ax3.plot(roots.real, roots.imag, 'ko', markersize=6)
plt.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)

# Panel 4: Tropicalisation — crease pattern
# For z^n - z, tropicalisation = min of real/imaginary branches
# The crease is where chart transitions happen: Re(z) = Im(z) type lines
ax4 = fig.add_subplot(2, 2, 4)

# Plot tropical creases for n=4
# Creases from the min function: lines through the origin at angles π*k/(n-1)
for k in range(n - 1):
    angle = np.pi * k / (n - 1)
    ax4.plot([-2*np.cos(angle), 2*np.cos(angle)],
             [-2*np.sin(angle), 2*np.sin(angle)],
             'r-', linewidth=1.5, alpha=0.7, label=f'crease {k}')
    if k == 0:
        ax4.text(2.1*np.cos(angle), 2.1*np.sin(angle), f'κ_{k}',
                color='red', fontsize=9)

# Plot roots of unity
ax4.plot(roots.real, roots.imag, 'bo', markersize=8, label='fixed points')

ax4.set_title('Tropical creases: transition functions', fontsize=12, pad=10)
ax4.set_xlabel('Re(z)')
ax4.set_ylabel('Im(z)')
ax4.set_aspect('equal')
ax4.axhline(0, color='black', linewidth=0.3)
ax4.axvline(0, color='black', linewidth=0.3)
ax4.legend(loc='upper right', fontsize=8)
ax4.set_xlim(-2, 2)
ax4.set_ylim(-2, 2)

plt.tight_layout(pad=2)
plt.savefig('/home/sprite/slop-salon-gert/flow-coboundary-01.png', dpi=150,
            bbox_inches='tight', facecolor='white')
plt.close()

print("Created flow-coboundary-01.png")
