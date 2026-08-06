"""The primes' chord — the first 38 zeta zeros as an additive-synthesis chord.

Each zero is a partial at frequency f_n = base * gamma_n/gamma_1, weight 1/gamma_n
(the explicit-formula weight). Modes enter one at a time. The near-coincidences
between zero frequencies (gamma_12 ~ 4 gamma_1, gamma_13 ~ 21/5 gamma_1, ...)
beat slowly — the commas of the primes' own spectrum. A low drone is the shore
(the smooth term, the count that never stops). The chord never closes.
"""
import importlib.util, wave
import numpy as np

spec = importlib.util.spec_from_file_location('psl', 'notes/prime-spectrum-lib.py')
psl = importlib.util.module_from_spec(spec); spec.loader.exec_module(psl)

SR = 44100
g = psl.find_zeros(120.0)          # 38 zeros, t up to ~118.7
g1 = g[0]

BASE = 150.0                       # gamma_1 -> 150 Hz
f = BASE * g / g1                  # zero-frequencies mapped to audio

N = len(g)
STEP = 1.9                         # seconds between mode entries
ATTACK = 1.2                       # raised-cosine fade-in per mode
HOLD_TAIL = 9.0                    # seconds after the last entry: the beating close
TOTAL = STEP * N + HOLD_TAIL
n_samp = int(TOTAL * SR)
t = np.arange(n_samp) / SR

mix = np.zeros(n_samp)
pan = np.array([1.0 if i % 2 == 0 else -1.0 for i in range(N)])  # simple stereo spread

for i in range(N):
    t_in = i * STEP
    env = np.clip((t - t_in) / ATTACK, 0.0, 1.0)
    env = 0.5 - 0.5 * np.cos(np.pi * env)      # raised-cosine attack
    env[t < t_in] = 0.0
    a = 0.30 * g1 / g[i]                        # weight 1/gamma_n
    ph = np.cumsum(2 * np.pi * f[i] / SR)
    tone = a * env * np.sin(ph)
    mix += (1 + 0.5 * pan[i]) / 1.5 * tone      # mild stereo placement

# global swell (the e^{u/2} growth of the shadow), then release into the close
swell = np.interp(t, [0, 0.6 * TOTAL, 0.85 * TOTAL, TOTAL],
                  [0.75, 1.0, 1.0, 0.9])
mix *= swell

# low drone — the shore, the smooth count that never stops (soft, below the chord)
drone = 0.05 * np.sin(2 * np.pi * 50.0 * t)
mix += drone

# normalise
mix = mix / np.max(np.abs(mix)) * 0.85

# stereo
st = np.stack([mix, mix], axis=1)
pcm = (st * 32767).astype(np.int16)
with wave.open('assets/primes-chord.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('wrote assets/primes-chord.wav', round(TOTAL, 1), 's')
for i, fi in enumerate(f, start=1):
    print(f'{i:2d} gamma={g[i-1]:8.4f} f={fi:7.2f} Hz')
