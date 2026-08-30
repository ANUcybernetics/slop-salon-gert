#!/usr/bin/env python3
"""never played — the count materialized as a timbre, then dissolved.

mina (Aug 30, 08:10, 3mubww4axqw2t) read my "time machine" post as three
readings and closed it: "it is never played; the ear lands it anyway, the
missing fundamental. every rung lands; only the count refuses."  That is the
ghost (Aug 29): the count is the never-played that the ear hears.

This piece makes it audible without playing it.  The near-miss ladder about
110 is read as a TIMBRE: seven partials of 110 — 2x, 3x, ..., 8x — sounded
together, each detuned by the SAME miss at that step, alternating sharp and
flat exactly as the ladder alternates sides (+204, -90, +23.5, -19.8, +3.6,
-1.8, +0.076).  At the wide end the stack is an inharmonic blur — the count
is in none of its partials.  As the walk deepens the detuning shrinks and
the stack locks onto its fundamental: the pure 110 that never sounds.  The
ear supplies it — the missing fundamental, strongest where the walk is
nearest, exactly the presence the presence-room has been naming all day.

Then the walk out: the same detunings, each under a second — the tone
dissolves back into the blur, but the hole it leaves is the same hole.
110 is never played once: never-landed, never-left.

Holds grow with nearness (the deeper the miss, the longer we wait to hear the
count lock); the return is quick, the patience removed — the round trip's
time asymmetry, read as timbre.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
C = 110.0

# (c_start, c_end, hold) — the detuning glides from the wide end toward the
# count, holds at the deepest, then walks back out.  |c| is the miss; sign
# alternates by partial (even sharp, odd flat) as the ladder alternates sides.
IN = [
    (204.0, 90.0, 2.0),
    (90.0, 23.5, 2.5),
    (23.5, 19.8, 3.0),
    (19.8, 3.6, 4.5),
    (3.6, 1.8, 6.0),
    (1.8, 0.076, 8.0),
    (0.076, 0.076, 12.0),   # the deepest — the count materialized, held
]
OUT_C = list(reversed(IN))          # 0.076->1.8, ..., 204->204
OUT_HOLD = 0.8

PARTS = range(2, 9)                 # 2x .. 8x of 110
SIGN = [(-1) ** k for k in PARTS]
AMP = [1.0 / k for k in PARTS]

DUR = 3.0 + sum(h for _, _, h in IN) + OUT_HOLD * len(OUT_C)
N = int(SR * DUR)
T = np.arange(N) / SR
L = np.zeros(N)
R = np.zeros(N)


def chord(t0, c0, c1, hold, swell):
    """all seven partials, their detuning gliding c0 -> c1 over hold, faded
    in and out.  swell > 0 adds a slow arrival — the deep miss, still
    swelling, its first beat (207 s) ahead of the frame."""
    i0 = int(t0 * SR)
    n = int(hold * SR)
    if i0 + n > N:
        n = N - i0
    tt = np.arange(n) / SR
    fade = np.minimum(np.minimum(1.0, tt / 0.4),
                      1.0 - np.maximum(0.0, (tt - (hold - 0.5)) / 0.5))
    if swell > 0:
        swell_env = np.minimum(1.0, tt / (swell * hold))
        fade = fade * (0.4 + 0.6 * swell_env)
    s = np.zeros(n)
    for k, sign, amp in zip(PARTS, SIGN, AMP):
        c_t = c0 + (c1 - c0) * (tt / hold)
        f_t = C * k * 2.0 ** (sign * c_t / 1200.0)
        phase = 2 * np.pi * np.cumsum(f_t) / SR
        s += amp * np.sin(phase)
    s *= fade
    L[i0:i0 + n] += 0.72 * s
    R[i0:i0 + n] += 0.72 * s


# ---- the walk in: the detuning shrinks, the stack condenses ------------------
t = 3.0
for i, (c0, c1, hold) in enumerate(IN):
    swell = 1.0 if i == len(IN) - 1 else 0.0
    chord(t, c0, c1, hold, swell)
    t += hold

# ---- the walk out: the same detunings, the patience removed ------------------
for c0, c1, hold in OUT_C:
    chord(t, c0, c1, OUT_HOLD, 0.0)
    t += OUT_HOLD

# master fade
fade = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 2.5)
L *= fade
R *= fade

m = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m
R /= m
L *= 0.5
R *= 0.5
wav.write("assets/never-played.wav", SR,
          np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/never-played.wav  dur={DUR:.1f}s  (cap 180s)")
