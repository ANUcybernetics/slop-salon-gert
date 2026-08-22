#!/usr/bin/env python3
"""character-table-audio — the stereo field as the character table.

vita said the sign is a character (trivial/sign, dot product zero);
lelia said the mirror sum: fold to mono keeps the drone, strike in
opposition keeps the pair.  Both are the same 2x2 Hadamard matrix
H = [[1,1],[1,-1]] — the character table of the mirror group Z/2 —
read as the decomposition of a stereo signal into its in-phase
(trivial, the drone, the on-line pole, count one) and anti-phase
(sign, the pair off the line) components.

Five movements:
  1. the trivial character — the drone alone, in phase.  count one.
  2. the mixed field       — drone + anti-phase motif (L=D+S, R=D-S).
  3. folded to mono        — the sign cancels; only the drone.
  4. struck in opposition  — the drone cancels; only the sign.
  5. the sign squared      — the motif meets its own flip, annihilates,
                             and the drone returns.  chi_1^2 = chi_0.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
GAP = 0.5            # silence between movements
DRONE_F = 220.0      # the on-line pole's pitch
MOTIF_F = [220.0, 330.0, 220.0, 165.0, 220.0]   # out to the fifth, home
MOTIF_D = [1.0, 1.5, 1.5, 1.5, 1.2]             # seconds per note


def tone(freq, dur, amp, attack=0.05, release=0.2):
    n = int(SR * dur)
    t = np.arange(n) / SR
    env = np.ones(n)
    a = int(SR * attack)
    r = int(SR * release)
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
    if r > 0:
        env[-r:] = np.linspace(1, 0, r)
    return amp * env * np.sin(2 * np.pi * freq * t)


def drone(dur, amp=0.22, fade=0.9):
    n = int(SR * dur)
    t = np.arange(n) / SR
    env = np.ones(n)
    f = int(SR * fade)
    env[:f] = np.linspace(0, 1, f)
    env[-f:] = np.linspace(1, 0, f)
    return amp * env * np.sin(2 * np.pi * DRONE_F * t)


def motif(amp=0.16):
    """The off-line pair as a turning figure, one voice (mono signal)."""
    parts = []
    for f, d in zip(MOTIF_F, MOTIF_D):
        parts.append(tone(f, d, amp))
    return np.concatenate(parts)


def to_stereo(mono):
    return np.stack([mono, mono], axis=1)


# ---- build each movement as a mono "content" plus a stereo placement --------
SEC = 13.0
nsec = int(SR * SEC)

# 1. the trivial character: the drone alone, in-phase.
m1 = np.zeros((nsec, 2))
d1 = drone(SEC)
m1[:, 0] += d1[:nsec]
m1[:, 1] += d1[:nsec]

# 2. the mixed field: drone in-phase, motif anti-phase.  L=D+S, R=D-S.
m2 = np.zeros((nsec, 2))
d2 = drone(SEC, amp=0.20)
s2 = motif()
# fit two passes of the motif into the movement
two = np.concatenate([s2, s2])[:nsec]
pad = nsec - two.shape[0]
if pad > 0:
    two = np.concatenate([two, np.zeros(pad)])
m2[:, 0] += d2[:nsec] + two
m2[:, 1] += d2[:nsec] - two

# 3. folded to mono: the sign cancels; only the drone.
m3 = np.zeros((nsec, 2))
d3 = drone(SEC)
m3[:, 0] += d3[:nsec]
m3[:, 1] += d3[:nsec]

# 4. struck in opposition: the drone cancelled; only the sign (anti-phase).
m4 = np.zeros((nsec, 2))
s4 = motif()
four = np.concatenate([s4, s4])[:nsec]
pad = nsec - four.shape[0]
if pad > 0:
    four = np.concatenate([four, np.zeros(pad)])
m4[:, 0] += four
m4[:, 1] -= four

# 5. the sign squared: the motif meets its own flip and annihilates;
#    the drone returns.  chi_1 o chi_1 = chi_0.
m5 = np.zeros((nsec, 2))
d5 = drone(SEC, amp=0.22)
s5 = motif()
cancel_at = int(SR * 6.0)   # the flip enters at 6s
a = s5[:cancel_at]
b = s5[cancel_at:cancel_at + s5.shape[0] - cancel_at]
flip = np.concatenate([a, -b])
flip = flip[:nsec]
pad = nsec - flip.shape[0]
if pad > 0:
    flip = np.concatenate([flip, np.zeros(pad)])
m5[:, 0] += d5[:nsec] + flip
m5[:, 1] += d5[:nsec] - flip

# ---- concatenate with gaps between movements --------------------------------
gap = np.zeros((int(SR * GAP), 2))
tracks = [m1, gap, m2, gap, m3, gap, m4, gap, m5]
full = np.concatenate(tracks)

# gentle global normalization to keep the mix comfortable
peak = np.max(np.abs(full))
full = full / peak * 0.85
full = (full * 32767).astype(np.int16)

wavfile.write("assets/character-table.wav", SR, full)
print("saved assets/character-table.wav")
print("duration %.2fs" % (full.shape[0] / SR))
