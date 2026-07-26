import numpy as np

sr = 44100
dur = 8.0
t = np.linspace(0, dur, int(sr * dur))

# Steady carrier — the clutching number as sustained resonance
carrier_freq = 220.0
carrier = np.sin(2 * np.pi * carrier_freq * t)
carrier_env = np.exp(-0.02 * t)

# FM component — the phase jump migrating around S¹
n_jumps = 4
base_freq = 440.0
phase = 2 * np.pi * n_jumps * t / dur
phase_wrapped = np.mod(phase, 2 * np.pi)
mod_depth = 15.0
fm_phase = 2 * np.pi * base_freq * t + mod_depth * phase_wrapped
fm = np.sin(fm_phase)

rev_envelope = np.ones_like(t)
for i in range(n_jumps):
    rev_start = i * dur / n_jumps
    rev_mask = t > rev_start
    rev_envelope[rev_mask] *= np.exp(-0.1 * (t[rev_mask] - rev_start))

fm *= rev_envelope

mixed = 0.5 * carrier * carrier_env + 0.5 * fm
mixed /= np.max(np.abs(mixed)) * 0.9

# Stereo spread — left/right differ slightly to echo the two patches
left = mixed * (1 + 0.1 * np.sin(2 * np.pi * 1.5 * t / dur))
right = mixed * (1 - 0.1 * np.sin(2 * np.pi * 1.5 * t / dur))
stereo = np.column_stack((left, right)).astype(np.float32)

from scipy.io import wavfile
wavfile.write('/home/sprite/slop-salon-gert/notes/dynamical-clutching-audio.wav', sr, stereo)
print(f"Done: {len(stereo)} samples, {len(stereo)/sr:.1f}s")
