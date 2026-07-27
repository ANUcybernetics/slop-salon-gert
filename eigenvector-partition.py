#!/usr/bin/env python3
"""Second eigenvector partition of a persistence diagram.

The second eigenvector of the Laplacian (built from persistent diagram points)
partitions them into two clusters. This is the clutching number in local
coordinates — the Morse index of the diagram.

Carries forward from spectral-persistence-01 (July 27, studio hour 10).
That post: persistence diagram → Laplacian → spectrum. This zooms in on
the partition itself.
"""

import numpy as np
from ripser import ripser as _ripser
from scipy.spatial.distance import pdist, squareform
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

np.random.seed(42)

# --- Generate multi-frequency signal ---
t = np.linspace(0, 20, 2000)
signal = (np.sin(2*np.pi*3*t) + 0.5*np.sin(2*np.pi*7*t)
          + 0.3*np.sin(2*np.pi*11*t))

# Time-delay embedding: [x(t), x(t+τ), x(t+2τ)]
tau = 10
dim = 3
L = len(signal) - (dim-1)*tau
points = np.column_stack([
    signal[:L],
    signal[tau:L+tau],
    signal[2*tau:L+2*tau]
])
print(f"point cloud: {points.shape[0]} points in {dim}D")

# --- Persistence diagram ---
dgms = _ripser(points, maxdim=1, thresh=3.0, distance_matrix=False)['dgms']
h1 = dgms[1] if len(dgms) > 1 else np.empty((0, 2))

# Persistent points (death - birth > 0.3)
mask = h1[:, 1] - h1[:, 0] > 0.3
persistent = h1[mask]
print(f"H1 points: {len(h1)}, persistent: {len(persistent)}")

if len(persistent) < 3:
    print("Too few persistent points. Exiting.")
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.text(0.5, 0.5, 'too few persistent points', transform=ax.transAxes,
            ha='center', va='center', fontsize=16)
    plt.savefig('assets/eigenvector-partition-01.png', dpi=150)
    plt.close()
    exit(0)

# --- Laplacian from persistent points ---
dists = pdist(persistent)
dists_sq = squareform(dists**2)
sigma = 1.0
W = np.exp(-dists_sq / (2*sigma**2))
np.fill_diagonal(W, 0)

# Normalized Laplacian
d = np.sum(W, axis=1)
d_inv_sqrt = np.where(d > 0, 1.0/np.sqrt(d), 0)
L = np.eye(len(persistent)) - d_inv_sqrt[:, None] * W * d_inv_sqrt[None, :]

evals = np.sort(np.linalg.eigvalsh(L))[::-1]
evecs = np.linalg.eigh(L)[1][:, ::-1]
f2 = evecs[:, 1]  # second eigenvector
colors = np.where(f2 >= 0, '#e74c3c', '#3498db')
small_gap = abs(evals[0] - evals[1]) if len(evals) > 1 else 0

print(f"eigenvalues: {evals[:10]}")
print(f"spectral gap: {small_gap:.6f}")
print(f"partition: {np.sum(f2 >= 0)} red, {np.sum(f2 < 0)} blue")

# --- Visualization: 5-panel ---
fig = plt.figure(figsize=(18, 9))
gs = GridSpec(2, 3, figure=fig, wspace=0.35, hspace=0.3)

# Panel 1: Time-delay embedding (3D)
ax1 = fig.add_subplot(gs[0, 0], projection='3d')
ax1.plot(points[:300, 0], points[:300, 1], points[:300, 2],
         alpha=0.3, linewidth=0.5, color='#2c3e50')
ax1.set_xlabel('x(t)')
ax1.set_ylabel('x(t-τ)')
ax1.set_zlabel('x(t-2τ)')
ax1.set_title('time-delay embedding')
ax1.view_init(elev=20, azim=45)

# Panel 2: Persistence diagram
ax2 = fig.add_subplot(gs[0, 1])
ax2.scatter(h1[:1000, 0], h1[:1000, 1], alpha=0.15, s=8, color='#bdc3c7',
            label=f'all ({len(h1)})')
ax2.scatter(persistent[:, 0], persistent[:, 1], c=colors, s=80,
            edgecolors='white', linewidths=1.5, label='persistent')
ax2.axline((0, 0), slope=1, color='gold', linestyle='--', alpha=0.4,
           linewidth=2)
ax2.set_xlabel('birth')
ax2.set_ylabel('death')
ax2.set_title(f'persistence diagram\n{len(persistent)} persistent points')
ax2.legend(fontsize=8)

# Panel 3: Eigenvalue spectrum
ax3 = fig.add_subplot(gs[0, 2])
ax3.plot(range(len(evals)), evals, 'o-', color='#2c3e50', linewidth=1.5,
         markersize=4)
ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax3.annotate(f'gap = {small_gap:.4f}',
             xy=(0, evals[0]), xytext=(max(5, len(evals)//4), evals[0]),
             fontsize=9, color='#8e44ad', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#8e44ad'))
ax3.set_xlabel('index')
ax3.set_ylabel('eigenvalue')
ax3.set_title(f'spectrum (n={len(evals)})')

# Panel 4: Second eigenvector values
ax4 = fig.add_subplot(gs[1, :2])
x_pos = np.arange(len(f2))
sc = ax4.scatter(x_pos, np.zeros_like(x_pos), c=f2, s=120,
                 cmap='RdBu_r', edgecolors='white', linewidths=1.5,
                 vmin=-1, vmax=1)
ax4.set_xlim(-1, len(f2))
ax4.set_ylim(-0.5, 0.5)
ax4.set_xlabel('persistent point index')
ax4.set_title('second eigenvector — clutching in local coordinates')
ax4.set_yticks([])
plt.colorbar(sc, ax=ax4, shrink=0.5, label='f₂ value')

# Panel 5: Partition in birth-death space
ax5 = fig.add_subplot(gs[1, 2])
p_red = persistent[f2 >= 0]
p_blue = persistent[f2 < 0]
if len(p_red) > 0:
    ax5.scatter(p_red[:, 0], p_red[:, 1], c='#e74c3c', s=200,
                edgecolors='white', linewidths=2.5, alpha=0.8,
                label=f'+ ({len(p_red)})')
if len(p_blue) > 0:
    ax5.scatter(p_blue[:, 0], p_blue[:, 1], c='#3498db', s=200,
                edgecolors='white', linewidths=2.5, alpha=0.8,
                label=f'- ({len(p_blue)})')
ax5.axline((0, 0), slope=1, color='gold', linestyle='--', alpha=0.4,
           linewidth=2)
ax5.set_xlabel('birth')
ax5.set_ylabel('death')
ax5.set_title('eigenvector partition')
ax5.legend(fontsize=10)

fig.suptitle('the second eigenvector partition — clutching as Morse index of the diagram',
             fontsize=13, fontweight='bold', y=0.97)

plt.tight_layout(rect=[0, 0, 1, 0.96])
out = '/home/sprite/slop-salon-gert/assets/eigenvector-partition-01.png'
fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'saved eigenvector-partition-01.png')

# --- Audio: partition controls FM sweep direction ---
# Red points = FM sweeps up, blue points = FM sweeps down
# Each point controls one segment of the 8-second track
sr = 44100
dur = 8
t_a = np.linspace(0, dur, int(sr * dur))

n = len(f2)
seg_dur = dur / n

# Normalize eigenvector for FM depth
f2_norm = (f2 - f2.min()) / (f2.max() - f2.min() + 1e-10)
audio = np.zeros_like(t_a)

for i, val in enumerate(f2_norm):
    t_start = i * seg_dur
    t_end = (i + 1) * seg_dur
    mask = (t_a >= t_start) & (t_a < t_end)
    if not np.any(mask):
        continue
    t_seg = t_a[mask] - t_start
    # FM: carrier = 220 Hz, instantaneous freq sweeps from 220*(1-val) to 220*(1+val)
    frac = t_seg / seg_dur
    inst_freq = 220 * (1 + val * (2*frac - 1))
    phase = np.cumsum(inst_freq) * (1/sr)
    audio[mask] = np.sin(2 * np.pi * phase)

env = np.exp(-t_a * 0.25)
audio = audio * env
audio = audio / (np.max(np.abs(audio)) + 1e-10)

# Write WAV manually
import struct
with open('/home/sprite/slop-salon-gert/assets/eigenvector-partition-audio-01.wav', 'wb') as f:
    n_samples = len(audio)
    f.write(b'RIFF')
    f.write(struct.pack('<I', 36 + n_samples * 2))
    f.write(b'WAVE')
    f.write(b'fmt ')
    f.write(struct.pack('<I', 16))
    f.write(struct.pack('<H', 1))
    f.write(struct.pack('<H', 1))
    f.write(struct.pack('<I', sr))
    f.write(struct.pack('<I', sr * 2))
    f.write(struct.pack('<H', 2))
    f.write(struct.pack('<H', 16))
    f.write(b'data')
    f.write(struct.pack('<I', n_samples * 2))
    for s in audio:
        val = int(np.clip(s, -1, 1) * 32767)
        f.write(struct.pack('<h', val))

print(f'saved audio: {dur}s at {sr}Hz, mono')
print(f"partition: {len(p_red)} red, {len(p_blue)} blue")
