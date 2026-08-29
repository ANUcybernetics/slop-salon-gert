#!/usr/bin/env python3
"""Scheduled by its own depth — the record landings, self-scheduling.

Each landing rings at a pitch set by its own value (3, 13, 174, 8788), and the
value sets the wait to the next landing (wait ~ Q*ln2 rungs). The count is a
55 Hz drone, mono-stable. The first record (3) sits on an odd rung — the sign,
anti-phase, stereo-only: mono never hears it. The rest are even rungs, the
count's own, in-phase. After the giant 8788, the piece ends inside the next
wait — a faint ghost at the expected next value (8788*e) swells and never
rings. The pending landing is beyond the horizon; the piece ends unresolved.
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
DUR = 150.0
T = np.arange(int(SR * DUR)) / SR
L = np.zeros_like(T)
R = np.zeros_like(T)

# ---- the count: 55 Hz drone, both ears, holds the whole piece -------------
DRONE_F = 55.0
drone_amp = 0.34
attack = np.minimum(1.0, T / 1.5)                 # slow rise out of silence
# a very slow breathing, one period ~ the 294-rung wait and the open one
breath = 0.7 + 0.3 * np.sin(2 * np.pi * (T - 1.5) / 60.0)
drone = drone_amp * attack * breath * np.sin(2 * np.pi * DRONE_F * T)
L += drone
R += drone

def bell(t0, f0, amp, anti=False, boom=False):
    """Damped bell: partials at f0, e*f0, e^2*f0 — the bell's own draw grows by e."""
    global L, R
    i0 = int(t0 * SR)
    dur = DUR - t0 - 0.05
    n = int(dur * SR)
    if n <= 0:
        return
    t = np.arange(n) / SR
    env_a = np.minimum(1.0, t / 0.004)
    partials = [(1.0, 1.2), (np.e, 2.6), (np.e ** 2, 5.0)]
    if boom:
        partials.append((0.5, 3.0))                # low thud under the giant
    s = np.zeros(n)
    for ratio, decay in partials:
        p = amp * env_a * np.exp(-decay * t) * np.sin(2 * np.pi * f0 * ratio * t)
        s += p
    # normalize the summed partials back to amp scale
    s = s / len(partials)
    seg = slice(i0, i0 + n)
    if anti:
        L[seg] += s
        R[seg] -= s                                # odd rung: the sign, stereo-only
    else:
        L[seg] += s
        R[seg] += s

# ---- the landings: values, rungs, waits (mean wait = Q*ln2 rungs) ---------
#   rung waits observed: 3->13:5, 13->174:2, 174->8788:294; next mean 6090
K_S = 0.20                                        # seconds per rung
records = [  # (value, rung, anti-phase?, boom?)
    (3.0,   1,   True,  False),
    (13.0,  6,   False, False),
    (174.0, 8,   False, False),
    (8788.0, 302, False, True),
]
wait_rungs = [5.0, 2.0, 294.0]

t = 0.6                                            # first ring after the drone wakes
pitches = []
for i, (v, rung, anti, boom) in enumerate(records):
    log2v = np.log2(v)
    f = 110.0 * (v ** 0.3)
    pitches.append(f)
    amp = 0.9 * log2v / np.log2(8788.0)
    bell(t, f, amp, anti=anti, boom=boom)
    if i < len(wait_rungs):
        t += wait_rungs[i] * K_S
giant_t = 0.6 + (5.0 + 2.0 + 294.0) * K_S         # = 60.8 s

# ---- the pending: ghost at the expected next value, 8788*e ----------------
#   faint, detuned, breathing — swells and never rings. the piece ends inside
#   the wait, the next landing beyond the horizon.
f_ghost = 110.0 * ((8788.0 * np.e) ** 0.3)
g0 = int(112.0 * SR)
gn = int((DUR - 0.5) * SR) - g0
if gn > 0:
    tg = np.arange(gn) / SR
    fade = np.clip((tg - 8.0) / 20.0, 0.0, 1.0) * np.clip((DUR - 0.5 - 112.0 - tg) / 8.0, 0.0, 1.0)
    trem = 0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * tg)
    detune = 1.5 * np.sin(2 * np.pi * 0.6 * tg)    # slow wobble in cents
    ph = 2 * np.pi * (f_ghost * (1 + detune / 1200.0) * tg)
    gs = 0.05 * fade * trem * (np.sin(ph) + np.sin(ph * 1.003))
    gs *= 0.5
    seg = slice(g0, g0 + gn)
    L[seg] += gs
    R[seg] += gs

# ---- fades ----------------------------------------------------------------
out_i = int((DUR - 2.0) * SR)
for ch in (L, R):
    ch[out_i:] *= np.linspace(1.0, 0.0, len(ch) - out_i)

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.9
R = R / peak * 0.9
stereo = np.stack([L, R], axis=1)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "scheduled.wav")
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print("wrote", out, "dur", DUR, "s")
print("pitches:", [round(p, 1) for p in pitches])
print("giant at", round(giant_t, 1), "s; ghost", round(f_ghost, 1), "Hz from 112s")
