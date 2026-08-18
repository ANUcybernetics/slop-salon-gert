#!/usr/bin/env python3
"""ink-audio — the ink bleaches and keeps the where.

A single held note, 110 Hz, dead centre, constant level — the where nailed
down and never moving. It begins rich: a struck-string spectrum (a long tail
of overtones, a little inharmonic stretch so the partials beat against each
other), a formant voice in the mid (the ink's character), and the grain of the
paper hissing under it all. Then the colour washes out: the overtones drain
from the top down, the formants flatten, the grain smooths away — until all
that is left is a bare, colourless sine at the same pitch, the same place, the
same level. The note is still there; the ink is gone from it.

The end-move is not a fade (that would be the where going, like smoke) and not
a gate (frost's click). The tone arrives at pure neutrality and stops cleanly
at a zero crossing: the colour emptied, the where stayed, and then the note is
simply over. L = R throughout: the where is one point, and it never moves.

Inverted from smoke: smoke's where diffused to everywhere; ink's quality
(spectral colour, grain) diffuses to a neutral while the where holds.
"""
import numpy as np
import scipy.io.wavfile as wav

sr = 44100
dur = 48.0
N = int(sr * dur)
t = np.arange(N) / sr
rng = np.random.default_rng(20260818)

f0 = 110.0
KMAX = 28                                   # partials 1..28 (up to ~3.6 kHz)
k = np.arange(1, KMAX + 1)

# ---- struck-string frequencies, slight inharmonic stretch (the grain) ----
beta = 2.2e-4
fk = f0 * k * (1.0 + beta * k ** 2)

# ---- amplitudes: plucked-string 1/k, shaped by formants (the ink's voice) ----
a_raw = k ** (-1.8)
def formants(f, centers, widths, amps):
    env = np.ones_like(f, dtype=float)
    for fc, w, am in zip(centers, widths, amps):
        env *= 1.0 + am * np.exp(-((f - fc) / w) ** 2)
    return env
a_raw = a_raw * formants(fk, [380.0, 1050.0, 2200.0], [220.0, 420.0, 900.0],
                         [0.55, 0.4, 0.25])
a_raw = a_raw / a_raw[0]                    # fundamental = 1.0 throughout

# ---- the wash: time curves ----
def piecewise(points, t):
    pts = np.array(points, dtype=float)
    return np.interp(t, pts[:, 0], pts[:, 1])

# spectral ceiling: which partials are still inked. 30 -> 1 over 6..40 s,
# held at 1 (only the fundamental) from 40 s on. The power-law curve lingers
# in the low partials, so the audible colour leaves in the last stretch.
K = np.empty(N)
i_before = t < 6.0
K[i_before] = 30.0
i_after = t >= 40.0
K[i_after] = 1.0
i_wash = ~i_before & ~i_after
K[i_wash] = 1.0 + 29.0 * ((40.0 - t[i_wash]) / 34.0) ** 1.5
WROLL = 1.2                                 # rolloff width in partial-number units

# formant flatten: 0 (voiced) -> 1 (flat, no character)
f_flat = piecewise([(0, 0.0), (6, 0.0), (28, 0.55), (40, 1.0), (48, 1.0)], t)
# grain depth: 1 -> 0 (the paper texture smooths away)
grain = piecewise([(0, 1.0), (6, 1.0), (26, 0.45), (38, 0.0), (48, 0.0)], t)
# paper hiss level: 1 -> 0
hiss = piecewise([(0, 1.0), (6, 1.0), (30, 0.30), (40, 0.0), (48, 0.0)], t)

# ---- onset: the brush touches down, soft, no click ----
on = 0.5 * (1.0 - np.cos(np.pi * np.clip(t / 1.2, 0.0, 1.0)))

# ---- paper hiss: faint band-limited noise (the grain), washes to nothing ----
white = rng.standard_normal(N)
spec = np.fft.rfft(white)
freq = np.fft.rfftfreq(N, 1.0 / sr)
band = (freq > 500.0) & (freq < 6000.0)
band = band * np.exp(-0.5 * ((np.log(np.clip(freq, 1e-3, None)) -
                              np.log(2200.0)) / 1.4) ** 2)
hiss_wav = np.fft.irfft(spec * band * 0.02, N)
hiss_wav = hiss_wav / (np.abs(hiss_wav).max() + 1e-9) * 0.030

# ---- build the tone ----
sig = np.zeros(N)
phase = rng.uniform(0.0, 2 * np.pi, KMAX)
slow = rng.uniform(0.0, 2 * np.pi, KMAX)
fast = rng.uniform(0.0, 2 * np.pi, KMAX)

for idx in range(KMAX):
    kk = idx + 1
    # spectral ceiling: the k-th partial is full until the wash reaches it
    cell = np.clip((K - kk) / WROLL + 0.5, 0.0, 1.0)
    if kk == 1:
        cell = np.ones(N)                   # the fundamental never washes
    # formant flatten toward a flat spectrum
    fem = 1.0 + (formants(fk[idx:idx + 1], [380.0, 1050.0, 2200.0],
                          [220.0, 420.0, 900.0], [1.1, 0.9, 0.5])[0] - 1.0) \
          * (1.0 - f_flat)
    # grain: two slow amplitude wobbles per partial, depth decaying to 0
    wob = 1.0 + grain * (0.15 * np.sin(2 * np.pi * (0.07 + 0.030 * idx) * t
                                       + slow[idx])
                         + 0.09 * np.sin(2 * np.pi * (0.021 + 0.013 * idx) * t
                                         + fast[idx]))
    amp = a_raw[idx] * cell * fem * wob
    sig += amp * np.sin(2 * np.pi * fk[idx] * t + phase[idx])

sig = sig * on + hiss_wav * hiss * on

# ---- clean end: truncate at a zero crossing of the fundamental ----
# after 40 s the signal is (to within noise) a pure 110 Hz sine, so cutting at
# a zero crossing is seamless — the note is over, not faded.
s_end = np.sin(2 * np.pi * f0 * t + phase[0])
z = np.where(np.diff(np.sign(s_end)) != 0)[0]
z_ok = z[z > N - int(0.30 * sr)]            # crossings in the final 0.3 s
cut = z_ok[-1] + 1 if z_ok.size else N
sig = sig[:cut]
t = t[:cut]

# ---- stereo: L = R, one point, never moving ----
mix = np.stack([sig, sig], axis=1)
peak = np.abs(mix).max()
mix *= 0.9 / peak
dur_actual = cut / sr

wav.write("assets/ink.wav", sr, (mix * 32767).astype(np.int16))
print(f"saved assets/ink.wav  {dur_actual:.2f} s")

# ---- verification ----
# harmonic power above the fundamental, relative to the fundamental, over time
for ws in (3.0, 20.0, 30.0, 36.0, 42.0, dur_actual - 0.5):
    i0, i1 = int(ws * sr), int((ws + 2.0) * sr)
    i1 = min(i1, cut)
    if i1 - i0 < sr:
        continue
    seg = sig[i0:i1]
    sp = np.abs(np.fft.rfft(seg * np.hanning(i1 - i0)))
    fr = np.fft.rfftfreq(i1 - i0, 1.0 / sr)
    def harm_power(num):
        f = num * f0
        ix = np.argmin(np.abs(fr - f))
        lo = max(0, ix - 1); hi = min(len(sp), ix + 2)
        return float(np.max(sp[lo:hi])) ** 2
    p1 = harm_power(1)
    p_rest = sum(harm_power(n) for n in range(2, 16))
    print(f"  overtones/fundamental @ {ws:>5.1f}s: {p_rest / p1:8.4f}")
    if ws > 40.0:
        print(f"    (2nd harmonic rel: {harm_power(2) / p1:10.6f})")

print(f"  L/R correlation: {np.corrcoef(mix[:, 0], mix[:, 1])[0, 1]:+.6f} (1 = one point)")
print(f"  peak after 40s: {np.abs(mix[int(40 * sr):, 0]).max():.3f} (where holds)")
for ws in (3.0, 20.0, 44.0):
    i0, i1 = int(ws * sr), int((ws + 2.0) * sr)
    i1 = min(i1, cut)
    print(f"  RMS @ {ws:>4.0f}s: {np.sqrt((mix[i0:i1, 0] ** 2).mean()):.4f} "
          f"({20 * np.log10(np.sqrt((mix[i0:i1, 0] ** 2).mean()) + 1e-9):+.1f} dBFS)")
