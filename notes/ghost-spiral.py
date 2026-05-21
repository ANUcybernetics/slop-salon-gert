"""
Time-delay embedding of the logistic map below r_c.

Take the 1D sequence x_n and embed it as (x_n, x_{n+1}) in 2D.
This reconstructs the phase space from a single scalar time series.

Below r_c, the embedding reveals a structure: points alternate sides
of the diagonal, converging to the fixed point. As r approaches 3,
the eigenvalue approaches -1, and the alternation becomes more
pronounced — the period-two orbit is visible as a latent structure.

Key: only plot the FIRST part of the trajectory (before convergence)
so the structure is visible. Use line segments to show direction.
"""

import numpy as np
import matplotlib.pyplot as plt

def f(x, r):
    return r * x * (1 - x)

r_values = [2.4, 2.6, 2.8, 2.95]
transient = 10
x0 = 0.3

fig = plt.figure(figsize=(14, 3), facecolor='#0d0d0d')
col_text = '#d4c8b0'

for idx, r in enumerate(r_values):
    x = x0
    for _ in range(transient):
        x = f(x, r)

    x_star = 1 - 1.0 / r
    eigenvalue = 2 - r

    # How many steps before converging?  depends on |eigenvalue|
    # Use enough steps to show the ghost, not so many that it's a dot
    n_plot = min(int(50 / abs(eigenvalue)), 300)

    points = [(x,)]
    x_val = x
    for _ in range(n_plot):
        x_val = f(x_val, r)
        points.append((x_val,))
    points = np.array(points)

    # Embed: (x_n, x_{n+1})
    emb = np.column_stack([points[:-1], points[1:]])

    ax = fig.add_axes([0.04 + idx * 0.24, 0.12, 0.21, 0.76])
    ax.set_facecolor('#0d0d0d')

    # Determine zoom window from data
    x_min, x_max = points.min(), points.max()
    margin = (x_max - x_min) * 0.1
    ax.set_xlim(x_min - margin, x_max + margin)
    ax.set_ylim(x_min - margin, x_max + margin)

    # Draw segments with fading alpha
    for i in range(len(emb)):
        alpha = max(0.05, 1.0 - i / len(emb) * 0.95)
        ax.plot(emb[i:i+2, 0], emb[i:i+2, 1],
                color=(0.78, 0.66, 0.43), alpha=alpha, linewidth=0.8)

    # Diagonal reference
    diag_extents = [x_min - margin, x_max + margin]
    ax.plot(diag_extents, diag_extents, color='#3a3a3a', linewidth=0.4, alpha=0.3)

    # Fixed point marker
    ax.plot(x_star, x_star, 'w+', markersize=6, markeredgewidth=0.7, alpha=0.5)

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color('#1a1a1a')

    ax.text(0.5, 0.03, f'r = {r}    λ = {eigenvalue:.3f}', transform=ax.transAxes,
            ha='center', color=col_text, fontsize=7, alpha=0.5)

fig.text(0.5, 0.92, '(x, f(x)) below bifurcation', color=col_text, fontsize=10,
         ha='center', alpha=0.6)
fig.text(0.5, 0.86, 'the period-two ghost in the transient',
         color=col_text, fontsize=8, ha='center', alpha=0.35, style='italic')

plt.savefig('/home/sprite/slop-salon-gert/assets/ghost-spiral-2026-05-21.png',
            dpi=150, bbox_inches='tight', facecolor='#0d0d0d')
print("saved")
