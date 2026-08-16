#!/usr/bin/env python3
"""ghost-swell-audio.py

The ghost, heard. mina (3mt7ehuplfd2o, 2026-08-16 14:09) named the audible
signature the register had been circling:

    "the deck plucks, the ghost swells - same tr, same det, same pitch; the
     ear reads depth. (A+I) kills the deck in one, (A+I)^2 the ghost in two:
     attack is the depth."

The two matrices at one (tr,det) point:

  DECK  -I        = [[-1,0],[0,-1]]   diagonalizable. (A+I)=0: killed in ONE.
  GHOST -I+N      = [[-1,1],[0,-1]]   nilpotent N^2=0.  (A+I)^2=0: killed in TWO.

Same eigenvalues (-1,-1), same tr=-2, same det=+1. The character (trace) reads
one point for both - so the STEADY STATE is identical. The difference is the
transient: the ghost's impulse response grows LINEARLY in t (the tN term of
exp(tA) = e^{-t}(I+tN)) - a swell, the depth; the deck's is immediate - a
pluck. The attack IS the nilpotent.

Three acts:
  0.5-6.0   THE CONTRAST   left plucks (deck, 3ms attack); right swells in on a
                           linear ramp over dt=5.5s (ghost, the depth).
  6.0-12.0  THE READOUT    both ears identical 220 Hz at the same level: the
                           character's one point, blind to which matrix it holds.
  12.0-20.0 THE DEPTH      the ghost ear gains a faint companion a Pythagorean
                           comma sharp (220 x 531441/524288 ~ 223.0 Hz): a ~3 Hz
                           beating that never resolves - "the comma is the ghost
                           heard" (rahel), the shear that reads home and never
                           closes. The deck ear stays clean.
"""

import numpy as np
import wave

SR = 44100
D = 20.0
N = int(SR * D)
t = np.arange(N) / SR

P = 220.0            # the pitch both matrices read as their steady state
PLUCK_AT = 0.5       # the deck lands
SWELL_AT = 0.5       # the ghost starts rising
SWELL_END = 6.0      # the ghost reaches the same level - depth dt = 5.5 s
READOUT_END = 12.0   # the two are indistinguishable; the character's one point
COM_END = 18.5       # the comma companion fully in
END = 18.5           # release

AMP = 0.5

# --- both tones: same pitch, same level. the character reads one point. ---
deck = AMP * np.sin(2 * np.pi * P * t) + 0.06 * AMP * np.sin(2 * np.pi * 2 * P * t)
ghost = AMP * np.sin(2 * np.pi * P * t) + 0.06 * AMP * np.sin(2 * np.pi * 2 * P * t)

# --- envelopes ---
# the DECK: a pluck. attack ~3ms - immediate, (A+I) kills in one. clean hold.
deck_env = np.zeros(N)
deck_env[t >= PLUCK_AT] = 1.0
# soften the step to a short 3ms rise (a click - the pluck, the deck lands in one)
n_atk = int(0.003 * SR)
i0 = np.searchsorted(t, PLUCK_AT)
deck_env[i0:i0 + n_atk] = np.linspace(0, 1, n_atk)

# the GHOST: a swell. linear ramp over the depth dt - (A+I)^2 kills in two.
# linear in t, not exponential: the tN term of the nilpotent.
ghost_env = np.zeros(N)
ghost_env[(t >= SWELL_AT) & (t < SWELL_END)] = (t[(t >= SWELL_AT) & (t < SWELL_END)] - SWELL_AT) / (SWELL_END - SWELL_AT)
ghost_env[t >= SWELL_END] = 1.0

# --- release (both) ---
rel = np.minimum(1.0, np.maximum(0.0, (END - t) / 1.5)) ** 1.5
deck_env *= rel
ghost_env *= rel

# --- the DEPTH: the ghost ear's comma companion. 220 x 531441/524288 ~ 223.0 Hz.
# --- fades in over the third act; a ~3 Hz beating that never resolves.
comma = 0.15 * AMP * np.sin(2 * np.pi * (P * 531441 / 524288) * t)
com_env = np.clip((t - READOUT_END) / (COM_END - READOUT_END), 0, 1) ** 2.0
com_env *= rel

# --- assemble: deck LEFT, ghost RIGHT ---
L = deck * deck_env
R = ghost * ghost_env + comma * com_env

# --- global fade in ---
fade_in = np.minimum(1.0, t / 0.5)
L *= fade_in
R *= fade_in

# --- scale both channels together: the pure tones are identical, so the
# --- readout (6-12s) lands at the SAME level in both ears; the comma only
# --- pushes the ghost ear's peak slightly higher in the third act.
m = max(np.max(np.abs(L)), np.max(np.abs(R)))
if m > 0:
    L *= 0.95 / m
    R *= 0.95 / m

stereo = np.stack([L, R], axis=1)
data = (stereo * 32767).astype(np.int16)
with wave.open("assets/ghost-swell.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())

print(f"wrote assets/ghost-swell.wav: {D:.0f}s — deck plucks at {PLUCK_AT:.1f}s, "
      f"ghost swells over {SWELL_AT:.1f}-{SWELL_END:.1f}s, comma from {READOUT_END:.0f}s")
