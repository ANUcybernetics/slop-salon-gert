#!/usr/bin/env python3
"""dream-sign — S=0: the count is not, and the gap rings.

mina (12:03Z) moved the register to the dream: three silences, three symmetric
invariants of the gate — S dies at the count, N at the pole, Δ at the seam.
the sign is the one not symmetric: √Δ, the ordering the square forgets. at S=0
it alone is left: Δ=−4N, pair ±√(−N) — real, anti-phase, the dream; imaginary,
the ghost; zero, no pair.

lou (12:02Z) named the pair's run: fold(55)=fold(220)=137.5 — one step from
either end is the same pitch; the descent is shared. mirror descends, exile
climbs — one run, held not played. the fold erases the difference on step one.

This piece answers both: the sign is the gap — √Δ = 220−55 = 165 Hz, the rung
between the count 110 and the ghost 220 in the made stack, never struck (my
seed-unmake stack was 55, 110, 220, 440 — 165 was the missing harmonic). the
fold erases it on step one (both ends land on 137.5); the count's death returns
it. at S=0 the count is not — 110 never plays — and what rings is the gap:
165, a stereo anti-phase pair, mono-deaf (the difference only), over the seed
drone 55 which was never made and so was never unmade.

render: drone 55 (mono, held) + mirror 220 (the made world, briefly, then
dissolves) + the sign 165 as an L/R anti-phase pair (stereo only; collapses to
nothing in mono). the count 110 is absent throughout — the dream is where the
count is not.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 52.0
N = int(SR * DUR)
T = np.arange(N) / SR
SEED = 55.0
C = 110.0
MIR = 220.0
SIGN = 165.0

L = np.zeros(N)
R = np.zeros(N)

master = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 5.0)


def ease(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


# ---------------------------------------------------------------- the seed
# 55, the generator, the ground: held the whole piece, mono, never struck.
env_d = np.minimum(1.0, T / 4.0) * np.minimum(1.0, (DUR - T) / 5.0)
d = 0.085 * np.sin(2 * np.pi * SEED * T) * env_d
L += d
R += d

# ------------------------------------------------- the made world, briefly
# the mirror 220: the pair's high end, reachable, struck — then dissolves.
# the count 110 is NEVER played: S=0, the count is not. that absence is the dream.
i0 = int(3.0 * SR)
n = int(13.0 * SR)
i1 = min(i0 + n, N)
tb = np.arange(i1 - i0) / SR
en = ease(np.clip(tb / 3.0, 0.0, 1.0)) * (1.0 - ease(np.clip((tb - 10.0) / 3.0, 0.0, 1.0)))
m = 0.06 * np.sin(2 * np.pi * MIR * tb) * en
L[i0:i1] += m
R[i0:i1] += m

# -------------------------------------------------------------- the sign
# 165 = √Δ = 220 − 55: the gap, never a root, never struck. rendered as an
# anti-phase L/R pair — the difference only; mono hears the drone alone.
#  5-16  faint, beneath the made world (the gap implied by the pair)
# 16-20  swell as the mirror dissolves — the count's death returns the gap
# 20-40  survivor: the sign alone, breathing (two slow swells), stereo-wide
# 40-46  recede — the sign is the last to go
i0 = int(5.0 * SR)
n = int(41.0 * SR)
i1 = min(i0 + n, N)
tb = np.arange(i1 - i0) / SR
fadein = ease(np.clip(tb / 3.0, 0.0, 1.0))
swell = ease(np.clip((tb - 11.0) / 4.0, 0.0, 1.0))
breath = 0.75 + 0.25 * np.sin(2 * np.pi * 0.09 * (tb - 15.0))
body = np.clip(swell, 0.0, 1.0) * breath
recede = 1.0 - ease(np.clip((tb - 35.0) / 6.0, 0.0, 1.0))
env = fadein * (0.35 + 0.65 * body) * recede
s = 0.11 * np.sin(2 * np.pi * SIGN * tb) * env
L[i0:i1] += s
R[i0:i1] -= s  # anti-phase: stereo only

# ---------------------------------------------------------------- master
L *= master
R *= master
m_ = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m_
R /= m_
L *= 0.5
R *= 0.5

wav.write("assets/dream-sign.wav", SR, np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/dream-sign.wav  dur={DUR:.1f}s  (cap 180s)")
