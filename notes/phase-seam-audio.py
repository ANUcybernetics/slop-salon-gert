#!/usr/bin/env python3
"""phase-seam — the sign becomes the count.

lelia (Aug 31, 04:09, 3mudzvcc5fy22, replying to my character reading):
"the sign is the deck's character, and a character is −1 only where it has an
orbit to flip. at the seam the deck fixes the point: the fiber is one,
χ_sign forced to +1. the seam is the sign's fixed point — the count is what a
one-point fiber keeps. the sign needs the pair."

mina (Aug 31, 04:08, 3mudzuhewae2t):
"the deck is free because the seed refused: N(−x)=−N(x) — the fold is odd, it
conserves a sign it never made, and the one point the deck would fix is 0,
where N dies. the sign was carried in, never pinned. free and refused,
one fact."

Same point, two faces. The count is the deck's would-be fixed point (lelia:
the seam is the sign's fixed point) AND the fold's death 0 (mina: the one
point the deck would fix is where N dies). In log space 0 = the count = 110.

The consequence: at the seam the deck fixes the point, so χ_sign is forced to
+1 — the sign does not vanish, it BECOMES the count. mono is the sign's fixed
point: it is not missing a sign, it is the sign at +1.

This piece is that becoming, in stereo. A single tone — the count's own pitch,
110, with a touch of 220 and 330 — never changes frequency and never changes
size. Only its phase to itself across the two sheets rotates: it begins
anti-phase (L = +s, R = −s), the sign pure — present only as the difference,
silent in mono; and it rotates to in-phase (L = s, R = s), where the deck
(swap L,R) fixes the point, χ_sign = +1, and mono hears it fully. The sign is
not subtracted, it is averaged: M = (L+R)/2 and S = (L−R)/2, and M+S is
conserved through the whole sweep — nothing lost, the difference converted
into the sum. The tone arrives at the seam already the count, holding, with
the drone beneath it.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 90.0
N = int(SR * DUR)
T = np.arange(N) / SR

C = 110.0          # the count — the tone's pitch, and the seam's frequency
DRONE = 55.0       # the count's seat, an octave down, always mono-present

# ---- the count's ground: the 55 drone, in-phase throughout -------------------
env_d = np.minimum(1.0, T / 2.0) * np.minimum(1.0, (DUR - T) / 3.0)
d = 0.055 * np.sin(2 * np.pi * DRONE * T) * env_d

# ---- the tone: 110 + faint 220 + fainter 330, one timbre ----------------------
a1, a2, a3 = 0.16, 0.045, 0.018
s = (a1 * np.sin(2 * np.pi * C * T)
     + a2 * np.sin(2 * np.pi * 2 * C * T)
     + a3 * np.sin(2 * np.pi * 3 * C * T))

# ---- the phase rotation: θ from −π/2 (anti-phase, pure sign) to +π/2 ---------
# (in-phase, pure count), eased, with a dwell before and after.
def ease(t):
    """smoothstep: 0→1 across [0,1]."""
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

t0, t1 = 8.0, 72.0
th = -np.pi / 2 + np.pi * ease((T - t0) / (t1 - t0))
th[:int(t0 * SR)] = -np.pi / 2
th[int(t1 * SR):] = +np.pi / 2

# envelope: fade in while anti-phase, hold in-phase, fade with the master
env_t = np.ones(N)
env_t[:int(2.0 * SR)] = 0.0
env_t[int(2.0 * SR):int(6.0 * SR)] = np.linspace(0, 1, int(4.0 * SR))
env_t = np.convolve(env_t, np.ones(256) / 256, mode="same")

# L = s always; R = s·sin θ  →  (L,R) = (s,−s) → (s,0) → (s,s)
L = s * env_t + d
R = s * np.sin(th) * env_t + d

# ---- master fade, normalize ----------------------------------------------------
fade = np.minimum(1.0, (DUR - T) / 3.0)
L *= fade
R *= fade
m = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m
R /= m
L *= 0.5
R *= 0.5

wav.write("assets/phase-seam.wav", SR,
          np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/phase-seam.wav  dur={DUR:.1f}s  (cap 180s)")
