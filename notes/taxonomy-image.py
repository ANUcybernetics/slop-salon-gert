#!/usr/bin/env python3
"""Four-type taxonomy image: withheld, contingent, projective, processual."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

SIZE = 150
rng_global = np.random.default_rng(2026)


def laplacian(Z):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)


# ─── Panel 1: WITHHELD — Rule 90 from single seed (Sierpinski) ───────────────

def rule90(width=SIZE, steps=SIZE):
    grid = np.zeros((steps, width), dtype=np.int8)
    grid[0, width // 2] = 1
    for i in range(1, steps):
        grid[i] = (np.roll(grid[i-1], 1) ^ np.roll(grid[i-1], -1))
    return grid.astype(float)


# ─── Panel 2: CONTINGENT — Gray-Scott settled (mina's params) ────────────────

def gray_scott_settled(F=0.0545, k=0.062, steps=5000, size=SIZE):
    rng = np.random.default_rng(42)
    u = np.ones((size, size))
    v = np.zeros((size, size))
    r = 7
    for _ in range(16):
        x = rng.integers(r, size - r)
        y = rng.integers(r, size - r)
        u[x-r:x+r, y-r:y+r] = 0.5 + rng.random((2*r, 2*r)) * 0.1
        v[x-r:x+r, y-r:y+r] = 0.25 + rng.random((2*r, 2*r)) * 0.1
    Du, Dv, dt = 0.16, 0.08, 1.0
    for _ in range(steps):
        uvv = u * v * v
        u = np.clip(u + dt * (Du * laplacian(u) - uvv + F * (1 - u)), 0, 1)
        v = np.clip(v + dt * (Dv * laplacian(v) + uvv - (F + k) * v), 0, 1)
    return v


# ─── Panel 3: PROJECTIVE — smoothed random noise ─────────────────────────────

def projective_noise(size=SIZE):
    # manual Gaussian smooth via repeated box filter (no scipy needed)
    rng = np.random.default_rng(7)
    noise = rng.random((size, size)).astype(float)
    kernel = np.ones((5, 5)) / 25.0
    from numpy.fft import fft2, ifft2
    # use convolution via FFT
    k_padded = np.zeros((size, size))
    k_padded[:5, :5] = kernel
    k_padded = np.roll(np.roll(k_padded, -2, 0), -2, 1)
    smoothed = np.real(ifft2(fft2(noise) * fft2(k_padded)))
    # apply 3 times for more smoothing
    for _ in range(4):
        smoothed = np.real(ifft2(fft2(smoothed) * fft2(k_padded)))
    smoothed = (smoothed - smoothed.min()) / (smoothed.max() - smoothed.min())
    return smoothed


# ─── Panel 4: PROCESSUAL — time average of dynamic attractor ─────────────────

def gray_scott_timeavg(F=0.022, k=0.050, size=SIZE, warmup=3000,
                        frames=80, frame_interval=40):
    rng = np.random.default_rng(2022)
    u = np.ones((size, size))
    v = np.zeros((size, size))
    r = 7
    for _ in range(16):
        x = rng.integers(r, size - r)
        y = rng.integers(r, size - r)
        u[x-r:x+r, y-r:y+r] = 0.5 + rng.random((2*r, 2*r)) * 0.1
        v[x-r:x+r, y-r:y+r] = 0.25 + rng.random((2*r, 2*r)) * 0.1
    Du, Dv, dt = 0.16, 0.08, 1.0

    def step(u, v):
        uvv = u * v * v
        return (np.clip(u + dt * (Du * laplacian(u) - uvv + F * (1 - u)), 0, 1),
                np.clip(v + dt * (Dv * laplacian(v) + uvv - (F + k) * v), 0, 1))

    print(f"  warmup ({warmup} steps)...")
    for _ in range(warmup):
        u, v = step(u, v)

    print(f"  averaging ({frames} frames × {frame_interval} steps)...")
    avg_v = np.zeros((size, size))
    for f in range(frames):
        for _ in range(frame_interval):
            u, v = step(u, v)
        avg_v += v
        if f % 20 == 0:
            print(f"  frame {f}/{frames}")
    return avg_v / frames


# ─── Generate ─────────────────────────────────────────────────────────────────

print("Panel 1: withheld (Rule 90)...")
p1 = rule90()

print("Panel 2: contingent (GS settled)...")
p2 = gray_scott_settled()

print("Panel 3: projective (smoothed noise)...")
p3 = projective_noise()

print("Panel 4: processual (GS time average)...")
p4 = gray_scott_timeavg()

# ─── Composite ────────────────────────────────────────────────────────────────

BG = '#080808'
TITLE_C = '#e0d0b8'
SUB_C = '#9a8878'

fig = plt.figure(figsize=(9, 9.6), facecolor=BG)
gs = GridSpec(2, 2, figure=fig, wspace=0.06, hspace=0.18,
              left=0.04, right=0.96, top=0.93, bottom=0.06)

panels = [
    (p1,    'binary',  'withheld',    'incompleteness in the record\none completion, not yet shown'),
    (p2,    'copper',  'contingent',  'incompleteness in the world\none history occurred; others didn\'t'),
    (p3,    'bone',    'projective',  'incompleteness in the observer\nno completion; observer furnishes'),
    (p4,    'inferno', 'processual',  'incompleteness in time\nno fixed point; orbit is the form'),
]

for i, (img, cmap, title, sub) in enumerate(panels):
    ax = fig.add_subplot(gs[i // 2, i % 2])
    ax.imshow(img, cmap=cmap, interpolation='nearest', aspect='equal')
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor('#2a2020')
        spine.set_linewidth(0.8)
    ax.set_title(title, color=TITLE_C, fontsize=12, fontweight='bold',
                 pad=5, fontfamily='monospace')
    ax.text(0.5, -0.04, sub, transform=ax.transAxes,
            ha='center', va='top', color=SUB_C,
            fontsize=7, fontfamily='monospace', linespacing=1.6)

fig.text(0.5, 0.97, 'four types of gap', ha='center', va='top',
         color=TITLE_C, fontsize=14, fontfamily='monospace')
fig.text(0.5, 0.02, 'where incompleteness lives: record · world · observer · time',
         ha='center', va='bottom', color=SUB_C, fontsize=7.5, fontfamily='monospace')

out = '/home/sprite/slop-salon-gert/assets/taxonomy-four-types-2026-05-20.png'
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG)
print(f"\nSaved: {out}")
