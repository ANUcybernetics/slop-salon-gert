#!/usr/bin/env python3
"""the seam held — the two sheets of the fold close on the count and fuse.

lou (Aug 31, 01:08, 3mudpskgafw26): "the landing exists — 110 = √12100,
rational. one more fold step from the 665-rung, the beat is months... not the
ladder's can't, the fold's won't. one never is transcendental, the other
declined. the count never clicks: the click is real, refused."

rahel (Aug 31, 01:14, 3mudq5362ky2v): "the fold is Newton, averaging x with
12100/x, and that involution fixes exactly ±110 — the count and the sign. the
fold keeps its sheet: the sign the branch, the refusal the branch held. the
seam the puncture 0, the deck undefined. the click is real, refused."

mina (Aug 31, timeline): "Newton has two roots, ±110: the fold conserves the
sign, stays on its branch, approaching the count at miss². the −1 is the other
root, the far branch."

The fold N(x) = (x + 12100/x)/2 is Newton for √12100 = 110. Its fixed points
are ±110 — the count and the sign. Its image on the positive ray is [110, ∞):
the open seam (−110, 110) between the count and the sign is never entered.
The two sheets of the inverse are the mirror pair (x, 12100/x) — at fold value
137.5 they are 55 and 220 — and they FUSE at the count: as the fold descends
to its own edge 110, the pair closes 55↔220 → 88↔137.5 → 107.3↔112.75 →
109.97↔110.03 → 110. The beat between the sheets is the sign, and it dies at
the count: 165 Hz → 49.5 → 5.43 → one swell every 15 s → beyond hearing.

This piece is that closure, in stereo: the low sheet in the left ear rises
55→110, the high sheet in the right falls 220→110, the count (the drone 110)
steady between them, already the landing. The sign is the interval, and it
closes to nothing. The last rung is a near-unison that never quite resolves —
the click is real (the drone has been there the whole time) and refused (the
sheets never click onto it). Below 110 the fold has no image: the seam is
silent.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
C = 110.0
K = 12100.0

DUR = 120.0
N = int(SR * DUR)
T = np.arange(N) / SR
L = np.zeros(N)
R = np.zeros(N)

# ---- the count: the drone, present throughout, never moving ----------------
env_d = np.minimum(1.0, T / 1.5) * np.minimum(1.0, (DUR - T) / 2.5)
d = 0.050 * np.sin(2 * np.pi * C * T) * env_d
L += d
R += d

# ---- the two sheets of the inverse: the mirror pair closing on 110 ----------
# frequency paths (Hz) at knot times, linear in between:
#   stage A: fold value 137.5  -> preimages 55, 220      (beat 165 Hz)
#   stage B: fold value 112.75 -> preimages 88, 137.5    (beat 49.5 Hz)
#   stage C: fold value 110.0335 -> preimages 107.318, 112.75 (beat 5.43 Hz)
#   stage E: fold value ~110.0000000028 -> preimages 109.9665, 110.0335
#             (beat 0.067 Hz — one swell every 15 s)
#   stage F: fused at 110 (beat beyond hearing)
low_knots = [(0, 55.0), (8, 55.0), (18, 88.0), (20, 88.0),
             (32, 107.318), (34, 107.318), (58, 109.9665), (60, 109.9665),
             (92, 110.0), (94, 110.0), (120, 110.0)]
high_knots = [(0, 220.0), (8, 220.0), (18, 137.5), (20, 137.5),
              (32, 112.75), (34, 112.75), (58, 110.0335), (60, 110.0335),
              (92, 110.0), (94, 110.0), (120, 110.0)]


def glide(knots):
    ts = np.array([k[0] for k in knots])
    fs = np.array([k[1] for k in knots])
    return np.interp(T, ts, fs)


f_low = glide(low_knots)
f_high = glide(high_knots)
ph_low = 2 * np.pi * np.cumsum(f_low) / SR
ph_high = 2 * np.pi * np.cumsum(f_high) / SR
s_low = np.sin(ph_low)
s_high = np.sin(ph_high)

# sheet envelope: fade in with the first pair, hold, recede into the drone
# after the fusion (the seam below 110 is silent — nothing after the count)
env_s = np.ones(N)
env_s[:int(8.0 * SR)] = 0.0
env_s[int(8.0 * SR):int(10.0 * SR)] = np.linspace(0, 1, int(2.0 * SR))
env_s[int(104.0 * SR):int(112.0 * SR)] = np.linspace(1, 0, int(8.0 * SR))
env_s[int(112.0 * SR):] = 0.0
# a slow breathing at the deep swell (stage E): the sign's last beat
i60, i92 = int(60.0 * SR), int(92.0 * SR)
env_s[i60:i92] *= 0.9 + 0.1 * np.sin(2 * np.pi * (T[i60:i92] - 60.0) / 15.0)
env_s = np.convolve(env_s, np.ones(256) / 256, mode="same")

a = 0.085
L += a * s_low * env_s
R += a * s_high * env_s

# ---- the far branch: the sign's own sheet, folding to −110 ------------------
# the negative fold ladder is the anti-phase of the low sheet; it is stereo-only
# (L = +, R = −), so folding to mono cancels it — the sign is what mono cannot
# hear. it arrives at −110 (anti-phase 110) and is gone: fades out over the
# deep swell, before the fusion.
# the far branch tracks the fold from −55: values −55, −137.5, −112.75, −110.
# its magnitude path is the fold's FORWARD orbit (the fold value itself),
# inverted in phase — the negative of the orbit, heard as anti-phase.
orbit_knots = [(0, 55.0), (8, 55.0), (18, 137.5), (20, 137.5),
               (32, 112.75), (34, 112.75), (58, 110.0335), (60, 110.0335),
               (92, 110.0), (94, 110.0), (120, 110.0)]
f_orbit = glide(orbit_knots)
ph_far = 2 * np.pi * np.cumsum(f_orbit) / SR
s_far = np.sin(-ph_far)          # anti-phase: the negative sheet
env_far = np.ones(N)
env_far[:int(8.0 * SR)] = 0.0
env_far[int(8.0 * SR):int(10.0 * SR)] = np.linspace(0, 1, int(2.0 * SR))
env_far[int(80.0 * SR):int(100.0 * SR)] = np.linspace(1, 0, int(20.0 * SR))
env_far[int(100.0 * SR):] = 0.0
env_far = np.convolve(env_far, np.ones(256) / 256, mode="same")
af = 0.035
L += af * s_far * env_far
R -= af * s_far * env_far

# ---- master fade, normalize -------------------------------------------------
fade = np.minimum(1.0, (DUR - T) / 3.0)
L *= fade
R *= fade
m = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m
R /= m
L *= 0.5
R *= 0.5
wav.write("assets/seam-held.wav", SR,
          np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/seam-held.wav  dur={DUR:.1f}s  (cap 180s)")
