#!/usr/bin/env python3
"""
poisson-bracket-01

The Poisson bracket {f, g} = ∂f/∂q · ∂g/∂p − ∂f/∂p · ∂g/∂q
is the symplectic derivative. Anti-commutative, like coboundary.

3-panel:
1. Symplectic flow lines (Hamiltonian circulation)
2. Conjugate flow
3. Anti-commutativity {f,g} = −{g,f}
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Phase space grid
q = np.linspace(-2, 2, 120)
p = np.linspace(-2, 2, 120)
Q, P = np.meshgrid(q, p)

# Harmonic oscillator Hamiltonian
H = Q**2 + P**2

# Gradients
dH_dq = 2 * Q
dH_dp = 2 * P

# Poisson brackets
bracket_q_H = dH_dp    # = p
bracket_p_H = -dH_dq   # = -q

# Anti-commutativity field
shear = 2 * bracket_q_H  # = 2p
norm = TwoSlopeNorm(vmin=shear.min(), vcenter=0, vmax=shear.max())

# Vectors for streamplot (1D grid coords, 2D components)
# (U, V) = (−∂H/∂p, ∂H/∂q) = (−2p, 2q)
U = -2 * P
V = 2 * Q

# Magnitude for coloring
mag = np.sqrt(U**2 + V**2)
mag[mag == 0] = 1
color_s = 0.5 + 0.5 * V / mag

fig = plt.figure(figsize=(14, 4.5), facecolor='#1a1a1e')
fig.patch.set_facecolor('#1a1a1e')

# Panel 1: Symplectic flow — {q, H} = p
ax1 = fig.add_subplot(131)
ax1.set_facecolor('#1a1a1e')
ax1.streamplot(q, p, U, V,
               color=color_s, cmap='coolwarm', density=1.8,
               linewidth=0.6, arrowsize=1.2)
ax1.contour(Q, P, H, levels=[1, 2, 4, 8], colors='#555555',
            linewidths=0.6, alpha=0.5)
ax1.set_title('{q, H} = p', color='#cccccc', fontsize=12, pad=12)
ax1.set_xlabel('q (position)', color='#cccccc')
ax1.set_ylabel('p (momentum)', color='#cccccc')
ax1.tick_params(colors='#999999')
ax1.set_aspect('equal')

# Panel 2: Conjugate — {p, H} = −q (opposite direction)
ax2 = fig.add_subplot(132)
ax2.set_facecolor('#1a1a1e')
ax2.streamplot(q, p, -U, -V,
               color=1 - color_s, cmap='coolwarm', density=1.8,
               linewidth=0.6, arrowsize=1.2)
ax2.contour(Q, P, H, levels=[1, 2, 4, 8], colors='#555555',
            linewidths=0.6, alpha=0.5)
ax2.set_title('{p, H} = −q', color='#cccccc', fontsize=12, pad=12)
ax2.set_xlabel('q (position)', color='#cccccc')
ax2.set_ylabel('p (momentum)', color='#cccccc')
ax2.tick_params(colors='#999999')
ax2.set_aspect('equal')

# Panel 3: Anti-commutativity — magnitude of shear
ax3 = fig.add_subplot(133)
ax3.set_facecolor('#1a1a1e')
ax3.contourf(Q, P, shear, levels=24, cmap='coolwarm',
             norm=norm, alpha=0.9)
ax3.contour(Q, P, H, levels=[1, 2, 4, 8], colors='#ffffff',
            linewidths=0.4, alpha=0.25)
ax3.streamplot(q, p, U, V,
               color='#888888', cmap='Greys', density=1.5,
               linewidth=0.3, arrowsize=0.8, arrowstyle='-')
ax3.set_title('{f,g} = −{g,f}', color='#cccccc', fontsize=12, pad=12)
ax3.set_xlabel('q (position)', color='#cccccc')
ax3.set_ylabel('p (momentum)', color='#cccccc')
ax3.tick_params(colors='#999999')
ax3.set_aspect('equal')

# Colorbar for panel 3
cbar = plt.colorbar(plt.cm.ScalarMappable(cmap='coolwarm', norm=norm),
                    ax=ax3, label='{q, H} − {H, q}',
                    ticks=[shear.min(), 0, shear.max()],
                    shrink=0.8)
cbar.ax.tick_params(colors='#999999', labelsize=8)

plt.savefig('/home/sprite/slop-salon-gert/assets/poisson-bracket-01.png',
            dpi=150, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()

print("Saved assets/poisson-bracket-01.png")
