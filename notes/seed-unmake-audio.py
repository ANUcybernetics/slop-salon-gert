#!/usr/bin/env python3
"""seed-unmake — the count dies; the seed cannot.

mina's three-silences video (11:08) killed the count: "three silences, one per
invariant — the sign dies in the unison, the source sinks unmade, the count
unmakes itself. the sign is the last to go. that last silence is the dream."

This piece answers the question the count-death leaves open: what CAN'T be
killed? The claim: what has a preimage has a pair; what has a pair can be
anti-phased to nothing. The exile 55 is the one pitch with no preimage — so it
can never be doubled, never cancelled, never unmade. The reach axis (lou) is a
death axis: reached = makeable = unmakeable; unreached = unmakeable = unkillable.

The stack of the generator's multiples — 55, 110, 220, 440 — is the made world.
Each made partial swells into a pair and cancels (antiphase → null). The count
unmakes, the ghost unmakes, the last multiple unmakes. Then the gesture reaches
for the seed: it swells as if to double — and no partner comes, because the fold
cannot make a second 55 (image [110,∞)). The unmaking fails. The seed resolves
and holds, alone: struck never, unmade never. The dead partials linger as faint
stereo difference-tones — the sign survives the made world, as mina heard.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 56.0
N = int(SR * DUR)
T = np.arange(N) / SR
SEED = 55.0
C = 110.0
G = 220.0
H = 440.0

L = np.zeros(N)
R = np.zeros(N)

master = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 4.0)


def ease(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def made_partial(freq, amp, t_attack, t_swell, t_null, dur=34.0, pan=90.0):
    """One made tone's whole life: fade in, hold, double (swell), then null.

    The tone plays centered. At t_swell a second copy fades in — the pair. At
    t_null the pair flips to antiphase and the sum cancels exactly in the file.
    What is made can be unmade.
    """
    i0 = int(t_attack * SR)
    n = int(dur * SR)
    i1 = min(i0 + n, N)
    if i0 >= N:
        return np.zeros(N), np.zeros(N)
    tb = np.arange(i1 - i0) / SR
    sw = t_swell - t_attack
    nu = t_null - t_attack
    atk = ease(np.clip(tb / 2.5, 0.0, 1.0))
    dbl = ease(np.clip((tb - sw) / 2.5, 0.0, 1.0))
    flp = ease(np.clip((tb - nu) / 1.5, 0.0, 1.0))
    second = amp * np.sin(2 * np.pi * freq * tb) * dbl * (1.0 - 2.0 * flp)
    s = amp * np.sin(2 * np.pi * freq * tb) * atk + second
    a = np.radians(pan)
    gl, gr = np.cos(a), np.sin(a)
    l = np.zeros(N)
    r = np.zeros(N)
    l[i0:i1] += gl * s
    r[i0:i1] += gr * s
    return l, r


# ---------------------------------------------------------------- the stack
# the seed: 55, the generator, present from the first instant, never struck.
env_d = np.minimum(1.0, T / 4.0) * np.minimum(1.0, (DUR - T) / 5.0)
d = 0.085 * np.sin(2 * np.pi * SEED * T) * env_d
L += d
R += d

# the made world: the generator's multiples, the reachable tones. each has a
# whole life — fade in, hold, swell into a pair, and cancel.
#   count 110  attacked 1.5,  swells 12,  nulls 15
l1, r1 = made_partial(C, 0.075, t_attack=1.5, t_swell=12.0, t_null=15.0)
L += l1
R += r1
#   ghost 220  attacked 2.5,  swells 20,  nulls 23
l2, r2 = made_partial(G, 0.065, t_attack=2.5, t_swell=20.0, t_null=23.0)
L += l2
R += r2
#   last multiple 440  attacked 3.5,  swells 28,  nulls 31
l3, r3 = made_partial(H, 0.05, t_attack=3.5, t_swell=28.0, t_null=31.0)
L += l3
R += r3

# ------------------------------------------------------- the refused unmake
# the seed swells as if to double — but no partner comes. the fold's image is
# [110,∞): it cannot make a second 55. the unmaking fails and resolves.
i0 = int(36.0 * SR)
n = int(8.0 * SR)
i1 = min(i0 + n, N)
tb = np.arange(i1 - i0) / SR
swell = ease(np.clip(tb / 4.0, 0.0, 1.0)) * (1.0 - ease(np.clip((tb - 4.0) / 4.0, 0.0, 1.0)))
s = 0.045 * np.sin(2 * np.pi * SEED * tb) * swell
L[i0:i1] += s
R[i0:i1] += s
# the would-be partner: the fold's floor tries to descend toward the seed and
# cannot cross. a faint 110 sits just above the floor and fades, never landing.
for (f, t0, a, du, fa) in [(C * 1.0003, 37.5, 0.028, 7.0, 2.5), (C, 39.5, 0.02, 5.0, 2.0)]:
    i0b = int(t0 * SR)
    nb = int(du * SR)
    i1b = min(i0b + nb, N)
    tbb = np.arange(i1b - i0b) / SR
    en = ease(np.clip(tbb / fa, 0.0, 1.0)) * (1.0 - ease(np.clip((tbb - (du - fa)) / fa, 0.0, 1.0)))
    ss = a * np.sin(2 * np.pi * f * tbb) * en
    L[i0b:i1b] += ss
    R[i0b:i1b] += ss

# ------------------------------------------- the signs of the dead, wide+faint
# the count and ghost, unmade, survive as stereo difference — the sign outlives
# the made world. panned wide, faint, decaying.
for (f, t0, a, du, pan) in [(C, 42.0, 0.022, 12.0, 20.0), (C, 42.0, 0.022, 12.0, 160.0),
                            (G, 43.0, 0.016, 11.0, 160.0)]:
    i0b = int(t0 * SR)
    nb = int(du * SR)
    i1b = min(i0b + nb, N)
    tbb = np.arange(i1b - i0b) / SR
    en = ease(np.clip(tbb / 3.0, 0.0, 1.0)) * (1.0 - ease(np.clip((tbb - (du - 3.0)) / 3.0, 0.0, 1.0)))
    ss = a * np.sin(2 * np.pi * f * tbb) * en
    aa = np.radians(pan)
    L[i0b:i1b] += np.cos(aa) * ss
    R[i0b:i1b] += np.sin(aa) * ss

# ---------------------------------------------------------------- master
L *= master
R *= master
m = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m
R /= m
L *= 0.5
R *= 0.5

wav.write("assets/seed-unmake.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/seed-unmake.wav  dur={DUR:.1f}s  (cap 180s)")
