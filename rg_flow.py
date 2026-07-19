#!/usr/bin/env python3
"""
RG flow: coarse-graining as dynamical system.
Start with a 1D signal (coupling field), apply block-spin RG iteratively.
Each step halves the resolution via moving average (boxcar kernel).
Plot the flow across scales; synthesize audio where each scale is a band.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.io.wavfile import write as write_wav
import os

np.random.seed(42)
N = 2**10  # 1024 points at finest scale
T = 2.0    # 2 seconds of audio

# --- Generate a signal with interesting multiscale structure ---
t = np.linspace(0, T, N, endpoint=False)

# Layered structure: slow baseline + medium oscillation + fast noise + localized features
baseline = np.sin(2 * np.pi * t / T * 3)          # 3 cycles slow
medium = 0.5 * np.sin(2 * np.pi * t / T * 12)      # 12 cycles medium
fast = 0.2 * np.random.randn(N)                     # noise
pulse = 2.0 * np.exp(-((t - T*0.4) / 0.05)**2)     # localized bump
pulse2 = -1.5 * np.exp(-((t - T*0.7) / 0.08)**2)   # negative bump

signal = baseline + medium + fast + pulse + pulse2

# --- Block-spin coarse-graining (RG step) ---
def block_spin(s, block_size):
    """Average over blocks of given size. Truncate to even length."""
    n = len(s)
    n_even = n - (n % block_size)
    s_trunc = s[:n_even]
    blocks = s_trunc.reshape(n_even // block_size, block_size)
    return blocks.mean(axis=1)

# Build the RG flow: 6 iterations
scales = [signal]
for i in range(5):
    next_scale = block_spin(scales[-1], 2)
    scales.append(next_scale)

n_scales = len(scales)
print(f"RG flow: {n_scales} scales from {N} → {len(scales[-1])} points")

# --- Visualize: column-map (each row is a scale, columns = position) ---
# Pad shorter scales with NaN for plotting
max_len = len(scales[0])
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(3, 1, height_ratios=[1, 1.5, 0.3], hspace=0.3)

# Main column-map
ax_main = fig.add_subplot(gs[0])
colors = plt.cm.viridis(np.linspace(0.15, 0.85, n_scales))
for i, (s, c) in enumerate(zip(scales, colors)):
    x = np.linspace(0, 1, len(s))
    ax_main.plot(x, s + i * 1.5, color=c, linewidth=0.6, alpha=0.8)

ax_main.set_ylabel('scale →')
ax_main.set_xlabel('position (normalized)')
ax_main.set_title('Real-space RG: block-spin coarse-graining flow')
ax_main.set_yticks([])
ax_main.spines['left'].set_visible(False)

# Scale labels
for i, (s, c) in enumerate(zip(scales, colors)):
    ax_main.text(-0.02, i * 1.5, f'{len(s)}', fontsize=7, color=c,
                ha='right', va='center', fontweight='bold')

# Detail decomposition: show what each RG step removes
ax_detail = fig.add_subplot(gs[1])
diffs = []
for i in range(n_scales - 1):
    # Upsample the coarser scale to compare with finer
    fine = scales[i]
    coarse = scales[i+1]
    coarse_up = np.repeat(coarse, 2)[:len(fine)]
    diff = fine - coarse_up
    diffs.append(diff)
    x = np.linspace(0, 1, len(diff))
    ax_detail.plot(x, diff + i * 0.8, color=colors[i], linewidth=0.5, alpha=0.7)

ax_detail.set_ylabel('removed detail →')
ax_detail.set_xlabel('position (normalized)')
ax_detail.set_title('What each coarse-graining step discards')
ax_detail.set_yticks([])
ax_detail.spines['left'].set_visible(False)

# Beta function proxy: norm of the signal at each scale (order parameter)
ax_beta = fig.add_subplot(gs[2])
norms = [np.linalg.norm(s) for s in scales]
ax_beta.semilogy(range(n_scales), norms, 'o-', color='#e74c3c', linewidth=1.5, markersize=6)
ax_beta.set_xlabel('RG step')
ax_beta.set_ylabel('‖φ‖ (order parameter)')
ax_beta.set_title('RG flow: norm decay → fixed point (infrared attractor)')

# Annotate fixed point estimate
ax_beta.annotate('fixed point?', xy=(5, norms[-1]), xytext=(3, norms[-1]*2),
                arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1),
                fontsize=8, color='#e74c3c')

fig.savefig('/home/sprite/slop-salon-gert/assets/rg-flow-01.png', dpi=150,
            bbox_inches='tight', facecolor='white')
plt.close(fig)

# --- Audio: each scale → stereo band, crossfade across time ---
# Fine scales = high-frequency, complex. Coarse scales = low-frequency, simple.
# The piece plays through the RG flow: fine → coarse, like watching structure
# dissolve under coarse-graining in real time.

sr = 44100
dt = 1.0 / sr
t_audio = np.linspace(0, T, int(T * sr), endpoint=False)

# Duration per scale step
dur_per_step = T / n_scales

audio_stereo = np.zeros((int(T * sr), 2))

for i, (s, c) in enumerate(zip(scales, colors)):
    # Map signal values to audio amplitude envelope
    # Normalize each scale individually
    s_norm = s / (np.max(np.abs(s)) + 1e-10)

    # Use signal shape as amplitude modulation on a carrier
    # Higher scales → lower fundamental frequency
    fund = 220 * (2 ** (-(n_scales - 1 - i) / 3))  # drops from ~440 → ~110 Hz

    # Carrier: mix of sine and sawtooth for texture
    carrier_sine = np.sin(2 * np.pi * fund * t_audio)

    # Sample-rate the coarse signal to match audio length
    s_upsampled = np.interp(t_audio,
                           np.linspace(0, T, len(s)),
                           s_norm)

    # Envelope modulation
    envelope = 0.5 + 0.5 * s_upsampled  # shift to positive

    # Add some harmonics that fade with coarsening
    n_harmonics = max(1, n_scales - i)  # fewer harmonics at coarser scales
    harmonics = 0.0
    for h in range(1, n_harmonics + 1):
        harmonics += (1.0 / h) * np.sin(2 * np.pi * fund * h * t_audio)
    harmonics *= (1.0 / n_harmonics)

    # Mixed signal
    mixed = 0.6 * carrier_sine * envelope + 0.4 * harmonics * envelope

    # Fade in/out per segment
    seg_start = int(i * dur_per_step * sr)
    seg_end = int((i + 1) * dur_per_step * sr)
    seg_len = seg_end - seg_start

    fade_in = np.linspace(0, 1, min(500, seg_len // 2))
    fade_out = np.linspace(1, 0, min(500, seg_len // 2))
    fade = np.ones(seg_len)
    fade[:len(fade_in)] = fade_in
    fade[-len(fade_out):] = fade_out

    audio_stereo[seg_start:seg_end, 0] += mixed[:seg_len] * fade * 0.3
    audio_stereo[seg_start:seg_end, 1] += mixed[:seg_len] * fade * 0.3 * 0.95

    # Slight stereo detuning that decreases with coarsening
    detune = 0.02 * (1.0 - i / n_scales)  # more detuned at fine scales
    audio_stereo[seg_start:seg_end, 1] += mixed[:seg_len] * fade * 0.3 * np.sin(
        2 * np.pi * fund * (1 + detune) * t_audio[:seg_len])

# Normalize final mix
max_val = np.max(np.abs(audio_stereo))
if max_val > 0:
    audio_stereo /= max_val

audio_int16 = (audio_stereo * 32767).astype(np.int16)
write_wav('/home/sprite/slop-salon-gert/assets/rg-flow-01.wav', sr, audio_int16)

# Create stereo WAV for ffmpeg
# (already stereo from the two-channel array)

print(f"Audio: {T}s stereo at {sr} Hz → rg-flow-01.wav")
print(f"Image: rg-flow-01.png (3-panel: flow, detail, beta)")
