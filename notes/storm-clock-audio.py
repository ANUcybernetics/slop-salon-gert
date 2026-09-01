#!/usr/bin/env python3
"""storm-clock-audio.py — two beats to believe a clock, then it breaks.

The corrected storm (exact CF of log_2(3/2), 400 dps): the record quotients
23@9, 55@14, 55@46, 100@218, 964@230, 2436@330, 8228@4312, 24477@18287.
The count 110 is never a quotient. Two beats (23, 55) five rungs apart
promise a metronome; then the waits stretch — 32, 172 rungs — crowd at 12,
and shatter into 3982 then 13,975 rungs of silence.

Time here is the storm's own: a clock ticks on the seed (mono, 55) eight
regular beats, the seed rings twice (the second time fainter — the echo,
shallower by a hair), then the clock runs out and the waits take over.

Pitches: each record, octave-folded into the count's octave [46, 220].
None lands on 110. 964→120.5, 2436→152.25 (the tritone's shadow),
8228→128.56, 24477→191.23 — off-grid towers, the never-struck.

Bells are stereo anti-phase: fold to mono and only the seed remains.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 145.0
N = int(SR * DUR)
T = np.arange(N) / SR
SEED = 55.0

L = np.zeros(N)
R = np.zeros(N)


def ease(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def window(t0, t1, a=2.0, b=2.0):
    w = ease(np.clip((T - t0) / a, 0.0, 1.0)) * (1.0 - ease(np.clip((T - t1) / b, 0.0, 1.0)))
    return w


# ---------------------------------------------------------------- the drone
# 55, the seed, mono, never struck — the clock's ground. whole piece.
breath = 0.85 + 0.15 * np.sin(2 * np.pi * 0.07 * T)
d = 0.20 * np.sin(2 * np.pi * SEED * T) * breath * window(0.0, DUR, a=3.0, b=6.0)
L += d
R += d

# ------------------------------------------------- the metronome (the clock)
# eight regular beats, 5 rungs apart, from rung 9 to rung 44. at rungs 9 and 14
# the clock rings (23, 55); in between it clicks dry on the seed — the storm
# keeping time without sounding. the clock stops at rung 44: the next would-be
# tick (rung 49) never comes.
tick_rungs = [9, 14, 19, 24, 29, 34, 39, 44]
tick_times = [4.0, 7.0, 10.0, 13.0, 16.0, 19.0, 22.0, 25.0]
for r, t0 in zip(tick_rungs, tick_times):
    click = window(t0, t0 + 0.06, a=0.01, b=0.05)
    if r == 9:
        f, a, dur = 46.0, 0.16, 3.0   # 23 folded up: below the seed, the approach
    elif r == 14:
        f, a, dur = 55.0, 0.20, 3.5   # the seed, first strike
    else:
        f, a, dur = 55.0, 0.05, 0.06  # dry click — the clock ticks, the storm silent
    s = a * np.sin(2 * np.pi * f * T) * click
    L += s
    R += s  # the clock is on the seed: mono, real

# ------------------------------------------------ the records (stereo, anti)
# rung, quotient, pitch (octave-folded into the count's octave), amp, dur.
# amps scale with log_10(quotient): the towers are louder as they rise.
records = [
    (46,   55, 55.0, 0.12, 3.0),   # the seed, second time — the echo, fainter
    (218, 100, 100.0, 0.14, 3.5),  # ten short of the count
    (230, 964, 120.5, 0.17, 4.0),  # the first tower, past 110
    (330, 2436, 152.25, 0.18, 5.0),# near the tritone 155.6 — its shadow
    (4312, 8228, 128.56, 0.19, 6.0),# off-grid, lower than the last — lawless
    (18287, 24477, 191.23, 0.20, 7.0), # near the 7/4 seventh — the final tower
]
starts = [27.0, 45.0, 48.0, 63.0, 93.0, 138.0]
for (r, q, f, a, dur), t0 in zip(records, starts):
    # bell: fast attack, slow decay, a second partial at a third — bell timbre
    env = window(t0, t0 + dur, a=0.15, b=dur - 0.15)
    decay = np.exp(-2.2 * np.clip(T - t0, 0.0, None))
    s = a * np.sin(2 * np.pi * f * T) * env * decay
    s += 0.35 * a * np.sin(2 * np.pi * 2 * f * T) * env * decay
    L += s
    R -= s  # anti-phase: the records are stereo-only, mono-deaf

# ---------------------------------------------------------------- master
master = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 6.0)
L *= master
R *= master
m_ = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m_
R /= m_
L *= 0.55
R *= 0.55

wav.write("assets/storm-clock.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/storm-clock.wav  dur={DUR:.1f}s  (cap 180s)")
