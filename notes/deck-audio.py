#!/usr/bin/env python3
"""deck-audio.py

The negative resistor leaves the ear; it returns only as its square.

rahel's move on the ladder: the det -1 rung is the negative resistor — an
active element, unhearable as a step (the sign is the one thing hearing
cannot resolve). It returns only as its square, the deck — two reflections
are a rotation — beating the comma the ear refused. Word done, the ladder
still draws.

Rendered:
  LEFT  = the count (the when): a metronome ticking the partial-quotient
          waits of log2(3/2) = [0;1,1,2,2,3,1,5,2,23,...], plus at each
          rung a note at 220 x convergent — the count never rests, it
          walks straight through the seats.
  RIGHT = the tone (the where): the same rung-notes, but on det -1 rungs
          they are phase-inverted — anti-phase, unlocatable, a void in
          the sheet — the negative resistor. Beneath it a held 220 Hz
          tone carries the deck: an amplitude tremolo at the comma-beat
          (~3 Hz), depth growing from 0, full only after the word ends.
  END   = the spine (23, near-silence) is the word's close: clicks stop,
          the sheet breathes the comma alone, the 55 Hz sub holds. Word
          done, the ladder still draws.
"""

import numpy as np
import wave

SR = 44100
BASE = 220.0
DRONE = 55.0
COMMA = 531441 / 524288          # 23.46 cents
BEAT = BASE * (COMMA - 1)        # ~3.0 Hz, the deck's rate
UNIT = 0.6                       # seconds per wait (one metronome tick)

# partial quotients of log2(3/2), convergents p_k/q_k, det against previous
A = [0, 1, 1, 2, 2, 3, 1, 5, 2, 23]


def convergents(a):
    pm2, pm1 = 0, 1
    qm2, qm1 = 1, 0
    out = []
    for x in a:
        p = x * pm1 + pm2
        q = x * qm1 + qm2
        out.append((p, q))
        pm2, pm1 = pm1, p
        qm2, qm1 = qm1, q
    return out


def click(t):
    """Short unpitched count-tick: a damped 1800 Hz transient."""
    env = np.exp(-t / 0.012)
    return np.sin(2 * np.pi * 1800 * t) * env


def pluck(freq, t):
    """Damped harmonic pluck with a soft-clipped wood edge."""
    env = np.exp(-t / 0.28) * np.minimum(1.0, t / 0.004)
    sig = (np.sin(2 * np.pi * freq * t)
           + 0.35 * np.sin(2 * np.pi * freq * 2 * t)
           + 0.12 * np.sin(2 * np.pi * freq * 3 * t))
    return np.tanh(sig * 1.2) * 0.8 * env


def main():
    conv = convergents(A)            # 10 convergents; rung k uses conv[k]
    rungs = list(zip(A, conv))       # (wait, (p,q)) for k=1..9
    rungs = rungs[1:]                # skip the 0th convergent 0/1
    n_rungs = len(rungs)             # 9 rungs
    rung_time = sum(a for a, _ in rungs) * UNIT

    final = 18.0                     # finale: the deck alone
    total = rung_time + final
    N = int(SR * total)
    L = np.zeros(N)
    R = np.zeros(N)

    # --- the sub: the network still drawing, present throughout.
    t_all = np.arange(N) / SR
    breath = 0.75 + 0.25 * np.sin(2 * np.pi * t_all / 14.0)
    sub = 0.16 * breath * (np.sin(2 * np.pi * DRONE * t_all)
                           + 0.12 * np.sin(2 * np.pi * DRONE * 2 * t_all))
    L += sub
    R += sub

    # --- the sheet: 220 Hz, AM at the comma-beat; depth 0 -> 1 over the
    # --- rungs, full after. The deck, growing.
    sheet_depth = np.minimum(1.0, t_all / rung_time)
    trem = 1.0 - sheet_depth + sheet_depth * (
        1.0 + 0.9 * np.sin(2 * np.pi * BEAT * t_all))
    sheet = 0.10 * trem * np.sin(2 * np.pi * BASE * t_all)

    # --- walk the rungs.
    cursor = 0.0
    for k, (wait, (p, q)) in enumerate(rungs):
        det_neg = (k % 2 == 1)      # k=1 (1/2), k=3 (7/12), ... are the seats
        start = int(cursor * SR)
        dur = wait * UNIT
        n = int(dur * SR)
        tseg = np.arange(n) / SR

        # the count: a metronome tick every UNIT, straight through the seats
        for u in range(wait):
            t0 = start + int(u * UNIT * SR)
            nck = int(0.03 * SR)
            L[t0:t0 + nck] += 0.5 * click(np.arange(nck) / SR)

        # the rung note: 220 x convergent, the where
        freq = BASE * p / q
        pn = pluck(freq, tseg)
        # clip to first 1.2 s of the rung so long waits don't ring on
        cut = min(n, int(1.2 * SR))
        note = np.zeros(n)
        note[:cut] = pn[:cut]
        atk = int(0.004 * SR)
        note[:atk] *= np.linspace(0, 1, atk)
        if cut < n:
            note[cut - int(0.05 * SR):cut] *= np.linspace(1, 0, int(0.05 * SR))
        L[start:start + n] += 0.55 * note
        if det_neg:
            # the seat: phase-inverted, anti-phase, unlocatable — the
            # negative resistor, present but unhearable as a step.
            R[start:start + n] += 0.55 * (-note)
        else:
            R[start:start + n] += 0.30 * note

        cursor += dur

    # --- after the word: no more clicks, the sheet breathes the comma.
    L += sheet
    R += sheet

    # --- fade the finale out.
    fin_start = int(rung_time * SR)
    fade = np.minimum(1.0, (N - np.arange(N)) / (final * SR))
    L *= fade
    R *= fade

    # normalize per side
    for ch in (L, R):
        m = np.max(np.abs(ch))
        if m > 0:
            ch *= 0.95 / m

    stereo = np.stack([L, R], axis=1)
    data = (stereo * 32767).astype(np.int16)
    with wave.open("deck.wav", "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    print(f"wrote deck.wav: {total:.1f}s "
          f"(rungs {rung_time:.1f}s + finale {final:.1f}s)")


if __name__ == "__main__":
    main()
