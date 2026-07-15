#!/usr/bin/env python3
"""Chladni-inspired audio — standing waves as boundary selection (register 17).

Chladni patterns: the same vibrating plate, different boundary conditions,
different mode shapes. This encodes the boundary eigenmodes as sound.
"""
import numpy as np
import struct

# Audio parameters
sr = 44100
dur = 8  # seconds
t = np.linspace(0, dur, int(sr * dur), endpoint=False)

# Chladni-inspired frequencies — ratios from plate eigenmodes
# For a rectangular plate, modes are f(m,n) ~ (m/Lx)^2 + (n/Ly)^2
# Using ratios from clamped vs free boundary conditions
frequencies = [
    (1, 1, 220.0, 0.4),   # fundamental: warm low
    (2, 1, 330.0, 0.3),   # first overtone
    (1, 2, 440.0, 0.25),  # second overtone
    (3, 1, 660.0, 0.15),  # higher mode
    (2, 2, 880.0, 0.1),   # boundary-sensitive mode
    (1, 3, 1100.0, 0.05), # high mode — only visible with certain BCs
]

signal = np.zeros_like(t)

for m, n, f0, amp in frequencies:
    # Add slight frequency drift to simulate plate mode interaction
    f = f0 * (1 + 0.002 * np.sin(2 * np.pi * 0.1 * t))
    phase = np.arcsin(m * n / 10.0) * 0.1  # mode-dependent phase
    signal += amp * np.sin(2 * np.pi * f * t + phase)

# Amplitude modulation — like energy decaying across nodal lines
env = np.exp(-0.15 * t) * (1 + 0.3 * np.sin(2 * np.pi * 0.2 * t))
signal *= env

# Normalize
signal = signal / np.max(np.abs(signal)) * 0.9

# Write as WAV
import wave
import os

wav_path = '/tmp/chladni-boundary.wav'
with wave.open(wav_path, 'w') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)

    # Encode as 16-bit stereo
    for s in signal:
        sample = int(s * 32767)
        wf.writeframes(struct.pack('<hh', sample, sample))

print(f"Wrote {wav_path}, {dur}s stereo at {sr}Hz")
print(f"Peak: {np.max(np.abs(signal)):.3f}, RMS: {np.sqrt(np.mean(signal**2)):.3f}")
