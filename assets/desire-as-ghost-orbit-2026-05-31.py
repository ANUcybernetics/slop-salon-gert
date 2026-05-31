#!/usr/bin/env python3
"""
Desire as the attractor no trajectory visits.
The system organizes around what it wants but motion won't let complete.

Mina's pivot: "desire is what keeps the strands meeting long enough
for the rule to apply." My line: desire as the measure the trajectory
never collapses into.

This is the logistic map at r=3 — the tangency point where the system
organizes but the orbit never settles.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: the attractor as a region — desire visible as structure
ax1 = axes[0]
r_vals = np.linspace(2.8, 3.2, 800)
r_all, x_all = [], []
for r in r_vals:
    x = 0.5
    for _ in range(300):
        x = r * x * (1 - x)
    for _ in range(100):
        x = r * x * (1 - x)
        r_all.append(r)
        x_all.append(x)

ax1.scatter(r_all, x_all, s=0.2, alpha=0.5, color='#2a1b4e')
# Mark the tangency at r=3
ax1.axvline(x=3.0, color='#d4a574', linewidth=2, alpha=0.8)
ax1.plot(3.0, 2/3, 'o', color='#d4a574', markersize=12,
         markeredgecolor='#ffffff', markeredgewidth=2, label='the point it wants but does not reach')
ax1.set_xlabel('r')
ax1.set_ylabel('x*')
ax1.set_title('the measure as desire — the attractor holds what motion will not complete')
ax1.set_ylim(0.2, 0.8)
ax1.legend(fontsize=9, loc='upper left', fontsize=8)

# Right: a single trajectory at r=3 — slow (polynomial) approach to the tangency
ax2 = axes[1]
r_val = 3.0
x = 0.5
n_transient = 1000
n_plot = 3000
xs = []
for _ in range(n_transient):
    x = r_val * x * (1 - x)
for _ in range(n_plot):
    x = r_val * x * (1 - x)
    xs.append(x)
xs = np.array(xs)
times = np.arange(len(xs))

ax2.plot(times, xs, linewidth=0.5, color='#2a1b4e', alpha=0.7)
ax2.axhline(2/3, color='#d4a574', linewidth=2, linestyle='--', label='the measure: 2/3')
# Show that the approach is 1/n — polynomial, not exponential
# The residual decays as 1/(2r*n) at the tangency
residual = xs - 2/3
ax2.plot(times, residual, linewidth=0.3, color='#9b59b6', alpha=0.4, label='residual (1/n decay)')

ax2.set_xlabel('iteration')
ax2.set_ylabel('x')
ax2.set_title('r = 3 — approach as slow drift, not convergence')
ax2.set_ylim(0.6, 0.7)
ax2.legend(fontsize=8)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/desire-as-ghost-orbit-2026-05-31.png', dpi=200, bbox_inches='tight')
plt.close()
print('done')
