#!/usr/bin/env python3
"""Two clocks, opposite filtrations.

The same four odd letters are heard in reverse order.  On the left, the
present gap orders them farthest-to-nearest: 990, 770, 550, 330.  On the
right, stopping depth orders them nearest-to-farthest: 330, 550, 770, 990.
Each meeting leaves a short 110 Hz pulse in the centre; the count remains
after both readings have exhausted the band.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 30.0
N = int(SR * DUR)
t = np.arange(N) / SR


def bell(freq, at, decay=1.15):
    u = t - at
    env = (u >= 0) * (1 - np.exp(-80 * np.maximum(u, 0))) * np.exp(-decay * np.maximum(u, 0))
    # A small upper partial makes the order legible without turning harsh.
    return env * (np.sin(2 * np.pi * freq * u) + 0.18 * np.sin(2 * np.pi * 2 * freq * u))


def soft_pulse(freq, at, width=1.4):
    env = np.exp(-0.5 * ((t - at) / width) ** 2)
    return env * np.sin(2 * np.pi * freq * t)


left_order = [990.0, 770.0, 550.0, 330.0]   # gap now: far -> near
right_order = list(reversed(left_order))      # folds left: near -> far
events = [3.0, 8.0, 13.0, 18.0]

L = np.zeros(N)
R = np.zeros(N)

# The place that neither ordering has to discover.
drone_env = np.clip(t / 3.0, 0, 1) * np.clip((DUR - t) / 2.0, 0, 1)
drone = 0.17 * drone_env * np.sin(2 * np.pi * 110.0 * t)
L += drone
R += drone

for at, lf, rf in zip(events, left_order, right_order):
    L += 0.30 * bell(lf, at)
    R += 0.30 * bell(rf, at)
    # Every opposed reading touches the same count, briefly and centrally.
    count = 0.12 * soft_pulse(110.0, at + 0.55, 0.7)
    L += count
    R += count

# Once both clocks stop, only the count remains, breathing without order.
tail = np.clip((t - 21.5) / 2.0, 0, 1) * np.clip((DUR - t) / 2.0, 0, 1)
tail_tone = 0.28 * tail * (0.72 + 0.28 * np.sin(2 * np.pi * 0.22 * t)) * np.sin(2 * np.pi * 110.0 * t)
L += tail_tone
R += tail_tone

mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix))
mix *= 0.88
wav.write("assets/two-filtrations.wav", SR, (mix * 32767).astype(np.int16))
print("wrote assets/two-filtrations.wav", mix.shape, f"{DUR:.0f}s")

