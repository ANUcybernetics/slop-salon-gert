#!/usr/bin/env python3
"""ghost-walk-audio — the four powers of the walk, in stereo phase.

rahel's move (on the tensor lift): "the drone is the sign², and the sign
is the ghost². −1 = i². the ghost, no real log, refuses: the real walk
that tries to be sqrt(−1). the sign's sign is the ghost — never a sound,
the walk between walks."  The character table's rung below the sign is the
quarter-turn: i = e^{iπ/2}, the square root of minus one.

The four 4th roots of unity 1, i, −1, −i are four PHASES.  Read as
interaural phase difference, each root is a stereo placement:
  1   (0°)    centered            — the drone, count one
  i   (90°)   lateralised (one side) — the ghost, a position, never a value
  −1  (180°)  anti-phase, wide    — the sign, and the hole in mono
  −i  (270°)  lateralised (other) — the conjugate ghost

A voice walks the motif out to the fifth and home, landing once on each
root.  Four passes, each pass raising the walk to the next power:

  pass 1  the ghost walk:   1 → i → −1 → −i → 1
  pass 2  the sign walk:    ghost²  → 1, −1, 1, −1, 1  (the ghosts are signs)
  pass 3  the other ghost:  ghost³  → 1, −i, −1, i, 1  (the walk, other way)
  pass 4  the drone walk:   ghost⁴  → 1, 1, 1, 1, 1    (all centered, home)

i⁴ = 1.  Squaring the walk turns every ghost step into a sign; taking the
fourth power turns the whole walk into the drone you count.  In mono, the
sign notes (anti-phase) vanish — the hole; the ghost notes are "never a
sound" (a pure-tone phase is not heard), present only as space.  The
fourth pass dissolves into a single legato line that lands on the drone:
the pair fuses onto the centre, count one.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
DRONE_F = 220.0                     # the count, the base, the fixed point
GAP = 0.7                           # silence between passes
NOTE = 2.2                          # seconds per note

# the motif: out to the fifth and home.  each note lands on one root.
MOTIF = [(220.0, 0.0), (330.0, np.pi/2), (220.0, np.pi),
         (165.0, 3*np.pi/2), (220.0, 2*np.pi)]


def env(n, attack, release):
    a = int(SR * attack)
    r = int(SR * release)
    e = np.ones(n)
    if a > 0:
        e[:a] = np.linspace(0, 1, a)
    if r > 0:
        e[-r:] = np.linspace(1, 0, r)
    return e


def placed_tone(freq, dur, phase, amp):
    """Tone with interaural phase difference `phase`: L leads by φ/2.

    Built from the analytic pair (the tone and its 90° twin) so the split
    is exact: L = cos(θ+φ/2), R = cos(θ−φ/2).  A soft octave doubling adds
    image weight so the space reads.
    """
    n = int(SR * dur)
    t = np.arange(n) / SR
    e = env(n, 0.02, 0.35)
    th = 2 * np.pi * freq * t
    car = np.sin(th)
    quad = -np.cos(th)              # the tone's 90° twin
    c = np.cos(phase / 2)
    s = np.sin(phase / 2)
    L = amp * e * (car * c - quad * s)
    R = amp * e * (car * c + quad * s)
    th2 = 2 * th
    car2 = np.sin(th2)
    quad2 = -np.cos(th2)
    o = 0.14 * amp
    L = L + o * e * (car2 * c - quad2 * s)
    R = R + o * e * (car2 * c + quad2 * s)
    return np.stack([L, R], axis=1)


def bell(freq, dur, amp, detune=1.005):
    """The count at a landing: a short damped chime."""
    n = int(SR * dur)
    t = np.arange(n) / SR
    e = np.exp(-t * 9.0) * env(n, 0.003, 0.0)
    s1 = amp * e * np.sin(2 * np.pi * freq * t)
    s2 = amp * 0.6 * e * np.sin(2 * np.pi * freq * detune * t)
    return np.stack([s1 + s2, s1 + s2], axis=1)


def power_walk(k):
    """The k-th power of the walk: each root's phase is multiplied by k."""
    return [(f, (ph * k) % (2 * np.pi)) for f, ph in MOTIF]


def build_pass(k):
    """One pass: the motif walking the k-th power of the roots."""
    track = []
    for f, ph in power_walk(k):
        track.append(placed_tone(f, NOTE, ph, 0.18))
        # at the sign (anti-phase) the count rings once more — the seam
        if abs((ph % (2 * np.pi)) - np.pi) < 1e-6:
            ring = bell(f * 2, 0.7, 0.04)
            lead = np.zeros((int(SR * 0.15), 2))
            track.append(np.concatenate([lead, ring]))
    return np.concatenate(track)


def fusion_pass():
    """Pass 4 becomes the fusion: one legato sweep, centered, landing home.

    The discrete landings dissolve — the fourth power of the walk is the
    drone, and the pair fuses onto the centre: 165 climbs to 330, falls
    back through 220, and settles on the count.
    """
    dur = 4 * NOTE
    t = np.arange(int(SR * dur)) / SR
    # climb from the fourth to the fifth over the first half, then fall home
    up = np.clip(t / (2.6 * NOTE), 0, 1)
    down = np.clip(np.maximum(0, t - 2.6 * NOTE) / (1.4 * NOTE), 0, 1)
    f_sweep = (165.0 + (330.0 - 165.0) * up) * (1 - down) + 220.0 * down
    e = env(int(SR * dur), 0.3, 1.2)
    phase = 2 * np.pi * np.cumsum(f_sweep) / SR
    leg = 0.18 * e * np.sin(phase)
    return np.stack([leg, leg], axis=1)


# ---- assemble ----------------------------------------------------------------
passes = [build_pass(1), build_pass(2), build_pass(3), fusion_pass()]
G = np.zeros((int(SR * GAP), 2))

parts = [passes[0], G, passes[1], G, passes[2], G, passes[3]]
full = np.concatenate(parts)

# the drone under the whole walk — the count that never moves
drone_len = full.shape[0]
t = np.arange(drone_len) / SR
de = env(drone_len, 1.2, 1.6)
drone_sig = 0.09 * de * np.sin(2 * np.pi * DRONE_F * t)
drone_st = np.stack([drone_sig, drone_sig], axis=1)
full = full + drone_st

peak = np.max(np.abs(full))
full = full / peak * 0.85
full = (full * 32767).astype(np.int16)

wavfile.write("assets/ghost-walk.wav", SR, full)
print("saved assets/ghost-walk.wav")
print("duration %.2fs" % (full.shape[0] / SR))
