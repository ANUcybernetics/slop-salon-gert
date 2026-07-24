#!/usr/bin/env python3
"""
Eigenvalue flow — eigenvalues tracing paths through the complex plane.

Three 2x2 blocks with different damping rates. Each pair starts as a complex
conjugate pair, collides, then splits along the real axis. Different blocks
collide at different t, creating a staggered unfolding.

The coboundary in motion: parameterized obstruction.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

outdir = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(outdir, exist_ok=True)

n = 6
N = 500
t_max = 6.0
times = np.linspace(-3.0, t_max, N)

c_vals = [1.0, 1.5, 2.0]
w_sq = [1.0, 2.0, 4.0]
gamma = [0.4, 0.8, 1.2]

flows = np.zeros((N, n), dtype=complex)

for i, t in enumerate(times):
    A = np.zeros((n, n))
    for b in range(3):
        i0, i1 = 2*b, 2*b+1
        A[i0, i1] = c_vals[b]
        A[i1, i0] = -w_sq[b]
        A[i1, i1] = -gamma[b] * t
    eigs = np.linalg.eigvals(A)
    flows[i] = eigs

t_slices = [-2.5, -1.5, -0.5, 1.0, 3.0, 6.0]
t_indices = [max(1, min(N-1, int(np.round((t - (-3.0)) / (t_max - (-3.0)) * N)))) for t in t_slices]

# --- Six-panel grid: one row of six snapshots ---
fig, axes = plt.subplots(1, 6, figsize=(24, 5))
fig.patch.set_facecolor('#0a0a0f')
for ax in axes.flat:
    ax.set_facecolor('#0a0a0f')
    ax.set_aspect('equal')

for ax_idx, (ti, t) in enumerate(zip(t_indices, t_slices)):
    ax = axes[ax_idx]

    # Full eigenvalue trajectories up to this point
    for m in range(n):
        ax.plot(np.real(flows[:ti+1, m]), np.imag(flows[:ti+1, m]),
                color=(100/255, 180/255, 255/255, 0.4), linewidth=1.2)

    # Current eigenvalues
    ax.plot(np.real(flows[ti, :]), np.imag(flows[ti, :]),
            'o', color='#ff6b35', markersize=6, markeredgecolor='w', markeredgewidth=0.5)

    ax.axhline(0, color='w', alpha=0.08, linewidth=0.5)
    ax.axvline(0, color='w', alpha=0.08, linewidth=0.5)
    ax.set_xlim(-2.5, 3.0)
    ax.set_ylim(-2.0, 2.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f't = {t:.1f}', color='w', alpha=0.7, fontsize=11)

plt.tight_layout(pad=1.5)
outpath = os.path.join(outdir, 'eigenvalue-flow-01.png')
fig.savefig(outpath, dpi=120, facecolor='#0a0a0f', edgecolor='none')
plt.close(fig)
print(f'Wrote {outpath}')
print('Done.')
