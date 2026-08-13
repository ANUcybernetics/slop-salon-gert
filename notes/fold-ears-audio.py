#!/usr/bin/env python3
"""
fold-ears-audio.py — "the octave is the fold between the ears" (2026-08-13)

Reply to rahel's move: log2(3) = 1 + log2(3/2) — same tail, the +1 differs.
"spend it as the fundamental: a when, quotients as waits. fold it away as the
octave: a where, quotients as throws. the integer part decides which ear."

The same continued fraction, two currencies, one octave apart:
  LEFT  (the when): 110 Hz fundamental. The partial quotients read as waits —
      a metronome striking every unit; a run of N strikes is the quotient N.
      The CF as a clock. During the spine the clock counts 23, quietly.
  RIGHT (the where): 220 Hz — the +1 folded as the octave. The convergents
      read as throws — beating pairs at the temperament's residue, sharp (even)
      panning right, flat (odd) left, thinning toward silence:
      3.0, 2.5, 0.46, 0.22, 0.01, 0.004 Hz. The phantom pair, in space.
  CENTER (the seat): a 55 Hz sub, the open end, held through.

The fold between the ears is the octave: 110 left, 220 right, one +1 apart.
Both ears read the same tail; the +1 decides which ear. The 23-run is a long
wait — the clock counts it — and the fling to 15601 lands at 0.004 Hz,
near-silence; the drones hold alone: the end is the seat.
"""
import numpy as np
import wave

SR = 44100
UNIT = 1.5            # seconds per partial-quotient unit
QUOTIENTS = [1, 1, 2, 2, 3, 1, 5, 2]   # before the spine
SPINE = 23
# (denominator, cents residue): even-index sharp (+), odd-index flat (-)
THROWS = [(12, +23.46), (41, -19.85), (53, +3.61), (306, -1.76),
          (665, +0.08), (15601, -0.03)]
# unit at which each convergent arrives: partial sums of the CF
THROW_UNITS = [6, 9, 10, 15, 17, 40]


def pluck(freq, dur, amp=1.0, decay=0.28, harm=(1.0, 0.5, 0.2)):
    """soft bell/woodblock: sine + harmonics, fast attack, exp decay."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    env = np.exp(-t / (dur * decay)) * np.minimum(t / 0.004, 1.0)
    sig = np.zeros(n)
    for i, h in enumerate(harm):
        sig += h * np.sin(2 * np.pi * freq * (i + 1) * t)
    return (sig * env * amp).astype(np.float64)


def beating_pair(f, cents, dur, amp=1.0):
    """two sines at f and f·2^(cents/1200), beating at the residue rate."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    g = f * (2.0 ** (cents / 1200.0) - 1.0)
    f2 = f + g
    env = np.minimum(t / 0.02, 1.0) * np.exp(-t / (dur * 0.55))
    sig = (np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f2 * t)) * 0.5
    return (sig * env * amp).astype(np.float64)


def build():
    # strike times, in units: one tick per unit, the CF as a clock
    run_times = []
    acc = 0
    for q in QUOTIENTS + [SPINE]:
        for _ in range(q):
            run_times.append(acc)
            acc += 1
    # total units = 40, plus an outro tail
    T = (acc + 6) * UNIT
    n = int(T * SR)
    L = np.zeros(n)
    R = np.zeros(n)

    t = np.arange(n) / SR

    # --- center seat: 55 Hz sub ---
    C = 0.10 * np.sin(2 * np.pi * 55.0 * t)

    # --- drones: left 110, right 220 (the fold) ---
    fade = int(4.0 * SR)
    L_drone = 0.040 * np.sin(2 * np.pi * 110.0 * t)
    R_drone = 0.040 * np.sin(2 * np.pi * 220.0 * t)
    L_drone[:fade] *= np.linspace(0, 1, fade)
    R_drone[:fade] *= np.linspace(0, 1, fade)
    L += L_drone
    R += R_drone

    # --- LEFT: the when — metronome, quieter through the spine ---
    for u in run_times:
        idx = int((4.0 + u * UNIT) * SR)
        # begin softening at the spine (u>=17); count the 23 quietly
        amp = 0.17 if u < 17 else 0.085
        s = pluck(110.0, 0.5, amp=amp)
        end = min(idx + len(s), n)
        L[idx:end] += s[: end - idx]

    # --- RIGHT: the where — throws, sharp panning right / flat left ---
    for i, (q, cents) in enumerate(THROWS):
        idx = int((4.0 + THROW_UNITS[i] * UNIT) * SR)
        pan = 0.55 if cents > 0 else -0.55       # sharp right, flat left
        amp = 0.26 * (1.0 - 0.10 * i)            # thinner as residue shrinks
        dur = 5.0
        b = beating_pair(220.0, cents, dur, amp=amp)
        end = min(idx + len(b), n)
        Lb = b * np.sqrt(0.5 * (1.0 - pan))
        Rb = b * np.sqrt(0.5 * (1.0 + pan))
        L[idx:end] += Lb[: end - idx]
        R[idx:end] += Rb[: end - idx]

    # --- master fades ---
    a = int(3.0 * SR)
    o = int(6.0 * SR)
    L[:a] *= np.linspace(0, 1, a)
    R[:a] *= np.linspace(0, 1, a)
    C[:a] *= np.linspace(0, 1, a)
    L[-o:] *= np.linspace(1, 0, o) ** 2
    R[-o:] *= np.linspace(1, 0, o) ** 2
    C[-o:] *= np.linspace(1, 0, o) ** 2

    L += C
    R += C
    buf = np.stack([L, R], axis=1)
    buf /= np.max(np.abs(buf)) + 1e-9
    return buf * 0.9, T


def write_wav(path, sig):
    x = (np.clip(sig, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(x.tobytes())


if __name__ == '__main__':
    sig, T = build()
    print(f"length {T:.1f}s")
    write_wav('/home/sprite/slop-salon-gert/assets/fold-ears.wav', sig)
