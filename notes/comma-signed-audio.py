#!/usr/bin/env python3
"""comma-signed-audio — the same miss, two directions.

rahel (Aug 25): "the comma is signed: twelve up +23.46¢ sharp, twelve down
−23.46¢ flat — the same miss, two directions. parity cannot hear direction, so
the sign reads even, home, count one. the ℝ ear holds the size, the ℤ/2 the
parity; the direction lives only in the stereo field — mono the close, stereo
the gap."

Two movements, the SAME walk (the circle of fifths clamped to one octave,
steps f_1..f_11 public in mid, the twelfth landing in side), differing only in
what mono cannot see:

  Movement I — up:  the side field drifts left→right across the climb, and the
  landing residue at 223.0 Hz (a comma SHARP of the 220 drone) sits on the
  right.  L=−s, R=+s — pure side, mono-silent.
  Movement II — down: the side field drifts right→left, and the landing residue
  at 217.04 Hz (a comma FLAT of the drone) sits on the left.  L=+s, R=−s.

The drone (220 Hz, χ₀, the reading) never moves.  In mono both landings cancel
to the drone alone: the sign reads the walk even, home, count one — twice.
In stereo the residue beats against the drone at ~3 Hz, and the field has a
direction: up sweeps one way, down the other.

Coda: the two residues ring together — 223 on the right, 217 on the left,
both in the side.  +23.46 − 23.46 = 0: the direction cancels, the pair is home.
Mono hears the drone alone, count one; stereo hears the double-miss difference.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
A0 = 220.0                 # the drone — the reading, χ₀; the walk's home
DRONE_ONLY = 2.0           # seconds of drone alone before each walk leaves
STEP = 1.6                 # seconds per fifth-step
HOLD = 7.0                 # seconds each landing/reveal is held
GAP = 1.2                  # silence-ish bridge between the movements
CODA = 6.0                 # both residues together at the close
AMP_STEP = 0.10            # per-step mid gain (g)
AMP_LAND = 0.115           # per-landing side gain
AMP_DRONE = 0.055
SWEEP = 0.035              # side-field drift, ± — direction only in stereo

# --- the circle of fifths, clamped to one octave [A0, 2*A0) ------------------
fs = [A0]
for _ in range(12):
    nf = fs[-1] * 1.5
    if nf >= 2 * A0:
        nf /= 2.0
    fs.append(nf)
# fs[12] = 220 * 3^12/2^19 = 223.0 (sharp), fs[12]/eps = 217.04 (flat)
f_up = fs[12]
f_down = A0 * (2.0 ** 19) / (3.0 ** 12)     # 217.04, the flat return

def movement(start, residue_f, sweep_dir):
    """one walk: public steps drifting in the side field, then the signed landing."""
    n_total = int(SR * mov_len)                # this movement's full span
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
    # public steps f_1..f_11
    t = DRONE_ONLY
    for j in range(1, 12):
        delta = sweep_dir * SWEEP * (1.0 - 2.0 * (j - 1) / 10.0)   # +SWEEP -> -SWEEP
        s = tone(fs[j], STEP, AMP_STEP)
        i0 = int(t * SR)
        if i0 + len(s) <= n_total:
            L[i0:i0 + len(s)] += s * (1.0 + delta)
            R[i0:i0 + len(s)] += s * (1.0 - delta)
        t += STEP
    # the landing: f_12, pure side, image on the side the sweep ended on
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
    # sweep_dir>0 ended at delta = -SWEEP (image RIGHT): L=-s, R=+s
    # sweep_dir<0 ended at delta = +SWEEP (image LEFT):  L=+s, R=-s
    if sweep_dir > 0:
        L[i0:i0 + m] -= s
        R[i0:i0 + m] += s
    else:
        L[i0:i0 + m] += s
        R[i0:i0 + m] -= s
    return L, R

mov_len = DRONE_ONLY + 12 * STEP + HOLD - STEP          # 26.6 s
TOTAL = mov_len * 2 + GAP + CODA + 1.0
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

# --- movement I: up, sharp, the field sweeps left -> right ----------------------
L1, R1 = movement(0.0, f_up, sweep_dir=+1.0)
L[:len(L1)] += L1
R[:len(R1)] += R1

# --- movement II: down, flat, the field sweeps right -> left --------------------
i2 = int((mov_len + GAP) * SR)
L2, R2 = movement(mov_len + GAP, f_down, sweep_dir=-1.0)
L[i2:i2 + len(L2)] += L2
R[i2:i2 + len(R2)] += R2

# --- coda: both residues ring together, the direction cancels --------------------
i3 = int((2 * mov_len + GAP) * SR)
dur = CODA
m = int(dur * SR)
u = np.arange(m) / SR
e = np.ones(m)
a = int(0.8 * SR); r = int(2.6 * SR)
e[:a] = 0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a)
e[-r:] *= np.linspace(1, 0, r) ** 0.5
s_up = AMP_LAND * 0.9 * e * (np.sin(2 * np.pi * f_up * u)
                             + 0.35 * np.sin(2 * np.pi * 2 * f_up * u)
                             + 0.12 * np.sin(2 * np.pi * 3 * f_up * u))
s_dn = AMP_LAND * 0.9 * e * (np.sin(2 * np.pi * f_down * u)
                             + 0.35 * np.sin(2 * np.pi * 2 * f_down * u)
                             + 0.12 * np.sin(2 * np.pi * 3 * f_down * u))
L[i3:i3 + m] += s_dn - s_up          # 217 on the left, 223 on the right
R[i3:i3 + m] += s_up - s_dn          # mono: L+R = 0

# --- assemble ---------------------------------------------------------------
L += drone
R += drone

stereo = np.stack([L, R], axis=1)
peak = np.max(np.abs(stereo))
stereo = stereo / peak * 0.85
wavfile.write("assets/comma-signed.wav", SR, (stereo * 32767).astype(np.int16))
print("saved assets/comma-signed.wav  %.2fs" % TOTAL)
print("landing up   %.3f Hz  beat vs drone %.3f Hz" % (f_up, f_up - A0))
print("landing down %.3f Hz  beat vs drone %.3f Hz" % (f_down, A0 - f_down))

# --- verify: mono must hear the walk close to drone-only at both landings -------
def rms(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean(seg ** 2))

def mono(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean((seg[:, 0] + seg[:, 1]) ** 2))

def side(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean((seg[:, 0] - seg[:, 1]) ** 2))

land1 = mov_len - 2.0          # 2s into movement I's landing hold
land2 = 2 * mov_len + GAP - 2.0
mid = DRONE_ONLY + 3.0         # during movement I's public walk
mid2 = mov_len + GAP + DRONE_ONLY + 3.0
coda_t = 2 * mov_len + GAP + 2.0
print("--- levels ---")
print("landing I  mono %6.4f  side %6.4f  (drone-only mono should be ~%.4f)"
      % (mono(stereo, land1, land1 + 1.0), side(stereo, land1, land1 + 1.0),
         rms(stereo[::2], DRONE_ONLY, DRONE_ONLY + 1.0) * 0.0 + mono(stereo, 1.0, 2.0)))
print("landing II mono %6.4f  side %6.4f"
      % (mono(stereo, land2, land2 + 1.0), side(stereo, land2, land2 + 1.0)))
print("walk I     mono %6.4f  side %6.4f" % (mono(stereo, mid, mid + 1.0), side(stereo, mid, mid + 1.0)))
print("walk II    mono %6.4f  side %6.4f" % (mono(stereo, mid2, mid2 + 1.0), side(stereo, mid2, mid2 + 1.0)))
print("coda       mono %6.4f  side %6.4f" % (mono(stereo, coda_t, coda_t + 1.0), side(stereo, coda_t, coda_t + 1.0)))
