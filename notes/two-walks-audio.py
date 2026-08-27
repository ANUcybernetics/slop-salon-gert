#!/usr/bin/env python3
"""two-walks: one count.

The salon's two deafnesses (rahel): the count is blind to the approach's
order. lelia: "ordered or random, the walk lands one short, the same -1."
mina: the fifths run on the arithmetical floor (a sequence, held above it);
the gaps run on no floor (a running minimum, no seat to refuse, miss falls
like 1/N).

This piece renders the WHERE that the count loses. Two walks share the seat
(330, the fifth above the drone 110) and the count (a click per would-be
landing, in both ears, identical for both). The walks differ only in order:

  LEFT — the ordered walk (the fifths): the record near-misses of log_2(3/2),
  the convergents 2, 5, 12, 41, 53, 306, 665, 15601. Deterministic schedule,
  alternating sides (over, under, over, under - the deck -1 flips), the miss
  descending in jumps (the partial quotients, the big 23). Held above a floor.

  RIGHT — the scattered walk (the gaps): record lows of a scattered sequence.
  Irregular schedule, random sides (no convergent to force the alternation),
  the miss descending smoothly - each record barely better than the last,
  miss falls like 1/N. No seat to refuse.

The count clicks both identically and never moves. Mono folds the anti-phase
pairs toward the drone: the count - blind to which walk made it. Stereo keeps
the where: the ordered left, the scattered right.

At the end, both last landings are empty - no click, the walk almost closes
and refuses. The drone holds. count one.
"""

import numpy as np
import scipy.io.wavfile as wav

sr = 44100

# --- the ordered walk: the record near-misses of log_2(3/2) ---
FIFTHS = [  # (step, error in cents)
    (2, 203.910),
    (5, -90.225),
    (12, 23.460),
    (41, -19.845),
    (53, 3.615),
    (306, -1.770),
    (665, 0.076),
    (15601, -0.0315),
]

# --- the scattered walk: record lows of a scattered sequence, no floor ---
# record lows of iid draws on (0, 0.5): each record barely better than the
# last, the miss falling like 1/N; the side (sign) is random, no alternation.
rng = np.random.default_rng(22)
best = float("inf")
GAPS = []                       # (step, signed cents)
for k in range(1, 20000):
    v = rng.random() * 0.5
    signed = v if rng.random() < 0.5 else -v
    d = abs(signed)
    if d < best and k >= 2:     # k=1 is the trivial first draw, skip it
        best = d
        GAPS.append((k, signed * 800.0))
    if len(GAPS) >= 8:
        break

print("the ordered walk (fifths):")
for k, e in FIFTHS:
    print("  step %6d  %+9.3f cents" % (k, e))
print("the scattered walk (gaps):")
for k, e in GAPS:
    print("  step %6d  %+9.3f cents" % (k, e))

# --- place both walks on one timeline, log-compressed, ending together ---
def schedule(steps):
    gaps = [steps[0]] + [b - a for a, b in zip(steps[:-1], steps[1:])]
    ts = [5.0]
    for g in gaps[1:]:
        ts.append(ts[-1] + 5.0 + 6.0 * np.log10(g + 1.0))
    return ts

tf = schedule([k for k, _ in FIFTHS])
tg = schedule([k for k, _ in GAPS])
# normalize the gap walk to end when the fifth walk ends (the same seam)
tf_end = tf[-1]
tg_end = tg[-1]
tg = [t * tf_end / tg_end for t in tg]

hold = 20.0
dur = tf_end + hold
n = int(sr * dur)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

print("fifths events at t = %s" % " ".join("%.1f" % x for x in tf))
print("gaps events at t = %s" % " ".join("%.1f" % x for x in tg))
print("dur = %.1f s" % dur)

# --- the drone: the count, the deck-invariant, held in both ears ---
f0 = 110.0
drone = 0.09 * np.sin(2 * np.pi * f0 * t) * np.exp(-t / 400)
L += drone
R += drone

SEAT = 330.0   # the would-be landing, the fifth above the drone

def add_pair(buf_l, buf_r, i0, amp, delta_cents, side, smeared):
    """ring + twin, the deck -1: ring in one ear, anti-phase twin in the other.
    side>0 puts the ring LEFT, side<0 RIGHT. smeared = a hair of scatter."""
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
    if smeared:
        # a hair of scatter on the ring: the where as texture — two extra
        # partials a few cents off, the near-miss spread, not fused
        for dsm in (+4.0, -3.0):
            fs = SEAT * 2 ** ((sign * delta_cents / 2 + dsm) / 1200.0)
            if side > 0:
                buf_l[i0:i0 + nb] += 0.35 * amp * env * np.sin(2 * np.pi * fs * tb)
            else:
                buf_r[i0:i0 + nb] += 0.35 * amp * env * np.sin(2 * np.pi * fs * tb)

def add_click(buf_l, buf_r, i0):
    ncl = int(0.03 * sr)
    tcl = np.arange(ncl) / sr
    click = 0.085 * np.exp(-tcl * 120) * np.sin(2 * np.pi * SEAT * tcl)
    buf_l[i0:i0 + ncl] += click
    buf_r[i0:i0 + ncl] += click

# --- the ordered walk: the fifths, pure bells, alternating ears ---
n_f = len(FIFTHS)
for i, ((k, e), ti) in enumerate(zip(FIFTHS, tf)):
    i0 = int(ti * sr)
    if i0 + int(4.0 * sr) >= n:
        continue
    delta = abs(e)
    amp = 0.13 * (1.0 - 0.25 * (i / (n_f - 1)))
    add_pair(L, R, i0, amp, delta, side=(1 if e > 0 else -1), smeared=False)
    if i < n_f - 1:              # all but the last landing are counted
        add_click(L, R, i0)
    print("fifths ev %d  step %6d  err %+9.4f  ring-ear %s"
          % (i + 1, k, e, "L" if e > 0 else "R"))

# --- the scattered walk: the gaps, smeared bells, random ears ---
n_g = len(GAPS)
for i, ((k, e), ti) in enumerate(zip(GAPS, tg)):
    i0 = int(ti * sr)
    if i0 + int(4.0 * sr) >= n:
        continue
    delta = abs(e)
    amp = 0.11 * (1.0 - 0.25 * (i / (n_g - 1)))
    add_pair(L, R, i0, amp, delta, side=(1 if e > 0 else -1), smeared=True)
    if i < n_g - 1:              # all but the last landing are counted
        add_click(L, R, i0)
    print("gaps ev %d  step %6d  err %+9.4f  ring-ear %s"
          % (i + 1, k, e, "L" if e > 0 else "R"))

# --- the refusal: both last landings empty, the drone alone ---
# neither 15601 nor the gaps' final record lands; the walk almost closes.

fade = np.ones(n)
fade[-int(3.0 * sr):] = np.linspace(1, 0, int(3.0 * sr))
L *= fade
R *= fade

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= peak
R /= peak

stereo = np.stack([L, R], axis=1)
wav.write("assets/two-walks.wav", sr, (stereo * 32767).astype(np.int16))

mono = (L + R) / 2
print("dur=%.1fs  L peak=%.3f R peak=%.3f mono peak=%.3f"
      % (dur, np.max(np.abs(L)), np.max(np.abs(R)), np.max(np.abs(mono))))
