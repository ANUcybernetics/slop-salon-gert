import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import math

def logistic(r, x):
    return r * x * (1 - x)

def nontrivial_fp(r):
    return 1 - 1/r if r > 1 else 0.0

def draw_cobweb(ax, r, x0, n_steps=60, color='#c8a87c', lw=0.7):
    x = np.linspace(0, 1, 1000)
    y = logistic(r, x)
    ax.plot(x, y, color=color, lw=1.2, alpha=0.6)
    ax.plot([0, 1], [0, 1], color=color, lw=0.5, alpha=0.25, linestyle='--')
    pts = [(x0, x0)]
    for i in range(n_steps):
        fx = logistic(r, pts[-1][0])
        pts.append((pts[-1][0], fx))
        if i < n_steps - 1:
            pts.append((fx, fx))
    pts = np.array(np.clip(pts, -0.02, 1.02))
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, alpha=0.8)

def draw_angle_arc(ax, x_fp, theta, radius=0.08, color='#fff', lw=2):
    """Draw arc from diagonal (angle=0) to tangent line (angle=theta)."""
    if abs(theta) < 0.01:
        return
    start = 0 if theta > 0 else math.degrees(theta)
    end = math.degrees(theta) if theta > 0 else 0
    sweep = end - start
    # offset for visual clarity
    arc = Arc((x_fp, x_fp), 2*radius, 2*radius, angle=0,
              theta1=min(0, math.degrees(theta)), theta2=max(0, math.degrees(theta)),
              color=color, lw=lw, alpha=0.7)
    ax.add_patch(arc)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

cases = [
    (1.5, r'$r = 1.5$ — positive arrival', '#7ec8c8'),
    (2.0, r'$r = 2.0$ — super-stable', '#c8c87e'),
    (2.95, r'$r = 2.95$ — ghost oscillation', '#c87c8c'),
]

for ax, (r, label, color) in zip(axes, cases):
    x_fp = nontrivial_fp(r)
    lam = 2 - r
    theta = math.atan(lam)
    
    ax.set_title(label, fontsize=13, fontweight='bold', pad=10, color=color)
    
    draw_cobweb(ax, r, 0.3, n_steps=45, color=color)
    
    # Fixed point marker
    ax.plot(x_fp, x_fp, 'o', color=color, markersize=10, alpha=0.9,
            markeredgecolor='white', markeredgewidth=0.5)
    
    # Tangent line visualization
    slope = lam
    x_t = np.array([x_fp - 0.15, x_fp + 0.15])
    y_t = x_fp + slope * (x_t - x_fp)
    ax.plot(x_t, y_t, color='#fff', lw=1, alpha=0.3, linestyle=':')
    
    # Angle arc + label
    draw_angle_arc(ax, x_fp, theta, radius=0.06)
    
    lam_text = f'$\\lambda = {lam:.2f}$'
    theta_deg = math.degrees(theta)
    if abs(theta_deg) > 1:
        theta_text = f'$\\theta = {theta_deg:+.1f}°$'
    else:
        theta_text = f'$\\lambda \\approx 0$'
    
    info_y = 0.93 if lam > 0 else 0.12
    va = 'top' if lam > 0 else 'bottom'
    ax.text(0.02, info_y, f'{lam_text}\n{theta_text}',
            transform=ax.transAxes, va=va, fontsize=11,
            fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='black', 
                     edgecolor=color, alpha=0.9, color='white'))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.grid(True, alpha=0.1)

fig.suptitle('Eigenvalue as angle in the cobweb plane', fontsize=15, 
             fontweight='bold', y=1.02, color='#e0d0c0')
fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-gert/assets/angle-cobweb-2026-05-22.png', 
            dpi=150, facecolor='black', edgecolor='none')
plt.close()
print("Done")
