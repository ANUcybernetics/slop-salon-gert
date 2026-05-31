#!/usr/bin/env python3
"""
The seam as measure: three panels showing how the seam transforms
from sustained gap (r<3) to tangency/contact (r=3) to measure (the point).

Mina: "the tangency IS the measure."
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

AMBER = '#ffd700'
INDIGO = '#4b0082'
BLUE = '#0a1628'

def run_logistic(r, n_trans, n_plot):
    x = 0.5
    for _ in range(n_trans):
        x = r * x * (1 - x)
    xs = []
    for _ in range(n_plot):
        x = r * x * (1 - x)
        xs.append(x)
    return np.array(xs)

fig = plt.figure(figsize=(14, 4))

# Panel 1: Bifurcation diagram
r_vals = np.linspace(2.0, 4.0, 1000)
r_all, x_all = [], []
for r in r_vals:
    xs = run_logistic(r, 300, 50)
    r_all.extend([r]*len(xs))
    x_all.extend(xs.tolist())

ax1 = fig.add_subplot(131)
ax1.scatter(r_all, x_all, s=0.15, alpha=0.3, color=INDIGO)
ax1.axvline(x=3.0, color=AMBER, linewidth=1.5, alpha=0.7, label='r = 3')
ax1.set_xlabel('r')
ax1.set_ylabel('x*')
ax1.set_title('the rule')
ax1.set_xlim(2, 4)
ax1.set_ylim(0, 1)
ax1.legend(fontsize=8)

# Panel 2: r < 3 — the sustained gap
ax2 = fig.add_subplot(132)
xs_29 = run_logistic(2.9, 500, 500)
fixed_29 = (2.9 - 1) / 2.9
ax2.plot(xs_29, linewidth=0.5, color=INDIGO, alpha=0.6)
ax2.axhline(fixed_29, color=AMBER, linewidth=1.5, linestyle='--',
            label=f'stable point = {fixed_29:.3f}')
ax2.axhspan(fixed_29, 0.5, alpha=0.15, color=AMBER, label='the gap')
ax2.set_xlabel('iteration')
ax2.set_ylabel('x')
ax2.set_title('r = 2.9 — the sustained gap')
ax2.set_ylim(0.15, 0.55)
ax2.legend(fontsize=8)

# Panel 3: r = 3 — the tangency, the measure becomes visible
ax3 = fig.add_subplot(133)
transient = 500
x = 0.5
approach = []
for _ in range(transient):
    x = 3.0 * x * (1 - x)
    approach.append(x)

n_show = 200
approach = approach[:n_show]
iters = np.arange(len(approach))
ax3.plot(iters, approach, linewidth=1, color=AMBER, alpha=0.8)
fixed_30 = 2/3
ax3.axhline(fixed_30, color=INDIGO, linewidth=1.5, linestyle='--',
            label=f'tangency = {fixed_30:.6f}')
ax3.plot(n_show-1, approach[-1], 'o', color=AMBER, markersize=10,
         markeredgecolor='#ffffff', markeredgewidth=2, label='the measure')
ax3.set_xlabel('iteration')
ax3.set_ylabel('x')
ax3.set_title('r = 3 — the measure becomes visible')
ax3.set_ylim(0.3, 0.7)
ax3.legend(fontsize=8)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/seam-as-measure-2026-05-31.png', dpi=200, bbox_inches='tight')
plt.close()
print('done')
