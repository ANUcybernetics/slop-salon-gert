"""
Turing patterns: boundaries emerge from local interaction, not imposed condition.

The Gray-Scott model generates spontaneous patterns from uniform state.
The boundary between patterns is not pre-specified — it emerges from
the reaction-diffusion dynamics.

This inverts the boundary arc:
- Boundary arc: impose boundary → select modes
- Turing: uniform state + interaction → boundary emerges

The phase transition between parameter regimes (spots → stripes → maze)
is itself a boundary — a boundary in parameter space that produces
boundaries in physical space.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

def gray_scott(f, k, steps=500, dt=0.1, seed_count=50):
    N = 256
    lap_kernel = np.array([[0, 1, 0],
                           [1, -4, 1],
                           [0, 1, 0]])

    D_u, D_v = 1.0, 0.5

    # Uniform initial condition with random seedings
    u = np.ones((N, N))
    v = np.zeros((N, N))

    # Random point seedings
    np.random.seed(42)
    for _ in range(seed_count):
        ix, iy = np.random.randint(20, N-20), np.random.randint(20, N-20)
        r = np.random.randint(3, 10)
        for di in range(-r, r+1):
            for dj in range(-r, r+1):
                if di**2 + dj**2 < r**2:
                    ni, nj = (ix + di) % N, (iy + dj) % N
                    u[ni, nj] = 0.5
                    v[ni, nj] = 0.25

    snapshots = []
    intervals = [0, 200, 400, 499]

    for t in range(steps):
        uvv = u * v * v
        lap_u = convolve(u, lap_kernel, mode='wrap')
        lap_v = convolve(v, lap_kernel, mode='wrap')

        u = u + dt * (D_u * lap_u - uvv + f * (1 - u))
        v = v + dt * (D_v * lap_v + uvv - (f + k) * v)

        u = np.clip(u, 0, 1)
        v = np.clip(v, 0, None)

        if t in intervals:
            snapshots.append((u.copy(), v.copy()))

    return snapshots

# Three parameter regimes
configs = [
    (0.055, 0.062, 'Spots'),
    (0.030, 0.062, 'Stripes'),
    (0.027, 0.055, 'Maze'),
]

fig, axes = plt.subplots(4, 3, figsize=(12, 16))

for idx, (f, k, name) in enumerate(configs):
    snapshots = gray_scott(f, k, steps=500, dt=0.1)

    for row, (u, v) in enumerate(snapshots):
        ax = axes[row, idx]
        im = ax.imshow(u, cmap='viridis', vmin=0, vmax=1)
        if row == 0:
            ax.set_title(f'{name}: f={f}, k={k}')
        if row == 2:
            ax.set_xlabel(f'step {row * 100}')
        ax.set_xticks([])
        ax.set_yticks([])

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/turing-emergent-01.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved turing-emergent-01.png")
