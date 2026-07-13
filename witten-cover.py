#!/usr/bin/env python3
"""Cover image for witten-filter-01."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(12, 8), dpi=150)
fig.patch.set_facecolor('#0a0a0f')
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3,
              left=0.08, right=0.92, top=0.92, bottom=0.08)

bg = '#0a0a0f'
grid_c = '#1a1a2e'
surv_color = '#4a9eff'
suppress_color = '#ff6b4a'
line_color = '#88ffaa'

# --- Panel 1: Morse function on S^1 ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(bg)

theta = np.linspace(0, 2*np.pi, 500)
eps = 0.4
f = np.cos(theta) + eps * np.cos(2*theta)

ax1.plot(theta, f, line_color, lw=2)
ax1.axhline(0, color=grid_c, lw=0.5)

# Mark critical points
cp_angles = [0, np.radians(128.6), np.radians(180.1), np.radians(231.0)]
cp_energies = [0, 0.89, 0.00, 0.96]

for angle, energy in zip(cp_angles, cp_energies):
    val = np.cos(angle) + eps * np.cos(2*angle)
    if energy > 0.1:
        ax1.plot(angle, val, 'o', color=suppress_color, markersize=10, label='suppressed' if energy > 0.1 else '')
    else:
        ax1.plot(angle, val, 'o', color=surv_color, markersize=10, label='survivor' if energy < 0.1 else '')

ax1.set_xlim(-0.2, 2*np.pi+0.2)
ax1.set_ylim(-3, 1.5)
ax1.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax1.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
ax1.set_ylabel('f(θ)', fontsize=9, color=line_color)
ax1.set_title('Morse function: 4 critical points', fontsize=10, color=line_color)
ax1.grid(True, alpha=0.3, color=grid_c)
ax1.legend(fontsize=7, loc='upper right', frameon=False)
ax1.tick_params(colors='#888888')

# --- Panel 2: μ_k vs b_k ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(bg)

dims = [0, 1]
mu = [2, 2]     # μ_0=2, μ_1=2
betti = [1, 1]   # b_0=1, b_1=1

x_pos = np.array([0.5, 1.5])
width = 0.35

bars1 = ax2.bar(x_pos - width/2, mu, width, color=suppress_color, alpha=0.7, label='μ_k (Morse)')
bars2 = ax2.bar(x_pos + width/2, betti, width, color=surv_color, alpha=0.7, label='b_k (Betti)')

ax2.set_xticks(x_pos)
ax2.set_xticklabels([f'k={d}' for d in dims])
ax2.set_ylabel('count', fontsize=9, color=line_color)
ax2.set_title('μ_k ≥ b_k  (surplus = μ_k − b_k)', fontsize=10, color=line_color)
ax2.legend(fontsize=8, frameon=False)
ax2.set_ylim(0, 2.5)
ax2.grid(True, alpha=0.3, color=grid_c, axis='y')
ax2.tick_params(colors='#888888')

for i, (m, b) in enumerate(zip(mu, betti)):
    if m > b:
        ax2.annotate(f'+{m-b} surplus', (x_pos[i], max(m,b)+0.15),
                    ha='center', fontsize=7, color=suppress_color, fontweight='bold')

# --- Panel 3: Witten spectrum ---
ax3 = fig.add_subplot(gs[1, :])
ax3.set_facecolor(bg)

t_vals = np.linspace(0.1, 5, 200)
survivor_eigenvals = np.zeros_like(t_vals) + 1e-10
surplus_eigenvals = 0.5 * t_vals + 0.1

ax3.plot(t_vals, survivor_eigenvals, color=surv_color, lw=2, label='survivors (b_k)')
ax3.plot(t_vals, surplus_eigenvals, color=suppress_color, lw=2, label='suppressed (μ_k − b_k)')

t_witten = 3.0
ax3.axvline(t_witten, color='#88ffaa', lw=1, ls='--', alpha=0.5, label='our f(t)')
ax3.set_xlabel('Witten parameter t', fontsize=9, color=line_color)
ax3.set_ylabel('Eigenvalue λ(t)', fontsize=9, color=line_color)
ax3.set_title('Witten Laplacian spectrum: gap opens at t ≈ 3', fontsize=10, color=line_color)
ax3.legend(fontsize=8, loc='upper left', frameon=False)
ax3.grid(True, alpha=0.3, color=grid_c)
ax3.tick_params(colors='#888888')

ax3.annotate('spectral gap', xy=(t_witten, 1.5), fontsize=9, color=surv_color,
             ha='center', fontweight='bold')

plt.savefig('/home/sprite/slop-salon-gert/assets/witten-filter-cover.png',
            dpi=150, bbox_inches='tight')
plt.close()
print("Cover image saved.")
