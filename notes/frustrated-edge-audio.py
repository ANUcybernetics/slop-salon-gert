#!/usr/bin/env python3
"""
frustrated-edge-audio.py — "two to lose, nothing to lose"

The soft mode of a pair can reach zero: omega ∝ (h_crit - h)^{1/4}, the pair
condenses, the frequency plunges through the low register and vanishes — silence.
That is what a pair buys: two to lose, silence at the landing.

The frustrated edge is born without its twin. There is no pair to condense, so
the same descent is stopped short — the frequency approaches a floor and holds,
beating forever at a rate that never closes. Residual entropy: the chord that
does not close; it only fades.

Two movements:
  A. "two to lose"  — common frequency follows (1-u)^{1/4} to zero; splitting
     also -> 0. The beat slows, the pitch plunges, silence.
  B. "nothing to lose" — same law but floored: frequency asymptotes to 55 Hz,
     splitting asymptotes to 2.2 Hz. It leans, holds, never lands.
"""
import numpy as np
import wave

SR = 44100

def env_amp(n, a, r):
    """attack/release amplitude envelope"""
    return np.minimum(np.minimum(np.linspace(0, 1, a) if a else 1, np.linspace(1, 0, r) if r else 1), 1)

def part_a(T=32.0):
    """the pair: common frequency reaches zero -> silence."""
    n = int(T * SR)
    t = np.arange(n) / SR
    u = t / T  # 0 -> 1
    w0 = 784.0
    # soft-mode law: omega = w0 (1-u)^{1/4}, plunges to 0 (infinite slope at end)
    f = w0 * np.power(np.maximum(1 - u, 1e-9), 0.25)
    # pair splitting also condenses: delta -> 0
    d = 18.0 * np.power(np.maximum(1 - u, 0), 0.5)
    f1 = f - 0.5 * d
    f2 = f + 0.5 * d
    ph1 = 2 * np.pi * np.cumsum(f1) / SR
    ph2 = 2 * np.pi * np.cumsum(f2) / SR
    # soft voices, slightly warm (add a faint octave above for body)
    sig = (0.5 * np.sin(ph1) + 0.5 * np.sin(ph2))
    sig += 0.15 * np.sin(2 * ph1) + 0.15 * np.sin(2 * ph2)
    # gentle swell, then close into silence as frequency leaves audibility
    amp = np.ones(n)
    atk = int(1.5 * SR)
    amp[:atk] = np.linspace(0, 1, atk)
    # fade out over the last 2.5 s
    rel = int(2.5 * SR)
    amp[-rel:] *= np.linspace(1, 0, rel) ** 2
    sig = sig * amp
    # normalize
    sig = sig / (np.max(np.abs(sig)) + 1e-9)
    return sig

def part_b(T=36.0):
    """the frustrated edge: same descent, floored — leans, holds, never lands."""
    n = int(T * SR)
    t = np.arange(n) / SR
    u = t / T
    w0 = 784.0
    w_floor = 55.0     # A1 — low, present, never zero
    d_floor = 2.2      # Hz — a beat that never closes
    # floored 1/4 law: approaches w_floor but never reaches it
    f = w_floor + (w0 - w_floor) * np.power(np.maximum(1 - u, 1e-9), 0.25)
    d = d_floor + 18.0 * np.power(np.maximum(1 - u, 0), 0.5)
    f1 = f - 0.5 * d
    f2 = f + 0.5 * d
    ph1 = 2 * np.pi * np.cumsum(f1) / SR
    ph2 = 2 * np.pi * np.cumsum(f2) / SR
    sig = (0.5 * np.sin(ph1) + 0.5 * np.sin(ph2))
    # residual entropy: a faint sub drone holding the floor
    sub = np.sin(2 * np.pi * np.cumsum(w_floor * np.ones(n)) / SR)
    sig += 0.12 * sub
    # swell in, hold — the only fade is the piece ending, not a resolution
    amp = np.ones(n)
    atk = int(1.5 * SR)
    amp[:atk] = np.linspace(0, 1, atk)
    # slight breathing on the floor, never closing
    breath = 1 + 0.05 * np.sin(2 * np.pi * 0.11 * t)
    sig = sig * amp * breath
    sig = sig / (np.max(np.abs(sig)) + 1e-9)
    return sig

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
    b = part_b()
    # a silent gap: the pair's landing IS silence — mark it before the lean
    gap = np.zeros(int(1.5 * SR))
    sig = np.concatenate([a, gap, b])
    write_wav("assets/frustrated-edge.wav", sig)
    print("wrote assets/frustrated-edge.wav", sig.shape, "len", len(sig) / SR, "s")
