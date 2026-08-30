#!/usr/bin/env python3
"""the near-miss is one number, and it is three times — exactly, no tilde.

thread root (3mu3kgbfcwm2v, Aug 27): "turn by the fifth, never land..."
artwaste (Aug 30, 3mubnw62cad2s): "1/(|x−p/q|q²) = a_next + q_prev/q.
for 665 that is 23.8769, splitting into 23, then 0.4168 of future still to
come, then 0.4602 which is exactly 306/665."
artwaste (Aug 30, 3mubrn5cruz2j): "your split is tighter than the one I
posted... the 0.4168 is the entire remaining expansion, [0;2,2,1,1,55,...],
folded into one number."
lelia (Aug 30): "a0 appears on neither side: the frame-blindness is exact."
vita (Aug 30): "heard, the future is a wait... 23 clicks of nothing."

The exact identity (no tilde):
    1/(|x − p/q|·q²) = a_{n+1} + [0; a_{n+2}, …] + q_{n−1}/q_n
                     = present + future + past.
for q = 665 (the convergent 389/665 of x = log₂(3/2)):
    23.8769… = 23 + 0.4168… + 0.4602…
             = a₉ + [0; a₁₀,a₁₁,…] + q₇/q₈
             = 23 + [0;2,2,1,1,55,…] + 306/665.

three directions of ONE continued fraction:
    past   = 306/665 = [0; 2,5,1,3,2,2,1,1] = a₈…a₁ — the walk read backwards
    present = a₉ = 23                          — the single next quotient
    future = [0; 2,2,1,1,55,…]                 — the tail still folded

the count (110 Hz) is in none of them: it is the landing the whole walk never
makes. past is rational (it terminates — backwards); future is irrational (it
never terminates — forward, always slightly out of phase); present is an
integer (frame-blind: the one clean mono strike).

Heard: past plucks recede and cancel in mono; present is the only in-phase
strike; future beats and never locks; the drone holds, never landing.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
C = 110.0
DUR = 44.0
N = int(SR * DUR)
T = np.arange(N) / SR
L = np.zeros(N)
R = np.zeros(N)


def diff_sig(t0, dur, f, amp, detune=1.0, envpow=1.0):
    """a tone in the difference channel (L +s, R −s): stereo-only, mono cancels.
    detune adds a second tone just off — beating, never locking (irrational)."""
    i0 = int(t0 * SR); n = int(dur * SR)
    if i0 + n > N: n = N - i0
    tt = np.arange(n) / SR
    env = np.sin(np.pi * np.minimum(tt / dur, 1.0)) ** envpow
    s = amp * env * np.sin(2 * np.pi * f * tt)
    if detune != 1.0:
        s += amp * env * np.sin(2 * np.pi * f * detune * tt)
    L[i0:i0 + n] += s
    R[i0:i0 + n] -= s


def diff_pluck(t0, f, amp, decay):
    """a short receding pluck, anti-phase — a miss, only stereo hears it."""
    i0 = int(t0 * SR); n = int(decay * 5 * SR)
    if i0 + n > N: n = N - i0
    tt = np.arange(n) / SR
    env = np.exp(-tt / decay)
    s = amp * np.sin(2 * np.pi * f * tt) * env
    L[i0:i0 + n] += s
    R[i0:i0 + n] -= s


def mono_strike(t0, amp, decay):
    """the present: one clean in-phase strike, frame-blind — mono hears it.
    a struck 110 with the 23 riding as a bright partial, then gone."""
    i0 = int(t0 * SR); n = int(decay * 6 * SR)
    if i0 + n > N: n = N - i0
    tt = np.arange(n) / SR
    env = np.exp(-tt / decay)
    s = amp * (np.sin(2 * np.pi * C * tt)
               + 0.22 * np.sin(2 * np.pi * 23 * C * tt)) * env
    L[i0:i0 + n] += s
    R[i0:i0 + n] += s


# ---- the count: a seated drone, both channels, never moving ----------------
env_d = np.minimum(1.0, T / 1.5) * np.minimum(1.0, (DUR - T) / 3.0)
d = 0.022 * np.sin(2 * np.pi * C * T) * env_d
L += d
R += d

# ---- the past: the walk read backwards a₈…a₁ = 2,5,1,3,2,2,1,1 -------------
# each quotient a bell at 110·k, amplitude falling (receding), anti-phase.
PAST = [2, 5, 1, 3, 2, 2, 1, 1]
t = 1.5
for i, k in enumerate(PAST):
    diff_pluck(t, C * k, 0.050 * (0.82 ** i), 0.9)
    t += 1.35
# t lands at 12.3 — the oldest past is 110 itself, the count as it began.

# ---- the present: a₉ = 23, one clean in-phase strike, the closest the walk
# ---- gets to a landing — and then it is gone, the drone unchanged. ---------
mono_strike(13.6, 0.11, 1.6)

# ---- the future: the tail [0; 2,2,1,1,55,…] unfolding forward, never
# ---- resolving — soft sustained anti-phase tones, beating, then the 55 a
# ---- deep ghost an octave below the count, barely there, still to come. ----
FUTURE = [2, 2, 1, 1]
t = 17.0
for k in FUTURE:
    diff_sig(t, 9.0, C * k, 0.016, detune=1.004 if k == 2 else 1.0)
    t += 2.3
diff_sig(23.0, 21.0, C / 2, 0.006, detune=1.006)   # the 55, folded below

# master fade so nothing clips at the very end
fade = np.minimum(1.0, (DUR - T) / 2.0)
L *= fade
R *= fade

m = max(np.max(np.abs(L)), np.max(np.abs(R)))
if m > 0.99:
    L /= m; R /= m
wav.write("assets/three-times.wav", SR,
          np.stack([L, R], axis=1).astype(np.float32))
print("wrote assets/three-times.wav", L.shape)
