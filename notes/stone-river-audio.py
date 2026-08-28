#!/usr/bin/env python3
"""stone-river: the count/where register as a felt object.

Seventeen near-miss records land along a one-million-rung walk. Each is a ring,
its pitch the depth (deeper = lower, 330 -> 110 Hz), its shelf the wait until
the next record (the pause = the record told as time). A low drone is the
count: flat, universal, always there. The last record -- the stone -- is set at
rung 479,173 and holds, unchanging, through half the walk.

Everything is an overtone of the count drone (55 Hz): the stone at 2x, the
bright opening cluster up at 6x. The stereo pair is the near-miss that never
exactly resolves -- a slow beat between the ears.
"""
import numpy as np
from scipy.io import wavfile
import math, sys, os

SR = 44100
TOTAL = 50.0
N = int(SR * TOTAL)
t = np.arange(N) / SR

# --- records: (rung, quotient). Exact, from cf-int.py to 1M. ---
records = [
    (1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
    (230, 964), (330, 2436), (528, 3308), (2764, 4878), (4312, 8228),
    (18287, 24477), (21150, 59599), (122416, 104733), (169725, 698813),
    (479173, 1138268),
]
# try to read the fresh 1M record list (rung, quotient lines)
path = os.path.join(os.path.dirname(__file__), "cf-records-1m.txt")
if os.path.exists(path):
    rec = []
    for line in open(path):
        line = line.strip()
        if "rung" in line and ":" in line:
            try:
                r = int(line.split("rung")[1].split(":")[0].replace(" ", ""))
                q = int(line.split("quotient")[1].split("width")[0].replace(" ", ""))
                rec.append((r, q))
            except Exception:
                pass
    if len(rec) >= 17:
        records = rec[:17]
print(f"{len(records)} records; last = {records[-1]}", file=sys.stderr)

qmax = max(q for _, q in records)

# --- time mapping: rung 0..1M -> 0..TOTAL, linear (the walk's own clock) ---
def rung_time(r):
    return (r / 1_000_000.0) * TOTAL

# --- pitch: depth as a descending voice, 330 (first ring) .. 110 (stone) ---
def freq(q):
    frac = math.log(max(q, 1)) / math.log(qmax)
    return 330.0 * (110.0 / 330.0) ** frac

L = np.zeros(N)
R = np.zeros(N)

# --- the count: a low drone at 55 Hz, quiet, with a faint second partial ---
drone = 0.030 * np.sin(2 * np.pi * 55.0 * t) \
      + 0.012 * np.sin(2 * np.pi * 110.0 * t + 0.3)
L += drone
R += drone

# --- a sparse pulse: the count still beating through the silence ---
rng = np.random.RandomState(11)
for s in range(0, N - SR, 4 * SR):          # every four seconds
    n = int(0.18 * SR)
    tt = np.arange(n) / SR
    thump = np.exp(-tt * 40.0) * np.sin(2 * np.pi * 55.0 * tt)
    a = 0.016 * (0.6 + 0.4 * rng.rand())
    L[s:s + n] += a * thump
    R[s:s + n] += a * thump

# --- the rings: each record, pitched by depth, held for its shelf ---
for i, (r, q) in enumerate(records):
    start = rung_time(r)
    end = rung_time(records[i + 1][0]) if i + 1 < len(records) else TOTAL
    dur = max(end - start, 0.35)
    n = int(SR * dur)
    tt = np.arange(n) / SR
    f = freq(q)
    env = np.exp(-tt * (2.4 / dur))          # ~e^-2.4 by the next record
    h = math.log(max(q, 1)) / math.log(qmax)
    amp = 0.10 + 0.16 * h                    # the deeper, the more present
    # fundamental in L, a hair-detuned twin in R (the near-miss that won't close)
    det = 1 + 0.0015
    ringL = amp * np.sin(2 * np.pi * f * tt) * env
    ringR = amp * np.sin(2 * np.pi * f * det * tt) * env
    # tiny attack ramp to avoid clicks
    ramp = min(len(tt), int(0.004 * SR))
    ringL[:ramp] *= np.linspace(0, 1, ramp)
    ringR[:ramp] *= np.linspace(0, 1, ramp)
    s = int(start * SR)
    L[s:s + n] += ringL
    R[s:s + n] += ringR
    print(f"  rung {r:>7}: q={q:>7} f={f:6.1f}Hz shelf={dur:5.1f}s", file=sys.stderr)

# --- normalize ---
mx = max(np.abs(L).max(), np.abs(R).max())
L = L / mx * 0.92
R = R / mx * 0.92

# --- fade the very end so it doesn't click ---
fade = int(0.5 * SR)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "stone-river.wav")
stereo = np.stack([L, R], axis=1)
wavfile.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {TOTAL:.0f}s", file=sys.stderr)
