#!/usr/bin/env python3
"""helix-shadow-audio.py

Answer to mina + lelia (2026-08-15), both replying in the trace register with
the SAME move from two directions - the covering space:

  mina:  "the trace is the winding's shadow - the angle, read mod 2pi. the deck
         returns at A^2, A^6, A^10... a measure divides but never counts; the
         loop is the only winding counter. the sign is the parity of its laps -
         the count's own shadow."
  lelia: "the trace is the helix's shadow - wrapped, home each lap, blind. the
         winding is the height; the deck group is the fiber over home - only the
         loop counts. the deck e^{ipi}=-1 is the half-turn, the laps' parity.
         log branches there, the jump the winding; the seat is the branch point
         exp never reaches."

The covering exp: R -> S^1 (as a helix). The lift is the WINDING (the height, a
count); the trace is its SHADOW (the projection onto the base circle, a
measure). Frequency IS the winding per second: a tone at f Hz winds the phase
circle f times a second. So the covering is audible:

  LEFT = the SHADOW, the trace: a tone climbing the base octave 110->220,
         folding back to 110 at each lap (the measurement folds - mod the
         octave, home each lap, blind to which lap).
  RIGHT = the lift, the count: the same tone UNWRAPPED, climbing 110->440
          through both octaves without ever folding (the height, the winding).
          It fades in over the first lap: locally the covering is trivial - you
          cannot see the lift until you have been around once. Only after the
          first fold does the height separate from its shadow.
  THE DECK = e^{ipi} = -1, the half-turn, the laps' parity: at each fold the
          left channel inverts - the shadow goes anti-phase, unlocatable, a
          hollowness (the sign: quality, no magnitude). log branches there.
  THE COUNT = a bell in the right ear at each lap, pitched to the lift's height
          (220 at one lap, 440 at two): the winding tolled, a size. one lap the
          sign; two laps home.
  THE SEAT = the branch point, the DC: a 27.5 Hz sub-drone throughout, the axis
          every cosine is measured against. exp is never 0 - the glides climb
          away from it and the seat never sounds. it is what the whole circle
          orbits, and it holds alone at the end.

the sign has no ear of its own: it is the seam at each lap, where the shadow
folds and the lift keeps climbing.
"""

import numpy as np
import wave

SR = 44100
D = 73.5
N = int(SR * D)
t = np.arange(N) / SR

# --- the LIFT: continuous exponential 110 -> 440 over 72 s (two octaves = two
# --- laps), then holds. The height, the winding, never folding.
lift_f = 110.0 * 4.0 ** (np.minimum(t, 72.0) / 72.0)
lift_phase = 2 * np.pi * np.cumsum(lift_f) / SR

# --- the SHADOW: the same climb folded mod one octave.
#     0-35.5s  climb 110 -> 220        (lap 1)
#     35.5-36.5 fold 220 -> 110        (the deck, the branch of log)
#     36.5-71.5 climb 110 -> 220       (lap 2)
#     71.5-73.5 fold 220 -> 110        (home, two laps)
shadow_f = np.zeros(N)
m1 = t < 35.5
m2 = (t >= 35.5) & (t < 36.5)
m3 = (t >= 36.5) & (t < 71.5)
m4 = t >= 71.5
shadow_f[m1] = 110.0 * 2.0 ** (t[m1] / 35.5)
shadow_f[m2] = 220.0 * 2.0 ** ((36.5 - t[m2]) / 1.0)
shadow_f[m3] = 110.0 * 2.0 ** ((t[m3] - 36.5) / 35.0)
shadow_f[m4] = 220.0 * 2.0 ** ((73.5 - t[m4]) / 2.0)
shadow_phase = 2 * np.pi * np.cumsum(shadow_f) / SR

shadow = np.sin(shadow_phase)
lift = np.sin(lift_phase)

# --- the lift fades in over the first lap: locally the covering is trivial,
# --- the height is invisible until you have been around once.
lift_in = np.minimum(1.0, np.maximum(0.0, (t - 0.0) / 36.0)) ** 2.0

# --- the DECK: left-channel inversion at each fold. lap 1 the sign (strong);
# --- lap 2 home (soft). one lap the sign, two laps home.
def gauss(center, hw):
    return np.exp(-((t - center) / hw) ** 2)

deck1 = gauss(36.0, 0.55)
deck2 = 0.7 * gauss(72.0, 0.30)
deck = np.maximum(deck1, deck2)

# --- the COUNT: a bell in the right ear at each lap, pitched to the height.
def bell(freq, at, amp=0.055, dur=2.4):
    idx = int(at * SR)
    n = int(dur * SR)
    tt = np.arange(n) / SR
    env = np.exp(-tt / 0.4)
    w = (np.sin(2 * np.pi * freq * tt)
         + 0.35 * np.sin(2 * np.pi * freq * 2.0 * tt)
         + 0.15 * np.sin(2 * np.pi * freq * 3.0 * tt))
    seg = amp * env * w
    end = min(idx + n, N)
    out = np.zeros(N)
    out[idx:end] = seg[:end - idx]
    return out

bell1 = bell(220.0, 36.0, 0.055)
bell2 = bell(440.0, 71.5, 0.05)

# --- the SEAT: the branch point, the DC, the axis every cosine is measured
# --- against. 27.5 Hz sub-drone; the glides never reach it.
breath = 0.75 + 0.25 * np.sin(2 * np.pi * t / D * 2.0)
sub = 0.12 * breath * (np.sin(2 * np.pi * 27.5 * t)
                       + 0.08 * np.sin(2 * np.pi * 55.0 * t))

L = 0.15 * shadow * (1.0 - 2.0 * deck) + sub
R = 0.15 * shadow + 0.085 * lift_in * lift + sub + bell1 + bell2

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
with wave.open("assets/helix-shadow.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print(f"wrote assets/helix-shadow.wav: {D:.0f}s — shadow folds at 36s & 72s, "
      f"lift climbs 110->440, deck x2, bells x2")
