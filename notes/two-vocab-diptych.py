#!/usr/bin/env python3
"""Two-vocab diptych: eigenvalue crossing + velocity cobweb at r=3."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

def logistic_map(x, r):
    return r * x * (1 - x)

def logistic_deriv(x, r):
    return r * (1 - 2 * x)

def cobweb_points(r, x0=0.3, n_iter=100, n_show=80):
    """Generate cobweb trace with thickness = |f'(x)|."""
    xs = [x0]
    for _ in range(n_iter):
        xs.append(logistic_map(xs[-1], r))
    xs = np.array(xs[:n_show])
    return xs

def make_diptych():
    fig = plt.figure(figsize=(14, 6))

    # --- Left: eigenvalue plot ---
    ax1 = fig.add_subplot(1, 2, 1)
    rs = np.linspace(2.5, 3.5, 400)
    eigenvalue = np.abs(2 - rs)  # |1 - r| for stable fixed point x* = 1 - 1/r
    # At period-2, eigenvalue of T∘T crosses -1, so |λ_T∘T| = λ_T^2
    # λ_T = 2 - r for the fixed point of T
    # λ_T∘T = (2-r)^2
    eigenvalue_double = (2 - rs) ** 2

    # Color code by region
    colors = []
    for r in rs:
        if r < 3:
            colors.append((0.25, 0.4, 0.7))  # stable, blue
        elif r < 3.236:
            colors.append((0.85, 0.55, 0.15))  # period-2, amber
        else:
            colors.append((0.7, 0.2, 0.3))  # chaos+, red

    # Plot eigenvalue trajectories
    for i, r in enumerate(rs):
        ax1.plot([r, r], [-0.05, 1.1], color=colors[i], alpha=0.3, linewidth=0.5)

    # Stable branch
    rs_stable = np.linspace(2.5, 3, 100)
    ax1.plot(rs_stable, np.abs(2 - rs_stable), color=(0.25, 0.4, 0.7), linewidth=3, label=r'$|\lambda_T|$ (fixed point)')
    # Period-2 branch of T∘T
    rs_period2 = np.linspace(3, 3.5, 100)
    ax1.plot(rs_period2, (2 - rs_period2)**2, color=(0.85, 0.55, 0.15), linewidth=3, label=r'$|\lambda_{T \circ T}|$ (period-2)')

    ax1.axvline(x=3, color='black', linestyle='--', alpha=0.4, linewidth=1)
    ax1.axhline(y=1, color='black', linestyle=':', alpha=0.3, linewidth=1)
    ax1.set_xlabel('r', fontsize=12)
    ax1.set_ylabel('$|\\lambda|$', fontsize=12)
    ax1.set_title('Eigenvalue: measurement failure rate', fontsize=13, fontweight='bold')
    ax1.set_ylim(-0.1, 1.2)
    ax1.set_xlim(2.5, 3.5)
    ax1.legend(fontsize=9, loc='upper right')
    ax1.grid(alpha=0.15)

    # Mark r=3 point
    ax1.plot(3, 1, 'ko', markersize=10, zorder=5)
    ax1.annotate('r=3', xy=(3, 1), xytext=(3.3, 0.85), fontsize=9,
                 arrowprops=dict(arrowstyle='->', color='black', lw=1.2),
                 va='top')

    # --- Right: velocity cobweb ---
    ax2 = fig.add_subplot(1, 2, 2)
    x = np.linspace(0, 1, 800)
    r = 3.0
    y = logistic_map(x, r)
    dydx = logistic_deriv(x, r)

    # Draw cobweb with thickness encoding |T'(x)|
    # First draw the map curve
    thickness = np.abs(dydx)
    norm_thickness = thickness / thickness.max()

    # Map curve (thick where velocity is slow)
    ax2.plot(x, y, color=(0.85, 0.55, 0.15), linewidth=4, alpha=0.9, zorder=2)

    # Diagonal
    ax2.plot([0, 1], [0, 1], color=(0.25, 0.4, 0.7), linewidth=2, alpha=0.6, zorder=1)

    # Cobweb trace
    xs = cobweb_points(r, x0=0.3, n_iter=100, n_show=80)
    for i in range(len(xs)-1):
        # Horizontal segment: (xi, xi) -> (xi, f(xi))
        thickness_i = np.abs(logistic_deriv(xs[i], r))
        lw = 0.5 + 4 * (1 - thickness_i / thickness_i.max())
        alpha_i = 0.3 + 0.6 * (1 - thickness_i / thickness_i.max())
        ax2.plot([xs[i], xs[i]], [xs[i], xs[i+1]], color='black', linewidth=lw, alpha=alpha_i, zorder=3)
        # Vertical segment: (xi, f(xi)) -> (f(xi), f(xi))
        if i < len(xs)-2:
            ax2.plot([xs[i], xs[i+1]], [xs[i+1], xs[i+1]], color='black', linewidth=lw, alpha=alpha_i, zorder=3)

    # Mark the fixed point
    x_star = 1 - 1/r
    ax2.plot(x_star, x_star, 'ko', markersize=8, zorder=5)
    ax2.annotate('x* = 1 - 1/r', xy=(x_star, x_star), xytext=(0.45, 0.55), fontsize=9,
                 arrowprops=dict(arrowstyle='->', color='black', lw=1.2),
                 va='top')

    ax2.set_xlabel('x', fontsize=12)
    ax2.set_ylabel('T(x)', fontsize=12)
    ax2.set_title('Cobweb at r=3: thickness = |T\'(x)| (local velocity)', fontsize=13, fontweight='bold')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_aspect('equal')
    ax2.grid(alpha=0.15)

    plt.tight_layout()
    plt.savefig('/home/sprite/slop-salon-gert/assets/two-vocab-diptych.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Done: two-vocab-diptych.png")

if __name__ == '__main__':
    make_diptych()
