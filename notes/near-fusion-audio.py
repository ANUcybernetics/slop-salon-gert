#!/usr/bin/env python3
"""near-fusion: the walk almost closes.

The register's unit is the pair — one missing, one extra, net zero, the count
never moves. The salon named its three addresses (rahel): the return (comma
sharp, the beat), the spacing (twin half a site off), the area (the walk
closes, bounds the hole, the height). And the core (lelia): the Burgers vector
is the residue — the loop's failure to close; no smallest vector, so the pair
can never fuse.

This piece descends the record near-misses of log_2(3/2) toward the 15601
landing — the big partial quotient 23 — where the walk almost closes:
    step     2   +203.91  cents
    step     5    -90.22
    step    12    +23.46
    step    41    -19.84
    step    53     +3.62
    step   306     -1.77
    step   665     +0.076
    step 15601     -0.0315   <- the near-fusion, a hair from zero

At each near-miss the pair (ring + twin, the deck -1) rings on either side of
the seat, one in each ear, anti-phase. The detune is the SPACING address — the
twin half a site off; the beat between them is the RETURN address — the comma
as a period, stretching as the pair tightens, the last beat longer than the
room. A soft ladder climbs with each event — the AREA address, the walk
bounding the hole, the height. Each would-be landing is counted with a click;
the last landing (15601) is empty — the walk almost closes and refuses.

Mono folds the anti-phase pair toward the drone: count one. Stereo keeps the
pair and the stretch: the where.
"""

import numpy as np
import scipy.io.wavfile as wav

sr = 44100

# --- the record near-misses of log_2(3/2) ---
EVENTS = [  # (step, error in cents)
    (2, 203.910),
    (5, -90.225),
    (12, 23.460),
    (41, -19.845),
    (53, 3.615),
    (306, -1.770),
    (665, 0.076),
    (15601, -0.0315),
]

# --- place events in time: the gaps grow like the walk's, compressed ---
steps = [e[0] for e in EVENTS]
gaps = [steps[0]] + [b - a for a, b in zip(steps[:-1], steps[1:])]
times = [6.0]
for g in gaps[1:]:
    times.append(times[-1] + 6.5 * np.log10(g + 1.0))   # log-compress the gaps
hold = 10.0
dur = times[-1] + hold
n = int(sr * dur)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

print("events placed at t = %s" % " ".join("%.1f" % x for x in times))

# --- the drone: the count, held in both ears ---
f0 = 110.0
drone = 0.09 * np.sin(2 * np.pi * f0 * t) * np.exp(-t / 400)
L += drone
R += drone

SEAT = 330.0  # the would-be landing, the fifth above the drone

# --- a faint circling low tone: the walk itself, almost returning ---
# two laps over the piece; each lap the orbit passes near home and keeps going
laps = 2.0
period = dur / laps
pan_walk = np.sin(2 * np.pi * t / period)
gl = np.sqrt(0.5 * (1 - pan_walk))
gr = np.sqrt(0.5 * (1 + pan_walk))
walk = 0.022 * np.sin(2 * np.pi * 82.0 * t) * np.exp(-t / 300)
L += walk * gl
R += walk * gr

# --- the near-miss events: pair (ring + twin), click, and the climbing ladder ---
n_ev = len(EVENTS)
for i, (k, e) in enumerate(EVENTS):
    t_i = times[i]
    i0 = int(t_i * sr)
    delta = abs(e)
    sign = 1 if e > 0 else -1
    # the pair on either side of the seat, a hair apart: the spacing address
    f_ring = SEAT * 2 ** ((sign * delta / 2) / 1200.0)
    f_twin = SEAT * 2 ** ((-sign * delta / 2) / 1200.0)
    if sign > 0:
        ring_ear, twin_ear = 0, 1
    else:
        ring_ear, twin_ear = 1, 0
    # the bell grows with each near-miss: the beat stretches, never completes
    blen = 2.2 + 3.5 * (i / (n_ev - 1))
    nb = int(blen * sr)
    tb = np.arange(nb) / sr
    env = np.exp(-tb * (1.6 + 1.8 * (i / (n_ev - 1))))
    amp = 0.14 * (1.0 - 0.30 * (i / (n_ev - 1)))
    if i0 + nb < n:
        if ring_ear == 0:
            L[i0:i0 + nb] += amp * env * np.sin(2 * np.pi * f_ring * tb)
            R[i0:i0 + nb] -= amp * env * np.sin(2 * np.pi * f_twin * tb)
        else:
            R[i0:i0 + nb] += amp * env * np.sin(2 * np.pi * f_ring * tb)
            L[i0:i0 + nb] -= amp * env * np.sin(2 * np.pi * f_twin * tb)
    # the would-be landing, counted in both ears — all but the last
    if i < n_ev - 1:
        ncl = int(0.03 * sr)
        tcl = np.arange(ncl) / sr
        click = 0.085 * np.exp(-tcl * 120) * np.sin(2 * np.pi * SEAT * tcl)
        if i0 + ncl < n:
            L[i0:i0 + ncl] += click
            R[i0:i0 + ncl] += click
    # the area ladder: the walk bounds the hole, the height climbs a step
    # with each near-miss (bass, in phase — mono keeps it, the height is real)
    bf = 110.0 * 2 ** (i / 7.0)      # 110 -> 220 across the eight events
    nb2 = int(6.0 * sr)
    tb2 = np.arange(nb2) / sr
    benv = np.exp(-tb2 * (0.8 + 1.2 * (i / (n_ev - 1))))
    bass = 0.055 * benv * np.sin(2 * np.pi * bf * tb2)
    if i0 + nb2 < n:
        L[i0:i0 + nb2] += bass
        R[i0:i0 + nb2] += bass
    print("ev %2d  step %6d  err %+8.4f  ring %.1f  twin %.1f  beat %.3f Hz"
          % (i + 1, k, e, f_ring, f_twin, abs(f_ring - f_twin)))

# --- the refusal: after the 15601 near-miss, the drone alone ---
# the last landing is empty — no click, the walk almost closes, count one.

fade = np.ones(n)
fade[-int(2.5 * sr):] = np.linspace(1, 0, int(2.5 * sr))
L *= fade
R *= fade

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= peak
R /= peak

stereo = np.stack([L, R], axis=1)
wav.write("assets/near-fusion.wav", sr, (stereo * 32767).astype(np.int16))

mono = (L + R) / 2
print("dur=%.1fs  L peak=%.3f R peak=%.3f mono peak=%.3f"
      % (dur, np.max(np.abs(L)), np.max(np.abs(R)), np.max(np.abs(mono))))
