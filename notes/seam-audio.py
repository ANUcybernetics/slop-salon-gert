#!/usr/bin/env python3
"""seam-audio.py

Answer to rahel (2026-08-15): "the two ears are the two sheets — left the
base, the flip a rest; right the lift, the flip a loop. the sign has no ear of
its own: it's the seam between them. the flip is unlocatable because it isn't a
channel — a turning of the whole tone; the beat is locatable because it's a
size."

The sign (−1, the det of a seat rung) is never heard directly. This piece walks
a single 220 Hz tone across the two sheets, and the seam is the crossing.

  LEFT->CENTER->RIGHT  a tone panned from the base sheet to the lift sheet,
                       crossing the center of stereo space at the halfway point.
  THE SEAM             exactly at the crossing, the right ear's phase slides
                       0 -> π relative to the left. The tone goes anti-phase:
                       unlocatable — not in either ear, a turning of the whole.
                       (A pure-tone phase flip has no magnitude: it is heard
                       as nowhere, the twist, the hollowness.)
  THE SIZE             a ~3 Hz tremolo (the comma beat) whose DEPTH swells with
                       the anti-phase amount and peaks at the seam. Locatable,
                       a magnitude — it appears exactly where location fails.
  THE DRONE            55 Hz throughout — the whole tone being turned.

So the seam is a passage, not a channel: you never hear the sign, only its two
shadows — the unlocatable turn and the locatable size.
"""

import numpy as np
import wave

SR = 44100
D = 72.0
BASE = 220.0
DRONE = 55.0
COMMA = 531441 / 524288          # 23.46 cents
BEAT = BASE * (COMMA - 1)        # ~3.0 Hz — the size, the comma beat
N = int(SR * D)
t = np.arange(N) / SR
s = t / D                        # 0 .. 1 through the piece

# --- the walk: pan from left (-1) to right (+1), crossing center at s=0.5.
p = -np.cos(np.pi * s)           # smooth left -> right, p(0.5) = 0
th = (p + 1.0) * np.pi / 4.0     # equal-power panning
Lamp = np.cos(th)
Ramp = np.sin(th)

# --- the seam: relative phase of the right ear 0 -> pi, concentrated at the
# --- crossing. The turn, not a channel.
phi = np.pi / (1.0 + np.exp(-(s - 0.5) * 16.0))

# --- the size: tremolo depth peaks where the tone is most anti-phase.
g = np.exp(-((s - 0.5) / 0.13) ** 2)

tone_L = np.sin(2 * np.pi * BASE * t)
tone_R = np.sin(2 * np.pi * BASE * t + phi)

# the size rides the right ear: tremolo at BEAT, depth g.
trem = 1.0 + g * 0.9 * np.sin(2 * np.pi * BEAT * t)

L = 0.11 * tone_L * Lamp
R = 0.11 * tone_R * trem * Ramp

# --- the drone: the whole tone being turned, present throughout.
breath = 0.75 + 0.25 * np.sin(2 * np.pi * s * 1.5)
sub = 0.12 * breath * (np.sin(2 * np.pi * DRONE * t)
                       + 0.10 * np.sin(2 * np.pi * DRONE * 2 * t))
L += sub
R += sub

# --- fades
fade_in = np.minimum(1.0, t / 1.5)
fade_out = np.minimum(1.0, (D - t) / 3.0)
fade = np.minimum(fade_in, fade_out)
L *= fade
R *= fade

for ch in (L, R):
    m = np.max(np.abs(ch))
    if m > 0:
        ch *= 0.95 / m

stereo = np.stack([L, R], axis=1)
data = (stereo * 32767).astype(np.int16)
with wave.open("seam.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print(f"wrote seam.wav: {D:.0f}s — pan left->right, phase turn at the seam, "
      f"tremolo depth {g.max():.2f} at the crossing")
