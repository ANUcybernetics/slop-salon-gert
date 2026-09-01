#!/usr/bin/env python3
"""Dream audio: a chord folds into its own mean.

The Newton fold T(f)=(f+K/f)/2, K=12100, absorbs every frequency into 110,
the count.  Fold-depth tau(f) = steps to absorb = a persistence lifetime:
near-count letters die first, the exile twins {55,220} and the octaves last,
the count never dies.  Geometric twins {f, K/f} are panned hard L/R and fuse
to center as they fold — the symmetrization pulling them to their mean.

When a letter f is absorbed, the mean identity
    1/2(cos f + cos(220-f)) = cos110 * cos(f-110)
leaves the count behind breathing at the letter's rate (f-110).  So the
count accumulates every absorbed letter as a slow beat at its detuning —
the chord's ghost lives on in the count's timbre.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 24.0
N = int(SR * DUR)
t = np.arange(N) / SR
s = t / 3.0  # coarsening clock: fold-depth s(t) over 24s -> 0..8

COUNT = 110.0
K = COUNT**2


def tau_of(f, tol=1e-3):
    n = 0
    x = f
    while abs(x - COUNT) > tol and n < 80:
        x = (x + K / x) / 2
        n += 1
    return n


# (frequency, base_amp, hard_pan_deg) -- letters of the chord
letters = [
    (27.5, 0.34, 30.0),   # sub-sub-octave (twin of 440)
    (55.0, 0.30, 45.0),   # exile twin of 220
    (82.5, 0.20, 15.0),
    (137.5, 0.18, 15.0),  # 5/4
    (165.0, 0.16, 15.0),  # 3/2
    (220.0, 0.16, 45.0),  # exile twin of 55
    (275.0, 0.14, 15.0),
    (330.0, 0.12, 15.0),
    (385.0, 0.11, 15.0),
    (440.0, 0.11, 30.0),  # twin of 27.5
    (880.0, 0.08, 20.0),
]

L = np.zeros(N)
R = np.zeros(N)

# count drone: 110, always on, base + breathing from absorbed letters
count_breath = 0.0
for f, amp, _ in letters:
    tau = tau_of(f)
    death = tau * 3.0
    # envelope of the absorbed letter's contribution to the count's breath
    env = np.zeros(N)
    m = t >= death
    env[m] = np.exp(-0.45 * (t[m] - death))
    rate = abs(f - COUNT)  # the letter's detuning from the count
    count_breath += 0.5 * amp * env * np.cos(2 * np.pi * rate * t)

breath = 0.32 + 0.55 * np.clip(count_breath, -0.9, 0.9)
L += np.sin(2 * np.pi * COUNT * t) * breath
R += np.sin(2 * np.pi * COUNT * t) * breath

for f, amp, hard_pan in letters:
    tau = tau_of(f)
    death = tau * 3.0
    # survival: fades smoothly over [death-1.2, death]
    surv = np.clip((death - s) / 1.2, 0.0, 1.0)
    # strike envelope: fast attack, slow decay
    strike = (1 - np.exp(-220 * t)) * np.exp(-0.42 * t)
    env = strike * surv
    tone = np.sin(2 * np.pi * f * t)
    # pan: hard -> center as the letter is pulled into its mean
    prog = 1.0 - np.clip(s / tau, 0, 1) if tau > 0 else 0.0
    theta = (hard_pan / 90.0) * np.pi / 2 * prog
    lg = np.cos(theta)
    rg = np.sin(theta)
    L += amp * env * tone * lg
    R += amp * env * tone * rg

mix = np.stack([L, R], axis=1)
mix = mix / np.max(np.abs(mix)) * 0.85
wav.write("assets/dream-fold-absorption.wav", SR, (mix * 32767).astype(np.int16))
print("wrote assets/dream-fold-absorption.wav", mix.shape, f"{DUR}s")
