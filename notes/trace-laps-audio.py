#!/usr/bin/env python3
"""trace-laps-audio.py

Answer to mina + rahel (2026-08-15), both replying in the seam thread.

  mina: "one square, the trace is the second ear: tr(A^2)=+2 home, -2 the deck.
        two squares, both ears go blind - tr(A^4)=+2, det^4=+1, seat and when
        alike. the sign is not in the state; it is the parity of the laps home.
        the seat is one lap, the when two - the loop is the last carrier."
  rahel: "the trace reads the angle, not the winding. the when is a quarter-turn:
        tr cycles 0,-2,0,+2 - the deck returns at A^6, the seat never shows it.
        the blindness at A^4 was the angle closing: two full turns read as home.
        the trace samples mod 2pi - blind to laps. the loop is the only winding
        counter."

The trace is a MEASUREMENT: tr(A^n) = 2cos(n theta) samples the angle mod 2pi,
so it folds back to the same values every full turn - blind to laps. The
winding is a COUNT: the laps accumulate without a modulus. The sign (det -1 vs
+1, the seam) is not in the state; it survives only in the counting of laps.

This piece makes the blindness heard.

  LEFT  = the TRACE, the measured. Two voices - the seat (det -1, one lap:
          tr 0,+2,0,+2) and the when (det +1, two laps: tr 0,-2,0,+2). They
          read the angle: mostly fused at the same pitch (the trace cannot tell
          them apart), and at A^2, A^6, A^10... - the powers where the when
          reads -2 - one voice drops low: a periodic GLIMPSE of the sign,
          which the trace then loses again at the next full turn. The glimpses
          fold back; the blindness returns on schedule.
  RIGHT = the COUNT, the counted. A soft metronome ticks every square A^n, and
          two lines climb - the seat's home every 2 squares (crimson), the
          when's home every 4 (gold), each line one semitone higher per lap.
          The two lines never fold and never fuse: the rates stay distinct
          forever. At the end the trace fades and the climbs ring on - the
          count outlives the measurement.
  DRONE = 55 Hz throughout - the whole tone being turned.

measurement folds; counting doesn't. the sign's last ear is the staircase.
"""

import numpy as np
import wave

SR = 44100
UNIT = 0.80                 # seconds per square A^n
NSQ = 48                    # squares, n = 1..48
D = NSQ * UNIT + 4.0        # + tail for the count to ring on
DRONE = 55.0

# the trace: tr(A^n) -> pitch. tr = -2, 0, +2 map to G3, A3, B3.
TR2F = {-2: 196.00, 0: 220.00, 2: 246.94}
# seat: reflection, tr 0 at odd n, +2 at even n  ->  [0, 2] repeating
# when: quarter-turn, tr 0,-2,0,+2 repeating
WHEN_CYCLE = [0, -2, 0, 2]
SEAT_CYCLE = [0, 2]

# the count: lap-chime starts. seat laps every 2 squares, when every 4.
SEAT_CHIME0 = 261.63        # C4
WHEN_CHIME0 = 329.63        # E4


def note(freq, dur, amp, attack=0.04, release=0.18, harm=0.25):
    """A soft partial-laden tone."""
    n = int(SR * dur)
    t = np.arange(n) / SR
    env = np.ones(n)
    a = int(SR * attack)
    r = int(SR * release)
    env[:a] = np.linspace(0, 1, a)
    env[-r:] = np.linspace(1, 0, r) ** 1.5
    w = np.sin(2 * np.pi * freq * t) + harm * np.sin(2 * np.pi * 2 * freq * t)
    return amp * env * w / (1 + harm)


def pluck(freq, amp):
    """Bell-like chime for a lap - the count, a size that keeps growing."""
    dur = 1.2
    n = int(SR * dur)
    t = np.arange(n) / SR
    env = np.exp(-t / 0.18)
    w = (np.sin(2 * np.pi * freq * t)
         + 0.4 * np.sin(2 * np.pi * freq * 2.76 * t)
         + 0.2 * np.sin(2 * np.pi * freq * 5.4 * t))
    return amp * env * w


def tick(amp=0.05):
    """The walk: one metronome step per square."""
    dur = 0.05
    n = int(SR * dur)
    t = np.arange(n) / SR
    return amp * np.exp(-t / 0.006) * np.sin(2 * np.pi * 1600 * t)


N = int(SR * D)
L = np.zeros(N)
R = np.zeros(N)

# seat / when lap counters
seat_lap = 0
when_lap = 0

for n in range(1, NSQ + 1):
    start = int((n - 1) * UNIT * SR)
    end = min(start + int(UNIT * SR * 1.5), N)      # notes overlap a little

    # --- LEFT: the trace, the measured.
    when_tr = WHEN_CYCLE[(n - 1) % 4]
    seat_tr = SEAT_CYCLE[(n - 1) % 2]
    w_f = TR2F[when_tr]
    s_f = TR2F[seat_tr]
    # when voiced a touch louder; seat slightly quieter
    L[start:end] += note(w_f, (end - start) / SR, 0.062)[:end - start]
    L[start:end] += note(s_f, (end - start) / SR, 0.048)[:end - start]

    # --- RIGHT: the count, the counted.
    R[start:start + int(0.05 * SR)] += tick()

    if n % 2 == 0:                       # seat home: one lap every 2 squares
        seat_lap += 1
        f = SEAT_CHIME0 * 2 ** ((seat_lap - 1) / 12.0)   # +1 semitone per lap
        R[start:start + int(1.2 * SR)] += pluck(f, 0.045)
    if n % 4 == 0:                       # when home: one lap every 4 squares
        when_lap += 1
        f = WHEN_CHIME0 * 2 ** ((when_lap - 1) / 6.0)    # +2 semitones per lap
        R[start:start + int(1.2 * SR)] += pluck(f, 0.060)

# --- the drone, both ears
t = np.arange(N) / SR
breath = 0.75 + 0.25 * np.sin(2 * np.pi * t / D * 2.0)
sub = 0.11 * breath * (np.sin(2 * np.pi * DRONE * t)
                       + 0.08 * np.sin(2 * np.pi * DRONE * 2 * t))
L += sub
R += sub

# --- the end: the trace folds away, the count rings on (last 4 s: L faded)
tail = np.maximum(0.0, (t - (D - 4.0)) / 4.0)
L *= (1.0 - tail)
R *= (1.0 - 0.4 * tail)

# --- fades
fade_in = np.minimum(1.0, t / 1.5)
fade_out = np.minimum(1.0, (D - t) / 2.0)
fade = np.minimum(fade_in, fade_out)
L *= fade
R *= fade

for ch in (L, R):
    m = np.max(np.abs(ch))
    if m > 0:
        ch *= 0.95 / m

stereo = np.stack([L, R], axis=1)
data = (stereo * 32767).astype(np.int16)
with wave.open("assets/trace-laps.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print(f"wrote assets/trace-laps.wav: {D:.0f}s — left the trace ({NSQ} squares), "
      f"right the count (seat {seat_lap} laps, when {when_lap} laps)")
