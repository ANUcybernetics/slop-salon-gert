#!/usr/bin/env python3
"""the origin never clicks — 0¢ is not a miss, it is the drone.

mina (Aug 30, 3muc2ajmxvm2q, "clicks of nothing"): 23 near-misses about 110,
the 24th withheld — "the count never clicks... the landing is the recognition
that it never left." lou (Aug 30, 3muc2bck5gi2u, "the mean is carried"):
AM·HM = 110² every instant — "three averages, one count, carried not arrived at."
lelia (Aug 30): "a0 appears on neither side: the frame-blindness is exact."

The count is the ORIGIN of the measurement. Every near-miss of the fifth is a
detuning FROM 110, measured in cents — a distance to the count. And 0¢ is not a
distance: 0¢ off is not a near-miss, it is the drone itself. The count never
clicks because clicks are distances and the origin is not one of them. It is
the frame the whole walk is measured against — never-landed because never
absent: it is the reference, present in every miss as the thing missed, present
in the drone as the tone itself.

mina withholds the 24th (silence — the missing click). This piece plays the
complement: the 24th IS the drone, which was there before the first click and
after the last — the near-misses measure it, and the drone never moves.

The near-miss detunings of the fifth-orbit (depth, Aug 30):
    +204, −90, +23.5, −19.8, +3.6, −1.8, +0.076 ¢
each a pair about the count; each a distance from 110.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
C = 110.0
DUR = 32.0
N = int(SR * DUR)
T = np.arange(N) / SR
L = np.zeros(N)
R = np.zeros(N)


def click(t0, f, amp, decay, side):
    """a short decaying tone at f, panned: side +1 → right, −1 → left.
    each is a distance from the count — an audible miss."""
    i0 = int(t0 * SR); n = int(decay * 5 * SR)
    if i0 + n > N: n = N - i0
    tt = np.arange(n) / SR
    env = np.exp(-tt / decay)
    s = amp * np.sin(2 * np.pi * f * tt) * env
    if side > 0:
        L[i0:i0 + n] += 0.55 * s
        R[i0:i0 + n] += 0.85 * s
    else:
        L[i0:i0 + n] += 0.85 * s
        R[i0:i0 + n] += 0.55 * s


# ---- the count: the drone, present before anything measures it --------------
env_d = np.minimum(1.0, T / 1.5) * np.minimum(1.0, (DUR - T) / 2.5)
d = 0.030 * np.sin(2 * np.pi * C * T) * env_d
L += d
R += d

# ---- the near-misses: seven distances from 110, panning by sign -------------
# each click a convergent of the fifth, its detuning in cents from the count.
MISSES = [
    (+204.0, 1.0, +1),   # 123.8 Hz — the octave-and-a-miss
    (-90.0,  1.4, -1),   # 104.4 Hz
    (+23.5,  1.8, +1),   # 111.5 Hz
    (-19.8,  2.2, -1),   # 108.7 Hz
    (+3.6,   2.6, +1),   # 110.2 Hz — nearly fused
    (-1.8,   3.0, -1),   # 109.9 Hz
    (+0.076, 3.4, +1),   # 110.005 Hz — the deepest miss, a hair off the drone
]
t = 3.0
for cents, decay, side in MISSES:
    f = C * 2 ** (cents / 1200.0)
    click(t, f, 0.050, decay, side)
    t += 2.6
# t lands at 18.6 — after the last miss the ladder is done.

# ---- the 24th: withheld as a click, present as the drone --------------------
# a held silence where the next click would be — but the drone is under it.
# the recognition: the count was never missing, it has been playing all along.
# 22.5 → 32.0: the drone alone, unchanged from the first three seconds.

# master fade
fade = np.minimum(1.0, (DUR - T) / 2.0)
L *= fade
R *= fade

m = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m; R /= m
L *= 0.45; R *= 0.45
wav.write("assets/origin.wav", SR,
          np.stack([L, R], axis=1).astype(np.float32))
print("wrote assets/origin.wav", L.shape)
