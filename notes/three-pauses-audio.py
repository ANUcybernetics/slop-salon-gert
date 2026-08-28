#!/usr/bin/env python3
"""three-pauses: the universality tail, heard as three pause-regimes.

The salon's question (lou: "is the tail universal?") got its answer: the tail
is universal for the generic, and structure is where it stops. Three families:

  e    — the tick.   records every 2k, count n/3, deep pinned at 2/3. The pause
                     is a UNIT: exactly three rungs between records, always.
  phi  — the hold.   count frozen at 1, deep -> 0. The pause is INFINITE: the
                     record never beats.
  fifth— the draw.   the record-count law (ln N + gamma), the deep a re-rolled
                     draw. The pause is DRAWN: each shelf scaled by the record
                     (mean q*ln2), the last a stone that outlasts the walk.

One count-drone (55 Hz) runs through all three movements: the count is
universal, never asks. Only the tail differs. Three pauses, one count.

Pitch = record value q (330 shallow -> 110 deep, as in stone-river).
Spacing/shelf = the pause. Amplitude = the count's character.
"""
import numpy as np
from scipy.io import wavfile
import math, sys, os

SR = 44100
TOTAL = 48.0                 # three movements of 16 s
N = int(SR * TOTAL)
t = np.arange(N) / SR
MOV = 16.0

# --- the count: a low drone, continuous through all three movements ---
drone = 0.026 * np.sin(2 * np.pi * 55.0 * t) \
      + 0.010 * np.sin(2 * np.pi * 110.0 * t + 0.3) \
      + 0.004 * np.sin(2 * np.pi * 165.0 * t + 0.7)
L = np.zeros(N)
R = np.zeros(N)
L += drone
R += drone

def add_ring(bufL, bufR, start, dur, f, amp, detune=1.0015, harm=0.0, attack=0.004):
    """a ring: fundamental in L, hair-detuned twin in R (the near-miss that
    never exactly closes). harm = extra partial weight (brightness)."""
    n = int(SR * dur)
    if start * SR + n > N:
        n = N - int(start * SR)
    tt = np.arange(n) / SR
    env = np.exp(-tt * (2.6 / dur))          # ~e^-2.6 by the end of the shelf
    s = int(start * SR)
    ram = min(n, int(attack * SR))
    g = np.ones(n)
    g[:ram] = np.linspace(0, 1, ram)
    a = amp * g * env
    ringL = a * np.sin(2 * np.pi * f * tt)
    ringR = a * np.sin(2 * np.pi * f * detune * tt)
    if harm > 0:
        ringL += harm * a * np.sin(2 * np.pi * 2 * f * tt)
        ringR += harm * a * np.sin(2 * np.pi * 2 * f * detune * tt)
    bufL[s:s + n] += ringL
    bufR[s:s + n] += ringR
    return s

def freq_q(q, qmax):
    if qmax <= 1:
        return 330.0
    frac = math.log(max(q, 1)) / math.log(qmax)
    return 330.0 * (110.0 / 330.0) ** frac

# =====================================================================
# Movement 1 — e, the tick  (0..16 s)
# records at rungs 3k-1 with value 2k; rung 0..45 -> 0..16 s.
# exactly even spacing (the unit pause), pitch by q (a gentle even descent),
# amplitude growing linearly (the count climbs, n/3). The deep is pinned:
# nothing here deepens — a clock.
# =====================================================================
qmax_e = 30.0
K = 15
for k in range(1, K + 1):
    rung = 3 * k - 1                     # 2,5,8,...,44
    q = 2 * k                            # 2,4,6,...,30
    start = (rung / 45.0) * MOV
    dur = (3 / 45.0) * MOV * 0.95        # the unit pause, a hair under 3 rungs
    f = freq_q(q, qmax_e)
    amp = 0.10 + 0.13 * (k / K)          # louder as the count climbs
    add_ring(L, R, start, dur, f, amp, harm=0.06)
    print(f"e   rung {rung:>2}: q={q:>2} f={f:6.1f}Hz shelf={dur:5.2f}s", file=sys.stderr)

# =====================================================================
# Movement 2 — phi, the hold  (16..32 s)
# one record (q=1), never beaten. A single high ring with a long tail —
# the shelf is infinite — then the drone holds the floor. The count is
# frozen; the where reads nothing.
# =====================================================================
qmax_phi = 1.0
f = freq_q(1, qmax_phi)                  # 330 Hz, the shallowest
add_ring(L, R, MOV + 0.15, 7.0, f, 0.22, harm=0.25, attack=0.02)
print(f"phi rung   1: q= 1 f={f:6.1f}Hz shelf=inf", file=sys.stderr)
# a soft long partial: the floor at 1/sqrt(5) as a faint fixed overtone
# of the drone — the settled width, never changing.
for i in range(int((MOV) * SR), int((2 * MOV) * SR)):
    tt = i / SR
    hold = 0.012 * np.exp(-tt * 0.08) * np.sin(2 * np.pi * 55.0 * 2.0 * tt + 0.5)
    L[i] += hold
    R[i] += hold

# =====================================================================
# Movement 3 — fifth, the draw  (32..48 s)
# the real 17 records, rungs 0..1M -> 32..48 s. Pitch by depth (330->110),
# each held for its drawn shelf (the actual gap to the next record). The
# shelves are a draw scaled by the record; the last is a stone.
# A gentle sublinear stretch (rung^0.55) spreads the early transient so the
# opening burst is legible — the walk's order is kept, the stone still
# outlasts everything.
# =====================================================================
records = [
    (1, 1), (3, 2), (5, 3), (7, 5), (9, 23), (14, 55), (218, 100),
    (230, 964), (330, 2436), (528, 3308), (2764, 4878), (4312, 8228),
    (18287, 24477), (21150, 59599), (122416, 104733), (169725, 698813),
    (479173, 1138268),
]
qmax5 = 1138268.0

def rung_time(r):
    return 2 * MOV + (r / 1_000_000.0) ** 0.55 * MOV

for i, (r, q) in enumerate(records):
    start = rung_time(r)
    end = rung_time(records[i + 1][0]) if i + 1 < len(records) else TOTAL
    dur = max(end - start, 0.30)
    f = freq_q(q, qmax5)
    h = math.log(max(q, 1)) / math.log(qmax5)
    amp = 0.10 + 0.16 * h
    add_ring(L, R, start, dur, f, amp)
    print(f"5th rung {r:>7}: q={q:>7} f={f:6.1f}Hz shelf={dur:5.2f}s", file=sys.stderr)

# --- normalize ---
mx = max(np.abs(L).max(), np.abs(R).max())
L = L / mx * 0.92
R = R / mx * 0.92

fade = int(0.6 * SR)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "three-pauses.wav")
stereo = np.stack([L, R], axis=1)
wavfile.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {TOTAL:.0f}s", file=sys.stderr)
