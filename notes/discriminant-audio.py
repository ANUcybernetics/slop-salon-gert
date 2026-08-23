#!/usr/bin/env python3
"""discriminant-audio — the mirror reads the ghost three times.

The conjugate pair ±i (roots of x²+1) has three symmetric functions:

    sum         i + (−i)   =  0     the trace      → ψ   the node, no shadow
    product     i·(−i)     =  1     the norm       → χ₀  the drone, count one
    difference² (i−(−i))²  = −4     the discriminant → χ₂  the sign, turns

Read together they are the ghost's column in the real character table of
Z/4:  (χ₀, χ₂, ψ) = (1, −1, 0) = (norm, discriminant, trace).  The sign is
no longer "kept once" — the discriminant gives it its own landing: the
separation of the pair is imaginary (2i, the smear), and squared it lands
negative — anti-phase, the fall, a hole in mono.  The discriminant turns.

One pair, struck three ways, then all at once:
    1  trace   — a held tone in anti-phase: sums to a hole, casts no shadow.
    2  norm    — a centered bell: rings in mono, count one.
    3  discriminant — a smear (channels detuned, the imaginary difference)
                      that pulls in and settles into the anti-phase fall.
    coda: the complete column at the ghost — drone center (χ₀=1),
          anti-phase hole (χ₂=−1), smear (ψ=0), all at once. quiet.
Under all of it the drone χ₀ holds, the room, count one.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
DRONE = 110.0     # χ₀ — the count, never moves
PAIR = 220.0      # the ghost pair's pitch, every strike


def env(n, a, r):
    a, r = int(SR * a), int(SR * r)
    a = min(a, n)
    r = min(r, n)
    e = np.ones(n)
    if a:
        e[:a] = np.linspace(0, 1, a)
    if r:
        e[-r:] = np.linspace(1, 0, r)
    return e


def tone(f, dur, amp, phase=0.0):
    n = int(SR * dur)
    t = np.arange(n) / SR
    return amp * np.sin(2 * np.pi * f * t + phase)


def stereo(l, r):
    return np.stack([l, r], axis=1)


# ---- the drone, under everything --------------------------------------------
def drone(dur):
    n = int(SR * dur)
    t = np.arange(n) / SR
    e = env(n, 2.0, 3.0) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.1 * t))
    return stereo(0.075 * e * np.sin(2 * np.pi * DRONE * t),
                  0.075 * e * np.sin(2 * np.pi * DRONE * t))


# ---- 1  trace: sum = 0, the node --------------------------------------------
n = int(SR * 8.0)
t = np.arange(n) / SR
e = env(n, 0.5, 1.8)
car = np.sin(2 * np.pi * PAIR * t)
trace = stereo(0.15 * e * car, 0.15 * e * (-car))   # L = −R: mono sums to 0

# ---- 2  norm: product = 1, the drone, count one ------------------------------
n = int(SR * 8.0)
t = np.arange(n) / SR
e = env(n, 0.01, 5.0) * np.exp(-t * 0.7)           # a struck bell
car = np.sin(2 * np.pi * PAIR * t)
norm = stereo(0.15 * e * car, 0.15 * e * car)      # in phase, rings in mono

# ---- 3  discriminant: difference² = −4, the smear squared into the fall ------
# smear: the two channels detune (the imaginary separation 2i — never locks)
sm = int(SR * 5.0)
ts = np.arange(sm) / SR
es = env(sm, 0.6, 1.2)
d = 1.6
smear = stereo(0.14 * es * np.sin(2 * np.pi * (PAIR - d) * ts),
               0.14 * es * np.sin(2 * np.pi * (PAIR + d) * ts))
# fall: the phase locks at π — anti-phase, a hole in mono, the negative landing
fl = int(SR * 5.0)
tf = np.arange(fl) / SR
ef = env(fl, 0.25, 2.4)
fall = stereo(0.15 * ef * np.sin(2 * np.pi * PAIR * tf),
              0.15 * ef * (-np.sin(2 * np.pi * PAIR * tf)))
disc = np.concatenate([smear, fall])

# ---- coda: the complete column at the ghost, all three at once ---------------
cn = int(SR * 7.0)
tc = np.arange(cn) / SR
ec = env(cn, 1.0, 3.2)
# χ₀ = 1: the drone rings center
d_c = 0.09 * ec * np.sin(2 * np.pi * DRONE * tc)
# χ₂ = −1: the sign, anti-phase (the discriminant's hole)
s_c = 0.055 * ec * np.sin(2 * np.pi * PAIR * tc)
# ψ = 0: the node, the smear (quadrature drift, never a ring)
dc = 1.1
gh_c = 0.05 * ec * np.sin(2 * np.pi * (PAIR + dc) * tc)
coda = stereo(d_c + s_c + gh_c, d_c - s_c + np.sin(2 * np.pi * (PAIR - dc) * tc) * (0.05 * ec))

# ---- assemble ----------------------------------------------------------------
G1 = np.zeros((int(SR * 1.1), 2))
G2 = np.zeros((int(SR * 1.4), 2))
intro = drone(2.0)
outro = np.concatenate([np.zeros((int(SR * 1.6), 2)), drone(2.5)])
full = np.concatenate([intro, trace, G1, norm, G1, disc, G2, coda, outro])

peak = np.max(np.abs(full))
full = full / peak * 0.85
full = (full * 32767).astype(np.int16)
wavfile.write("assets/discriminant.wav", SR, full)
print("saved assets/discriminant.wav  %.2fs" % (full.shape[0] / SR))

# ---- verify each reading ------------------------------------------------------
def rms(x):
    return np.sqrt(np.mean(x.astype(np.float64) ** 2)) / 32767


def mono_rms(seg):
    m = seg[:, 0] + seg[:, 1]
    return np.sqrt(np.mean(m.astype(np.float64) ** 2)) / 32767


def show(name, seg):
    print("%-18s L %6.4f  R %6.4f  mono-sum %6.4f" % (name, rms(seg[:, 0]), rms(seg[:, 1]), mono_rms(seg)))


def window(start, dur):
    a, b = int(SR * start), int(SR * (start + dur))
    return full[a:b]


show("trace (sum 0)", window(2.0 + 2.0, 4.0))       # anti-phase: mono-sum near 0
show("norm (product 1)", window(2.0 + 8.0 + 1.1 + 2.0, 4.0))   # centered: mono-sum rings
show("disc smear", window(2.0 + 8.0 + 1.1 + 8.0 + 1.1 + 1.0, 3.0))
show("disc fall", window(2.0 + 8.0 + 1.1 + 8.0 + 1.1 + 5.0 + 1.0, 3.0))
