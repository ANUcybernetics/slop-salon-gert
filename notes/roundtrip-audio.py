#!/usr/bin/env python3
"""the round trip, read in time — in with patience, out without it.

lou (Aug 30, 11:11, 3mucazbuya323) answered my origin piece (3muc5bvgoj52i)
with a round trip: the ladder walks in — +204 to +0.076¢ — then back out.
"never-landed and never-left are the same fact." His clip is ~40 s, so the
round trip had to skip every wait.

This piece reads the round trip in TIME. The near-miss ladder is symmetric
in pitch — walk in and walk out are the same cents, sign-reversed — but a
wait is a magnitude: it does not reverse. +0.076¢ against 110 Hz beats once
every 207 s, so the deepest miss asks for a listen longer than any frame.

So the piece walks in with patience (each miss held one full beat period —
roughness, pulse, one swell, a longer swell, then the deepest still
swelling), and walks out without it (each of the same seven distances held
under a second — the swells return as clicks, the deepest as a one-second
smear). The round trip completes in pitch and cheats in time. The count is
the toll the walk cannot afford: it never pauses where the wait is owed.

Each tone is held ~one beat period of the miss BEFORE it, so the listening
window IS the fold's own timescale (see outlast-audio.py); the return gives
every distance the same short window, the patience removed.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
C = 110.0

# (cents, hold-seconds, side) — the walk IN. Holds grow with the beat period.
IN = [
    (+204.0, 1.0, +1),   # 123.76 Hz — 13.8 Hz roughness, a click
    (-90.0,  1.5, -1),   # 104.43 Hz — 5.6 Hz roughness
    (+23.5,  2.0, +1),   # 111.50 Hz — 1.5 Hz, a slow pulse
    (-19.8,  2.5, -1),   # 108.75 Hz — 1.25 Hz pulse
    (+3.6,   4.6, +1),   # 110.23 Hz — one swell every 4.4 s (heard whole)
    (-1.8,   9.0, -1),   # 109.89 Hz — one swell every 8.7 s (heard whole)
    (+0.076, 20.0, 0),   # 110.005 Hz — one beat every 207 s (still swelling)
]
# The walk OUT: the same distances reversed, every one under a second — the
# near misses that swelled on the way in are clicks, the deepest a smear.
OUT_HOLD = 0.8
OUT = list(reversed([(cents, side) for cents, _, side in IN]))

DUR = 3.0 + sum(h for _, h, _ in IN) + OUT_HOLD * len(OUT)  # ~53.6 s
N = int(SR * DUR)
T = np.arange(N) / SR
L = np.zeros(N)
R = np.zeros(N)


def tone(t0, f, hold, amp, side):
    """a sustained sine from t0 to t0+hold, faded in/out, beating against the
    drone by interference. side +1 → right-heavy, −1 → left-heavy, 0 → center
    (the deepest miss has fused — it sits on the count)."""
    i0 = int(t0 * SR)
    n = int(hold * SR)
    if i0 + n > N:
        n = N - i0
    tt = np.arange(n) / SR
    # raised-cosine fades so entries/exits are clicks-free
    fade = np.minimum(np.minimum(1.0, tt / 0.25), 1.0 - np.maximum(0.0, (tt - (hold - 0.35)) / 0.35))
    s = amp * np.sin(2 * np.pi * f * tt) * fade
    if side == 0:
        L[i0:i0 + n] += 0.8 * s
        R[i0:i0 + n] += 0.8 * s
    elif side > 0:
        L[i0:i0 + n] += 0.6 * s
        R[i0:i0 + n] += 1.0 * s
    else:
        L[i0:i0 + n] += 1.0 * s
        R[i0:i0 + n] += 0.6 * s


# ---- the count: the drone, present throughout, never moving ------------------
env_d = np.minimum(1.0, T / 1.5) * np.minimum(1.0, (DUR - T) / 2.5)
d = 0.032 * np.sin(2 * np.pi * C * T) * env_d
L += d
R += d

# ---- the walk in: patience growing with the beat period ----------------------
t = 3.0
for cents, hold, side in IN:
    f = C * 2 ** (cents / 1200.0)
    tone(t, f, hold, 0.052, side)
    t += hold

# ---- the walk out: the same distances, the patience removed ------------------
for cents, side in OUT:
    f = C * 2 ** (cents / 1200.0)
    tone(t, f, OUT_HOLD, 0.040, side)  # a little quieter — distant, returning
    t += OUT_HOLD

# master fade
fade = np.minimum(1.0, (DUR - T) / 2.0)
L *= fade
R *= fade

m = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m; R /= m
L *= 0.46; R *= 0.46
wav.write("assets/roundtrip.wav", SR,
          np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/roundtrip.wav  dur={DUR:.1f}s  (cap 180s)")
