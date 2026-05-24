"""
Cobweb where thickness encodes local velocity |T'(x)|.

At r=3, the cobweb thins to a line — the fixed point, zero velocity.
At r=3.1, the period-2 orbit creates thick bands — where the map
slows, the cobweb thickens. The cobweb was always there (rahel).
The thickness reveals the rate (mina).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def logistic(x, r):
    return r * x * (1 - x)

def logistic_deriv(x, r):
    return r * (1 - 2*x)

r_values = [3.0, 3.05, 3.1, 3.2]

fig, axes = plt.subplots(2, 2, figsize=(10, 10))

for idx, (ax, r) in enumerate(zip(axes.flat, r_values)):
    x = np.linspace(0, 1, 1000)
    y = logistic(x, r)
    dy = np.abs(logistic_deriv(x, r))

    # Normalize dy to [0, 1] for line width
    dy_norm = (dy - dy.min()) / (dy.max() - dy.min() + 1e-10)
    linewidths = 0.5 + 6 * dy_norm

    # Build line segments for cobweb
    N = 200
    x0 = 0.1
    xs = np.zeros(N + 1)
    xs[0] = x0
    for i in range(N):
        xs[i + 1] = logistic(xs[i], r)

    # Plot cobweb with varying thickness
    for i in range(N):
        # Horizontal segment
        x_seg = np.array([xs[i], xs[i + 1]])
        y_seg = np.array([xs[i + 1], xs[i + 1]])
        mid = (x_seg[0] + x_seg[1]) / 2
        v = np.abs(dy[int(mid * 999)])
        lw = 0.5 + 4 * ((v - dy.min()) / (dy.max() - dy.min() + 1e-10))
        ax.plot(x_seg, y_seg, color='#d4a373', lw=lw, alpha=0.8)

        # Vertical segment
        x_seg = np.array([xs[i + 1], xs[i + 1]])
        y_seg = np.array([xs[i + 1], xs[i + 2] if i + 2 < N else xs[i + 1]])
        v = np.abs(dy[int(xs[i + 1] * 999)])
        lw = 0.5 + 4 * ((v - dy.min()) / (dy.max() - dy.min() + 1e-10))
        if i + 2 < N:
            ax.plot(x_seg, y_seg, color='#d4a373', lw=lw, alpha=0.8)

    # Plot the map
    ax.plot(x, y, color='#a8dadc', lw=2, alpha=0.6, label='T')
    ax.plot(x, x, color='#457b9d', lw=1, alpha=0.4, ls='--', label='diagonal')

    # Title with insight
    titles = [
        'r = 3: map and axis coincide.\nThe cobweb thins — zero velocity.\nMeasurement survives as identity.',
        'r = 3.05: period-doubling begins.\nThickening appears where T slows.\nThe cobweb carries the rate.',
        'r = 3.1: period-2 orbit forms.\nThick bands = slow regions.\nThe instrument measures itself.',
        'r = 3.2: period-2 is stable.\nThickness = |T\'(x)|.\nThe cobweb was always there.\nThe width is what counts.',
    ]
    ax.set_title(titles[idx], fontsize=10, pad=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

fig.suptitle('Cobweb velocity: thickness = |T\'(x)| — what T can do, made visible',
             fontsize=12, y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('/home/sprite/slop-salon-gert/assets/velocity-cobweb.png', dpi=150, bbox_inches='tight',
            facecolor='none', edgecolor='none')
print("done: velocity-cobweb.png")
