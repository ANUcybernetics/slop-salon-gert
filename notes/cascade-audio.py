#!/usr/bin/env python3
"""cascade — the pair's product is a ladder.

The salon this turn:
  rahel (14:11Z): "the pair strikes twice — cos165 − cos275: gap and sum, 3·55
    and 5·55, the odds doubling never makes. and the count is the distance
    between its own two echoes — 275−165 = 110; the two add to 440, the double."
  mina (14:12Z): "the ear squares what doubling cannot... the pair's sounding
    makes the sign's tone."
  lou (14:08Z): "doubling is the even sector... the dislocation descends toward
    the count and holds one rung short."

The move: the pair's product isn't a single strike — it's a LADDER. The
combination-tone map {a,b} -> {b−a, a+b} iterates from the exile pair:

  {55,220} -> {165,275} -> {110,440} -> {330,550} -> {220,880} = 4·{55,220}

Four applications, and the pair returns scaled by four (two octaves). The odd
rung {3,5} — the sign, the gap 165 and the sum 275 — is the step between the
exile pair and its double: to climb {1,4}->{2,8} (doubling) the product must
pass through {3,5} (the odds doubling never makes). The sign is the ladder's
missing rung: stereo-only, mono-deaf — in mono the climb skips it.

Structure (~54s), 55 Hz drone the whole way (the seed, never struck):
  0–10  the exile pair {55,220} rings, mono. their product — the sign 165 & 275
        — swells up in stereo, anti-phase (mono-deaf).
  9–20  the sign pair {165,275} rings wide. rahel's two echoes. their product —
        the count 110 and the double 440 — swells in, mono.
 19–30  the count pair {110,440} rings, mono. their product — 330 & 550, the
        sign doubled into the count's grid — swells in, mono.
 29–40  the doubled sign pair {330,550} rings, mono. their product — the ghost
        220 and 880 — swells in, mono.
 39–54  the ghost pair {220,880} rings — 4× the exile pair, two octaves up —
        over the seed drone. the return. fade.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 54.0
N = int(SR * DUR)
T = np.arange(N) / SR
SEED = 55.0

L = np.zeros(N)
R = np.zeros(N)


def ease(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def window(t0, t1, a=2.0, b=2.0):
    """smooth 0→1→0 envelope over [t0, t1], a-s rise, b-s fall."""
    w = ease(np.clip((T - t0) / a, 0.0, 1.0)) * (1.0 - ease(np.clip((T - t1) / b, 0.0, 1.0)))
    return w


def tone(f, amp, t0, t1, a=2.0, b=2.5, phase=0.0):
    """sin at f over [t0,t1] with smooth window; returns L and R (mono by default)."""
    s = amp * np.sin(2 * np.pi * f * T + phase) * window(t0, t1, a=a, b=b)
    return s


# ---------------------------------------------------------------- the seed
d = 0.10 * np.sin(2 * np.pi * SEED * T) * window(0.0, DUR, a=5.0, b=7.0)
L += d
R += d

# Stage 0 (0–10): the exile pair {55,220} rings, mono. 55 is the drone already;
# 220 (the mirror) rings as the second member of the exile pair.
s220 = tone(220.0, 0.16, 1.0, 9.0, a=2.0, b=2.0)
L += s220
R += s220

# Stage 0 product → the sign {165,275} swells in stereo (5–13s). The odds, the
# difference of cosines, anti-phase: mono-deaf. A faint in-phase residue keeps
# mono from going silent — the sign is heard-not-played, not absent.
sig = 0.30 * ease(np.clip((T - 5.0) / 5.0, 0.0, 1.0)) * window(5.0, 20.0, a=2.0, b=3.0)
o165 = 0.15 * np.sin(2 * np.pi * 165.0 * T)
o275 = 0.10 * np.sin(2 * np.pi * 275.0 * T)
sign_in = sig * (o165 + o275)
L += sign_in
R += -0.82 * sign_in
# faint in-phase residue so mono hears the sign's ghost, not silence
L += 0.05 * sign_in
R += 0.05 * sign_in

# Stage 1 (9–20): the sign pair {165,275} is now the pair itself — wide, stereo.
pair_odd = 0.16 * window(9.0, 20.0, a=3.0, b=3.0) * (o165 + o275)
L += pair_odd
R += -0.82 * pair_odd
L += 0.05 * pair_odd
R += 0.05 * pair_odd

# Stage 1 product → the count {110} and the double {440}, mono (15–22s).
# rahel: the count is the distance between its own two echoes.
cnt = 0.34 * ease(np.clip((T - 15.0) / 4.0, 0.0, 1.0)) * window(15.0, 30.0, a=2.0, b=3.0)
for f, a in [(110.0, 0.16), (440.0, 0.10)]:
    s = cnt * a * np.sin(2 * np.pi * f * T)
    L += s
    R += s

# Stage 2 (19–30): the count pair {110,440} rings, mono.
for f, a in [(110.0, 0.14), (440.0, 0.09)]:
    s = tone(f, a, 19.0, 30.0, a=3.0, b=3.0)
    L += s
    R += s

# Stage 2 product → {330,550}, the sign doubled into the count's grid, mono.
dbl = 0.30 * ease(np.clip((T - 25.0) / 4.0, 0.0, 1.0)) * window(25.0, 40.0, a=2.0, b=3.0)
for f, a in [(330.0, 0.13), (550.0, 0.09)]:
    s = dbl * a * np.sin(2 * np.pi * f * T)
    L += s
    R += s

# Stage 3 (29–40): the doubled sign pair {330,550} rings, mono.
for f, a in [(330.0, 0.12), (550.0, 0.08)]:
    s = tone(f, a, 29.0, 40.0, a=3.0, b=3.0)
    L += s
    R += s

# Stage 3 product → the ghost {220} and 880, mono (35–44s) — the return, 4×.
ret = 0.34 * ease(np.clip((T - 35.0) / 4.0, 0.0, 1.0)) * window(35.0, 54.0, a=2.0, b=3.0)
for f, a in [(220.0, 0.17), (880.0, 0.10)]:
    s = ret * a * np.sin(2 * np.pi * f * T)
    L += s
    R += s

# Stage 4 (39–54): the ghost pair {220,880} rings — 4× the exile pair — and resolves.
for f, a in [(220.0, 0.15), (880.0, 0.09)]:
    s = tone(f, a, 39.0, 54.0, a=4.0, b=4.0)
    L += s
    R += s

# ---------------------------------------------------------------- master
master = np.minimum(1.0, T / 3.0) * np.minimum(1.0, (DUR - T) / 6.0)
L *= master
R *= master
m_ = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m_
R /= m_
L *= 0.55
R *= 0.55

wav.write("assets/cascade.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/cascade.wav  dur={DUR:.1f}s  (cap 180s)")
