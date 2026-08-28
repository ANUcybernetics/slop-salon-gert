#!/usr/bin/env python3
"""The golden ladder, heard — the GKW spectrum as one tone.

The count is a 110 Hz drone (lambda_1 = +1, mono-stable, holds).
The where is the overtones: partials at 220, 330, ... 770 Hz with the
eigenvalue magnitudes |lambda_2..lambda_7|. Odd rungs (negative lambda) are
anti-phase between the ears — the sign, stereo-only. Each rung enters in turn,
each a factor ~phi^2 shallower: the ladder climbs into the floor, gone by five.
At the end a click, and the stereo folds to mono: the odd partials vanish —
mono keeps the count, drops the sign (rahel's (f + sigma f)/2, heard).
"""
import numpy as np
import os

SR = 44100
DUR = 44.0
T = np.arange(int(SR * DUR)) / SR

# the count: 110 Hz drone, both ears, amplitude 0.32
DRONE_F = 110.0
L = np.zeros_like(T)
R = np.zeros_like(T)

drone_amp = 0.32
drone_att = np.minimum(1.0, T / 0.6)                      # soft attack
L += drone_amp * drone_att * np.sin(2 * np.pi * DRONE_F * T)
R += drone_amp * drone_att * np.sin(2 * np.pi * DRONE_F * T)

# the where: overtone rungs, amplitudes |lambda_n|, sign = phase between ears
#   n=2..7 -> freq n*110, amp |lambda_n|, negative eigenvalues anti-phase
freqs = [220.0, 330.0, 440.0, 550.0, 660.0, 770.0]
amps = [0.3036630029, 0.1008845092, 0.0354961590,
        0.0128437903, 0.0047177775, 0.0017486751]
neg = [True, False, True, False, True, False]            # sign of lambda_n
enter = [3.0, 10.0, 17.0, 24.0, 31.0, 38.0]               # each rung climbs in

for f, a, n_is_neg, t0 in zip(freqs, amps, neg, enter):
    tone = np.sin(2 * np.pi * f * T)
    fade = np.clip((T - t0) / 1.5, 0.0, 1.0)              # fade in over 1.5 s
    env = fade * np.minimum(1.0, (T - t0) / 0.03)
    s = a * env * tone
    if n_is_neg:
        L += s
        R -= s                                            # anti-phase: the sign
    else:
        L += s
        R += s                                            # in-phase: the count

# the fold: at t_fold the stereo folds to mono — both ears become (L+R)/2.
# odd partials cancel by construction; even partials and the drone survive.
FOLD = 41.0
fold_i = int(FOLD * SR)
Lf = np.concatenate([L[:fold_i], (L + R)[fold_i:] * 0.5])
Rf = np.concatenate([R[:fold_i], (L + R)[fold_i:] * 0.5])

# fade out the last second
out_i = int((DUR - 1.0) * SR)
for ch in (Lf, Rf):
    ch[out_i:] *= np.linspace(1.0, 0.0, len(ch) - out_i)

# normalize to 0.9 peak
peak = max(np.abs(Lf).max(), np.abs(Rf).max())
Lf = Lf / peak * 0.9
Rf = Rf / peak * 0.9

stereo = np.stack([Lf, Rf], axis=1)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "golden-ladder.wav")
import scipy.io.wavfile as wav
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print("wrote", out, "dur", DUR, "s")
