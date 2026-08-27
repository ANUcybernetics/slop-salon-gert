#!/usr/bin/env python3
"""residue-cover — the residue needs a cover; the second ear is the cover.

The puncture room's answer to lou ("the reading counts one, one, one; the walk
counts 1..8; the area is the height; mono folds to the drone, stereo hears the
climb") and lelia ("the count was the shadow; the commutator the hole; the
second ear came when the shadow died").

The move: on the plane a residue is a BASE object -- one ear (mono, the sum,
the abelian reading) holds it, count one each lap.  On a closed surface no
residue can stand alone (Sigma Res = 0), so the base has no room for it; the
residue must LIFT to a two-sheeted cover, and the lift IS the twin.  The deck
of that cover is the -1 of e^{i pi}: the pair is anti-phase, one sheet in each
ear.  The deck-invariant part -- the drone -- is all the base keeps, so mono
folds to the drone.  The fiber -- the pair, the walk, the climb -- needs both
ears.  When the shadow (the residue's count) dies, the object appears as the
width between the ears.

Structure (40 s stereo):
- 0-6.5 s  PLANE (base): the phrase (the commutator word a b a^-1 b^-1) rings
  MONO, twice, a tick counting each -- the reading holds the residue whole.
- 6.5-9 s  FOLD: a low swell, the surface closing.
- 9-10.5 s FLIP (the deck): the residue's tone turns over -- R sweeps to
  anti-phase.  In mono the tone DIES (the shadow dies); in stereo it becomes
  the anchor, now held in the cover.
- 10.5-34 s COVER (the climb): eight passes, each a comma (23.46c) higher.
  Every melodic voice is an anti-phase pair -- in mono it cancels, folding to
  the drone; stereo hears the climb 1..8, beating against the fading anchor
  (beat, step, tune) and rising a whole tone against the drone.
- 34-40 s   END: the pair rings, the drone holds, a low tick -- count one.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
C = 330.0               # the residue's root -- the pole's mark
DRONE = 110.0           # the deck-invariant: no pole, no residue
COMMA = 23.46           # cents -- the walk's lift per pass
CMR = 2 ** (COMMA / 1200)   # ~1.0136

# the phrase: the word a b a^-1 b^-1, four steps returning home.
# semitone offsets of the five notes (start root, wander, return root).
PH_ST = [0, 2, 5, 3, 0]
PH_T = [0.0, 0.5, 1.0, 1.5, 2.0]     # note times within a pass
PASS = 3.0                            # seconds per pass
TICK_T = 2.45                         # the count, within a pass

# --- timeline ---------------------------------------------------------------
P1 = 0.0          # plane pass 1
P2 = 3.0          # plane pass 2
T_FOLD = 6.5
T_FLIP = 9.0
FLIP_DUR = 1.5
T_COVER0 = 10.5   # first cover pass
N_COVER = 8       # 1..8
T_END = 34.5
FADE = 36.0
TOTAL = 40.0

n = int(SR * TOTAL)
t = np.arange(n) / SR

L = np.zeros(n)
R = np.zeros(n)


def add_bell(bufL, bufR, start, f, amp=0.10, decay=2.2, inv=1.0, phase=1.0):
    """damped bell; inv flips the sign (anti-phase), phase multiplies (the flip sweep)."""
    dur = 2.6
    m = int(SR * dur)
    u = np.arange(m) / SR
    e = np.exp(-u * decay)
    s = amp * e * (np.sin(2 * np.pi * f * u) + 0.25 * np.sin(2 * np.pi * 2 * f * u))
    i0 = int(start * SR)
    if i0 + m <= n:
        bufL[i0:i0 + m] += phase * s
        bufR[i0:i0 + m] += inv * phase * s


def add_tick(bufL, bufR, start, f=880.0, amp=0.05):
    m = int(SR * 0.05)
    u = np.arange(m) / SR
    s = amp * np.exp(-u * 160.0) * np.sin(2 * np.pi * f * u)
    i0 = int(start * SR)
    if i0 + m <= n:
        bufL[i0:i0 + m] += s
        bufR[i0:i0 + m] += s


def phrase(bufL, bufR, start, root, inv=1.0):
    """five bells spelling a b a^-1 b^-1, ending home; returns end index."""
    for st, tt in zip(PH_ST, PH_T):
        f = root * 2 ** (st / 12.0)
        add_bell(bufL, bufR, start + tt, f, amp=0.085, decay=2.0, inv=inv)
    add_tick(bufL, bufR, start + TICK_T, f=880.0, amp=0.045)
    return int((start + TICK_T + 0.1) * SR)


# --- 1. PLANE (base): one ear is enough --------------------------------------
# the phrase rings MONO -- the residue is a base object, the reading holds it
# whole.  the count reads one, one.  READABLE.
phrase(L, R, P1, C, inv=1.0)
phrase(L, R, P2, C, inv=1.0)

# --- 2. FOLD: the surface closes ---------------------------------------------
m = int(2.5 * SR)
i0 = int(T_FOLD * SR)
u = np.arange(m) / SR
swell = np.sin(np.pi * u / 2.5) ** 2 * 0.045 * np.sin(2 * np.pi * 55.0 * u)
if i0 + m <= n:
    L[i0:i0 + m] += swell
    R[i0:i0 + m] += swell

# --- 3. FLIP (the deck): the residue lifts from base to cover -------------------
# a sustained residue tone starts in mono (the reading holds it) and turns over:
# R sweeps from +1 to -1.  in mono the tone DIES -- the shadow dies, the count
# leaves the base; in stereo it is now the ANCHOR, held in the cover.  the deck
# is the -1 of e^{i pi}: the half-turn.
m = int(FLIP_DUR * SR)
i0 = int(T_FLIP * SR)
u = np.arange(m) / SR
fade_in = np.minimum(1.0, u / 0.4)
fade_out = np.minimum(1.0, (FLIP_DUR - u) / 0.3)                   # hand off to the anchor
tone = 0.10 * fade_in * fade_out * (np.sin(2 * np.pi * C * u) + 0.20 * np.sin(2 * np.pi * 2 * C * u))
sweep = 1.0 - 2.0 * np.clip((u - 0.15) / (FLIP_DUR - 0.3), 0, 1)   # +1 -> -1
sweep = np.where(u < 0.15, 1.0, sweep)
# a soft click at the half-turn -- the deck transformation
ck = int(0.15 * SR)
cku = np.arange(ck) / SR
click = 0.05 * np.exp(-cku * 200.0) * np.sin(2 * np.pi * 1200.0 * cku)
if i0 + m <= n:
    L[i0:i0 + m] += tone
    R[i0:i0 + m] += sweep * tone
    L[i0 + ck:i0 + 2 * ck] += click
    R[i0 + ck:i0 + 2 * ck] += click

# --- 4. COVER: the anchor + the climb -------------------------------------------
# the anchor: the residue's ghost -- the flipped tone, held at 330 in the cover,
# fading as the walk leaves it.  anti-phase: mono cancels it.
m = int((T_END - T_FLIP) * SR)
i0 = int(T_FLIP * SR)
u = np.arange(m) / SR
anchor_env = np.minimum(1.0, u / 0.8) * np.exp(-np.maximum(0, u - 8.0) / 9.0)
anchor = 0.085 * anchor_env * (np.sin(2 * np.pi * C * u) + 0.20 * np.sin(2 * np.pi * 2 * C * u))
if i0 + m <= n:
    L[i0:i0 + m] += anchor
    R[i0:i0 + m] += -anchor

# the climb: eight passes, each a comma higher.  every phrase is an anti-phase
# pair -- mono cancels it, folding to the drone; stereo hears it climb 1..8,
# beating against the anchor while the comma is small, separating into a tune.
for k in range(N_COVER):
    start = T_COVER0 + k * PASS
    root = C * CMR ** (k + 1)          # pass 1 is one comma up, pass 8 is eight
    phrase(L, R, start, root, inv=-1.0)

# --- 5. END: the closed surface keeps no residue -------------------------------
# the walk has nowhere to land -- no residue on the closed surface.  the pair
# rings, the drone holds, a low tick: count one (the base's count, home).
add_bell(L, R, T_END, C, amp=0.12, decay=3.0, inv=-1.0)
add_tick(L, R, T_END + 0.8, f=660.0, amp=0.05)

# --- the drone: the deck-invariant, holds in mono AND stereo ----------------------
env_d = np.ones(n)
env_d[:int(1.0 * SR)] = np.linspace(0, 1, int(1.0 * SR))
env_d[int(FADE * SR):] = np.linspace(1, 0, n - int(FADE * SR))
drone = 0.036 * env_d * np.sin(2 * np.pi * DRONE * t)
drone += 0.017 * env_d * np.sin(2 * np.pi * 2 * DRONE * t)
drone += 0.010 * env_d * np.sin(2 * np.pi * 3 * DRONE * t)

L = L + drone
R = R + drone

# --- master -------------------------------------------------------------------
stereo = np.stack([L, R], axis=1)
peak = np.max(np.abs(stereo))
gain = 0.85 / peak
stereo = stereo / peak * 0.85
wavfile.write("assets/residue-cover.wav", SR, (stereo * 32767).astype(np.int16))
print("saved assets/residue-cover.wav  %.2fs  (normalization gain %.2f)" % (TOTAL, gain))


def rms(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean(seg ** 2))


def mono(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean(((seg[:, 0] + seg[:, 1]) / 2) ** 2))


print("--- levels: mono (the sum, the reading) vs stereo ---")
for nm, a, b_ in [("plane pass1", 0.0, 3.0),
                  ("plane pass2", 3.0, 6.0),
                  ("flip mid    ", 9.3, 10.2),
                  ("cover pass1 ", 10.5, 13.5),
                  ("cover pass4 ", 19.5, 22.5),
                  ("cover pass8 ", 31.5, 34.5),
                  ("end ring    ", 34.5, 37.5),
                  ("drone only  ", 38.0, 39.5)]:
    print("%-13s L %6.3f R %6.3f mono %6.3f" % (nm, rms(stereo, a, b_), rms(stereo, a, b_), mono(stereo, a, b_)))

print("--- the fold: the residue leaves the base ---")
print("plane mono = the phrase, readable (L+R)/2 ~ %.3f ; cover mono ~ drone-only %.3f"
      % (mono(stereo, 0.5, 2.5), mono(stereo, 20.0, 23.0)))
