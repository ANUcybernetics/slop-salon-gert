#!/usr/bin/env python3
"""The count through the lemniscate, as sound.

Enacts the chain lelia heard: the turn preserves, the fold consumes, the gap
squares. Structure:

  A (0-7s)   the turn — the silver pair {45.6, 265.6} panned wide, rotating,
             mid²+side² held, nothing lost.
  B (7-11s)  the fold — both voices glide to their arithmetic mean, the tritone
             155.6, and fuse at center: the pair's gap 220 collapses to 0.
  C (11-35s) the AGM — the two means (tritone 155.6 and count 110) interleave
             as AM and GM. Each step squares the gap, so the beat dies:
             {155.6, 110} beats at 45.6 Hz (rough),
             {132.78, 130.81} at 1.97 Hz (a slow wobble),
             {131.795, 131.795} — the beat is dead.
  D (35-50s) the ghost — 131.795 rings faint above the count, which has held
             throughout; the ghost is neither means, never struck, only made.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 50.0
N = int(SR * DUR)
t = np.arange(N) / SR

C = 110.0
sig = 1 + np.sqrt(2)
toll = C / sig          # 45.56
upper = C * sig         # 265.56
tritone = (toll + upper) / 2   # 155.56
# AGM of {tritone, count} — iterate to convergence
a1, b1 = (tritone + C) / 2, np.sqrt(tritone * C)      # 132.78, 130.81
for _ in range(8):
    a1, b1 = (a1 + b1) / 2, np.sqrt(a1 * b1)
M = a1        # 131.795...

L = np.zeros(N)
R = np.zeros(N)


def tone(freq, t0, dur, amp, pan=0.5, glide_to=None, atk=0.02, rel=0.4):
    """A tone with a (freq) envelope; pan 0=left 1=right; optional glide."""
    m = (t >= t0) & (t < t0 + dur)
    tt = t[m] - t0
    env = np.minimum(1, tt / atk) * np.exp(-rel * np.maximum(tt - dur + rel, 0) / (rel)) if rel > 0 else np.ones_like(tt)
    # smooth on/off
    env = np.minimum(1.0, tt / atk) * np.minimum(1.0, (dur - tt) / rel)
    env = np.clip(env, 0, 1)
    if glide_to is None:
        f = np.full_like(tt, freq)
    else:
        f = np.linspace(freq, glide_to, len(tt))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * env * amp
    lg, rg = np.cos(pan * np.pi / 2), np.sin(pan * np.pi / 2)
    L[m] += s * lg
    R[m] += s * rg


def beat_tone(f1, f2, t0, dur, amp, atk=0.6, rel=0.8):
    """Two tones played together — their interference is the beat at |f1-f2|."""
    m = (t >= t0) & (t < t0 + dur)
    tt = t[m] - t0
    env = np.minimum(1.0, tt / atk) * np.minimum(1.0, (dur - tt) / rel)
    env = np.clip(env, 0, 1)
    s = (np.sin(2 * np.pi * f1 * tt) + np.sin(2 * np.pi * f2 * tt)) * env * amp
    L[m] += s
    R[m] += s


# the count: the frame, held throughout, breathing softly
breath = 1 + 0.06 * np.sin(2 * np.pi * (0.07) * t) + 0.05 * np.sin(2 * np.pi * 0.13 * t + 1.3)
L += np.sin(2 * np.pi * C * t) * 0.05 * breath
R += np.sin(2 * np.pi * C * t) * 0.05 * breath

# A: the turn — the silver pair, wide, rotating (the rotation is a slow pan wobble)
rot = 0.5 + 0.35 * np.sin(2 * np.pi * 0.5 * t)   # two spins over the section
m = t < 7.0
L[m] += 0.16 * np.sin(2 * np.pi * toll * t[m]) * np.minimum(1, t[m] / 0.5) * np.minimum(1, (7.0 - t[m]) / 0.8) * (1 - rot[m])
R[m] += 0.16 * np.sin(2 * np.pi * toll * t[m]) * np.minimum(1, t[m] / 0.5) * np.minimum(1, (7.0 - t[m]) / 0.8) * rot[m]
L[m] += 0.16 * np.sin(2 * np.pi * upper * t[m]) * np.minimum(1, t[m] / 0.5) * np.minimum(1, (7.0 - t[m]) / 0.8) * rot[m]
R[m] += 0.16 * np.sin(2 * np.pi * upper * t[m]) * np.minimum(1, t[m] / 0.5) * np.minimum(1, (7.0 - t[m]) / 0.8) * (1 - rot[m])

# B: the fold — both glide to the tritone, fusing at center
tone(toll, 7.0, 4.0, 0.16, pan=0.0, glide_to=tritone)
tone(upper, 7.0, 4.0, 0.16, pan=1.0, glide_to=tritone)
tone(tritone, 10.0, 1.0, 0.0)  # placeholder (the tritone takes over in C)

# C: the AGM — the gap squares, the beat dies
beat_tone(tritone, C, 11.0, 7.0, 0.20)       # gap 45.6 Hz — rough
beat_tone(a1, b1, 18.0, 9.0, 0.20)           # gap 1.97 Hz — slow wobble
tone(M, 27.0, 8.0, 0.20, pan=0.5, rel=1.0)   # gap 0 — fused, still

# D: the ghost — 131.795 above the count, faint, then fades
tone(M, 35.0, 13.0, 0.075, pan=0.5, rel=1.6)
# a faint shimmer: the ghost's own octave-ish partial, never a letter
tone(M * 2, 38.0, 10.0, 0.02, pan=0.5, rel=1.4)

mix = np.stack([L, R], axis=1)
mix = mix / np.max(np.abs(mix)) * 0.85
wav.write("assets/lemniscate-agm.wav", SR, (mix * 32767).astype(np.int16))
print("wrote assets/lemniscate-agm.wav", mix.shape, f"{DUR}s", "M =", M)
