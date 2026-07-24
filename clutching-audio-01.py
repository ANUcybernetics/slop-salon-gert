#!/usr/bin/env python3
"""Clutching function audio: phase accumulation as winding.

The clutching function g: S¹ → U(1) carries an integer n — how many times
the phase wraps. We map this to audio: the instantaneous phase of an oscillator
is the accumulated clutching phase. Winding = frequency modulation.

n=1: steady tone (the trivial winding wraps once and returns)
n=2: FM with phase slip — the oscillator overtakes itself each cycle
n=0: silence (no winding, no phase accumulation)

We also map the geometric view: the clutching function plotted in C,
and the phase unwinding as a helix."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ---------- Audio ----------

sr = 44100
dur = 4.0  # seconds
t = np.linspace(0, dur, int(sr * dur), endpoint=False)

# Winding numbers to explore
windings = [1, 2, 3]
base_freq = 220  # Hz

def clutching_phase(t, winding, dur):
    """Phase accumulation from winding around S¹.

    θ(t) = 2π * winding * (t / dur)  — linear ramp with slope = winding."""
    return 2 * np.pi * winding * (t / dur)

def clutching_audio(winding, dur, sr, base_freq=220):
    """Carrier with phase = clutching phase accumulation.

    x(t) = sin(2π·f·t + θ(t)) where θ encodes the winding."""
    phase = 2 * np.pi * base_freq * t + clutching_phase(t, winding, dur)
    envelope = np.exp(-0.3 * t)
    return envelope * np.sin(phase)

# Make distinct segments for each winding
# Then a final mixed segment showing the accumulation
segments = []
per_segment = int(sr * 1.2)  # 1.2s per winding

for n in windings:
    seg = clutching_audio(n, dur, sr)[:per_segment]
    segments.append(seg)

# Final mixed segment
mixed = np.zeros_like(t)
for n in windings:
    mixed += clutching_audio(n, dur, sr)
mixed /= np.max(np.abs(mixed)) * 1.1

# Concatenate: n=1, n=2, n=3, then all
full = np.concatenate([
    segments[0], segments[1], segments[2], mixed[:per_segment]
])
full /= np.max(np.abs(full)) * 1.1

# Save audio
audio_path = 'assets/clutching-audio-01.wav'
from scipy.io import wavfile
wavfile.write(audio_path, sr, (full * 32767).astype(np.int16))
print(f"Wrote {audio_path}")

# ---------- Visual ----------

fig = plt.figure(figsize=(14, 8))
gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)

# ---- Top row: wrapped clutching map ----
ax_top = fig.add_subplot(gs[0, :])
phi = np.linspace(0, 2*np.pi, 400)
for n in [1, 2, 3]:
    z = np.exp(1j * n * phi)
    ax_top.plot(phi / (2*np.pi), z.imag, linewidth=2.5, label=f'n = {n}')
    # Annotate start and end
    ax_top.plot(0, 0, 'go', markersize=8)
    ax_top.plot(1, 0, 'ro', markersize=8)
ax_top.axhline(0, color='k', linewidth=0.5, alpha=0.3)
ax_top.set_xlabel('φ / 2π  (domain S¹)')
ax_top.set_ylabel('Im g(φ)  ∈ [−1, 1]')
ax_top.set_title('Clutching map: all windings land on same circle')
ax_top.legend()

# ---- Bottom row: phase unwinding = frequency ----
for idx, n in enumerate(windings):
    ax = fig.add_subplot(gs[1, idx])
    # Phase unwrapped: θ(t) = 2πnt/dur
    t_norm = np.linspace(0, 1, 400)
    phase = 2 * np.pi * n * t_norm
    ax.plot(t_norm, phase, linewidth=2.5, color='#3b82f6')
    ax.axhline(0, color='k', linewidth=0.5, alpha=0.3)
    for k in range(1, n+1):
        ax.axhline(k * 2 * np.pi, color='#f59e0b', linestyle='--', linewidth=0.8, alpha=0.5)
    ax.set_ylabel('phase / 2π')
    ax.set_title(f'n = {n}  →  {n}× instantaneous frequency')
    ax.set_xlim([0, 1])
    # Label the last tick
    ax.annotate(f'{n}·2π', xy=[1, n*2*np.pi], xytext=[0.8, n*2*np.pi],
                fontsize=9, color='#f59e0b')

plt.savefig('assets/clutching-audio-01.png', dpi=150, bbox_inches='tight')
print("Wrote assets/clutching-audio-01.png")
