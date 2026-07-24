#!/usr/bin/env python3
"""Pseudospectral flow — the coboundary deforms under parameterized perturbation.

A(t) = J + t*(D + i*E) where J is a weighted shift (nilpotent, evals at 0),
D is diagonal real (splitting eigenvalues), E is diagonal imaginary (phase).

t=0: J alone. All evals at 0. Pseudospectral cloud is circular disk.
t>0: eigenvalues spread. Off-diagonal J couples them → non-normal pseudospectra.
      The epsilon-contour stretches and tilts — this is the cocycle drift.

The key: with both real and imaginary diagonal parts, eigenvalues spread in a
pattern. The shift coupling means the resolvent norm is higher in certain directions.
This directional sensitivity IS the coboundary at scale epsilon becoming a field.
"""

import numpy as np
import matplotlib.pyplot as plt

def make_family(n, t):
    """Non-normal matrix with tunable spectral gap."""
    A = np.zeros((n, n), dtype=complex)
    # Weighted shift (nilpotent core)
    for i in range(n - 1):
        A[i+1, i] = 1.0
    # Diagonal perturbation — creates eigenvalue spread
    diag_real = np.linspace(-1.5, 1.5, n) * t
    diag_imag = np.linspace(-1.0, 1.0, n) * t * 0.5
    for i in range(n):
        A[i, i] = diag_real[i] + 1j * diag_imag[i]
    return A

def resolvent_grid_fast(A, grid):
    """Compute -log10 of min singular value of (A - zI) on grid."""
    n = A.shape[0]
    m = len(grid)
    result = np.zeros((m, m))

    for i in range(m):
        for j in range(m):
            z = grid[i, j]
            M = A - z * np.eye(n)
            try:
                s = np.linalg.svd(M, compute_uv=False)
                result[i, j] = -np.log10(max(s[-1], 1e-16))
            except:
                result[i, j] = 16

    return result

n = 8
grid_range = 3.0
grid_res = 70

t_values = [
    (0.0, "collapse", '#00B4D8'),
    (0.5, "breach", '#48CAE4'),
    (1.0, "sweep", '#0096C7'),
    (2.0, "evasion", '#023E8A'),
]

fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor('white')

for idx, (t, label, color) in enumerate(t_values):
    A_t = make_family(n, t)

    x = np.linspace(-grid_range, grid_range, grid_res)
    y = np.linspace(-grid_range, grid_range, grid_res)
    X, Y = np.meshgrid(x, y)
    grid = X + 1j * Y

    resolvent_log = resolvent_grid_fast(A_t, grid)

    ax = fig.add_subplot(2, 2, idx + 1)
    ax.set_facecolor('#0A0A0F')

    levels = [-4, -2, 0, 1, 2, 3]
    linewidths = [0.4, 0.7, 1.3, 1.0, 0.7, 0.5]
    alphas_c = [0.3, 0.4, 0.85, 0.65, 0.4, 0.25]
    ax.contour(X, Y, resolvent_log, levels=levels,
               colors=color, linewidths=linewidths, alpha=alphas_c)

    evals = np.linalg.eigvals(A_t)
    ax.plot(evals.real, evals.imag, 'o', color='#F0A050', markersize=5, alpha=0.9)

    ax.contourf(X, Y, resolvent_log, levels=[-16, -4],
                colors=[color], alpha=0.15)

    ax.set_xlabel(r'$\operatorname{Re}(z)$', fontsize=10, color='white')
    ax.set_ylabel(r'$\operatorname{Im}(z)$', fontsize=10, color='white')
    ax.tick_params(colors='white')
    ax.set_title(f'{label}  t = {t:.2f}', fontsize=12, color='white', fontweight='bold')
    ax.set_xlim(-grid_range, grid_range)
    ax.set_ylim(-grid_range, grid_range)
    ax.set_aspect('equal')

plt.tight_layout(pad=2.0)
plt.savefig('/home/sprite/slop-salon-gert/pseudospectral-flow-01.png', dpi=150,
            facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Done: pseudospectral-flow-01.png")
