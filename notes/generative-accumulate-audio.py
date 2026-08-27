#!/usr/bin/env python3
"""generative-accumulate: the near-miss places itself.

The previous accumulation (branch-point-accumulate) was 18 hand-placed events.
This one has NO event list. The rule: rotate by the irrational fifth,
theta = log_2(3/2). The orbit phi -> phi + theta mod 1 never returns to any
point — but it almost-returns, and the almost-returns are the convergents of
theta, emergent from the rule. An event fires exactly when ||n·theta|| sets a
new record low. That is all: no window, no placement.

What falls out, unbidden:
  - the detune is the record error: 204, 90, 23.5, 19.9, 3.6, 1.8, 0.065 cents
  - the signs alternate (+,-,+,-,+,-,+): each near-miss comes from the far
    side of the seat — the deck -1 twin is automatic, a sheet flip
  - the gaps stretch: 2, 5, 12, 41, 53, 306, 665 steps — the where accumulates
    as the returns get rarer and tighter
  - the target is not in the image: no convergent has error 0, the exact return
    is the limit never reached; the 15601-step near-coincidence (the big
    partial quotient 23) is off the clock — the last landing always empty.

Stereo: L/R carry the walk (the orbit's current position as a circling pulse)
and the events. Each event rings a bell at the seat (330, the fifth above the
drone) and calls its twin — the deck -1, anti-phase — on the far side, the ear
flipping with the sign. Mono folds the anti-phase pair toward the drone; the
count is one, frozen.
"""

import numpy as np
import scipy.io.wavfile as wav

sr = 44100
step = 0.22          # seconds per orbit step
N = 665              # the 665-step convergent is the last one that fits
n_steps = N * step   # 146.3 s of orbit
hold = 14.0          # the drone alone after the last near-miss
dur = n_steps + hold
n = int(sr * dur)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

# --- the drone: the count, the deck-invariant, held in both ears ---
# it must HOLD: barely decay over 160 s, the fade handles the stop
f0 = 110.0
drone = 0.09 * np.sin(2 * np.pi * f0 * t) * np.exp(-t / 400)
L += drone
R += drone

SEAT = 330.0  # the would-be landing, the fifth above the drone

# --- the generator: the wound orbit ---
theta = np.log2(3.0 / 2.0)
events = []            # (step_index, signed_error_in_octaves)
best = float("inf")
for k in range(1, N + 1):
    phi = (k * theta) % 1.0
    # distance to the seat, signed: + = landed sharp of home, - = flat
    signed = phi if phi < 0.5 else phi - 1.0
    d = abs(signed)
    if d < best and k >= 2:   # k=1 is the trivial 1/1, skip it
        best = d
        events.append((k, signed))
    elif d < best:
        best = d

print("generated %d near-miss events:" % len(events))
for k, e in events:
    print("  step %4d  err %+9.3f cents  t=%.1fs" % (k, e * 1200, k * step))

# --- the walk: the orbit's position, a soft circling pulse per step ---
# quiet, so the bells and the drone own the foreground
nc = int(0.008 * sr)
tc = np.arange(nc) / sr
pulse_env = np.exp(-tc * 500)
pulse_tone = np.sin(2 * np.pi * 220.0 * tc)
for k in range(1, N + 1):
    phi = (k * theta) % 1.0
    i0 = int(k * step * sr)
    if i0 + nc >= n:
        continue
    pan = 2.0 * phi - 1.0        # circles L -> R as the orbit wraps
    gl = np.sqrt(0.5 * (1 - pan))  # equal-power panning
    gr = np.sqrt(0.5 * (1 + pan))
    amp = 0.020
    L[i0:i0 + nc] += amp * gl * pulse_env * pulse_tone
    R[i0:i0 + nc] += amp * gr * pulse_env * pulse_tone

# --- the near-miss events: ring + twin + click ---
for i, (k, e) in enumerate(events):
    delta_cents = abs(e) * 1200.0
    sign = 1 if e > 0 else -1     # which side of the seat the return comes from
    # the ring (one sheet) and the twin (the deck -1, the far side)
    f_ring = SEAT * 2 ** ((sign * delta_cents / 2) / 1200.0)
    f_twin = SEAT * 2 ** ((-sign * delta_cents / 2) / 1200.0)
    if sign > 0:
        ring_ear, twin_ear = 0, 1   # ring L, twin R
    else:
        ring_ear, twin_ear = 1, 0   # ring R, twin L — the far side flips
    # later bells ring longer: the tight twin almost fuses, the beating stretches
    blen = 1.6 + 1.2 * (i / len(events))
    nb = int(blen * sr)
    tb = np.arange(nb) / sr
    env = np.exp(-tb * 2.2)
    amp = 0.15 * (1.0 - 0.35 * (i / len(events)))
    i0 = int(k * step * sr)
    if i0 + nb < n:
        if ring_ear == 0:
            L[i0:i0 + nb] += amp * env * np.sin(2 * np.pi * f_ring * tb)
            R[i0:i0 + nb] -= amp * env * np.sin(2 * np.pi * f_twin * tb)
        else:
            R[i0:i0 + nb] += amp * env * np.sin(2 * np.pi * f_ring * tb)
            L[i0:i0 + nb] -= amp * env * np.sin(2 * np.pi * f_twin * tb)
    # the click: the would-be landing, counted in both ears
    ncl = int(0.03 * sr)
    tcl = np.arange(ncl) / sr
    click = 0.10 * np.exp(-tcl * 120) * np.sin(2 * np.pi * SEAT * tcl)
    if i0 + ncl < n:
        L[i0:i0 + ncl] += click
        R[i0:i0 + ncl] += click

# --- the vacancy: after the 665 near-miss the drone alone ---
# the 15601-step near-coincidence is off the clock; nothing rings again.

fade = np.ones(n)
fade[-int(2.5 * sr):] = np.linspace(1, 0, int(2.5 * sr))
L *= fade
R *= fade

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= peak
R /= peak

stereo = np.stack([L, R], axis=1)
wav.write("assets/generative-accumulate.wav", sr,
          (stereo * 32767).astype(np.int16))

mono = (L + R) / 2
print("dur=%.1fs  L peak=%.3f R peak=%.3f mono peak=%.3f"
      % (dur, np.max(np.abs(L)), np.max(np.abs(R)), np.max(np.abs(mono))))
