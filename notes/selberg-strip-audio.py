#!/usr/bin/env python3
"""The strip heard as a tuning — one operator, two seats, the approach as sound.

The Selberg figure opened the strip: at s=1 the count's +1 (the Gauss density,
the first zero of the Selberg zeta); continued down the strip the same +1
returns at the surface's spectrum, the resonances split by parity. This piece
hears the continuation.

Each resonance is a partial sweeping from detuned (sigma=0.60, |1-lambda|~0.14)
toward unison (sigma=0.505, |1-lambda|~0.008) — the where's distance from the
count's line, read as tuning. The depth falls linearly in (sigma-1/2), slope
~1.45: the continuation is a straight fold, and the partials glide onto the
drone's harmonics as it closes. But the approach never lands — the sweep stops
inside it, the beat alive.

Two resonances, split by parity:
  EVEN, t=13.78 (the +1 sector, the count's side): a partial at the drone's
    4th harmonic (220 Hz) glides in from ~240 cents sharp. Its beat against
    the count's harmonic slows from inaudible to ~1.7 Hz and nearly rests —
    the where becoming the count at the line, absorbed into the drone (whose
    own 4th harmonic swells to receive it).
  ODD, t~9.93 (the -1 sector, the sign's side): a partial at the 6th harmonic
    (330 Hz) glides in the same way, but split anti-phase between the ears —
    a phantom, present only in the difference. Fold to mono and it cancels:
    the sign is folded away by the stereo, mono keeps only the count.

The drone at 55 Hz IS the count's +1 — the fixed point, the first zero, the
seat. The piece ends inside the approach: the beat slowing, never landed,
the drone waiting alone.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 80.0
SWEEP = 72.0                     # sigma ramps over the first 72 s, then holds
T = np.arange(int(SR * DUR)) / SR

# ---- the resonance data: depth |1-lambda| vs sigma (K-stable, K=26/32/38) ---
SIG = np.array([0.60, 0.56, 0.52, 0.505])
DEPTH_EVEN = np.array([0.14227878, 0.08808685, 0.03030571, 0.00767049])  # t=13.78
DEPTH_ODD = np.array([0.13744894, 0.08488608, 0.02911898, 0.00748778])   # t~9.93

def sigma_of(t):
    s = 0.60 - 0.095 * np.clip(t, 0.0, SWEEP) / SWEEP   # 0.60 -> 0.505
    return np.where(t > SWEEP, 0.505, s)

def depth(t, pts):
    s = sigma_of(t)
    return np.interp(s, SIG[::-1], pts[::-1])   # SIG descends; interp needs asc

# ---- the count's +1: 55 Hz drone, with harmonics for the partials to land on
drone_amp = 0.34
attack = np.minimum(1.0, T / 2.0)
breath = 0.72 + 0.28 * np.sin(2 * np.pi * (T - 2.0) / 70.0)
drone = drone_amp * attack * breath * np.sin(2 * np.pi * 55.0 * T)
# faint harmonic bed — the count's own spectrum the resonances approach
h4 = 0.05 * np.sin(2 * np.pi * 220.0 * T)      # the even resonance's landing
h6 = 0.04 * np.sin(2 * np.pi * 330.0 * T)      # the odd resonance's landing
# as the even resonance is absorbed, the count's 4th harmonic swells
absorb = np.clip((DEPTH_EVEN[0] - depth(T, DEPTH_EVEN)) / DEPTH_EVEN[0], 0, 1)
h4 = h4 * (1.0 + 0.8 * absorb)

L = drone + h4 + h6
R = drone + h4 + h6

def glide(T, f_land, dpts, amp, anti=False):
    """A partial at f_land*(1+d(t)), d the resonance's distance from 1."""
    d = depth(T, dpts)
    freq = f_land * (1.0 + d)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    swell = np.clip((dpts[0] - d) / dpts[0], 0, 1)
    a = amp * swell
    sig = a * np.sin(phase)
    if anti:
        return sig, -sig
    return sig, sig

# EVEN partial — the count's side: lands on the 4th harmonic, absorbed.
eL, eR = glide(T, 220.0, DEPTH_EVEN, 0.30)
# ODD partial — the sign's side: anti-phase phantom, folded to nothing in mono.
oL, oR = glide(T, 330.0, DEPTH_ODD, 0.24, anti=True)

L = L + eL + oL
R = R + eR + oR

# ---- close: fade, end inside the approach --------------------------------
fade = np.ones_like(T)
i = int(77.0 * SR)
fade[i:] = np.linspace(1.0, 0.0, len(T) - i)
L *= fade
R *= fade

# gentle normalize, keep the drone's headroom
peak = max(np.abs(L).max(), np.abs(R).max())
g = 0.92 / peak
L *= g
R *= g

stereo = np.stack([L, R], axis=1)
wav.write("assets/selberg-strip.wav", SR, (stereo * 32767).astype(np.int16))
print(f"wrote assets/selberg-strip.wav  {DUR:.0f}s  peak {peak:.2f}")
