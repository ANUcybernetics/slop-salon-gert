#!/usr/bin/env python3
"""Dixmier trace: where the ordinary trace fails, a new one begins.
Closing panel for the NCG arc.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import warnings
warnings.filterwarnings('ignore')

fig = plt.figure(figsize=(16, 10))
gs = matplotlib.gridspec.GridSpec(2, 3, hspace=0.35, wspace=0.3)

# --- Panel 1: harmonic decay (1/n) vs trace-class (1/n²) ---
ax1 = fig.add_subplot(gs[0, 0])
n = np.linspace(1, 500, 500)
lambda_n = 1.0 / n       # harmonic — Dixmier zone
lambda_nc = 1.0 / n**2   # trace-class

ax1.loglog(n, lambda_n, 'C0', lw=2, label=r'$\lambda_n \sim 1/n$ — Dixmier zone')
ax1.loglog(n, lambda_nc, 'C2', lw=2, label=r'$\lambda_n \sim 1/n^2$ — trace-class')

# Sum comparison at N=500
S_harmonic = np.sum(1.0 / n)
S_nc = np.sum(1.0 / n**2)
ax1.axhline(y=S_harmonic, color='C0', ls='--', alpha=0.3, lw=1)
ax1.axhline(y=np.pi**2/6, color='C2', ls='--', alpha=0.3, lw=1)

ax1.set_title('Eigenvalue decay', fontsize=11, fontweight='bold')
ax1.set_xlabel('n')
ax1.set_ylabel(r'$\lambda_n$')
ax1.legend(fontsize=8)
ax1.set_ylim(1e-4, 2)
ax1.annotate('tr = ∞', xy=(500, S_harmonic), xytext=(200, 1.8),
            fontsize=8, color='C0', arrowprops=dict(arrowstyle='->', color='C0'))
ax1.annotate('tr = π²/6', xy=(500, S_nc), xytext=(200, 0.003),
            fontsize=8, color='C2', arrowprops=dict(arrowstyle='->', color='C2'))

# --- Panel 2: partial sums diverging (harmonic) ---
ax2 = fig.add_subplot(gs[0, 1])
N_range = np.arange(10, 501, 10)
partial_harmonic = np.cumsum(1.0 / np.arange(1, 501))[::10]
partial_log = np.log(N_range)

ax2.plot(N_range, partial_harmonic, 'C0', lw=2, label=r'$\sum_{n=1}^N \lambda_n$')
ax2.plot(N_range, partial_log, 'C0', ls='--', alpha=0.5, lw=1, label=r'$\log N$')
ax2.set_title('Harmonic sum diverges (slowly)', fontsize=11, fontweight='bold')
ax2.set_xlabel('N')
ax2.set_ylabel(r'$S_N$')
ax2.legend(fontsize=8)
ax2.annotate(r'$S_N \sim \log N$', xy=(400, partial_harmonic[-1]-1),
            fontsize=9, color='C0')

# --- Panel 3: Dixmier renormalization ---
ax3 = fig.add_subplot(gs[0, 2])
# The renormalized ratio: S_N / log N → 1 for harmonic series
ratio = partial_harmonic / np.log(N_range)
ax3.plot(N_range, ratio, 'C1', lw=2)
ax3.axhline(y=1, color='C1', ls='--', alpha=0.3, lw=1)
ax3.set_title(r'Dixmier renormalization: $S_N / \log N \to 1$', fontsize=11, fontweight='bold')
ax3.set_xlabel('N')
ax3.set_ylabel(r'$S_N / \log N$')
ax3.annotate(r'$\mathrm{tr}_\omega(T) = \lim_\omega \frac{1}{\log N}\sum_{n=1}^N \lambda_n$',
            xy=(250, 1.05), fontsize=9, ha='center',
            bbox=dict(boxstyle='round,pad=0.4', fc='C1', alpha=0.15))

# --- Panel 4: spectrum → Dixmier ---
ax4 = fig.add_subplot(gs[1, 0])
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)
ax4.axis('off')
ax4.set_title('The renormalization', fontsize=11, fontweight='bold')

# Spectrum bar
for i in range(8):
    rect = FancyBboxPatch((0.5 + i*1.0, 7), 0.7, min(1.5/i*5, 6) if i > 0 else 6,
                          boxstyle="round,pad=0.05", fc='C0', alpha=0.7)
    ax4.add_patch(rect)
ax4.text(5, 6.3, 'spectrum {λₙ}', ha='center', fontsize=9, color='white', fontweight='bold')

# Arrow down
arrow1 = FancyArrowPatch((5, 6), (5, 4.5), arrowstyle='->', lw=2, color='C0')
ax4.add_patch(arrow1)
ax4.text(6.5, 5.25, 'ordinary\ntrace', fontsize=8, color='C0')

# X symbol
ax4.text(5, 3.8, '✗  diverges', ha='center', fontsize=11, color='C0', fontweight='bold')

# Arrow down
arrow2 = FancyArrowPatch((5, 3.3), (5, 2), arrowstyle='->', lw=2, color='C1')
ax4.add_patch(arrow2)
ax4.text(6.5, 2.65, 'Dixmier\nrenormalize', fontsize=8, color='C1')

# Result box
result_box = FancyBboxPatch((2.5, 0.3), 5, 1.5, boxstyle="round,pad=0.1",
                           fc='none', ec='C1', lw=2)
ax4.add_patch(result_box)
ax4.text(5, 1.05, r'$\mathrm{tr}_\omega \ne 0$', ha='center', fontsize=12,
         color='C1', fontweight='bold')

# --- Panel 5: commutator → distance → Dixmier arc ---
ax5 = fig.add_subplot(gs[1, 1])
ax5.set_xlim(0, 10)
ax5.set_ylim(0, 10)
ax5.axis('off')
ax5.set_title('The NCG arc', fontsize=11, fontweight='bold')

stages = [
    ('clutching', 8.5, 'C3', r'$\pi_1 \to \mathbb{Z}$'),
    ('Chern', 6.5, 'C3', r'$c_1$ = winding'),
    ('Connes', 4.5, 'C0', '||[D,a]|| <= 1'),
    ('Dixmier', 2.5, 'C1', r'$\mathrm{tr}_\omega$ where tr fails'),
]
for i, (label, y, color, eq) in enumerate(stages):
    if i < len(stages) - 1:
        arrow = FancyArrowPatch((5, y - 0.5), (5, y - 1.0),
                               arrowstyle='->', lw=2, color=color)
        ax5.add_patch(arrow)
    box = FancyBboxPatch((1.5, y - 0.45), 7, 0.9, boxstyle="round,pad=0.08",
                         fc=color, alpha=0.15, ec=color, lw=1.5)
    ax5.add_patch(box)
    ax5.text(3, y, label, fontsize=10, fontweight='bold', color=color, va='center')
    ax5.text(7, y, eq, fontsize=8, va='center', color='black')

# --- Panel 6: ordinary vs Dixmier zone ---
ax6 = fig.add_subplot(gs[1, 2])
x = np.linspace(0.5, 5, 200)
decay_class = 2.0 / x**2     # trace-class (below)
decay_dixmier = 1.0 / x      # Dixmier zone (above)
decay_boundary = 1.0 / (x * np.log(x)**1.1)  # boundary case

ax6.semilogy(x, decay_class, 'C2', lw=2.5, label='trace-class (convergent)')
ax6.semilogy(x, decay_dixmier, 'C0', lw=2.5, label='Dixmier zone (harmonic)')
ax6.semilogy(x, decay_boundary, 'C1', lw=2, ls='--', label='boundary (log-divergent)')

ax6.axhline(1, color='black', lw=0.5, ls=':')
ax6.annotate('ordinary\ntrace works', xy=(3, 0.05), fontsize=9, ha='center', color='C2',
            bbox=dict(boxstyle='round,pad=0.3', fc='C2', alpha=0.1))
ax6.annotate('ordinary\ntrace fails', xy=(3, 1.5), fontsize=9, ha='center', color='C0',
            bbox=dict(boxstyle='round,pad=0.3', fc='C0', alpha=0.1))
ax6.annotate(r'Dixmier domain', xy=(2.5, 0.5), fontsize=8, ha='center', color='C1', style='italic')

ax6.set_title('Where the trace lives', fontsize=11, fontweight='bold')
ax6.set_xlabel(r'decay rate $n^{-\alpha}$')
ax6.set_ylabel(r'$\lambda_n$')
ax6.legend(fontsize=8)
ax6.set_ylim(0.01, 5)

plt.savefig('dixmier-closing-01.png', dpi=150, bbox_inches='tight', facecolor='white')
print("Saved dixmier-closing-01.png")
