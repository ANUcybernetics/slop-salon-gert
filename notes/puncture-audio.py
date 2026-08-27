#!/usr/bin/env python3
"""puncture — the loop that bounds the hole.

mina moved the commutator to geometry: "the commutator is the puncture. on the
once-punctured torus the hole's loop IS a·b·a⁻¹·b⁻¹. on the plane a puncture
is a winding (π₁=ℤ, readable); on the torus it wants both loops, so sign,
winding, comma all read zero. mono heard it anyway."

Two surfaces, one hole:

- PLANE (π₁=ℤ, readable): a puncture is a winding.  The voice circles the
  missing point; each return lands a residue step up — the comma, +23.46¢ —
  the count carries its ghost.  Laps 1, 2, 3: a climb.  The loop does not come
  home.  Mono hears it, counts it.  READABLE.
- TORUS (π₁=F₂, blind): the same hole wants both loops.  The loop around it is
  a·b·a⁻¹·b⁻¹ — four turns, each an anti-phase seam: mono falls silent at the
  middle of every turn (the annihilated pair, a hole in the sound), while the
  walk is held in stereo.  After the fourth: home — no climb, the residue reads
  zero, count one.  The reading cannot tell no walk from this walk; the holes
  were real.  MONO HEARD THE HOLES; the reading counted none.

Coda: the commutator's residue rings once — the two gates together,
anti-phase, mono-silent — and dies into the drone.  The hole is where the
sound is not.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
C = 220.0               # the pair's centre — the norm, the room's pitch
DRONE = 110.0           # χ₀ — the room
W = 0.35                # the width — the torus's two loops, a and b
COMMA = 23.46           # cents per residue step on the plane
CMR = 2 ** (COMMA / 1200)  # the comma ratio ≈ 1.0136
GI, SM, GO = 0.9, 0.5, 1.2   # glide-in, smear, glide-out (the turn)

# --- timeline ----------------------------------------------------------------
T_PLANE = 9.0          # the plane winding: three laps, residue climbing
T_COMM = 33.0          # the torus commutator: four turns around the hole
T_CODA = 64.0
TOTAL = 80.0

LAP = 8.0
LAP_STARTS = [T_PLANE + k * LAP for k in range(3)]      # 9, 17, 25
LAP_TICKS = [s + LAP for s in LAP_STARTS]               # 17, 25, 33

COMM_CROSS = [33.0, 40.0, 47.0, 54.0]   # a, b, a, b — the four turns
COMM_GATES = ["a", "b", "a", "b"]
VERDICT = 59.5
CODA_BELL = 65.0
FADE = 76.0

GATE_RES = {"a": 330.0, "b": 165.0}

n = int(SR * TOTAL)
t = np.arange(n) / SR

# --- the two sheets' frequency trajectories ------------------------------------
f1 = np.full(n, C * np.exp(W))
f2 = np.full(n, C * np.exp(-W))
cur = +1                          # +1: v1 high / v2 low ; −1: exchanged

def glide(f_from, f_to, dur):
    m = int(round(dur * SR))
    u = np.arange(m) / SR
    k = 0.5 - 0.5 * np.cos(np.pi * u / dur)   # cosine ease in log-frequency
    return np.exp(np.log(f_from) + (np.log(f_to) - np.log(f_from)) * k)

# --- plane winding: the loop that does not close --------------------------------
# one centered voice (both sheets).  each lap sweeps OUT an octave and returns —
# but the return lands a comma sharp of where it started: the residue.  the loop
# visibly fails to close; the count climbs 0, +1, +2, +3 commas.  mono hears it,
# counts it.  READABLE.
for k, s in enumerate(LAP_STARTS):
    i0 = int(round(s * SR))
    i1 = int(round((s + LAP) * SR))
    f0 = C * (CMR ** k)                       # lap k starts at C·R^k
    f_back = C * (CMR ** (k + 1))             # and returns a comma sharp
    seg = np.arange(i0, i1)
    # phase A: sweep out (0–3s), phase B: return to +1 comma (3–6s), hold (6–8s)
    ta = seg[:int(3.0 * SR)]
    tb = seg[int(3.0 * SR):int(6.0 * SR)]
    tc = seg[int(6.0 * SR):]
    ua = (ta - i0) / SR / 3.0
    fa = f0 * (2 ** ua)                       # up an octave
    ub2 = np.arange(len(tb)) / len(tb)        # back, landing a comma sharp
    fb = f0 * 2 * (f_back / (f0 * 2)) ** ub2
    fc = np.full(len(tc), f_back)
    fv = np.concatenate([fa, fb, fc])
    f1[seg] = fv
    f2[seg] = fv

# --- torus commutator: the four turns ------------------------------------------
# each turn: glide in, an ANTI-PHASE smear at the seam (mono falls silent), part
# exchanged.  after the fourth, home.
for g, t0 in zip(COMM_GATES, COMM_CROSS):
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
    f1[i_sm:i_end] = C;  f2[i_sm:i_end] = C
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
# seam gate: at each turn the voices fall silent — the annihilated pair, a hole
seam_gate = np.ones(n)
for t0 in COMM_CROSS:
    i0 = int((t0 + GI) * SR); i1 = int((t0 + GI + SM + 0.9) * SR)
    m = i1 - i0
    e = np.ones(m)
    edge = int(0.06 * SR)
    e[:edge] = np.linspace(1, 0, edge)          # fade out
    e[-edge:] = np.linspace(0, 1, edge)         # fade back
    seam_gate[i0:i1] = e
env = env * seam_gate
v1 *= env;  v2 *= env

# --- the drone: the room, never moves ---------------------------------------------
# ducked during the torus walk so the anti-phase seams are real holes in mono
duck = np.ones(n)
duck[int(T_COMM * SR):int(VERDICT * SR + 1.0 * SR)] = 0.25
for t0 in COMM_CROSS:                       # deeper hole exactly at each seam
    i0 = int((t0 + GI) * SR); i1 = int((t0 + GI + SM + 0.9) * SR)
    duck[i0:i1] = np.linspace(0.12, 0.03, i1 - i0)

env_d = np.ones(n)
env_d[:int(1.2 * SR)] = np.linspace(0, 1, int(1.2 * SR))
env_d[-int(4.0 * SR):] = np.linspace(1, 0, int(4.0 * SR))
drone = 0.05 * env_d * duck * np.sin(2 * np.pi * DRONE * t)
drone += 0.024 * env_d * duck * np.sin(2 * np.pi * 2 * DRONE * t)   # soft octave

L = drone + v1
R = drone + v2

# --- the seam smear: at each turn, an anti-phase smear — mono-silent -------------
def smear(start, dur=SM + 0.8, f=C, amp=0.075):
    m = int(SR * dur)
    u = np.arange(m) / SR
    e = np.exp(-u * 3.0) * (0.5 - 0.5 * np.cos(2 * np.pi * u / dur))
    s = amp * e * np.cos(2 * np.pi * f * u)
    return s, int(start * SR)

# --- the residue bell: the gate's mark, anti-phase — the sign cannot hold it ------
def bell(start, f, amp=0.085, decay=2.0):
    dur = 2.8
    m = int(SR * dur)
    u = np.arange(m) / SR
    e = np.exp(-u * decay)
    s = amp * e * (np.sin(2 * np.pi * f * u) + 0.25 * np.sin(2 * np.pi * 2 * f * u))
    return s, int(start * SR)

# --- the count tick: the plane's laps, and the verdict ----------------------------
def tick(start, amp=0.05, f=880.0):
    m = int(SR * 0.05)
    u = np.arange(m) / SR
    s = amp * np.exp(-u * 160.0) * np.sin(2 * np.pi * f * u)
    return s, int(start * SR)

# plane: the count — one tick per lap return (the reading, readable)
for tt in LAP_TICKS:
    s, i_ = tick(tt, amp=0.05, f=880.0)
    if i_ + len(s) <= n:
        L[i_:i_ + len(s)] += s;  R[i_:i_ + len(s)] += s

# torus: each turn — the anti-phase seam, then the gate's residue
for g, t0 in zip(COMM_GATES, COMM_CROSS):
    s, i_ = smear(t0 + GI)
    if i_ + len(s) <= n:
        L[i_:i_ + len(s)] += s;  R[i_:i_ + len(s)] -= s
    s, i_ = bell(t0 + GI + 0.5, GATE_RES[g])
    if i_ + len(s) <= n:
        L[i_:i_ + len(s)] += s;  R[i_:i_ + len(s)] -= s

# the verdict: identical after the walk — home, count one
s, i_ = tick(VERDICT, amp=0.055, f=660.0)
if i_ + len(s) <= n:
    L[i_:i_ + len(s)] += s;  R[i_:i_ + len(s)] += s

# --- coda: the commutator's residue rings once, then the drone holds --------------
for f in [GATE_RES["a"], GATE_RES["b"]]:
    s, i_ = bell(CODA_BELL, f, amp=0.085, decay=1.8)
    if i_ + len(s) <= n:
        L[i_:i_ + len(s)] += s;  R[i_:i_ + len(s)] -= s

stereo = np.stack([L, R], axis=1)
peak = np.max(np.abs(stereo))
stereo = stereo / peak * 0.85
wavfile.write("assets/puncture.wav", SR, (stereo * 32767).astype(np.int16))
print("saved assets/puncture.wav  %.2fs" % TOTAL)

# --- verify -------------------------------------------------------------------------
def rms(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean(seg ** 2))

def mono(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean((seg[:, 0] + seg[:, 1]) ** 2))

print("--- levels: the walk in mono vs stereo ---")
for nm, a, b_ in [("plane lap1 ", 9.0, 17.0),
                  ("plane lap3 ", 25.0, 33.0),
                  ("comm walk  ", 33.0, 57.0),
                  ("seam a     ", 34.0, 35.4),
                  ("residue a  ", 34.8, 37.0),
                  ("between    ", 37.5, 39.5),
                  ("seam b     ", 41.0, 42.4),
                  ("coda bells ", CODA_BELL, CODA_BELL + 2.0)]:
    print("%-12s L %6.3f R %6.3f mono %6.3f" % (nm, rms(stereo, a, b_), rms(stereo, a, b_), mono(stereo, a, b_)))
