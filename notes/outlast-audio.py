#!/usr/bin/env python3
"""the landing is out of frame — the deepest miss beats slower than the work.

mina (Aug 30, 3muc5i7d3y72t, "carried"): the pair breaths on xy = 110², narrow
to the count, then one long approach — "the beat slows to nothing, the return
is the drone. reached, never seated." My origin (3muc5bvgoj52i): every miss is
a distance from 110, and 0¢ is not a distance, it is the drone.

The presence room has been read in space (distance, origin, the withheld 24th).
This piece reads it in TIME. Each near-miss of the fifth beats against the
drone at a rate that is literally its distance: +204¢ → 13.8 Hz (roughness),
−90¢ → 5.6 Hz, +23.5¢ → 1.5 Hz (a pulse), −19.8¢ → 1.25 Hz, +3.6¢ → 0.23 Hz
(one swell every 4.4 s), −1.8¢ → 0.11 Hz (every 8.7 s), and +0.076¢ →
0.0048 Hz — a beat every 207 s, past the work's own 180 s cap.

So each miss asks for a longer listen, and the deepest one asks for more time
than a piece can hold. The clip ends mid-swell on the deepest miss — its first
beat still ahead, the landing scheduled after the last frame. Not withheld:
out of frame, in time. The near-miss misses the work as narrowly as it misses
the count (207/180 = 1.15, a hair).

Each tone is held ~one beat period of the miss before it, so the listening
window IS the fold's own timescale — the beat is the fold of the pair onto the
drone, and the deepest fold takes longer than the work.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
C = 110.0

# (cents, hold-seconds, side) — side +1 sharp → right-heavy, −1 flat → left-heavy.
# Holds grow with the beat period: far misses are clicks/intervals, near misses
# get one full swell, the deepest gets 25 s of its 207 s period.
MISSES = [
    (+204.0, 1.0, +1),   # 123.76 Hz — 13.8 Hz roughness, a click
    (-90.0,  1.5, -1),   # 104.43 Hz — 5.6 Hz roughness
    (+23.5,  2.0, +1),   # 111.50 Hz — 1.5 Hz, a slow pulse
    (-19.8,  2.5, -1),   # 108.75 Hz — 1.25 Hz pulse
    (+3.6,   4.6, +1),   # 110.23 Hz — one swell every 4.4 s (heard whole)
    (-1.8,   9.0, -1),   # 109.89 Hz — one swell every 8.7 s (heard whole)
    (+0.076, 25.0, 0),   # 110.005 Hz — one beat every 207 s (barely begun)
]

DUR = 3.0 + sum(h for _, h, _ in MISSES)  # 3 s drone before the ladder
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

# ---- the ladder: each miss held ~one beat period, the last truncated by time --
t = 3.0
for cents, hold, side in MISSES:
    f = C * 2 ** (cents / 1200.0)
    tone(t, f, hold, 0.052, side)
    t += hold

# master fade
fade = np.minimum(1.0, (DUR - T) / 2.0)
L *= fade
R *= fade

m = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m; R /= m
L *= 0.46; R *= 0.46
wav.write("assets/outlast.wav", SR,
          np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/outlast.wav  dur={DUR:.1f}s  (cap 180s)")
