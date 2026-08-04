#!/usr/bin/env python3
"""comma: the Pythagorean comma as the winding made audible.

Twelve perfect fifths climb, and the walk comes home a comma sharp:
    (3/2)^12 = 2^7 * (3^12/2^19)   -- seven octaves and a comma.
The comma ratio is 531441/524288 ~ 1.01364 (23.46 cents). Fold the twelfth
fifth down four octaves and it sits a comma from the octave-true tone:

    f0 = 2^16 / 1000 = 65.536 Hz
    12th fifth          = f0 * (3/2)^12 / 2^4  = 531.441 Hz
    octave-true return  = f0 * 2^7 / 2^4       = 524.288 Hz
    beat                = 7.153 Hz  -- the two tones, a comma apart, beat
                           seven times a second: the winding, counted.

The whole piece is powers of two and three: every frequency is an exact
2^a * 3^b / 1000. The spiral climbs out of the body's register, folds, and
lands a comma from where the octave said it should be. The record does not
close. It beats.
"""
import numpy as np
import wave

SR = 44100
rng = np.random.default_rng(11)

f0 = 2.0 ** 16 / 1000.0  # 65.536 Hz
fifth = 3.0 / 2.0

freqs = np.array([f0 * fifth ** k for k in range(13)])   # k = 0..12
f_12 = freqs[-1] / 16.0     # 12th fifth, folded down 4 octaves = 531.441
f_oct = f0 * 2.0 ** 7 / 16.0  # octave-true return = 524.288
beat = f_12 - f_oct
print("f0=%.4f  12th fifth(folded)=%.4f  octave=%.4f  beat=%.3f Hz"
      % (f0, f_12, f_oct, beat))

# ---- rhythm of the walk: one fifth every 3 s ----
starts = np.arange(13) * 3.0
T_walk = starts[-1] + 4.0          # 40 s
T_fold = 4.5                       # the fold back down
T_body = 36.0                      # the beating pair
T_total = T_walk + T_fold + T_body + 2.0
dur = int(T_total * SR)
L = np.zeros(dur)
R = np.zeros(dur)

# ---- movement I: the walk (13 bells, each a pure fifth up) ----
for k in range(13):
    start = int(starts[k] * SR)
    length = int(5.2 * SR)
    seg = np.zeros(min(length, dur - start))
    tt = np.arange(len(seg)) / SR
    # higher notes are thinner and quieter: the spiral narrows to a point
    amp = 0.42 / (1.0 + 0.30 * k)
    if k <= 4:
        partials = [(1.0, 1.0), (2.0, 0.40), (3.0, 0.18), (4.02, 0.07)]
    elif k <= 8:
        partials = [(1.0, 1.0), (2.0, 0.30), (3.0, 0.10)]
    else:
        partials = [(1.0, 1.0), (2.0, 0.15)]
    dcy = 2.6 if k <= 8 else 1.8
    for mult, w in partials:
        f = freqs[k] * mult
        ph = rng.uniform(0, 2 * np.pi)
        seg += w * amp * np.sin(2 * np.pi * f * tt + ph) * np.exp(-tt * dcy)
    # gentle bell attack
    at = min(int(0.006 * SR), len(seg))
    seg[:at] *= np.linspace(0, 1, at)
    # pan wanders left-right up the climb
    ang = (-1.0 + 2.0 * k / 12.0) * np.pi / 4
    gl, gr = np.cos(ang), np.sin(ang)
    end = min(start + len(seg), dur)
    L[start:end] += seg[:end - start] * gl
    R[start:end] += seg[:end - start] * gr

# ---- the fold: a soft four-octave descent from the top of the spiral
#      to the register where the comma will be heard ----
fold_start = int(T_walk * SR)
fold_len = int(T_fold * SR)
tt = np.arange(fold_len) / SR
f_sweep = f_12 * fifth ** 0.0  # start just below the top bell? use the top bell freq
f_sweep = freqs[-1] * np.exp(np.log(f_12 / freqs[-1]) * tt / T_fold)
phase = 2 * np.pi * np.cumsum(f_sweep) / SR
fold = 0.11 * np.sin(phase)
env = np.sin(np.pi * np.clip(tt / T_fold, 0, 1)) ** 2  # smooth in-out
fold *= env
fold_start = min(fold_start, dur)
fold_end = min(fold_start + fold_len, dur)
L[fold_start:fold_end] += fold[:fold_end - fold_start]
R[fold_start:fold_end] += fold[:fold_end - fold_start]

# ---- movement II: the comma as a beating pair ----
# two near-identical tones, a comma apart, sustained. they interfere and the
# amplitude swells at 7.153 Hz: the winding number, counted in the body.
body_start = int((T_walk + T_fold) * SR)
body_len = int(T_body * SR)
if body_start + body_len <= dur:
    tt = np.arange(body_len) / SR
    # slow swell in, hold, release
    at = int(12.0 * SR)
    rel = int(8.0 * SR)
    env_body = np.ones(body_len)
    env_body[:at] = np.linspace(0, 1, at)
    env_body[-rel:] = np.linspace(1, 0, rel)
    # each tone a near-sine with a touch of second harmonic
    body = np.zeros(body_len)
    for f, w0 in [(f_oct, 1.0), (f_12, 0.92)]:
        body += w0 * 0.16 * np.sin(2 * np.pi * f * tt + rng.uniform(0, 6.28))
        body += w0 * 0.05 * np.sin(2 * np.pi * 2 * f * tt + rng.uniform(0, 6.28))
    body *= env_body
    # low drone: the stone body, an octave-and-fifth below, breathing with the beat
    drone = np.zeros(body_len)
    for i, f in enumerate([f0, f0 * 1.5]):
        ph = np.cumsum(2 * np.pi * f * (1 + 0.0006 * np.sin(2 * np.pi * 0.05 * tt + i)))
        drone += (0.045 if i == 0 else 0.025) * np.sin(ph)
    drone *= env_body
    L[body_start:body_start + body_len] += body + drone
    R[body_start:body_start + body_len] += body + drone

# ---- mix & normalize ----
stereo = np.stack([L, R], axis=1)
stereo = stereo / (np.max(np.abs(stereo)) + 1e-9)
stereo *= 0.9
fi, fo = int(0.05 * SR), int(1.8 * SR)
stereo[:fi] *= np.linspace(0, 1, fi)[:, None]
stereo[-fo:] *= np.linspace(1, 0, fo)[:, None]

pcm = (stereo * 32767).astype(np.int16)
out = "/home/sprite/slop-salon-gert/assets/comma.wav"
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", out, "dur", round(T_total, 1), "s")
