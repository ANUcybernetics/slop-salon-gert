#!/usr/bin/env python3
"""discriminant-map-audio — a walk across the discriminant's plane.

Fix the norm c = 1 and walk the trace b from −3 to +3.  Every point on the
walk is a monic quadratic; the discriminant Δ = b² − 4c decides the character:

    Δ > 0  — two real roots, the sign: the pair rings as two tones, the
             geometric center the norm's pitch 220.  They split wide at the
             ends (at b=∓3 the roots are φ² and 1/φ²) and converge toward the
             seam.
    Δ = 0  — the fused landing, count one: the two tones become a single ring.
    Δ < 0  — the ghost: the roots leave the real line; the two tones smear —
             a widening detune that never locks, widest at b=0, the point
             x²+1 itself, the refusal.

A drone at 110 Hz (the norm, the room, count one) holds under the whole walk.
Bells mark the two seams; the centre is the widest smear — the ghost never
rings, it refuses.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
DUR = 40.0
DRONE = 110.0          # χ₀ — the norm, the room, never moves
UNIT = 220.0           # the pair's geometric centre (|r₁·r₂| = 1)
DETUNE = 3.0           # widest smear half-width, at the ghost point b=0

n = int(SR * DUR)
t = np.arange(n) / SR

# --- the walk: b from −3 to +3 across [2, 38] s --------------------------------
walk = np.clip((t - 2.0) / (DUR - 4.0), 0.0, 1.0)
b = -3.0 + 6.0 * walk

Delta = b * b - 4.0
real = Delta >= 0.0
sq = np.sqrt(np.abs(Delta))
r_mag = np.abs((-b + sq) / 2.0)      # first root magnitude (larger)
r_neg = np.abs((-b - sq) / 2.0)      # second root magnitude (smaller)
w = np.sqrt(np.clip(4.0 - b * b, 0.0, None)) / 2.0   # imag part, 0→1→0

fL = np.where(real, UNIT * r_mag, UNIT + DETUNE * w)
fR = np.where(real, UNIT * r_neg, UNIT - DETUNE * w)

# amplitude: the sign rings clear; the ghost smears, slightly softer
ampL = np.where(real, 0.135, 0.115)
ampR = np.where(real, 0.135, 0.115)

phL = 2 * np.pi * np.cumsum(fL) / SR
phR = 2 * np.pi * np.cumsum(fR) / SR
pairL = ampL * np.sin(phL)
pairR = ampR * np.sin(phR)

# --- the drone under everything -------------------------------------------------
env_d = np.ones(n)
env_d[: int(2.0 * SR)] = np.linspace(0, 1, int(2.0 * SR))
env_d[-int(2.0 * SR):] = np.linspace(1, 0, int(2.0 * SR))
drone = 0.06 * env_d * np.sin(2 * np.pi * DRONE * t)

# --- bells at the seams (count one): b = ±2, t = 8 and 32 ----------------------
def bell(start, dur=2.2, f=220.0, amp=0.12):
    n2 = int(SR * dur)
    tt = np.arange(n2) / SR
    e = np.exp(-tt * 2.2)
    # fundamental + a soft fifth, both centred, ring in mono
    s = e * (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 1.5 * f * tt))
    s *= amp
    return s, int(start * SR)

s1, i1 = bell(8.0)
s2, i2 = bell(32.0)

L = drone + pairL
R = drone + pairR
for s, i in ((s1, i1), (s2, i2)):
    if i + len(s) <= n:
        L[i:i + len(s)] += s
        R[i:i + len(s)] += s

# --- global fades, normalise ---------------------------------------------------
fade = np.ones(n)
fade[: int(0.4 * SR)] = np.linspace(0, 1, int(0.4 * SR))
fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR))
stereo = np.stack([L * fade, R * fade], axis=1)
peak = np.max(np.abs(stereo))
stereo = stereo / peak * 0.85
wavfile.write("assets/discriminant-map.wav", SR, (stereo * 32767).astype(np.int16))
print("saved assets/discriminant-map.wav  %.2fs" % (DUR))

# --- verify the character is legible --------------------------------------------
def rms(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)]
    return np.sqrt(np.mean(seg.astype(np.float64) ** 2)) / 32767

def mono_rms(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)]
    m = seg[:, 0] + seg[:, 1]
    return np.sqrt(np.mean(m.astype(np.float64) ** 2)) / 32767

for name, a, b_ in [("split wide   t=4  (b=-3)", 4, 5),
                    ("converging   t=6.5", 6.5, 7.5),
                    ("seam         t=8  (b=-2)", 7.5, 8.5),
                    ("ghost smear  t=20 (b=0)", 19.5, 20.5),
                    ("seam         t=32 (b=+2)", 31.5, 32.5),
                    ("split wide   t=36 (b=+3)", 36, 37)]:
    print("%-22s L %6.4f R %6.4f mono-sum %6.4f" % (name, rms(stereo, a, b_), rms(stereo, a, b_), mono_rms(stereo, a, b_)))
