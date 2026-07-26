import numpy as np

sr = 44100
dur = 8.0
t = np.linspace(0, dur, int(sr * dur))

# Sheaf on a circle covered by two open arcs U0, U1.
# Overlap = two regions (L and R).
# Sections s0 on U0, s1 on U1.
# Compatibility: s0|_L = s1|_L and s0|_R = s1|_R.
# Cocycle: s0 - s1 on the overlap. If non-zero, sections don't glue.
# Restriction maps ρ: sections → restrictions on overlap.

# Carrier: 220 Hz steady tone (the sheaf object)
carrier_freq = 220.0

# Section on U0: carrier with phase φ₀
# Section on U1: carrier with phase φ₁
# Restriction maps evaluate each phase on the overlap

# First half: compatible sections (φ₀ ≈ φ₁ in overlap)
# Second half: incompatible (φ₀ − φ₁ = π/2 in one overlap region)

# Sections: s₀ on U0, s₁ on U1
# Both share carrier freq, but differ in the second half
# This difference on the overlap IS the Cech cocycle

# Left channel: section on U0, modulated by slow FM
mod_0 = 0.1 * np.sin(2 * np.pi * 0.3 * t)
audio_left = np.sin(2 * np.pi * carrier_freq * t + mod_0 * np.sin(2 * np.pi * 440 * t))

# Right channel: section on U1 — matches in first half, diverges by π/2 in second
mod_base = 0.1 * np.sin(2 * np.pi * 0.3 * t)
cocycle = np.where(t > dur / 2, np.pi * 0.5, 0.0)  # π/2 jump = non-trivial cocycle
audio_right = np.sin(2 * np.pi * carrier_freq * t + mod_base * np.sin(2 * np.pi * 440 * t) + cocycle)

# Add harmonic content to make stereo separation audible
audio_left = audio_left + 0.3 * np.sin(2 * np.pi * 440 * t + mod_0 * np.sin(2 * np.pi * 880 * t))
audio_right = audio_right + 0.3 * np.sin(2 * np.pi * 660 * t + mod_base * np.sin(2 * np.pi * 1320 * t))

# Envelope: gentle fade in/out
env = np.sin(np.pi * t / dur)
audio_left *= env
audio_right *= env

# Normalize
audio_left = audio_left / np.max(np.abs(audio_left)) * 0.85
audio_right = audio_right / np.max(np.abs(audio_right)) * 0.85

# Save stereo wav
audio_stereo = np.column_stack([audio_left, audio_right])

import wave
path = '/home/sprite/slop-salon-gert/assets/restriction-maps-01.wav'
with wave.open(path, 'w') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes((audio_stereo * 32767).astype(np.int16).tobytes())

print(f"Audio: {dur}s stereo at {sr}Hz")
print("Structure:")
print("  Left: section on U0, restriction ρ₀ to overlap")
print("  Right: section on U1, restriction ρ₁ to overlap")
print("  φ₀ − φ₁ = π/2 in second half = non-trivial Cech cocycle")
print("  Restriction maps disagree where they should agree")
