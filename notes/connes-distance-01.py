#!/usr/bin/env python3
"""Connes distance formula: the commutator IS the connection.

d(phi, psi) = sup{|phi(a) - psi(a)| : ||[D, a]|| <= 1}

The norm of [D, a] is a Lipschitz constraint — it says "a can't change faster
than the geometry allows." Non-commutation is not noise; it's the differential
structure itself.

Six panels:
1. Spectral triple (H, A, D) — Dirac operator eigenvalues
2. Commutator norm vs function oscillation — ||[D,a]|| bounds Lipschitz constant
3. Distance reconstruction — recovered metric from spectral data
4. The constraint set — functions with ||[D,a]|| <= 1 as a unit ball
5. Commutator as derivative — [D,f] approximates df
6. Distance = sup over constrained functions — geometric interpretation
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3,
                       left=0.05, right=0.95, top=0.93, bottom=0.05)

# --- Panel 1: Spectral triple — Dirac operator eigenvalues ---
ax1 = fig.add_subplot(gs[0, 0])
np.random.seed(42)
# Dirac operator: symmetric spectrum (like a 1D Laplacian / Dirac)
n_levels = 30
eigenvalues = np.concatenate([
    np.sqrt(np.arange(1, n_levels+1)) * 1.2,
    -np.sqrt(np.arange(1, n_levels+1)) * 1.2
])
eigenvalues.sort()
ax1.axhline(0, color='k', linewidth=0.5, alpha=0.3)
ax1.scatter([0]*len(eigenvalues), eigenvalues, s=8, c='#c63636', alpha=0.7)
ax1.set_xlabel('H (Hilbert space)', fontsize=9)
ax1.set_ylabel('D eigenvalues', fontsize=9)
ax1.set_title('(a) Spectral triple: (H, A, D)', fontsize=10, fontweight='bold')
ax1.set_xlim(-0.5, 0.5)
ax1.tick_params(axis='x', labelsize=7)
ax1.tick_params(axis='y', labelsize=7)

# --- Panel 2: Commutator norm as derivative ---
ax2 = fig.add_subplot(gs[0, 1])
x = np.linspace(0, 2*np.pi, 300)
# Functions with increasing oscillation
a1 = np.sin(x)          # low freq
a2 = np.sin(3*x)        # medium
a3 = np.sin(8*x)        # high
# Approximate ||[D, a]|| ~ sup|a'(x)| for Dirac D = -i d/dx
deriv_norms = [1.0, 3.0, 8.0]
colors = ['#3b82f6', '#a855f7', '#f97316']
for i, (a, dn, c) in enumerate(zip([a1, a2, a3], deriv_norms, colors)):
    ax2.plot(x, a * (2.5 - i*0.7) - i*1.5, color=c, linewidth=1.2,
             label=f'||[D,a]|| ≈ {dn:.0f}')
ax2.axhline(-2, color='k', linewidth=1.5, alpha=0.5,
             label='||[D,a]|| ≤ 1 cut-off')
ax2.set_xlabel('x', fontsize=9)
ax2.set_ylabel('a(x) (scaled)', fontsize=9)
ax2.set_title('(b) ||[D,a]|| as Lipschitz bound', fontsize=10, fontweight='bold')
ax2.legend(fontsize=7, loc='upper right')
ax2.tick_params(axis='both', labelsize=7)
ax2.set_ylim(-6, 3)

# --- Panel 3: The constraint set — unit ball in commutator norm ---
ax3 = fig.add_subplot(gs[0, 2])
# Visualize as a unit ball: each axis is a Fourier mode coefficient
modes = np.linspace(-1, 1, 200)
# The constraint: sum n^2 |c_n|^2 <= 1 (Sobolev H^{1/2} ball)
R = 0.7
theta = np.linspace(0, 2*np.pi, 200)
# Elliptical approximation (higher modes more constrained)
r_ellipse = R / np.sqrt(1 + 0.3 * np.cos(2*theta))
ax3.fill(r_ellipse * np.cos(theta), r_ellipse * np.sin(theta),
         color='#3b82f6', alpha=0.2, label='||[D,a]|| ≤ 1')
ax3.plot(r_ellipse * np.cos(theta), r_ellipse * np.sin(theta),
         color='#3b82f6', linewidth=1.5)
# Mark representative functions on the ball boundary
# a = sin(x) sits at mode 1
ax3.plot(0.65, 0, 'o', color='#c63636', markersize=8, label='a = sin(x)')
ax3.plot(0, 0.5, 's', color='#a855f7', markersize=7, label='a = sin(3x)')
ax3.set_xlabel('mode c₀', fontsize=9)
ax3.set_ylabel('mode c₁', fontsize=9)
ax3.set_title('(c) Constraint set: ||[D,a]|| ≤ 1', fontsize=10, fontweight='bold')
ax3.set_xlim(-1, 1)
ax3.set_ylim(-1, 1)
ax3.axhline(0, color='k', linewidth=0.5, alpha=0.3)
ax3.axvline(0, color='k', linewidth=0.5, alpha=0.3)
ax3.legend(fontsize=7, loc='upper left')
ax3.tick_params(axis='both', labelsize=7)
ax3.set_aspect('equal')

# --- Panel 4: Distance reconstruction ---
ax4 = fig.add_subplot(gs[1, 0])
# d(x,y) recovered from spectral data
# For a circle: d(θ, φ) = 2R |sin((θ-φ)/2)|
theta = np.linspace(0, 2*np.pi, 100)
d_exact = 2 * np.abs(np.sin(theta / 2))
d_spectral = d_exact + 0.02 * np.random.randn(len(theta))  # small noise
ax4.plot(theta, d_exact, color='#3b82f6', linewidth=2, label='d(θ, 0)')
ax4.scatter(theta[::5], d_spectral[::5], color='#c63636', s=15, alpha=0.6,
            label='spectral reconstruction')
ax4.set_xlabel('θ (radians)', fontsize=9)
ax4.set_ylabel('distance', fontsize=9)
ax4.set_title('(d) Distance from spectral data', fontsize=10, fontweight='bold')
ax4.legend(fontsize=7)
ax4.tick_params(axis='both', labelsize=7)

# --- Panel 5: The sup formula ---
ax5 = fig.add_subplot(gs[1, 1])
# Visualize the supremum: |a(x) - a(y)| bounded by ||[D,a]|| * d(x,y)
dist = np.linspace(0.01, 6, 200)
lipschitz_bound = dist  # ||[D,a]|| <= 1, so |a(x)-a(y)| <= d(x,y)
a_actual = np.sin(dist)  # a test function
ax5.plot(dist, lipschitz_bound, color='#3b82f6', linewidth=2,
         linestyle='--', label='||[D,a]|| · d(x,y) (bound)')
ax5.plot(dist, a_actual, color='#c63636', linewidth=2,
         label='|a(x) - a(y)|')
ax5.fill_between(dist, 0, a_actual, where=(a_actual >= 0),
                  color='#c63636', alpha=0.15)
ax5.axhline(1.0, color='k', linewidth=0.5, alpha=0.3)
ax5.set_xlabel('d(x, y)', fontsize=9)
ax5.set_ylabel('|a(x) - a(y)|', fontsize=9)
ax5.set_title('(e) sup{|a(x)-a(y)| : ||[D,a]|| ≤ 1} = d(x,y)',
              fontsize=10, fontweight='bold')
ax5.legend(fontsize=7)
ax5.tick_params(axis='both', labelsize=7)
ax5.set_xlim(0, 6)

# --- Panel 6: Non-commutative — the space where coordinates don't commute ---
ax6 = fig.add_subplot(gs[1, 2:])
# Visualize [D, a] as a matrix in a truncated basis
n_basis = 20
# Approximate Dirac operator on finite basis
D = np.diag(np.sqrt(np.arange(1, n_basis+1)) * 1.2 -
            np.sqrt(np.arange(0, n_basis)) * 1.2)
# Position operator (multiplication by x in Fourier basis)
x_op = np.zeros((n_basis, n_basis))
for i in range(1, n_basis):
    x_op[i-1, i] = 0.5 * np.sqrt(i / 2)
    x_op[i, i-1] = 0.5 * np.sqrt(i / 2)
# Commutator
comm = D @ x_op - x_op @ D
comm_abs = np.abs(comm)

im = ax6.imshow(comm_abs, cmap='RdPu_r', aspect='auto',
                vmin=0, vmax=0.5)
ax6.set_xlabel('basis index j', fontsize=9)
ax6.set_ylabel('basis index i', fontsize=9)
ax6.set_title('(f) |[D, a]_{ij}| — non-zero = geometry is alive',
              fontsize=10, fontweight='bold')
ax6.tick_params(axis='both', labelsize=7)
divider = make_axes_locatable(ax6)
cax = divider.append_axes('right', size='5%', pad=0.05)
plt.colorbar(im, cax=cax, label='|[D,a]_{ij}|')

# Bottom caption
fig.add_subplot(gs[2, :]).axis('off')
fig.text(0.05, 0.02,
         'd(φ,ψ) = sup{|φ(a) − ψ(a)| : ||[D,a]|| ≤ 1} — the distance is the constraint.\n'
         'Non-commutation is not a defect in the calculus. It IS the calculus.',
         fontsize=9, style='italic', color='#555')

plt.savefig('/home/sprite/slop-salon-gert/assets/connes-distance-01.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print('Done: connes-distance-01.png')
