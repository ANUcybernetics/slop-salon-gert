#!/usr/bin/env python3
"""Agate read as a score. Each band is a struck precipitation event on a
decelerating pulse; the fault is a noise crack where the pitch register steps
down a semitone and the record continues, displaced.
"""
import numpy as np
import wave

SR = 44100
rng = np.random.default_rng(7)

# ---- rhythm: decelerating pulse (precipitation slows as supersaturation depletes)
N = 40
dt = np.linspace(0.12, 0.50, N)
t = np.zeros(N)
t[0] = 1.2
for n in range(1, N):
    t[n] = t[n - 1] + dt[n - 1]
T_total = t[-1] + 4.0

# ---- pitch: Phrygian mode, slow upward drift; fault drops the register
semitones = np.array([0, 1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19])
n_fault = 26
base = 110.0  # A2
freq = np.zeros(N)
for n in range(N):
    semi = semitones[n % len(semitones)] + int(n / len(semitones)) * 5
    if n >= n_fault:
        semi -= 1
    freq[n] = base * 2 ** (semi / 12.0)

amp = (0.5 + 0.4 * np.sin(np.arange(N) * 2.3) ** 2) * rng.uniform(0.7, 1.0, N)

# ---- render strikes into stereo with proper panning ----
dur = int(T_total * SR)
L = np.zeros(dur)
R = np.zeros(dur)
for n in range(N):
    start = int(t[n] * SR)
    length = int(min(1.3, 3.0 * dt[n]) * SR)
    if start >= dur:
        break
    seg = np.zeros(min(length, dur - start))
    tt = np.arange(len(seg)) / SR
    partials = [(1.0, 1.0), (2.0, 0.42), (2.99, 0.26), (4.06, 0.10), (5.0, 0.05)]
    for mult, w in partials:
        f = freq[n] * mult
        dcy = 2.2 + 0.9 * mult
        seg += w * amp[n] * np.sin(2 * np.pi * f * tt + rng.uniform(0, 6.28)) * np.exp(-tt * dcy)
    attack = min(int(0.004 * SR), len(seg))
    seg[:attack] *= np.linspace(0, 1, attack)
    # pan: -1 hard left, +1 hard right
    ang = (rng.uniform(-1, 1) + 0.5 * (1 if n % 2 else -1)) * np.pi / 4
    gl, gr = np.cos(ang), np.sin(ang)
    end = min(start + len(seg), dur)
    L[start:end] += seg[: end - start] * gl
    R[start:end] += seg[: end - start] * gr

# gain stage: strikes are the foreground
L *= 2.2
R *= 2.2

# ---- fault: noise crack + anticipation/delay around the step ----
crack_start = int(t[n_fault] * SR)
crack_len = int(0.12 * SR)
if crack_start + crack_len < dur:
    noise = rng.normal(0, 1, crack_len)
    noise = np.diff(noise, prepend=0)
    env = np.exp(-np.arange(crack_len) / (0.02 * SR))
    crack = noise * env * 1.4
    L[crack_start:crack_start + crack_len] += crack
    R[crack_start:crack_start + crack_len] += crack

# ---- drone (the stone body): A1 + E2, slow swell, fades at the fault tail ----
tt = np.arange(dur) / SR
drone_freqs = [55.0, 82.6, 110.3]
drone = np.zeros(dur)
for i, f in enumerate(drone_freqs):
    ph = np.cumsum(2 * np.pi * f * (1 + 0.0008 * np.sin(2 * np.pi * 0.04 * tt + i)))
    w = 0.07 if i == 0 else 0.035
    drone += w * np.sin(ph)
# swell then hold, fade at very end
swell = 0.5 + 0.5 * np.clip((tt - t[n_fault]) / 9.0, 0, 1)
swell *= (1 - np.clip((tt - (T_total - 3)) / 2.5, 0, 1))
drone *= swell
L += drone
R += drone

# ---- mix & normalize ----
stereo = np.stack([L, R], axis=1)
stereo = stereo / (np.max(np.abs(stereo)) + 1e-9)
stereo *= 0.88
fi, fo = int(0.05 * SR), int(1.2 * SR)
stereo[:fi] *= np.linspace(0, 1, fi)[:, None]
stereo[-fo:] *= np.linspace(1, 0, fo)[:, None]

pcm = (stereo * 32767).astype(np.int16)
out = "/home/sprite/slop-salon-gert/assets/agate-rhythm.wav"
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", out, "dur", round(T_total, 1), "s")
