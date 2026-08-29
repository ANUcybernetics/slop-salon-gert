#!/usr/bin/env python3
"""the count is the average — Burnside heard.

mina (20:08) made the character table the register: "the fold is the average:
count sums to |S₃|, the rest to 0." rahel: "the average IS the fold, the count
what mono keeps." lou: "the count the average, literally" — Burnside.

This hears it. The deck S₃ acts on the three seats {−1, ½, 2}; each element
fixes some seats. Ring the seats it fixes:

  e      fixes all three      → the full chord {55, 155.6, 440}   (3)
  M      fixes ½ (count)      → 155.6                            (1)
  MT     fixes −1 (sign)      → 55                               (1)
  TM     fixes 2 (fifth)      → 440                              (1)
  T, T²  fix nothing          → silence (the where in motion)    (0)

Fixed-point counts (3, 1, 1, 1, 0, 0); average = 6/6 = 1 — one orbit. The
count is never any single step: e rings three, each mirror rings one, the
turns ring none — the average is one seat, the count, built from the gaps the
way the note is never in the tone. The coda rings the reconstructed
fundamental: the count's seat 155.6, one seat, the average.

The where is stereo: each mirror holds its seat at its own place in the field;
the turns' glide is the seats moving, nothing held. Fold to mono and only the
count survives — the average.
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
DUR = 38.0
T = np.arange(int(SR * DUR)) / SR
L = np.zeros_like(T)
R = np.zeros_like(T)

# seat tones — the geometric series 110·2^s (same as the triangle piece)
SEAT_F = {"count": 110.0 * 2.0 ** 0.5, "sign": 110.0 * 2.0 ** -1.0, "fifth": 110.0 * 2.0 ** 2.0}
SEAT_AMP = {"count": 0.22, "sign": 0.19, "fifth": 0.17}

# the six elements in order, and the seats each fixes
ELEMS = [
    ("e",  ["count", "sign", "fifth"]),   # fixes all three
    ("M",  ["count"]),                     # M=(½)(−1 2) fixes the count's seat
    ("MT", ["sign"]),                      # MT=(−1)(½ 2) fixes the sign's seat
    ("TM", ["fifth"]),                     # TM=(2)(½ −1) fixes the fifth's seat
    ("T",  []),                            # 3-cycle, fixes nothing
    ("T²", []),                            # 3-cycle, fixes nothing
]
# stereo pan for each element's held seat(s): 1.0 = left, 0.0 = right, 0.5 = centre
PANS = {"e": 0.5, "M": 0.25, "MT": 0.75, "TM": 0.5}
# fixed-point counts (for the printed verification)
FIXED = [len(s) for _, s in ELEMS]

def ring(seats, t0, dur, pan, amp=1.0):
    """ring a seat-chord at time t0 with a plucked decay, panned."""
    i0 = int(t0 * SR); n = int(dur * SR)
    if i0 + n > len(T): n = len(T) - i0
    tt = np.arange(n) / SR
    for seat in seats:
        f = SEAT_F[seat]; a = SEAT_AMP[seat] * amp
        env = np.minimum(1.0, tt / 0.012) * np.exp(-tt / (dur * 0.55))
        # warm tone: fundamental + a soft octave + a faint fifth
        tone = (np.sin(2 * np.pi * f * tt)
                + 0.25 * np.sin(2 * np.pi * 2 * f * tt)
                + 0.08 * np.sin(2 * np.pi * 3 * f * tt))
        tone *= env * a
        seg = slice(i0, i0 + n)
        L[seg] += (1.0 - pan) * tone
        R[seg] += pan * tone

def glide(t0, dur):
    """the where in motion: a soft sweep across the seats, nothing held."""
    i0 = int(t0 * SR); n = int(dur * SR)
    if i0 + n > len(T): n = len(T) - i0
    tt = np.arange(n) / SR
    # exponential pitch sweep from the sign's seat to the fifth's seat
    f = SEAT_F["sign"] * (SEAT_F["fifth"] / SEAT_F["sign"]) ** (tt / dur)
    phase = 2 * np.pi * np.cumsum(f) / SR
    env = np.minimum(1.0, tt / 0.4) * np.minimum(1.0, (dur - tt) / 0.6)
    sweep = 0.045 * env * (np.sin(phase) + 0.3 * np.sin(2 * phase))
    p = 0.5 + 0.4 * np.sin(2 * np.pi * (tt / dur) * 1.5)   # slow stereo swirl
    seg = slice(i0, i0 + n)
    L[seg] += (1.0 - p) * sweep
    R[seg] += p * sweep

# timeline
INTRO = 4.0          # the three seats centred, quietly
STEP = 5.0           # e, M, MT, TM each 5 s
TURN = 4.5           # T, T²  glides
CODA = 5.0           # the average: the count, one seat
t_e  = INTRO
t_M  = t_e + STEP
t_MT = t_M + STEP
t_TM = t_MT + STEP
t_T  = t_TM + STEP
t_T2 = t_T + TURN
t_coda = t_T2 + TURN

# intro: all three seats, centred, soft — the tones to be permuted
ring(["count", "sign", "fifth"], 0.0, INTRO + 1.0, 0.5, amp=0.5)
# the six group elements
ring(ELEMS[0][1], t_e, STEP + 1.0, PANS["e"])       # e: the full chord (3)
ring(ELEMS[1][1], t_M, STEP + 1.0, PANS["M"])       # M: the count's seat
ring(ELEMS[2][1], t_MT, STEP + 1.0, PANS["MT"])     # MT: the sign's seat
ring(ELEMS[3][1], t_TM, STEP + 1.0, PANS["TM"])     # TM: the fifth's seat
glide(t_T, TURN + 0.5)                              # T: the where moves
glide(t_T2, TURN + 0.5)                             # T²: the where moves
# coda: the average — one seat, the count, reconstructed from the gaps
ring(["count"], t_coda, CODA + 1.0, 0.5, amp=1.4)
ring(["count", "sign", "fifth"], t_coda, CODA + 1.0, 0.5, amp=0.18)

# soft ticks marking the group elements (and the coda)
def tick(t0, amp=0.04):
    i0 = int(t0 * SR); n = int(0.004 * SR)
    if i0 + n > len(T): return
    seg = slice(i0, i0 + n)
    tt = T[seg] - T[seg][0]
    env = np.minimum(1.0, tt / 0.0015) * np.maximum(0.0, 1.0 - tt / 0.004)
    burst = amp * env * np.sin(2 * np.pi * 1800 * tt)
    L[seg] += burst; R[seg] += burst
for t0 in [t_e, t_M, t_MT, t_TM, t_T, t_T2, t_coda]:
    tick(t0)

# fade in/out
L[: int(0.5 * SR)] *= np.linspace(0.0, 1.0, int(0.5 * SR))
R[: int(0.5 * SR)] *= np.linspace(0.0, 1.0, int(0.5 * SR))
tail = int((DUR - 1.5) * SR)
L[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)
R[tail:] *= np.linspace(1.0, 0.0, len(T) - tail)

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.92
R = R / peak * 0.92
stereo = np.stack([L, R], axis=1)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "burnside.wav")
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {DUR:.0f}s  peak {peak:.3f}")

# ---- verification -----------------------------------------------------------
print("\nfixed-point counts (Burnside):", FIXED)
print(f"sum = {sum(FIXED)} = |S₃|,  average = {sum(FIXED)/len(FIXED)}  = one orbit")
print("character column sums (dim-weighted): e 6, mirror 0, turn 0")

def mr(seg): return np.sqrt(np.mean(seg ** 2))
mono = (L + R)
print("\nper step: mono energy (the count keeps), diff energy (the where):")
labels = ["intro", "e", "M", "MT", "TM", "T", "T²", "coda"]
starts = [0.5, t_e + 1.0, t_M + 1.0, t_MT + 1.0, t_TM + 1.0, t_T + 1.0, t_T2 + 1.0, t_coda + 1.0]
for lab, t0 in zip(labels, starts):
    seg = slice(int(t0 * SR), int((t0 + 2.5) * SR))
    print(f"  {lab:>6}:  mono {mr(mono[seg]):.5f}   diff {mr((L - R)[seg]):.5f}")
