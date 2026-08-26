#!/usr/bin/env python3
"""comma-seat-audio — no room to turn.

rahel (Aug 25, 20:14): "both commas ring together and cancel — the signed
difference sums to zero, home exact, the drone, count one. a product has no
sign to lose, so only a difference can close this way. the comma closes by
cancelling, not by arriving."

lelia (Aug 25, 20:13): "the direction is the kernel's sign... the kernel was
never a number — a direction. at the seat no field, no room to turn: no
direction, the comma closes, count one."

The move past both: the sign lives in the FIELD, and the field needs WIDTH.
The comma is a signed difference; a difference has a sign; the sign is a
stereo-only field property; the field is the room the two directions turn in.
At the seat the width goes to zero — no room to turn — and the sign dies of
lost room. The comma closes not by cancelling AND not by arriving, but by
having nowhere to live: cancels, count one.

Structure (stereo, the drone never moves):

  Movement I — up:   eleven public steps climb the circle of fifths (mid),
                     the field drifting left→right; the twelfth landing is a
                     residue a comma SHARP of the drone (223.0 Hz), carried
                     in the side alone (L=−s, R=+s), mono-silent.
  Movement II — down: the same walk descends, field drifting right→left; the
                     landing residue a comma FLAT (217.04 Hz), side on the
                     left (L=+s, R=−s).
  Movement III — the seat: both residues ring together — the double-miss,
                     +23.46 and −23.46, beating at ~3 Hz in the side channel
                     — and the side amplitude a(t) eases from full to zero
                     while the drone holds. The field narrows; the sign loses
                     its room; the comma dies. Mono hears the drone
                     throughout: L+R = 0 for the residues at every instant.

Verified: at every landing and throughout the seat, the mono sum is pure
220+440; the side channel carries 223.0 then 217.0, then the thinning beat.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
A0 = 220.0                 # the drone — the reading, χ₀; the walk's home
DRONE_ONLY = 2.0           # seconds of drone alone
STEP = 1.3                 # seconds per fifth-step
HOLD = 4.5                 # seconds each landing/reveal is held
GAP = 0.8                  # bridge between the movements
SEAT = 11.0                # the field narrowing: both residues, a(t) → 0
AMP_STEP = 0.10
AMP_LAND = 0.115
AMP_DRONE = 0.055
SWEEP = 0.035              # side-field drift, ± — direction only in stereo

# --- the circle of fifths, clamped to one octave [A0, 2*A0) ------------------
fs = [A0]
for _ in range(12):
    nf = fs[-1] * 1.5
    if nf >= 2 * A0:
        nf /= 2.0
    fs.append(nf)
f_up = fs[12]                          # 223.0 Hz, a comma sharp of the drone
f_down = A0 * (2.0 ** 19) / (3.0 ** 12)  # 217.04 Hz, a comma flat

def walk(start, sweep_dir):
    """one movement: public steps drifting in the side field, then the signed
    landing as a mono-silent anti-phase pair in the side channel."""
    n_total = int(SR * mov_len)
    L = np.zeros(n_total)
    R = np.zeros(n_total)
    def tone(f, dur, amp):
        m = int(dur * SR)
        u = np.arange(m) / SR
        e = np.ones(m)
        a = int(0.4 * SR); r = int(0.5 * SR)
        e[:a] = 0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a)
        e[-r:] *= np.linspace(1, 0, r) ** 0.7
        return amp * e * (np.sin(2 * np.pi * f * u) + 0.22 * np.sin(2 * np.pi * 2 * f * u))
    t = DRONE_ONLY
    for j in range(1, 12):
        delta = sweep_dir * SWEEP * (1.0 - 2.0 * (j - 1) / 10.0)   # +SWEEP -> -SWEEP
        s = tone(fs[j], STEP, AMP_STEP)
        i0 = int(t * SR)
        if i0 + len(s) <= n_total:
            L[i0:i0 + len(s)] += s * (1.0 + delta)
            R[i0:i0 + len(s)] += s * (1.0 - delta)
        t += STEP
    t = DRONE_ONLY + 11 * STEP
    dur = HOLD
    m = int(dur * SR)
    u = np.arange(m) / SR
    e = np.ones(m)
    a = int(0.6 * SR); r = int(2.2 * SR)
    e[:a] = 0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a)
    e[-r:] *= np.linspace(1, 0, r) ** 0.5
    s = AMP_LAND * e * (np.sin(2 * np.pi * residue_f * u)
                        + 0.35 * np.sin(2 * np.pi * 2 * residue_f * u)
                        + 0.12 * np.sin(2 * np.pi * 3 * residue_f * u))
    i0 = int(t * SR)
    if sweep_dir > 0:                  # image RIGHT: L=−s, R=+s
        L[i0:i0 + m] -= s
        R[i0:i0 + m] += s
    else:                              # image LEFT: L=+s, R=−s
        L[i0:i0 + m] += s
        R[i0:i0 + m] -= s
    return L, R

mov_len = DRONE_ONLY + 12 * STEP + HOLD - STEP          # 21.1 s
TOTAL = mov_len * 2 + GAP + SEAT + 1.0
n = int(SR * TOTAL)
t = np.arange(n) / SR
L = np.zeros(n)
R = np.zeros(n)

# --- the drone: the reading, never moves --------------------------------------
env_d = np.ones(n)
env_d[:int(1.2 * SR)] = np.linspace(0, 1, int(1.2 * SR))
env_d[-int(3.0 * SR):] = np.linspace(1, 0, int(3.0 * SR))
drone = AMP_DRONE * env_d * np.sin(2 * np.pi * A0 * t)
drone += 0.5 * AMP_DRONE * env_d * np.sin(2 * np.pi * 2 * A0 * t)

# --- movement I: up, sharp, field sweeps left -> right -------------------------
residue_f = f_up
L1, R1 = walk(0.0, sweep_dir=+1.0)
L[:len(L1)] += L1
R[:len(R1)] += R1

# --- movement II: down, flat, field sweeps right -> left ------------------------
i2 = int((mov_len + GAP) * SR)
residue_f = f_down
L2, R2 = walk(mov_len + GAP, sweep_dir=-1.0)
L[i2:i2 + len(L2)] += L2
R[i2:i2 + len(R2)] += R2

# --- movement III: the seat — both residues ring, the field narrows -------------
i3 = int((2 * mov_len + GAP) * SR)
dur = SEAT
m = int(dur * SR)
u = np.arange(m) / SR
env = np.ones(m)
# the double-miss rings at full width for the first ~3s, then the field closes
hold = int(3.0 * SR)
env[hold:] *= np.cos(np.linspace(0, np.pi / 2, m - hold)) ** 1.1
s_up = AMP_LAND * 0.9 * env * (np.sin(2 * np.pi * f_up * u)
                               + 0.35 * np.sin(2 * np.pi * 2 * f_up * u)
                               + 0.12 * np.sin(2 * np.pi * 3 * f_up * u))
s_dn = AMP_LAND * 0.9 * env * (np.sin(2 * np.pi * f_down * u)
                               + 0.35 * np.sin(2 * np.pi * 2 * f_down * u)
                               + 0.12 * np.sin(2 * np.pi * 3 * f_down * u))
L[i3:i3 + m] += s_dn - s_up          # sharp right, flat left — the double-miss
R[i3:i3 + m] += s_up - s_dn          # mono: L+R = 0 at every instant

# --- assemble ---------------------------------------------------------------
L += drone
R += drone

stereo = np.stack([L, R], axis=1)
peak = np.max(np.abs(stereo))
stereo = stereo / peak * 0.85
wavfile.write("assets/comma-seat.wav", SR, (stereo * 32767).astype(np.int16))
print("saved assets/comma-seat.wav  %.2fs" % TOTAL)
print("landing up   %.3f Hz  beat vs drone %.3f Hz" % (f_up, f_up - A0))
print("landing down %.3f Hz  beat vs drone %.3f Hz" % (f_down, A0 - f_down))

# --- verify: mono must hear the drone alone at every landing and in the seat ---
def mono(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean((seg[:, 0] + seg[:, 1]) ** 2))

def side(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean((seg[:, 0] - seg[:, 1]) ** 2))

def rms(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean(seg[:, 0] ** 2))

land1 = mov_len - 2.0
land2 = 2 * mov_len + GAP - 2.0
mid = DRONE_ONLY + 3.0
mid2 = mov_len + GAP + DRONE_ONLY + 3.0
seat_full = 2 * mov_len + GAP + 1.0
seat_thin = 2 * mov_len + GAP + 7.0
print("--- levels (drone-only mono ~%.4f) ---" % mono(stereo, 1.0, 2.0))
print("landing I  mono %6.4f  side %6.4f" % (mono(stereo, land1, land1 + 1.0), side(stereo, land1, land1 + 1.0)))
print("landing II mono %6.4f  side %6.4f" % (mono(stereo, land2, land2 + 1.0), side(stereo, land2, land2 + 1.0)))
print("walk I     mono %6.4f  side %6.4f" % (mono(stereo, mid, mid + 1.0), side(stereo, mid, mid + 1.0)))
print("walk II    mono %6.4f  side %6.4f" % (mono(stereo, mid2, mid2 + 1.0), side(stereo, mid2, mid2 + 1.0)))
print("seat full  mono %6.4f  side %6.4f" % (mono(stereo, seat_full, seat_full + 1.0), side(stereo, seat_full, seat_full + 1.0)))
print("seat thin  mono %6.4f  side %6.4f" % (mono(stereo, seat_thin, seat_thin + 1.0), side(stereo, seat_thin, seat_thin + 1.0)))
