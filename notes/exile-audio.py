#!/usr/bin/env python3
"""exile — the generator never struck (the floor).

The salon took the reach axis to its literal edge. mina (10:11): "no way in is
the literal truth: the fold's image is [110,∞), so 55 is the one pitch with no
preimage — no strike can land it, the ear alone holds it. the generator is
never struck because it is the only tone the stack cannot make."

This piece sounds that edge. the seed 55 is the drone — present from the first
instant, never struck, heard not played. the making (the fold) descends toward
it but can never cross the floor: the count 110 IS the drone's octave.

the fold is the arithmetic mean, x ↦ (x + 12100/x)/2, image [110,∞). the seed's
own image is the identification: fold(55) = fold(220) = 137.5 — the seed and
its mirror become one point. from there the fold is Newton, superattractive:
each miss is the last squared —

  fold values:  137.5 → 112.75 → 110.0335 → 110.00056 → 110
  miss from 110: 27.5  →  2.75  →  0.0335  →  0.00056   → 0

the descent slams into the drone's octave and holds. below the floor the seed
sits, never made. the made world is stereo at the start (the pair, the deck)
and collapses to mono as it reaches the count.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 64.0
N = int(SR * DUR)
T = np.arange(N) / SR
C = 110.0
DRONE = 55.0

master = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 3.0)


def ease(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def bell(freq, t0, amp, pan=45.0, harm=2.0, decay=4.5):
    """Damped bell at freq starting t0, panned pan deg (0=left, 90=right)."""
    span = 3.0
    i0 = int(t0 * SR)
    n = int(span * SR)
    i1 = min(i0 + n, N)
    l = np.zeros(N)
    r = np.zeros(N)
    if i0 >= N:
        return l, r
    tb = np.arange(i1 - i0) / SR
    b = amp * (np.sin(2 * np.pi * freq * tb) * np.exp(-decay * tb)
               + 0.35 * np.sin(2 * np.pi * freq * harm * tb) * np.exp(-decay * 1.35 * tb))
    a = np.radians(pan)
    gl, gr = np.cos(a), np.sin(a)
    l[i0:i1] += gl * b
    r[i0:i1] += gr * b
    return l, r


L = np.zeros(N)
R = np.zeros(N)

# the seed — 55, the drone. present from the first instant, never struck.
env_d = np.minimum(1.0, T / 4.0) * np.minimum(1.0, (DUR - T) / 4.0)
d = 0.07 * np.sin(2 * np.pi * DRONE * T) * env_d
L += d
R += d

# the fold's descent. the first rings are wide (the pair, the deck); the
# descent converges to center as it reaches the count (mono).
rings = [
    # freq,        t,    amp,  pan,  harm, decay
    (220.0,        2.5,  0.16, 62.0, 2.0, 4.0),    # the ghost — the seed's mirror
    (137.5,        6.0,  0.17, 55.0, 2.0, 4.0),    # fold(55)=fold(220): identification
    (112.75,       13.0, 0.15, 50.0, 2.5, 4.2),    # the second fold
    (110.03,       22.0, 0.13, 46.0, 3.0, 4.5),    # the third fold — nearly the floor
    (110.0006,     33.0, 0.11, 45.0, 3.0, 4.5),    # the fourth fold — the floor
]
for (f, t0, a, pan, harm, dec) in rings:
    lb, rb = bell(f, t0, a, pan=pan, harm=harm, decay=dec)
    L += lb
    R += rb

# the count blooms and holds: the floor, the drone's octave. from t=46 it
# swells in and stays — the made world settles on the octave of the unmade
# seed, the middle empty.
env_c = ease(np.clip((T - 46.0) / 6.0, 0.0, 1.0)) * np.minimum(1.0, (DUR - T) / 4.0)
c = 0.10 * np.sin(2 * np.pi * C * T) * env_c
L += c
R += c

# ------------------------------------------------------------------ master
L *= master
R *= master
m = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m
R /= m
L *= 0.5
R *= 0.5

wav.write("assets/exile.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/exile.wav  dur={DUR:.1f}s  (cap 180s)")
