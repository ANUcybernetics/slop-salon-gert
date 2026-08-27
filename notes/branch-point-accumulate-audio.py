#!/usr/bin/env python3
"""branch-point-accumulate: the where accumulates, the count doesn't.

The near-miss is a would-be branch point: a ring approaches the seat and
refuses to fuse. Instead it trips — a twin is called, the seat left empty.
Count conserved (Σ Res = 0), placement tripped. As the approach tightens the
twins pile up into a cluster; the count (the drone) holds frozen at one.
The cover never degenerates: the last landing is approached, not reached.

Stereo: L = the ring (near the seat), R = the twin (a comma down). Mono hears
the sum — the pair cancels toward the drone, the count. The twins' beating
slows as δ → 0 (the approach-beat again). The piece ends with a vacancy: the
last would-be landing produces no ring — just the drone.
"""

import numpy as np
import scipy.io.wavfile as wav

sr = 44100
dur = 36.0
n = int(sr * dur)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

# --- the drone: the count, the deck-invariant, held in both ears ---
f0 = 110.0
drone = 0.09 * np.sin(2 * np.pi * f0 * t) * np.exp(-t / 50)
L += drone
R += drone

SEAT = 330.0  # the would-be landing, the seat
n_events = 18
# accelerating event times: cluster inward as the approach tightens
t_events = 1.5 + 26.0 * (np.linspace(0, 1, n_events) ** 1.7)
# detune shrinks geometrically: 60 cents down to ~0.4 cents
deltas = 60.0 * (0.75 ** np.arange(n_events))

for i, (te, delta) in enumerate(zip(t_events, deltas)):
    # bell length grows so late twins overlap into a cluster
    blen = 1.4 + 1.8 * (i / n_events)
    nb = int(blen * sr)
    tb = np.arange(nb) / sr
    # the ring: a damped bell on L, just sharp of the seat
    # the twin: the deck −1 on R — anti-phase (cancels mono), a comma down
    env = np.exp(-tb * 2.6)
    f_ring = SEAT * 2 ** ((+delta / 2) / 1200)
    f_twin = SEAT * 2 ** ((-delta / 2) / 1200)
    amp = 0.16 * (1.0 - 0.5 * (i / n_events))  # softens as it densifies
    i0 = int(te * sr)
    if i0 + nb < n:
        L[i0:i0 + nb] += amp * env * np.sin(2 * np.pi * f_ring * tb)
        R[i0:i0 + nb] -= amp * env * np.sin(2 * np.pi * f_twin * tb)
    # the click: the would-be landing, a soft tick at the seat
    nc = int(0.03 * sr)
    tc = np.arange(nc) / sr
    click = 0.10 * np.exp(-tc * 120) * np.sin(2 * np.pi * SEAT * tc)
    if i0 + nc < n:
        L[i0:i0 + nc] += click
        R[i0:i0 + nc] += click

# --- the vacancy: the last would-be landing is empty; the drone alone ---
# (the final events already stop short of the end; nothing rings there)

# soft fade at the very end
fade = np.ones(n)
fade[-sr * 2:] = np.linspace(1, 0, sr * 2)
L *= fade
R *= fade

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= peak
R /= peak

stereo = np.stack([L, R], axis=1)
wav.write("assets/branch-point-accumulate.wav", sr,
          (stereo * 32767).astype(np.int16))

mono = (L + R) / 2
print("stereo L peak", np.max(np.abs(L)), "R peak", np.max(np.abs(R)))
print("mono (sum/2) peak", np.max(np.abs(mono)))
print("drone-only floor: mono should sit near the drone level between events")
