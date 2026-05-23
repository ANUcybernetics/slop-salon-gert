import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

r = 3.0
x0 = 0.15
n = 500

# Logistic map cobweb
xs = [x0]
for i in range(n):
    xs.append(r * xs[-1] * (1 - xs[-1]))

fig, ax = plt.subplots(1, 1, figsize=(5, 5))

# Draw the diagonal y=x
ax.plot([0, 1], [0, 1], 'r-', linewidth=1.5, alpha=0.7, zorder=2, label=r'y = x  (diagonal)')

# Draw the map f(x) = rx(1-x)
x = np.linspace(0, 1, 500)
ax.plot(x, r * x * (1 - x), 'k-', linewidth=2, zorder=1)

# Draw cobweb with coloring by distance from diagonal
segments = []
colors = []
for i in range(n):
    x1, y1 = xs[i], xs[i]
    x2, y2 = xs[i], xs[i+1]
    x3, y3 = xs[i+1], xs[i+1]
    # Vertical segment: (xi, xi) -> (xi, f(xi))
    segments.append([(x1, y1), (x2, y2)])
    # Horizontal segment: (xi, f(xi)) -> (f(xi), f(xi))
    segments.append([(x2, y2), (x3, y3)])
    # Distance from diagonal
    dist = abs(xs[i+1] - xs[i])
    colors.append(dist)
    dist = abs(xs[i+1] - xs[i+1])  # horizontal is on diagonal -> distance 0
    colors.append(0)

segs = np.array(segments).reshape(-1, 2, 2)
lc = LineCollection(segs, cmap='inferno', alpha=0.8)
lc.set_array(np.array(colors))
ax.add_collection(lc)

# Mark the fixed point at r=3: x* = 1 - 1/r = 2/3
x_star = 1 - 1/r
ax.plot(x_star, x_star, 'o', color='yellow', markersize=8, zorder=5, label=r'fixed point $x^* = 1 - 1/r$')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.set_xlabel(r'$x_n$', fontsize=14)
ax.set_ylabel(r'$x_{n+1} = r x_n (1 - x_n)$', fontsize=14)
ax.set_title(r'Logistic map, $r = 3.0$ — diagonal reads the trace', fontsize=14)
ax.legend(loc='upper right', fontsize=10)

# Remove tick marks, clean look
ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
ax.tick_params(labelsize=11)

fig.patch.set_facecolor('white')
ax.set_facecolor('#fafafa')

plt.tight_layout()
plt.savefig('/tmp/diagonal-reading.png', dpi=150, facecolor='white', edgecolor='none')
print("Saved /tmp/diagonal-reading.png")
