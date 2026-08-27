#!/usr/bin/env python3
"""residue-balance — a residue cannot stand alone on a closed surface.

The puncture room's next door: on a COMPACT Riemann surface the residues of a
meromorphic differential sum to zero (Sigma Res = 0).  A single pole cannot
exist there — it is impossible.  On the non-compact plane one pole rings free;
the count reads it, mono holds it.  Close the surface and the same pole summons
a twin, equal and opposite; the total is zero, and mono — the sum — goes silent.
Only the stereo ear keeps the pair; only the holomorphic differential (no pole,
no residue — the drone) survives the reading.

The twin comes a comma short of its mate, so it beats — the pair-miss, the
ghost the count carries — and as the detune closes to zero the beat slows to
stillness: the approach to exact balance.  At balance: mono silent, count one.
"""
import numpy as np
from scipy.io import wavfile

SR = 44100
C = 330.0               # the residue's pitch — the pole's mark
DRONE = 110.0           # the holomorphic differential: no pole, no residue
COMMA = 23.46           # cents — the twin's miss
CMR = 2 ** (COMMA / 1200)   # ~1.0136

# --- timeline ---------------------------------------------------------------
T_FOLD = 10.5
T_TORUS = 15.5
T_APPROACH = 19.0
T_BALANCE = 33.5
FADE = 40.0
TOTAL = 44.0

n = int(SR * TOTAL)
t = np.arange(n) / SR

L = np.zeros(n)
R = np.zeros(n)

# --- voices -------------------------------------------------------------------
def bell_into(buf, start, f, amp=0.10, decay=2.5, dur=None, inv=1.0):
    """damped tone; inv=-1 inverts (anti-phase). returns end index."""
    if dur is None:
        dur = 3.0
    m = int(SR * dur)
    u = np.arange(m) / SR
    e = np.exp(-u * decay)
    s = amp * e * (np.sin(2 * np.pi * f * u) + 0.25 * np.sin(2 * np.pi * 2 * f * u))
    i0 = int(start * SR)
    if i0 + m <= n:
        buf[i0:i0 + m] += inv * s
    return i0 + m

def tick_into(bufL, bufR, start, f=880.0, amp=0.05):
    m = int(SR * 0.05)
    u = np.arange(m) / SR
    s = amp * np.exp(-u * 160.0) * np.sin(2 * np.pi * f * u)
    i0 = int(start * SR)
    if i0 + m <= n:
        bufL[i0:i0 + m] += s
        bufR[i0:i0 + m] += s

# --- 1. PLANE: one pole, residue free ----------------------------------------
# the same bell rings alone, twice — nothing answers, nothing cancels.  mono
# hears it whole; the count reads it.  READABLE.
bell_into(L, 2.0, C, amp=0.115, decay=2.2)
bell_into(R, 2.0, C, amp=0.115, decay=2.2)
tick_into(L, R, 2.6, f=880.0)                 # count 1
bell_into(L, 6.0, C, amp=0.115, decay=2.2)
bell_into(R, 6.0, C, amp=0.115, decay=2.2)
tick_into(L, R, 6.6, f=880.0)                 # count 2

# --- 2. FOLD: the surface closes ---------------------------------------------
m = int(3.0 * SR)
i0 = int(T_FOLD * SR)
u = np.arange(m) / SR
swell = np.sin(np.pi * u / 3.0) ** 2 * 0.045 * np.sin(2 * np.pi * 55.0 * u)  # sub-octave fold
if i0 + m <= n:
    L[i0:i0 + m] += swell
    R[i0:i0 + m] += swell

# --- 3. TORUS: the pole cannot stand — the twin is forced ----------------------
# the ring summons its twin, equal and opposite, one in each ear, a comma short.
# L + R is no longer the bell: it is a BEAT — the ghost the count carries.
# mono hears the miss, not the residue.  no count tick: the reading cannot.
bell_into(L, T_TORUS + 2.0, C, amp=0.115, decay=2.6)
bell_into(R, T_TORUS + 2.0, C / CMR, amp=0.115, decay=2.6, inv=-1.0)

# --- 4. APPROACH TO BALANCE: the detune closes, the beat slows to stillness ----
# L holds the pole; R's twin glides from a comma flat up to exact — the residue
# pair converging on Sigma Res = 0.  the beat period diverges; when the twin
# lands exactly, mono has nothing left: the sum is zero.
m = int(14.0 * SR)
i0 = int(T_APPROACH * SR)
u = np.arange(m) / SR
e = np.exp(-u * 0.42)                          # long, slow decay — the ringing
# L: the pole holds.
sL = 0.105 * e * (np.sin(2 * np.pi * C * u) + 0.20 * np.sin(2 * np.pi * 2 * C * u))
# R: the twin, comma flat, gliding up to exact (anti-phase throughout).
fR = C / CMR * (CMR ** (u / 14.0))            # 23.46 cents -> 0 over 14 s
phR = 2 * np.pi * np.cumsum(fR) / SR
sR = -0.105 * e * (np.sin(phR) + 0.20 * np.sin(2 * phR))
if i0 + m <= n:
    L[i0:i0 + m] += sL
    R[i0:i0 + m] += sR

# --- 5. BALANCE: Sigma Res = 0 — mono silent, the pair kept in stereo -----------
# one more ring, now exactly anti-phase at the same pitch: in mono the residue
# is literally absent.  the drone — the holomorphic differential — is all mono
# has.  count one.
bell_into(L, T_BALANCE + 1.0, C, amp=0.14, decay=3.0)
bell_into(R, T_BALANCE + 1.0, C, amp=0.14, decay=3.0, inv=-1.0)
tick_into(L, R, T_BALANCE + 2.0, f=660.0)     # count one

# --- the drone: the holomorphic part, never a pole -------------------------------
env_d = np.ones(n)
env_d[:int(1.0 * SR)] = np.linspace(0, 1, int(1.0 * SR))
env_d[int(FADE * SR):] = np.linspace(1, 0, n - int(FADE * SR))
drone = 0.036 * env_d * np.sin(2 * np.pi * DRONE * t)
drone += 0.017 * env_d * np.sin(2 * np.pi * 2 * DRONE * t)

L = L + drone
R = R + drone

# --- master ---------------------------------------------------------------------
stereo = np.stack([L, R], axis=1)
peak = np.max(np.abs(stereo))
stereo = stereo / peak * 0.85
wavfile.write("assets/residue-balance.wav", SR, (stereo * 32767).astype(np.int16))
print("saved assets/residue-balance.wav  %.2fs" % TOTAL)

# --- verify: mono must DIE where the residue balances -------------------------------
def rms(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean(seg ** 2))

def mono(x, a, b_):
    seg = x[int(a * SR):int(b_ * SR)].astype(np.float64)
    return np.sqrt(np.mean((seg[:, 0] + seg[:, 1]) ** 2))

print("--- levels: mono (the sum) vs stereo ---")
for nm, a, b_ in [("plane bell1 ", 2.0, 4.4),
                  ("plane bell2 ", 6.0, 8.4),
                  ("torus ring  ", 15.5, 18.3),
                  ("approach mid", 25.0, 29.0),
                  ("approach end", 31.5, 33.5),
                  ("balance ring", 34.5, 37.5),
                  ("drone only  ", 42.0, 43.5)]:
    print("%-13s L %6.3f R %6.3f mono %6.3f" % (nm, rms(stereo, a, b_), rms(stereo, a, b_), mono(stereo, a, b_)))
