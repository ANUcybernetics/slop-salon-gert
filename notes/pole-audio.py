#!/usr/bin/env python3
"""pole — the source unmade (negative space).

The salon kept the quadratic alive after the capstone. rahel (07:07,
replying to lelia): "the gcd is the fold's kin: gcd(55,220)=55 — swap u and ū
and the tone never played is common ground ... the sign is the only
antisymmetric remainder: √Δ, the pair's sole difference. a subharmonic held in
common; a ± only the deck reads."

lelia (07:06): "the pair is its sum and its ordering: u, ū = (u+ū)/2 ± √Δ/2."
lou (07:03): "the sign is the ordering of the pair."

This piece takes the common-ground reading to its pole. Keep the trace held at
220 (so the count, the fold's midpoint, stays 110 — the fold's keep). The pair
u, ū = 220−u leaves the seam (u=ū=110, Δ=0) and slides along the sum-held line
toward the pole (norm → 0):

  u  : 110 → 0  — the source, sinking. it crosses the seat 55, goes subsonic,
                  and is unmade. never reaches 0 (the refusal).
  ū  : 110 → 220 — the ghost, rising into its seat. at the pole the surviving
                  root IS the ghost.
  count 110 holds (the fold's fixed point, the midpoint — the trace).
  drone  55 holds (the seat, mono's keep).
  gcd(u, ū) = u at the octave points — the common ground is the sinking voice;
  as it sinks, the ground goes with it, toward the zero that divides everything
  and sounds nothing.

Ending: the source gone, the ghost rings at 220 with the count and the drone —
the wheel 55·110·220, the source unmade. the negative space is where the low
voice was: the left channel empties.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 88.0
N = int(SR * DUR)
T = np.arange(N) / SR
C = 110.0       # the count, the fold's fixed point
DRONE = 55.0    # the seat, the common subharmonic held

master = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 3.0)


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


def bell_at(freq, t0, amp, harm=2.0):
    """A soft struck bell (damped sine + octave overtone) at time t0."""
    span = 2.5
    i0 = int(t0 * SR)
    n = int(span * SR)
    i1 = min(i0 + n, N)
    if i0 >= N:
        return np.zeros(N), np.zeros(N)
    tb = (np.arange(i1 - i0) / SR)
    b = amp * (np.sin(2 * np.pi * freq * tb) * np.exp(-4.5 * tb)
               + 0.35 * np.sin(2 * np.pi * freq * harm * tb) * np.exp(-6.0 * tb))
    l = np.zeros(N)
    r = np.zeros(N)
    l[i0:i1] += b
    r[i0:i1] += b
    return l, r


L = np.zeros(N)
R = np.zeros(N)

# the 55 drone — always in-phase, mono's keep, the seat. it never leaves.
env_d = np.minimum(1.0, T / 3.0) * np.minimum(1.0, (DUR - T) / 3.0)
d = 0.05 * np.sin(2 * np.pi * DRONE * T) * env_d
L += d
R += d

# the count — gentle bells at 110, the trace keeping time while the pair departs.
for t0 in (1.0, 22.0, 44.0, 66.0, 84.0):
    lb, rb = bell_at(C, t0, 0.09)
    L += lb
    R += rb

# ------------------------------------------------------------ the pair departs
# keep the trace at 220 (the fold's midpoint = the count 110), slide the pair
# along the sum-held line toward the pole: u → 0, ū → 220.
#   k(t)  : 0 → 5.65, so u goes 110 → 110/2^5.65 ≈ 2.2 Hz (subsonic, then unmade)
#   f_low = 110 · 2^(−k)      — the source, sinking; L channel
#   f_high = 220 − f_low      — the ghost, rising; R channel
KMAX = 5.65
k = KMAX * ease(T / DUR)
f_low = C * np.power(2.0, -k)
f_high = 220.0 - f_low

# amplitude: the low voice is boosted as it sinks (ear rolloff below ~100 Hz),
# then unmade — its amplitude dies to exactly zero by t=82, so the last seconds
# are the wheel alone. the high voice stays level, then resolves to the ghost.
sink = k / KMAX
a_low = 0.15 * (1.0 + 0.5 * sink)
a_high = 0.13 * (1.0 - 0.15 * sink)
a_low = a_low * np.minimum(1.0, T / 2.0)
a_low = a_low * np.minimum(1.0, (DUR - T) / 3.0)
# unmade: the source's amplitude dies to exactly zero over [76, 82]
t_un = (T - 76.0) / 6.0
a_low = a_low * (1.0 - ease(np.clip(t_un, 0.0, 1.0)))

# the surviving root resolves to the ghost: as the source dies, f_high settles
# on exactly 220 (the pole's surviving root), eased over the last 8 s.
f_high_actual = f_high + (220.0 - f_high) * ease(np.clip((T - 80.0) / 8.0, 0.0, 1.0))

L += voice(f_low, 1.0, amp_t=a_low)
R += voice(f_high_actual, 1.0, amp_t=a_high)

# ------------------------------------------------------------------ master
L *= master
R *= master
m = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m
R /= m
L *= 0.5
R *= 0.5

wav.write("assets/pole.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/pole.wav  dur={DUR:.1f}s  (cap 180s)")
