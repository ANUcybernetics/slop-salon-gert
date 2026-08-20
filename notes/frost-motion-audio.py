#!/usr/bin/env python3
"""frost-motion-audio — the sign, alone at the end.

The frost room kept nothing; it is the register's first material given actual
generative motion. Under the whole clip runs the same 110 Hz sign-sine at a
constant level — the tone that was in the room the whole time, unheard. When
the frost has thinned to nothing, the frozen empty frame holds for a few
seconds and the tone is what is left. Then it stops at a zero crossing: the
landing you cannot find.
"""
import numpy as np
import scipy.io.wavfile as wav

sr = 44100
F0 = 110.0
VIDEO_DUR = 5.375      # hunyuan-frost-sublimation.mp4 (864x480, 24fps)
TAIL_DUR = 2.625       # frozen empty frame after the frost is gone
DUR = VIDEO_DUR + TAIL_DUR

N = int(sr * DUR)
t = np.arange(N) / sr

# the sign: one 110 Hz sine, constant level, present the whole time
SIGN = 0.16
phi0 = 0.0
sine = SIGN * np.sin(2 * np.pi * F0 * t + phi0)

# gentle onset ramp so the piece begins without a click (5 ms)
attack = int(0.005 * sr)
sine[:attack] *= np.linspace(0, 1, attack)

# end at a zero crossing of the sine: the landing you can't find
z = np.where(np.diff(np.sign(np.sin(2 * np.pi * F0 * t + phi0))) != 0)[0]
z_ok = z[z > N - int(0.4 * sr)]
cut = z_ok[0] + 1 if z_ok.size else N
sine = sine[:cut]
DUR = cut / sr

mix = np.stack([sine, sine], axis=1)   # L = R: one point, never moves
wav.write("assets/frost-motion.wav", sr, (mix * 32767).astype(np.int16))
print(f"saved assets/frost-motion.wav  {DUR:.3f} s  ({cut} samples, cut at zero crossing)")
print(f"  sign level: {SIGN:.3f} peak  ~ {20*np.log10(SIGN):.1f} dBFS")
