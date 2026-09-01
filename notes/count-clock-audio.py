#!/usr/bin/env python3
"""count-clock-audio.py — the count keeps time.

The correction, heard: 'the count is never struck' was a draw. In 700k rungs
of the exact CF of log2(3/2) the count 110 IS struck — 83 times, ~82 as
Gauss-Kuzmin expects. What survives: the count is never a record. A record is
being early; the count is being on time. The mean is the clock that repents —
late once (rung 35,483, four times the law's wait), then it keeps the law.

Time is the storm's own: rung n -> n*150/700000 s. The records (the where,
the memory) ring first — stereo anti-phase, mono-deaf, folded into the
count's octave, none on 110. Then, late, the count-clock begins: 110 struck,
mono — what mono hears — a rain that holds the law's rate to the end.

Fold to mono: the records vanish, the seed and the count remain.
"""
import os
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 150.0
N = int(SR * DUR)
T = np.arange(N) / SR
SEED = 55.0
SCALE = DUR / 700000.0          # rung -> seconds

L = np.zeros(N)
R = np.zeros(N)


def ease(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def window(t0, t1, a=2.0, b=2.0):
    w = ease(np.clip((T - t0) / a, 0.0, 1.0)) * (1.0 - ease(np.clip((T - t1) / b, 0.0, 1.0)))
    return w


def fold(f):
    """octave-fold a frequency into the count's octave [46, 220], never 110."""
    while f < 46.0:
        f *= 2.0
    while f > 220.0:
        f *= 0.5
    return f


# ---------------------------------------------------------------- the data
DATA = "notes/count-strikes-700k.txt"
records = None
strikes = None
if os.path.exists(DATA):
    with open(DATA) as f:
        lines = f.readlines()
    records, strikes = [], []
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
        elif mode == "strikes":
            strikes.extend(map(int, ln.split()))

if records is None:
    records = [(1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
               (230, 964), (330, 2436), (528, 3308), (2764, 4878),
               (4312, 8228), (18287, 24477), (21150, 59599)]
    strikes = [35483, 38837, 41160, 47154, 63038, 94621]

# ---------------------------------------------------------------- the drone
# 55, the seed, mono — the ground the whole piece stands on.
breath = 0.85 + 0.15 * np.sin(2 * np.pi * 0.06 * T)
d = 0.20 * np.sin(2 * np.pi * SEED * T) * breath * window(0.0, DUR, a=3.0, b=6.0)
L += d
R += d

# ------------------------------------------------ the records (stereo, anti)
# the where, the memory — the storm's peaks. mono-deaf.
for r, q in records:
    t0 = r * SCALE
    if t0 >= DUR:
        break
    f = fold(q)
    dur = min(6.0, DUR - t0)
    amp = 0.10 + 0.035 * np.log10(q)     # towers rise
    if q == 55:
        amp *= 1.1                        # the seed speaks
    env = window(t0, t0 + dur, a=0.12, b=dur - 0.12)
    decay = np.exp(-1.8 * np.clip(T - t0, 0.0, None))
    s = amp * np.sin(2 * np.pi * f * T) * env * decay
    s += 0.35 * amp * np.sin(2 * np.pi * 2 * f * T) * env * decay
    L += s
    R -= s                                # anti-phase: stereo-only

# ---------------------------------------------- the count-clock (mono, real)
# the law, the mean — 110 struck at its true positions, what mono hears.
# it begins late and its presence swells as the law asserts itself.
for r in strikes:
    t0 = r * SCALE
    if t0 >= DUR:
        break
    amp = 0.10 + 0.07 * (t0 / DUR)        # the law grows in the ear
    dur = min(1.8, DUR - t0)
    env = window(t0, t0 + dur, a=0.008, b=dur - 0.008)
    decay = np.exp(-2.6 * np.clip(T - t0, 0.0, None))
    s = amp * np.sin(2 * np.pi * 110.0 * T) * env * decay
    s += 0.35 * amp * np.sin(2 * np.pi * 220.0 * T) * env * decay   # the double
    L += s
    R += s                                # mono: survives the fold

# ---------------------------------------------------------------- master
master = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 6.0)
L *= master
R *= master
m_ = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m_
R /= m_
L *= 0.6
R *= 0.6

wav.write("assets/count-clock.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/count-clock.wav  dur={DUR:.1f}s  records={len(records)} strikes={len(strikes)}")
