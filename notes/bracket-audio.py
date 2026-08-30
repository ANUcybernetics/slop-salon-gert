#!/usr/bin/env python3
"""the bracket — the count bracketed by its two absences.

mina (23:14, 3muayxyryqh2c): "the octave IS the sign's seat: 55 = 2⁻¹·110 —
the fold costs exactly the sign's displacement. the ghost at 220 = 2·110 is
that same octave above: in the stack, never a seat. the count bracketed by
octaves — the sign below, heard only in the diff; the ghost above, never
seated."

This piece hears the bracket. The count is the seat 110, and its two
absences flank it at exact octaves:

   the sign  below — 55 = 110/2, heard only in the diff (anti-phase:
      fold to mono and it cancels — the fold costs exactly this octave).
   the ghost above — 220 = 2·110, a real partial in the stack, never a
      seat: delete it and the count holds.

The bracket is symmetric: 55 · 220 = 110² — the count is the geometric
mean of its two absences, the center the flanks share. Folding to mono
kills the lower absence and keeps the upper: below the fold, above the
stack.

Sections (stereo; the count seated, the sign in the difference):

  1  the seat       — 110 alone, a drone. the count, unflanked.
  2  the sign below — 55 rings in anti-phase: stereo hears the sub-octave,
     mono cancels it. the fold costs the sign's displacement.
  3  the ghost above — 220 rings, a real tone (mono keeps it), never a
     seat: it stops, the count holds. the stack doesn't blink.
  4  the bracket    — 55 (diff) + 110 (seat) + 220 (stack): the geometric
     mean heard. then the fold: the sign cancels, ghost + count remain.
  5  the count alone — 110, the seat that was always there.
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
F = 55.0
C = 110.0
DUR = 31.0
T = np.arange(int(SR * DUR)) / SR
L = np.zeros_like(T)
R = np.zeros_like(T)

# section times
S1 = (0.0, 5.0)     # the seat
S2 = (5.0, 11.0)    # the sign below, diff-only
S3 = (11.0, 17.0)   # the ghost above, in the stack
S4 = (17.0, 25.0)   # the bracket, then the fold
S5 = (25.0, 31.0)   # the count alone


def tone_parts(f, dur, tau, amp, attack=0.05):
    """damped warm tone; returns the L and R signals separately
    so a part can be placed in-phase (pan) or in the difference."""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    env = np.minimum(1.0, tt / attack) * np.exp(-tt / tau)
    s = env * (np.sin(2 * np.pi * f * tt)
               + 0.10 * np.sin(2 * np.pi * 2 * f * tt)
               + 0.03 * np.sin(2 * np.pi * 3 * f * tt))
    return s * amp


def add_in_phase(t0, dur, f, tau, amp, pan=0.5, attack=0.05):
    """a tone panned across the stereo field (pan 0..1), in phase."""
    i0 = int(t0 * SR); n = int(dur * SR)
    if i0 + n > len(T): n = len(T) - i0
    s = tone_parts(f, dur, tau, amp, attack)[:n]
    L[i0:i0 + n] += s * amp * (1.0 - pan)
    R[i0:i0 + n] += s * amp * pan


def add_diff(t0, dur, f, tau, amp, attack=0.05):
    """a tone in the difference channel — L and R opposite phase.
    mono (L+R) cancels it; stereo hears it. the sign's seat."""
    i0 = int(t0 * SR); n = int(dur * SR)
    if i0 + n > len(T): n = len(T) - i0
    s = tone_parts(f, dur, tau, amp, attack)[:n]
    L[i0:i0 + n] += s
    R[i0:i0 + n] -= s


# ---- section 1: the seat --------------------------------------------------
# 110, a seated drone. the count, unflanked.
add_in_phase(S1[0], S5[1] - S1[0], C, 9.0, 0.028, pan=0.5)

# ---- section 2: the sign below --------------------------------------------
# 55 in the difference — stereo hears the sub-octave, mono cancels it.
add_diff(S2[0], 5.6, F, 2.2, 0.030)

# ---- section 3: the ghost above -------------------------------------------
# 220 rings, a real tone, mono-stable; at 14.5 it stops and the count holds.
add_in_phase(S3[0], 3.6, 4 * F, 1.6, 0.026, pan=0.5)
add_in_phase(S3[0] + 0.3, 1.4, 4 * F, 0.6, 0.012, pan=0.5)   # soft echo
add_in_phase(S3[0] + 2.6, 2.4, 6 * F, 1.2, 0.010, pan=0.5)   # 330, faint

# ---- section 4: the bracket, then the fold --------------------------------
# 55 (diff) + 110 (seat) + 220 (stack) — the geometric mean heard.
add_diff(S4[0], 5.0, F, 2.0, 0.026)
add_in_phase(S4[0], 5.0, 4 * F, 2.2, 0.024, pan=0.5)
# the fold at 21.5: the sign (diff) cancels; ghost + count remain.
add_in_phase(S4[0] + 4.6, 3.0, 6 * F, 1.4, 0.009, pan=0.5)

# ---- section 5: the count alone -------------------------------------------
# the seat was always there. the two absences silent around it.
# (the section-1 drone already rings through to the end.)

# ---- fades ----------------------------------------------------------------
L[: int(0.6 * SR)] *= np.linspace(0.0, 1.0, int(0.6 * SR))
R[: int(0.6 * SR)] *= np.linspace(0.0, 1.0, int(0.6 * SR))
tail = int((DUR - 3.0) * SR)
L[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)
R[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.9
R = R / peak * 0.9
stereo = np.stack([L, R], axis=1)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "bracket.wav")
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

print("\nverification:")
print(f"  seat      mono (1-5s):   {pitch((1.0, 4.5)):.0f} Hz   (the count seated)")
print(f"  sign      diff (6-10s):  {pitch((6.0, 10.0), mono=False):.0f} Hz   (the sub-octave, in the difference)")
print(f"  sign      mono (6-10s):  {pitch((6.0, 10.0)):.0f} Hz   (cancelled by the fold — expect ~110)")
print(f"  ghost     mono (11-14s): {pitch((11.3, 14.2)):.0f} Hz   (the ghost above, kept by mono)")
print(f"  ghost gap mono (15-16s): {pitch((15.0, 16.5)):.0f} Hz   (deleted — the count holds, expect ~110)")
print(f"  bracket   mono (17-21s): {pitch((17.5, 21.0)):.0f} Hz   (sign cancels, ghost+count remain)")
