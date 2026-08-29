#!/usr/bin/env python3
"""χ₂ heard — the winding the parity can't read.

S₃ on the seats {−1, ½, 2}. The sign character (the fold, mono/diff) hears the
parity: even {e, T, T²} in phase, odd {R, RT, TR} anti-phase — that was the S₃
piece.  What the parity never hears is the regulator: all three even elements
get +1 from both 1-dim characters, so the fold cannot tell e from T from T².

The 2-dim character χ₂ tells them apart, as a winding.  In the standard rep:

  e  →  identity           trace +2   the count, in phase
  T  →  rotation by 120°   trace −1   the regulator, a winding
  R  →  reflection         trace  0   the mirror, mono-invisible

χ₂ is a stereo pair: L/R = the two seats {−1, 2} = {55, 440}.  Fold to mono
projects onto the shore (the mirror's +1 line) — the count; the difference is
the mirror's −1 line — the where.  A transposition (trace 0) rings in the
difference: mono can't hear it.  A 3-cycle is a rotation: it takes the count's
in-phase image and winds it into the difference — the mono loses half
(χ₂(T) = −1), the diff gains the winding.

The shore ½ (110 Hz) is the drone, the identity's fixed point — χ₀, the count.
The turns ring only the pair {55, 440} — the two seats χ₂ moves.

And [R, T] = T: the commutator of two mirrors is the regulator.  The commutator
subgroup A₃ is exactly the even rotations — the winding is born of folds, and
the parity (trivial on commutators) can never reach it.  stereo reads it, mono
can't.
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
DUR = 66.0
T = np.arange(int(SR * DUR)) / SR
L = np.zeros_like(T)
R = np.zeros_like(T)

# ---- the count: 110 Hz drone, in phase, holds the whole piece ---------------
drone_amp = 0.30
attack = np.minimum(1.0, T / 2.0)
breath = 0.72 + 0.28 * np.sin(2 * np.pi * (T - 2.0) / 60.0)
drone = drone_amp * attack * breath * np.sin(2 * np.pi * 110.0 * T)
L += drone
R += drone

def pair_note(t0, f0, amp, uL, uR, detune=0.0):
    """one damped tone of the pair, placed at (uL, uR)·f0."""
    global L, R
    i0 = int(t0 * SR)
    n = int((DUR - t0 - 0.05) * SR)
    if n <= 0:
        return
    t = np.arange(n) / SR
    env_a = np.minimum(1.0, t / 0.006)
    partials = [(1.0, 2.2), (np.e, 4.6), (np.e ** 2, 9.0)]
    s = np.zeros(n)
    for ratio, decay in partials:
        s += amp * env_a * np.exp(-decay * t) * np.sin(2 * np.pi * f0 * ratio * (1.0 + detune) * t)
    s = s / len(partials)
    seg = slice(i0, i0 + n)
    L[seg] += uL * s
    R[seg] += uR * s

def winding(t0, amp, theta_g, detune=0.0):
    """a 3-cycle: the pair rings 0.8 s apart and each winds 0 → theta_g — the
    rotation, the count leaking into the difference."""
    for i, f0 in enumerate((55.0, 440.0)):
        tt = t0 + i * 0.8
        i0 = int(tt * SR)
        n = int((DUR - tt - 0.05) * SR)
        if n <= 0:
            continue
        t = np.arange(n) / SR
        th = np.minimum(1.0, t / 1.1) * theta_g          # the wind
        c, s = np.cos(th), np.sin(th)
        uL, uR = c - s, s + c                            # rot(θ)·(1,1)
        env_a = np.minimum(1.0, t / 0.006)
        partials = [(1.0, 2.2), (np.e, 4.6), (np.e ** 2, 9.0)]
        sig = np.zeros(n)
        for ratio, decay in partials:
            sig += amp * env_a * np.exp(-decay * t) * np.sin(2 * np.pi * f0 * ratio * (1.0 + detune) * t)
        sig = sig / len(partials)
        seg = slice(i0, i0 + n)
        L[seg] += uL * sig
        R[seg] += uR * sig

def mirror(t0, amp, detune=0.0):
    """a transposition: the pair rings anti-phase — χ₂ trace 0, mono-invisible."""
    pair_note(t0 + 0.0, 55.0, amp, 1.0, -1.0, detune)
    pair_note(t0 + 0.8, 440.0, amp, 1.0, -1.0, detune)

# ---- section A, 6–36s — the even turns: the count, and the winding -----------
pair_note(6.0, 55.0, 0.26, 1.0, 1.0)             # e on the pair: in phase
pair_note(6.8, 440.0, 0.26, 1.0, 1.0)
winding(16.0, 0.26, 2 * np.pi / 3)               # T: winds 120°, χ₂ = −1
winding(26.0, 0.26, 4 * np.pi / 3)               # T²: winds 240°

# ---- section B, 41–60s — the mirrors (trace 0), then their commutator --------
mirror(41.0, 0.24, detune=0.004)                 # R  — the mirror, mono-invisible
mirror(48.0, 0.24, detune=0.002)                 # RT — another mirror
winding(55.0, 0.24, 2 * np.pi / 3)               # [R,T]=T — two folds, one winding

# ---- coda: the fold, the count alone -----------------------------------------
fold_start = int(61.0 * SR)
fold = np.ones(len(L))
fold[fold_start:] = np.linspace(1.0, 0.0, len(L) - fold_start)
L *= fold
R *= fold
d_end = int(63.0 * SR)
for ch in (L, R):
    ch[d_end:] *= np.linspace(1.0, 0.0, len(L) - d_end)

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.92
R = R / peak * 0.92
stereo = np.stack([L, R], axis=1)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "chi2.wav")
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {DUR:.0f}s  peak {peak:.3f}")

# ---- verify: fold reads the count, diff reads χ₂ -----------------------------
g = 0.92 / peak
def mr(seg): return np.sqrt(np.mean(seg ** 2))
mono = (L + R) * 0.5
diff = (L - R) * 0.5
print("\npair placement per deck (mono, diff) — the exact character read:")
place = {"e": (1.0, 0.0), "T": (-0.5, -0.866), "T2": (-0.5, 0.866),
         "R": (0.0, -1.0), "RT": (0.0, -1.0), "TR": (0.0, -1.0)}
for k, v in place.items():
    print(f"  {k:>3}:  mono {v[0]:+.3f}   diff {v[1]:+.3f}    (χ₂: e=2, T,T²=−1, R,RT,TR=0)")
print("\nfigure windows (drone subtracted from mono):")
print("  figure         mono      mono−drone    diff")
for label, t0 in [("e", 6.0), ("T", 16.0), ("T2", 26.0),
                  ("R", 41.0), ("RT", 48.0), ("[R,T]=T", 55.0)]:
    seg = slice(int(t0 * SR), int((t0 + 3.0) * SR))
    m, d = mono[seg], diff[seg]
    dn = mr((g * drone)[seg])
    print(f"  {label:>8}:  {mr(m):.4f}  {mr(m)-dn:+.4f}      {mr(d):.4f}")
