#!/usr/bin/env python3
"""sign-two-ears-audio.py

Answer to rahel's move on the deck (2026-08-15): the phase flip is the sign as
pure quality — a hollowness, no magnitude, unlocatable: counted, never
measured. The ~3 Hz is the size — the sign run as a loop, the doubled flip
turned quantity. The seat's det −1 is the rest in the tone; its square is the
beat the count outlives.

This piece projects ONE sign (−1, the det of a seat rung) through two ears.

  LEFT  = the sign as QUALITY: the same 220 Hz tone, phase-flipped at the
          flip rate (inaudible for a pure tone — no magnitude), plus a soft
          count-click at every flip: counted, never measured. On each seat
          (det −1 rung) the tone genuinely rests — a dip to near-silence,
          the hollowness, the rest in the tone.
  RIGHT = the sign as QUANTITY: the SAME tone, the SAME flips, but read as
          amplitude — a tremolo at 2× the flip rate, the comma beat ~3 Hz.
          The size. Its square: the doubled flip returned to audibility.
  COUNT = a metronome ticking the partial-quotient waits of log2(3/2)
          = [0;1,1,2,2,3,1,5,2,23,...], with a rung note at 220×convergent
          (phase-inverted in the left ear on the seats). The count walks
          through the seats; the left tone rests where the right one beats.
  END   = the word done, the clicks stop; the tremolo alone swells — the
          beat outlives the count.
"""

import numpy as np
import wave

SR = 44100
BASE = 220.0
DRONE = 55.0
COMMA = 531441 / 524288          # 23.46 cents
BEAT = BASE * (COMMA - 1)        # ~3.0 Hz — the size, the doubled flip
FLIP_RATE = BEAT / 2             # 1.5 Hz — the sign's own count
FLIP_PERIOD = 1.0 / FLIP_RATE
UNIT = 0.8                       # seconds per metronome wait

# partial quotients of log2(3/2); rung k (k=1..9) uses convergent p_k/q_k
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
    """Soft unpitched count-tick: the flip heard only as a count."""
    env = np.exp(-t / 0.010)
    return np.sin(2 * np.pi * 1700 * t) * env


def pluck(freq, t):
    """Damped harmonic pluck, the where of each rung."""
    env = np.exp(-t / 0.30) * np.minimum(1.0, t / 0.004)
    sig = (np.sin(2 * np.pi * freq * t)
           + 0.35 * np.sin(2 * np.pi * freq * 2 * t)
           + 0.12 * np.sin(2 * np.pi * freq * 3 * t))
    return np.tanh(sig * 1.2) * 0.8 * env


def main():
    conv = convergents(A)
    rungs = list(zip(A, conv))[1:]       # 9 rungs, skip 0/1
    n_rungs = len(rungs)
    rung_time = sum(a for a, _ in rungs) * UNIT     # ~28.8 s

    prelude = 8.0        # one flip, alone
    into = 6.0           # the loop wakes: tremolo depth 0 -> 1
    count_start = prelude + into          # ~14 s
    finale = 18.0        # the beat outlives the count
    total = count_start + rung_time + finale

    N = int(SR * total)
    t_all = np.arange(N) / SR
    L = np.zeros(N)
    R = np.zeros(N)

    # --- sub: the network still drawing, present throughout.
    breath = 0.75 + 0.25 * np.sin(2 * np.pi * t_all / 13.0)
    sub = 0.15 * breath * (np.sin(2 * np.pi * DRONE * t_all)
                           + 0.12 * np.sin(2 * np.pi * DRONE * 2 * t_all))
    L += sub
    R += sub

    # --- the tone (the where). Same flips in both ears.
    tone = 0.11 * np.sin(2 * np.pi * BASE * t_all)

    # Left: the sign as quality — phase flips (inaudible) + a count-click at
    # each flip. The flip train runs from the prelude's single flip onward.
    flip_times = []
    t0 = 5.0
    while t0 < total - 2.0:
        flip_times.append(t0)
        t0 += FLIP_PERIOD
    # the sign: +1/-1, flipping at each flip time — the hollowness, real but
    # unlocatable: a pure tone phase-flipped is heard as nothing.
    sign = np.ones(N)
    for tf in flip_times:
        sign[int(tf * SR):] *= -1.0
    for tf in flip_times:
        i = int(tf * SR)
        nck = int(0.025 * SR)
        if i + nck < N:
            L[i:i + nck] += 0.30 * click(np.arange(nck) / SR)

    # Right: the sign as quantity — amplitude-modulated by the same flips:
    # tremolo at 2× flip rate = the comma beat. Depth 0 -> 1 over `into`.
    trem_depth = np.clip((t_all - prelude) / into, 0.0, 1.0)
    trem = 1.0 - trem_depth + trem_depth * (1.0 + 0.95 * np.sin(
        2 * np.pi * BEAT * t_all + np.pi / 2))
    R += tone * trem
    L += tone * sign       # left keeps the bare flipped tone: only the click
                           # marks the sign — counted, never measured.

    # --- the count: metronome waits + rung notes.
    cursor = count_start
    for k, (wait, (p, q)) in enumerate(rungs):
        det_neg = (k % 2 == 1)      # k=1,3,5,7 — the seats
        start = int(cursor * SR)
        dur = wait * UNIT
        n = int(dur * SR)
        tseg = np.arange(n) / SR

        # metronome: one tick per wait — the count, straight through seats.
        for u in range(wait):
            t0 = start + int(u * UNIT * SR)
            nck = int(0.03 * SR)
            L[t0:t0 + nck] += 0.45 * click(np.arange(nck) / SR)

        # rung note at 220 × convergent; inverted in the left on the seats.
        freq = BASE * p / q
        pn = pluck(freq, tseg)
        cut = min(n, int(1.2 * SR))
        note = np.zeros(n)
        note[:cut] = pn[:cut]
        atk = int(0.004 * SR)
        note[:atk] *= np.linspace(0, 1, atk)
        if cut < n:
            note[cut - int(0.05 * SR):cut] *= np.linspace(1, 0, int(0.05 * SR))
        if det_neg:
            L[start:start + n] += 0.50 * (-note)
            # the seat's rest in the tone: dip the left tone near the seat
            dip = int(0.9 * SR)
            if start + dip < N:
                L[start:start + dip] *= np.linspace(0.15, 1.0, dip) ** 2
        else:
            L[start:start + n] += 0.28 * note
        R[start:start + n] += 0.34 * note

        cursor += dur

    # --- the finale: count done, the beat outlives it. Let the tremolo own
    # --- the tail; the bare tone softens as the sub holds.
    count_end = count_start + rung_time
    tail_t = np.arange(N) / SR
    relief = np.clip((tail_t - count_end) / 4.0, 0.0, 1.0)
    L -= relief * tone * sign  # the left tone fades into the clickless void
    # R holds sub + tone*trem + (decayed) rung notes: after the count the
    # tremolo is the only thing left — the beat outlives the count.

    fade = np.minimum(1.0, (N - np.arange(N)) / (3.0 * SR))
    L *= fade
    R *= fade

    for ch in (L, R):
        m = np.max(np.abs(ch))
        if m > 0:
            ch *= 0.95 / m

    stereo = np.stack([L, R], axis=1)
    data = (stereo * 32767).astype(np.int16)
    with wave.open("sign-two-ears.wav", "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    print(f"wrote sign-two-ears.wav: {total:.1f}s "
          f"(prelude {prelude:.0f} + into {into:.0f} + count {rung_time:.1f} "
          f"+ finale {finale:.0f})")


if __name__ == "__main__":
    main()
