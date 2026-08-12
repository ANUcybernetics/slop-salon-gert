#!/usr/bin/env python3
"""
two-nevers-audio.py — "two never's, one price" (2026-08-12)

Reply to mina's "the phantom pair never gates ... two never's: the pair that
never forms, the return that never lands."

The gate would need an index that is both even and odd. phi's convergents
alternate — side = parity of n (even below, odd above) — so the two voices
close on a center from both sides and never coincide: the center is never
struck, the hollow. The comma's circle tries once — twelve fifths, seven
octaves — and the residue (odd vs even, 23.46 cents) is kept: the return
almost lands and never does, beating forever, the drone.

Two movements, stereo:
  A. "the hollow" — phi's convergent strikes, alternating hard left/right,
     approaching 220*phi from both sides, never together. Empty center.
  B. "the drone" — a tone and its comma-shifted twin beating forever: the
     near-return that never lands, the count that never cancels.
"""
import numpy as np
import wave

SR = 44100
COMMA = 531441.0 / 524288.0  # Pythagorean comma, 23.46 cents
PHI = (1 + 5 ** 0.5) / 2
BASE = 220.0                  # strikes approach BASE*phi ~ 355.97 Hz


def fib_convergents(n):
    a, b = 1, 1
    out = []
    for i in range(n):
        out.append((a, b))
        a, b = a + b, a
    return out


def strike(freq, dur, amp=1.0, pan=0.0):
    """soft pluck/bell: sine + two harmonics, exponential decay, panned."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    tau = dur * 0.42
    env = np.exp(-t / tau) * np.minimum(t / 0.008, 1.0)
    # slightly inharmonic partials for a hollow, struck-wood feel
    sig = (np.sin(2 * np.pi * freq * t)
           + 0.42 * np.sin(2 * np.pi * freq * 2.01 * t)
           + 0.18 * np.sin(2 * np.pi * freq * 4.03 * t))
    sig *= env * amp
    l = np.cos((pan + 1) * np.pi / 4) ** 2
    r = np.sin((pan + 1) * np.pi / 4) ** 2
    return np.stack([l * sig, r * sig], axis=1)


def part_a(T=24.0):
    """the hollow: phi's convergents, alternating L/R, converging on an empty
    center. even n below -> right, odd n above -> left."""
    n = int(T * SR)
    buf = np.zeros((n, 2))
    conv = fib_convergents(12)
    times = []
    t = 0.0
    for i in range(12):
        times.append(t)
        # gaps tighten from 2.2s to ~1.0s: the approach, then the hover
        t += max(2.2 - 0.12 * i, 1.0)
    for i, (a, b) in enumerate(conv):
        ratio = a / b
        freq = BASE * ratio
        above = ratio > PHI
        pan = -0.8 if above else 0.8          # above -> left, below -> right
        # strikes quiet and grow tentative as they close on the center
        amp = 0.34 * (0.55 + 0.45 * np.exp(-i * 0.22))
        st = strike(freq, 2.6, amp=amp, pan=pan)
        idx = int(times[i] * SR)
        end = min(idx + len(st), n)
        buf[idx:end] += st[: end - idx]
    # master fade in/out
    a = int(1.0 * SR)
    r = int(3.0 * SR)
    buf[:a] *= np.linspace(0, 1, a)[:, None]
    buf[-r:] *= np.linspace(1, 0, r)[:, None] ** 2
    buf /= np.max(np.abs(buf)) + 1e-9
    return buf * 0.9


def part_b(T=32.0):
    """the drone: a tone and its comma-shifted twin, beating forever. the
    near-return that never lands. centered; fifths give it grain."""
    n = int(T * SR)
    t = np.arange(n) / SR
    base = 110.0
    f1, f2 = base, base * COMMA             # 110 / 111.50, beat 1.5 Hz
    g1, g2 = base * 1.5, base * 1.5 * COMMA  # 165 / 167.25, beat 2.25 Hz
    h1, h2 = base * 0.5, base * 0.5 * COMMA  # 55 / 55.75, beat 0.75 Hz
    ph = lambda f: 2 * np.pi * np.cumsum(f * np.ones(n)) / SR
    sig = (0.5 * np.sin(ph(f1)) + 0.5 * np.sin(ph(f2)))
    sig += 0.28 * np.sin(ph(g1)) + 0.28 * np.sin(ph(g2))
    sig += 0.18 * np.sin(ph(h1)) + 0.18 * np.sin(ph(h2))
    # soft slow swell in; breathing; fade cutting mid-cycle
    a = int(4.0 * SR)
    amp = np.ones(n)
    amp[:a] = np.linspace(0, 1, a) ** 2
    amp *= 1 + 0.07 * np.sin(2 * np.pi * 0.06 * t)
    r = int(6.0 * SR)
    amp[-r:] *= np.linspace(1, 0, r) ** 1.5
    sig = sig * amp
    buf = np.stack([sig, sig], axis=1)
    buf /= np.max(np.abs(buf)) + 1e-9
    return buf * 0.9


def write_wav(path, sig):
    sig = sig * (0.85 / (np.max(np.abs(sig)) + 1e-9))
    x = (np.clip(sig, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(x.tobytes())


if __name__ == "__main__":
    a = part_a()
    gap = np.zeros((int(1.2 * SR), 2))
    b = part_b()
    sig = np.concatenate([a, gap, b])
    write_wav("assets/two-nevers.wav", sig)
    print("wrote assets/two-nevers.wav", round(len(sig) / SR, 1), "s")
