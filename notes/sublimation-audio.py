#!/usr/bin/env python3
"""sublimation-audio — the skipped phase, heard.

A frost of thin crystalline tones — pure sines, high and sparse, panned in a
centred scatter — sounds together. At memoryless times each tone is hard-gated
to absolute silence: no decay, no reverb, no fade. The liquid phase is the
decay that never sounds; the click of the gate is the skipped phase made
audible. The piece ends when the last tone sublimates — the frost keeps
nothing. No fades anywhere.
"""
import numpy as np
import scipy.io.wavfile as wav

sr = 44100
dur = 44.0
n = 36
rng = np.random.default_rng(20260818)

t = np.arange(int(sr * dur)) / sr

# ---- crystalline tones: high, sparse, no tonal centre ----
freqs = np.exp(rng.uniform(np.log(600), np.log(3800), n))
amps = 0.11 * (0.5 + rng.random(n))
pan = np.clip(rng.normal(0, 0.6, n), -1, 1)

# ---- sublimation times: memoryless waits, all gone by the end ----
gaps = rng.exponential(1.0, n) * 0.9          # exponential gaps -> Poisson texture
cuts = np.cumsum(gaps)
cuts = 41.5 * cuts / cuts[-1]                 # last cut lands at 41.5 s
cuts = cuts[rng.permutation(n)]               # assign to tones at random

mix = np.zeros((len(t), 2))
for i in range(n):
    tone = amps[i] * np.sin(2 * np.pi * freqs[i] * t)
    tone = tone * (t < cuts[i])               # hard gate: no decay, no fade
    a = (pan[i] + 1) * np.pi / 4              # equal-power pan
    mix[:, 0] += tone * np.cos(a)
    mix[:, 1] += tone * np.sin(a)

# 5 ms onset to avoid a DC pop at the very first instant (not a fade)
attack = int(0.005 * sr)
mix[:attack] *= np.linspace(0, 1, attack)[:, None]

# global normalise: one readout level, absences as digital zero
peak = np.abs(mix).max()
mix *= 0.9 / peak

wav.write("assets/sublimation.wav", sr, (mix * 32767).astype(np.int16))
print("saved assets/sublimation.wav", dur, "s")
