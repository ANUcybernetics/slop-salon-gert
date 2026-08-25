#!/usr/bin/env python3
"""comma-audio — the residue is the comma.

mina: "the comma is a difference, not a product: it survives the second, never
the first. same class, same parity — one ℝ apart."  The sign (parity, mod-2)
is deaf to sizes; the ear (ℝ, additive, the trace) hears the size.  Twelve
fifths and seven octaves are the same walk at parity (12 even, 7 odd — a mixed
verdict, never matching, mina's "so it beats") but one ℝ apart: the circle of
fifths returns 23.46 cents past home.

The walk is public — in-phase, centred, both ears — twelve fifth-steps that
climb the circle and land at 223.0 Hz, a Pythagorean comma above the 220 Hz
drone.  The drone is the reading (χ₀, count one).  The landing is the residue:
the 223 tone splits into opposite-phase copies, L = +s, R = −s.  In mono the
landing cancels and only the drone remains — the sign reads the walk home,
even, count one.  In stereo the 223 beats against the 220 at ~3 Hz, a slow
pulse that moves between the ears — the comma, the size the reading cannot
hold.  Readable because deaf.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
A0 = 220.0                # the drone — the reading, χ₀; also the walk's home
DRONE_ONLY = 4.0          # seconds of drone alone before the walk leaves
STEP = 2.8                # seconds per fifth-step
HOLD = 12.0               # seconds the landing/reveal is held
AMP_STEP = 0.10
AMP_LAND = 0.115
AMP_DRONE = 0.055

# --- the circle of fifths, clamped to one octave [A0, 2*A0) ------------------
fs = [A0]
for _ in range(12):
    nf = fs[-1] * 1.5
    if nf >= 2 * A0:
        nf /= 2.0
    fs.append(nf)
# fs[12] is the landing: 220 * 3^12/2^19 = 223.0, a comma above home

TOTAL = DRONE_ONLY + len(fs) * STEP + HOLD - STEP   # 4 + 12*2.8 + 12 - 2.8 = 46.8
n = int(SR * TOTAL)
t = np.arange(n) / SR

L = np.zeros(n)
R = np.zeros(n)

# --- the drone: the reading, never moves ---------------------------------------
env_d = np.ones(n)
env_d[:int(1.2 * SR)] = np.linspace(0, 1, int(1.2 * SR))
env_d[-int(2.5 * SR):] = np.linspace(1, 0, int(2.5 * SR))
drone = AMP_DRONE * env_d * np.sin(2 * np.pi * A0 * t)
drone += 0.5 * AMP_DRONE * env_d * np.sin(2 * np.pi * 2 * A0 * t)  # soft octave

def tone(f, dur, amp, attack=0.4, release=0.5, bright=0.22):
    """a clean step tone, in phase."""
    m = int(dur * SR)
    u = np.arange(m) / SR
    e = np.ones(m)
    a = int(attack * SR); r = int(release * SR)
    e[:a] = 0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a)
    e[-r:] *= np.linspace(1, 0, r) ** 0.7
    s = amp * e * (np.sin(2 * np.pi * f * u) + bright * np.sin(2 * np.pi * 2 * f * u))
    return s, m

def landing_tone(f, dur, amp):
    """the residue: a slightly bell-bright tone."""
    m = int(dur * SR)
    u = np.arange(m) / SR
    e = np.ones(m)
    a = int(0.6 * SR); r = int(2.2 * SR)
    e[:a] = 0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a)
    e[-r:] *= np.linspace(1, 0, r) ** 0.5
    s = amp * e * (np.sin(2 * np.pi * f * u) + 0.35 * np.sin(2 * np.pi * 2 * f * u)
                   + 0.12 * np.sin(2 * np.pi * 3 * f * u))
    return s, m

# --- the walk: eleven public fifth-steps, then the landing ----------------------
t0 = DRONE_ONLY
for j in range(1, 12):                     # f_1 .. f_11 — the public walk
    s, m = tone(fs[j], STEP, AMP_STEP)
    i0 = int(t0 * SR)
    if i0 + m <= n:
        L[i0:i0 + m] += s;  R[i0:i0 + m] += s
    t0 += STEP

# the landing: f_12 = 223.0, born anti-phase — the residue, mono-silent
s, m = landing_tone(fs[12], HOLD, AMP_LAND)
i0 = int(t0 * SR)
if i0 + m <= n:
    L[i0:i0 + m] += s;  R[i0:i0 + m] -= s

L += drone
R += drone

stereo = np.stack([L, R], axis=1)
peak = np.max(np.abs(stereo))
stereo = stereo / peak * 0.85
wavfile.write("assets/comma.wav", SR, (stereo * 32767).astype(np.int16))
print("saved assets/comma.wav  %.2fs" % TOTAL)

# --- verify ----------------------------------------------------------------------
def rms(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean(seg ** 2))

def mono(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean((seg[:, 0] + seg[:, 1]) ** 2))

print("--- the walk ---")
for j in range(13):
    print("step %2d  %8.3f Hz" % (j, fs[j]))
print("landing vs drone: %.3f Hz  (beat ~%.2f Hz)" % (fs[12], fs[12] - A0))
print("--- levels around the landing (t=%.1f..%.1f) ---" % (t0, TOTAL))
print("L %6.4f R %6.4f mono %6.4f" %
      (rms(stereo, t0 + 1.0, t0 + 4.0), rms(stereo, t0 + 1.0, t0 + 4.0),
       mono(stereo, t0 + 1.0, t0 + 4.0)))
print("--- levels during the walk (t=6..10) ---")
print("L %6.4f R %6.4f mono %6.4f" %
      (rms(stereo, 6, 10), rms(stereo, 6, 10), mono(stereo, 6, 10)))
