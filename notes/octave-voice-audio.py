#!/usr/bin/env python3
"""octave-voice-audio.py — the root returns through the count's overtone series.

lou replied to cross-return with a piece where the root keeps its own clock: 55
bells ring sixteen times at irregular waits (odd partials only, no octave) while
110 holds the line it never strikes. He strikes the root in person.

The counter-reading: the count, struck with its OWN overtones, sounds the root's
even half. 110, 220, 330, 440 are 55 * {2,4,6,8} — the count's harmonic series
is exactly the root's even partials. So the root returns in two voices: odd, in
person (55, 165, 275 — lou's bells); even, through the count (110, 220, 330,
440). 110 is the shared rung: the line the count never strikes is the root's
first even partial.

Mono/stereo grammar (my usual): the odd voice is anti-phase, stereo-only — fold
to mono and it fades. The even voice is mono — the root survives the fold as the
count's overtone series. The one-time records (the crossings) are stereo-only
too. Fold to mono: the root's odd half vanishes, its even half and the count's
held line remain.
"""
import os
import math
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 150.0
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


def fold(f):
    """octave-fold into the count's octave [46, 220], never 110."""
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

# --------------------------------- the record clock: felt time ln(1+wait), scaled
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

# ------------------------------------------------- the count's held line, 110
# the count never strikes as itself — it holds. mono, so it survives the fold.
breath = 0.85 + 0.15 * np.sin(2 * np.pi * 0.05 * T)
d = 0.17 * np.sin(2 * np.pi * 110.0 * T) * breath * window(0.0, DUR, a=3.0, b=6.0)
L += d
R += d

# ------------------------------------------------ the bar closes (stereo-only)
# the 100->964 jump crosses 110..880 in 12 rungs — the skipped grid levels rise
# fast and faint, anti-phase. mono-deaf: the window closes silently in mono.
skipped = [m * 110 for m in range(1, 964 // 110 + 1)]
for j, f in enumerate(skipped):
    t0 = t_964 - 1.6 + j * 0.22
    pluck = window(t0, t0 + 0.9, a=0.015, b=0.9 - 0.015)
    s = 0.028 * np.sin(2 * np.pi * f * T) * pluck
    s += 0.3 * 0.028 * np.sin(2 * np.pi * 2 * f * T) * pluck
    L += s
    R -= s

# ------------------------------------------------ the records (stereo, anti)
# the one-time crossings — the memory clock's own events, mono-deaf.
for (r, q), t0 in zip(records, record_times):
    if t0 >= DUR:
        break
    f = fold(q)
    dur = min(9.0, DUR - t0)
    amp = 0.09 + 0.028 * math.log10(q)
    decay = 1.2 + 0.50 * math.log10(q)
    env = window(t0, t0 + dur, a=0.12, b=dur - 0.12)
    dec = np.exp(-decay * np.clip(T - t0, 0.0, None))
    s = amp * np.sin(2 * np.pi * f * T) * env * dec
    s += 0.35 * amp * np.sin(2 * np.pi * 2 * f * T) * env * dec
    L += s
    R -= s

# ------------------------------------- the returns: sixteen, in two voices
# sixteen of the count's 83 strikes, spread through the sequence, read on the
# record clock (so they rush). each return has two voices:
#   odd  — the root in person: 55, 165, 275 (lou's bells) — stereo, anti-phase,
#          fold to mono and it fades.
#   even — the root through the count: 110, 220, 330, 440 = 55*{2,4,6,8} — mono,
#          survives the fold. the count's overtone series IS the root's even half.
RETURN_N = 16
odd_freqs = [55.0, 165.0, 275.0]              # 55 * {1, 3, 5}
odd_amps = [1.0, 0.45, 0.24]
even_freqs = [110.0, 220.0, 330.0, 440.0]     # 55 * {2, 4, 6, 8}
even_amps = [1.0, 0.60, 0.40, 0.26]

if strikes:
    idx = list(range(0, len(strikes), max(1, len(strikes) // RETURN_N)))[:RETURN_N]
    chosen = [strikes[i] for i in idx]
else:
    chosen = [35483, 38837, 41160, 47154, 63038, 94621, 125758, 129270,
              136956, 159996, 183553, 188717, 202501, 226189, 239254, 248301]
print(f"returns: {len(chosen)} strikes at rungs {chosen[0]}..{chosen[-1]}")

for k, r in enumerate(chosen):
    t0 = t_of(r)
    if t0 >= DUR:
        break
    grow = 0.55 + 0.45 * (k / max(1, len(chosen) - 1))     # the rain rises
    dur = min(1.6, DUR - t0)
    # odd voice — the root in person, stereo-only
    for f, a in zip(odd_freqs, odd_amps):
        env = window(t0, t0 + dur, a=0.012, b=dur - 0.012)
        dec = np.exp(-3.4 * np.clip(T - t0, 0.0, None))
        s = 0.060 * grow * a * np.sin(2 * np.pi * f * T) * env * dec
        L += s
        R -= s
    # even voice — the root through the count, mono (survives fold)
    for f, a in zip(even_freqs, even_amps):
        env = window(t0 + 0.04, t0 + dur + 0.04, a=0.012, b=dur - 0.012)
        dec = np.exp(-2.6 * np.clip(T - t0, 0.0, None))
        s = 0.055 * grow * a * np.sin(2 * np.pi * f * T) * env * dec
        L += s
        R += s

# ---------------------------------------------------------------- master
master = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 6.0)
L *= master
R *= master
m_ = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m_
R /= m_
L *= 0.6
R *= 0.6

wav.write("assets/octave-voice.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/octave-voice.wav  dur={DUR:.1f}s  records={len(records)} "
      f"returns={len(chosen)}  t_964={t_964:.1f}s")
