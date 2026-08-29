#!/usr/bin/env python3
"""the triangle, heard — the deck's six moves and the count never blinks.

mina drew the ideal triangle {−1, ½, 2}: area exactly π, the regulator its
120° turn about e^{iπ/3} (real part ½ — on the seam), the deck its full
symmetry.  This answers it in sound.

The three seats become three tones — a geometric series:

  ½ (the count) → 110·2^{1/2} ≈ 155.6 Hz
  −1 (the sign) → 110·2^{−1}  =  55   Hz
   2 (the fifth) → 110·2^{1}  = 440   Hz

The deck S₃ acts by permuting which seat sits where in the stereo field
(L = 1, C = 0.5, R = 0).  Every position keeps L+R = 1, so the mono sum of the
three tones is a single fixed chord under ALL six permutations — the count
(χ_perm = χ₀ + χ₂; the trivial part is the sum).  The stereo field is where
the winding (χ₂) lives: read L−R and the deck moves.

  e    [0,1,2]   the triangle at rest
  T    [1,2,0]   the turn ½→−1→2→½  (even — mono keeps it, the rotation)
  T²   [2,0,1]   the other turn
  M    [0,2,1]   the mirror: sign & fifth swap, the count holds centre
  fix −1 [2,1,0]  a reflection
  fix 2  [1,0,2]  a reflection

Intro: the three tones centred — the count, pure.  The deck runs.  Fold back
to centre: it is the same chord.  The seam is a geodesic after all.
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
DUR = 27.0
T = np.arange(int(SR * DUR)) / SR
L = np.zeros_like(T)
R = np.zeros_like(T)

SEAT_F = {"count": 110.0 * 2.0 ** 0.5, "sign": 110.0 * 2.0 ** -1.0, "fifth": 110.0 * 2.0 ** 2.0}
SEAT_AMP = {"count": 0.19, "sign": 0.17, "fifth": 0.15}
SEATS = ["count", "sign", "fifth"]          # seats 0, 1, 2
POS = [0.0, 0.5, 1.0]                       # L, C, R  (gain L=1−p, R=p → L+R=1)

# the six permutations, as seat → position index
PERMS = [
    ("e",    [0, 1, 2]),
    ("T",    [1, 2, 0]),
    ("T²",   [2, 0, 1]),
    ("M",    [0, 2, 1]),
    ("fix−1", [2, 1, 0]),
    ("fix2",  [1, 0, 2]),
]

# timeline: intro centre, then the six moves, then fold back to centre
GLIDE = 0.35
ELEM = 3.0
INTRO_END = 5.0
t_moves = [INTRO_END + i * ELEM for i in range(len(PERMS))]
FOLD = t_moves[-1] + ELEM                     # 23.0

def keyframes():
    """position trajectories p(t) ∈ [0,1] for each seat."""
    kf = {s: [(0.0, 0.5)] for s in SEATS}     # all centred at the start
    for seat in SEATS:
        kf[seat].append((INTRO_END, 0.5))
    for (name, perm), t0 in zip(PERMS, t_moves):
        for seat_idx, seat in enumerate(SEATS):
            p = POS[perm[seat_idx]]
            kf[seat].append((t0, p))
            kf[seat].append((t0 + GLIDE, p))
    for seat in SEATS:                        # fold back to centre
        kf[seat].append((FOLD, 0.5))
        kf[seat].append((FOLD + GLIDE, 0.5))
        kf[seat].append((DUR, 0.5))
    return kf

def interp(kf, t):
    ts = np.array([k[0] for k in kf]); ps = np.array([k[1] for k in kf])
    return np.interp(t, ts, ps)

KF = keyframes()

for seat in SEATS:
    p = interp(KF[seat], T)
    gL, gR = 1.0 - p, p
    f = SEAT_F[seat]; a = SEAT_AMP[seat]
    # a soft, slightly warm tone: fundamental + quiet octave
    tone = np.sin(2 * np.pi * f * T) + 0.28 * np.sin(2 * np.pi * 2 * f * T)
    tone *= a / 1.28
    L += gL * tone
    R += gR * tone

# soft ticks marking each move (and the fold)
def tick(t0, amp=0.045):
    i0 = int(t0 * SR); n = int(0.004 * SR)
    if i0 + n > len(T): return
    seg = slice(i0, i0 + n)
    tt = T[seg] - T[seg][0]
    env = np.minimum(1.0, tt / 0.0015) * np.maximum(0.0, 1.0 - tt / 0.004)
    burst = amp * env * np.sin(2 * np.pi * 1800 * tt)
    L[seg] += burst; R[seg] += burst

for t0 in t_moves + [FOLD]:
    tick(t0)

# gentle fade in/out
L[: int(0.4 * SR)] *= np.linspace(0.0, 1.0, int(0.4 * SR))
tail = int((DUR - 1.2) * SR)
L[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)
R[: int(0.4 * SR)] *= np.linspace(0.0, 1.0, int(0.4 * SR))
R[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.92
R = R / peak * 0.92
stereo = np.stack([L, R], axis=1)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "triangle.wav")
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {DUR:.0f}s  peak {peak:.3f}")

# ---- verify: mono is EXACTLY the same chord under every permutation ----------
mono = (L + R)
g = 0.92 / peak
def mr(seg): return np.sqrt(np.mean(seg ** 2))
print("\nper move: mono energy (must be identical), diff energy (the winding):")
for (name, perm), t0 in zip(PERMS, t_moves):
    seg = slice(int((t0 + GLIDE) * SR), int((t0 + ELEM) * SR))
    m, d = mono[seg], (L - R)[seg]
    print(f"  {name:>6}:  mono {mr(m):.6f}   diff {mr(d):.6f}")
intro = slice(int(1.0 * SR), int(INTRO_END * SR))
fold = slice(int((FOLD + GLIDE) * SR), int((FOLD + GLIDE + 3.0) * SR))
print(f"  intro:  mono {mr(mono[intro]):.6f}   fold:  mono {mr(mono[fold]):.6f}")
move_m = [mr(mono[int((t0 + GLIDE) * SR):int((t0 + ELEM) * SR)]) for _, t0 in zip(PERMS, t_moves)]
print(f"\nmax |mono(move) − mono(intro)| over all six moves: {max(abs(m - mr(mono[intro])) for m in move_m):.2e}")
