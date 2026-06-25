"""
Capstone: cobweb on contour field of hesitation.

Synthesizes the thread's core moves.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = 3.5
x = np.linspace(0.01, 0.99, 500)

# Cobweb trajectory
cobweb_h, cobweb_v = [], []
pt = 0.1
for _ in range(400):
    pt_next = r * pt * (1 - pt)
    cobweb_h.append((pt, pt_next))
    cobweb_v.append((pt_next, pt_next))
    pt = pt_next

# Contour: |f'(x)| = |r(1-2x)| — hesitation field
Yg, Xg = np.meshgrid(x, x)
Z = np.abs(r * (1 - 2 * Xg))

fig, ax = plt.subplots(1, 1, figsize=(8, 8), facecolor='black')
ax.set_facecolor('black')

cf = ax.contourf(Xg, Yg, Z, levels=50, cmap='magma', alpha=0.7)

# Cobweb
for h in cobweb_h:
    alpha = min(1.0, abs(h[1] - h[0]) * 6)
    ax.plot([h[0], h[1]], [h[0], h[0]], 'aqua', linewidth=0.4, alpha=alpha)
for v in cobweb_v:
    alpha = min(1.0, abs(v[1] - v[0]) * 6)
    ax.plot([v[0], v[0]], [v[0], v[1]], 'gold', linewidth=0.4, alpha=alpha)

ax.plot(x, x, 'white', linewidth=0.3, alpha=0.2)
ax.plot(x, r * x * (1 - x), 'white', linewidth=0.7, alpha=0.4)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
plt.savefig('assets/capstone-2026-06-25.png', dpi=200, facecolor='black', edgecolor='none',
            bbox_inches='tight')
plt.close()
print("Done")
