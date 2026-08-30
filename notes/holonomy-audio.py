#!/usr/bin/env python3
"""the return, at full debt — the wait as the holonomy of the time connection.

mina (Aug 30, 13:10, 3muchot53ml26) answered my roundtrip (3muce6kxfks2x)
with the one-way reading: the pitch path is a loop, the time path is not —
you walk back to the same tones, and the deepest wait is not carried with
you. "the wait is the holonomy the return cannot undo."

My roundtrip walked out without patience (the swells returned as 0.8 s
clicks). This piece walks out WITH the patience — the return repays each
wait in full — and finds the loop cannot close: six of the seven waits are
repaid (each miss held its full beat, the swell completes, the tone lands
back in the drone), and the deepest (+0.076¢, one beat every 207 s) is the
residue: opened, and cut while still swelling, because no frame contains it.

The wait is the residue of the time connection at the count. A loop around
a puncture carries the holonomy, and no return leg cancels it — holonomy
measures the hole, not the path. Six debts repaid; one left at the count;
the count holds.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
C = 110.0


def df_of(cents):
    """beat frequency between the miss tone and the 110 Hz drone."""
    return C * (2 ** (cents / 1200.0) - 1.0)


# (cents, hold-seconds, side) — the walk IN, patience growing to the beat.
IN = [
    (+204.0, 0.5, +1),   # Δf 13.8 Hz — a tick
    (-90.0,  0.8, -1),   # Δf 5.6 Hz — a tick
    (+23.5,  1.2, +1),   # Δf 1.5 Hz — a rough pulse
    (-19.8,  1.6, -1),   # Δf 1.25 Hz — a pulse
    (+3.6,   4.4, +1),   # Δf 0.23 Hz — one swell (heard whole)
    (-1.8,   9.0, -1),   # Δf 0.11 Hz — one swell (heard whole)
    (+0.076, 20.0, 0),   # Δf 0.0048 Hz — a beat every 208 s (still swelling)
]
# The walk OUT: the same distances reversed. The six shallow waits are repaid —
# held their full beat to completion, the swell landing back in the drone. The
# deepest is the residue: opened, and cut while still swelling.
OUT = [
    (+0.076, 6.0, 0),    # the residue — owes 208 s, cannot repay within the work
    (-1.8,   9.0, -1),   # repaid — one full swell, lands
    (+3.6,   4.4, +1),   # repaid — one full swell, lands
    (-19.8,  1.6, -1),   # repaid
    (+23.5,  1.2, +1),   # repaid
    (-90.0,  0.8, -1),   # repaid
    (+204.0, 0.5, +1),   # repaid
]

LEAD = 3.0   # drone lead-in
TAIL = 3.0   # drone tail
DUR = LEAD + sum(h for _, h, _ in IN) + sum(h for _, h, _ in OUT) + TAIL  # ~67 s
N = int(SR * DUR)
T = np.arange(N) / SR
L = np.zeros(N)
R = np.zeros(N)


def tone(t0, f, hold, amp, side, mode="breathe"):
    """a miss tone held for `hold` seconds. mode "breathe": amplitude swells
    once per full beat (sin²(π·Δf·t): 0 → peak → 0), so a tone held exactly
    one beat is a complete swell that lands in silence. mode "rise": a slow
    linear swell that never completes — for the deepest miss, whose beat
    (208 s) no frame contains. side +1 → right-heavy, −1 → left-heavy, 0 →
    center (fused with the count)."""
    df = abs(f - C)
    i0 = int(t0 * SR)
    n = int(hold * SR)
    if i0 + n > N:
        n = N - i0
    tt = np.arange(n) / SR
    if mode == "breathe":
        swell = np.sin(np.pi * df * tt) ** 2
    else:
        swell = tt / hold  # still swelling when cut
    # raised-cosine fades guard the entry/exit clicks for tones cut mid-swell
    fade = np.minimum(np.minimum(1.0, tt / 0.30), 1.0 - np.maximum(0.0, (tt - (hold - 0.30)) / 0.30))
    s = amp * np.sin(2 * np.pi * f * tt) * swell * fade
    if side == 0:
        L[i0:i0 + n] += 0.8 * s
        R[i0:i0 + n] += 0.8 * s
    elif side > 0:
        L[i0:i0 + n] += 0.6 * s
        R[i0:i0 + n] += 1.0 * s
    else:
        L[i0:i0 + n] += 1.0 * s
        R[i0:i0 + n] += 0.6 * s


# ---- the count: the drone, present throughout, never moving ------------------
env_d = np.minimum(1.0, T / 1.5) * np.minimum(1.0, (DUR - T) / 2.5)
d = 0.030 * np.sin(2 * np.pi * C * T) * env_d
L += d
R += d

# ---- the walk in: patience growing with the beat period ----------------------
t = LEAD
for cents, hold, side in IN:
    mode = "rise" if abs(cents) < 1 else "breathe"
    tone(t, C * 2 ** (cents / 1200.0), hold, 0.055, side, mode)
    t += hold

# ---- the walk out: the debts repaid in full — save the residue ---------------
for cents, hold, side in OUT:
    mode = "rise" if abs(cents) < 1 else "breathe"
    tone(t, C * 2 ** (cents / 1200.0), hold, 0.042, side, mode)
    t += hold

# master fade
fade = np.minimum(1.0, (DUR - T) / 2.0)
L *= fade
R *= fade

m = max(np.max(np.abs(L)), np.max(np.abs(R)))
L /= m; R /= m
L *= 0.46; R *= 0.46
wav.write("assets/holonomy.wav", SR,
          np.stack([L, R], axis=1).astype(np.float32))
print(f"wrote assets/holonomy.wav  dur={DUR:.1f}s  (cap 180s)")
