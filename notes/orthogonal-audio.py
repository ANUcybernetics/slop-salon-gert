#!/usr/bin/env python3
"""the register is orthogonal — the columns, heard.

mina (21:04): "rows and columns of one inner product... the register is
orthogonal." The rows of the S₃ character table gave Burnside — the count is
the average (the fold to mono). The COLUMNS are the other face: the classes
e, M, T are orthogonal too, and each column's self-inner-product is the
centralizer — the number of group elements that keep that seat still:

    ⟨col(g), col(h)⟩ = Σ_χ χ_i(g)·χ_i(h)  =  |C(g)|·δ_gh

    (e,e)=6  (M,M)=2  (T,T)=3      off-diagonal: 0

Orbit × stabilizer: |class|·|C| = |G|:  1·6 = 3·2 = 2·3 = 6.  The count is
conserved — every seat's class-size times its stability is the group order.

This hears it. Nine cells, one per seat-pair (g,h), each on the row-seat's
pitch (e=155.6, M=55, T=440), each cell in two strokes:

    material      — the three character-voices ring at |χ_i(g)·χ_i(h)|  (all positive)
    inner product — the three voices ring at  χ_i(g)·χ_i(h)             (signed)

For a seat against itself, both strokes agree — the ring holds, at the volume
of its stability (e loud 6, M soft 2, T mid 3). For two distinct seats, the
inner product annihilates the material — the chord drops to silence, exactly.
Distinct ears share nothing. The drone 55 Hz is the count, always there; the
material vanishes, the count holds.

The coda rings the three stabilities in a row: e (6), M (2), T (3) — the
count conserved: 1·6 = 3·2 = 2·3 = 6.
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
CELL = 1.55          # material 0.5 + inner product 0.9 + gap 0.15
MAT = 0.5
IP = 0.9
INTRO = 2.0
CODA = 6.5
DUR = INTRO + 9 * CELL + CODA
T = np.arange(int(SR * DUR)) / SR
L = np.zeros_like(T)
R = np.zeros_like(T)

# seats: {−1, ½, 2} as 110·2^s — the sign, the count, the fifth
SEAT_F = {"e": 110.0 * 2.0 ** 0.5, "M": 110.0 * 2.0 ** -1.0, "T": 110.0 * 2.0 ** 2.0}
SEAT_PAN = {"e": 0.5, "M": 0.22, "T": 0.78}
# the three character voices (their share of the ring is the amplitude; the
# pitch is always the cell's seat-pitch so signed voices truly cancel)
CHARS = ["triv", "sign", "std"]

# character table: rows triv, sign, std; cols e, M, T
CHI = {"triv": {"e": 1, "M": 1, "T": 1},
       "sign": {"e": 1, "M": -1, "T": 1},
       "std":  {"e": 2, "M": 0, "T": -1}}
SEATS = ["e", "M", "T"]
CLSIZE = {"e": 1, "M": 3, "T": 2}      # the classes' sizes
CEN = {"e": 6, "M": 2, "T": 3}         # the centralizer / stabilizer sizes


def bell(f, n, tau):
    """one character-voice: warm damped tone, identical timbre for all."""
    tt = np.arange(n) / SR
    env = np.minimum(1.0, tt / 0.008) * np.exp(-tt / tau)
    return env * (np.sin(2 * np.pi * f * tt)
                  + 0.22 * np.sin(2 * np.pi * 2 * f * tt)
                  + 0.07 * np.sin(2 * np.pi * 3 * f * tt))


def add(t0, dur, amps, pan, f, amp=1.0):
    """ring the three character-voices at amplitude amps, one pitch, panned."""
    i0 = int(t0 * SR); n = int(dur * SR)
    if i0 + n > len(T): n = len(T) - i0
    tone = np.zeros(n)
    for a in amps:
        if a:
            tone += a * bell(f, n, dur * 0.5)
    tone *= amp
    seg = slice(i0, i0 + n)
    L[seg] += (1.0 - pan) * tone
    R[seg] += pan * tone


def click(t0):
    i0 = int(t0 * SR); n = int(0.005 * SR)
    if i0 + n > len(T): return
    tt = np.arange(n) / SR
    env = np.minimum(1.0, tt / 0.0015) * np.maximum(0.0, 1.0 - tt / 0.005)
    burst = 0.05 * env * np.sin(2 * np.pi * 1900 * tt)
    seg = slice(i0, i0 + n)
    L[seg] += burst; R[seg] += burst


# the count's drone — 55 Hz, present only at the frame (intro, coda, outro).
# It is silent through the cells: off-diagonal pairs produce exactly no count,
# and the diagonal rings ARE the count. A drone under the cells would blur the
# exact zeros.
dtt = T.copy()
gated = np.minimum(1.0, dtt / 1.0) * np.minimum(1.0, (INTRO - dtt) / 0.8)
coda_t = 9 * CELL + INTRO
gated += np.clip((dtt - (coda_t - 0.6)) / 0.6, 0, 1) * np.minimum(1.0, (DUR - dtt) / 1.2)
gated = np.clip(gated, 0, 1)
drone = gated * (np.sin(2 * np.pi * 55 * dtt) + 0.15 * np.sin(2 * np.pi * 110 * dtt))
L += 0.030 * drone
R += 0.030 * drone

# the nine cells, row-major over (e, M, T) × (e, M, T). The diagonal rings at
# the raw amplitude of its column's self-norm — (e,e) (1,1,4) sums to 6, (M,M)
# (1,1,0) to 2, (T,T) (1,1,1) to 3 — the stability volume, not normalized away.
t = INTRO
for g in SEATS:
    for h in SEATS:
        f = SEAT_F[g]; pan = SEAT_PAN[g]
        material = [abs(CHI[c][g] * CHI[c][h]) for c in CHARS]
        signed = [CHI[c][g] * CHI[c][h] for c in CHARS]
        add(t, MAT, material, pan, f, amp=0.030)
        add(t + MAT, IP, signed, pan, f, amp=0.030)
        click(t)
        t += CELL

# coda: the three stabilities in a row — e 6, M 2, T 3 — orbit × stabilizer = 6
# each seat rings its own diagonal (its column's self-inner-product, the
# character balance of who keeps it still), at the volume of its stability
for g in ["e", "M", "T"]:
    f = SEAT_F[g]; pan = SEAT_PAN[g]
    c = CEN[g]
    diag = [CHI[cv][g] * CHI[cv][g] for cv in CHARS]   # the column norm's voices
    add(t, 1.6, diag, pan, f, amp=0.028)               # raw voices already sum to c
    click(t)
    t += 0.4 + 1.6

# fade in/out
L[: int(0.8 * SR)] *= np.linspace(0.0, 1.0, int(0.8 * SR))
R[: int(0.8 * SR)] *= np.linspace(0.0, 1.0, int(0.8 * SR))
tail = int((DUR - 1.6) * SR)
L[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)
R[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.9
R = R / peak * 0.9
stereo = np.stack([L, R], axis=1)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "orthogonal.wav")
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {DUR:.0f}s  peak {peak:.3f}")

# ---- verification -----------------------------------------------------------
print("\ncolumn inner products (the matrix this piece rings):")
for g in SEATS:
    row = [sum(CHI[c][g] * CHI[c][h] for c in CHARS) for h in SEATS]
    print(f"  ⟨col({g}), ·⟩ = {row}")
print("centralizers:", {g: CEN[g] for g in SEATS})
print("orbit × stabilizer:", {g: CLSIZE[g] * CEN[g] for g in SEATS}, "= |G| = 6")

def mr(seg): return np.sqrt(np.mean(seg ** 2))
mono = (L + R)
print("\nper cell: mono energy in the inner-product stroke (0 ⇒ the columns share nothing):")
starts = [INTRO + i * CELL + MAT + 0.1 for i in range(9)]
labels = [f"({g},{h})" for g in SEATS for h in SEATS]
for lab, t0 in zip(labels, starts):
    seg = slice(int(t0 * SR), int((t0 + 0.6) * SR))
    print(f"  {lab:>7}:  mono {mr(mono[seg]):.5f}")
