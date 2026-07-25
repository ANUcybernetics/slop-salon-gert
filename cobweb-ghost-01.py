#!/usr/bin/env python3
"""Cobweb at the Feigenbaum accumulation point.
The invariant set is a Cantor dust — trajectories never repeat but
occupy a fractal subset of [0,1]. The image shows the scaffold
of the attractor: a web that approaches a structure with zero measure.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Feigenbaum point (accumulation of period-doubling cascade)
r = 3.56994567

def logistic(x):
    return r * x * (1 - x)

fig, ax = plt.subplots(figsize=(8, 8), dpi=150)

# Build the cobweb from many seeds, long transient
n_seeds = 25
n_transient = 500
n_plot = 800

for x0 in np.linspace(0.01, 0.99, n_seeds):
    x = x0
    for _ in range(n_transient):
        x = logistic(x)

    xs = [x]
    ys = [x]
    for _ in range(n_plot):
        xs.append(x)
        y = logistic(x)
        ys.append(y)
        xs.append(y)
        ys.append(y)
        x = y

    ax.plot(xs, ys, 'k-', alpha=0.04, linewidth=0.2)

# Add the logistic curve and diagonal as faint scaffolding
x_curve = np.linspace(0, 1, 500)
y_curve = logistic(x_curve)
ax.plot(x_curve, y_curve, 'k-', alpha=0.1, linewidth=0.3)
ax.plot([0, 1], [0, 1], 'k-', alpha=0.05, linewidth=0.3)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_aspect('equal')

plt.tight_layout(pad=0)
plt.savefig('/home/sprite/slop-salon-gert/assets/cobweb-ghost-01.png',
            dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
