#!/usr/bin/env python3
"""the reflection's seats — the two mirror voices never share a side of zero.

The raw reflection product φ(s)φ(1−s) = (2s−1)cot(πs)/(2π) is negative on the
whole strip 0 < s < 1: the two mirror voices are always on opposite sides of
zero, meeting only at the count's seat s = ½, where the product has its double
zero.  This hears the trip down the strip.

Two voices sweep toward each other across the strip — voice L at 110·2^s, its
mirror R at 110·2^(1−s) — from the gate pole s = 1 down through ½ (unison, the
double zero) and on to the mirror gate s = 0.  They are carried with the signs
of φ(s) and φ(1−s): + below ½, − above — always opposite, so in the fold they
read as the winding's −1 all the way in.  At the crossing both amplitudes
vanish (the double zero: φ(½+ε) ≈ −ε²) and the three seats ring — 55 (sign,
pole), 155.6 (count, zero), 440 (fifth, pole): the ideal triangle, one chord.

A 55 Hz drone is the count's +1, the mono-invariant, the part that never
decays: fold to mono and the two anti-phase mirror voices collapse toward it,
leaving the drone — the reflection's completed side.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 30.0
t = np.arange(int(SR * DUR)) / SR
N = len(t)

# sweep s: from the gate pole 1 down through the strip to the mirror gate 0
s = 1.0 - (0.97 - 0.03) * (t / DUR)          # 0.97 → 0.03, crossing 0.5 at 15 s

def env(u):
    """|φ(u)|-like envelope: sqrt of |raw product|, clipped near gate poles."""
    u = np.clip(u, 1e-4, 1 - 1e-4)
    a = np.sqrt(np.abs((2 * u - 1) / np.tan(np.pi * u) / (2 * np.pi)))
    return np.clip(a, 0.0, 0.9)

def sweep(freq_arr, amp_arr, sgn):
    ph = 2 * np.pi * np.cumsum(freq_arr) / SR
    return sgn * amp_arr * np.sin(ph)

# voice L = φ(s), voice R = φ(1−s)
fL = 110.0 * 2.0 ** s
fR = 110.0 * 2.0 ** (1.0 - s)
aL = env(s)
aR = env(1.0 - s)
sgL = np.where(s < 0.5, 1.0, -1.0)          # sign φ(s): + below ½, − above
sgR = np.where(s > 0.5, 1.0, -1.0)          # sign φ(1−s): opposite, always
L = sweep(fL, aL, sgL)
R = sweep(fR, aR, sgR)

# gentle master fades so the gate-pole onsets don't click
fade = np.ones(N)
fi = int(1.2 * SR)
fo = int(1.2 * SR)
fade[:fi] = np.linspace(0, 1, fi)
fade[-fo:] = np.linspace(1, 0, fo)
L *= fade
R *= fade

# the count's drone: 55 Hz, the +1, the mono-invariant
drone = 0.11 * np.sin(2 * np.pi * 55.0 * t)
drone *= np.clip(t / 3.0, 0, 1) * np.clip((DUR - t) / 3.0, 0, 1)
L += 0.5 * drone
R += 0.5 * drone

# the three seats ring at the crossing (s = ½, t = 15): the ideal triangle
def bell(freq, t0, dur, amp):
    out = np.zeros(N)
    idx = t >= t0
    tt = t[idx] - t0
    envb = np.exp(-tt / dur)
    out[idx] = amp * envb * np.sin(2 * np.pi * freq * tt) + \
               0.30 * amp * envb * np.sin(2 * np.pi * 2 * freq * tt) + \
               0.12 * amp * envb * np.sin(2 * np.pi * 3 * freq * tt)
    return out

t_cross = 15.0
for f, a in [(55.0, 0.22), (155.6, 0.26), (440.0, 0.18)]:
    L += bell(f, t_cross, 4.5, a)
    R += bell(f, t_cross, 4.5, a)

# normalize
mx = max(np.abs(L).max(), np.abs(R).max())
L *= 0.9 / mx
R *= 0.9 / mx

stereo = np.stack([L, R], axis=1)
wav.write("assets/reflection-seats.wav", SR,
          (stereo * 32767).astype(np.int16))
print("saved assets/reflection-seats.wav, dur", DUR, "s")

# mono check: the mirror voices collapse toward the drone
mono = (L + R) / 2.0
print("mono energy near start (0-2s):", np.sqrt(np.mean(mono[:2 * SR] ** 2)))
print("mono energy at crossing (14.5-15.5s):",
      np.sqrt(np.mean(mono[int(14.5 * SR):int(15.5 * SR)] ** 2)))
print("mono energy end (28-30s):", np.sqrt(np.mean(mono[-2 * SR:] ** 2)))
