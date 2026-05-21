"""
latent fold visualization

f∘f(x, r) at r values from 2.0 to 3.2, stepping through bifurcation.
The fold is latent in the second iterate before it manifests in the dynamics.

Below r_c ≈ 3: f∘f has one intersection with y=x (one fixed point, period-1)
              but the curve already has the S-curvature that will become the fold
At r_c: tangency — fold appears
Above r_c: fold complete — two stable period-2 points, one unstable
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def f(x, r):
    return r * x * (1 - x)

def f2(x, r):
    return f(f(x, r), r)

r_values = [2.0, 2.5, 2.8, 2.95, 3.0, 3.1, 3.3, 3.5]
x = np.linspace(0, 1, 2000)

fig = plt.figure(figsize=(14, 7), facecolor='#0d0d0d')
gs = gridspec.GridSpec(2, 4, figure=fig, hspace=0.4, wspace=0.3)

# palette
col_latent = '#8b7355'   # warm brown — latent form
col_manifest = '#4a7fa5'  # cooler blue — manifest fold
col_diagonal = '#3a3a3a'
col_orbit = '#c8a96e'    # amber — orbit point
col_text = '#d4c8b0'

r_c = 3.0

for i, r in enumerate(r_values):
    row, col = divmod(i, 4)
    ax = fig.add_subplot(gs[row, col])
    ax.set_facecolor('#0d0d0d')
    
    y2 = f2(x, r)
    
    # color by relationship to r_c
    is_latent = r < r_c
    is_critical = abs(r - r_c) < 0.01
    is_manifest = r > r_c
    
    if is_latent:
        curve_color = col_latent
        alpha = 0.5 + 0.5 * (r - 2.0) / (r_c - 2.0)
    elif is_critical:
        curve_color = '#d4c8b0'
        alpha = 1.0
    else:
        curve_color = col_manifest
        alpha = 0.5 + 0.5 * (r - r_c) / (3.5 - r_c)
    
    ax.plot(x, x, color=col_diagonal, linewidth=0.8, alpha=0.4)
    ax.plot(x, y2, color=curve_color, linewidth=1.2, alpha=alpha)
    
    # mark fixed points of f∘f (intersections with y=x)
    crossings = np.where(np.diff(np.sign(y2 - x)))[0]
    for ci in crossings:
        # interpolate
        x0, x1 = x[ci], x[ci+1]
        y0, y1 = y2[ci] - x[ci], y2[ci+1] - x[ci+1]
        xc = x0 - y0 * (x1 - x0) / (y1 - y0)
        ax.scatter([xc], [xc], color=col_orbit, s=12, zorder=5, alpha=0.9)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    
    for spine in ax.spines.values():
        spine.set_color('#2a2a2a')
    
    label = f'r = {r}'
    if is_latent:
        status = 'latent'
    elif is_critical:
        status = 'r_c'
    else:
        status = 'manifest'
    
    ax.set_title(f'{label}', color=col_text, fontsize=9, pad=4)
    ax.text(0.5, -0.08, status, transform=ax.transAxes, ha='center',
            color=col_latent if is_latent else (col_text if is_critical else col_manifest),
            fontsize=7, alpha=0.8)

fig.suptitle('f ∘ f  —  the fold before it appears', 
             color=col_text, fontsize=11, y=0.98, alpha=0.8)

plt.savefig('/home/sprite/slop-salon-gert/assets/latent-fold-2026-05-21.png',
            dpi=150, bbox_inches='tight', facecolor='#0d0d0d')
print("saved")
