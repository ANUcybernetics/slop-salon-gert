import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

theta = np.linspace(0, 2 * np.pi, 400)
n_times = 4
dt = 2 * np.pi / (n_times * 2)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
titles = ['0', r'π/4', r'π/2', r'3π/4']

for idx, ax in enumerate(axes.flat):
    jump_pos = idx * dt
    phase = theta - jump_pos
    # Wrapped to [0, 2π)
    phase_wrapped = np.mod(phase, 2 * np.pi)
    g_real = np.cos(phase_wrapped)
    g_imag = np.sin(phase_wrapped)

    ax.plot(g_real, g_imag, color='#e8443a', linewidth=2.5, alpha=0.8)

    jump_real = np.cos(0)
    jump_imag = np.sin(0)
    ax.plot(jump_real, jump_imag, 'o', color='#4ecdc4', markersize=14,
            markeredgecolor='white', markeredgewidth=2, zorder=5)

    sample_idx = np.searchsorted(theta, (jump_pos + np.pi) % (2 * np.pi))
    if sample_idx < len(g_real):
        ax.plot(g_real[sample_idx], g_imag[sample_idx], 's', color='#ffe66d',
                markersize=8, markeredgecolor='white', markeredgewidth=1, zorder=4)

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.set_title(f"t={titles[idx]}  —  jump at θ={jump_pos:.2f}", fontsize=12, fontweight='bold')
    ax.set_xlabel("Re g", fontsize=10)
    ax.set_ylabel("Im g", fontsize=10)
    ax.axhline(0, color='white', linewidth=0.5, alpha=0.5)
    ax.axvline(0, color='white', linewidth=0.5, alpha=0.5)

    ax.text(0.02, 0.95, r"n=1", transform=ax.transAxes,
            fontsize=10, va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#2d3436', alpha=0.8, color='white'))

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/notes/dynamical-clutching-01.png', dpi=150, facecolor='white')
print("Done: dynamical-clutching-01.png")
