"""
coarsening length scale over time.
F=0.025, k=0.055 — worm region.

measure: peak wavelength from radially-averaged power spectrum of V.
run to 60,000 steps, sample every 2,000.
does the length scale grow as a power law? does it plateau?
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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
    """
    radial average of power spectrum; return wavelength at peak.
    """
    N = field.shape[0]
    f = np.fft.fft2(field - field.mean())
    ps = np.abs(np.fft.fftshift(f))**2

    # radial average
    cy, cx = N // 2, N // 2
    y, x = np.indices((N, N))
    r = np.sqrt((x - cx)**2 + (y - cy)**2).astype(int)
    r_max = min(cx, cy)
    radial = np.bincount(r.ravel(), ps.ravel())[:r_max]
    counts = np.bincount(r.ravel())[:r_max]
    counts = np.where(counts > 0, counts, 1)
    radial /= counts

    # skip DC (r=0)
    peak_r = np.argmax(radial[2:]) + 2
    if peak_r == 0:
        return float('nan')
    wavelength = N / peak_r
    return wavelength

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

# ── run and measure ───────────────────────────────────────────────────────────
sample_every = 500   # measure every 500 steps
batch_size = 100     # inner loop size
total_steps = 60000

times = []
wavelengths = []
snapshots = {}       # save frames at 2k, 10k, 30k, 60k
snap_targets = {2000, 10000, 30000, 60000}

steps_done = 0
print("running...")
while steps_done < total_steps:
    batches = sample_every // batch_size
    for _ in range(batches):
        U, V = gs_step_batch(U, V, n=batch_size)
    steps_done += sample_every

    wl = characteristic_wavelength(V)
    times.append(steps_done)
    wavelengths.append(wl)

    if steps_done in snap_targets:
        snapshots[steps_done] = V.copy()
        print(f"  step {steps_done:,}  λ={wl:.1f}px")

print("done.")

# ── figure ────────────────────────────────────────────────────────────────────
cmap = LinearSegmentedColormap.from_list(
    'worm', ['#0a0a14', '#1a2040', '#2a4a7a', '#4a7aaa', '#8abacc', '#d0e8f0']
)

fig = plt.figure(figsize=(14, 8), facecolor='#080808')

# top: 4 snapshots
snap_times = [2000, 10000, 30000, 60000]
for i, t in enumerate(snap_times):
    ax = fig.add_subplot(2, 4, i + 1)
    ax.set_facecolor('#080808')
    frame = snapshots[t]
    ax.imshow(frame, cmap=cmap, vmin=0, vmax=frame.max() * 0.9,
              interpolation='nearest')
    ax.axis('off')
    ax.set_title(f'step {t:,}', color='#687880', fontsize=9,
                 fontfamily='monospace', pad=5)

# bottom: length scale over time
ax_l = fig.add_subplot(2, 1, 2)
ax_l.set_facecolor('#0d0d1a')

t_arr = np.array(times)
w_arr = np.array(wavelengths)

ax_l.plot(t_arr, w_arr, color='#4a7aaa', lw=1.2, alpha=0.9)
ax_l.scatter(t_arr, w_arr, color='#8abacc', s=4, alpha=0.6, zorder=3)

# mark snapshot times
for t in snap_times:
    ax_l.axvline(t, color='#2a3a50', lw=0.8, ls='--', alpha=0.6)

ax_l.set_xlabel('step', color='#4a5a68', fontsize=9, fontfamily='monospace')
ax_l.set_ylabel('characteristic wavelength (px)', color='#4a5a68',
                fontsize=9, fontfamily='monospace')
ax_l.tick_params(colors='#3a4a58', labelsize=8)
for spine in ax_l.spines.values():
    spine.set_edgecolor('#2a3a50')
ax_l.xaxis.label.set_color('#4a5a68')
ax_l.yaxis.label.set_color('#4a5a68')

# log-log fit for power law
valid = (t_arr > 3000) & np.isfinite(w_arr)
if valid.sum() > 5:
    log_t = np.log(t_arr[valid])
    log_w = np.log(w_arr[valid])
    slope, intercept = np.polyfit(log_t, log_w, 1)
    fit_t = t_arr[valid]
    fit_w = np.exp(intercept) * fit_t**slope
    ax_l.plot(fit_t, fit_w, color='#a06050', lw=1.0, ls='--', alpha=0.8,
              label=f'λ ∝ t^{slope:.2f}')
    ax_l.legend(facecolor='#0d0d1a', edgecolor='#2a3a50',
                labelcolor='#a06050', fontsize=8)

fig.text(0.5, 0.97, 'worm coarsening  F=0.025  k=0.055',
         ha='center', color='#3a4a58', fontsize=9, fontfamily='monospace')
fig.text(0.5, 0.5, 'characteristic wavelength = peak of radial power spectrum',
         ha='center', color='#2a3540', fontsize=8, fontfamily='monospace')

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('./assets/worm-coarsening-2026-05-20.png',
            dpi=160, bbox_inches='tight', facecolor='#080808')
plt.close()
print("figure saved.")
