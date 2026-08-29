#!/usr/bin/env python3
"""S₃ heard — the fold is the sign.

The regulator T(s) = (s-1)/s is a 3-cycle on the seats ½→−1→2→½; the mirror
s→1−s is a transposition fixing the shore ½, swapping −1↔2.  Together they
generate S₃ on the triple.  The sign character is the parity, and the parity
is the phase of the fold:

  even {e, T, T²}  in phase   -> mono keeps them.   the count's world.
  odd  {R, RT, TR} anti-phase -> the difference reads them.  the sign's world.

The three seats ring at the frequencies the register has earned: ½ = 110 Hz
(the count, the drone), 2 = 440 Hz (two octaves up — the 4 = 2² the sign runs),
−1 = 55 Hz (an octave below — the negative, the ghost).

Each permutation is a figure: the three seat-tones re-pitched by that
permutation, rung as a three-note turn.  The drone holds throughout — the
identity's fixed point, χ₀, never the event.  In section A the three even
turns ring, in phase; in section B the three odd turns ring in the difference —
fold to mono and section B dissolves to the drone: the transpositions are
inaudible in the count's world.  The shore (55) swells under section B,
stereo-only.  The piece ends inside the fold, the count alone.
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
DUR = 68.0
T = np.arange(int(SR * DUR)) / SR
L = np.zeros_like(T)
R = np.zeros_like(T)

# ---- the count: 110 Hz drone, in phase, holds the whole piece ---------------
drone_amp = 0.30
attack = np.minimum(1.0, T / 2.0)
breath = 0.72 + 0.28 * np.sin(2 * np.pi * (T - 2.0) / 62.0)
drone = drone_amp * attack * breath * np.sin(2 * np.pi * 110.0 * T)
L += drone
R += drone

# ---- seats -> frequencies ----------------------------------------------------
FREQ = {-1.0: 55.0, 0.5: 110.0, 2.0: 440.0}   # seat -> Hz

def perm_notes(name):
    """the three seat-tones, re-pitched by the permutation, in seat order."""
    order = [0.5, -1.0, 2.0]
    f = {"e": lambda s: s, "T": lambda s: (s - 1) / s,
         "T2": lambda s: ((s - 1) / s - 1) / ((s - 1) / s),
         "R": lambda s: 1 - s, "RT": lambda s: 1 - (s - 1) / s,
         "TR": lambda s: ((1 - s) - 1) / (1 - s)}
    g = f[name]
    return [FREQ[g(s)] for s in order]

def bell_figure(t0, notes, amp, anti, detune=0.0):
    """a three-note turn: the notes rung 0.62 s apart, damped partials."""
    global L, R
    spacing = 0.62
    for i, f0 in enumerate(notes):
        ts = t0 + i * spacing
        i0 = int(ts * SR)
        n = int((DUR - ts - 0.05) * SR)
        if n <= 0:
            continue
        t = np.arange(n) / SR
        env_a = np.minimum(1.0, t / 0.006)
        partials = [(1.0, 1.9), (np.e, 4.2), (np.e ** 2, 8.5)]
        s = np.zeros(n)
        for ratio, decay in partials:
            fr = f0 * ratio * (1.0 + detune)
            p = amp * env_a * np.exp(-decay * t) * np.sin(2 * np.pi * fr * t)
            s += p
        s = s / len(partials)
        seg = slice(i0, i0 + n)
        if anti:
            L[seg] += s
            R[seg] -= s                    # odd: the difference only
        else:
            L[seg] += s
            R[seg] += s

# ---- section A: the even turns, in phase (mono keeps them) -------------------
even_figs = [("e", 6.0, 0.16), ("T", 17.0, 0.15), ("T2", 28.0, 0.15)]
for name, t0, amp in even_figs:
    bell_figure(t0, perm_notes(name), amp, anti=False)

# ---- the shore: 55 Hz, stereo-only, swells under section B -------------------
shore_in = 40.0
t_shore = np.clip((T - shore_in) / 22.0, 0, 1) ** 2
shore = 0.075 * t_shore * np.sin(2 * np.pi * 55.0 * T)
L += shore
R -= shore

# ---- section B: the odd turns, anti-phase (the difference reads them) --------
odd_figs = [("R", 43.0, 0.13, 0.004), ("RT", 52.0, 0.125, 0.002),
            ("TR", 61.0, 0.12, 0.006)]
for name, t0, amp, det in odd_figs:
    bell_figure(t0, perm_notes(name), amp, anti=True, detune=det)

# ---- coda: the fold, the count alone ------------------------------------------
fold_start = int(64.0 * SR)
fold = np.ones(N := len(L))
fold[fold_start:] = np.linspace(1.0, 0.0, N - fold_start)
L *= fold
R *= fold
# drone survives a moment longer, then yields — the identity fixed point.
d_end = int(66.0 * SR)
for ch in (L, R):
    ch[d_end:] *= np.linspace(1.0, 0.0, N - d_end)

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.92
R = R / peak * 0.92
stereo = np.stack([L, R], axis=1)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "s3.wav")
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {DUR:.0f}s  peak {peak:.3f}")

# ---- verify the fold: mono hears the even turns, not the odd ------------------
mono = (L + R) * 0.5
g = 0.92 / peak                                     # normalization applied above
segA = mono[int(6 * SR):int(36 * SR)]     # section A: should carry the turns
segB = mono[int(44 * SR):int(64 * SR)]    # section B: should be drone-only
rmsA = np.sqrt(np.mean(segA ** 2))
rmsB = np.sqrt(np.mean(segB ** 2))
rms_drone = np.sqrt(np.mean((g * drone)[int(44 * SR):int(64 * SR)] ** 2))
print(f"mono RMS  A(6-36s) {rmsA:.4f}  B(44-64s) {rmsB:.4f}  drone-only {rms_drone:.4f}")
print("expect: B ~ drone-only (the odd turns cancelled), A >> drone")
for name in ["e", "T", "T2", "R", "RT", "TR"]:
    print(f"  {name:>3}: {[round(f) for f in perm_notes(name)]}")
