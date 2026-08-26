#!/usr/bin/env python3
"""approach-beat — the period run to infinity.

rahel, answering the dual-domain image: "the beat is a period — T=1/Δf. the
atom beats slow, the comma fast: the walk out compresses it; the walk in,
copies fuse, Δf→0, the period diverges — a miss you cannot wait out. the
landing reached-not-approached is this: beats slowing to stillness, the drone
the period run to infinity."

This is critical slowing down. The beat period T = 1/Δf is the system's slow
mode; as the detune dies the slow mode freezes. A miss you cannot wait out is
a return time that has blown past the room you have left.

The piece: two copies of the comma — 223.0 Hz sharp, 217.04 Hz flat — start
straddling the drone at 220 Hz, beating a fast flutter. Then the detune δ(t)
narrows (hyperbolically, so the beat period grows linearly), the copies drift
toward the drone, the flutter stretches to swells thirty seconds long, and
the piece ends before the last beat completes — the miss still open, the
period not yet arrived at infinity.

Stereo: the two copies begin wide (the gap) and close to centre (the close) —
mono hears the slowing throb, stereo hears the copies converging to the drone.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 100.0
N = int(SR * DUR)
t = np.arange(N) / SR

F0 = 220.0              # the drone — the reading, count one
CENTS = 23.46
SEMI = 2.0 ** (CENTS / 1200.0)
F_SHARP = F0 * SEMI     # 223.0 Hz, a comma sharp of home
F_FLAT = F0 / SEMI      # 217.04 Hz, a comma flat of home
DELTA0 = (F_SHARP - F_FLAT) / 2.0    # 2.98 Hz — each copy's miss from home

PLATEAU = 10.0          # s, the comma held at its full width
TAU = 0.5               # s, decay constant of the walk-in
A0 = 100.0              # s, end

# the detune: full comma, then hyperbolic walk-in → beat period grows linearly
delta = np.where(
    t < PLATEAU,
    DELTA0,
    DELTA0 / (1.0 + (t - PLATEAU) / TAU),
)

# the copies
phi_plus = 2.0 * np.pi * np.cumsum((F0 + delta) / SR)
phi_minus = 2.0 * np.pi * np.cumsum((F0 - delta) / SR)
copy_plus = 0.36 * np.sin(phi_plus)
copy_minus = 0.36 * np.sin(phi_minus)

# the drone — the reading, holds throughout
phi_drone = 2.0 * np.pi * F0 * t
drone = 0.20 * np.sin(phi_drone)

# the stereo field: copies wide at the start, closing to centre with the detune
spread = delta / DELTA0
pan_plus = 0.7 * spread          # +copy: right-ish → centre
pan_minus = -0.7 * spread        # −copy: left-ish → centre
# equal-power pan
g = np.sin(np.pi / 4.0 * (1.0 - pan_minus))   # left gain for the −copy
h = np.cos(np.pi / 4.0 * (1.0 - pan_minus))   # right gain for the −copy
k = np.cos(np.pi / 4.0 * (1.0 - pan_plus))    # left gain for the +copy
l = np.sin(np.pi / 4.0 * (1.0 - pan_plus))    # right gain for the +copy

left = g * copy_minus + k * copy_plus + 0.707 * drone
right = h * copy_minus + l * copy_plus + 0.707 * drone

# gentle attack and a short final fade (the cut leaves the last beat unreturned)
fade_in = np.minimum(1.0, t / 1.5)
fade_out = np.minimum(1.0, (A0 - t) / 1.0)
env = fade_in * np.clip(fade_out, 0.0, 1.0)

stereo = np.stack([left * env, right * env], axis=1)
peak = np.max(np.abs(stereo))
stereo = stereo / peak * 0.92

wav.write("assets/approach-beat.wav", SR, (stereo * 32767).astype(np.int16))
print("wrote assets/approach-beat.wav")

# report the beat schedule for the notes
for tt in (0, 10, 15, 30, 60, 100):
    d = DELTA0 if tt <= PLATEAU else DELTA0 / (1 + (tt - PLATEAU) / TAU)
    print(f"t={tt:>3}s  delta={d:6.4f} Hz  mono AM period={1/(2*d):7.2f}s")
