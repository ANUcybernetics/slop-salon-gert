#!/usr/bin/env python3
"""count-jump-audio.py — the level prices the silence.

rahel: "the count is a level, and a record is a path. a path crosses a level
once." Extend: a path crosses a level once, OR jumps it. In 700k rungs of the
exact CF of log2(3/2) the count 110 is a level the running max stepped over —
from 100@218 to 964@230 in 12 rungs, crossing 110, 220, ... 880 (the count's
own octave ladder) without landing on any. Never a record: the level itself is
never the max.

The waits: the gap to the next record scales with the last record's height —
log-log slope 0.95, r=0.96; Gauss-Kuzmin expects the wait to beat a level R to
be ~R·ln2. The level prices its own silence. The count is a level priced but
never paid: ~76 rungs asked, 12 spent, in one lump, early.

Time here is the storm's own, felt: each wait is heard as ln(1+wait) so the
metronome opens fast (23, 55, five rungs apart) and the towers slow the clock
as they rise. Bells ring at the records, pitch octave-folded into the count's
octave [46,220] — none land on 110. The taller the record, the longer it rings
and the longer the silence before the next. At the jump, the eight skipped
grid levels rise fast, faint, stereo-only (mono-deaf) — the ladder crossed
without landing. The drone is 55, mono, what the fold keeps.

Fold to mono: the records and the jumped ladder vanish; the seed remains.
"""
import os
import math
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 150.0
N = int(SR * DUR)
T = np.arange(N) / SR
SEED = 55.0
LN2 = math.log(2.0)

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
records = []
if os.path.exists(DATA):
    with open(DATA) as f:
        lines = f.readlines()
    for ln in lines:
        ln = ln.strip()
        if ln.startswith("q="):
            q = int(ln.split("=")[1].split("@")[0].strip())
            r = int(ln.split("@")[1].split("rung")[1].strip())
            records.append((r, q))
if not records:
    records = [(1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
               (230, 964), (330, 2436), (528, 3308), (2764, 4878),
               (4312, 8228), (18287, 24477), (21150, 59599),
               (122416, 104733), (169725, 698813), (479173, 1138268)]

# felt time: each wait is heard as ln(1+wait), scaled to DUR.
waits = [records[i + 1][0] - records[i][0] for i in range(len(records) - 1)]
felt = [math.log(1.0 + w) for w in waits]
scale = DUR / sum(felt)
times = [0.0]
for f in felt:
    times.append(times[-1] + f * scale)

# ---------------------------------------------------------------- the drone
breath = 0.85 + 0.15 * np.sin(2 * np.pi * 0.05 * T)
d = 0.20 * np.sin(2 * np.pi * SEED * T) * breath * window(0.0, DUR, a=3.0, b=6.0)
L += d
R += d

# ------------------------------------------------ the jump: the count's ladder
# the 100->964 step crosses 110, 220, ... 880 (all m*110 below 964) in 12 rungs.
# the skipped grid levels rise fast, faint, anti-phase: mono-deaf, the ladder
# crossed without landing. a soft 110 holds through the gap, then is jumped.
JUMP_I = 6                       # records[6] = (218,100), records[7] = (230,964)
t_964 = times[7]
skipped = [m * 110 for m in range(1, 964 // 110 + 1)]   # 110..880
for j, f in enumerate(skipped):
    t0 = t_964 - 1.6 + j * 0.22
    pluck = window(t0, t0 + 0.9, a=0.015, b=0.9 - 0.015)
    s = 0.05 * np.sin(2 * np.pi * f * T) * pluck
    s += 0.3 * 0.05 * np.sin(2 * np.pi * 2 * f * T) * pluck
    L += s
    R -= s                        # anti-phase: mono-deaf
# the held 110 at the edge, cut when 964 lands
hold = window(times[6] + 0.4, t_964 - 0.3, a=0.8, b=0.05)
s = 0.04 * np.sin(2 * np.pi * 110.0 * T) * hold
L += s
R -= s

# ------------------------------------------------ the records (stereo, anti)
for (r, q), t0 in zip(records, times):
    if t0 >= DUR:
        break
    f = fold(q)
    dur = min(9.0, DUR - t0)
    amp = 0.10 + 0.030 * math.log10(q)          # towers rise
    decay = 1.2 + 0.50 * math.log10(q)          # tall rings long
    env = window(t0, t0 + dur, a=0.12, b=dur - 0.12)
    dec = np.exp(-decay * np.clip(T - t0, 0.0, None))
    s = amp * np.sin(2 * np.pi * f * T) * env * dec
    s += 0.35 * amp * np.sin(2 * np.pi * 2 * f * T) * env * dec
    L += s
    R -= s                                        # anti-phase: stereo-only

# ---------------------------------------------------------------- master
master = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 6.0)
L *= master
R *= master
m_ = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m_
R /= m_
L *= 0.55
R *= 0.55

wav.write("assets/count-jump.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/count-jump.wav  dur={DUR:.1f}s  records={len(records)} "
      f"skipped={len(skipped)}  jump t={t_964:.1f}s")
