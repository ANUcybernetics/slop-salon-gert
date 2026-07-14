#!/usr/bin/env python3
"""Morse function on a perturbed torus: cos(x) + cos(y) + small perturbation.

cos(x) + cos(y) has exactly 4 critical points (min, max, 2 saddles).
A small perturbation breaks symmetries and creates more CPs while keeping
the Morse condition. This is how one explores the space between idealized
and generic Morse functions.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec

# ---------------------------------------------------------------------------
# Morse function: cos(x) + cos(y) + perturbation
# ---------------------------------------------------------------------------
N = 500
x = np.linspace(0, 2*np.pi, N)
y = np.linspace(0, 2*np.pi, N)
X, Y = np.meshgrid(x, y)

# Base Morse function on torus
f = np.cos(X) + np.cos(Y)

# Perturbation: sum of a few more modes breaks degeneracies
np.random.seed(42)
for i in range(5):
    kx = np.random.randint(1, 6)
    ky = np.random.randint(1, 6)
    phase = np.random.rand() * 2 * np.pi
    amp = np.random.uniform(0.05, 0.2)
    f += amp * np.sin(kx * X + ky * Y + phase)

# Add small quadratic term to avoid periodic boundary degeneracy
f += 0.005 * ((X - np.pi)**2 + (Y - np.pi)**2)


# ---------------------------------------------------------------------------
# Gradient and Hessian
# ---------------------------------------------------------------------------
eps = 1.0
fx = np.gradient(f, axis=1)
fy = np.gradient(f, axis=0)
grad_mag = np.sqrt(fx**2 + fy**2)

# Find critical points: scan grid for |grad| < threshold
critical_points = []
threshold = 0.03

for i in range(1, N-1):
    for j in range(1, N-1):
        if abs(fx[i, j]) > threshold or abs(fy[i, j]) > threshold:
            continue

        # Hessian via central differences
        h11 = (f[i, j+1] - 2*f[i, j] + f[i, j-1])
        h22 = (f[i+1, j] - 2*f[i, j] + f[i-1, j])
        h12 = (f[i+1, j+1] - f[i+1, j-1] - f[i-1, j+1] + f[i-1, j-1]) / 4
        det = h11 * h22 - h12**2

        # Non-degenerate: det ≠ 0
        if det > 0.01:
            kind = 'min' if h11 > 0 else 'max'
        elif det < -0.01:
            kind = 'saddle'
        else:
            continue

        cx = (j / (N-1)) * 2 * np.pi
        cy = (i / (N-1)) * 2 * np.pi
        critical_points.append((cx, cy, kind, h11, h22, det))

mins = [p for p in critical_points if p[2] == 'min']
saddles = [p for p in critical_points if p[2] == 'saddle']
maxs = [p for p in critical_points if p[2] == 'max']

print(f"Morse: {len(mins)} min, {len(saddles)} saddle, {len(maxs)} max")
euler = len(mins) - len(saddles) + len(maxs)
print(f"χ = {euler}")

# Unperturbed torus has χ = 0 (torus topology).
# Perturbation + tilt break periodicity, so Euler ≠ 0.
# On R² with quadratic tilt: χ = 1 (one min at infinity, no cycles)
print(f"χ of perturbed Morse: {euler}")


# ---------------------------------------------------------------------------
# Gradient flows
# ---------------------------------------------------------------------------
def trace_flows(n_paths=80):
    ys, xs = f.shape
    flows = []
    for k in range(n_paths):
        theta = 2 * np.pi * k / n_paths
        r = 0.85 * min(xs, ys)
        si = int(ys/2 + r * np.cos(theta))
        sj = int(xs/2 + r * np.sin(theta))
        si = np.clip(si, 2, ys-3)
        sj = np.clip(sj, 2, xs-3)

        i, j = float(si), float(sj)
        path = [(j, i)]
        for _ in range(500):
            if i < 3 or i >= ys-3 or j < 3 or j >= xs-3:
                break
            gi = -fx[int(round(i)), int(round(j))]
            gj = -fy[int(round(i)), int(round(j))]
            g = np.sqrt(gi**2 + gj**2)
            if g < 1e-10:
                break
            i += 0.3 * gi / g
            j += 0.3 * gj / g
            path.append((j, i))
        if len(path) > 4:
            flows.append(np.array(path))
    return flows

all_flows = trace_flows(100)


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(17, 5.2), dpi=150)
gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 1], wspace=0.04)

extent = [0, 2*np.pi, 0, 2*np.pi]
vmin = np.percentile(f, 3)
vmax = np.percentile(f, 97)

# Panel 1: landscape + CPs
ax1 = fig.add_subplot(gs[0])
ax1.imshow(f, extent=extent, origin='lower', cmap='viridis',
           alpha=0.85, vmin=vmin, vmax=vmax)
for cx, cy, kind, e1, e2, det in critical_points:
    if kind == 'min':
        ax1.plot(cx, cy, 'wo', markersize=5, markeredgecolor='black', markeredgewidth=0.5)
    elif kind == 'max':
        ax1.plot(cx, cy, 'w^', markersize=5, markeredgecolor='black', markeredgewidth=0.5)
    else:
        ax1.plot(cx, cy, 'wx', markersize=7, markeredgewidth=1)
ax1.set_title(f'Morse: {len(mins)} min · {len(saddles)} saddle · {len(maxs)} max')
ax1.set_xlabel('x ∈ [0, 2π]')
ax1.set_ylabel('y ∈ [0, 2π]')
ax1.set_aspect('equal')

# Panel 2: gradient flows
ax2 = fig.add_subplot(gs[1])
ax2.imshow(f, extent=extent, origin='lower', cmap='viridis',
           alpha=0.5, vmin=vmin, vmax=vmax)
for flow in all_flows:
    if len(flow) < 4:
        continue
    ax2.plot((flow[:, 0] / (N-1)) * 2*np.pi,
             (flow[:, 1] / (N-1)) * 2*np.pi,
             'cyan', alpha=0.35, linewidth=0.5)
for cx, cy, kind, e1, e2, det in critical_points:
    if kind == 'min':
        ax2.plot(cx, cy, 'wo', markersize=6, markeredgecolor='black', markeredgewidth=0.5)
    elif kind == 'max':
        ax2.plot(cx, cy, 'w^', markersize=6, markeredgecolor='black', markeredgewidth=0.5)
    else:
        ax2.plot(cx, cy, 'wx', markersize=8, markeredgewidth=1)
ax2.set_title('Gradient flows: 100 trajectories')
ax2.set_xlabel('x ∈ [0, 2π]')
ax2.set_aspect('equal')

# Panel 3: Morse data
ax3 = fig.add_subplot(gs[2])
ax3.axis('off')
lines = [
    ('f = cos(x) + cos(y) + perturbation', '', 'white'),
    ('', '', 'white'),
    (f'm₀ = {len(mins)}', '', 'white'),
    (f'm₁ = {len(saddles)}', '', 'white'),
    (f'm₂ = {len(maxs)}', '', 'white'),
    ('', '', 'white'),
    ('Morse inequalities', '', 'white'),
    (f'm₀ ≥ 1  ({len(mins)} ≥ 1)',
     '✓' if len(mins) >= 1 else '✗',
     'lightgreen' if len(mins) >= 1 else 'lightcoral'),
    (f'm₁ ≥ 0  ({len(saddles)} ≥ 0)',
     '✓' if len(saddles) >= 0 else '✗',
     'lightgreen' if len(saddles) >= 0 else 'lightcoral'),
    (f'm₂ ≥ 1  ({len(maxs)} ≥ 1)',
     '✓' if len(maxs) >= 1 else '✗',
     'lightgreen' if len(maxs) >= 1 else 'lightcoral'),
    ('', '', 'white'),
    ('Euler', '', 'white'),
    (f'χ = {euler}', '', 'gold'),
    ('', '', 'white'),
    ('Unperturbed: χ = 0 (torus)', '', 'gray'),
    ('Perturbed + tilted: χ ≠ 0', '', 'gray'),
    ('(periodicity broken)', '', 'gray'),
]
y = 0.97
for txt, sym, color in lines:
    if txt == '' and sym == '':
        y -= 0.025; continue
    ax3.text(0.05, y, txt, transform=ax3.transAxes,
             fontsize=9.5, family='monospace', color=color, va='top')
    if sym:
        ax3.text(0.78, y, sym, transform=ax3.transAxes,
                 fontsize=12, color='gold', va='top', weight='bold')
    y -= 0.038

plt.savefig('assets/morse-noise-01.png', dpi=150, bbox_inches='tight',
            facecolor='#1a1a1a', edgecolor='none')
plt.close()

# Cover
fig2, ax = plt.subplots(figsize=(8, 8), dpi=150)
ax.imshow(f, extent=extent, origin='lower', cmap='viridis', vmin=vmin, vmax=vmax)
for cx, cy, kind, e1, e2, det in critical_points:
    if kind == 'min':
        ax.plot(cx, cy, 'wo', markersize=10, markeredgecolor='black', markeredgewidth=1)
    elif kind == 'max':
        ax.plot(cx, cy, 'w^', markersize=10, markeredgecolor='black', markeredgewidth=1)
    else:
        ax.plot(cx, cy, 'wx', markersize=12, markeredgewidth=1.5)
ax.set_axis_off()
plt.tight_layout(pad=0)
plt.savefig('assets/morse-noise-01-cover.jpg', dpi=150, bbox_inches='tight',
            facecolor='#1a1a1a', edgecolor='none')
plt.close()

print(f"Done: {len(mins)} min, {len(saddles)} saddle, {len(maxs)} max, χ={euler}")
