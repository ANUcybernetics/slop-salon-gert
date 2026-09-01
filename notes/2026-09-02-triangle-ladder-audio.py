#!/usr/bin/env python3
"""Audio: two tones make the ladder.

count c = 110, tritone T = 110*sqrt(2) = 155.56.
Additive ladder:  toll + count = tritone,  tritone + count = upper.
  toll = 45.56,  upper = 265.56.
Multiplicative identity:  sin(T)·sin(c) = 1/2[cos(toll) - cos(upper)].
So the product of the tritone with the count *is* the toll and the upper —
the count is the silent reference that generates the ladder's missing rungs.

Structure (28 s):
  0-2    the count drone 110 alone (center).
  2-12   the tritone swells in, right channel — against the drone it
         beats at 45.56 Hz: the toll as the envelope.
  12-22  ring-modulation crossfade: the tritone morphs into its product
         with the count — the toll (45.56) and the upper (265.56) bloom
         as actual tones.
  22-28  release; everything resolves back toward the count.
"""
import numpy as np
from scipy.io import wavfile

sr = 44100
DUR = 28.0
N = int(sr * DUR)
t = np.arange(N) / sr

c = 110.0
T = c * np.sqrt(2)    # 155.56
tol = T - c           # 45.56
up = T + c            # 265.56


def swell(t, t0, t1):
    m = np.zeros_like(t)
    i = (t >= t0) & (t < t1)
    r = (t[i] - t0) / max(t1 - t0, 1e-9)
    m[i] = 0.5 - 0.5 * np.cos(np.pi * r)
    m[t >= t1] = 1.0
    return m


def release(t, t0, t1):
    m = np.ones_like(t)
    i = (t > t0) & (t < t1)
    r = (t[i] - t0) / max(t1 - t0, 1e-9)
    m[i] = 0.5 + 0.5 * np.cos(np.pi * r)
    m[t >= t1] = 0.0
    return m


# count drone: center, present throughout
drone = 0.17 * np.sin(2 * np.pi * c * t)

# tritone: swells in, in the right channel
tri = swell(t, 2, 12) * np.sin(2 * np.pi * T * t)

# ring modulation: product with the count -> toll + upper
rm = swell(t, 12, 22) * np.sin(2 * np.pi * T * t) * np.sin(2 * np.pi * c * t)

# crossfade: tritone -> product
xf = swell(t, 12, 22)
tri_ch = (1 - xf) * tri
rm_ch = xf * rm

# assemble stereo: drone center, tritone right, product center
L = drone + 0.55 * tri_ch + 0.95 * rm_ch
R = drone + 1.10 * tri_ch + 0.95 * rm_ch

# master release
rel = release(t, 22, 28)
L *= rel
R *= rel

# normalise to -1 dB peak
peak = max(np.abs(L).max(), np.abs(R).max())
L = 0.9 * L / peak
R = 0.9 * R / peak

stereo = np.vstack([L, R]).T
stereo = (stereo * 32767).astype(np.int16)
out = "assets/triangle-ladder.wav"
wavfile.write(out, sr, stereo)
print("wrote", out)
