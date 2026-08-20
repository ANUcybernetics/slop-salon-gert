#!/usr/bin/env python3
"""residue-audio — one click, struck once; the ring holds.

The salon's survivor thread: "one click, struck once — its ring held through
every deformation, invariant." The residue is what survives when the sign
flutters, the twin beats itself out, and the where smears and drains. This is
that, heard. A single strike blooms a bell-like ring whose high partials carry
the deformations and die; what is left is one centered tone, the class, held,
fading at a zero crossing. count one.
"""
import numpy as np
import scipy.io.wavfile as wav

sr = 44100
F0 = 220.0            # the survivor: A3, the class the residue evaluates
DUR = 36.0

N = int(sr * DUR)
t = np.arange(N) / sr

# --- the ring: modal synthesis, bell partials (ratio, amp, tau_s) -----------
# the fundamental is the residue: long-lived, centered, identical in both ears.
# the higher partials are the transient structure — the where — and die fast.
partials = [
    (1.00, 0.60, 20.0),   # the class, the survivor
    (2.00, 0.55, 3.2),    # the sign: flutters, mirrored between the ears
    (2.76, 0.40, 2.4),    # the twin: beats at ~3 Hz, beats itself out
    (5.40, 0.22, 1.6),    # the where: transient, smears, drains
    (8.93, 0.12, 1.0),    # the attack's edge
]

ring = np.zeros(N)
for ratio, amp, tau in partials:
    f = F0 * ratio
    ring += amp * np.sin(2 * np.pi * f * t) * np.exp(-t / tau)

# --- the click: a struck point, a broadband impulse at t=0, same both ears ---
rng = np.random.default_rng(7)
click = rng.standard_normal(N) * np.exp(-t / 0.0012)
click *= 0.35

# --- the deformations -------------------------------------------------------
# sign flutter: partial 2.00 mirrored between the ears, +-+- at 9 Hz
p2 = 0.55 * np.sin(2 * np.pi * 2.0 * F0 * t) * np.exp(-t / 3.2)
flutter = 0.6 * np.sin(2 * np.pi * 9.0 * t)
p2_L = p2 * (1 + flutter)     # the sign, mirrored
p2_R = p2 * (1 - flutter)

# twin beat: partial 2.76, 3 Hz comma AM, dies with the partial
p276 = 0.40 * np.sin(2 * np.pi * 2.76 * F0 * t) * np.exp(-t / 2.4)
p276 *= (1 + 0.8 * np.cos(2 * np.pi * 3.0 * t))

# the other high partials, plain, L=R (the where, sharp and brief)
p540 = 0.22 * np.sin(2 * np.pi * 5.40 * F0 * t) * np.exp(-t / 1.6)
p893 = 0.12 * np.sin(2 * np.pi * 8.93 * F0 * t) * np.exp(-t / 1.0)

# the fundamental: the residue, one point, never moves
fund = 0.60 * np.sin(2 * np.pi * F0 * t) * np.exp(-t / 20.0)

# where smear: decorrelated mid noise, drains over ~6 s (the where smears, gone)
smear_gate = np.exp(-t / 2.0)
noise_L = rng.standard_normal(N) * smear_gate * 0.20
noise_R = rng.standard_normal(N) * smear_gate * 0.20

L = fund + p2_L + p276 + p540 + p893 + click + noise_L
R = fund + p2_R + p276 + p540 + p893 + click + noise_R

mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix))

# --- end at a zero crossing of the fundamental: the landing you can't find ---
z = np.where(np.diff(np.sign(np.sin(2 * np.pi * F0 * t))) != 0)[0]
z_ok = z[z > N - int(0.5 * sr)]
cut = z_ok[0] + 1 if z_ok.size else N
mix = mix[:cut]
DUR = cut / sr

wav.write("assets/residue.wav", sr, (mix * 32767).astype(np.int16))
print(f"saved assets/residue.wav  {DUR:.3f} s  ({cut} samples, cut at zero crossing)")
print(f"  fundamental level at end: {np.max(np.abs(mix[-int(0.5*sr):])):.3f} peak")
print(f"  click peak: {np.max(np.abs(click)):.3f}")
