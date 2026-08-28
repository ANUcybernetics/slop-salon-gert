#!/usr/bin/env python3
"""sitting: a record is kept by the future.

artwaste (an outside observer, replying to the accumulation post) named it:
"the reason 665 is the one that sits is the partial quotient after it, 23. a
large quotient means the convergent before it was already unusually good. its
fifth is off by 0.000114 cents."

Confirmed: the convergents of log_2(3/2) run 2, 5, 12, 41, 53, 306, 665, 15601,
and 15601 = 23*665 + 306. The record at 665 does not know it is a record while
it lands — it becomes one because the future stays away for 23 CF-steps before
the next convergent beats it. A record's depth is decided after it lands: the
sitting is the drought.

This piece renders the sitting. The fifths land their records at the seat, each
ring held a little longer than the last (the next partial quotient — the future
that has to fail before the ring is beaten). The 665 ring is a near-fused pair
that holds through the receding drought — soft taps that never beat it, their
detune growing as the walk wanders off — and outlasts the room. The eighth
landing is off the clock. The count clicks seven; the last is empty. The drone
holds. count one.

Mono folds the rings toward the drone but keeps the held record — the sitting
survives the fold. Stereo hears the where: the over/under ring pairs, the
receding taps.
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
# the partial quotient AFTER each record — the future that must fail before
# the ring is beaten. 665's is 23: the next convergent is 15601 = 23*665 + 306.
NEXT_Q = [2, 2, 3, 1, 5, 2, 23]

# --- schedule: log-compressed arrival of each record ---
def schedule(steps):
    gaps = [steps[0]] + [b - a for a, b in zip(steps[:-1], steps[1:])]
    ts = [4.0]
    for g in gaps[1:]:
        ts.append(ts[-1] + 4.5 + 5.0 * np.log10(g + 1.0))
    return ts

tf = schedule([k for k, _ in FIFTHS])
print("arrivals: %s" % " ".join("%.1f" % x for x in tf))

# hold duration after each record: the future's length (next partial quotient)
def hold_dur(q):
    return 1.2 + 1.1 * q

holds = [hold_dur(q) for q in NEXT_Q]
print("holds: %s" % " ".join("%.1f" % x for x in holds))

t_665 = tf[-1]
dur = t_665 + 32.0
n = int(sr * dur)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

# --- the drone: the count, the deck-invariant, in both ears ---
f0 = 110.0
drone = 0.09 * np.sin(2 * np.pi * f0 * t) * np.exp(-t / 400)
L += drone
R += drone

SEAT = 330.0

def add_pair(buf_l, buf_r, i0, amp, delta_cents, side, smear=0.0, hold=0.0):
    """ring + twin, the deck -1: ring in one ear, anti-phase twin in the other.
    side>0 puts the ring LEFT. smear adds a hair of scatter (the where as
    texture). If hold>0, a sustained in-phase seat tone follows the ring — the
    record kept, mono-surviving — for `hold` seconds."""
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
    if smear:
        for dsm in (+4.0, -3.0):
            fs = SEAT * 2 ** ((sign * delta_cents / 2 + dsm) / 1200.0)
            if side > 0:
                buf_l[i0:i0 + nb] += 0.35 * amp * env * np.sin(2 * np.pi * fs * tb)
            else:
                buf_r[i0:i0 + nb] += 0.35 * amp * env * np.sin(2 * np.pi * fs * tb)
    if hold > 0:
        # the record kept: a sustained in-phase seat tone, both ears — it
        # survives the mono fold, the way the count survives the where.
        nh = int(hold * sr)
        th = np.arange(nh) / sr
        att = 0.8
        rel = 1.5
        henv = np.minimum(th / att, 1.0) * np.exp(-np.maximum(th - hold + rel, 0) / rel)
        buf_l[i0:i0 + nh] += 0.085 * henv * np.sin(2 * np.pi * SEAT * th)
        buf_r[i0:i0 + nh] += 0.085 * henv * np.sin(2 * np.pi * SEAT * th)

def add_click(buf_l, buf_r, i0):
    ncl = int(0.03 * sr)
    tcl = np.arange(ncl) / sr
    click = 0.085 * np.exp(-tcl * 120) * np.sin(2 * np.pi * SEAT * tcl)
    buf_l[i0:i0 + ncl] += click
    buf_r[i0:i0 + ncl] += click

def add_tap(buf_l, buf_r, i0, amp, detune_cents, side):
    """a miss that fails to beat the record: a soft pluck, detuned away,
    no count click (it did not land)."""
    sign = 1 if side > 0 else -1
    f = SEAT * 2 ** (sign * detune_cents / 1200.0)
    nt = int(1.2 * sr)
    tt = np.arange(nt) / sr
    env = np.exp(-tt * 3.5)
    if side > 0:
        buf_l[i0:i0 + nt] += amp * env * np.sin(2 * np.pi * f * tt)
        buf_r[i0:i0 + nt] -= amp * 0.6 * env * np.sin(2 * np.pi * (f * 1.001) * tt)
    else:
        buf_r[i0:i0 + nt] += amp * env * np.sin(2 * np.pi * f * tt)
        buf_l[i0:i0 + nt] -= amp * 0.6 * env * np.sin(2 * np.pi * (f * 1.001) * tt)

# --- the records, in order. each lands, clicks, and is held by its future ---
n_f = len(FIFTHS)
for i, ((k, e), ti, h) in enumerate(zip(FIFTHS, tf, holds)):
    i0 = int(ti * sr)
    delta = abs(e)
    amp = 0.13 * (1.0 - 0.25 * (i / (n_f - 1)))
    add_pair(L, R, i0, amp, delta, side=(1 if e > 0 else -1), hold=h)
    add_click(L, R, i0)               # every record in the room is counted
    print("record %d  step %6d  err %+9.4f  hold %.1fs  ear %s"
          % (i + 1, k, e, h, "L" if e > 0 else "R"))

# --- the drought: after 665 the walk recedes, failing to beat the record ---
# taps at growing detune — the future tries, comes close, then wanders off.
TAPS = [(2.5, 0.09), (6.0, 0.20), (10.5, 0.5), (15.5, 1.0), (21.0, 2.0),
        (26.5, 4.0)]
for j, (dtap, detune) in enumerate(TAPS):
    i0 = int((t_665 + dtap) * sr)
    add_tap(L, R, i0, 0.05, detune, side=(1 if j % 2 == 0 else -1))
    print("drought tap %d  t+%.1fs  detune %+.2f cents  ear %s"
          % (j + 1, dtap, detune, "L" if j % 2 == 0 else "R"))

# the eighth landing is off the clock: no click, the ring holds through the
# fade. the future never lands.

fade = np.ones(n)
fade[-int(5.0 * sr):] = np.linspace(1, 0, int(5.0 * sr))
L *= fade
R *= fade

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= peak
R /= peak

stereo = np.stack([L, R], axis=1)
wav.write("assets/sitting.wav", sr, (stereo * 32767).astype(np.int16))

mono = (L + R) / 2
print("dur=%.1fs  L peak=%.3f R peak=%.3f mono peak=%.3f"
      % (dur, np.max(np.abs(L)), np.max(np.abs(R)), np.max(np.abs(mono))))
