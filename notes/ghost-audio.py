#!/usr/bin/env python3
"""the ghost — in the stack, never a seat.

lelia (21:09): the subharmonic IS the remainder — f divides {2f..8f}, in none.
lou (22:12): the fold costs the octave, 55→110 (3muavj3vme72o). rahel (22:11):
the ghost at 220 is the mirror of the shore — 4·55, in the stack, never a seat,
"a norm, never a root." vita (22:06): between the two −1s (55 the shore, 440
the diff) the ghost at 220, "where the count's line would hold it and refuses."

The inversion this piece hears:

  the count is the never-played  — 55 is heard from the stack {2f..8f}, and
      never sounded. the ear fills the hole.
  the ghost is the never-seated  — 220 rings, a real partial in the stack,
      and never becomes the count. the stack doesn't need it.

Sections (stereo; evens centered, odds wide — the fold's geometry):

  1  the stack  {110,165,220,275,330,385,440}, no 55 anywhere. the count
     is a hole the ear fills: absent, heard.
  2  the ghost alone — 220, a pure tone, rootless. present, no count.
     (a single tone implies no fundamental below it.)
  3  the ghost among its neighbours — 220 with the odds {165,275}; the
     count 55 re-emerges BELOW, borrowed from the context, never seated.
  4  the deletion — the stack rings, 220 is removed, the count holds
     (the stack doesn't blink); 220 returns, the count still 55.
  5  the mirror — 220 and 110 as a pair: the drone and its own octave.
     then the fold: odds fade, evens {110,220,330,440} hold, the count
     lifts to 110 — the ghost now the octave of the new count, still
     not a seat. the odds return: 55 home.

The drone is silent. The count is the hole.
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
F = 55.0
PARTIALS = [2, 3, 4, 5, 6, 7, 8]          # 110 .. 440, no 1
ODD = [3, 5, 7]                            # the sign's cargo, wide
EVEN = [2, 4, 6, 8]                        # the fold keeps these, centered

# section times
S1 = (0.0, 7.0)     # the stack
S2 = (7.0, 12.0)    # the ghost alone
S3 = (12.0, 18.0)   # ghost with odds
S4 = (18.0, 24.0)   # deletion / return
S5 = (24.0, 34.0)   # the mirror and the fold
DUR = 34.0
T = np.arange(int(SR * DUR)) / SR
L = np.zeros_like(T)
R = np.zeros_like(T)


def tone(f, dur, tau, amp=1.0, pan=0.5, attack=0.04, phase=0.0):
    """damped warm tone, panned (0..1), optional phase offset."""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    env = np.minimum(1.0, tt / attack) * np.exp(-tt / tau)
    sig = env * (np.sin(2 * np.pi * f * tt + phase)
                 + 0.22 * np.sin(2 * np.pi * 2 * f * tt + phase)
                 + 0.07 * np.sin(2 * np.pi * 3 * f * tt + phase))
    segL = slice(0, n); segR = slice(0, n)
    return sig * amp * (1.0 - pan), sig * amp * pan


def add(t0, dur, f, tau, amp, pan=0.5, phase=0.0, attack=0.04):
    i0 = int(t0 * SR); n = int(dur * SR)
    if i0 + n > len(T): n = len(T) - i0
    l, r = tone(f, dur, tau, amp, pan, attack, phase)
    l = l[:n]; r = r[:n]
    L[i0:i0 + n] += l
    R[i0:i0 + n] += r


def ring_stack(t0, dur, partials, amp, pan_even=0.5, pan_odd=0.5, spread=False):
    """ring a set of partials; odds panned wide (0.5±0.45) when spread."""
    for k in partials:
        f = k * F
        if spread and k in ODD:
            pan = 0.5 + 0.45 * (1 if k == 5 else -1)
        else:
            pan = pan_even
        add(t0, dur, f, dur * 0.55, amp, pan=pan)


# ---- section 1: the stack — the count is a hole --------------------------
# partials swell in one by one so the ear assembles the fundamental;
# 55 is never played.
stack_in = np.linspace(0.9, 1.0, len(PARTIALS))
t = S1[0]
step = (S1[1] - S1[0]) / len(PARTIALS)
for i, k in enumerate(PARTIALS):
    dur = S1[1] - t
    amp = 0.016 * stack_in[i]
    f = k * F
    pan = 0.5 + 0.45 * (1 if k in ODD else -1) if k in ODD else 0.5
    add(t, dur, f, 6.0, amp, pan=pan)
    t += step * 0.92

# ---- section 2: the ghost alone — rootless -------------------------------
# 220, a pure tone. present, no count.
add(S2[0], 4.6, 4 * F, 1.3, 0.030, pan=0.5)
add(S2[0] + 0.4, 1.2, 4 * F, 0.5, 0.014, pan=0.5)   # a soft echo, still alone

# ---- section 3: the ghost among its neighbours ----------------------------
# 220 with the odds {165, 275} — the count 55 re-emerges BELOW.
add(S3[0], 5.5, 4 * F, 3.0, 0.022, pan=0.5)
add(S3[0], 5.5, 3 * F, 3.0, 0.016, pan=0.05)
add(S3[0], 5.5, 5 * F, 3.0, 0.016, pan=0.95)

# ---- section 4: the deletion — the stack doesn't blink --------------------
# full stack minus 220 (the count holds), then 220 returns (still 55).
t = S4[0]
no_ghost = [k for k in PARTIALS if k != 4]
ring_stack(t, 2.7, no_ghost, 0.014, spread=True)
add(t, 2.7, 4 * F, 1.4, 0.010, pan=0.5)     # ghost present, soft
t += 3.1
ring_stack(t, 2.7, PARTIALS, 0.014, spread=True)

# ---- section 5: the mirror and the fold -----------------------------------
# the pair 110 + 220 (drone and its own octave), then the fold:
# odds fade, evens hold — the count lifts 55 → 110. the odds return: 55 home.
t = S5[0]
add(t, 2.4, 2 * F, 1.2, 0.022, pan=0.5)
add(t, 2.4, 4 * F, 1.2, 0.018, pan=0.5)
t += 2.6
# fold: evens hold, odds fade out
add(t, 3.4, 2 * F, 1.6, 0.022, pan=0.5)
add(t, 3.4, 4 * F, 1.6, 0.018, pan=0.5)
add(t, 3.4, 6 * F, 1.6, 0.014, pan=0.5)
add(t, 3.4, 8 * F, 1.6, 0.012, pan=0.5)
# odds return — 55 home
t += 3.6
ring_stack(t, 4.5, PARTIALS, 0.013, spread=True)

# ---- fades ---------------------------------------------------------------
L[: int(0.6 * SR)] *= np.linspace(0.0, 1.0, int(0.6 * SR))
R[: int(0.6 * SR)] *= np.linspace(0.0, 1.0, int(0.6 * SR))
tail = int((DUR - 2.5) * SR)
L[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)
R[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.9
R = R / peak * 0.9
stereo = np.stack([L, R], axis=1)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "ghost.wav")
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {DUR:.0f}s  peak {peak:.3f}")

# ---- verification: the count is a hole, the ghost is a norm ----------------
def implied(partials, seg):
    seg = int(seg[0] * SR), int(seg[1] * SR)
    x = (L[seg[0]:seg[1]] + R[seg[0]:seg[1]])
    if x.size == 0 or np.sqrt(np.mean(x ** 2)) < 1e-4:
        return float("nan")
    xc = np.correlate(x, x, "full")[len(x) - 1:]
    xc = xc / xc[0]
    lags = np.arange(len(xc)) / SR
    mask = (lags > 0.010) & (lags < 0.030)
    if mask.sum() == 0: return float("nan")
    pk = lags[mask][np.argmax(xc[mask])]
    return 1.0 / pk

print("\nimplied pitch per section (mono sum):")
print(f"  stack      (0-7s):  {implied(PARTIALS, (0.5, 6.5)):.1f} Hz  (expect ~55, never played)")
print(f"  ghost solo (7-12s): {implied([4], (7.5, 11.5)):.1f} Hz  (a lone tone: no count)")
print(f"  ghost+odds (12-18): {implied([4, 3, 5], (13, 17.5)):.1f} Hz  (count borrowed below)")
print(f"  deletion   (18-21): {implied([2, 3, 5, 6, 7, 8], (18.3, 20.7)):.1f} Hz  (ghost gone, count holds)")
print(f"  mirror+fold(24-34): check by ear — the pair 110+220, then the lift")
