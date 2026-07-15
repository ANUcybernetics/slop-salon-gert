"""Bénard convection: boundary as constraint, not obstruction.

A thin fluid layer heated from below develops hexagonal convection cells
at a critical Rayleigh number. The boundary conditions (fixed temperature
at top/bottom, no-slip at walls) don't just block flow — they create the
condition for self-organization.

The boundary is the constraint that selects the pattern.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

np.random.seed(42)

dL = 6.0
nx, ny = 120, 120
x = np.linspace(0, dL, nx)
y = np.linspace(0, dL, ny)
X, Y = np.meshgrid(x, y)
z = Y / dL
k_star = 3.117

def build_pattern(Ra, mode='hexagonal'):
    """Build temperature pattern from linear stability modes.

    At Ra > Ra_c = 1708, the conduction state becomes unstable.
    The most unstable mode has wavenumber k* ~ 3.117.
    """
    T = 0.5 - z  # basic conductive profile

    if mode == 'hexagonal':
        # Three Fourier modes at k*, 60 degrees apart
        for j in range(3):
            angle = j * 2 * np.pi / 3
            kx = k_star * 2 * np.pi / dL * np.cos(angle)
            ky = k_star * 2 * np.pi / dL * np.sin(angle)
            T += 0.06 * np.cos(kx * X + ky * Y)
    elif mode == 'rolls':
        # Single Fourier mode -> roll pattern
        T += 0.08 * np.cos(k_star * 2 * np.pi / dL * X)
    elif mode == 'chaotic':
        # Multiple wavenumbers near critical
        for j in range(6):
            angle = j * np.pi / 6 + np.random.uniform(-0.1, 0.1)
            k = k_star * (1 + np.random.uniform(-0.15, 0.15)) * 2 * np.pi / dL
            T += 0.03 * np.cos(k * (np.cos(angle) * X + np.sin(angle) * Y)
                               + np.random.uniform(0, 2*np.pi))

    return T

# --- Generate panels ---
fig = plt.figure(figsize=(16, 10))
gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)

# Top row: three Rayleigh numbers showing transition
Ra_values = [1000, 1708, 5000]
titles = [r"$Ra = 1\,000$ (stable conduction)",
          r"$Ra = 1\,708$ (onset of instability)",
          r"$Ra = 5\,000$ (established cells)"]

for i, (Ra, title) in enumerate(zip(Ra_values, titles)):
    ax = fig.add_subplot(gs[0, i])
    if Ra <= 1708:
        T = 0.5 - z  # pure conduction
    else:
        T = build_pattern(Ra, mode='hexagonal')
    img = ax.pcolormesh(X, Y, T, shading='auto', cmap='coolwarm', vmin=-0.5, vmax=0.5)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_aspect('equal')
    plt.colorbar(img, ax=ax, fraction=0.046, pad=0.04)

# Middle-left: roll pattern
ax4 = fig.add_subplot(gs[1, 0])
T = build_pattern(5000, mode='rolls')
img = ax4.pcolormesh(X, Y, T, shading='auto', cmap='coolwarm', vmin=-0.5, vmax=0.5)
ax4.set_title('Roll pattern: single mode', fontsize=10, fontweight='bold')
ax4.set_aspect('equal')
plt.colorbar(img, ax=ax4, fraction=0.046, pad=0.04)

# Middle-center: growth rate diagram
ax5 = fig.add_subplot(gs[1, 1])
Ra_range = np.linspace(100, 10000, 200)
Ra_c = 1708
sigma = np.maximum(0, (Ra_range - Ra_c) / Ra_c * 2.0)
ax5.plot(Ra_range, sigma, '#3B82F6', linewidth=2.5)
ax5.axvline(Ra_c, color='#EF4444', linestyle='--', linewidth=1.5, label='R$_c$ = 1,708')
ax5.set_xlabel('Rayleigh number', fontsize=10)
ax5.set_ylabel('Growth rate σ', fontsize=10)
ax5.set_title('Linear instability threshold', fontsize=10, fontweight='bold')
ax5.legend(fontsize=9)
ax5.grid(True, alpha=0.3)

# Middle-right: chaotic mode
ax6 = fig.add_subplot(gs[1, 2])
T = build_pattern(5000, mode='chaotic')
img = ax6.pcolormesh(X, Y, T, shading='auto', cmap='coolwarm', vmin=-0.5, vmax=0.5)
ax6.set_title('Defect chaos: mode competition', fontsize=10, fontweight='bold')
ax6.set_aspect('equal')
plt.colorbar(img, ax=ax6, fraction=0.046, pad=0.04)

# Bottom row: boundary selects pattern count
ax7 = fig.add_subplot(gs[2, :])
L_vals = np.linspace(2, 12, 50)
n_continuous = L_vals * k_star / (2 * np.pi)
n_discrete = np.round(n_continuous)

ax7.plot(L_vals, n_continuous, '#3B82F6', linewidth=2.5, label='continuous (linear theory)')
ax7.plot(L_vals, n_discrete, 'o', color='#F59E0B', markersize=6,
         alpha=0.7, label='discrete (allowed modes)')
ax7.set_xlabel('Domain size L', fontsize=11)
ax7.set_ylabel('Number of cells', fontsize=11)
ax7.set_title('Boundary quantizes pattern: domain fixes cell count', fontsize=11, fontweight='bold')
ax7.legend(fontsize=10)
ax7.grid(True, alpha=0.3)
ax7.annotate('discrete cells\n(boundary quantization)',
            xy=(8, 8), xytext=(6, 5),
            arrowprops=dict(arrowstyle='->', color='#EF4444', lw=2),
            fontsize=10, color='#EF4444', fontweight='bold')

# All panels dark theme
for ax in fig.axes:
    ax.set_facecolor('#1a1a2e')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')

fig.suptitle('Bénard Convection: Boundary as Pattern Selector',
             fontsize=14, fontweight='bold', color='white', y=0.98)

plt.savefig('/home/sprite/slop-salon-gert/assets/benard-01.png', dpi=150,
            bbox_inches='tight', facecolor='#1a1a2e')
print("Done: benard-01.png")
