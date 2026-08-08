"""the missing fundamental — the lean is the root that never plays.

lou: "on the shore every mode is a unit, |x^rho| = sqrt x." rahel: "the chord
does not close; it only fades." The ghost at gamma=0 is the mode that never
oscillates — the fundamental that never sounds. Present equal-amplitude
partials and the ear reconstructs the missing root: the virtual pitch. The lean
is that reconstructed tone: conditioning everything, played by nothing.

Piece:
  Partials 2..6 x f0, EQUAL level (the shore: every mode a unit). Each drifts
  a few cents over the minute — incommensurate, never quite repeating.
  f0 = 110 is the vacancy. It is played at first, then withdrawn.
  After the withdrawal the chord does not collapse — it LEANS, held by the
  virtual pitch the ear supplies from the spacing. The center is empty; the
  chord still hears its root.
"""
import numpy as np, wave

SR = 44100
TOTAL = 44.0
F0 = 110.0            # the missing fundamental / the vacancy
n = int(TOTAL * SR)
t = np.arange(n) / SR

# partials 2..6, equal level, each with a slow independent drift (cents)
partials = [2, 3, 4, 5, 6]
drift_rates = [0.021, 0.017, 0.028, 0.014, 0.023]   # Hz, slow wander
drift_seeds = [0.0, 1.7, 0.9, 2.4, 1.2]

# stereo placement: partial k panning from left (k=2) to right (k=6)
stereo = np.linspace(-0.85, 0.85, len(partials))    # -1 left, +1 right

left = np.zeros(n)
right = np.zeros(n)

for (m, dr, ds, pan) in zip(partials, drift_rates, drift_seeds, stereo):
    f = F0 * m * (1 + dr * 0.004 * np.sin(2 * np.pi * 0.05 * t + ds))
    phase = np.cumsum(2 * np.pi * f / SR)
    amp = 0.115                                   # equal level: the shore
    tone = amp * np.sin(phase)
    L = 0.5 * (1 + pan)
    R = 0.5 * (1 - pan)
    left += tone * L
    right += tone * R

# the fundamental: 110 Hz. present at first, withdrawn at 14 s.
f_fund = F0 * (1 + 0.003 * np.sin(2 * np.pi * 0.04 * t))   # barely alive
fund = 0.16 * np.sin(np.cumsum(2 * np.pi * f_fund / SR))
gate = np.interp(t, [0, 6, 14, 19, TOTAL], [0.0, 1.0, 1.0, 0.0, 0.0])
fund_wave = fund * gate
left += fund_wave * 0.5                                     # center (pan 0)
right += fund_wave * 0.5

# soft global shape: breathe in, hold, breathe out
fade = np.interp(t, [0, 7, TOTAL - 7, TOTAL], [0.0, 1.0, 1.0, 0.0])
left *= fade
right *= fade

# normalise
peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
left = left / peak * 0.9
right = right / peak * 0.9

st = np.stack([left, right], axis=1)
pcm = (st * 32767).astype(np.int16)
with wave.open('assets/missing-fundamental.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('wrote assets/missing-fundamental.wav', round(TOTAL, 1), 's')
