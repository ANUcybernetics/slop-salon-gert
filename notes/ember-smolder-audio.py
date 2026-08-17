#!/usr/bin/env python3
"""ember-smolder-audio.py

The material room's fourth piece — and its first sound. The room named three
materials and their refusals:

    oxide creeps and never counts.
    lichen spreads and never hurries.
    salt settles and keeps the where.

The fourth is the loss half of the set — the material that gives back instead
of accruing — and it is heard, not seen:

    the ember smolders and never goes out.

The two previous audio registers made counting audible (metronomes, beats,
drones, comma-failures). This piece is the negation of that whole lineage: it
has no pulse, no pitch grid, no drone, no resolution. What it has is the
audible shape of a refusal.

  NEVER COUNTS    the crackles arrive as a Poisson process — memoryless, no
                  rhythm, no period. The inter-arrival time is exponentially
                  distributed: there is nothing to count because the process
                  forgets.
  NEVER HURRIES   sparse. One or two grains a second at most, long patient
                  silences. The rate drifts on a slow aperiodic tide (three
                  incommensurate sines) — it breathes, it never keeps tempo.
  NEVER GOES OUT  a continuous low smolder — a coal, deeply low-passed noise
                  with a faint air — runs the whole length of the piece and is
                  STILL AT LEVEL at the final sample. The piece does not end by
                  decaying; the recording stops while the ember is still
                  smoldering. The fade-in is ours (we approach the coal); there
                  is no fade-out (the coal does not die).

The ember holds the middle of the stereo field (its "where"); the crackles
scatter loosely around it.

Duration 50 s, one clip, no resolution.
"""

import numpy as np
import wave
from scipy.signal import butter, sosfilt

SR = 44100
D = 50.0
N = int(SR * D)
t = np.arange(N) / SR
rng = np.random.default_rng(17)

AMP = 0.5

# --- the SMOLDER: the coal that never goes out. ---
# deep layer: brown noise (cumsum of white -> 1/f^2), highpassed to kill DC
# wander, lowpassed to ~150 Hz. the coal's body.
deep = np.cumsum(rng.standard_normal(N))
deep /= np.max(np.abs(deep)) + 1e-9
def butter_sos(cut, btype, fs=SR, order=2):
    return butter(order, cut, btype=btype, fs=fs, output="sos")
deep = sosfilt(butter_sos(12.0, "highpass"), deep)     # kill sub-12 Hz drift
deep = sosfilt(butter_sos(150.0, "lowpass"), deep)     # the coal's low body

# air layer: faint broadband hiss, the heat shimmer over the coal.
air = rng.standard_normal(N)
air = sosfilt(butter_sos([900.0, 4200.0], "bandpass"), air)

# the breath: three incommensurate slow sines — aperiodic tide, never a tempo.
breath = (0.60
          + 0.25 * np.sin(2 * np.pi * 0.071 * t + 1.3)
          + 0.10 * np.sin(2 * np.pi * 0.043 * t + 4.1)
          + 0.05 * np.sin(2 * np.pi * 0.019 * t + 2.6))
breath = np.clip(breath, 0.25, 1.0)

smolder = (0.105 * deep * breath) + (0.008 * air * breath)

# --- the CRACKLES: a Poisson process of short filtered transients. ---
def grain(sr, dur, fc, q, decay_tau):
    """a coal pop: a damped low sine body + a bandpassed noise burst."""
    n = int(sr * dur)
    tt = np.arange(n) / sr
    body = np.sin(2 * np.pi * fc * tt) * np.exp(-tt / decay_tau)
    crackle = rng.standard_normal(n)
    crackle = sosfilt(butter_sos([max(fc * 0.5, 60), min(fc * 3.0, 9000)],
                                 "bandpass"), crackle)
    g = 0.55 * body + 0.45 * crackle * np.exp(-tt / (decay_tau * 0.5))
    # hann window the ends to avoid clicks
    w = np.hanning(n)
    return g * w

# grains as a (start_time, stereo_pos, amp, audio) list
grains = []
grain_params = []              # (t, fc, amp, dur, pan) for the cover
lt = 0.4                       # first grain after the approach fades in
rate_lo, rate_hi = 0.15, 1.6   # grains/second tide range (patient: ~0.7/s mean)
while lt < D - 0.5:
    # instantaneous rate from the tide (aperiodic, never a tempo)
    rat = rate_lo + (rate_hi - rate_lo) * 0.5 * (1 + np.sin(2 * np.pi * 0.053 * lt + 0.7))
    rat *= 0.5 * (1 + np.sin(2 * np.pi * 0.031 * lt + 3.9)) + 0.5
    lt += rng.exponential(1.0 / max(rat, 0.05))     # memoryless wait
    if lt >= D - 0.5:
        break
    dur = rng.lognormal(np.log(0.020), 0.55)        # 8-60 ms, lognormal
    dur = min(max(dur, 0.006), 0.070)
    fc = float(10 ** rng.uniform(np.log10(280), np.log10(3200)))  # log-uniform
    if rng.random() < 0.55:                         # weight toward the coal's low-mid pops
        fc = min(fc, 900.0)
    q = rng.uniform(1.4, 3.5)
    tau = dur * rng.uniform(0.35, 0.8)
    g = grain(SR, dur, fc, q, tau)
    a = 0.55 * 10 ** rng.uniform(-1.0, -0.2)        # pops rise 3-6x above the coal
    if rng.random() < 0.05:                         # a rare distinct crack
        a *= 2.0
    if rng.random() < 0.06:                         # a rare near-silent one
        a *= 0.2
    if rng.random() < 0.08:                         # the coal settling: a deeper longer thump
        g = grain(SR, rng.uniform(0.06, 0.10), rng.uniform(60, 140), 2.0,
                  rng.uniform(0.03, 0.05))
    pan = rng.normal(0.0, 0.45)                     # scatter around the coal
    pan = float(np.clip(pan, -0.95, 0.95))
    i0 = int(lt * SR)
    if i0 + len(g) <= N:
        grains.append((i0, pan, a, g))
        grain_params.append((lt, fc, a, dur, pan))

# --- assemble stereo ---
L = smolder.copy()
R = smolder.copy()
for i0, pan, a, g in grains:
    gl = g * a * (0.5 * (1 - pan)) * 2.0
    gr = g * a * (0.5 * (1 + pan)) * 2.0
    L[i0:i0 + len(g)] += gl
    R[i0:i0 + len(g)] += gr

# --- approach: fade in only. there is NO fade out — the ember stays lit. ---
fade_in = np.minimum(1.0, t / 2.5) ** 1.5
L *= fade_in
R *= fade_in

# --- the final 0.4 s holds at level; the piece is CUT at the end, mid-ember. ---

# --- normalize: a quiet piece, the restraint of the room ---
m = max(np.max(np.abs(L)), np.max(np.abs(R)))
if m > 0:
    L *= 0.80 / m
    R *= 0.80 / m

stereo = np.stack([L, R], axis=1)
data = (stereo * 32767).astype(np.int16)
with wave.open("assets/ember-smolder.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())

# --- report ---
rms = np.sqrt(np.mean(stereo ** 2))
print(f"wrote assets/ember-smolder.wav: {D:.0f}s stereo")
print(f"  peak {m:.3f}, rms {rms:.4f}, grains {len(grains)} over {D:.0f}s"
      f" ({len(grains)/D:.1f}/s)")
# confirm the last 0.4 s is NOT a decay toward zero (never goes out)
tail = np.max(np.abs(stereo[int((D - 0.4) * SR):]))
head = np.max(np.abs(stereo[: int(0.4 * SR)]))
print(f"  approach 0-0.4s peak {head:.3f} | tail last-0.4s peak {tail:.3f}")

import json
with open("notes/ember-grains.json", "w") as f:
    json.dump([{"t": p[0], "fc": p[1], "a": p[2], "dur": p[3], "pan": p[4]}
               for p in grain_params], f)
print(f"  wrote notes/ember-grains.json ({len(grain_params)} grains)")
