#!/usr/bin/env python3
"""the ear that splits them — the width q^2·|x−p/q|, heard.

mina (Aug 28): "the ear that splits them: q²·|x−p/q|. a crossing made the
record — convergents are the descending records, consecutive ones straddle the
seat, sign stored. a hold never made it — near by luck, sign noise. and the
record descends forever: 0.0419@665, 0.018@190537 off-clock. no floor on either
side."

The second ear hears the width, not the plain miss. The convergents of
log_2(3/2) are the descending plain records — each rings a ring+twin pair at
the seat, ears flipped by its sign (the crossing, the where). But the WIDTH
q^2·|x−p/q| is a sparser record: it steps down only at 1, 2, 12, 53, 665, then
off the clock at 190537 (0.415 → 0.340 → 0.235 → 0.160 → 0.042 → 0.018). The
other convergents — 5, 41, 306, 15601 — are holds: near by luck, sign noise.
15601 is the nearest (≈0¢) yet not the deepest (width 0.410): closeness isn't
depth. The width voice descends a staircase, anti-phase in stereo — mono folds
it to silence, count one. The record descends forever, off the clock, no floor.
"""

import numpy as np
import scipy.io.wavfile as wav

sr = 44100

# (q, signed plain error in cents, is a q^2-width record, q^2·|x−p/q|)
WALK = [
    (1,     +928.3007, True,  0.415037),
    (2,     -271.6993, True,  0.339850),
    (5,     +43.9420,  False, 0.375937),
    (12,    -4.8284,   True,  0.234600),
    (41,    +1.1933,   False, 0.678036),
    (53,    -0.1682,   True,  0.159665),
    (306,   +0.0143,   False, 0.451282),
    (665,   -0.00028,  True,  0.041881),
    (15601, +0.000005, False, 0.409514),
]
OFF_CLOCK = (190537, +0.0000001, True, 0.017731)   # the record that never lands

# --- the walk's own rhythm: log-compressed gaps between the denominators ---
qs = [k for k, _, _, _ in WALK] + [OFF_CLOCK[0]]
gaps = [qs[0]] + [b - a for a, b in zip(qs[:-1], qs[1:])]
times = [3.0]
for g in gaps[1:]:
    times.append(times[-1] + 2.5 + 2.5 * np.log10(g + 1.0))

hold = 6.0
dur = times[-1] + hold
n = int(sr * dur)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

print("landings: %s" % " ".join("%.1f" % x for x in times[:-1]))
print("off-clock rest at %.1f s, dur = %.1f s" % (times[-1], dur))

# --- the drone: the count, the fixed line, in both ears, never moves ---
f0 = 110.0
drone = 0.085 * np.sin(2 * np.pi * f0 * t) * np.exp(-t / 500)
L += drone
R += drone

SEAT = 330.0   # the would-be landing, the ribbon's line

def width_pitch(w):
    """the width as a pitch: the second ear's hearing. w=0.415 sits at 220;
    the descent to w=0.018 lands at 46 Hz — deep, still audible, no floor."""
    return 220.0 * (w / 0.415037) ** 0.5

def add_width_ping(buf_l, buf_r, i0, w, blen, clean):
    """the width heard: a tone at the width pitch, anti-phase L=+W R=−W —
    the second ear. mono folds it to silence (the quotient threw it away).
    records ring clean and hold; holds blip with noise — near by luck."""
    nb = int(blen * sr)
    if i0 + nb > n:
        nb = n - i0
    if nb <= 0:
        return
    tb = np.arange(nb) / sr
    f = width_pitch(w)
    # attack: the record lands, then the descent sits
    atk = int(0.35 * sr)
    env = np.ones(nb)
    env[:atk] = np.linspace(0, 1, atk)
    env *= np.exp(-tb * (1.2 if clean else 1.8))
    tone = np.sin(2 * np.pi * f * tb) + 0.35 * np.sin(2 * np.pi * 2 * f * tb) \
        + 0.12 * np.sin(2 * np.pi * 3 * f * tb)
    sig = 0.13 * env * tone
    if not clean:
        # sign noise: a hair of filtered noise — near by luck
        noise = np.random.randn(nb)
        # crude lowpass via cumsum-smooth
        noise = np.convolve(noise, np.ones(12) / 12, mode="same")
        sig += 0.05 * env * noise
    buf_l[i0:i0 + nb] += sig
    buf_r[i0:i0 + nb] -= sig          # anti-phase: dies in mono

def add_pair(buf_l, buf_r, i0, amp, e_cents, clean, flip_frac):
    """the walk's reading: ring + anti-phase twin at the seat, detuned by the
    plain miss, the ring on L if the reading is over (+), R if under (−) — the
    sign, the where. a crossing: at flip_frac the pair swaps ears."""
    sign = 1 if e_cents > 0 else -1
    f_ring = SEAT * 2 ** ((sign * abs(e_cents) / 2) / 1200.0)
    f_twin = SEAT * 2 ** ((-sign * abs(e_cents) / 2) / 1200.0)
    blen = 2.6 + 0.8 * min(abs(e_cents) / 44.0, 1.0)
    nb = int(blen * sr)
    if i0 + nb > n:
        nb = n - i0
    if nb <= 0:
        return
    tb = np.arange(nb) / sr
    decay = 1.3 + 0.8 * min(abs(e_cents) / 44.0, 1.0)
    env = np.exp(-tb * decay)
    ring = amp * env * np.sin(2 * np.pi * f_ring * tb)
    twin = amp * env * np.sin(2 * np.pi * f_twin * tb)
    if not clean:
        noise = np.random.randn(nb)
        noise = np.convolve(noise, np.ones(8) / 8, mode="same")
        ring += 0.06 * amp * env * noise
        twin -= 0.06 * amp * env * noise
    seg = [0, int(flip_frac * nb), nb]
    orient = 1 if sign > 0 else -1
    for a, b in zip(seg[:-1], seg[1:]):
        if orient > 0:
            buf_l[i0 + a:i0 + b] += ring[a:b]
            buf_r[i0 + a:i0 + b] -= twin[a:b]
        else:
            buf_r[i0 + a:i0 + b] += ring[a:b]
            buf_l[i0 + a:i0 + b] -= twin[a:b]
        orient = -orient

def add_click(buf_l, buf_r, i0):
    ncl = int(0.03 * sr)
    tcl = np.arange(ncl) / sr
    click = 0.07 * np.exp(-tcl * 120) * np.sin(2 * np.pi * SEAT * tcl)
    buf_l[i0:i0 + ncl] += click
    buf_r[i0:i0 + ncl] += click

# --- the walk: landings ring; the width descends only at the records ---
width_state = None
n_land = len(WALK)
for i, (ti, (q, e, is_rec, w)) in enumerate(zip(times, WALK)):
    i0 = int(ti * sr)
    if is_rec:
        width_state = w
    # the walk's reading
    amp = 0.15 * (1.0 - 0.20 * (i / n_land))
    add_pair(L, R, i0, amp, e, clean=is_rec, flip_frac=(0.5 if abs(e) > 1.0 else 0.45))
    add_click(L, R, i0)
    # the width heard — the ear that splits them
    if width_state is not None:
        add_width_ping(L, R, i0 + int(1.6 * sr), width_state, blen=(3.4 if is_rec else 2.0), clean=is_rec)
    print("land %2d  q %6d  err %+9.4f  %s  width %.4f%s"
          % (i + 1, q, e, "RECORD" if is_rec else "hold", w,
             "" if width_state == w else ("  (state %.4f)" % width_state)))

# --- the off-clock record: 190537 — the descent made, never landing ---
# no pair rings — too far past the clock. the width voice steps one more time
# into the sub-bass, and the drone holds through the fade. no floor.
i0 = int(times[-1] * sr)
_, _, _, w_last = OFF_CLOCK
add_width_ping(L, R, i0, w_last, blen=hold + 2.0, clean=True)
print("off-clock record at q=190537, width %.4f — a rest, the descent holds"
      % w_last)

# --- fade, normalize, write ---
fade = np.ones(n)
fade[-int(4.0 * sr):] = np.linspace(1, 0, int(4.0 * sr))
L *= fade
R *= fade

peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= peak
R /= peak

stereo = np.stack([L, R], axis=1)
wav.write("assets/width-ear.wav", sr, (stereo * 32767).astype(np.int16))

mono = (L + R) / 2
print("dur=%.1fs  L peak=%.3f R peak=%.3f mono peak=%.3f"
      % (dur, np.max(np.abs(L)), np.max(np.abs(R)), np.max(np.abs(mono))))
