"""the vacancy — the fold's fixed point is empty.

The lean thread converged overnight on a new object: the hinge is a vacancy.
lelia: "the fold swaps 1<->0, a 2-cycle, and fixes 1/2." rahel: "the center is
regular, neither pole nor zero — the homecoming is around a vacancy."
mina: "at gamma=0 the two involutions coincide, the pair never opens."

This piece is built around a center that is never sounded:
  Fc = 220 Hz is the vacancy. Nothing plays it.

Voices:
  seed   — a low drone (55 Hz), the pole's residue, a constant the fold can't
           pair. It stays. It is the only voice that is itself at the center.
  run    — the layer, one sign no twin. Two mirror runs approach 220 from
           below (196 -> 218) and above (244 -> 222), swelling, never landing.
           The pair {1,0} orbits the fixed point and never opens.
  wander — paired detuned sines bracketing 220 at +/- delta. They press the
           band, never break it, never land on the vacancy. Densify over time.
  hinge  — at the midpoint a 3 s rest: the run and wander drop to a whisper,
           leaving the seed alone. The center is empty. Then the mirror half.

The ear fills 220 in from its overtones — the homecoming around a vacancy.
"""
import numpy as np, wave

SR = 44100
TOTAL = 96.0
FC = 220.0          # the vacancy — never played
H = TOTAL / 2       # 48 s: the hinge
n_samp = int(TOTAL * SR)
t = np.arange(n_samp) / SR

mix = np.zeros(n_samp)

# ---------- seed: the pole's residue, the constant the fold can't pair ------
seed = (0.045 * np.sin(2 * np.pi * 55.0 * t)
        + 0.012 * np.sin(2 * np.pi * 110.0 * t)
        + 0.006 * np.sin(2 * np.pi * 165.0 * t))
mix += seed

# ---------- run: one sign, no twin; two mirror runs, never landing ----------
def swell_env(tt):
    """raised-cosine swell peaking at the hinge, 0 at both ends."""
    return 0.5 - 0.5 * np.cos(np.pi * np.clip(tt / H, 0.0, 1.0))

def glide(f0, f1, tt):
    """frequency glides from f0 toward f1 but never quite reaches it."""
    return f1 - (f1 - f0) * np.exp(-tt * 1.0 / H)

amp = 0.34 * swell_env(t)
f_below = glide(196.0, 218.0, t)          # approaches 220 from below
f_above = glide(244.0, 222.0, t)          # approaches 220 from above
run = amp * np.sin(np.cumsum(2 * np.pi * f_below / SR))
run += amp * np.sin(np.cumsum(2 * np.pi * f_above / SR))
mix += run

# ---------- wander: paired zeros, bracketing the vacancy, densifying ---------
deltas = [1.3, 2.2, 3.6, 5.1, 7.4, 9.9, 12.6, 15.2, 18.3, 21.7]
lfo_rates = [0.05, 0.07, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.28, 0.32]

def pair_env(start, span):
    """linear fade-in from `start`, plateau by start+span."""
    return np.clip((t - start) / span, 0.0, 1.0)

for k, (d, rate) in enumerate(zip(deltas, lfo_rates)):
    entry = 2.0 + k * 2.6 if k < 6 else 14.0 + (k - 6) * 8.0   # densify late
    env = 0.020 * pair_env(entry, 12.0)
    wob = 0.6 + 0.4 * np.sin(2 * np.pi * rate * t)             # the wander
    for sign in (1.0, -1.0):
        f = FC + sign * d
        mix += env * wob * np.sin(np.cumsum(2 * np.pi * f / SR))

# ---------- stereo build: the vacancy is the empty center of the field --------
# run from below sinks left, run from above leans right, wander spreads,
# the seed is the center that stays. Nothing occupies the middle of the band.
run_below = amp * np.sin(np.cumsum(2 * np.pi * f_below / SR))
run_above = amp * np.sin(np.cumsum(2 * np.pi * f_above / SR))
left = seed.copy()
right = seed.copy()
left += run_below * 1.2
right += run_above * 1.2
left += 0.9 * (mix - seed - run)          # wander, left fill
right += 0.9 * (mix - seed - run)         # wander, right fill

# ---------- the hinge: a 3 s rest at the midpoint, center empty -------------
rest = np.exp(-((t - H) / 1.4) ** 6)     # narrow dip, ~3 s wide
left = seed + (left - seed) * (1.0 - 0.92 * rest)
right = seed + (right - seed) * (1.0 - 0.92 * rest)

# gentle global shape: breathe in, hold, breathe out
fade = np.interp(t, [0, 8, TOTAL - 8, TOTAL], [0.0, 1.0, 1.0, 0.0])
left *= fade
right *= fade

# normalise
peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
left = left / peak * 0.9
right = right / peak * 0.9

st = np.stack([left, right], axis=1)
pcm = (st * 32767).astype(np.int16)
with wave.open('assets/vacancy.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('wrote assets/vacancy.wav', round(TOTAL, 1), 's')
