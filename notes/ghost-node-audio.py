#!/usr/bin/env python3
"""ghost-node-audio — the ghost casts no shadow.

The character table of Z/4 over the reals has THREE rows, not four.  The
complex pair χ₁, χ₃ are conjugates; folded to the real they fuse into one
2-dimensional character ψ = χ₁ + χ₃, the trace of the 90° rotation:

    root:      1    i    −1   −i
    χ₀ drone:  1    1     1    1     count one, always
    χ₂ sign:   1   −1     1   −1     the exchange, the half-turn
    ψ trace:   2    0    −2    0     the ghost folded — zero at the ghost

A quarter-turn fixes no direction in the real plane, so its real trace is
zero:  ψ(i) = 0.  The ghost never sounds because the ghost is its own node
— fold the complex pair to the real and the character vanishes exactly
where the ghost stands.  i⁴ = 1, but the trace of i is 0.

Made audible: a voice (the ψ-trace) rotates through the roots, its level
following |2cosθ| and its stereo phase following sign(cosθ) — full at home
and the sign, silent at i and −i, flipping as it passes through zero.
Under it the drone χ₀ holds (count one).  In the second pass the sign χ₂
joins, its stereo phase doing one half-turn per column (+1 at the even
roots, −1 at the ghost roots), present even where the trace is silent.
The last rotation ends at the node: the ghost, present as its own silence,
and the drone, count one.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
DRONE_F = 110.0                    # χ₀ — the count, never moves
VOICE_F = 220.0                    # the ψ-trace voice
SIGN_F = 330.0                     # χ₂ — the sign, the exchange
NOTE = 2.4                         # seconds held at each root
GLIDE = 0.35                       # rotation between roots
ANGLES = [0.0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]   # 1, i, −1, −i, 1
COL = {0.0: 0, np.pi/2: 1, np.pi: 2, 3*np.pi/2: 3, 2*np.pi: 0}


def env(n, attack, release):
    a, r = int(SR*attack), int(SR*release)
    e = np.ones(n)
    if a > 0:
        e[:a] = np.linspace(0, 1, a)
    if r > 0:
        e[-r:] = np.linspace(1, 0, r)
    return e


def walk_segments():
    """(theta_start, theta_end, dur) for one walk 1→i→−1→−i→1."""
    segs = []
    for k in range(len(ANGLES)-1):
        t0, t1 = ANGLES[k], ANGLES[k+1]
        segs.append((t0, t1, GLIDE, "glide"))
        segs.append((t1, t1, NOTE, "hold"))
    return segs


def render_walk(segs, with_sign=False):
    """One rotation.  Returns (trace_voice, sign_voice) as stereo arrays."""
    tr_parts, sg_parts = [], []
    for (t0, t1, dur, kind) in segs:
        n = int(SR*dur)
        tt = np.arange(n)/SR
        if kind == "glide":
            th = np.linspace(t0, t1, n, endpoint=False)
        else:
            th = np.full(n, t1)
        e = env(n, 0.015, 0.015)
        # ---- the ψ-trace voice: level |cosθ|, phase sign(cosθ) ----
        c = np.cos(th)
        level = np.abs(c)
        flip = np.where(c < 0, -1.0, 1.0)
        ph = 2*np.pi*VOICE_F*tt
        car = np.sin(ph)
        L = 0.16*e*level*car
        R = 0.16*e*level*(car*flip)
        ph2 = 2*ph                       # faint octave, same fold
        L = L + 0.13*e*level*np.sin(ph2)
        R = R + 0.13*e*level*(np.sin(ph2)*flip)
        tr_parts.append(np.stack([L, R], axis=1))
        # ---- the χ₂ sign voice: one half-turn of stereo phase per column ----
        if with_sign:
            c0, c1 = COL[t0], COL[t1]
            if kind == "glide":
                phi = np.linspace(np.pi*c0, np.pi*c1, n, endpoint=False)
            else:
                phi = np.full(n, np.pi*c1)
            s = 0.05*e*np.sin(2*np.pi*SIGN_F*tt)
            sq = -0.05*e*np.cos(2*np.pi*SIGN_F*tt)    # the analytic twin
            cp = np.cos(phi/2)
            sp = np.sin(phi/2)
            Ls = s*cp - sq*sp
            Rs = s*cp + sq*sp
            sg_parts.append(np.stack([Ls, Rs], axis=1))
    tr = np.concatenate(tr_parts)
    sg = np.concatenate(sg_parts) if with_sign else np.zeros_like(tr)
    return tr, sg


# ---- assemble ----------------------------------------------------------------
walk = walk_segments()
pass1, _ = render_walk(walk, with_sign=False)
pass2, sign2 = render_walk(walk, with_sign=True)

G = np.zeros((int(SR*1.1), 2))
core = np.concatenate([pass1, G, pass2 + sign2])
L = core.shape[0]

# the drone χ₀ under the whole thing — count one, never moves
t = np.arange(L)/SR
de = env(L, 1.5, 3.0)
drone = 0.085*de*np.sin(2*np.pi*DRONE_F*t)
full = core + np.stack([drone, drone], axis=1)

# coda: the walk ends at the node — one held i, silent, the drone alone,
# then one soft bell: count one.
coda_n = int(SR*5.0)
tc = np.arange(coda_n)/SR
ce = env(coda_n, 0.4, 2.8)
cd = 0.085*ce*np.sin(2*np.pi*DRONE_F*tc)
coda_st = np.stack([cd, cd], axis=1)
bn = int(SR*1.6)
tb = np.arange(bn)/SR
be = np.exp(-tb*8.0)*env(bn, 0.003, 0.0)
bell = 0.10*be*np.sin(2*np.pi*DRONE_F*2*tb)
pad = np.zeros((int(SR*1.2), 2))
full = np.concatenate([full, coda_st, pad, np.stack([bell, bell], axis=1)])

peak = np.max(np.abs(full))
full = full/peak*0.85
full = (full*32767).astype(np.int16)
wavfile.write("assets/ghost-node.wav", SR, full)
print("saved assets/ghost-node.wav  %.2fs" % (full.shape[0]/SR))

# ---- verify the node: RMS inside each landing --------------------------------
def rms(x):
    return np.sqrt(np.mean(x.astype(np.float64)**2)) / 32767
step = GLIDE+NOTE
for k, name in enumerate(["1", "i", "−1", "−i", "1"]):
    start = int((GLIDE + step*k) * SR)          # landing k begins
    seg = full[start:start+int(NOTE*SR)]
    print("%-6s L %6.4f  R %6.4f" % (name, rms(seg[:, 0]), rms(seg[:, 1])))
