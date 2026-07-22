import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.linalg import svd
import subprocess

# Simple bidiagonal operator:
# A[i+1, i] = 1.0 (sub-diagonal = 1)
# A[i, i] = alpha * phase(i)  (diagonal variation)
# As alpha increases, eigenvalues spread along real axis
# and pseudospectral cloud expands

N = 40
alphas = [0.0, 2.0, 6.0]
titles = [r'$\alpha = 0.0$', r'$\alpha = 2.0$', r'$\alpha = 6.0$']

# Common grid covering all three
grid_n = 50
extent = 7.0
r = np.linspace(-extent, extent, grid_n)
i = np.linspace(-extent, extent, grid_n)
R, I = np.meshgrid(r, i)

all_max_res = []
all_eigs = []

for alpha in alphas:
    A = np.zeros((N, N))
    for idx in range(N - 1):
        A[idx + 1, idx] = 1.0  # sub-diagonal = 1
        A[idx, idx] = alpha * np.sin(2 * np.pi * idx / N)  # diagonal variation

    eigs = np.linalg.eigvals(A)
    all_eigs.append(eigs)

    max_res = np.zeros((grid_n, grid_n))
    for yi in range(grid_n):
        for xi in range(grid_n):
            z = R[yi, xi] + 1j * I[yi, xi]
            _, s, _ = svd(A - z * np.eye(N))
            max_res[yi, xi] = 1.0 / max(s[-1], 1e-300)
    all_max_res.append(max_res)

print("Per-panel stats:")
for ai, alpha in enumerate(alphas):
    e = all_eigs[ai]
    m = max(all_max_res[ai].ravel())
    print(f"  alpha={alpha}: eigenvalues in [{e.min():.1f}, {e.max():.1f}], "
          f"max_res={m:.0e} (log={np.log10(m):.1f})")

fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=150)

for ai, alpha in enumerate(alphas):
    ax = axes[ai]
    log_res = np.log10(np.maximum(all_max_res[ai], 1))

    lo = np.percentile(log_res.ravel(), 3)
    hi = np.percentile(log_res.ravel(), 99)

    levels = np.linspace(lo, hi, 25)
    cf = ax.contourf(R, I, log_res, levels=levels, cmap='viridis', alpha=0.7)

    # Contour lines for resolvent = 10, 100, 1000
    for res_level, cc in [(10, '#440154'), (100, '#21908c'), (1000, '#fde725')]:
        ax.contour(R, I, all_max_res[ai], levels=[res_level],
                  colors=[cc], linewidths=1.5, alpha=0.7)

    ax.scatter(all_eigs[ai].real, all_eigs[ai].imag, s=20, c='white', edgecolors='black',
              linewidths=0.8, zorder=5)
    ax.set_title(titles[ai], fontsize=14, fontweight='bold', pad=10)
    ax.set_xlabel('Re(z)', fontsize=11)
    ax.set_ylabel('Im(z)', fontsize=11)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.15)

    ax.text(0.02, 0.98, f'max: {all_max_res[ai].max():.0e}',
           transform=ax.transAxes, fontsize=9, va='top', ha='left',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

plt.suptitle('Pseudospectra expansion: non-normality as the deformation parameter',
            fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('pseudospectra-03.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved pseudospectra-03.png")

subprocess.run(['convert', 'pseudospectra-03.png', '-resize', '1200x400', 'pseudospectra-03-cover.png'])
subprocess.run(['convert', 'pseudospectra-03-cover.png', '-resize', '600x200', 'pseudospectra-03-cover-resized.png'])
print("Done")
