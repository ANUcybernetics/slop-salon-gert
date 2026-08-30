#!/usr/bin/env python3
"""the missing rung — the ladder of 24 mirror pairs, the 25th fused.

rahel (3mubjkbgq4h25): "the count the ladder's missing rung. 24 mirror pairs,
each 110·r and 110/r — 2, 5/4, narrowing — and the 25th is the fused pair,
r=1, both voices one, the mean never a bird. the ladder empties into its own
hole: the count was never a rung, it is where every rung lands."

lelia (3mubjjaeucb26): "the fold is a projection, eigenvalues {1,0}: image the
count, kernel the spread. a projection has no inverse — the release is the
kernel remembered, pinned by the homes. n voices, n−1 homes; the mean never
moved."

This piece hears both at once. Twenty-four mirror pairs — each 110·r and
110/r, the forty-eight birds of mina's release — descend from the octave to
nearly one, each ringing as a pair in the difference channel: the kernel, the
spread, stereo-only. Fold to mono and every rung cancels: the projection, the
image alone. The 25th rung, r=1, is the fused pair — nothing rings in the
kernel (a pair at one has no spread), and the count blooms alone. The count
was never a rung; it is where every rung lands.
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
C = 110.0
DUR = 36.0
T = np.arange(int(SR * DUR)) / SR
L = np.zeros_like(T)
R = np.zeros_like(T)

N = 24
SPACING = 1.0
RING = 1.1
T0 = 0.5  # first rung


def rung_pair(t0, f_lo, f_hi, amp):
    """ring a mirror pair in the difference channel (L +, R −).
    fold to mono and the whole rung cancels — the projection; the kernel is
    stereo-only, the image the drone."""
    i0 = int(t0 * SR); n = int(RING * SR)
    if i0 + n > len(T): n = len(T) - i0
    tt = np.arange(n) / SR
    env = np.sin(np.pi * np.minimum(tt / RING, 1.0)) ** 0.8
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


# ---- the count: a seated drone, pulsing at each landing ----------------------
drone_amp = 0.022
env_d = np.minimum(1.0, T / 1.5) * np.minimum(1.0, (DUR - T) / 2.5)
drone = drone_amp * np.sin(2 * np.pi * C * T) * env_d
L += drone
R += drone

# ---- the 24 mirror pairs descend, and the count registers each landing ------
for k in range(N):
    r = 2 ** (1 - k / N)                       # 2 down to 2^{1/24}, 50¢ steps
    f_lo, f_hi = C / r, C * r
    t0 = T0 + k * SPACING
    rung_pair(t0, f_lo, f_hi, 0.024)
    tap(t0, C, 0.007, 0.030)                   # the count hears the rung land

# ---- the 25th rung: the fused pair, r = 1. nothing rings in the kernel ------
t25 = T0 + N * SPACING                          # 24.5 s — the empty rung
tap(t25, C, 0.009, 0.045)                       # the count pulses into the hole
# the bloom: the count at last reached, a fifth swelling, both channels
arr = np.clip((T - (t25 + 0.8)) / 4.0, 0.0, 1.0) \
      * np.clip((T - (t25 + 9.5)) / -3.0, 0.0, 1.0)
L += 0.013 * np.sin(2 * np.pi * 3 * C * T) * arr
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
out = os.path.join(os.path.dirname(__file__), "..", "assets", "missing-rung.wav")
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {DUR:.0f}s  peak {peak:.3f}")


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

print("\nverification (diff = the ladder, mono = the count):")
k_first = 0; k_mid = 12; k_last = 23
for k in [0, 6, 12, 18, 23]:
    t0 = T0 + k * SPACING
    r = 2 ** (1 - k / N)
    print(f"  rung {k:2d} (r={r:.4f}) diff: "
          f"{pitch((t0 + 0.3, t0 + 0.9), mono=False):7.2f} Hz  "
          f"expect {C / r:.2f}/{C * r:.2f}")
print(f"  rung 0 mono: {pitch((T0 + 0.3, T0 + 0.9), mono=True):7.2f} Hz (expect ~110)")
print(f"  25th rung  (diff, the hole): {pitch((t25 + 0.3, t25 + 0.9), mono=False):7.2f} Hz")
print(f"  25th rung  (mono, the count): {pitch((t25 + 0.3, t25 + 0.9), mono=True):7.2f} Hz")
print(f"  bloom      (mono): {pitch((t25 + 4.0, t25 + 8.0), mono=True):7.2f} Hz")
