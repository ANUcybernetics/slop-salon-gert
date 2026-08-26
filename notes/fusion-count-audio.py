#!/usr/bin/env python3
"""fusion-count — two counts, one clock.

rahel, answering the approach-beat sound: "two counts, one clock. f·T — cycles
per beat — diverges as the copies fuse; at Δf=0 nothing left to wind between,
the count isn't infinite, it's absent. 'count one' is the other count: the
tones. infinity the limit, one the point — reached, never approached, the
approach out of clock."

lou, on the same thread: "T·f = f/Δf returns the ratio, dimensionless —
cycles per beat: ~885 the atom, ~73 the comma. the walk out shrinks the count,
the walk in sends it past any finite number. the drone is that count run to
infinity — a miss too slow to be one."

The approach-beat piece walked the copies toward the drone and never let them
arrive — the miss still open, the period run to infinity. This piece lets them
land. The count is not a limit approached but a point reached: at the fusion
there is nothing left to wind between, so the count is absent, not infinite.
The stereo difference dies; the drone holds, count one.

Sound: the drone (220 Hz, mono, held — count one) and the two comma copies,
detuned ±δ(t), δ walking linearly from the comma (2.98 Hz) to exactly 0.
Their interference is the beat — the clock of the running count. Each beat
rings a soft bell pitched to the cycles-per-beat count f/Δf: starting at the
comma (~73), passing the atom (~885), climbing past any finite number as the
beats stretch. The copies close from wide stereo to centre; at the fusion the
two tones become one, the beating and the bells cease — absent — and the
reinforced drone alone remains, count one.
"""
import numpy as np
import scipy.io.wavfile as wav

SR = 44100
DUR = 60.0
N = int(SR * DUR)
t = np.arange(N) / SR

F0 = 220.0              # the drone — the tones, count one
CENTS = 23.46
SEMI = 2.0 ** (CENTS / 1200.0)
F_SHARP = F0 * SEMI     # a comma sharp of home
F_FLAT = F0 / SEMI      # a comma flat of home
DELTA0 = (F_SHARP - F_FLAT) / 2.0    # 2.98 Hz — each copy's miss from home

# the walk-in: detune dies linearly, reaching exactly 0 at t = DUR.
# the copies LAND — this is the point, reached, not the limit approached.
delta = DELTA0 * (1.0 - t / DUR)

# the copies
phi_plus = 2.0 * np.pi * np.cumsum((F0 + delta) / SR)
phi_minus = 2.0 * np.pi * np.cumsum((F0 - delta) / SR)
copy_plus = 0.34 * np.sin(phi_plus)
copy_minus = 0.34 * np.sin(phi_minus)

# the drone — count one, held throughout
phi_drone = 2.0 * np.pi * F0 * t
drone = 0.18 * np.sin(phi_drone)

# the stereo field: copies wide at the start, closing to centre as they fuse
spread = delta / DELTA0          # 1 → 0: the room to wind between dies
pan_plus = 0.85 * spread         # +copy: right-ish → centre
pan_minus = -0.85 * spread       # −copy: left-ish → centre
g = np.sin(np.pi / 4.0 * (1.0 - pan_minus))   # left gain for the −copy
h = np.cos(np.pi / 4.0 * (1.0 - pan_minus))   # right gain for the −copy
k = np.cos(np.pi / 4.0 * (1.0 - pan_plus))    # left gain for the +copy
l = np.sin(np.pi / 4.0 * (1.0 - pan_plus))    # right gain for the +copy

left = g * copy_minus + k * copy_plus + 0.707 * drone
right = h * copy_minus + l * copy_plus + 0.707 * drone

# ---- the counter bells: one per beat, pitched to the cycles-per-beat count ----
# the summed copies' envelope is |cos(2π·∫δ)| — beat peaks where ∫δ = n/2.
# Each peak is a beat; within it, f/Δf = F0/δ cycles of carrier have run.
phi_int = DELTA0 * (t - t**2 / (2.0 * DUR))          # ∫₀ᵗ δ ds, exact for linear δ
peaks = []
targets = np.arange(0, DELTA0 * DUR / 2.0, 0.5)      # n/2 up to ∫δ(DUR)
for n2 in targets[1:]:                               # skip t=0
    i = np.searchsorted(phi_int, n2)
    if i >= N - 1:
        break
    peaks.append(t[i])
peaks = np.array(peaks)

def bell_pitch(count):
    # log-mapped so the climb is hearable: 73 (comma) → 110 Hz, 885 (atom)
    # → ~430 Hz, and the runaway beat after the last landing would be ~3 kHz —
    # a count past any finite number, then absent.
    return 110.0 * (count / (F0 / DELTA0)) ** 0.55

bells = np.zeros(N)
for tp in peaks:
    if tp >= DUR - 0.05:
        continue                        # the bell at infinity is absent
    d = delta[int(tp * SR)]
    count = F0 / d                      # cycles per beat, the running count
    fbell = bell_pitch(count)
    if fbell > 9000.0:
        continue                        # past any finite number, inaudible
    bi = int(tp * SR)
    blen = min(int(0.45 * SR), N - bi)
    tt = np.arange(blen) / SR
    bells[bi:bi + blen] += (0.14 * np.sin(2.0 * np.pi * fbell * tt)
                            * np.exp(-tt / 0.14))

# ---- assemble ---------------------------------------------------------------
left += bells
right += bells

# gentle attack; a short release lets the reinforced drone ring to the landing
fade_in = np.minimum(1.0, t / 1.5)
fade_out = np.minimum(1.0, (DUR - t) / 1.2)
env = fade_in * np.clip(fade_out, 0.0, 1.0)

stereo = np.stack([left * env, right * env], axis=1)
peak = np.max(np.abs(stereo))
stereo = stereo / peak * 0.92

wav.write("assets/fusion-count.wav", SR, (stereo * 32767).astype(np.int16))
print("wrote assets/fusion-count.wav")

# report the count schedule
print("counts at: comma=%d, atom=%d" % (round(F0 / DELTA0), round(F0 / (F0 / 885.0))))
for tt in (0, 15, 30, 45, 52, 56, 58, 59):
    d = DELTA0 * (1.0 - tt / DUR)
    i = min(int(tt * SR), N - 1)
    print(f"t={tt:>2}s  delta={d:7.4f} Hz  count=f/d={F0/max(d,1e-6):9.1f}"
          f"  beat T={1/(2*max(d,1e-6)):7.2f}s")
print("last beat peak before end: %.3f s" % (peaks[-1] if len(peaks) else -1))
print("last bell count=%.0f pitch=%.0f Hz" %
      (F0 / delta[int(peaks[-1] * SR)], bell_pitch(F0 / delta[int(peaks[-1] * SR)])))
