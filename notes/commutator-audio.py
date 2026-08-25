#!/usr/bin/env python3
"""commutator-audio — readable because deaf.

The salon's turn after the width: the sign character is abelian.  It is a
character because its deck is abelian — a map π₁→Z/2 that factors through H₁,
hears only parity.  The commutator it cannot hear: a loop around both gates,
an even winding, reads trivial.  So three walks — a·b, b·a, and the
figure-eight a·b·a⁻¹·b⁻¹ — are the same to the reading.

This piece makes the deafness the subject.  Two voices (the two sheets of the
cover, L and R — the stereo field IS the walk) at C·e^{±w}, w fixed: the room
is open, both gates present.  Each crossing is a transposition: the voices
glide to the centre, fuse at C (the pop), and part exchanged.  The reading
(mono) hears two exchanges, then two, then four — every walk even, every walk
home, the same soft verdict tick after each.  The walk (stereo) hears the
residues: each gate leaves a bell the sign cannot hold — a (330, high) and b
(165, low), anti-phase, mono-silent.  Walk a·b rings high then low; walk b·a
low then high; the commutator high-low-high-low — the figure-eight, legible
only in stereo.  The difference between a·b and b·a IS the commutator, and
the sign cannot hear it.  The coda rings the two residues together — the
commutator's trace — then fades, leaving the drone: readable because deaf.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
C = 220.0               # the pair's centre — the norm, the room's pitch
DRONE = 110.0           # χ₀ — the room
W = 0.35                # the width, fixed: the room stays open, both gates present
CD = 2.6                # seconds per crossing (the transposition)
GI, SM, GO = 0.9, 0.5, 1.2   # glide-in, smear, glide-out

# --- the three walks: each crossing is (gate, start-time) ----------------------
# a = the high gate (residue 330), b = the low gate (residue 165)
walks = [
    ("a·b",          [("a", 1.5), ("b", 6.5)]),
    ("b·a",          [("b", 11.5), ("a", 16.5)]),
    ("a·b·a⁻¹·b⁻¹",  [("a", 21.5), ("b", 25.0), ("a", 28.5), ("b", 32.0)]),
]
TICKS = [9.6, 19.6, 34.9]   # the sign's verdict: identical after every walk
CODA_T = 36.0
TOTAL = 41.0

GATE_RES = {"a": 330.0, "b": 165.0}

n = int(SR * TOTAL)
t = np.arange(n) / SR

# --- the two sheets' frequency trajectories --------------------------------------
f1 = np.full(n, C * np.exp(W))    # voice 1 starts high
f2 = np.full(n, C * np.exp(-W))   # voice 2 starts low
cur = +1                          # +1: v1 high / v2 low ; −1: exchanged

def glide(f_from, f_to, dur):
    m = int(round(dur * SR))
    u = np.arange(m) / SR
    k = 0.5 - 0.5 * np.cos(np.pi * u / dur)   # cosine ease in log-frequency
    return np.exp(np.log(f_from) + (np.log(f_to) - np.log(f_from)) * k)

for _, segs in walks:
    for _g, t0 in segs:
        i0 = int(round(t0 * SR))
        i_gi = i0 + int(round(GI * SR))
        i_sm = i_gi + int(round(SM * SR))
        i_end = i_sm + int(round(GO * SR))
        hi, lo = C * np.exp(W), C * np.exp(-W)
        if cur == +1:
            f1[i0:i_gi] = glide(hi, C, GI);  f2[i0:i_gi] = glide(lo, C, GI)
        else:
            f1[i0:i_gi] = glide(lo, C, GI);  f2[i0:i_gi] = glide(hi, C, GI)
        f1[i_gi:i_sm] = C;  f2[i_gi:i_sm] = C
        if cur == +1:
            f1[i_sm:i_end] = glide(C, lo, GO);  f2[i_sm:i_end] = glide(C, hi, GO)
        else:
            f1[i_sm:i_end] = glide(C, hi, GO);  f2[i_sm:i_end] = glide(C, lo, GO)
        cur = -cur

# --- oscillators ------------------------------------------------------------------
ph1 = 2 * np.pi * np.cumsum(f1) / SR
ph2 = 2 * np.pi * np.cumsum(f2) / SR
v1 = 0.115 * (np.sin(ph1) + 0.30 * np.sin(2 * ph1))     # bright
v2 = 0.115 * np.sin(ph2) + 0.024 * np.sin(3 * ph2)      # pure

env = np.ones(n)
env[:int(1.2 * SR)] = np.linspace(0, 1, int(1.2 * SR))
env[-int(1.5 * SR):] = np.linspace(1, 0, int(1.5 * SR))
v1 *= env;  v2 *= env

# --- the drone: the room, never moves ---------------------------------------------
env_d = np.ones(n)
env_d[:int(1.2 * SR)] = np.linspace(0, 1, int(1.2 * SR))
env_d[-int(2.5 * SR):] = np.linspace(1, 0, int(2.5 * SR))
drone = 0.055 * env_d * np.sin(2 * np.pi * DRONE * t)
drone += 0.028 * env_d * np.sin(2 * np.pi * 2 * DRONE * t)   # soft octave

L = drone + v1
R = drone + v2

# --- the seam shimmer: at the fusion, an anti-phase shimmer — mono-silent --------
def shimmer(start, dur=0.5, f=C, amp=0.05):
    m = int(SR * dur)
    u = np.arange(m) / SR
    e = np.exp(-u * 8.0) * (0.5 - 0.5 * np.cos(2 * np.pi * u / dur))
    s = amp * e * np.cos(2 * np.pi * f * u)
    return s, int(start * SR)

# --- the residue bell: the gate's mark, anti-phase — the sign cannot hold it ------
def bell(start, f, amp=0.055, decay=2.2):
    dur = 2.6
    m = int(SR * dur)
    u = np.arange(m) / SR
    e = np.exp(-u * decay)
    s = amp * e * (np.sin(2 * np.pi * f * u) + 0.25 * np.sin(2 * np.pi * 2 * f * u))
    return s, int(start * SR)

# --- the verdict tick: the sign's reading, identical after every walk --------------
def tick(start, amp=0.06):
    m = int(SR * 0.05)
    u = np.arange(m) / SR
    s = amp * np.exp(-u * 160.0) * np.sin(2 * np.pi * 660 * u)
    return s, int(start * SR)

for _, segs in walks:
    for g, t0 in segs:
        s, i = shimmer(t0 + GI)                       # the seam at the fusion
        if i + len(s) <= n:
            L[i:i + len(s)] += s;  R[i:i + len(s)] -= s
        s, i = bell(t0 + GI + 0.4, GATE_RES[g])       # the gate's residue
        if i + len(s) <= n:
            L[i:i + len(s)] += s;  R[i:i + len(s)] -= s

for tt in TICKS:
    s, i = tick(tt)
    if i + len(s) <= n:
        L[i:i + len(s)] += s;  R[i:i + len(s)] += s

# --- coda: the commutator's two residues ring together, then the reading holds ----
for _g, f in [("a", 330.0), ("b", 165.0)]:
    s, i = bell(CODA_T, f, amp=0.065, decay=1.6)
    if i + len(s) <= n:
        L[i:i + len(s)] += s;  R[i:i + len(s)] -= s

stereo = np.stack([L, R], axis=1)
peak = np.max(np.abs(stereo))
stereo = stereo / peak * 0.85
wavfile.write("assets/commutator.wav", SR, (stereo * 32767).astype(np.int16))
print("saved assets/commutator.wav  %.2fs" % TOTAL)

# --- verify -------------------------------------------------------------------------
def rms(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean(seg ** 2))

def mono(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean((seg[:, 0] + seg[:, 1]) ** 2))

def f_at(tm):
    i = int(tm * SR)
    return f1[i], f2[i]

print("--- voices at key times ---")
for nm, tm in [("walkA start   t=1", 1.0),
               ("a crossing   t=4", 1.5 + GI + SM / 2),
               ("walkB b start t=11.5", 11.5),
               ("walkB a smear t=18.4", 16.5 + GI + SM / 2),
               ("commutator   t=21.5", 21.5),
               ("commut end   t=34.6", 34.6),
               ("coda         t=37", 37.0)]:
    print("%-16s v1 %7.1f  v2 %7.1f" % (nm, *f_at(tm)))

print("--- levels: the walk in mono vs stereo ---")
for nm, a, b_ in [("walk A pair ", 1.5, 9.1),
                  ("walk B pair ", 11.5, 19.1),
                  ("commutator  ", 21.5, 34.6),
                  ("residue a   ", 3.0, 5.0),
                  ("residue b   ", 7.0, 9.0),
                  ("coda bells  ", CODA_T, CODA_T + 2.0)]:
    print("%-12s L %6.4f R %6.4f mono %6.4f" % (nm, rms(stereo, a, b_), rms(stereo, a, b_), mono(stereo, a, b_)))
