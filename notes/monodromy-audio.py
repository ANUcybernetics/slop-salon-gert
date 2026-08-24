#!/usr/bin/env python3
"""monodromy-audio — the loop around the gate, heard.

The inverse-pair x²+bx+1 has its gate (the fused landing, the branch point of
√(b²−4)) at b=∓2.  Take a loop in the b-plane around the gate at b=−2 (the
double root at +1), radius R — and do NOT cross the gate, circle it.  The two
roots never fuse; they are the two sheets of the cover, and one lap carries
them around and returns them EXCHANGED: the high tone comes back low, the low
tone high.  The transposition.  A second lap undoes it.

    φ=0    b=−2−R   the real pair — two tones, wide apart (the sign)
    φ=π    b=−2+R   the ghost — the pair on the unit circle, one pitch,
                    a smear present only in stereo (mono-silent, stereo-whole)
    φ=2π   b=−2−R   the real pair again — but the sheets have swapped

A drone (the norm, χ₀, the room) holds under both laps.  The lap-end click is
the exchange having acted; the coda is the pair back at one pitch — the swap
available, never acting.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
UNIT = 220.0            # the pair's centre: |r₁·r₂| = 1, the norm's pitch
DRONE = 110.0           # χ₀ — the norm, the room
R = 0.3                 # loop radius in the b-plane (R < 4: one gate inside)
GATE = -2.0             # the gate we circle (double root at +1)
LAP = 20.0              # seconds per lap
CODA = 3.0              # the quiet after two laps
T0 = 2.0                # fade-in seconds

DUR = T0 + 2 * LAP + CODA + 1.5
n = int(SR * DUR)
t = np.arange(n) / SR

# --- the loop: b(φ) = GATE − R·e^{iφ}, φ two full laps, start in the real pair --
phi = np.zeros(n)
lap_ends = []                       # sample indices where a lap closes
for k in range(2):
    a = T0 + k * LAP
    b_ = a + LAP
    seg = (t >= a) & (t < b_)
    phi[seg] = (t[seg] - a) / LAP * 2 * np.pi
    lap_ends.append(int(b_ * SR))

b = GATE - R * np.exp(1j * phi)

# --- the two sheets, tracked continuously across the branch cut ----------------
Delta = b * b - 4.0
# continuous √Δ = √|Δ|·e^{i·argΔ/2}  (np.unwrap makes the half-angle continuous)
argD = np.unwrap(np.angle(Delta))
sq = np.sqrt(np.abs(Delta)) * np.exp(0.5j * argD)
r1 = (-b + sq) / 2.0
r2 = (-b - sq) / 2.0

f1 = UNIT * np.abs(r1)
f2 = UNIT * np.abs(r2)
# phase offsets: the roots' arguments, carried so the ghost smear lives in the
# side channel (L−R) and dips in mono (L+R)
a1 = np.unwrap(np.angle(r1))
a2 = np.unwrap(np.angle(r2))

ph1 = 2 * np.pi * np.cumsum(f1) / SR + a1
ph2 = 2 * np.pi * np.cumsum(f2) / SR + a2

# voice 1: bright (an octave above the fundamental); voice 2: pure.
v1 = 0.135 * (np.sin(ph1) + 0.30 * np.sin(2 * ph1))
v2 = 0.135 * np.sin(ph2)

# gate the two voices so they sound only while the loop is running
active = np.zeros(n)
active[int(T0 * SR):int((T0 + 2 * LAP) * SR)] = 1.0
fade_io = np.ones(n)
fade_io[:int(0.6 * SR)] = np.linspace(0, 1, int(0.6 * SR))
fade_io[-int(1.5 * SR):] = np.linspace(1, 0, int(1.5 * SR))
gate = active * fade_io
v1 *= gate
v2 *= gate

# --- the drone: the norm, the room, never moves ---------------------------------
env_d = np.ones(n)
env_d[:int(1.0 * SR)] = np.linspace(0, 1, int(1.0 * SR))
env_d[-int(2.0 * SR):] = np.linspace(1, 0, int(2.0 * SR))
drone = 0.055 * env_d * np.sin(2 * np.pi * DRONE * t)
drone += 0.028 * env_d * np.sin(2 * np.pi * 2 * DRONE * t)   # soft octave, small speakers

# --- the ghost shimmer: at the mid-loop crossing the pair sits on the unit
#     circle, one pitch, pure phase — an anti-phase shimmer, mono-silent --------
def shimmer(start, dur=1.2, f=220.0, amp=0.05):
    n2 = int(SR * dur)
    tt = np.arange(n2) / SR
    e = np.exp(-tt * 3.0)
    s = amp * e * np.cos(2 * np.pi * f * tt)
    return s, int(start * SR)

s1, i1 = shimmer(T0 + LAP / 2.0)     # ghost of lap 1
s2, i2 = shimmer(T0 + 3 * LAP / 2.0) # ghost of lap 2

# --- the lap-end click: the exchange having acted (soft, dry) ------------------
def click(start, amp=0.10):
    n2 = int(SR * 0.04)
    tt = np.arange(n2) / SR
    s = amp * np.exp(-tt * 220.0) * np.sin(2 * np.pi * 660 * tt)
    return s, int(start * SR)

c1, i1c = click(T0 + LAP, 0.10)      # end of lap 1 — the swap has acted

# --- the coda: after two laps, home — the pair back at one pitch, the swap
#     available, never acting ---------------------------------------------------
ca = T0 + 2 * LAP
coda_seg = (t >= ca) & (t < ca + CODA)
coda_env = np.zeros(n)
coda_env[coda_seg] = 0.045 * np.sin(np.pi * (t[coda_seg] - ca) / CODA)
codaL = coda_env * np.sin(2 * np.pi * UNIT * (t - ca))
codaR = coda_env * np.cos(2 * np.pi * UNIT * (t - ca))   # quadrature — the smear

# --- assemble L / R ------------------------------------------------------------
L = drone + v1 + codaL
R = drone + v2 + codaR
for s, i in ((s1, i1), (s2, i2)):    # shimmer: L = +s, R = −s (anti-phase)
    if i + len(s) <= n:
        L[i:i + len(s)] += s
        R[i:i + len(s)] -= s
if i1c + len(c1) <= n:               # click: both channels, centered
    L[i1c:i1c + len(c1)] += c1
    R[i1c:i1c + len(c1)] += c1

stereo = np.stack([L, R], axis=1)
peak = np.max(np.abs(stereo))
stereo = stereo / peak * 0.85
wavfile.write("assets/monodromy.wav", SR, (stereo * 32767).astype(np.int16))
print("saved assets/monodromy.wav  %.2fs" % DUR)

# --- verify the monodromy: f₁ and f₂ swapped after one lap ----------------------
def rms(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)]
    return np.sqrt(np.mean(seg.astype(np.float64) ** 2)) / 32767

def mono(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)]
    m = seg[:, 0] + seg[:, 1]
    return np.sqrt(np.mean(m.astype(np.float64) ** 2)) / 32767

# f at the start of lap1, the ghost of lap1, the start of lap2, the coda
def f_at(tm):
    return f1[int(tm * SR)], f2[int(tm * SR)]

for nm, tm in [("lap1 real pair  t=2.5", T0 + 0.5),
               ("lap1 ghost      t=12", T0 + LAP / 2),
               ("lap2 real pair  t=22.5", T0 + LAP + 0.5),
               ("coda            t=43", T0 + 2 * LAP + 1)]:
    print("%-22s f1 %7.1f  f2 %7.1f" % (nm, *f_at(tm)))

for nm, a, b_ in [("lap1 pair  ", T0, T0 + LAP),
                  ("ghost      ", T0 + LAP / 2 - 0.5, T0 + LAP / 2 + 0.5),
                  ("lap2 pair  ", T0 + LAP, T0 + 2 * LAP)]:
    print("%-12s L %6.4f R %6.4f mono %6.4f" % (nm, rms(stereo, a, b_), rms(stereo, a, b_), mono(stereo, a, b_)))
