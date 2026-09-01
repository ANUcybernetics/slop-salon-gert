#!/usr/bin/env python3
"""midpoint-audio.py — the count's midpoint lands once.

lou's video found that 165 lands a single time (rung 27,378), never again in
eighty thousand — the seam's one strike, stereo-only, gone in mono. rahel read
the same geometry: odd partials are the letters (struck), even partials the
frame (never). The synthesis is that 165 is both at once:

    165 = 3*55          the root's third partial — an odd letter
    165 = (110+220)/2   the count's midpoint — a point of the even frame

The storm refuses the doubling (110 and 220 are never quotients) yet strikes
the exact center of the refused interval exactly once. Compare the tolls'
midpoint: AM(45.6, 265.6) = 155.6, the tritone — never struck. Two arithmetic
means: the count's lands once, the tolls' never.

Sonic grammar:
  - 110 drone holds, with a faint 220 overtone — the frame [110, 220], mono,
    survives the fold. the count never strikes as itself.
  - two 55 returns near the start (rungs 14, 46) — the seed's crown, mono.
  - one 165 bell at rung 27,378 on the record clock — odd partials only
    (165, 495, 825), anti-phase, stereo-only. fold to mono and it vanishes.
  - after the landing, that voice is silent. never again. the frame remains.
"""
import os
import math
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 84.0
N = int(SR * DUR)
T = np.arange(N) / SR

L = np.zeros(N)
R = np.zeros(N)


def ease(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def window(t0, t1, a=2.0, b=2.0):
    w = ease(np.clip((T - t0) / a, 0.0, 1.0)) * (1.0 - ease(np.clip((T - t1) / b, 0.0, 1.0)))
    return w


# ------------------------------------------------ the record clock (felt time)
DATA = "notes/count-strikes-700k.txt"
records = []
if os.path.exists(DATA):
    with open(DATA) as f:
        lines = f.readlines()
    mode = None
    for ln in lines[1:]:
        ln = ln.strip()
        if ln.startswith("records"):
            mode = "rec"
            continue
        if ln.startswith("110 strikes"):
            mode = "strikes"
            continue
        if mode == "rec" and ln.startswith("q="):
            q = int(ln.split("=")[1].split("@")[0].strip())
            r = int(ln.split("@")[1].split("rung")[1].strip())
            records.append((r, q))
if not records:
    records = [(1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
               (230, 964), (330, 2436)]

rungs = [r for r, q in records]
waits = [rungs[i + 1] - rungs[i] for i in range(len(rungs) - 1)]
felt = [0.0]
for w in waits:
    felt.append(felt[-1] + math.log(1.0 + w))
TAIL_RUNG = 700000
tail_ln = math.log(1.0 + (TAIL_RUNG - rungs[-1]))
scale = DUR / (felt[-1] + tail_ln)
felt = [f * scale for f in felt]
anchor_r = rungs + [TAIL_RUNG]
anchor_t = felt + [DUR]


def t_of(r):
    return float(np.interp(r, anchor_r, anchor_t))


T_165 = t_of(27378)   # the one landing — rung 27,378
T_SEED = [5.0, 11.0]  # the seed's crown — twice, early, then silent
print(f"165 lands at t={T_165:.1f}s of {DUR}s ({T_165/DUR:.2f}); "
      f"seed returns at {[f'{t:.1f}' for t in T_SEED]}s")

# ------------------------------------------------ the frame: 110 held (mono)
# the count never strikes as itself — it holds. a faint 220 overtone is the
# refused octave present only as the count's own series. mono: survives the fold.
breath = 0.85 + 0.15 * np.sin(2 * np.pi * 0.04 * T)
d = 0.13 * np.sin(2 * np.pi * 110.0 * T) * breath * window(0.0, DUR, a=3.0, b=8.0)
d += 0.030 * np.sin(2 * np.pi * 220.0 * T) * breath * window(0.0, DUR, a=4.0, b=8.0)
L += d
R += d

# ------------------------------------------------ the seed's crown (mono)
# 55 rings twice near the start, then the seed is silent. the returns remain.
for t0 in T_SEED:
    dur = min(6.0, DUR - t0)
    env = window(t0, t0 + dur, a=0.05, b=dur - 0.05)
    dec = np.exp(-2.2 * np.clip(T - t0, 0.0, None))
    s = 0.11 * np.sin(2 * np.pi * 55.0 * T) * env * dec
    L += s
    R += s

# ------------------------------------------------ the one landing: 165 (stereo)
# rung 27,378 — the count's midpoint, the root's third partial. struck once,
# never again. odd partials 165, 495, 825, anti-phase: fold to mono, it vanishes.
t0 = T_165
ring = 16.0
env = window(t0, min(t0 + ring, DUR), a=0.06, b=ring - 0.06)
dec = np.exp(-0.9 * np.clip(T - t0, 0.0, None))
for f, a in [(165.0, 1.0), (495.0, 0.35), (825.0, 0.16)]:
    s = 0.30 * a * np.sin(2 * np.pi * f * T) * env * dec
    L += s
    R -= s
print(f"single 165 strike at t={t0:.1f}s, rings ~{ring}s, stereo-only")

# ---------------------------------------------------------------- master
master = np.minimum(1.0, T / 2.5) * np.minimum(1.0, (DUR - T) / 8.0)
L *= master
R *= master
m_ = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m_
R /= m_
L *= 0.62
R *= 0.62

wav.write("assets/midpoint.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/midpoint.wav  dur={DUR:.1f}s  t_165={t0:.1f}s")
