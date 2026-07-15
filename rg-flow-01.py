#!/usr/bin/env python3
"""Renormalization group flow for the 2D Ising model.

RG flow lines in coupling space mirror gradient flow: both are vector fields
with fixed points governing trajectories. RG lives in the space of Hamiltonians
— it tells you how the system rewrites itself at different scales.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

np.random.seed(42)

# ---------------------------------------------------------------------------
# Ising model parameters
# ---------------------------------------------------------------------------
Kc = 0.4406868  # exact critical coupling for 2D Ising

# ---------------------------------------------------------------------------
# RG flow: simplified 1D beta function for K (h = 0)
# dK/dl > 0 for K > Kc (flows to ordered phase)
# dK/dl < 0 for K < Kc (flows to disordered phase)
# This captures the essential separatrix structure
# ---------------------------------------------------------------------------
K_range = np.linspace(0.05, 2.0, 30)
h_range = np.linspace(-0.6, 0.6, 30)
K_grid, h_grid = np.meshgrid(K_range, h_range)

# Beta functions: critical point at Kc, stable fixed points at K→0 and K→∞
# dK/dl = (K - Kc) * (K > Kc ? 1 : -1)  essentially
# More smoothly: dK/dl = (K - Kc) * tanh(K) / tanh(Kc)
# This gives: dK/dl > 0 for K > Kc, dK/dl < 0 for K < Kc
dK = (K_grid - Kc) * np.tanh(K_grid) / (np.tanh(Kc) + 1e-10)

# h always flows to zero (relevant operator at critical point, irrelevant elsewhere)
# At Kc, h grows (unstable direction); away from Kc, h decays
dh = h_grid * (1 - Kc / (K_grid + 0.3))

# Normalize
magnitude = np.sqrt(dK**2 + dh**2)
dK_n = dK / (magnitude + 1e-10)
dh_n = dh / (magnitude + 1e-10)

# ---------------------------------------------------------------------------
# Magnetization curve from Onsager exact solution
# ---------------------------------------------------------------------------
def magnetization_onsager(K):
    """Spontaneous magnetization from Onsager's exact solution."""
    m = (1 - (1.0 / np.sinh(K)**4))
    m = np.where(m > 0, m, 0)
    return m**0.25

K_vals = np.linspace(0.05, 2.0, 200)
m_vals = np.array([magnetization_onsager(k) for k in K_vals])

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(14, 5.5))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.3, 1])

# --- Left panel: RG flow ---
ax1 = fig.add_subplot(gs[0])

stream = ax1.streamplot(K_grid, h_grid, dK, dh,
                        color=magnitude,
                        linewidth=1.5,
                        cmap='coolwarm',
                        arrowsize=1.2,
                        density=1.0)

# Fixed points
ax1.plot(Kc, 0, 'rs', markersize=14, zorder=10,
         label=f'critical (Kc = {Kc:.3f})')
ax1.plot(0, 0, 'bo', markersize=10, zorder=10,
         label='disordered (K = 0)')
ax1.plot(2.0, 0, 'go', markersize=10, zorder=10,
         label='ordered (K → ∞)')

ax1.axhline(y=0, color='white', linestyle='--', alpha=0.3, linewidth=1)

ax1.set_xlabel('Coupling K = βJ', fontsize=12)
ax1.set_ylabel('Field h', fontsize=12)
ax1.set_title('RG flow in coupling space', fontsize=14, fontweight='bold')
ax1.set_xlim(0, 2.0)
ax1.set_ylim(-0.6, 0.6)
ax1.legend(fontsize=8, loc='upper left')
ax1.set_aspect('equal')
ax1.grid(alpha=0.15)

cbar = fig.colorbar(stream.lines, ax=ax1, pad=0.02)
cbar.set_label('flow speed', fontsize=10)

# --- Right panel: magnetization curve ---
ax2 = fig.add_subplot(gs[1])

ax2.plot(K_vals, m_vals, 'k-', linewidth=2.5, label='magnetization')
ax2.axvline(Kc, color='red', linestyle='--', alpha=0.5, linewidth=1.5,
            label=f'Kc = {Kc:.3f}')
ax2.fill_between(K_vals, 0, m_vals, where=(K_vals >= Kc),
                  alpha=0.3, color='steelblue', label='ordered phase')
ax2.fill_between(K_vals, 0, m_vals, where=(K_vals < Kc),
                  alpha=0.3, color='coral', label='disordered phase')

ax2.set_xlabel('Coupling K = βJ', fontsize=12)
ax2.set_ylabel('Magnetization m', fontsize=12)
ax2.set_title('Magnetization (Onsager exact)', fontsize=14, fontweight='bold')
ax2.set_xlim(0, 2.0)
ax2.set_ylim(0, 1.15)
ax2.legend(fontsize=9)
ax2.grid(alpha=0.15)

ax2.annotate('ordered', xy=(1.4, 0.18), fontsize=16, color='steelblue',
             fontweight='bold')
ax2.annotate('disordered', xy=(0.15, 0.08), fontsize=16, color='coral',
             fontweight='bold')
ax2.annotate('critical', xy=(Kc, 0.03), fontsize=12, color='red',
             fontweight='bold', ha='center')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/rg-flow-01.png', dpi=150,
            bbox_inches='tight', facecolor='white')
print("Written: rg-flow-01.png")
