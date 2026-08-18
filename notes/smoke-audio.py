#!/usr/bin/env python3
"""smoke-audio — the where becomes nowhere.

A noise bed that begins as a single localizable source — a where: correlated
between the ears, bright-edged, you could point at it. Then it disperses. The
cutoff glides 8 kHz -> 150 Hz, so the high edge that locates a sound blurs
away. The stereo image decorrelates into two independent beds, so the where
spreads across the whole field — everywhere, which is nowhere. In the last
stretch the residual source-image turns anti-phase: the where inverts into a
hole at the centre. Then the whole bed thins to the air — a diffusion, not a
gate and not a pop. The smoke never had atoms, so there was never a count;
it only spreads, and then it is not there.

Inverted from salt (kept the where): smoke loses the where to everywhere.
Breaks the room's run of gated/popped tones — the first fully continuous,
eventless material.
"""
import numpy as np
import scipy.io.wavfile as wav
from scipy import signal

sr = 44100
dur = 50.0
N = int(sr * dur)
rng = np.random.default_rng(20260818)

t = np.arange(N) / sr

# ---- three noise beds ----
# S: the shared source (a where).  A, B: independent dispersal (the everywhere).
S = rng.standard_normal(N)
A = rng.standard_normal(N)
B = rng.standard_normal(N)

# ---- time-varying one-pole lowpass, cutoff 8000 -> 150 Hz ----
fc = 8000.0 * (150.0 / 8000.0) ** (t / dur)

def one_pole(x, fc):
    """y[n] = (1-a[n]) x[n] + a[n] y[n-1], a = exp(-2 pi fc/sr), per block."""
    y = np.empty_like(x)
    zi = np.zeros(1)
    block = 2048
    for s in range(0, len(x), block):
        e = min(s + block, len(x))
        a = np.exp(-2 * np.pi * fc[s] / sr)
        y[s:e], zi = signal.lfilter([1.0 - a], [1.0, -a], x[s:e], zi=zi)
    return y

print("filtering ...", flush=True)
Sf = one_pole(S, fc)
Af = one_pole(A, fc)
Bf = one_pole(B, fc)

# ---- envelopes ----
def piecewise(points, t):
    pts = np.array(points, dtype=float)
    return np.interp(t, pts[:, 0], pts[:, 1])

# onset: a soft waft up, no percussive start
on = 1.0 - np.exp(-t / 0.7)

# source level: 1 -> 0.35 as it disperses (the ghost that later inverts)
w_s = piecewise([(0, 1.0), (6, 1.0), (30, 0.35), (50, 0.35)], t)
# independent beds rise to carry the everywhere
w_i = piecewise([(0, 0.0), (6, 0.0), (30, 0.65), (50, 0.65)], t)
# inversion rotation: the source-image swings from same-phase to anti-phase
psi = piecewise([(0, 0.0), (30, 0.0), (46, np.pi / 2.0)], t)

# ---- stereo build ----
# source component rotates: (cos+sin)S in L, (cos-sin)S in R
L_s = (np.cos(psi) + np.sin(psi)) * Sf * w_s
R_s = (np.cos(psi) - np.sin(psi)) * Sf * w_s

# slow independent curls, so the two ears drift apart like smoke eddies
mod_L = 0.78 + 0.22 * np.sin(2 * np.pi * 0.11 * t + 0.0)
mod_R = 0.78 + 0.22 * np.sin(2 * np.pi * 0.16 * t + 2.1)

# dispersal end: thins exponentially from 38 s — a diffusion, not a cut
end = np.ones(N)
mask = t > 38.0
end[mask] = np.exp(-(t[mask] - 38.0) / 1.5)

L = (L_s + Af * w_i) * on * end * mod_L
R = (R_s + Bf * w_i) * on * end * mod_R

mix = np.stack([L, R], axis=1)

# global normalise: one readout level, absences as the air
peak = np.abs(mix).max()
mix *= 0.9 / peak

wav.write("assets/smoke.wav", sr, (mix * 32767).astype(np.int16))
print(f"saved assets/smoke.wav  {dur} s")

# ---- verification: the correlation should fall from high to negative ----
def corr(a, b):
    a = a - a.mean(); b = b - b.mean()
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

for ws in (2.0, 20.0, 40.0, 47.0):
    i0, i1 = int(ws * sr), int((ws + 3) * sr)
    print(f"  L/R corr @ {ws:>4.0f}s: {corr(L[i0:i1], R[i0:i1]):+.3f}")

tail = np.abs(mix[int(48.5 * sr):]).max()
print(f"  peak |mix| after 48.5s: {tail:.2e}  (diffused to the air)")
