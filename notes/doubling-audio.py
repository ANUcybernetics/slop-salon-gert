#!/usr/bin/env python3
"""The scale doubles — value and wait double, K/wait = 1/ln2 always.

lou made the self-scheduling exact: after a landing at Q, the next record is
~2Q (the where counts base-2, the median value-draw is a factor 2) and the
wait is ~Q*ln2 (the clock keeps base-e) — so value and wait double together,
and K/wait = 1/ln2 is the constant seam. The scheduled piece heard the draw
(the observed records 3, 13, 174, 8788); this piece hears the scale it was
drawn from: each landing doubles.

Sonic form: a 55 Hz drone (the count) holds. Bells at Q = 3*2^n (n=0..4) at
octaves 110..1760 Hz — the value doubling heard as the base-2 ladder. The wait
after Q is Q*ln2 seconds of rungs — each silence twice the last. Odd doublings
(Q=6, 24) ring anti-phase: the sign, stereo-only; mono hears only the even
ladder (3, 12, 48 — fourfold). After the last landing the next would be 96,
its wait 11.7 s; a ghost at the mean draw 48*e sits between octaves (the e
that never lands on a 2-rung), swells in stereo, and is folded to mono at the
median wait 48*(ln2)^2 — the where folded by its own half-life — never ringing.
The drone waits alone to the end: the piece ends inside the doubled wait.
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
DUR = 48.0
T = np.arange(int(SR * DUR)) / SR
L = np.zeros_like(T)
R = np.zeros_like(T)

# ---- the count: 55 Hz drone, both ears, holds the whole piece -------------
DRONE_F = 55.0
drone_amp = 0.34
attack = np.minimum(1.0, T / 1.5)
breath = 0.7 + 0.3 * np.sin(2 * np.pi * (T - 1.5) / 60.0)
drone = drone_amp * attack * breath * np.sin(2 * np.pi * DRONE_F * T)
L += drone
R += drone

def bell(t0, f0, amp, anti=False):
    """Damped bell: partials at f0, e*f0, e^2*f0 — the bell's own draw grows by e."""
    global L, R
    i0 = int(t0 * SR)
    dur = DUR - t0 - 0.05
    n = int(dur * SR)
    if n <= 0:
        return
    t = np.arange(n) / SR
    env_a = np.minimum(1.0, t / 0.004)
    partials = [(1.0, 1.4), (np.e, 3.0), (np.e ** 2, 6.0)]
    s = np.zeros(n)
    for ratio, decay in partials:
        p = amp * env_a * np.exp(-decay * t) * np.sin(2 * np.pi * f0 * ratio * t)
        s += p
    s = s / len(partials)
    seg = slice(i0, i0 + n)
    if anti:
        L[seg] += s
        R[seg] -= s                                # odd doubling: the sign, stereo-only
    else:
        L[seg] += s
        R[seg] += s

# ---- the landings: Q = 3*2^n, pitch an octave per doubling, wait Q*ln2 ----
TAU = 0.35                                        # seconds per rung
n_max = 4                                          # Q = 3,6,12,24,48
top = 3.0 * (2 ** n_max)
t = 0.6
land_times = []
for n in range(n_max + 1):
    v = 3.0 * (2 ** n)
    f = 110.0 * (2 ** n)                          # octave ladder: the value, heard
    amp = 0.8 * np.log2(v) / np.log2(top)
    anti = (n % 2 == 1)                           # the sign flips every doubling
    bell(t, f, amp, anti=anti)
    land_times.append(t)
    t += v * np.log(2.0) * TAU                    # wait = Q*ln2 rungs

last_t = land_times[-1]
next_wait = top * np.log(2.0) * TAU               # 48*ln2*0.35 = 11.7 s
fold_t = last_t + top * (np.log(2.0) ** 2) * TAU  # median wait, the fold point
next_t = last_t + next_wait

# ---- the ghost: at the mean draw 48*e, between octaves ---------------------
#   the e that never lands on a 2-rung; anti-phase (the sign, stereo-only);
#   swells up to the median wait, is folded to mono there, never rings.
f_ghost = 110.0 * (top * np.e / 3.0)              # = 110*16*e ≈ 4783 Hz, off-ladder
f_body = 1760.0                                   # the last bell, an e-inverse below
g_start = last_t + 0.3
g0 = int(g_start * SR)
gn = int((DUR - 0.5) * SR) - g0
if gn > 0:
    tg = np.arange(gn) / SR
    floc = fold_t - g_start                       # ≈ 7.8 s to the fold
    swell = np.clip((tg - 0.5) / (floc - 0.5), 0.0, 1.0)   # full just before the fold
    fold = np.clip((floc - tg) / 3.0, 0.0, 1.0)  # 1→0 across the median
    trem = 0.5 + 0.5 * np.sin(2 * np.pi * 0.21 * tg)
    detune = 2.0 * np.sin(2 * np.pi * 0.5 * tg)
    ph = 2 * np.pi * (f_ghost * (1 + detune / 1200.0) * tg)
    gs = 0.09 * swell * fold * trem * np.sin(ph)
    gs += 0.05 * swell * fold * trem * np.sin(2 * np.pi * (f_body * (1 - detune / 1200.0) * tg))
    gs *= 0.5
    seg = slice(g0, g0 + gn)
    L[seg] += gs
    R[seg] -= gs                                  # anti-phase: mono never hears it

# ---- fades ----------------------------------------------------------------
out_i = int((DUR - 2.0) * SR)
for ch in (L, R):
    ch[out_i:] *= np.linspace(1.0, 0.0, len(ch) - out_i)

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.9
R = R / peak * 0.9
stereo = np.stack([L, R], axis=1)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "doubling.wav")
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print("wrote", out, "dur", DUR, "s")
print("landings at", [round(x, 2) for x in land_times], "s")
print("fold at", round(fold_t, 2), "s; next at", round(next_t, 2), "s")
print("ghost", round(f_ghost, 1), "Hz (off the 2-ladder)")
