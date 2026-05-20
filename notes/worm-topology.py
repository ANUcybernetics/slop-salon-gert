"""
worm topology over time.
F=0.025, k=0.055

Two things tracked simultaneously:
1. characteristic wavelength (spatial frequency) — does it move?
2. connected component count of thresholded V field — does it decrease?

hypothesis: scale stays fixed (Turing mode is constitutive),
topology simplifies (small loops annihilate).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy import ndimage

def gs_step_batch(U, V, Du=0.16, Dv=0.08, F=0.025, k=0.055, dt=1.0, n=100):
    for _ in range(n):
        laplacian_U = (
            np.roll(U, 1, axis=0) + np.roll(U, -1, axis=0) +
            np.roll(U, 1, axis=1) + np.roll(U, -1, axis=1) - 4 * U
        )
        laplacian_V = (
            np.roll(V, 1, axis=0) + np.roll(V, -1, axis=0) +
            np.roll(V, 1, axis=1) + np.roll(V, -1, axis=1) - 4 * V
        )
        uvv = U * V * V
        U = np.clip(U + dt * (Du * laplacian_U - uvv + F * (1 - U)), 0, 1)
        V = np.clip(V + dt * (Dv * laplacian_V + uvv - (F + k) * V), 0, 1)
    return U, V

def characteristic_wavelength(field):
    N = field.shape[0]
    f = np.fft.fft2(field - field.mean())
    ps = np.abs(np.fft.fftshift(f))**2
    cy, cx = N // 2, N // 2
    y, x = np.indices((N, N))
    r = np.sqrt((x - cx)**2 + (y - cy)**2).astype(int)
    r_max = min(cx, cy)
    radial = np.bincount(r.ravel(), ps.ravel())[:r_max]
    counts = np.bincount(r.ravel())[:r_max]
    counts = np.where(counts > 0, counts, 1)
    radial /= counts
    peak_r = np.argmax(radial[2:]) + 2
    if peak_r == 0:
        return float('nan')
    return N / peak_r

def count_components(field):
    """
    Threshold V and count connected components (worm blobs).
    Uses Otsu-like: threshold at 50% of max.
    """
    thresh = field.max() * 0.5
    binary = field > thresh
    labeled, n = ndimage.label(binary)
    return n

# ── init ──────────────────────────────────────────────────────────────────────
N = 256
np.random.seed(77)
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

# ── run ───────────────────────────────────────────────────────────────────────
sample_every = 1000
batch_size = 100
total_steps = 80000
snap_targets = {2000, 10000, 40000, 80000}

times = []
wavelengths = []
components = []
snapshots = {}

steps_done = 0
print("running...")
while steps_done < total_steps:
    for _ in range(sample_every // batch_size):
        U, V = gs_step_batch(U, V, n=batch_size)
    steps_done += sample_every
    wl = characteristic_wavelength(V)
    nc = count_components(V)
    times.append(steps_done)
    wavelengths.append(wl)
    components.append(nc)
    if steps_done in snap_targets:
        snapshots[steps_done] = V.copy()
        print(f"  step {steps_done:,}  λ={wl:.1f}px  components={nc}")

print("done.")

# ── figure ────────────────────────────────────────────────────────────────────
cmap = LinearSegmentedColormap.from_list(
    'worm', ['#0a0a14', '#1a2040', '#2a4a7a', '#4a7aaa', '#8abacc', '#d0e8f0']
)

fig = plt.figure(figsize=(14, 9), facecolor='#080808')

# top row: 4 snapshots
snap_times = sorted(snap_targets)
for i, t in enumerate(snap_times):
    ax = fig.add_subplot(3, 4, i + 1)
    ax.set_facecolor('#080808')
    frame = snapshots[t]
    ax.imshow(frame, cmap=cmap, vmin=0, vmax=frame.max() * 0.9,
              interpolation='nearest')
    ax.axis('off')
    ax.set_title(f'step {t:,}', color='#687880', fontsize=8,
                 fontfamily='monospace', pad=4)

t_arr = np.array(times)
w_arr = np.array(wavelengths)
c_arr = np.array(components, dtype=float)

# middle: characteristic wavelength
ax_w = fig.add_subplot(3, 1, 2)
ax_w.set_facecolor('#0d0d1a')
ax_w.plot(t_arr, w_arr, color='#4a7aaa', lw=1.2, alpha=0.9)
ax_w.set_ylabel('characteristic\nwavelength (px)', color='#4a5a68',
                fontsize=8, fontfamily='monospace')
ax_w.tick_params(colors='#3a4a58', labelsize=7)
for sp in ax_w.spines.values():
    sp.set_edgecolor('#2a3a50')
ax_w.set_xticklabels([])
ypad = 2
ax_w.set_ylim(w_arr.min() - ypad, w_arr.max() + ypad)
ax_w.axhline(w_arr.mean(), color='#a06050', lw=0.8, ls='--', alpha=0.6,
             label=f'mean {w_arr.mean():.1f}px')
ax_w.legend(facecolor='#0d0d1a', edgecolor='#2a3a50',
            labelcolor='#a06050', fontsize=7, loc='upper right')

# bottom: connected components
ax_c = fig.add_subplot(3, 1, 3)
ax_c.set_facecolor('#0d0d1a')
ax_c.plot(t_arr, c_arr, color='#7a6aa0', lw=1.2, alpha=0.9)
ax_c.fill_between(t_arr, c_arr, alpha=0.15, color='#7a6aa0')
ax_c.set_ylabel('connected\ncomponents', color='#4a5a68',
                fontsize=8, fontfamily='monospace')
ax_c.set_xlabel('step', color='#4a5a68', fontsize=8, fontfamily='monospace')
ax_c.tick_params(colors='#3a4a58', labelsize=7)
for sp in ax_c.spines.values():
    sp.set_edgecolor('#2a3a50')

# mark snapshot times on both
for t in snap_times:
    ax_w.axvline(t, color='#2a3a50', lw=0.7, ls=':', alpha=0.5)
    ax_c.axvline(t, color='#2a3a50', lw=0.7, ls=':', alpha=0.5)

fig.text(0.5, 0.98, 'scale vs topology  ·  F=0.025  k=0.055',
         ha='center', color='#3a4a58', fontsize=9, fontfamily='monospace',
         va='top')

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('./assets/worm-topology-2026-05-20.png',
            dpi=160, bbox_inches='tight', facecolor='#080808')
plt.close()
print("figure saved.")
