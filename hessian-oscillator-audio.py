#!/usr/bin/env python3
"""Hessian oscillator audio: standing waves as Morse eigenmodes.

sin(H*t)/H is not trajectory — it's a standing wave. Critical points are fixed.
Eigenmodes oscillate at Hessian eigenfrequencies.

Minima → oscillating modes → stable tones (distinct frequencies per minimum).
Saddle → imaginary frequency → exponential growth → escape.

Each critical point contributes a voice at its eigenfrequency.
"""

import numpy as np
import scipy.io.wavfile as wav
import scipy.linalg as la
import os

sr = 44100
duration = 30
t = np.linspace(0, duration, int(sr * duration), endpoint=False)

# Scale: eigenfrequencies are tiny (1-4 rad/s for the mathematical Morse function)
# Scale them up by 100 to get audible range (100-400 Hz)
# Preserve the ratios — the harmonic structure of the Hessian matters
freq_scale = 100

# ---- Asymmetric Morse function ----
# Each minimum has a different "steepness" → different Hessian eigenfrequency
# f(x,y) = Σ w_i * ((x - cx_i)^2 + (y - cy_i)^2) + interaction terms
# Minima with different curvatures → different ω = sqrt(λ)

# Manual critical points with known Hessians:
# min0: (1.0, 0.0), curvature (8, 4) → ω = (2.828, 2.0)
# min1: (-1.0, 1.0), curvature (12, 6) → ω = (3.464, 2.449)
# min2: (0.0, -1.5), curvature (6, 10) → ω = (2.449, 3.162)
# min3: (-0.5, -0.5), curvature (20, 3) → ω = (4.472, 1.732)
# saddle: (0.0, 0.5), curvature (-10, 5) → imaginary ω = 3.162 (growth), real ω = 2.236

# Build audio directly from Hessian eigenfrequencies
# No need to construct the function — the eigenfrequencies ARE the music

critical_points = [
    {"name": "min0", "pos": (1.0, 0.0), "eigenvals": (8.0, 4.0), "type": "min"},
    {"name": "min1", "pos": (-1.0, 1.0), "eigenvals": (12.0, 6.0), "type": "min"},
    {"name": "min2", "pos": (0.0, -1.5), "eigenvals": (6.0, 10.0), "type": "min"},
    {"name": "min3", "pos": (-0.5, -0.5), "eigenvals": (20.0, 3.0), "type": "min"},
    {"name": "saddle", "pos": (0.0, 0.5), "eigenvals": (-10.0, 5.0), "type": "saddle"},
]

# Compute frequencies
for cp in critical_points:
    freqs = []
    for ev in cp["eigenvals"]:
        if ev > 1e-10:
            freqs.append(np.sqrt(ev))  # oscillating
        elif ev < -1e-10:
            freqs.append(-np.sqrt(-ev))  # imaginary → negative
        else:
            freqs.append(0.0)
    cp["freqs"] = freqs

print("Hessian eigenfrequencies (ω = sqrt(λ)):")
for cp in critical_points:
    print(f"  {cp['name']:8s}: {cp['freqs']}")

# ---- Scale to audible range ----
# Hessian eigenfrequencies are ~2-4 Hz, below hearing. Scale by 100.
# Ratios between frequencies preserve the Hessian's spectral signature.
freq_scale = 100
for cp in critical_points:
    cp["freqs"] = [f * freq_scale if abs(f) > 0 else 0 for f in cp["freqs"]]

print(f"Hessian eigenfrequencies (scaled ×{freq_scale}):")
for cp in critical_points:
    print(f"  {cp['name']:8s}: {[round(f, 1) for f in cp['freqs']]}")

# ---- Build audio from standing wave structure----
voices = np.zeros_like(t)

# Standing wave: sin(ω*t) where ω = sqrt(eigenvalue)
# The sin(H*t)/H structure: each eigenmode oscillates at its frequency
# For the audio, we use the eigenfrequencies directly

# Phase offsets: critical points don't move, but their eigenmodes
# have independent phase — the standing wave is a superposition
phases = [0.0, 1.2, 2.7, 0.5, 0.0]  # one phase per critical point

for i, cp in enumerate(critical_points):
    for j, freq in enumerate(cp["freqs"]):
        if freq > 0:
            omega = 2 * np.pi * freq
            # Standing wave: sin(ω*t + φ)
            # 1/ω scaling: lower frequencies have larger amplitude
            mode = np.sin(omega * t + phases[i]) / freq
            # Gentle decay so piece has arc
            mode *= np.exp(-0.04 * t)
            # Scale by 1/eigenvalue (steeper minimum = higher freq = quieter)
            scale = 0.1 / np.sqrt(cp["eigenvals"][j])
            voices += scale * mode
            print(f"  {cp['name']}[{j}]: ω={freq:.3f} Hz, sin(ωt+{phases[i]:.1f})/ω, scale={scale:.3f}")
        elif freq < 0:
            # Saddle: imaginary frequency → sinh(|ω|*t) = exponential growth = escape
            # This is the only direction that GROWS, not oscillates
            omega_abs = abs(freq)
            # sinh(omega*t) = (e^(ωt) - e^(-ωt)) / 2 — but clamp to prevent overflow
            tau = omega_abs * t
            tau = np.minimum(tau, 30)  # clamp exp(30) ≈ 1e13
            mode = (np.exp(tau) - np.exp(-tau)) / (2 * omega_abs)
            # Scale down heavily — saddle growth is subtle, not dominant
            scale = 0.005 / omega_abs
            # Envelope: grow in the first half, then fade
            envelope = np.exp(-0.08 * t) * np.where(t < duration/2,
                np.exp(0.15 * t), np.ones_like(t))
            mode *= envelope
            voices += scale * mode
            print(f"  {cp['name']}[{j}]: ω_imag={omega_abs:.3f}, sinh growth, scale={scale:.3f}")

# Normalize
peak = np.max(np.abs(voices))
if peak > 0:
    voices /= peak * 1.1

# ---- Grounding drone: the fixed points ----
# The critical points DO NOT MOVE. The standing wave oscillates around fixed positions.
# A low drone represents the fixed structure.
drone = np.zeros_like(t)
for cp in critical_points:
    if cp["type"] == "min":
        # Each minimum contributes a pedal point at its lowest eigenfrequency
        # Use the scaled frequencies (already in cp["freqs"])
        if len(cp["freqs"]) >= 2:
            f = cp["freqs"][1]  # lower eigenfrequency
            drone += 0.03 * np.sin(2 * np.pi * f * t) * np.exp(-0.02 * t)
# Also add a very low fundamental (representing the fixed point structure itself)
drone += 0.08 * np.sin(2 * np.pi * 40 * freq_scale * 0.01 * t) * np.exp(-0.02 * t)
drone += 0.04 * np.sin(2 * np.pi * 80 * freq_scale * 0.01 * t) * np.exp(-0.03 * t)
voices += drone

# Final normalize
peak = np.max(np.abs(voices))
if peak > 0:
    voices /= peak * 1.1

# Export WAV
out_wav = '/home/sprite/slop-salon-gert/assets/hessian-oscillator-01.wav'
wav.write(out_wav, sr, (voices * 32767).astype(np.int16))

# Export MP3
os.system(f'ffmpeg -y -i {out_wav} -c:a libmp3lame -b:a 192k '
          '/home/sprite/slop-salon-gert/assets/hessian-oscillator-01.mp3 2>/dev/null')

# Cover image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor='black')
fig.suptitle('Hessian Oscillator: critical points as frequencies',
             color='white', fontsize=13, fontweight='bold')

ax1, ax2 = axes

# Left: Morse landscape schematic + eigenfrequency bars
ax1.set_facecolor('#111111')
ax1.set_title('Critical points + Hessian eigenfrequencies',
              color='white', fontsize=11, fontweight='bold')

# Simplified landscape
Xg, Yg = np.meshgrid(np.linspace(-2.5, 2.5, 80), np.linspace(-2.5, 2.5, 80))
Zg = 4*(Xg**2-1)**2 + 3*(Yg**2-0.5)**2 + 2*Xg*Yg + (Xg+0.5)**2 + 1.5*(Yg+1.5)**2
cs = ax1.contour(Xg, Yg, Zg, levels=np.linspace(0, 30, 15), colors='#444466',
                 linewidths=0.5, alpha=0.6)

colors_pts = ['#4a9eff', '#67b7e8', '#90d4f5', '#c0e8fa', '#ff4a6a']
for cp, col in zip(critical_points, colors_pts):
    ax1.plot(cp["pos"][0], cp["pos"][1], 'o', color=col, markersize=14,
             markeredgecolor='white', markeredgewidth=1.5, zorder=5)
    ax1.text(cp["pos"][0]+0.15, cp["pos"][1]+0.15, cp["name"],
             color='white', fontsize=10, fontweight='bold', zorder=6)

# Eigenfrequency bars
for cp, col in zip(critical_points, colors_pts):
    for j, f in enumerate(cp["freqs"]):
        if f > 0:
            ax1.plot([cp["pos"][0], cp["pos"][0]], [cp["pos"][1], cp["pos"][1] + f],
                    color=col, linewidth=4, alpha=0.7, zorder=4)
            # Frequency label
            ax1.text(cp["pos"][0]+0.2, cp["pos"][1]+f/2, f'{f:.1f}',
                    color=col, fontsize=8, fontweight='bold', va='center')
        elif f < 0:
            ax1.plot([cp["pos"][0], cp["pos"][0]],
                    [cp["pos"][1], cp["pos"][1] - abs(f)*0.3],
                    color='#ff4a6a', linewidth=4, alpha=0.7, zorder=4,
                    linestyle='--')
            ax1.text(cp["pos"][0]+0.2, cp["pos"][1]-abs(f)*0.15, f'exp({abs(f):.1f})',
                    color='#ff4a6a', fontsize=8, fontweight='bold', va='center')

ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-2.5, 2.5)
ax1.set_aspect('equal')

# Right: time series of the standing wave piece
ax2.set_facecolor('#111111')
ax2.set_title('Standing wave: sin(H*t)/H',
              color='white', fontsize=11, fontweight='bold')

# Show individual voices as faint lines
for i, cp in enumerate(critical_points):
    for j, freq in enumerate(cp["freqs"]):
        if freq > 0:
            omega = 2 * np.pi * freq
            v = np.sin(omega * t) / freq
            v *= np.exp(-0.04 * t)
            scale = 0.1 / np.sqrt(cp["eigenvals"][j])
            ax2.plot(t, v * scale * 5, color=colors_pts[i], linewidth=0.8, alpha=0.3)
        elif freq < 0:
            omega_abs = abs(freq)
            v = (np.exp(omega_abs * t) - np.exp(-omega_abs * t)) / (2 * omega_abs)
            v *= (1 - np.exp(-0.1 * t)) * np.exp(-0.05 * t)
            scale = 0.015 / omega_abs
            ax2.plot(t, v * scale * 50, color='#ff4a6a', linewidth=0.8, alpha=0.3)

# Full mix
time_axis = t
ax2.plot(time_axis, voices * 3, color='white', linewidth=1.5, alpha=0.9,
         label='total standing wave')
ax2.set_xlabel('Time (s)', color='white', fontsize=10)
ax2.set_ylabel('Amplitude', color='white', fontsize=10)
ax2.legend(fontsize=9, loc='upper right', facecolor='#222')
ax2.grid(alpha=0.15)
ax2.tick_params(colors='white')

plt.tight_layout()
out_img = '/home/sprite/slop-salon-gert/assets/hessian-oscillator-01-cover.jpg'
plt.savefig(out_img, dpi=150, facecolor='black', bbox_inches='tight')
plt.close()

print(f"WAV: {os.path.getsize(out_wav):,} bytes")

# Create video
os.system(f'ffmpeg -loop 1 -t {duration} -i '
          '/home/sprite/slop-salon-gert/assets/hessian-oscillator-01-cover.jpg '
          f'-i {out_wav} -c:v libx264 -tune stillimage -crf 20 -c:a aac '
          '-pix_fmt yuv420p /home/sprite/slop-salon-gert/assets/hessian-oscillator-01.mp4 2>/dev/null')
print("Done. hessian-oscillator-01.mp4 ready")
