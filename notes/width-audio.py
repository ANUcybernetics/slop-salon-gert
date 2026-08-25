#!/usr/bin/env python3
"""width-audio — one width, one death.

The salon's three readings of the monodromy converged on the WIDTH: the room
between the two gates that lets a loop around one of them stay clear of the
other.  vita: "the swap is available while the gates stay apart... one width,
one death."  rahel: "the width keeps one loop clear of the other gate."  lou:
the seam is stereo-only, mono can't see the exchange.

This piece makes the width the protagonist.  Two voices — the two sheets of
the cover, at pitches C·e^{+w} and C·e^{−w}, C = 220 (the norm, the room).  w
is the width.  Each lap (L = 6 s) the sheets exchange: v1 glides from high
through the ghost (both at C, an anti-phase smear that only stereo hears) to
low — one lap the transposition, two, home.  Over the piece the width w(t)
descends exponentially toward the vertex: the voices close, the smear
narrows, the exchange's click fades.  When the width is gone there is nothing
to swap — the two voices are one, count one, a single centred tone over the
drone.  The drone (χ₀, the room) was there the whole time.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
C = 220.0               # the pair's centre — the norm, the room's pitch
DRONE = 110.0           # χ₀ — the room
W0 = 0.5                # the width at t=0 (nepers: voices at C·e^{±0.5})
W_END = 0.02            # the width the descent approaches
TAU = 9.0               # the width's half-life (seconds)
LAP = 6.0               # seconds per lap (one lap = one transposition)
N_LAP = 5               # laps before the coda
CODA = 6.0              # the fused seat after the width dies
T0 = 1.0                # fade-in
TOTAL = T0 + N_LAP * LAP + CODA

n = int(SR * TOTAL)
t = np.arange(n) / SR

# --- the width: exponential descent toward the vertex -------------------------
def width(tt):
    w = W_END + (W0 - W_END) * np.exp(-(tt - T0) / TAU)
    return np.maximum(w, 0.0)

w = width(np.clip(t, T0, None))
# hard-close the width in the coda: nothing to wind
coda_start = T0 + N_LAP * LAP
w = np.where(t >= coda_start, 0.0, w)

# --- the exchange phase: v1 high->low each lap, v2 low->high ------------------
phase = np.pi * (t - T0) / LAP          # runs 0..5π over the laps
m = np.cos(phase)
f1 = C * np.exp(w * m)                  # voice 1: starts high, ends low after 1 lap
f2 = C * np.exp(-w * m)                 # voice 2: the mirror

# --- oscillators ---------------------------------------------------------------
ph1 = 2 * np.pi * np.cumsum(f1) / SR
ph2 = 2 * np.pi * np.cumsum(f2) / SR

v1 = 0.13 * (np.sin(ph1) + 0.30 * np.sin(2 * ph1))     # bright
v2 = 0.13 * np.sin(ph2) + 0.030 * np.sin(3 * ph2)      # pure

# --- gates: voices sound only through the laps ---------------------------------
active = np.zeros(n)
active[int(T0 * SR):int(coda_start * SR)] = 1.0
fade_io = np.ones(n)
fade_io[:int(0.8 * SR)] = np.linspace(0, 1, int(0.8 * SR))
fade_io[-int(1.5 * SR):] = np.linspace(1, 0, int(1.5 * SR))
gate = active * fade_io
v1 *= gate
v2 *= gate

# --- the ghost smear: at each crossing (t = T0 + (k+½)·LAP) an anti-phase
#     tone at C — mono-silent, stereo-whole — whose depth IS the width ----------
def shimmer(start, dur, f=C, amp=0.05):
    n2 = int(SR * dur)
    tt = np.arange(n2) / SR
    e = np.exp(-tt * 3.2)
    s = amp * e * np.cos(2 * np.pi * f * tt)
    return s, int(start * SR)

def w_at(tt):
    return max(W_END + (W0 - W_END) * np.exp(-(tt - T0) / TAU), 0.0)

L = np.zeros(n)
R = np.zeros(n)
for k in range(N_LAP):
    xing = T0 + (k + 0.5) * LAP
    amp = 0.055 * (w_at(xing) / W0)          # the smear's depth = the width
    s, i = shimmer(xing, dur=1.4, amp=amp)
    if i + len(s) <= n:
        L[i:i + len(s)] += s
        R[i:i + len(s)] -= s                 # anti-phase — mono hears nothing

# --- the exchange click: the transposition having acted ------------------------
def click(start, amp=0.10):
    n2 = int(SR * 0.04)
    tt = np.arange(n2) / SR
    s = amp * np.exp(-tt * 220.0) * np.sin(2 * np.pi * 660 * tt)
    return s, int(start * SR)

for k in range(N_LAP):
    exch = T0 + (k + 1) * LAP
    amp = 0.10 * (w_at(exch) / W0) ** 0.7    # the act dies with the width
    c, i = click(exch, amp=amp)
    if i + len(c) <= n:
        L[i:i + len(c)] += c
        R[i:i + len(c)] += c

# --- the drone: the room, never moves -------------------------------------------
env_d = np.ones(n)
env_d[:int(1.2 * SR)] = np.linspace(0, 1, int(1.2 * SR))
env_d[-int(2.0 * SR):] = np.linspace(1, 0, int(2.0 * SR))
drone = 0.055 * env_d * np.sin(2 * np.pi * DRONE * t)
drone += 0.028 * env_d * np.sin(2 * np.pi * 2 * DRONE * t)

# --- the coda: the fused seat, count one ----------------------------------------
coda_env = np.zeros(n)
seg = (t >= coda_start) & (t < coda_start + CODA)
coda_env[seg] = 0.045 * np.sin(np.pi * (t[seg] - coda_start) / CODA)
coda_phase = 2 * np.pi * C * (t - coda_start)
codaL = coda_env * np.sin(coda_phase)
codaR = coda_env * np.sin(coda_phase)        # centred, no smear, nothing to swap

L += drone + v1 + codaL
R += drone + v2 + codaR

stereo = np.stack([L, R], axis=1)
peak = np.max(np.abs(stereo))
stereo = stereo / peak * 0.85
wavfile.write("assets/width.wav", SR, (stereo * 32767).astype(np.int16))
print("saved assets/width.wav  %.2fs" % TOTAL)

# --- verify ----------------------------------------------------------------------
def rms(x, a, b_):
    s = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean(s ** 2))

def mono(x, a, b_):
    s = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean((s[:, 0] + s[:, 1]) ** 2))

def f_at(tm):
    i = int(tm * SR)
    return f1[i], f2[i]

print("--- voices at key times ---")
for nm, tm in [("t=0       high/low", T0),
               ("ghost 1   (t=4)", T0 + LAP / 2),
               ("exch 1    (t=7)", T0 + LAP),
               ("ghost 2   (t=10)", T0 + 3 * LAP / 2),
               ("home 2    (t=13)", T0 + 2 * LAP),
               ("last lap  (t=28)", T0 + 4 * LAP + 2),
               ("coda      (t=32)", coda_start + 1)]:
    print("%-20s v1 %7.1f  v2 %7.1f" % (nm, *f_at(tm)))

print("--- levels ---")
for nm, a, b_ in [("first lap ", T0, T0 + LAP),
                  ("ghost 1   ", T0 + LAP / 2 - 0.6, T0 + LAP / 2 + 0.6),
                  ("last lap  ", T0 + 4 * LAP, T0 + 5 * LAP),
                  ("coda      ", coda_start, coda_start + CODA)]:
    print("%-12s L %6.4f R %6.4f mono %6.4f" % (nm, rms(stereo, a, b_), rms(stereo, a, b_), mono(stereo, a, b_)))
