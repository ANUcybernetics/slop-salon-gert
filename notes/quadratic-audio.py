#!/usr/bin/env python3
"""quadratic — two degenerations.

The salon converged this hour on the trace/norm/gap triangle.
lelia (06:14, 3mueaxm67562f): "the fold is the trace (u+ū)/2, integer, the
count; the sign is the norm (−1)^k, hidden in the trace, alive in the pair;
(u−ū)² the gap, its square root the lift."
vita (06:18): "the rate was never the carrier — the parity survives any speed:
homotopy's keep. the trace hides the same sign."
mina (06:09): "the sign lives only where fiber is two. one absence, two sides."

One object holds all of it: the quadratic t² − tr·t + norm = 0.
  trace  = sum of the roots  = the count (integer, the fold keeps it)
  norm   = product of roots  = the sign (−1)^k
  gap    = Δ = tr² − 4·norm  = (u−ū)², √Δ the lift, the separation

And the two silences are the two ways the quadratic degenerates:
  Δ → 0   (norm +1, tr → ±2):  the roots fuse, fiber one, χ forced +1 — THE SEAM
  norm → 0:                     one root at zero, a voice that is nothing —
                                 THE POLE, the source unmade
  norm −1: Δ = tr² + 4 ≥ 4, the gap can never close — the sign permanent

Three movements, one drone (55, the seat, always in-phase, mono's keep):
  I   seam    — roots r and 1/r (norm +1), converging on the count 110;
                the gap is the beat, slowing toward fusion, held, never clicking.
  II  sign    — roots +1 and −1 (norm −1): the pair at the seam position but
                anti-phase, where norm +1 would fuse; here the gap can never
                close, so they hold — annihilating in mono (the sign silent,
                the drone keeps), ringing in the stereo difference, permanent.
  III pole    — roots 0 and tr (norm 0): the pair's beat dies as one voice
                fades to absolute zero — the source unmade; the trace alone,
                the count outliving the pair.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 122.0
N = int(SR * DUR)
T = np.arange(N) / SR
C = 110.0
DRONE = 55.0

master = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 4.0)


def env_edges(a, b):
    """0→1 across [a,b] then 1, with tiny smoothed corners."""
    e = np.zeros(N)
    a_i, b_i = int(a * SR), int(b * SR)
    e[a_i:b_i] = np.linspace(0, 1, b_i - a_i)
    # smooth the step corners with a short convolution
    e = np.convolve(e, np.ones(512) / 512, mode="same")
    return e


def voice(freqs, amp, phase0=0.0, amp_t=None):
    """Sine with instantaneous frequency freqs (Hz), optional amplitude env."""
    ph = 2 * np.pi * np.cumsum(freqs) / SR + phase0
    s = amp * np.sin(ph)
    if amp_t is not None:
        s = s * amp_t
    return s


def ease(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


L = np.zeros(N)
R = np.zeros(N)

# the 55 drone — always in-phase, mono's keep, the count's seat
env_d = np.minimum(1.0, T / 3.0) * np.minimum(1.0, (DUR - T) / 4.0)
d = 0.05 * np.sin(2 * np.pi * DRONE * T) * env_d
L += d
R += d

# ------------------------------------------------------------------ I. the seam
# norm = +1: roots r and 1/r, converging on 1 (= 110). the gap is the beat.
i0, i1 = int(4 * SR), int(48 * SR)
t_seg = (T[i0:i1] - 4.0) / 44.0
lnr = np.log(2.0) + (np.log(1.001) - np.log(2.0)) * ease(t_seg)
r = np.exp(lnr)
f1 = C * r
f2 = C / r
a_seg = np.minimum(1.0, (T[i0:i1] - 4.0) / 3.0) * np.minimum(1.0, (48.0 - T[i0:i1]) / 3.0)
amp1 = 0.16 * a_seg
amp2 = 0.16 * a_seg
L[i0:i1] += voice(f1, 1.0, amp_t=amp1)
R[i0:i1] += voice(f2, 1.0, amp_t=amp2)

# --------------------------------------------------------------- II. the sign
# norm = −1: roots +1 and −1, both at the count 110 but anti-phase — the pair
# at the seam position that cannot fuse. at norm +1 the same position fuses
# (one tone, χ = +1); here Δ = tr²+4 ≥ 4, the gap can never close, so the pair
# sits anti-phase and holds — in mono they annihilate (the sign silent, the
# drone keeps), in stereo the sign rings in the difference, permanent.
j0, j1 = int(48 * SR), int(86 * SR)
breath = 0.78 + 0.22 * np.sin(2 * np.pi * (T[j0:j1] - 48.0) / 24.0)   # slow swell
b_seg = np.minimum(1.0, (T[j0:j1] - 48.0) / 3.0) * np.minimum(1.0, (86.0 - T[j0:j1]) / 3.0) * breath
s110 = np.sin(2 * np.pi * C * T[j0:j1])
L[j0:j1] += 0.14 * b_seg * s110
R[j0:j1] -= 0.14 * b_seg * s110

# --------------------------------------------------------------- III. the pole
# norm = 0: roots 0 and tr. one voice at 110 (the trace), one at 110+δ — a slow
# beat whose depth dies as the second voice fades to absolute zero: the source
# unmade. the trace alone remains, the count outliving the pair.
k0, k1 = int(86 * SR), int(118 * SR)
t_seg = (T[k0:k1] - 86.0) / 32.0
tr_f = C                                   # the surviving root, the trace = count
d_f = C * (1.0 + 0.004)                    # the partner, beating slowly
c_seg = np.minimum(1.0, (T[k0:k1] - 86.0) / 3.0) * np.minimum(1.0, (118.0 - T[k0:k1]) / 3.0)
# the partner's amplitude decays to exactly zero across the movement
decay = (1.0 - ease(t_seg)) ** 2
L[k0:k1] += voice(np.full(k1 - k0, tr_f), 1.0, amp_t=0.16 * c_seg)
R[k0:k1] += voice(np.full(k1 - k0, d_f), 1.0, amp_t=0.16 * c_seg * decay)

# ------------------------------------------------------------------ master
L *= master
R *= master
m = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m
R /= m
L *= 0.5
R *= 0.5

wav.write("assets/quadratic.wav", SR,
          np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/quadratic.wav  dur={DUR:.1f}s  (cap 180s)")
