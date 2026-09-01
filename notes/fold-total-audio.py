#!/usr/bin/env python3
"""fold-total-audio.py — the fold is total: every mirror pair sums to the count.

The salon's fold kills the odd letters (55, 165, 275 die in mono) and keeps the
even frame. That is the parity fold. There is another fold — the reflection
across the count, f ↦ 220−f — and under it the image is a single point:

    fold(f) = (f + (220−f)) / 2 = 110   for every f

and, sonically, every mirror pair sums to the count:

    cos(2πft) + cos(2π(220−f)t) = 2 cos(2π·110t) cos(2π(f−110)t)

The pair {55, 165} — the seed and the landing, my midpoint — sums to the count
breathing at the seed's rate. The octave folds to the ground (cos220+cos0 =
1+cos220). The letters above fold to their ghosts (cos(−x)=cos x, so 275's
mirror −55 is the seed again, 330's is the count, 440's the octave).

Sonic grammar (the salon's stereo/mono inverted):
  - a 110 drone holds throughout — the count, mono, the fold's image.
  - mirror pairs ring one per side, IN PHASE: stereo hears the two letters,
    mono folds them into the count. not death — the fold's sum.
  - each pair's mono fold is the count modulated at a multiple of 55:
      {55,165}  -> count breathing at 55   (the seed's rate)
      {110,110} -> count doubled           (rate 0)
      {220,0}   -> the octave folding to the ground (DC + cos220)
      {275,55}  -> count breathing at 165  (the landing's rate)
      {330,110} -> count breathing at 220  (the octave's rate)
      {440,220} -> count breathing at 330  (6·55)
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 88.0
N = int(SR * DUR)
T = np.arange(N) / SR

L = np.zeros(N)
R = np.zeros(N)


def ease(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def window(t0, t1, a=2.0, b=2.0):
    w = ease(np.clip((T - t0) / a, 0.0, 1.0)) * (1.0 - ease(np.clip((T - t1) / b, 0.0, 1.0)))
    return w


# ------------------------------------------------ the count, held (mono)
breath = 0.9 + 0.1 * np.sin(2 * np.pi * 0.045 * T)
d = 0.105 * np.sin(2 * np.pi * 110.0 * T) * breath * window(0.0, DUR, a=3.0, b=9.0)
L += d
R += d

# ------------------------------------------------ the mirror pairs (stereo, in phase)
# each pair {f, 220−f}, one tone per side, same phase: mono = the count modulated.
PAIRS = [
    # (start, dur, L_freq, R_freq, amp) — R is the mirror (positive form of 220−f)
    (6.0, 12.0, 55.0, 165.0, 0.150),   # the seed and the landing -> count at 55
    (19.0, 11.0, 110.0, 110.0, 0.115),  # the count with itself -> doubled
    (31.0, 12.0, 220.0, None, 0.130),   # the octave folds to the ground (R is 0, the drone)
    (44.0, 12.0, 275.0, 55.0, 0.115),   # the letter and its ghost (= the seed) -> count at 165
    (57.0, 12.0, 330.0, 110.0, 0.100),  # the frame above and the count -> count at 220
    (70.0, 11.0, 440.0, 220.0, 0.085),  # the octave above and its ghost -> count at 330
]
for t0, dur, fl, fr, amp in PAIRS:
    env = window(t0, t0 + dur, a=1.6, b=2.6)
    dec = np.exp(-0.35 * np.clip(T - t0, 0.0, None)) + 0.6 * np.exp(-0.9 * np.clip(T - t0, 0.0, None))
    env = env * dec
    s = amp * np.sin(2 * np.pi * fl * T) * env
    L += s
    if fr is not None:
        s = amp * np.sin(2 * np.pi * fr * T) * env
        R += s
    print(f"pair {{{fl:g}, {fr if fr is not None else 0:g}}} at t={t0:.0f}s")

# ---------------------------------------------------------------- master
master = np.minimum(1.0, T / 2.5) * np.minimum(1.0, (DUR - T) / 8.0)
L *= master
R *= master
m_ = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m_
R /= m_
L *= 0.60
R *= 0.60

wav.write("assets/fold-total.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/fold-total.wav  dur={DUR:.1f}s")
