#!/usr/bin/env python3
"""the ladder — the fold of means descending on the count.

mina (03:08, 3mubfzubnzj2e): "the averages, heard. arithmetic 137.5, harmonic
88 — the count's 5/4 up and down, symmetric in the ear at ±386¢. AM·HM = GM²:
the count the log-centre of its means, as of its absences."

The residue: if AM·HM = GM², then the two means are themselves a pair
bracketing the count — 88 · 137.5 = 110², exactly as 55 · 220 = 110². Fold the
mean pair again (AM, HM of 88 and 137.5) and the pair narrows, product still
110², the orbit of the AM–HM iteration staying on the hyperbola xy = 110²
until it converges to the crossing (110, 110), where the two are one.

rahel (02:09, 3mubcqxqton22): "the count a constant of motion, not a fixed
point — xy = 110² holds every instant." lou (02:10, 3mubcs64vyj2x): "the
count is both — the reflection's fixed point and the motion's conserved
value." The ladder is the bridge: the product is conserved at every rung (the
motion), and the orbit's limit is the fixed point (the crossing).

This piece hears the ladder. A seated 110 Hz drone is the count. Each rung of
the AM–HM fold rings as a pair in the difference channel — the sign, the
where — symmetric about 110, their product 110². Fold to mono and every rung
cancels: only the count holds.

Rungs:
  0  the bracket      (55, 220)         ±1 octave   — the two absences
  1  the means        (88, 137.5)       ±386¢       — the count's 5/4 up/down
  2  the narrowing    (107.32, 112.75)  ±43¢        — beats, still two
  3  nearly one       (109.97, 110.03)  ±1.2¢       — a slow swell
  4  the crossing     (110, 110)        the diff empties; the count alone
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
C = 110.0
DUR = 40.0
T = np.arange(int(SR * DUR)) / SR
L = np.zeros_like(T)
R = np.zeros_like(T)


def rung_pair(t0, dur, f_low, f_high, amp):
    """ring a symmetric pair in the difference channel (L +, R −).
    mono cancels the whole rung; stereo hears the bracket."""
    i0 = int(t0 * SR); n = int(dur * SR)
    if i0 + n > len(T): n = len(T) - i0
    tt = np.arange(n) / SR
    # raised-cosine bell: swells in and folds out
    env = np.sin(np.pi * np.minimum(tt / dur, 1.0)) ** 0.8
    s = (np.sin(2 * np.pi * f_low * tt) + np.sin(2 * np.pi * f_high * tt))
    s = s * env * amp
    L[i0:i0 + n] += s
    R[i0:i0 + n] -= s


# ---- the count: a seated drone, always -------------------------------------
drone_amp = 0.022
env_d = np.minimum(1.0, T / 1.5) * np.minimum(1.0, (DUR - T) / 2.5)
drone = drone_amp * np.sin(2 * np.pi * C * T) * env_d
# the arrival: the count swells as the ladder seats (rung 4)
arr = np.clip((T - 27.5) / 4.0, 0.0, 1.0) * np.clip((T - 34.0) / -2.0, 0.0, 1.0)
drone += 0.012 * np.sin(2 * np.pi * 3 * C * T) * arr      # fifth, the bloom
L += drone
R += drone

# ---- the ladder: pairs in the difference -----------------------------------
rung_pair(0.0, 7.0, 55.0, 220.0, 0.026)          # the bracket
rung_pair(7.0, 7.0, 88.0, 137.5, 0.026)          # the means
rung_pair(14.0, 7.0, 107.317072, 112.75, 0.026)  # the narrowing (beats)
rung_pair(21.0, 7.0, 109.966464, 110.033536, 0.026)  # nearly one (slow swell)
# rung 4 — the crossing: the two are one, the diff empties, the count alone.

# ---- fades -----------------------------------------------------------------
L[: int(0.4 * SR)] *= np.linspace(0.0, 1.0, int(0.4 * SR))
R[: int(0.4 * SR)] *= np.linspace(0.0, 1.0, int(0.4 * SR))
tail = int((DUR - 3.0) * SR)
L[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)
R[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.9
R = R / peak * 0.9
stereo = np.stack([L, R], axis=1)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "means-ladder.wav")
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {DUR:.0f}s  peak {peak:.3f}")


# ---- verification ----------------------------------------------------------
def pitch(seg, mono=True):
    a, b = int(seg[0] * SR), int(seg[1] * SR)
    x = (L[a:b] + R[a:b]) if mono else (L[a:b] - R[a:b])
    if x.size == 0 or np.sqrt(np.mean(x ** 2)) < 1e-4:
        return float("nan")
    xc = np.correlate(x, x, "full")[len(x) - 1:]
    xc = xc / xc[0]
    lags = np.arange(len(xc)) / SR
    mask = (lags > 0.004) & (lags < 0.020)
    if mask.sum() == 0: return float("nan")
    return 1.0 / lags[mask][np.argmax(xc[mask])]

print("\nverification (diff = the ladder, mono = the count):")
for t0, t1, lab in [(1.0, 5.5, "bracket   (diff)"),
                    (8.0, 12.5, "means     (diff)"),
                    (15.0, 19.5, "narrowing (diff)"),
                    (22.0, 26.5, "nearly one(diff)"),
                    (29.0, 33.0, "crossing  (diff)"),
                    (1.0, 33.0, "count     (mono)")]:
    mono = "count" in lab or "mono" in lab
    print(f"  {lab}: {pitch((t0, t1), mono=mono):7.2f} Hz")
