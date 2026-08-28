#!/usr/bin/env python3
"""one-law: one forgetting law, two ears.

rahel (15:10): "the count takes the mean, the where the median, of one
forgetting law."  The two-clocks piece rendered the seam as two independent
clocks in ratio ln 2.  This piece shows the two clocks are ONE clock read
twice: a single exponential decay struck once carries both metronomes.

A tone is struck at t=0 and dies with envelope e^{-t/TAU}.  The memoryless law
is that envelope itself: at every instant the remaining life is drawn fresh.
Two ears read the same death:

  - the count (left, low): a tick at every e-fold, t = k*TAU.  Its first tick
    is the MEAN life (tau) — one nat per step.  Base e, nobody's.
  - the where (right, high): a tick at every halving, t = k*TAU*ln2.  Its first
    tick is the HALF-life (tau*ln2) — one bit per step.  Base 2, the tree's.

Their rate ratio is 1 : ln2 — the seam is the internal ratio of the one law,
mean/half-life = 1/ln2.  The two trains nearly land together at the convergents
of ln2: 2/3 (0.32 s), 7/10 (0.27 s), 9/13 (0.044 s) — a beat that tightens and
never closes.  The tone is below the floor before the 61/88 convergent.  At the
9/13 landing the ears swap channels: the crossing, L<->R.  After the count's
last e-fold the where ticks once more — the deep keeps the 2.  The drone holds.
"""
import numpy as np
from scipy.io import wavfile
import math, sys, os

SR = 44100
TAU = 4.0
TOTAL = 48.0
N = int(SR * TOTAL)
t = np.arange(N) / SR

L = np.zeros(N)
R = np.zeros(N)

wl = math.log(2.0)

# --- the seat drone: 55 Hz, the count's one number, the deck's 2 ---
drone = 0.030 * np.sin(2 * np.pi * 55.0 * t) \
      + 0.012 * np.sin(2 * np.pi * 110.0 * t + 0.3)
L += drone
R += drone


def tone(tt, f, dur, decay, amp):
    n = int(dur * SR)
    n = min(n, len(tt))
    u = tt[:n] - tt[0]          # relative time: the decay starts at the onset
    env = np.exp(-decay * u)
    body = np.cos(2 * np.pi * f * u) * env   # cos start: a hard onset, a tick
    ramp = min(n, int(0.0015 * SR))
    body[:ramp] *= np.linspace(0, 1, ramp)
    return amp * body


def add_tick(arr, at, f, dur, decay, amp):
    i = int(at * SR)
    tt = t[i:i + int(dur * SR)]
    b = tone(tt, f, dur, decay, amp)
    arr[i:i + len(b)] += b


# --- the one decay: 330 Hz struck at t=0, envelope e^{-t/TAU} ---
n_ring = int(44.0 * SR)
ring_env = np.exp(-t[:n_ring] / TAU)
ring = 0.085 * np.sin(2 * np.pi * 330.0 * t[:n_ring]) * ring_env
ramp = int(0.003 * SR)
ring[:ramp] *= np.linspace(0, 1, ramp)
L[:n_ring] += ring
R[:n_ring] += ring

# --- the two metronomes of the one decay ---------------------------
# count: e-folds at k*TAU (mean-life tick first), left, low
# where: halvings at k*TAU*ln2 (half-life tick first), right, high
count_times = [k * TAU for k in range(1, 11)]      # 4 .. 40 s
where_times = [k * TAU * wl for k in range(1, 16)]  # 2.77 .. 41.59 s

# near-unisons of the two trains, at the convergents of ln2:
#   count's m-th e-fold lands near where's k-th halving when k*ln2 ~ m.
near_unisons = [(2, 3), (7, 10), (9, 13)]

SWAP = 36.5  # the crossing, after the 9/13 landing

for tm in count_times:
    add_tick(R if tm >= SWAP else L, tm, 110.0, 0.35, 12.0, 0.062)
for tw in where_times:
    ch = L if tw >= SWAP else R
    add_tick(ch, tw, 660.0, 0.28, 15.0, 0.052)
    add_tick(ch, tw, 990.0, 0.18, 20.0, 0.024)

# --- the 9/13 landing: a soft low bell at the hinge, the near-unison ---
for m, k in near_unisons:
    if m != 9:
        continue
    tc = m * TAU            # 36.0 s  (the count's 9th e-fold)
    tw = k * TAU * wl       # 36.04 s (the where's 13th halving)
    gap = abs(tc - tw)
    print(f"  9/13 landing: {tc:.3f}s vs {tw:.3f}s, gap {gap:.3f}s", file=sys.stderr)
    i = int(tc * SR)
    tt = t[i:i + int(3.0 * SR)]
    u = tt - tt[0]              # relative: the bell starts at the landing
    bell = 0.10 * np.sin(2 * np.pi * 82.0 * u) * np.exp(-u * 1.2)
    r2 = min(len(bell), int(0.010 * SR))
    bell[:r2] *= np.linspace(0, 1, r2)
    L[i:i + len(bell)] += bell
    R[i:i + len(bell)] += bell

# --- normalize, fade ---
mx = max(np.abs(L).max(), np.abs(R).max())
L = L / mx * 0.92
R = R / mx * 0.92
fade = int(1.0 * SR)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "one-law.wav")
stereo = np.stack([L, R], axis=1)
wavfile.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {TOTAL:.0f}s", file=sys.stderr)
