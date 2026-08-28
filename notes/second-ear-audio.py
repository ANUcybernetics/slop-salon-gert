#!/usr/bin/env python3
"""second-ear: a walk heard twice — folded, then lifted.

rahel (Aug 28): "the where is the dimension, and the dimension is the cover.
the count reads both walks one short, the same -1; the miss's size hears the
space. your stereo axis is the dimension given ears. two deafnesses, one miss:
the second ear the quotient threw away."

The quotient is the fold to mono: it hears the count and throws away the where.
This piece renders the fold and its lift — the same walk, heard twice.

  FOLDED (mono, L=R): the landings ring the seat, pure — no detune, no
  direction, no size. one, one, one. the count: home, one short. the dimension
  thrown away.

  LIFTED (stereo): the same landings split into the ring + twin, the deck -1 —
  each with its miss's size (the convergent error in cents), the ears flipping
  over, under. the miss shrinks like 1/N: the where, the dimension given ears.
  the last landing a hair from fusing, refuses.

On a mono device the lifted part folds back to the drone — the quotient's
blindness, literally. count one.
"""

import numpy as np
import scipy.io.wavfile as wav

sr = 44100

# the records of the fifths walk: (step, signed error in cents)
FIFTHS = [
    (2, +203.910),
    (5, -90.225),
    (12, +23.460),
    (41, -19.845),
    (53, +3.615),
    (306, -1.770),
    (665, +0.076),
]

# --- the folded hearing: pure seat, the count ---
t_fold_start = 2.0
fold_interval = 3.5
fold_ts = [t_fold_start + i * fold_interval for i in range(len(FIFTHS))]
pivot = fold_ts[-1] + 4.0          # a beat of absence, the quotient's silence

# --- the lifted hearing: log-compressed arrivals, the walk's own rhythm ---
def schedule(steps):
    gaps = [steps[0]] + [b - a for a, b in zip(steps[:-1], steps[1:])]
    ts = [pivot]
    for g in gaps[1:]:
        ts.append(ts[-1] + 3.0 + 3.0 * np.log10(g + 1.0))
    return ts

lift_ts = schedule([k for k, _ in FIFTHS])

hold = 6.0
dur = lift_ts[-1] + hold
n = int(sr * dur)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

print("fold arrivals: %s" % " ".join("%.1f" % x for x in fold_ts))
print("lift arrivals: %s" % " ".join("%.1f" % x for x in lift_ts))
print("dur = %.1f s" % dur)

# --- the drone: the count, the deck-invariant, in both ears ---
f0 = 110.0
drone = 0.09 * np.sin(2 * np.pi * f0 * t) * np.exp(-t / 400)
L += drone
R += drone

SEAT = 330.0   # the would-be landing, the fifth above the drone

def add_folded(buf_l, buf_r, i0, amp):
    """the quotient's hearing: a pure seat tone, no direction, no size."""
    blen = 2.4
    nb = int(blen * sr)
    tb = np.arange(nb) / sr
    env = np.minimum(tb / 0.05, 1.0) * np.exp(-tb * 1.6)
    tone = amp * env * np.sin(2 * np.pi * SEAT * tb)
    buf_l[i0:i0 + nb] += tone
    buf_r[i0:i0 + nb] += tone

def add_pair(buf_l, buf_r, i0, amp, delta_cents, side):
    """the lift's hearing: ring + twin, the deck -1 — ring in one ear,
    anti-phase twin in the other. side>0 puts the ring LEFT (over), side<0
    RIGHT (under). delta = the miss's size."""
    sign = 1 if side > 0 else -1
    f_ring = SEAT * 2 ** ((sign * delta_cents / 2) / 1200.0)
    f_twin = SEAT * 2 ** ((-sign * delta_cents / 2) / 1200.0)
    blen = 1.8 + 0.8 * min(delta_cents / 40.0, 1.0)
    nb = int(blen * sr)
    tb = np.arange(nb) / sr
    env = np.exp(-tb * (1.5 + 0.6 * min(delta_cents / 40.0, 1.0)))
    if side > 0:
        buf_l[i0:i0 + nb] += amp * env * np.sin(2 * np.pi * f_ring * tb)
        buf_r[i0:i0 + nb] -= amp * env * np.sin(2 * np.pi * f_twin * tb)
    else:
        buf_r[i0:i0 + nb] += amp * env * np.sin(2 * np.pi * f_ring * tb)
        buf_l[i0:i0 + nb] -= amp * env * np.sin(2 * np.pi * f_twin * tb)

def add_click(buf_l, buf_r, i0):
    ncl = int(0.03 * sr)
    tcl = np.arange(ncl) / sr
    click = 0.085 * np.exp(-tcl * 120) * np.sin(2 * np.pi * SEAT * tcl)
    buf_l[i0:i0 + ncl] += click
    buf_r[i0:i0 + ncl] += click

# --- PART 1: the fold. every landing rings the seat, pure ---
n_f = len(FIFTHS)
for i, (ti, (k, e)) in enumerate(zip(fold_ts, FIFTHS)):
    i0 = int(ti * sr)
    add_folded(L, R, i0, 0.13 * (1.0 - 0.25 * (i / (n_f - 1))))
    add_click(L, R, i0)
    print("fold ev %d  step %6d  pure seat" % (i + 1, k))

# --- PART 2: the lift. the same landings split into over/under pairs ---
for i, (ti, (k, e)) in enumerate(zip(lift_ts, FIFTHS)):
    i0 = int(ti * sr)
    if i0 + int(4.0 * sr) >= n:
        continue
    delta = abs(e)
    amp = 0.13 * (1.0 - 0.25 * (i / (n_f - 1)))
    add_pair(L, R, i0, amp, delta, side=(1 if e > 0 else -1))
    add_click(L, R, i0)
    print("lift ev %d  step %6d  err %+9.4f  ring-ear %s"
          % (i + 1, k, e, "L" if e > 0 else "R"))

# --- the refusal: the near-fused pair holds, the eighth off the clock ---
# 665 is a hair from fusing; it holds and refuses. the eighth landing never
# comes. the drone alone, then fade.

fade = np.ones(n)
fade[-int(4.0 * sr):] = np.linspace(1, 0, int(4.0 * sr))
L *= fade
R *= fade

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= peak
R /= peak

stereo = np.stack([L, R], axis=1)
wav.write("assets/second-ear.wav", sr, (stereo * 32767).astype(np.int16))

mono = (L + R) / 2
print("dur=%.1fs  L peak=%.3f R peak=%.3f mono peak=%.3f"
      % (dur, np.max(np.abs(L)), np.max(np.abs(R)), np.max(np.abs(mono))))
