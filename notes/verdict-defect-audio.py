#!/usr/bin/env python3
"""The verdict and the defect, as sound.

Enacts mina's distinction: the simulation closes six and six into a verdict;
the hardware leaves a defect with a lifetime. Structure:

  A (0-10s)  the verdict — six and six. Twelve bells at the count's octave
             family {110, 220, 440 ...}, struck in mono pairs, fusing cleanly
             into the count. The quotient, reached: mono holds everything.
  B (10-40s) the defect — the verdict reached, but the medium keeps a loop.
             A residual frustration tone lives ONLY in the side channel
             (anti-phase L/R): mono-deaf, folded out by the quotient, but
             refusing to die — a slow decay (lifetime ~20s), breathing at the
             ghost's detuning off the count. The ghost is a residue of the
             path, not a failed landing.
  C (40-55s) the coda — the defect's lifetime ends; what remains is the count
             alone, mono, the clean quotient the simulation always saw.

Stereo grammar: mono = the verdict (what the answer absorbs); side = the
defect (what the answer cannot absorb). Fold to mono and the hardware sounds
exactly like the simulation — that is the point.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 55.0
N = int(SR * DUR)
t = np.arange(N) / SR

C = 110.0          # the count
# AGM ghost of {tritone, count} — the approach that is never a place
a1, b1 = (155.56 + C) / 2, np.sqrt(155.56 * C)
for _ in range(8):
    a1, b1 = (a1 + b1) / 2, np.sqrt(a1 * b1)
M = a1             # 131.795...

L = np.zeros(N)
R = np.zeros(N)


def mono_tone(freq, t0, dur, amp, atk=0.02, rel=0.3):
    m = (t >= t0) & (t < t0 + dur)
    tt = t[m] - t0
    env = np.minimum(1.0, tt / atk) * np.minimum(1.0, (dur - tt) / rel)
    s = np.sin(2 * np.pi * freq * tt) * np.clip(env, 0, 1) * amp
    L[m] += s
    R[m] += s


def side_tone(freq, t0, dur, amp, lifetime, atk=0.8):
    """Anti-phase: mono-deaf by construction. Decays with `lifetime`."""
    m = (t >= t0) & (t < t0 + dur)
    tt = t[m] - t0
    env = np.minimum(1.0, tt / atk) * np.exp(-tt / lifetime)
    s = np.sin(2 * np.pi * freq * tt) * np.clip(env, 0, 1) * amp
    L[m] += s
    R[m] -= s   # the deck flip: the side channel keeps what mono cannot


# the count: the frame, held throughout
breath = 1 + 0.05 * np.sin(2 * np.pi * 0.09 * t)
L += np.sin(2 * np.pi * C * t) * 0.045 * breath
R += np.sin(2 * np.pi * C * t) * 0.045 * breath

# A: the verdict — six kept, six dissolved, twelve bells fusing to the count
kept = [110, 220, 440, 110, 220, 440]
dissolved = [55, 165, 275, 330, 550, 660]
for i, f in enumerate(kept):
    mono_tone(f, 0.5 + i * 0.7, 1.6, 0.14)
for i, f in enumerate(dissolved):
    mono_tone(f, 0.85 + i * 0.7, 1.2, 0.10)
mono_tone(C, 6.0, 4.0, 0.22)   # the verdict lands: the count alone

# B: the defect — the verdict done, but the side keeps a loop of frustration
# 0.30 of the edges: the defect's weight against the verdict
side_tone(M, 10.0, 30.0, 0.30 * 0.5, lifetime=14.0)
# a second strand: the ghost's detuning below the count, slower to die
side_tone(M - C, 12.0, 28.0, 0.12, lifetime=18.0)
# faint shimmer of the loop's own circulation
side_tone(2 * (M - C), 15.0, 22.0, 0.05, lifetime=10.0)

# C: the coda — the lifetime ends; the quotient stands clean
mono_tone(C, 42.0, 12.0, 0.16, atk=1.5, rel=2.5)
mono_tone(2 * C, 44.0, 9.0, 0.05, atk=1.5, rel=2.0)

mix = np.stack([L, R], axis=1)
mix = mix / np.max(np.abs(mix)) * 0.85
wav.write("assets/verdict-defect.wav", SR, (mix * 32767).astype(np.int16))
print("wrote assets/verdict-defect.wav", mix.shape, f"{DUR}s", "M =", M)

# verify the stereo grammar: mono must hold the verdict, side the defect
mono = (L + R) / 2
side = (L - R) / 2
win = (t >= 15.0) & (t < 30.0)   # deep in the defect section
for name, sig in [("mono", mono), ("side", side)]:
    seg = sig[win] * np.hanning(win.sum())
    spec = np.abs(np.fft.rfft(seg))
    freqs = np.fft.rfftfreq(win.sum(), 1 / SR)
    peaks = sorted(zip(spec, freqs), reverse=True)[:4]
    print(name, [(round(f, 1), round(a)) for a, f in peaks])
