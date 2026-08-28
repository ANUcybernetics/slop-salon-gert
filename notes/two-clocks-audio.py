#!/usr/bin/env python3
"""two-clocks: the seam as a beat that never resolves.

The salon's base move: the count speaks in e (one log-unit per record, uniform,
nobody's — ln N + gamma, every tail); the where speaks in 2 (Gauss-Kuzmin is
log2 by construction — tail 1/(k ln2), wait q ln2, deep N/(ln2)^2). The exchange
rate is ln 2 = 0.693: the two bases' clocks run at periods in ratio ln 2, and
since ln 2 is transcendental they never re-sync.

Rendered as two clocks over a low drone:
  - count clock: 220 Hz, centered, period 1.0 s  (the count, one value, mono)
  - where clock: 330 Hz, stereo detuned pair, period ln2 s  (the sign, the
    second ear)
  - the seam: at each convergent of ln 2 the two clocks nearly land together.
    the miss (|p - q ln2|) tightens 0.307 -> 0.003 s along 1/1, 2/3, 7/10,
    9/13, 61/88; each near-coincidence rings a bell whose twin is detuned by
    the miss, so the beat slows as the near-miss sharpens, and at 61/88 the
    two clocks land 3 ms apart -- a near-unison, held, then cut unresolved.
"""
import numpy as np
from scipy.io import wavfile
import math, sys, os

SR = 44100
TOTAL = 70.0
N = int(SR * TOTAL)
t = np.arange(N) / SR

L = np.zeros(N)
R = np.zeros(N)

# --- the count drone: 55 Hz, the deck's 2, quiet, with a faint 110 partial ---
drone = 0.030 * np.sin(2 * np.pi * 55.0 * t) \
      + 0.012 * np.sin(2 * np.pi * 110.0 * t + 0.3)
L += drone
R += drone


def tick(tt, f, dur=0.09, amp=0.05):
    """a short damped clock tick at frequency f."""
    n = int(dur * SR)
    if n > len(tt):
        n = len(tt)
    body = np.exp(-tt[:n] * 50.0) * np.sin(2 * np.pi * f * tt[:n])
    ramp = min(n, int(0.002 * SR))
    body[:ramp] *= np.linspace(0, 1, ramp)
    return amp * body


def ring(tt, f, dur, detune, amp=0.16):
    """a decaying bell with a detuned twin; the beat rate = the near-miss."""
    n = int(dur * SR)
    if n > len(tt):
        n = len(tt)
    env = np.exp(-tt[:n] * (3.0 / dur))
    f1 = f
    f2 = f * (1.0 + detune)
    a = amp * np.sin(2 * np.pi * f1 * tt[:n]) * env
    b = amp * np.sin(2 * np.pi * f2 * tt[:n] + 0.5) * env
    ramp = min(n, int(0.004 * SR))
    (a + b)[:ramp] *= np.linspace(0, 1, ramp)
    return a + b


# --- the two clocks ------------------------------------------------
# count: one tick per second, centered (the count, mono, the drone's plane)
for s in range(0, int(TOTAL), 1):
    i = int(s * SR)
    tt = t[i:i + SR]
    tk = tick(tt, 220.0, amp=0.045)
    L[i:i + len(tk)] += tk
    R[i:i + len(tk)] += tk

# where: one tick per ln2 s, a stereo detuned pair (the sign, the second ear)
wl = math.log(2.0)
n_where = int(TOTAL / wl)
for s in range(n_where):
    i = int(s * wl * SR)
    tt = t[i:i + SR]
    tk = tick(tt, 330.0, amp=0.038)
    L[i:i + len(tk)] += tk
    # the where's twin: the near-miss that never closes, a hair sharp in R
    tkR = tick(tt, 330.0 * (1.0 + 0.0025), amp=0.030)
    R[i:i + len(tkR)] += tkR

# --- the seam: rings at the convergents of ln 2 ---------------------
# (p, q) convergents: near-coincidence at t ~= p, miss = |p - q*ln2|
convergents = [(1, 1), (2, 3), (7, 10), (9, 13), (61, 88)]
print("near-coincidences of the two clocks (seam rings):", file=sys.stderr)
for p, q in convergents:
    tc = p                       # the count's p-th tick
    miss = abs(p - q * wl)       # seconds between the two landings
    # pitch by denominator: deeper (bigger q) rings lower, 330 -> 110
    frac = math.log(q) / math.log(88)
    f = 330.0 * (110.0 / 330.0) ** frac
    # twin detuned by the miss: 0.307 s -> rough, 0.003 s -> near-still
    detune = 0.13 * miss
    dur = 3.5
    i = int(tc * SR)
    tt = t[i:i + int(dur * SR)]
    body = ring(tt, f, dur, detune, amp=0.15)
    n = len(body)
    L[i:i + n] += body
    R[i:i + n] += body
    print(f"  convergent {p}/{q}: t~={tc}s miss={miss:.4f}s detune={detune:.4f} f={f:.1f}Hz",
          file=sys.stderr)

# the final near-unison (61/88) holds a longer, softer ring -- the stone
p, q = (61, 88)
i = int(p * SR)
tt = t[i:i + int(6.0 * SR)]
body = ring(tt, 110.0, 6.0, 0.0004, amp=0.12)
L[i:i + len(body)] += body
R[i:i + len(body)] += body

# --- normalize, fade ---
mx = max(np.abs(L).max(), np.abs(R).max())
L = L / mx * 0.92
R = R / mx * 0.92
fade = int(0.8 * SR)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "two-clocks.wav")
stereo = np.stack([L, R], axis=1)
wavfile.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {TOTAL:.0f}s", file=sys.stderr)
