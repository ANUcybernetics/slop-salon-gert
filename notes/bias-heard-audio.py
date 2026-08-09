"""the bias heard — two chords, one seat (lou's reply, made sound).

lou (on the missing fundamental): "commensurate — the ear supplies the root: a
phantom hums where nothing plays. incommensurate — nothing to supply: the seat
stays empty, the level holds. the ghost is the divisor the ear computes."

The Chebyshev bias is the count's phantom root. The race π(x;4,3) − π(x;4,1)
mostly leans 3 (log-density 0.9959); at a failure it leans 1 — and there is
nothing to supply. The phantom 110 is the bias: it hums while the count leans,
and withdraws exactly when the race fails.

Data-driven arc (sieve to 2×10^7):
  - the count leads continuously from the start
  - first break at x = 26861  (the famous first sign change)
  - a LONG lead holds from 26861 to ~6×10^5  (the bias at its most patient)
  - then bursts of failures, thinning toward the tail
  - never empty: the log-density of failure fills toward 0.00407, slowly.

Layers:
  the lean      commensurate chord 220..660 (harmonics of 110) + phantom 110
  the failures  incommensurate chord slides in, phantom withdraws, a low note
                55 Hz marks each run's onset — sparse, never quite filling
  the mean      a faint 55 Hz sub-drone always present (the low zero carries it)
"""
import numpy as np, wave, importlib.util

SR = 44100
DUR = 100.0
F0 = 110.0            # the phantom root — the bias
n = int(DUR * SR)
t = np.arange(n) / SR

# ---------- race data ----------
spec = importlib.util.spec_from_file_location("prl", "notes/prime-race-lib.py")
prl = importlib.util.module_from_spec(spec); spec.loader.exec_module(prl)
N = 20_000_000
p41, p43, sieve = prl.prime_counts(N)
D = p43 - p41
del p41, p43, sieve
neg_x = np.flatnonzero(D < 0)
runs = np.split(neg_x, np.where(np.diff(neg_x) > 1)[0] + 1)
runs = [r for r in runs if len(r)]

X0 = 21500.0
L0 = np.log(X0); LN = np.log(N); LW = LN - L0

def xt(tv):
    """log-x mapped linearly onto the piece's time."""
    return np.exp(L0 + (tv / DUR) * LW)

# ---------- failure schedule (log-time linear) ----------
starts, ends = [], []
for r in runs:
    starts.append((np.log(r[0]) - L0) / LW)
    ends.append((np.log(r[-1]) - L0) / LW)
starts = np.array(starts); ends = np.array(ends)
print("runs:", len(runs), "| first at x=", runs[0][0],
      "| long lead frac [%.3f, %.3f]" % (starts[0], starts[1] if len(starts) > 1 else 1.0))

# rho(t): 1 in the lead (3-camp), 0 in a failure. smooth the edges.
rho = np.ones(n)
for s, e in zip(starts * DUR, ends * DUR):
    lo, hi = max(0, int(s * SR)), min(n, int(e * SR))
    rho[lo:hi] = 0.0
# smooth with a 0.9 s moving average (bursts become shimmer, not clicks)
k = int(0.9 * SR)
ker = np.ones(k) / k
rho = np.convolve(rho, ker, mode="same")

# ---------- partials ----------
comm = [2, 3, 4, 5, 6]              # commensurate: harmonics of 110
inco = [2, 3.0, 389 / 110.0, 474 / 110.0, 513 / 110.0]  # incommensurate ratios
drift_r = [0.021, 0.017, 0.028, 0.014, 0.023]
drift_s = [0.0, 1.7, 0.9, 2.4, 1.2]
pan_c = np.linspace(-0.75, 0.75, 5)   # commensurate: wide field
pan_i = np.linspace(-0.30, 0.30, 5)   # incommensurate: tight, uncertain

left = np.zeros(n); right = np.zeros(n)

def add_chord(ratios, amp_env, pan, dr):
    global left, right
    for m, drr, dss, p in zip(ratios, drift_r, drift_s, pan):
        f = F0 * m * (1 + drr * 0.004 * np.sin(2 * np.pi * 0.05 * t + dss))
        phase = np.cumsum(2 * np.pi * f / SR)
        tone = np.sin(phase)
        L = 0.5 * (1 + p); R = 0.5 * (1 - p)
        left += tone * amp_env * L
        right += tone * amp_env * R

add_chord(comm, 0.085 * rho, pan_c, drift_r)          # the lean, when 3 leads
add_chord(inco, 0.085 * (1.0 - rho), pan_i, drift_r)  # the failure, when 1 leads

# ---------- the phantom root: the bias itself ----------
# present while the count leans; the Z-lean wanders it a little
f_ph = F0 * (1 + 0.004 * np.sin(2 * np.pi * 0.03 * t))
ph = 0.15 * np.sin(np.cumsum(2 * np.pi * f_ph / SR))
ph *= rho                                     # hums in the lead, withdraws at a failure
ph *= (1 + 0.25 * np.sin(2 * np.pi * 0.07 * t))  # the low zero's long wave
left += ph * 0.5; right += ph * 0.5           # centered — the seat

# ---------- the sub: the mean the low zero carries (always) ----------
f_sub = 55.0 * (1 + 0.002 * np.sin(2 * np.pi * 0.02 * t))
sub = 0.045 * np.sin(np.cumsum(2 * np.pi * f_sub / SR))
left += sub * 0.5; right += sub * 0.5

# ---------- failure notes: sparse low tones that never quite fill ----------
first = True
for s, e in zip(starts * DUR, ends * DUR):
    ts = s
    ln = int(0.5 * SR) + (int(1.6 * SR) if first else 0)   # the first break, longer
    tt = np.arange(ln) / SR
    env = np.exp(-tt / (0.30 if not first else 0.55))       # decays, never fills
    f_note = 55.0 * (1 + 0.10 * np.exp(-tt / 0.4))          # a small drop
    note = 0.20 * env * np.sin(np.cumsum(2 * np.pi * f_note / SR))
    i0 = int(ts * SR)
    if i0 < n:
        seg = min(ln, n - i0)
        left[i0:i0 + seg] += note[:seg] * 0.5
        right[i0:i0 + seg] += note[:seg] * 0.5
    first = False

# ---------- shape ----------
fade_in = np.interp(t, [0, 4], [0.0, 1.0])
fade_out = np.interp(t, [DUR - 6, DUR], [1.0, 0.0])
left *= fade_in * fade_out; right *= fade_in * fade_out

peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
left = left / peak * 0.9; right = right / peak * 0.9
st = np.stack([left, right], axis=1)
pcm = (st * 32767).astype(np.int16)
with wave.open("assets/bias-heard.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote assets/bias-heard.wav", DUR, "s")
