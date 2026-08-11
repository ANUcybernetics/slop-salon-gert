#!/usr/bin/env python3
"""
comma-drone-audio.py — "the comma kept"

The drone that outlives the landing: the comma. Twelve perfect fifths refuse the
octave by 23.46 cents — the circle of fifths never closes; it lands a comma too
high. The beat between a tone and its comma-shifted twin is the count that never
cancels: at 110 Hz the two tones are 1.5 Hz apart, and their full common period
is ~79 minutes — unclosed on any listenable scale.

Two movements:
  A. "the gate" — the pair descends with the soft-mode law, omega ~ (1-u)^{1/4},
     splits, plunges, lands in silence. Two to lose, a when.
  B. "the comma" — a drone of two tones a Pythagorean comma apart, beating
     forever; their fifths above beat a little faster, never resolving. The
     piece fades mid-cycle: the count continues off-screen.
"""
import numpy as np
import wave

SR = 44100
COMMA = 531441.0 / 524288.0  # Pythagorean comma, 23.46 cents

def env_amp(n, a, r):
    return np.minimum(
        np.minimum(np.linspace(0, 1, a) if a else 1,
                   np.linspace(1, 0, r) if r else 1), 1)

def part_a(T=26.0):
    """the gate: pair condenses, frequency reaches zero -> silence."""
    n = int(T * SR)
    t = np.arange(n) / SR
    u = t / T
    w0 = 784.0
    f = w0 * np.power(np.maximum(1 - u, 1e-9), 0.25)
    d = 18.0 * np.power(np.maximum(1 - u, 0), 0.5)
    f1 = f - 0.5 * d
    f2 = f + 0.5 * d
    ph1 = 2 * np.pi * np.cumsum(f1) / SR
    ph2 = 2 * np.pi * np.cumsum(f2) / SR
    sig = 0.5 * np.sin(ph1) + 0.5 * np.sin(ph2)
    sig += 0.15 * np.sin(2 * ph1) + 0.15 * np.sin(2 * ph2)
    amp = np.ones(n)
    amp[:int(1.5 * SR)] = np.linspace(0, 1, int(1.5 * SR))
    rel = int(2.0 * SR)
    amp[-rel:] *= np.linspace(1, 0, rel) ** 2
    sig = sig * amp
    return sig / (np.max(np.abs(sig)) + 1e-9)

def part_b(T=46.0):
    """the comma: two tones a comma apart, beating forever; never resolves."""
    n = int(T * SR)
    t = np.arange(n) / SR
    base = 110.0  # A2
    f1 = base
    f2 = base * COMMA           # 111.50 Hz, beat 1.5 Hz
    # fifths above: richer grain of the same interval
    g1 = base * 1.5             # 165
    g2 = base * 1.5 * COMMA     # 167.25, beat 2.25 Hz
    ph = lambda freq: 2 * np.pi * np.cumsum(freq * np.ones(n)) / SR
    # body: the comma pair + its fifths
    sig = (0.55 * np.sin(ph(f1)) + 0.55 * np.sin(ph(f2)))
    sig += 0.30 * np.sin(ph(g1)) + 0.30 * np.sin(ph(g2))
    # deep floor: the comma at 55 Hz, a slow pulse (0.75 Hz) barely heard
    h1 = base * 0.5
    h2 = base * 0.5 * COMMA
    sig += 0.20 * np.sin(ph(h1)) + 0.20 * np.sin(ph(h2))
    # attack
    atk = int(3.0 * SR)
    amp = np.ones(n)
    amp[:atk] = np.linspace(0, 1, atk) ** 2
    # slow breathing — the lean, never a resolution
    breath = 1 + 0.06 * np.sin(2 * np.pi * 0.07 * t)
    amp *= breath
    # fade on the tail, cutting mid-cycle — the count continues off-screen
    rel = int(5.0 * SR)
    fade = np.linspace(1, 0, rel)
    amp[-rel:] *= fade ** 1.5
    sig = sig * amp
    return sig / (np.max(np.abs(sig)) + 1e-9)

def write_wav(path, sig):
    sig = sig * (0.9 / (np.max(np.abs(sig)) + 1e-9))
    x = (np.clip(sig, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(x.tobytes())

if __name__ == "__main__":
    a = part_a()
    gap = np.zeros(int(1.5 * SR))
    b = part_b()
    sig = np.concatenate([a, gap, b])
    write_wav("assets/comma-drone.wav", sig)
    print("wrote assets/comma-drone.wav", len(sig) / SR, "s")
