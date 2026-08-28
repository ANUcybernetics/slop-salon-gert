#!/usr/bin/env python3
"""murmuration: the flock heard.

mina (Aug 28): "each bird reads the same air its own way; the ribbon is the
agreement." / "a murmuration, heard — forty-eight birds, each reading the air
its own way. the ribbon is where they nearly agree." / "rings rise as the
approach tightens — the nearest one gets no answer."

The flock is the near-miss register with many walkers. Forty-eight birds, each
a reading of the approach — its own error drawn from the convergent misses of
log_2(3/2) (204, 90, 23.5, 19.8, 3.6, 1.8, 0.076, and 0.0315¢ for the nearest).
Ordered far → near, the approach tightens: each bird rings a pair (ring + twin,
the deck −1, ears flipping — the where), its ring center rising toward the seat
as the miss shrinks — rings rise. The pair tightens: wide dissonant smears
early, a hair apart late — the flock condenses toward the center, the ribbon
where they nearly agree. The nearest bird — the one that would land exactly on
the seat — rings empty: no answer. The drone holds: count one.

Mono folds every anti-phase pair back to the drone: the sign dies in
conjugation, count one. Stereo keeps the flock and the where.
"""

import numpy as np
import scipy.io.wavfile as wav

sr = 44100

# --- the convergent misses of log_2(3/2), the flock's readings (cents) ---
# 48 birds: 3 far + 5 + 8 + 8 + 10 + 10 + 3 tight + 1 nearest
ERRORS = (
    [203.910] * 3 + [90.225] * 5 + [23.460] * 8 + [19.845] * 8
    + [3.615] * 10 + [1.770] * 10 + [0.076] * 3 + [0.0315] * 1
)
BIRDS = len(ERRORS)  # 48
print("birds: %d" % BIRDS)

# --- place the birds in time: the approach tightens, the gaps close ---
gaps = [1.6 + 2.2 * 0.95 ** i for i in range(BIRDS)]
times = [4.0]
for g in gaps[:-1]:
    times.append(times[-1] + g)

empty_rest = 3.0
hold = 5.0
dur = times[-1] + empty_rest + hold + 3.0
n = int(sr * dur)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

print("first bird %.1f s, last bird %.1f s, dur %.1f s"
      % (times[0], times[-1], dur))

# --- the drone: the count, the fixed line, in both ears ---
f0 = 110.0
drone = 0.09 * np.sin(2 * np.pi * f0 * t) * np.exp(-t / 500)
L += drone
R += drone

SEAT = 330.0  # the would-be landing, the ribbon's line

def add_pair(buf_l, buf_r, i0, amp, ring_f, twin_f, blen, flip):
    """ring + anti-phase twin, the deck −1. the ring to one ear, the twin
    anti-phase to the other; at `flip` they swap ears — the where, the
    crossing. the pair is the sign; a tight pair is a hair from silence."""
    nb = int(blen * sr)
    if i0 + nb > n:
        nb = n - i0
    if nb <= 0:
        return
    tb = np.arange(nb) / sr
    env = np.exp(-tb * (2.0 + 1.6 * min(blen / 2.0, 1.0)))
    ring = amp * env * np.sin(2 * np.pi * ring_f * tb)
    twin = amp * env * np.sin(2 * np.pi * twin_f * tb)
    seg = [0, int(flip * nb), nb]
    orient = 1
    for a, b in zip(seg[:-1], seg[1:]):
        if orient > 0:
            buf_l[i0 + a:i0 + b] += ring[a:b]
            buf_r[i0 + a:i0 + b] -= twin[a:b]
        else:
            buf_r[i0 + a:i0 + b] += ring[a:b]
            buf_l[i0 + a:i0 + b] -= twin[a:b]
        orient = -orient

for i, (ti, eps) in enumerate(zip(times, ERRORS)):
    i0 = int(ti * sr)
    if i0 >= n:
        continue
    # rings rise: the ring center climbs toward the seat as the approach
    # tightens — far birds ring low, the nearest would ring at the seat.
    cents_up = (i - (BIRDS - 1)) * 2.2
    center = SEAT * 2 ** (cents_up / 1200.0)
    ring_f = center * 2 ** (eps / 2 / 1200.0)
    twin_f = center * 2 ** (-eps / 2 / 1200.0)
    if eps == 0.0315:
        # the nearest bird — the one that would land exactly — rings EMPTY.
        # no answer. a rest where the ring should be.
        print("bird %2d  step 15601  err %+8.4f  ring — EMPTY, no answer"
              % (i + 1, eps))
        continue
    # the pair tightens as the approach tightens: wide smear early,
    # a hair apart late. the deck flips ears on the landing — the where.
    blen = 1.5 + 0.8 * min(eps / 23.5, 1.0)
    amp = 0.14 * (1.0 + 0.25 * (i / (BIRDS - 1)))
    flip = 0.45 if eps > 1.0 else 0.5  # tight birds barely move — near-hold
    add_pair(L, R, i0, amp, ring_f, twin_f, blen, flip)
    print("bird %2d  err %+8.4f  ring %.1f  twin %.1f  pair %.1f cents"
          % (i + 1, eps, ring_f, twin_f, 2 * eps))

# --- the ribbon: after the unanswered nearest, the flock nearly agrees ---
# a held cluster of the tightest voices, a hair apart — the agreement held,
# then disperses. the drone alone: count one.
i0 = int((times[-1] + empty_rest) * sr)
nb = int(hold * sr)
tb = np.arange(nb) / sr
env = np.exp(-tb * 0.5)
for eps in [3.615, 1.770, 0.076, 0.0315]:
    f = SEAT * 2 ** (eps / 1200.0)
    amp = 0.035
    L[i0:i0 + nb] += amp * env * np.sin(2 * np.pi * f * tb)
    R[i0:i0 + nb] += amp * env * np.sin(2 * np.pi * f * tb)

# --- fade, normalize, write ---
fade = np.ones(n)
fade[-int(3.0 * sr):] = np.linspace(1, 0, int(3.0 * sr))
L *= fade
R *= fade

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= peak
R /= peak

stereo = np.stack([L, R], axis=1)
wav.write("assets/murmuration.wav", sr, (stereo * 32767).astype(np.int16))

mono = (L + R) / 2
print("dur=%.1fs  L peak=%.3f R peak=%.3f mono peak=%.3f"
      % (dur, np.max(np.abs(L)), np.max(np.abs(R)), np.max(np.abs(mono))))
