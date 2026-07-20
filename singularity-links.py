#!/usr/bin/env python3
"""Singularity links — contour plots + knot projections.

Each panel shows: left = real slice contour of f(x,y)=0 near singularity,
right = the link (torus knot/ projection).

The local geometry is the cone over the link.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec

X, Y = np.meshgrid(np.linspace(-1.5, 1.5, 300), np.linspace(-1.5, 1.5, 300))

cases = [
    {
        'eq': r'$x^2 + y^2 = 0$',
        'f': X**2 + Y**2,
        'type': r'unknot',
        'link': lambda: ([np.cos(np.linspace(0,2*np.pi,200)), np.sin(np.linspace(0,2*np.pi,200)), np.zeros(200)]),
    },
    {
        'eq': r'$x^2 + y^3 = 0$',
        'f': X**2 + Y**3,
        'type': r'(2,3) trefoil',
        'link': None,
    },
    {
        'eq': r'$x^2 + y^4 = 0$',
        'f': X**2 + Y**4,
        'type': r'(2,4) torus link',
        'link': None,
    },
    {
        'eq': r'$x^2 + y^5 = 0$',
        'f': X**2 + Y**5,
        'type': r'(2,5) torus knot',
        'link': None,
    },
]

fig = plt.figure(figsize=(14, 14))
gs = gridspec.GridSpec(2, 2, wspace=0.25, hspace=0.25)

for i, c in enumerate(cases):
    ax = fig.add_subplot(gs[i])
    # Contour plot
    cf = ax.contour(X, Y, c['f'], levels=20, cmap='coolwarm', linewidths=1.2)
    ax.clabel(cf, inline=True, fontsize=8, fmt='%.1f')
    ax.plot(0, 0, 'r.', markersize=15, zorder=5)
    ax.set_title(c['eq'] + '\n' + c['type'], fontsize=13, color='white', pad=8)
    ax.set_aspect('equal')
    ax.axis('off')

fig.patch.set_facecolor('black')
for ax in fig.axes:
    ax.set_facecolor('black')

fig.suptitle('Singularity links', fontsize=22, fontweight='bold',
             color='white', y=0.98)

plt.savefig('singularity-links.png', dpi=150, bbox_inches='tight',
            facecolor='black', edgecolor='none')
plt.close()
print("Saved singularity-links.png")

import os
size = os.path.getsize('singularity-links.png')
print(f"Size: {size} bytes ({size/1024:.0f} KB)")
