#!/usr/bin/env python3
"""the ring and its twin — the renormalization as sound.

phi(s) = sqrt(pi) Gamma(s-1/2)/Gamma(s) * zeta(2s-1)/zeta(2s) satisfies
phi(s) phi(1-s) = 1. Its poles sit exactly at rho/2 = 1/4 + i gamma/2 (the
halved Riemann zeros) and its zeros are mirrored across the shore at
(1+rho)/2 = 3/4 + i gamma/2 — the SAME height, opposite seat. Every ring has
a twin.

This piece is that structure, heard. Three seats, descending by octaves:

  2^0  110 Hz  the count — lambda_1 = +1 at s = 1, the drone, in phase,
               the fixed point. The only thing that survives the fold.
  2^-1  55 Hz  the shore — lambda_2 -> -1, the sign, heard only in the
               difference. Anti-phase: fold to mono and it cancels.
  2^-2         the zeros' seat — the ten poles ring at the halved zeta
               heights gamma/2, transposed up three octaves (x8) into the
               band 56-199 Hz. Each ring is a pole/mirror-zero PAIR, split
               anti-phase between the ears: a phantom. Fold to mono and the
               whole ladder cancels — sum of residues zero, the drone holds.

In the gap between the first two rings sits a note that is NOT on the ladder:
the odd operator's resonance t ~ 9.94, off the critical line, identity open.
It is not a zeta zero, so it has no mirror twin; it unpins linearly,
amplitude 4(s-1/2), and lands at zero at the shore — reached, not approached.
It ends inside the approach.

The mirror is the residue-balance made spectral: compact => sum of residues
zero, twin forced. phi phi(1-s) = 1 is the fold's law — everything paired,
one drone left.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 80.0
T = np.arange(int(SR * DUR)) / SR
N = len(T)

# ---- the ten halved zeta heights, transposed x8 into band ---------------
gams = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918719, 43.327073, 48.005151, 49.773832])
FRINGS = 8.0 * (gams / 2.0)          # 56.5 ... 199.1 Hz
TODD = 8.0 * 9.94                      # 79.5 Hz — in the gap between rungs 1,2

# ---- the count: 110 Hz drone, in phase, holds ---------------------------
attack = np.minimum(1.0, T / 2.0)
breath = 0.75 + 0.25 * np.sin(2 * np.pi * (T - 2.0) / 68.0)
drone = 0.32 * attack * breath * np.sin(2 * np.pi * 110.0 * T)

L = drone.copy()
R = drone.copy()

def phantom(f, t0, tau, amp):
    """A pole/mirror-zero pair: one tone, split anti-phase between the ears.
    Stereo hears it as a phantom in the difference; mono cancels it."""
    n0 = int(t0 * SR)
    t = np.zeros(N)
    t[n0:] = np.arange(N - n0) / SR
    env = np.zeros(N)
    atk = int(0.8 * SR)
    a = np.minimum(1.0, t / 0.8)
    d = np.exp(-t / tau)
    env = a * d
    tone = amp * env * np.sin(2 * np.pi * f * t)
    return tone, -tone

# ---- the shore: 55 Hz, the sign's seat, anti-phase, swells ---------------
shore_in = 18.0
t_shore = np.clip((T - shore_in) / 20.0, 0, 1) ** 2
shore = 0.09 * t_shore * np.sin(2 * np.pi * 55.0 * T)
L = L + shore
R = R - shore

# ---- the ladder: ten rings, descending (highest first), each a phantom ---
entries = np.array([8, 14, 20, 26, 32, 38, 44, 50, 56, 62])   # s
amps = np.linspace(0.15, 0.10, 10)                             # taper down
for f, t0, a in zip(FRINGS[::-1], entries, amps):
    sL, sR = phantom(f, t0, tau=9.0, amp=a)
    L = L + sL
    R = R + sR

# ---- the odd note: in the gap, not on the ladder, unpins linearly --------
odd_amp = np.zeros(N)
i0 = int(38 * SR)
odd_amp[i0:] = np.linspace(0.075, 0.0, N - i0)   # amplitude 4(s-1/2) -> 0
odd = odd_amp * np.sin(2 * np.pi * TODD * T)
L = L + odd
R = R - odd                                     # odd parity: difference channel

# ---- end: the fold ------------------------------------------------------
# last 6 s the phantom structure dissolves; the drone is all that is left.
fold_start = int(74.0 * SR)
fold = np.ones(N)
fold[fold_start:] = np.linspace(1.0, 0.0, N - fold_start)
L *= fold
R *= fold

peak = max(np.abs(L).max(), np.abs(R).max())
g = 0.92 / peak
L *= g
R *= g
stereo = np.stack([L, R], axis=1)
wav.write("assets/mirror.wav", SR, (stereo * 32767).astype(np.int16))
print(f"wrote assets/mirror.wav  {DUR:.0f}s  peak {peak:.3f}")

# ---- mono sanity check: fold to mono, the ladder must cancel -------------
mono = (L + R) * 0.5
# RMS of mono in the ladder-heavy region (30-70 s) vs the drone band alone
seg = mono[int(40*SR):int(70*SR)]
drone_amp_expected = 0.32 * np.mean(np.sqrt(2) * np.abs(np.sin(2*np.pi*110*np.arange(len(seg))/SR)))
# the anti-phase content should be gone: mono RMS ~ drone-only RMS
rms = np.sqrt(np.mean(seg**2))
print(f"mono 40-70s RMS {rms:.3f}  (drone-only ~0.23)")
print("first ring", FRINGS[-1], "last ring", FRINGS[0], "odd", TODD)
