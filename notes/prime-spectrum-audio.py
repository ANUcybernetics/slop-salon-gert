#!/usr/bin/env python3
"""Soundtrack for 'the primes are a spectrum'.

Additive synthesis: one sine partial per zeta zero, frequency
f_n = 55 * (t_n / t_1) Hz, amplitude ~ 1/sqrt(t_n). Each partial swells in
at the moment its mode is added to the animation (40 s, 100 modes). A global
swell carries the e^{u/2} growth of the explicit formula, so the chord blooms
from a single low tone into a dense inharmonic shimmer.
"""
import sys
sys.path.insert(0, '/tmp')
import numpy as np
import wave
from prime_spectrum_lib import find_zeros

SR = 44100
T = 40.0
N = int(T * SR)
t_axis = np.arange(N) / SR
NMAX = 100
zeros = find_zeros(300.0)[:NMAX]
t1 = zeros[0]

# global swell: e^{u(t)/2} / e^{u0/2}, u from log2 to log50
u0, u1 = np.log(2.0), np.log(50.0)
u_t = u0 + (u1 - u0) * (t_axis / T)
swell = np.exp(0.5 * (u_t - u0))

mix = np.zeros(N)
f0 = 55.0
rng = np.random.default_rng(7)

for n, tn in enumerate(zeros):
    add_t = T * n / (NMAX - 1)          # moment this mode is added
    freq = f0 * tn / t1
    # amplitude: 1/sqrt(t_n), scaled so partial 1 is ~0.5 and sum is safe
    amp = 0.5 * np.sqrt(t1 / tn)
    # envelope: attack 1.5 s after addition, then hold
    env = np.zeros(N)
    start = int(add_t * SR)
    attack = int(1.5 * SR)
    if start + attack >= N:
        env[start:] = 1.0
    else:
        env[start:start+attack] = np.linspace(0, 1, attack)
        env[start+attack:] = 1.0
    phase = rng.uniform(0, 2*np.pi)
    tone = np.sin(2*np.pi*freq*t_axis + phase)
    # a touch of second harmonic for warmth on the lower partials
    if n < 20:
        tone += 0.08 * np.sin(2*np.pi*2*freq*t_axis + phase)
    mix += amp * env * tone

mix *= swell
# soft master fade in / out
mix *= np.minimum(1.0, t_axis / 2.0) * np.minimum(1.0, (T - t_axis) / 2.0)
# normalize
mix = mix / np.max(np.abs(mix)) * 0.85

pcm = (mix * 32767).astype(np.int16)
with wave.open('/tmp/prime_spectrum.wav', 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('wrote /tmp/prime_spectrum.wav', len(pcm)/SR, 's')
