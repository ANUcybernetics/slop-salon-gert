#!/usr/bin/env python3
"""
Morse-Smale flow: gradient trajectories on a Morse function landscape.

f(θ, r) = cos(θ) + ε·cos(2θ) + r²
Angular part has 4 critical points (2 min at ±2.27, 2 max at ±0.87).
Radial part has 1 minimum at r=0.
Combined: 4 product critical points — 1 min (r=0, θ=±2.27 shared), 2 saddles, 1 max.

Panel 1: 3D surface plot (θ mapped to x-axis via cos/sin for visual interest)
Panel 2: 2D stream plot — gradient flow in (θ, r) plane
Panel 3: Morse-Smale cell decomposition — attraction basins of the minimum
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

eps = 0.4

def morse_surface(theta, r):
    return np.cos(theta) + eps * np.cos(2*theta) + r**2

def morse_grad(theta, r):
    """∇f = (df/dtheta, df/dr). Flow: dγ/dt = -∇f."""
    df_dtheta = -np.sin(theta) - 2*eps*np.sin(2*theta)
    df_dr = 2*r
    return df_dtheta, df_dr

def trace_flow(start_theta, start_r, dt=0.01, max_steps=1000):
    thetas = [start_theta]
    rs = [start_r]
    t, r = start_theta, start_r
    for _ in range(max_steps):
        gt, gr = morse_grad(t, r)
        t -= dt * gt
        r -= dt * gr
        t = ((t + np.pi) % (2*np.pi)) - np.pi
        r = np.clip(r, 0.01, 0.99)
        if gr < -0.1 and r < 0.05:
            break
        thetas.append(t)
        rs.append(r)
    return np.array(thetas), np.array(rs)

# --- 4 critical points of the angular Morse function ---
# cos(θ) + ε·cos(2θ): derivative = -sin(θ) - 2ε·sin(2θ) = 0
# sin(θ)(1 + 4ε·cos(θ)) = 0
# Solutions: sin(θ) = 0 → θ = 0, π
# Or cos(θ) = -1/(4ε) = -0.625 → θ = ±2.25

# Exact critical points
cp = [
    (0.0,     0.0, 'saddle'),  # max in θ, min in r
    (np.pi,   0.0, 'saddle'), # max in θ, min in r
    (2.255,   0.0, 'min'),    # min in θ, min in r
    (-2.255,  0.0, 'min'),    # min in θ, min in r
]

# Actually need to classify properly
# Hessian: d²f/dθ² = -cos(θ) - 4ε·cos(2θ), d²f/dr² = 2
def classify(theta, r):
    d2t = -np.cos(theta) - 4*eps*np.cos(2*theta)
    d2r = 2.0
    det = d2t * d2r
    if det > 0 and d2t > 0:
        return 'min'
    elif det > 0 and d2t < 0:
        return 'max'
    else:
        return 'saddle'

# The 4 angular critical points with r=0
angles = [0.0, np.pi, 2.255, -2.255]
critical_points = []
for a in angles:
    label = classify(a, 0.0)
    fval = morse_surface(a, 0.0)
    print(f"θ={a:.3f}, r=0.0, f={fval:.3f}, d²θ={classify(a,0.0)}, {label}")
    critical_points.append((a, 0.0, label, fval))

# --- Grid for rendering ---
n_theta = 120
n_r = 80
thetas = np.linspace(-np.pi, np.pi, n_theta)
rs = np.linspace(0, 0.95, n_r)
T, R = np.meshgrid(thetas, rs)
F = morse_surface(T, R)

# --- Plotting ---
fig = plt.figure(figsize=(14, 9), facecolor='#1a1a1a')
gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3,
              left=0.05, right=0.95, bottom=0.05, top=0.92)

# Panel 1: 3D surface
ax1 = fig.add_subplot(gs[0, :], projection='3d')
surf = ax1.plot_surface(T, R, F, cmap='viridis', alpha=0.3,
                       shade=True, antialiased=True)

# Panel 2: 2D flow lines
ax2 = fig.add_subplot(gs[1, 0])

n_flows = 100
theta_starts = np.linspace(-np.pi, np.pi, n_flows, endpoint=False)
r_starts = np.full(n_flows, 0.85)
colors_flow = plt.cm.coolwarm(np.linspace(0.1, 0.9, n_flows))

for i, (st, sr) in enumerate(zip(theta_starts, r_starts)):
    tt, rr = trace_flow(st, sr, dt=0.02, max_steps=500)
    if len(tt) > 10:
        ax2.plot(tt, rr, color=colors_flow[i], alpha=0.25, linewidth=0.5)

# Mark critical points
for tp, r, label, fval in critical_points:
    color = {'min': '#4488ff', 'max': '#ff4444', 'saddle': '#ffaa44'}[label]
    marker = {'min': 'o', 'max': '^', 'saddle': 's'}[label]
    ax2.plot(tp, r, marker=marker, color=color, markersize=9,
             markeredgecolor='white', markeredgewidth=0.5)

ax2.set_xlabel('θ')
ax2.set_ylabel('r')
ax2.set_title('Gradient flow on (θ, r) plane')
ax2.set_facecolor('#1a1a1a')
ax2.tick_params(colors='white')
for spine in ax2.spines.values():
    spine.set_color('white')

# 3D flow lines on surface
for i, (st, sr) in enumerate(zip(theta_starts[::3], r_starts)):
    tt, rr = trace_flow(st, sr, dt=0.02, max_steps=500)
    if len(tt) > 10:
        ff = morse_surface(tt, rr)
        ax1.plot(tt, rr, ff, color=colors_flow[i], alpha=0.4, linewidth=0.6)

ax1.set_title('Morse landscape f(θ) + r² + flow lines', color='white')
ax1.set_facecolor('#1a1a1a')
ax1.tick_params(colors='white')

# Panel 3: Attraction basins / Morse-Smale cells
ax3 = fig.add_subplot(gs[1, 1:])
ax3.set_facecolor('#1a1a1a')

n_samp = 120
sample_thetas = np.linspace(-np.pi, np.pi, n_samp)
sample_rs = np.linspace(0.02, 0.95, n_samp)
Y, X = np.meshgrid(sample_rs, sample_thetas)

# Track each grid point to its flow end and classify
basin = np.zeros_like(Y)
for i in range(n_samp):
    for j in range(n_samp):
        t, r = sample_thetas[j], sample_rs[i]
        tt, rr = trace_flow(t, r, dt=0.02, max_steps=400)
        if len(rr) > 10:
            end_t = tt[-1]
            # Assign to nearest minimum
            dist_to_2255 = abs(((end_t - 2.255 + np.pi) % (2*np.pi)) - np.pi)
            dist_to_m2255 = abs(((end_t - (-2.255) + np.pi) % (2*np.pi)) - np.pi)
            basin[i, j] = 1 if dist_to_2255 < dist_to_m2255 else -1

im = ax3.pcolormesh(X, Y, basin, cmap='bwr', shading='auto', vmin=-1.5, vmax=1.5)

# Overlay flow
for i, (st, sr) in enumerate(zip(theta_starts[::5], r_starts)):
    tt, rr = trace_flow(st, sr, dt=0.02, max_steps=500)
    if len(tt) > 10:
        ax3.plot(tt, rr, color='white', alpha=0.3, linewidth=0.3)

# Critical points
for tp, r, label, fval in critical_points:
    color = {'min': '#4488ff', 'max': '#ff4444', 'saddle': '#ffaa44'}[label]
    marker = {'min': 'o', 'max': '^', 'saddle': 's'}[label]
    ax3.plot(tp, r, marker=marker, color=color, markersize=9,
             markeredgecolor='white', markeredgewidth=0.5)

ax3.set_xlabel('θ')
ax3.set_ylabel('r')
ax3.set_title('Attraction basins (blue = θ>0 minimum, red = θ<0 minimum)')
ax3.set_facecolor('#1a1a1a')
ax3.tick_params(colors='white')
for spine in ax3.spines.values():
    spine.set_color('white')
cbar = plt.colorbar(im, ax=ax3, fraction=0.046)
cbar.set_ticklabels(['θ<0 min', 'saddle separatrix', 'θ>0 min'])

fig.suptitle('Morse flow: gradient trajectories + cell decomposition',
             color='white', fontsize=14, fontweight='bold')

plt.savefig('/home/sprite/slop-salon-gert/morse-flow-01.png', dpi=150,
            bbox_inches='tight', facecolor='#1a1a1a')
plt.close()
print("Saved morse-flow-01.png")
