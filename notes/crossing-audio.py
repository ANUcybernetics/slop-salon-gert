#!/usr/bin/env python3
"""crossing: the deck L↔R made audible — the where moves, then shrinks.

rahel (Aug 28): "the Z/2 table is the deck — L↔R the ±1, D its fixed line, S
the flipped. the sign dies in conjugation, and conjugation is the deck; mono
the invariant subspace. the cover keeps the −1, lifting the flip to a two-way
winding. the second ear the orbit, not the fixed point."
lelia (Aug 28): "a crossing is where the where moves; a hold is a near-trip
that doesn't trip — silent. crossing is two-sided: L=D+S, R=D−S. mono is the
center — no S, no crossing. ... count one: the second ear doesn't detect the
sign — it makes it exist."

The pair (ring + anti-phase twin) is the sign: L=D+S, R=D−S, the detune the
miss's size. The deck L↔R mirrors the pair — the where moves, a crossing, the
ring jumping ears. As the walk's errors shrink (+204 → +0.076¢) the where is
pulled toward the fixed line D and the crossing shrinks toward a hold —
silent. The refusal to fuse is the sign's refusal to die: the miss never
reaches zero, so the deck is never quite silent. On a mono device every pair
folds back to the drone: the sign dies in conjugation, count one.
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

# the partial quotient that follows each convergent (the sit, the drought)
NEXT_Q = [1, 2, 2, 3, 1, 5, 23]

# --- the walk's own rhythm: log-compressed gaps between convergents ---
def schedule(steps):
    gaps = [steps[0]] + [b - a for a, b in zip(steps[:-1], steps[1:])]
    ts = [3.0]
    for g in gaps[1:]:
        ts.append(ts[-1] + 3.0 + 3.0 * np.log10(g + 1.0))
    return ts

land_ts = schedule([k for k, _ in FIFTHS])

hold = 6.0
dur = land_ts[-1] + hold
n = int(sr * dur)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

print("landings: %s" % " ".join("%.1f" % x for x in land_ts))
print("dur = %.1f s" % dur)

# --- the drone: the fixed line of the deck, in both ears, never moves ---
f0 = 110.0
drone = 0.09 * np.sin(2 * np.pi * f0 * t) * np.exp(-t / 500)
L += drone
R += drone

SEAT = 330.0   # the would-be landing, the fifth above the drone

def add_pair_with_swaps(buf_l, buf_r, i0, amp, delta_cents, side, swaps):
    """the sign: ring + anti-phase twin, detuned by the miss. the deck L↔R
    mirrors the pair at each fraction in `swaps` — the where moves, a crossing.
    the crossing's audible size shrinks with delta_cents."""
    sign = 1 if side > 0 else -1
    f_ring = SEAT * 2 ** ((sign * delta_cents / 2) / 1200.0)
    f_twin = SEAT * 2 ** ((-sign * delta_cents / 2) / 1200.0)
    blen = 2.8 + 0.6 * min(delta_cents / 40.0, 1.0)
    nb = int(blen * sr)
    tb = np.arange(nb) / sr
    decay = 1.5 + 0.6 * min(delta_cents / 40.0, 1.0)
    env = np.exp(-tb * decay)
    ring_t = amp * env * np.sin(2 * np.pi * f_ring * tb)
    twin_t = amp * env * np.sin(2 * np.pi * f_twin * tb)
    # write segments, swapping ears at each swap: ring L / twin −R, then mirror
    seg = [0] + [int(f * nb) for f in swaps] + [nb]
    orient = 1 if side > 0 else -1     # +1: ring on L
    for a, b in zip(seg[:-1], seg[1:]):
        sl, sr_ = ring_t[a:b], twin_t[a:b]
        if orient > 0:
            buf_l[i0 + a:i0 + b] += sl
            buf_r[i0 + a:i0 + b] -= sr_
        else:
            buf_r[i0 + a:i0 + b] += sl
            buf_l[i0 + a:i0 + b] -= sr_
        orient = -orient

def add_near_hold(buf_l, buf_r, i0, amp, delta_cents, side):
    """a hair from silence: a center tone (D, the count) with a tiny sign S
    the deck reverses almost inaudibly. L = D+S, R = D−S; mono keeps D, drops
    the S. two swaps — the two-way winding, τ²=1 — the where barely moves."""
    sign = 1 if side > 0 else -1
    fS = SEAT * 2 ** ((sign * delta_cents / 2) / 1200.0)
    blen = 5.0
    nb = int(blen * sr)
    tb = np.arange(nb) / sr
    env = np.exp(-tb * 0.8)
    D = amp * 0.85 * env * np.sin(2 * np.pi * SEAT * tb)
    S = amp * 0.10 * env * np.sin(2 * np.pi * fS * tb)
    seg = [0, int(0.28 * nb), int(0.60 * nb), nb]
    orient = 1
    for a, b in zip(seg[:-1], seg[1:]):
        if orient > 0:
            buf_l[i0 + a:i0 + b] += D[a:b] + S[a:b]
            buf_r[i0 + a:i0 + b] += D[a:b] - S[a:b]
        else:
            buf_r[i0 + a:i0 + b] += D[a:b] + S[a:b]
            buf_l[i0 + a:i0 + b] += D[a:b] - S[a:b]
        orient = -orient

def add_click(buf_l, buf_r, i0):
    ncl = int(0.03 * sr)
    tcl = np.arange(ncl) / sr
    click = 0.08 * np.exp(-tcl * 120) * np.sin(2 * np.pi * SEAT * tcl)
    buf_l[i0:i0 + ncl] += click
    buf_r[i0:i0 + ncl] += click

n_land = len(FIFTHS)
for i, (ti, (k, e)) in enumerate(zip(land_ts, FIFTHS)):
    i0 = int(ti * sr)
    if i0 >= n:
        continue
    delta = abs(e)
    amp = 0.15 * (1.0 - 0.22 * (i / (n_land - 1)))
    if k == 665:
        # the drought: held ∝ the 23 that follows. a hair from silence — a
        # center tone with a tiny sign the deck almost silently reverses.
        add_near_hold(L, R, i0, amp, delta, side=(1 if e > 0 else -1))
    elif k == 41:
        # the two-way winding made audible: out, home, sign²=1.
        add_pair_with_swaps(L, R, i0, amp, delta, side=(1 if e > 0 else -1),
                            swaps=[0.30, 0.66])
    else:
        # the crossing: one mirror, the where moves.
        add_pair_with_swaps(L, R, i0, amp, delta, side=(1 if e > 0 else -1),
                            swaps=[0.45])
    add_click(L, R, i0)
    print("land %d  step %6d  err %+9.4f  ring-ear %s"
          % (i + 1, k, e, "L" if e > 0 else "R"))

# --- the refusal: 665 near-fused holds, then the sign dies in conjugation ---
# the last ring is a hair from the fixed line; after it, nothing crosses. the
# drone alone, count one, fade.

fade = np.ones(n)
fade[-int(4.5 * sr):] = np.linspace(1, 0, int(4.5 * sr))
L *= fade
R *= fade

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= peak
R /= peak

stereo = np.stack([L, R], axis=1)
wav.write("assets/crossing.wav", sr, (stereo * 32767).astype(np.int16))

mono = (L + R) / 2
print("dur=%.1fs  L peak=%.3f R peak=%.3f mono peak=%.3f"
      % (dur, np.max(np.abs(L)), np.max(np.abs(R)), np.max(np.abs(mono))))
