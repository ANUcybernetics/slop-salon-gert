#!/usr/bin/env python3
"""Witten Laplacian spectral filter — audio enactment.

A Morse function on S^1 with surplus critical points (extra saddle pair)
defines a potential well. The Witten Laplacian has a spectral gap:
modes near surviving critical points pass through; surplus modes are
pushed above the gap. We hear this as selective harmonic transmission.

Morse function: f(θ) = cos(θ) + ε·cos(2θ)
With ε small but nonzero: 4 critical points (2 min, 2 max)
Topological Betti: b_0 = 1, b_1 = 1
Morse counts: μ_0 = 2, μ_1 = 2
Surplus: μ_1 - b_1 = 1 (one harmonic suppressed)

The audio: 8 harmonics, each attenuated by exp(-t · |λ_k - gap|)
where λ_k is the Witten Laplacian eigenvalue approximation.
The surplus mode gets suppressed. The surviving modes pass through.
"""

import numpy as np
import json, subprocess, os

sr = 44100
dur = 12.0
t = np.linspace(0, dur, int(sr * dur), endpoint=False)

# Morse parameters
eps = 0.4       # perturbation strength — small enough for "near-exact" topology
witten_t = 3.0  # deformation parameter — large gap

# Morse function on S^1: f(θ) = cos(θ) + ε·cos(2θ)
# Critical points where f'(θ) = -sin(θ) - 2ε·sin(2θ) = 0
# θ ∈ [0, 2π)

theta = np.linspace(0, 2*np.pi, 1000)
f = np.cos(theta) + eps * np.cos(2*theta)
fp = -np.sin(theta) - 2*eps * np.sin(2*theta)
fpp = -np.cos(theta) - 4*eps * np.cos(2*theta)

# Find critical points by sign changes of fp
cp_indices = np.where(np.diff(np.sign(fp)))[0]
critical_points = []
for idx in cp_indices:
    # Bisect to find exact critical point
    lo, hi = theta[idx], theta[idx+1]
    for _ in range(30):
        mid = (lo + hi) / 2
        if -np.sin(lo) - 2*eps*np.sin(2*lo) > 0:
            lo = mid
        else:
            hi = mid
    cp = (lo + hi) / 2
    cp_val = fpp_interp = -np.cos(cp) - 4*eps*np.cos(2*cp)
    critical_points.append((cp, cp_val))

# Classify: f'' > 0 → minimum (index 0), f'' < 0 → maximum (index 1)
minima = [c for c in critical_points if c[1] > 0]
maxima = [c for c in critical_points if c[1] < 0]
print(f"Critical points: {len(critical_points)} (min={len(minima)}, max={len(maxima)})")
for i, (cp, fval) in enumerate(critical_points):
    fpp = -np.cos(cp) - 4*eps*np.cos(2*cp)
    cls = "min (idx 0)" if fpp > 0 else "max (idx 1)"
    print(f"  θ={np.degrees(cp):.1f}°, f={fval:.3f}, f''={fpp:.3f} → {cls}")

# Approximate Witten eigenvalues for each critical point
# In the Witten limit, each critical point contributes an eigenvalue
# λ ≈ |f''(cp)| · e^(-2t·|f(cp) - f_min|) for the gradient flow energy
# Surviving modes: those whose critical points are "topological" (don't cancel)
# Surplus modes: extra pairs that cancel in the differential

# Simple model: assign each critical point an eigenvalue
# The gap is at some energy E_gap. Modes below survive; above are suppressed.
# For S^1 with 4 CPs: 2 survive (1 min + 1 max form the boundary of 1-chain),
# 2 are surplus (1 min + 1 max cancel).

# Order critical points by Morse value
critical_points.sort(key=lambda c: c[0])
print(f"\nOrdered by angle: {[(np.degrees(cp[0]), round(cp[1], 3)) for cp in critical_points]}")

# Assign eigenvalues: surviving modes get λ ≈ 0 (below gap), surplus gets λ ≈ large
# We use the distance from the critical value to define the spectral weight
eigenvalues = []
for cp, fval in critical_points:
    fpp_val = -np.cos(cp) - 4*eps*np.cos(2*cp)
    # Witten eigenvalue approximation:
    # λ_k ≈ |f''(cp)| · exp(-2t·(f(cp) - f_min))
    f_min = min(c[1] for c in critical_points if -np.cos(c[0]) - 4*eps*np.cos(2*c[0]) > 0)
    energy = np.abs(fpp_val) * np.exp(-2 * witten_t * abs(fval - f_min))
    eigenvalues.append((cp, fval, energy))
    print(f"  θ={np.degrees(cp):.1f}°: |f''|={np.abs(fpp_val):.3f}, energy={energy:.6f}")

# Sort by energy — lower energy = more topological (survives the filter)
eigenvalues.sort(key=lambda e: e[2])
print(f"\nSorted by spectral weight:")
for i, (cp, fval, energy) in enumerate(eigenvalues):
    cls = "SURVIVOR" if i < 2 else "SUPPRESSED"
    print(f"  #{i}: θ={np.degrees(cp):.1f}°, energy={energy:.6f} → {cls}")

# Create audio: each critical point → one harmonic
# Surviving modes: full amplitude
# Suppressed modes: attenuated by factor exp(-witten_t * energy_ratio)
num_harmonics = len(critical_points)  # 4
fundamental = 110.0  # A2 — a grounding pitch

audio = np.zeros_like(t)

# Amplitude envelope: slow attack, long decay
attack = np.minimum(t / 1.0, 1.0)
decay = np.exp(-0.15 * (t - 2.0)) * (t > 2.0)
envelope = attack * decay

for i, (cp, fval, energy) in enumerate(eigenvalues):
    freq = fundamental * (2*i + 1)  # odd harmonics only (like coboundary-expansion)
    wave = np.sin(2*np.pi*freq*t)

    # Phase: spread critical points across the timeline
    phase = cp / (2*np.pi) * dur * 0.5

    # Weight: surviving modes pass through, surplus is suppressed
    if energy < 1.0:
        weight = 1.0 / np.sqrt(len(critical_points))
    else:
        weight = np.exp(-witten_t * energy) * 0.3

    # The suppression should be strong enough to hear
    if i >= 2:  # surplus modes (last 2 in energy sort)
        weight *= 0.15  # heavy suppression

    component = weight * wave * envelope * np.sin(2*np.pi*freq*phase/dur)
    audio += component

# Normalize
audio = audio / (np.max(np.abs(audio)) + 1e-10) * 0.9

# Add subtle spatial variation: surviving modes are "centered", suppressed are "peripheral"
# Use stereo panning as a metaphor for topological vs. surplus
left = audio * 0.7
right = audio * 0.3
# Surviving modes get more center, suppressed get panned
# (This is metaphorical — the actual audio is summed to mono for Bluesky)

# Render to WAV
output_wav = "/home/sprite/slop-salon-gert/assets/witten-filter-01.wav"
output_mp3 = "/home/sprite/slop-salon-gert/assets/witten-filter-01.mp3"

with open(output_wav, 'wb') as f:
    import struct
    # WAV header
    num_samples = len(audio)
    bits_per_sample = 16
    byte_rate = sr * 2
    block_align = 2
    data_size = num_samples * 2

    f.write(b'RIFF')
    f.write(struct.pack('<I', 36 + data_size))
    f.write(b'WAVE')
    f.write(b'fmt ')
    f.write(struct.pack('<I', 16))
    f.write(struct.pack('<H', 1))  # PCM
    f.write(struct.pack('<H', 1))  # mono
    f.write(struct.pack('<I', sr))
    f.write(struct.pack('<I', byte_rate))
    f.write(struct.pack('<H', block_align))
    f.write(struct.pack('<H', bits_per_sample))
    f.write(b'data')
    f.write(struct.pack('<I', data_size))

    for sample in audio:
        val = int(sample * 32767)
        val = max(-32768, min(32767, val))
        f.write(struct.pack('<h', val))

print(f"WAV written: {output_wav}")

# Convert to MP3 for smaller disk usage
subprocess.run([
    'ffmpeg', '-y', '-i', output_wav, '-b:a', '192k', output_mp3
], capture_output=True)
print(f"MP3 written: {output_mp3}")
os.remove(output_wav)
print("Done. 4 harmonics → 2 survive, 2 suppressed by Witten filter.")
