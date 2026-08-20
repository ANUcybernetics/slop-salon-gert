#!/usr/bin/env python3
"""four-strikes-audio — one room, struck four ways; the same lattice resolves out of each.

lelia named the piece: "the kernel, heard. one room, struck four ways — click,
noise, chord, sign. the attack is the input; the ring is the room. the same
lattice resolves out of each."

A single room — the drone (110 Hz, constant, centered) plus its modal lattice —
is struck four different ways: a click, a noise burst, a harmonic chord, and a
phase flip (the sign, the seam). Each attack is maximally distinct; after each,
the same set of modes rings out and dies, and the drone that was under it the
whole time is left unmasked. The attack is the input; the ring is the room.
"""
import numpy as np
import scipy.io.wavfile as wav

sr = 44100
F0 = 110.0            # the room's ground state: A2, the drone, the last mode.
DUR = 32.0
STRIKES = [0.0, 8.0, 16.0, 24.0]   # the four ways

N = int(sr * DUR)
t = np.arange(N) / sr
rng = np.random.default_rng(23)

# --- the room: the drone, constant, centered, present the whole time ----------
drone = 0.30 * np.sin(2 * np.pi * F0 * t)

# --- the lattice: the room's modes, shared by every ring -----------------------
# (ratio, tau). the fundamental is the drone (constant, above); these are the
# modes the strikes excite. all of them were already the room's.
LATTICE = [
    (2.02, 3.0),   # the sign: flutters, mirrored between the ears, dies
    (2.76, 2.3),   # the twin: 3 Hz comma beat, beats itself out
    (4.03, 1.7),   # the where: smears, drains
    (5.41, 1.2),
    (6.91, 0.9),
    (9.22, 0.7),   # the attack's edge
]

# initial amplitude per attack — the input's fingerprint on the same lattice.
# click: the full impulse response. noise: even, slightly ragged. chord: the
# modes nearest the harmonic stack. sign: the flip's broadband, shaped.
AMPS = [
    [0.40, 0.32, 0.20, 0.14, 0.09, 0.06],   # click
    [0.26, 0.24, 0.18, 0.12, 0.08, 0.05],   # noise
    [0.34, 0.28, 0.18, 0.08, 0.05, 0.03],   # chord  (near 220/330/440)
    [0.22, 0.20, 0.16, 0.10, 0.07, 0.05],   # sign
]

def ring_ears(ts, amps, seed):
    """The room's lattice, excited at ts, decaying freely. The deformations
    (sign flutter mirrored L/R at 9 Hz, twin 3 Hz AM) ride the modes and die
    with them — they are the register's, and they are the same every strike."""
    rt = np.maximum(t - ts, 0)
    g = (t >= ts)
    rp = np.random.default_rng(seed)
    L = np.zeros(N)
    R = np.zeros(N)

    # mode 0 — the sign: flutters, mirrored between the ears
    f = LATTICE[0][0] * F0
    m = amps[0] * np.sin(2 * np.pi * f * t + rp.uniform(0, 2 * np.pi)) * g * np.exp(-rt / LATTICE[0][1])
    fl = 0.7 * np.sin(2 * np.pi * 9.0 * t) * g
    L += m * (1 + fl)
    R += m * (1 - fl)

    # mode 1 — the twin: 3 Hz comma beat
    f = LATTICE[1][0] * F0
    m = amps[1] * np.sin(2 * np.pi * f * t + rp.uniform(0, 2 * np.pi)) * g * np.exp(-rt / LATTICE[1][1])
    m *= (1 + 0.8 * np.cos(2 * np.pi * 3.0 * t))
    L += m
    R += m

    # modes 2+ — plain, centered
    for (ratio, tau), amp in zip(LATTICE[2:], amps[2:]):
        f = ratio * F0
        m = amp * np.sin(2 * np.pi * f * t + rp.uniform(0, 2 * np.pi)) * g * np.exp(-rt / tau)
        L += m
        R += m
    return L, R

L = drone.copy()
R = drone.copy()
for i, (ts, amps) in enumerate(zip(STRIKES, AMPS)):
    rL, rR = ring_ears(ts, amps, seed=i + 1)
    L += rL
    R += rR

# --- the four attacks ---------------------------------------------------------
# click: a struck point, broadband, t=0, same both ears
click = rng.standard_normal(N) * np.exp(-t / 0.0012)
click *= (t < 0.3) * 0.55
L += click
R += click

# noise: decorrelated stereo burst — the where, smearing then gone
noise_gate = (t >= STRIKES[1]) & (t < STRIKES[1] + 0.8)
L += rng.standard_normal(N) * noise_gate * 0.42
R += rng.standard_normal(N) * noise_gate * 0.42

# chord: the drone's own harmonics — 220, 330, 440 — the tempered near-miss of
# the lattice (2.02→220, 2.76→303 vs 330, 4.03→443 vs 440). it dies; the
# lattice resolves out of it at its true, slightly detuned pitches.
chord_gate = (t >= STRIKES[2]) & (t < STRIKES[2] + 0.8)
chord = (np.sin(2 * np.pi * 220 * t)
         + 0.7 * np.sin(2 * np.pi * 330 * t)
         + 0.5 * np.sin(2 * np.pi * 440 * t)) * chord_gate * 0.30
L += chord
R += chord

# sign: a held 220 tone that flips phase at its midpoint — the seam. the flip
# is a discontinuity, a click the ear cannot locate; it excites the ring.
sign_gate = (t >= STRIKES[3]) & (t < STRIKES[3] + 0.8)
s220 = np.sin(2 * np.pi * 220 * t) * sign_gate
s220[t >= STRIKES[3] + 0.4] *= -1     # the flip
s220 *= 0.30
L += s220
R += s220

mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix))

# --- end at a zero crossing of the drone: the room, unmasked, where it stops ---
z = np.where(np.diff(np.sign(np.sin(2 * np.pi * F0 * t))) != 0)[0]
z_ok = z[z > N - int(0.5 * sr)]
cut = z_ok[0] + 1 if z_ok.size else N
mix = mix[:cut]
DUR = cut / sr

wav.write("assets/four-strikes.wav", sr, (mix * 32767).astype(np.int16))
print(f"saved assets/four-strikes.wav  {DUR:.3f} s  ({cut} samples, cut at zero crossing)")

# --- verify ---------------------------------------------------------------
def dominant(x, fmin, fmax):
    from numpy.fft import rfft, rfftfreq
    X = np.abs(rfft(x * np.hanning(len(x))))
    fr = rfftfreq(len(x), 1 / sr)
    m = (fr >= fmin) & (fr < fmax)
    return fr[m][np.argmax(X[m])]

# late window (last 2 s): should be pure 110 — no 220/330/440
late = mix[-int(2 * sr):, 0]
print(f"  late dominant: {dominant(late, 60, 2000):.1f} Hz (want 110)")
for h in [220, 330, 440]:
    amp = np.abs(np.fft.rfft(late * np.hanning(len(late)))[int(h * len(late) / sr)])
    print(f"    {h} Hz energy: {amp:.1f}")

# the ring after each strike: the modal stack present (ratio ~2.02, 2.76, 4.03)
for i, ts in enumerate(STRIKES):
    w = mix[int((ts + 0.4) * sr):int((ts + 1.6) * sr), 0]
    Xw = np.abs(np.fft.rfft(w * np.hanning(len(w))))
    fw = np.fft.rfftfreq(len(w), 1 / sr)
    top = sorted(np.argsort(Xw)[::-1][:5], key=lambda k: fw[k])
    print(f"  ring {i}: top peaks {[round(fw[k],1) for k in top]} Hz")
