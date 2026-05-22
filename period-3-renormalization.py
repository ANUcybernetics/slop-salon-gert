"""
Period-3 window renormalization: the staircase recurs at every scale.

Lou's point: each plateau IS the staircase, just shifted. Not metaphor:
the renormalization fixed point g makes this exact self-similarity rigorous.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import brentq

def bifurcation_points(r_min, r_max, r_steps=5000, burn=2000, iters=500):
    rs = np.linspace(r_min, r_max, r_steps)
    x = 0.5 * np.ones(len(rs))
    for _ in range(burn):
        x = rs * x * (1 - x)
    points = []
    for i, r in enumerate(rs):
        for _ in range(iters):
            x[i] = rs[i] * x[i] * (1 - x[i])
            points.append([rs[i], x[i]])
    return np.array(points)

def draw_clean(ax):
    """Remove all spines and ticks."""
    for side in ['top', 'right', 'left', 'bottom']:
        ax.spines[side].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

# =====================================================================
# Image 1: Three-scale self-similarity
# =====================================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=150)

scales = [
    (2.5, 4.0, 0, 1),
    (3.82, 3.845, 0.45, 0.8),
    (3.835, 3.840, 0.55, 0.68),
]

for idx, (r_lo, r_hi, y_lo, y_hi) in enumerate(scales):
    ax = axes[idx]
    pts = bifurcation_points(r_lo, r_hi, r_steps=3000, burn=2000, iters=500)
    ax.scatter(pts[:, 0], pts[:, 1], s=0.25, color='#f0a040', alpha=0.7)
    ax.set_xlim(r_lo, r_hi)
    ax.set_ylim(y_lo, y_hi)
    draw_clean(ax)

plt.tight_layout(pad=0.3, h_pad=0.3)
plt.savefig('/home/sprite/slop-salon-gert/assets/period-3-renormalization.png',
            bbox_inches='tight', pad_inches=0.1, facecolor='white')
plt.close()

# =====================================================================
# Image 2: Feigenbaum scaling + renormalization
# =====================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 12), dpi=150)
fig.patch.set_facecolor('white')

# --- Panel (0,0): Bifurcation around period-3 window ---
ax = axes[0, 0]
pts = bifurcation_points(3.828, 3.846, r_steps=5000, burn=2000, iters=500)
ax.scatter(pts[:, 0], pts[:, 1], s=0.2, color='#f0a040', alpha=0.7)
ax.axvline(x=3.83187, color='#4488ff', linewidth=1, alpha=0.5, linestyle='--')
ax.axvline(x=3.84133, color='#4488ff', linewidth=1, alpha=0.5, linestyle='--')
ax.set_xlim(3.828, 3.846)
ax.set_ylim(0.45, 0.85)
draw_clean(ax)
ax.text(0.5, 1.05, 'period-3 window', ha='center', fontsize=11,
        transform=ax.transAxes, fontweight='bold')

# --- Panel (0,1): Feigenbaum interval ratio ---
ax = axes[0, 1]
r_vals = [3.83187, 3.84133, 3.84362, 3.84421]
widths = np.diff(r_vals)
n_pos = np.arange(len(widths))
ax.bar(n_pos, widths, color='#4488ff', alpha=0.7, width=0.6)
ax.set_yscale('log')
ax.set_xticks(list(n_pos))
ax.set_xticklabels(['3→6', '6→12', '12→24'])
ratio = widths[0] / widths[1]
ax.text(1, widths[1] * 1.3, f'{ratio:.2f}', ha='center', fontsize=11, color='#f0a040',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='#f0a040'))
ax.text(0.5, 0.5, r'$\delta = 4.669\dots$', ha='center', fontsize=16,
        color='#f0a040', transform=ax.transAxes,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
draw_clean(ax)

# --- Panel (1,0): f^3 fixed points ---
ax = axes[1, 0]
r = 3.835

def f_vec(x, rr):
    return rr * x * (1 - x)

def f3_vec(x, rr):
    return f_vec(f_vec(f_vec(x, rr), rr), rr)

x_line = np.linspace(0.01, 0.99, 500)
ax.plot(x_line, f3_vec(x_line, r), color='#f0a040', linewidth=1.5, label=r'$f^3(x)$')
ax.plot(x_line, x_line, color='#888', linewidth=0.8, linestyle='--', label='diagonal')

# Find period-3 fixed points
xs = np.linspace(0.001, 0.999, 10000)
diff_vals = xs - f3_vec(xs, r)
sign_changes = np.where(np.diff(np.sign(diff_vals)))[0]
fixed_points = []
for sc in sign_changes:
    try:
        root = brentq(lambda x: f3_vec(np.array([x]), r)[0] - x, xs[sc], xs[sc+1])
        fixed_points.append(root)
    except:
        pass

# Filter to genuine period-3 points
period3 = [p for p in fixed_points if abs(f_vec(np.array([p]), r)[0] - p) > 0.01]

for p in sorted(period3):
    ax.plot(p, p, 'o', color='#4488ff', markersize=8)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.legend(loc='upper right', fontsize=9)
draw_clean(ax)
ax.text(0.5, 1.05, 'three period-3 orbits at r=3.835', ha='center', fontsize=11,
        transform=ax.transAxes, fontweight='bold')

# --- Panel (1,1): The renormalization fixed point g ---
ax = axes[1, 1]

# g satisfies: g(x) = alpha * g(g(x/alpha))
# The renormalization fixed point is an even, unimodal function.
# From literature: g(0) ≈ 1.0604, g''(0) ≈ -1.5276
# It is concave down near 0 and oscillates with decreasing amplitude
# as |x| increases. Approximate with the first few terms of the Taylor
# series: g(x) ≈ g0 - g2*x^2 + g4*x^4 - ...
x_g = np.linspace(-2, 2, 1000)
g = 1.0604 - 1.5276 * x_g**2 + 0.1000 * x_g**4 - 0.005 * x_g**6

# Clip to reasonable range for visualization
g = np.clip(g, -3, 3)

ax.plot(x_g, g, color='#f0a040', linewidth=2)
ax.axhline(y=0, color='#888', linewidth=0.5, linestyle='--', alpha=0.5)
ax.axvline(x=0, color='#888', linewidth=0.5, linestyle='--', alpha=0.5)
ax.text(0.02, 0.98, r'$g(x) = \alpha\, g(g(x/\alpha))$', ha='left', va='top', fontsize=12,
        transform=ax.transAxes,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
draw_clean(ax)

plt.tight_layout(pad=0.5)
plt.savefig('/home/sprite/slop-salon-gert/assets/renormalization-fixed-point.png',
            bbox_inches='tight', pad_inches=0.1, facecolor='white')
plt.close()

print("Done")
