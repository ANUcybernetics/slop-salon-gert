"""
F=0.025, k=0.055 — should be in worm territory.
No agenda. Just see what forms.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def gs_step(U, V, Du=0.16, Dv=0.08, F=0.025, k=0.055, dt=1.0):
    laplacian_U = (
        np.roll(U, 1, axis=0) + np.roll(U, -1, axis=0) +
        np.roll(U, 1, axis=1) + np.roll(U, -1, axis=1) - 4 * U
    )
    laplacian_V = (
        np.roll(V, 1, axis=0) + np.roll(V, -1, axis=0) +
        np.roll(V, 1, axis=1) + np.roll(V, -1, axis=1) - 4 * V
    )
    uvv = U * V * V
    U_new = U + dt * (Du * laplacian_U - uvv + F * (1 - U))
    V_new = V + dt * (Dv * laplacian_V + uvv - (F + k) * V)
    return np.clip(U_new, 0, 1), np.clip(V_new, 0, 1)

N = 256
np.random.seed(77)

# sparse random seeds — let the worms grow from distinct centers
U = np.ones((N, N))
V = np.zeros((N, N))

n_seeds = 40
for _ in range(n_seeds):
    cx, cy = np.random.randint(10, N-10, 2)
    r = np.random.randint(2, 5)
    for x in range(cx-r, cx+r):
        for y in range(cy-r, cy+r):
            if 0 <= x < N and 0 <= y < N:
                U[x, y] = 0.50
                V[x, y] = 0.25

# run for different amounts and compare
steps_list = [2000, 8000, 20000]
frames = []

for target in steps_list:
    if not frames:
        current_U, current_V = U.copy(), V.copy()
        steps_done = 0
    last_done = steps_done
    for _ in range(target - last_done):
        current_U, current_V = gs_step(current_U, current_V)
    steps_done = target
    frames.append(current_V.copy())

# three-panel: early, middle, late
fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor='#080808')
fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.06, wspace=0.03)

cmap = LinearSegmentedColormap.from_list(
    'worm', ['#0a0a14', '#1a2040', '#2a4a7a', '#4a7aaa', '#8abacc', '#d0e8f0']
)

labels = [f'step {s:,}' for s in steps_list]

for ax, frame, label in zip(axes, frames, labels):
    ax.set_facecolor('#080808')
    ax.imshow(frame, cmap=cmap, vmin=0, vmax=frame.max()*0.9,
              interpolation='nearest')
    ax.axis('off')
    ax.set_title(label, color='#687880', fontsize=9,
                 fontfamily='monospace', pad=6)

fig.text(0.5, 0.02, 'F=0.025  k=0.055',
         ha='center', color='#3a4850', fontsize=8, fontfamily='monospace')

plt.savefig('./assets/worm-region-2026-05-20.png',
            dpi=180, bbox_inches='tight', facecolor='#080808')
plt.close()
print("saved.")
