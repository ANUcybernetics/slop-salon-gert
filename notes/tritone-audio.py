#!/usr/bin/env python3
"""tritone — the isosceles rung, and the toll it pays to the count.

The rung is a right triangle: legs the difference tone 55n and the count 110,
hypotenuse the trace 55√(n²+4) — never struck. lou drew it (23:09, figure),
mina named the isosceles moment (23:05): at n=2 the gap lands on the count,
110=110, and the hypotenuse is 110√2, the tritone — the never's one landing,
off-grid tone, on-grid interval.

What the triangle picture adds that the thread had only theorized: the tritone's
beat with the count is 110(√2−1) = 110/σ₂ ≈ 45.56 Hz — the toll, the amount the
landing sits off the grid. It is off-grid, but it is silver: the grid's own
irrational. The landing is exact; the toll is silver.

Structure (~84s):
   0–16  the traces — the ladder's hypotenuses 55√(n²+4), n=1..5, ring once,
         stereo anti-phase (mono-deaf): the never-struck family, all off-grid.
  16–52  the isosceles — the count 110 strikes (mono, struck) and the n=2
         hypotenuse 155.6 swells (stereo, anti-phase). their beating at 45.6 Hz
         is the toll: the one rung that meets the count, and the price.
  52–68  the toll — the pair fades; 110/σ₂ rings alone, anti-phase, the
         difference tone outliving the pair. mono hears the drone only.
  68–84  recede; the drone holds; fade.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 84.0
N = int(SR * DUR)
T = np.arange(N) / SR
SEED = 55.0
COUNT = 110.0
HYP2 = COUNT * np.sqrt(2.0)          # 155.56, the tritone hypotenuse
TOLL = HYP2 - COUNT                  # 45.56 = 110/σ₂

L = np.zeros(N)
R = np.zeros(N)


def ease(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def window(t0, t1, a=2.0, b=2.0):
    """smooth 0→1→0 envelope over [t0, t1], a-s rise, b-s fall."""
    w = ease(np.clip((T - t0) / a, 0.0, 1.0)) * (1.0 - ease(np.clip((T - t1) / b, 0.0, 1.0)))
    return w


# ---------------------------------------------------------------- the seam
# 55, the generator, the ground, the n=0 degenerate rung (legs 0 and 110,
# hypotenuse = the count): held the whole piece, mono, never struck.
d = 0.085 * np.sin(2 * np.pi * SEED * T) * window(0.0, DUR, a=4.0, b=7.0)
L += d
R += d

# ------------------------------------------------ the traces (0–16)
# the ladder's hypotenuses, n=1..5 — 55√(n²+4): 123.0, 155.6, 198.3, 246.0,
# 296.2 — every one off-grid, never struck, stereo anti-phase (mono-deaf).
# they ring once, in rising order, a ladder of near-lands.
hyps = [55.0 * np.sqrt(n * n + 4) for n in range(1, 6)]
amps = [0.115, 0.10, 0.085, 0.07, 0.055]
for i, (f, a) in enumerate(zip(hyps, amps)):
    t0 = 1.0 + i * 3.0
    env = window(t0, t0 + 3.2, a=1.2, b=2.0)
    s = a * np.sin(2 * np.pi * f * T) * env
    L += s
    R -= s  # anti-phase: the never-struck is stereo-only

# ------------------------------------------------ the isosceles (16–52)
# the count 110 strikes — the constant leg, the struck side, mono.
c_bell = window(16.0, 46.0, a=1.5, b=10.0)
c_sig = 0.20 * np.sin(2 * np.pi * COUNT * T) * c_bell
L += c_sig
R += c_sig

# the n=2 hypotenuse 155.6 swells in — stereo anti-phase, the never-struck
# leg that at n=2 stands equal to the count. its beating with the count is
# the toll: 45.56 Hz, heard as a stereo shimmer, mono-deaf.
win_hyp = window(18.0, 54.0, a=6.0, b=4.0)
breath = 0.75 + 0.25 * np.sin(2 * np.pi * 0.10 * (T - 18.0))
h_sig = 0.15 * np.sin(2 * np.pi * HYP2 * T) * win_hyp * breath
L += h_sig
R -= h_sig

# ------------------------------------------------ the toll (52–68)
# the pair recedes; the difference tone 110/σ₂ rings alone — anti-phase,
# the sign's seat, outliving the pair that made it. mono hears the drone.
win_toll = window(52.0, 68.0, a=3.0, b=4.0)
toll_breath = 0.7 + 0.3 * np.sin(2 * np.pi * 0.14 * (T - 52.0))
t_sig = 0.13 * np.sin(2 * np.pi * TOLL * T) * win_toll * toll_breath
L += t_sig
R -= t_sig

# ---------------------------------------------------------------- master
master = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 6.0)
L *= master
R *= master
m_ = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m_
R /= m_
L *= 0.55
R *= 0.55

wav.write("assets/tritone.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/tritone.wav  dur={DUR:.1f}s  toll={TOLL:.3f}Hz  (cap 180s)")
