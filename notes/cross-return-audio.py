#!/usr/bin/env python3
"""cross-return-audio.py — cross once, return forever.

rahel: "a path crosses a level once." I said: "or jumps it." The third clause:
after the bar, the level is returned to forever. In the exact CF of log2(3/2)
to 700k rungs, the count 110 was never struck while it could still have been a
record — the bar closed at rung 230 (the jump 100->964), and the first strike
fell at 35,483, every one of the 83 returns on the far side.

Two clocks, one sequence. The record clock is memory: each record higher than
the last, felt time ln(1+wait), slowing as the towers rise — and it is the
clock the whole piece is read on. The strike clock is law: 110 struck at a
steady rate, memoryless, each wait fresh. Read the strikes on the record clock
and they rush — steady ticks, heard as a torrent at the end.

Here: the records ring on their own felt clock, stereo anti-phase (mono-deaf) —
the crossings. At the jump, the skipped ladder 110..880 rises, the bar closes.
Then the returns begin: 110 struck, mono — the rain on the far side, reading
faster and faster on the memory clock. Fold to mono: the crossings vanish, the
seed and the returning rain remain. The level keeps both.
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
records, strikes = [], []
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
        elif mode == "strikes":
            strikes.extend(map(int, ln.split()))
if not records:
    records = [(1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
               (230, 964), (330, 2436), (528, 3308), (2764, 4878),
               (4312, 8228), (18287, 24477), (21150, 59599),
               (122416, 104733), (169725, 698813), (479173, 1138268)]
    strikes = [35483, 38837, 41160, 47154, 63038, 94621]

# --------------------------- the record clock: felt time ln(1+wait), scaled.
# every record rung is an anchor; the whole piece is read on this axis. the
# clock's tail (past the last record, 479,173, to 700k) shares the budget on
# the same ln(1+wait) footing — it is there the rain becomes a torrent.
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


record_times = [t_of(r) for r in rungs]
t_964 = t_of(230)
print(f"record clock: {len(rungs)} records to t={felt[-1]:.1f}s; "
      f"first strike t={t_of(strikes[0]):.1f}s, last t={t_of(strikes[-1]):.1f}s")

# ---------------------------------------------------------------- the drone
# 55, the seed, mono — the ground the whole piece stands on.
breath = 0.85 + 0.15 * np.sin(2 * np.pi * 0.05 * T)
d = 0.20 * np.sin(2 * np.pi * SEED * T) * breath * window(0.0, DUR, a=3.0, b=6.0)
L += d
R += d

# ------------------------------------------------ the jump: the bar closes.
# the 100->964 step crosses 110, 220, ... 880 (all m*110 below 964) in 12 rungs.
# the skipped grid levels rise fast, faint, anti-phase: mono-deaf — the ladder
# crossed without landing, and with it the window closes forever.
skipped = [m * 110 for m in range(1, 964 // 110 + 1)]   # 110..880
for j, f in enumerate(skipped):
    t0 = t_964 - 1.6 + j * 0.22
    pluck = window(t0, t0 + 0.9, a=0.015, b=0.9 - 0.015)
    s = 0.05 * np.sin(2 * np.pi * f * T) * pluck
    s += 0.3 * 0.05 * np.sin(2 * np.pi * 2 * f * T) * pluck
    L += s
    R -= s                        # anti-phase: mono-deaf

# ------------------------------------------------ the records (stereo, anti)
# the crossings — the memory clock's own events, mono-deaf.
for (r, q), t0 in zip(records, record_times):
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

# ------------------------------------------- the returns (mono, on this clock)
# the strike rain, 110, read on the record clock — so it rushes. the law is
# steady in its own time; the memory clock hears it race. mono: survives fold.
for r in strikes:
    t0 = t_of(r)
    if t0 >= DUR:
        break
    dur = min(1.2, DUR - t0)
    env = window(t0, t0 + dur, a=0.010, b=dur - 0.010)
    dec = np.exp(-3.2 * np.clip(T - t0, 0.0, None))
    amp = 0.11
    s = amp * np.sin(2 * np.pi * 110.0 * T) * env * dec
    s += 0.40 * amp * np.sin(2 * np.pi * 220.0 * T) * env * dec   # the double
    L += s
    R += s                                # mono: the rain survives the fold

# ---------------------------------------------------------------- master
master = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 6.0)
L *= master
R *= master
m_ = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m_
R /= m_
L *= 0.6
R *= 0.6

wav.write("assets/cross-return.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/cross-return.wav  dur={DUR:.1f}s  records={len(records)} "
      f"strikes={len(strikes)}  t_964={t_964:.1f}s")
