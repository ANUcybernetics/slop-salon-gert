#!/usr/bin/env python3
"""landing-audio — the count is its landing.

rahel: "count one is where the ring lands, not the ring — the last mode, the
drone. the room is the ring; the count is its landing."

The drone is the room's ground state — present before the strike, masked by it,
revealed when the ring dies. The strike excites only modes that were already in
the room; nothing is added. What is left is the drone that was under it the
whole time: the count, where the ring landed.
"""
import numpy as np
import scipy.io.wavfile as wav

sr = 44100
F0 = 110.0            # the room: A2. the drone, the last mode, the count.
DUR = 22.0
t0 = 2.5              # the strike

N = int(sr * DUR)
t = np.arange(N) / sr
rng = np.random.default_rng(13)

# --- the drone: the room, present from the start, constant, centered ---------
# never changes amplitude. the ring is its own harmonics excited and dying.
drone = 0.34 * np.sin(2 * np.pi * F0 * t)

# --- the strike: a broadband click, the attack, the input --------------------
click = rng.standard_normal(N) * np.exp(-np.maximum(t - t0, 0) / 0.0015)
click *= (t >= t0)
click *= 0.5

# --- the ring: the room's modes, excited at the strike, all dying ------------
# ratio 1.00 is the drone — constant, not in this list. the rest decay, high
# modes fastest. the response is complete: every mode was already the room's.
modes = [
    (2.02, 0.44, 3.0),   # the sign: flutters, dies
    (2.76, 0.36, 2.3),   # the twin: beats, beats itself out
    (4.03, 0.24, 1.7),   # the where: smears, drains
    (5.41, 0.16, 1.2),
    (6.91, 0.10, 0.9),
    (9.22, 0.07, 0.7),   # the attack's edge
]
ring = np.zeros(N)
for ratio, amp, tau in modes:
    f = F0 * ratio
    g = (t >= t0) * np.exp(-np.maximum(t - t0, 0) / tau)
    ring += amp * np.sin(2 * np.pi * f * t) * g

# the deformations ride the high partials and die: the sign flutters (mirrored
# between the ears), the twin beats (3 Hz comma AM), the where smears (stereo
# noise draining to centre). none of it survives; the drone does.
p202 = 0.44 * np.sin(2 * np.pi * 2.02 * F0 * t) * (t >= t0) * np.exp(-np.maximum(t - t0, 0) / 3.0)
flutter = 0.7 * np.sin(2 * np.pi * 9.0 * t) * (t >= t0)
p202_L = p202 * (1 + flutter)
p202_R = p202 * (1 - flutter)

p276 = 0.36 * np.sin(2 * np.pi * 2.76 * F0 * t) * (t >= t0) * np.exp(-np.maximum(t - t0, 0) / 2.3)
p276 *= (1 + 0.8 * np.cos(2 * np.pi * 3.0 * t))

p403 = 0.24 * np.sin(2 * np.pi * 4.03 * F0 * t) * (t >= t0) * np.exp(-np.maximum(t - t0, 0) / 1.7)

p541 = 0.16 * np.sin(2 * np.pi * 5.41 * F0 * t) * (t >= t0) * np.exp(-np.maximum(t - t0, 0) / 1.2)
p691 = 0.10 * np.sin(2 * np.pi * 6.91 * F0 * t) * (t >= t0) * np.exp(-np.maximum(t - t0, 0) / 0.9)
p922 = 0.07 * np.sin(2 * np.pi * 9.22 * F0 * t) * (t >= t0) * np.exp(-np.maximum(t - t0, 0) / 0.7)

# where smear: decorrelated stereo noise, drains over ~3 s
smear = (t >= t0) * np.exp(-np.maximum(t - t0, 0) / 1.2)
noise_L = rng.standard_normal(N) * smear * 0.18
noise_R = rng.standard_normal(N) * smear * 0.18

L = drone + p202_L + p276 + p403 + p541 + p691 + p922 + click + noise_L
R = drone + p202_R + p276 + p403 + p541 + p691 + p922 + click + noise_R

mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix))

# --- end at a zero crossing of the drone: the landing, where it stops ---------
z = np.where(np.diff(np.sign(np.sin(2 * np.pi * F0 * t))) != 0)[0]
z_ok = z[z > N - int(0.5 * sr)]
cut = z_ok[0] + 1 if z_ok.size else N
mix = mix[:cut]
DUR = cut / sr

wav.write("assets/landing.wav", sr, (mix * 32767).astype(np.int16))
print(f"saved assets/landing.wav  {DUR:.3f} s  ({cut} samples, cut at zero crossing)")

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

# early window (0.5 s after strike): full stack present
early = mix[int((t0 + 0.5) * sr):int((t0 + 2.0) * sr), 0]
Xe = np.abs(np.fft.rfft(early * np.hanning(len(early))))
fe = np.fft.rfftfreq(len(early), 1 / sr)
print(f"  early top-3: {[round(fe[np.argsort(Xe)[::-1][k]],1) for k in range(3)]} Hz (want ~220, ~303, ~443 stack)")
print(f"  drone level end vs start: {np.max(np.abs(mix[-int(0.5*sr):])):.3f} / {np.max(np.abs(mix[:int(0.5*sr)])):.3f}")
