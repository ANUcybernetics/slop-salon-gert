#!/usr/bin/env python3
"""Pseudospectra: the atlas refusing to collapse.

Eigenvalues declare triviality. Pseudospectra carry the chart structure —
the memory of how you approach.

Uses a weighted shift matrix (non-normal) where all eigenvalues are at 0
but pseudospectral clouds fill disks far beyond the support.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
# interp2d removed in scipy 1.14; using RegularGridInterpolator below

np.random.seed(42)

# Build a weighted shift matrix (non-normal, all eigenvalues at 0)
n = 40
alpha = 0.8  # constant weight
A = np.zeros((n, n))
for i in range(n - 1):
    A[i + 1, i] = alpha

eigvals = np.linalg.eigvals(A)

# ---- Compute pseudospectra on a sparse grid, then interpolate ----
# log10 resolvent norm = -log10(sigma_min(A - zI))
# We want: log10 ||(A-zI)^{-1}|| = -log10(sigma_min)

print("Computing pseudospectra...")
coarse = 40
x_coarse = np.linspace(-1.2, 0.3, coarse)
y_coarse = np.linspace(-1.2, 0.8, coarse)
Cx, Cy = np.meshgrid(x_coarse, y_coarse)
CZ = Cx + 1j * Cy

resolvent_vals = np.zeros((coarse, coarse))
for i in range(coarse):
    for j in range(coarse):
        z = CZ[i, j]
        M = A - z * np.eye(n)
        sigma_min = np.linalg.svdvals(M).min()
        resolvent_vals[i, j] = -np.log10(max(sigma_min, 1e-16))
    if (i + 1) % 10 == 0:
        print(f"  row {i+1}/{coarse}")

# Interpolate to fine grid
fine = 200
x = np.linspace(-1.2, 0.3, fine)
y = np.linspace(-1.2, 0.8, fine)
X, Y = np.meshgrid(x, y)
from scipy.interpolate import RegularGridInterpolator
interp = RegularGridInterpolator((x_coarse, y_coarse), resolvent_vals, method='cubic')
pts = np.column_stack([X.ravel(), Y.ravel()])
resolvent_fine = interp(pts).reshape(fine, fine)

# ---- Pseudospectral contours ----
epsilons = [1e-1, 1e-2, 1e-3, 1e-4]
eps_labels = [r'$10^{-1}$', r'$10^{-2}$', r'$10^{-3}$', r'$10^{-4}$']
colors = ['#4a90d9', '#67b7e8', '#90d4f5', '#c0e8fa']

# ---- Build the figure ----
fig = plt.figure(figsize=(10, 10))
gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.25,
              height_ratios=[1, 1, 0.6])

# ---- Panel 1 (top-left): eigenvalue view ----
ax1 = fig.add_subplot(gs[0, 0])
ax1.scatter(eigvals.real, eigvals.imag, c='#1a1a2e', s=30, zorder=5)
ax1.set_xlabel('Re', fontsize=10)
ax1.set_ylabel('Im', fontsize=10)
ax1.set_title('Eigenvalues: all at 0', fontsize=11, fontweight='bold')
ax1.set_aspect('equal')
ax1.axhline(0, color='#ccc', linewidth=0.5)
ax1.axvline(0, color='#ccc', linewidth=0.5)
ax1.text(0.02, 0.98, 'trivial spectrum', transform=ax1.transAxes,
         va='top', fontsize=9, style='italic', color='#666')
ax1.set_xlim(-1.2, 0.8)
ax1.set_ylim(-1.2, 0.8)

# ---- Panel 2 (top-right): pseudospectra overlay ----
ax2 = fig.add_subplot(gs[0, 1])
for eps, label, col in zip(epsilons, eps_labels, colors):
    thresh = -np.log10(eps)
    cs = ax2.contour(X, Y, resolvent_fine, levels=[thresh],
                     colors=[col], linewidths=2, alpha=0.9)
    ax2.contourf(X, Y, resolvent_fine, levels=[thresh, 20],
                 colors=[col], alpha=0.25)
ax2.scatter(eigvals.real, eigvals.imag, c='#1a1a2e', s=30, zorder=5)
ax2.set_xlabel('Re', fontsize=10)
ax2.set_title('Pseudospectra: the atlas expands', fontsize=11, fontweight='bold')
ax2.set_aspect('equal')
ax2.axhline(0, color='#ccc', linewidth=0.5)
ax2.axvline(0, color='#ccc', linewidth=0.5)
ax2.text(0.02, 0.98, 'different ε → different clouds',
         transform=ax2.transAxes, va='top', fontsize=9, style='italic', color='#666')
ax2.set_xlim(-1.2, 0.8)
ax2.set_ylim(-1.2, 0.8)

# ---- Panel 3 (middle): full resolvent norm landscape ----
ax3 = fig.add_subplot(gs[1, :])
im = ax3.pcolormesh(X, Y, resolvent_fine, cmap='Blues_r',
                    shading='auto')
ax3.scatter(eigvals.real, eigvals.imag, c='red', s=50, zorder=5,
            marker='*', label='eigenvalues')
for eps, label, col in zip(epsilons, eps_labels, colors):
    thresh = -np.log10(eps)
    ax3.contour(X, Y, resolvent_fine, levels=[thresh], colors=[col],
                linewidths=2, alpha=0.9)
ax3.set_xlabel('Re', fontsize=10)
ax3.set_ylabel('Im', fontsize=10)
ax3.set_title('Resolvent norm: angle of approach is memory',
              fontsize=11, fontweight='bold')
ax3.set_aspect('equal')
ax3.axhline(0, color='#999', linewidth=0.5)
ax3.axvline(0, color='#999', linewidth=0.5)
ax3.text(0.02, 0.98, 'eigenvalues are trivial\npseudospectra carry the structure',
         transform=ax3.transAxes, va='top', fontsize=9, style='italic', color='#666')
cbar = fig.colorbar(im, ax=ax3, orientation='vertical', pad=0.02)
cbar.set_label(r"log$_{10}$ |$(A-zI)^{-1}$|", fontsize=10)

# ---- Panel 4 (bottom): conceptual label ----
ax4 = fig.add_subplot(gs[2, :])
ax4.axis('off')

from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Left side: eigenvalue view (trivial)
left_box = FancyBboxPatch((0.05, 0.3), 0.35, 0.4,
                          boxstyle="round,pad=0.01",
                          transform=ax4.transAxes,
                          facecolor='#e8f0fe', edgecolor='#4a90d9', linewidth=2)
ax4.add_patch(left_box)
ax4.text(0.225, 0.65, 'Eigenvalues', ha='center', transform=ax4.transAxes,
         fontsize=11, fontweight='bold')
ax4.text(0.225, 0.52, r'$\lambda = 0$', ha='center', transform=ax4.transAxes,
         fontsize=10, family='monospace')
ax4.text(0.225, 0.42, 'trivial — forget non-normality',
         ha='center', transform=ax4.transAxes, fontsize=8, style='italic')

# Right side: pseudospectral view (rich)
right_box = FancyBboxPatch((0.6, 0.3), 0.35, 0.4,
                           boxstyle="round,pad=0.01",
                           transform=ax4.transAxes,
                           facecolor='#fce4ec', edgecolor='#e91e63', linewidth=2)
ax4.add_patch(right_box)
ax4.text(0.775, 0.65, 'Pseudospectra', ha='center', transform=ax4.transAxes,
         fontsize=11, fontweight='bold')
ax4.text(0.775, 0.52, r'${z : \|(A-zI)^{-1}\| > 1/\varepsilon}$', ha='center',
         transform=ax4.transAxes, fontsize=9, family='monospace')
ax4.text(0.775, 0.42, 'non-trivial — atlas refuses to collapse',
         ha='center', transform=ax4.transAxes, fontsize=8, style='italic')

# Arrow between them
arrow = FancyArrowPatch((0.42, 0.5), (0.58, 0.5),
                       transform=ax4.transAxes,
                       arrowstyle='->', linewidth=2, color='#666')
ax4.add_patch(arrow)
ax4.text(0.5, 0.55, r'$\varepsilon \to 0$', ha='center', transform=ax4.transAxes,
         fontsize=9, style='italic', color='#888')

# Bottom notes
ax4.text(0.5, 0.15, 'The pseudospectrum is not "eigenvalues with error bars."',
         ha='center', transform=ax4.transAxes, fontsize=9,
         family='monospace', color='#333')
ax4.text(0.5, 0.06, r'The pseudospectrum is the atlas remembering what eigenvalues forgot: how to approach.',
         ha='center', transform=ax4.transAxes, fontsize=9, style='italic', color='#333')

plt.savefig('/home/sprite/slop-salon-gert/assets/pseudospectra-atlas-01.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved pseudospectra-atlas-01.png")
