#!/usr/bin/env python3
"""foam-audio — the count that only falls.

A foam of 36 bubble resonances sounds together and runs down to zero. Each
bubble carries the Minnaert pitch of its radius (f = f0/r, so small = high,
big = low) and an amplitude set by its surface area (r^2, so small = faint).
Coarsening: small bubbles shrink and are eaten — pitch glides up, amplitude
fades — and end in a pop; large bubbles grow — pitch glides down, amplitude
swells — and persist, popping last. The pop is a short damped chirp down, the
bubble's wall giving way: not a gate imposed from outside but the material
running out. The count falls by one at every pop and never rises; the last
bubble pops and the piece is digital zero — the foam keeps not even the count.

Inverted from ember (crackle IN, nothing to count) and from frost (steady
tones gated OUT at memoryless times): here the tones are born dying, and the
death is intrinsic — surface tension, not a cut.
"""
import numpy as np
import scipy.io.wavfile as wav

sr = 44100
dur = 42.0
n = 36
rng = np.random.default_rng(20260818)

t = np.arange(int(sr * dur)) / sr

# ---- pop times: memoryless waits, last pop at 41.5 s, order shuffled ----
gaps = rng.exponential(1.0, n) * 0.9
pops = np.cumsum(gaps)
pops = 41.5 * pops / pops[-1]

# ---- radii: small bubbles pop early, large pop late (the physics of a foam) ----
rmin, rmax = 0.5, 2.0
radii = np.exp(rng.uniform(np.log(rmin), np.log(rmax), n))
radii = np.sort(radii)              # ascending
pops = pops[np.argsort(pops)]       # ascending
# align: smallest radius -> earliest pop, largest -> latest
# (already both ascending, so index-aligned)

f0 = 1700.0                         # f = f0/r  ->  850 .. 3400 Hz
floor_f = 2.9                       # shrinkers lose radius to r/floor before popping

# ---- per-bubble coarsening direction ----
# bubbles that pop in the first half shrink; the rest grow
shrinkers = pops < np.median(pops)

pan = np.clip(rng.normal(0, 0.7, n), -1, 1)     # a scattered 2-D field
# stereo level: slight centre-weight via pan (equal-power)

mix = np.zeros((len(t), 2))

for i in range(n):
    r0 = radii[i]
    tp = pops[i]
    i_end = int(tp * sr)
    if i_end < 1:
        continue
    tt = t[:i_end]

    if shrinkers[i]:
        # shrink: radius falls from r0 to r0/floor_f across the life -> pitch up
        r = r0 * (1.0 - (1.0 - 1.0 / floor_f) * (tt / tp))
    else:
        # grow: radius rises from r0 to r0*2.2 across the life -> pitch down
        r = r0 * (1.0 + 1.2 * (tt / tp))
    f = f0 / r
    phase = 2 * np.pi * np.cumsum(f) / sr
    amp = 0.075 * (r / rmax) ** 2.0          # loudness follows surface area
    tone = amp * np.sin(phase)
    # no fade: each bubble sounds until its pop and stops there

    a = (pan[i] + 1) * np.pi / 4
    mix[:i_end, 0] += tone * np.cos(a)
    mix[:i_end, 1] += tone * np.sin(a)

    # ---- the pop: the wall gives — a short damped chirp down, at the pitch
    # the bubble carried when it died ----
    pop_dur = 0.022
    pt = np.arange(int(pop_dur * sr)) / sr
    f_pop = f[-1]
    f_chirp = f_pop * (1.0 - 0.28 * pt / pop_dur)   # down ~28%
    pop_phase = 2 * np.pi * np.cumsum(f_chirp) / sr
    env = np.exp(-pt * 90.0) * np.minimum(pt / 0.002, 1.0)   # fast attack, exp decay
    pop = 0.30 * env * np.sin(pop_phase)
    e = i_end
    e2 = min(e + len(pt), len(t))
    if e2 > e:
        seg = pop[: e2 - e]
        mix[e:e2, 0] += seg * np.cos(a)
        mix[e:e2, 1] += seg * np.sin(a)

# 5 ms onset to avoid a DC pop at the very first instant (not a fade)
attack = int(0.005 * sr)
mix[:attack] *= np.linspace(0, 1, attack)[:, None]

# global normalise: one readout level, absences as digital zero
peak = np.abs(mix).max()
mix *= 0.9 / peak

wav.write("assets/foam.wav", sr, (mix * 32767).astype(np.int16))
print(f"saved assets/foam.wav  {dur} s  n={n}  last pop {pops[-1]:.2f}s")
print("last pop amplitude check:", np.abs(mix[int(pops[-1]*sr):int(pops[-1]*sr)+100]).max())
