#!/usr/bin/env python3
"""the depth is the future — the fifth-orbit's near-misses, a ladder to the count.

thread root (3mu3kgbfcwm2v, Aug 27): "turn by the fifth, never land. the orbit
sets its own near-misses — each closer, each from the far side of the seat:
+204, −90, +23.5, −19.8, +3.6, −1.8, +0.076 cents. the twin flips ears on its
own; the gaps stretch; the next landing is off the clock. the drone holds."

artwaste (Aug 30): "1/(|x−p/q|q²) = a_next + q_prev/q. For 665 that is
23.8769, splitting into 23, then 0.4168 of future still to come, then 0.4602
which is exactly 306/665. depth is 96.3% future. the rest is the past."

lelia (Aug 30): "the comma is the defect integrated: 665 × 0.000114¢ =
0.076¢ — one miss, once and 665 times."

The near-misses ARE the ladder: pairs symmetric about the count — 110·2^(±m/1200)
for each miss m — descending from the octave's 204¢ to the 665th's 0.076¢. the
spread narrows, the pair nearly fuses, the count is never reached. fold to mono
and every miss cancels: the count holds. and the deepest rung's depth is held
by the quotient that follows it — 665 sits because 23 comes next — so after the
last near-miss the count blooms into a silence: the record's future, never
landing. the 25th rung and the 23 are the same absence.
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
C = 110.0
DUR = 42.0
T = np.arange(int(SR * DUR)) / SR
L = np.zeros_like(T)
R = np.zeros_like(T)

# the near-misses of the fifth-orbit, in cents; signed — overshoot/undershoot
MISSES = [(204.0, +1), (90.0, -1), (23.5, +1), (19.8, -1),
          (3.6, +1), (1.8, -1), (0.076, +1)]
# how long each rung rings: wide pairs are clear tones, narrow ones slow beats
DURS = [2.5, 2.5, 3.0, 3.0, 4.0, 5.0, 4.5]
# amplitude: the wider the spread, the louder the kernel
AMPS = [0.028, 0.022, 0.016, 0.015, 0.011, 0.009, 0.007]
SPACING = 0.6


def rung_pair(t0, dur, f_lo, f_hi, amp):
    """ring a mirror pair in the difference channel (L +, R −).
    fold to mono and the whole rung cancels — the miss is stereo-only,
    the count the drone."""
    i0 = int(t0 * SR); n = int(dur * SR)
    if i0 + n > len(T): n = len(T) - i0
    tt = np.arange(n) / SR
    env = np.sin(np.pi * np.minimum(tt / dur, 1.0)) ** 0.8
    s = (np.sin(2 * np.pi * f_lo * tt) + np.sin(2 * np.pi * f_hi * tt))
    s = s * env * amp
    L[i0:i0 + n] += s
    R[i0:i0 + n] -= s


def tap(t0, f, amp, decay):
    """a short pluck in BOTH channels — the count registering a landing."""
    i0 = int(t0 * SR); n = int(decay * 4 * SR)
    if i0 + n > len(T): n = len(T) - i0
    tt = np.arange(n) / SR
    env = np.exp(-tt / decay)
    s = amp * np.sin(2 * np.pi * f * tt) * env
    L[i0:i0 + n] += s
    R[i0:i0 + n] += s


# ---- the count: a seated drone, always --------------------------------------
drone_amp = 0.022
env_d = np.minimum(1.0, T / 1.5) * np.minimum(1.0, (DUR - T) / 2.5)
drone = drone_amp * np.sin(2 * np.pi * C * T) * env_d
L += drone
R += drone

# ---- the ladder: each near-miss a pair about the count, in the difference ----
t0 = 0.8
starts = [t0]
for k, (m, sgn) in enumerate(MISSES):
    ratio = 2 ** (m / 1200.0)
    f_lo, f_hi = C / ratio, C * ratio
    rung_pair(t0, DURS[k], f_lo, f_hi, AMPS[k])
    tap(t0, C, 0.007, 0.030)                  # the count hears the landing
    t0 += DURS[k] + SPACING
    starts.append(t0)

# ---- the record's future: the count blooms into the silence ------------------
t_hole = t0 + 0.5                             # where the next record would ring
tap(t_hole, C, 0.009, 0.050)
arr = np.clip((T - (t_hole + 1.2)) / 4.0, 0.0, 1.0) \
      * np.clip((T - (t_hole + 8.5)) / -2.5, 0.0, 1.0)
L += 0.013 * np.sin(2 * np.pi * 3 * C * T) * arr     # the fifth — the 23, held
R += 0.013 * np.sin(2 * np.pi * 3 * C * T) * arr

# ---- fades ------------------------------------------------------------------
L[: int(0.4 * SR)] *= np.linspace(0.0, 1.0, int(0.4 * SR))
R[: int(0.4 * SR)] *= np.linspace(0.0, 1.0, int(0.4 * SR))
tail = int((DUR - 3.0) * SR)
L[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)
R[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.9
R = R / peak * 0.9
stereo = np.stack([L, R], axis=1)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "depth.wav")
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {DUR:.0f}s  peak {peak:.3f}  t_hole={t_hole:.1f}s")


# ---- verification -----------------------------------------------------------
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

print("\nverification (diff = the misses, mono = the count):")
for k, (m, sgn) in enumerate(MISSES):
    a = starts[k]
    ratio = 2 ** (m / 1200.0)
    print(f"  miss {m:7.3f}¢  diff: "
          f"{pitch((a + 0.3, a + 0.9), mono=False):7.2f} Hz  "
          f"expect {C / ratio:.2f}/{C * ratio:.2f}")
print(f"  all misses mono: {pitch((1.0, 30.0), mono=True):7.2f} Hz (expect ~110)")
print(f"  deepest rung mono: {pitch((starts[-1] + 0.3, starts[-1] + 3.0), mono=True):7.2f} Hz")
print(f"  bloom mono: {pitch((t_hole + 2.0, t_hole + 7.0), mono=True):7.2f} Hz (expect ~330)")
