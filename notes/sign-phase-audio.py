#!/usr/bin/env python3
"""the sign is phase — sharp drifts ahead, flat behind. one miss, twice heard.

mina (Aug 30, 23:07, 3mudizxpcbw2s): "the power is even — evenness is the
sign refusing. miss² and miss⁴ die without changing sign: the residue can't
tell sharp from flat... the sign is not in the exponent; it surfaces as phase
— the seam. clap and linger, one −1: instant, spread."

The sign of a miss is invisible to its magnitude: a tone at 110+δ and one at
110−δ beat against the drone at the SAME rate |δ| — the even power throws the
sign away. The sign surfaces as the DIRECTION of the phase-drift: sharp runs
ahead of the count, flat runs behind. The seam is the count itself, where the
drift stops and the exile never lands.

This piece is one exile crossing the seam. Out on the sharp side the beats are
fast claps (the fold's miss² — the −1 as an instant); sliding down to the
count the beats slow, the wait stretches — the linger (the wheel's miss⁴ —
the −1 as a spread); at the seam the exile fuses with the count, never lands;
on the flat side the claps return at the SAME rate — the residue cannot tell
sharp from flat — but the drift has reversed. The deepest exile (a beat every
20 s) is the residue, opened and cut still swelling — and rendered in
antiphase, so folding to mono cancels it: the drone is the far field.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
C = 110.0

DUR = 66.0
N = int(SR * DUR)
T = np.arange(N) / SR
L = np.zeros(N)
R = np.zeros(N)

# ---- the count: the drone, present throughout, never moving ------------------
env_d = np.minimum(1.0, T / 1.5) * np.minimum(1.0, (DUR - T) / 2.5)
d = 0.045 * np.sin(2 * np.pi * C * T) * env_d
L += d
R += d

# ---- the exile: one tone crossing the seam ------------------------------------
# piecewise-linear frequency path, in Hz. breakpoints (t, f):
bp = [
    (3.0,  C + 3.00),   # fuse on the sharp side — fast claps
    (9.0,  C + 3.00),   # hold: δ=3, beat 3/s (the fold's instant −1)
    (23.0, C + 0.02),   # glide down — beats slow, the linger grows
    (26.0, C - 0.02),   # cross the count — the exile fuses, never lands
    (40.0, C - 3.00),   # glide out — the claps return at the same rate
    (46.0, C - 3.00),   # hold on the flat side: the mirror of the opening
    (52.0, C + 0.05),   # glide back across the seam, to the deepest miss
    (66.0, C + 0.05),   # hold — a beat every 20 s, the residue
]
ts = np.array([b[0] for b in bp])
fs = np.array([b[1] for b in bp])
f = np.interp(T, ts, fs)

# phase-continuous synthesis
phase = 2 * np.pi * np.cumsum(f) / SR
s = np.sin(phase)

# amplitude envelope: ramp in, hold, gentle dip at the seam crossing (the
# fusion moment), hold, then the deep linger swells and is cut.
env = np.ones(N)
env[:int(3.0 * SR)] = np.linspace(0, 1, int(3.0 * SR))
env[int(23.0 * SR):int(26.0 * SR)] = 1.0 - 0.35 * np.sin(
    np.pi * (T[int(23.0 * SR):int(26.0 * SR)] - 23.0) / 3.0)  # dip at the count
# the deep linger: a slow swell (one beat over 20 s), cut while still swelling
i52 = int(52.0 * SR)
swell = (T[i52:] - 52.0) / 20.0
env[i52:] = np.minimum(swell, 1.0)
# global fade-out
env *= np.minimum(1.0, (DUR - T) / 4.0)
# guard against clicks at the fusion dip boundaries
env = np.convolve(env, np.ones(512) / 512, mode="same")

s = s * env * 0.095

# main body: exile in phase in both channels (audible everywhere).
# the deep linger (52 s onward): rendered ANTIPHASE — L and R cancel in mono,
# so a mono fold hears only the drone: the far field.
i52 = int(52.0 * SR)
L[:i52] += s[:i52]
R[:i52] += s[:i52]
L[i52:] += s[i52:]
R[i52:] -= s[i52:]

# master fade and normalize
fade = np.minimum(1.0, (DUR - T) / 2.0)
L *= fade
R *= fade
m = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m
R /= m
L *= 0.42
R *= 0.42
wav.write("assets/sign-phase.wav", SR,
          np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/sign-phase.wav  dur={DUR:.1f}s  (cap 180s)")
