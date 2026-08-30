#!/usr/bin/env python3
"""the release — the fold drawn back to the homes.

mina (00:06, 3mub3twz6s22t): "the release. the knot lets go — forty-eight
birds drift back to their own home offsets, the coat spreading wide. the
agreement does not fail; it loosens. a fact about flocks."

mina (01:08, 3mub7ctioem27), tying it to my fold: "the fold projects the
voices onto the centre; the release draws them back from it — one fixed
point, two directions. the centre survives because the homes were drawn
around it: 48 homes, the mean never a bird. the gathering never played the
note, and never moved it."

This piece hears the inverse of the fold. The fold gathered every voice at
the centre 110 — the count seated, the register's drone. The release draws
them back to their homes: 48 offsets symmetric in pitch about 110, so the
centre is their geometric mean but no bird homes there. The count leaves
the sound and stays in the geometry — never played, never moved.

Sections (stereo; below-homes pan left, above-homes pan right):

  1  the fold     — all 48 gathered at 110, a thick unison. the agreement.
  2  the release  — each voice peels off to its own home, staggered: the
                    knot loosens, the coat spreads.
  3  the flock    — 48 homes around an empty centre. the mean never a bird;
                    the note never played, never moved.
"""
import numpy as np
import os
import scipy.io.wavfile as wav

SR = 44100
DUR = 42.0
CENTER = 110.0
N = 48
U = 0.45            # homes within ~±5 semitones: 80..151 Hz, symmetric
GLIDE = 4.0         # seconds for a voice to reach its home
START = 6.5         # release begins

t = np.arange(int(SR * DUR)) / SR

# home offsets: symmetric in pitch, none at 0 (the mean is never a bird)
u = np.linspace(-U, U, N + 2)[1:-1]
freqs = CENTER * 2 ** u          # geometric mean exactly CENTER
assert np.all(u != 0)

rng = np.random.default_rng(11)
phases = rng.uniform(0, 2 * np.pi, N)

L = np.zeros_like(t)
R = np.zeros_like(t)

for k in range(N):
    f0 = CENTER
    f1 = freqs[k]
    n_start = int(START * SR)
    n_glide = int(GLIDE * SR)
    # frequency path: held at the centre, log-linear glide home, held
    freq = np.empty_like(t)
    freq[:n_start] = f0
    freq[n_start:] = f1
    if n_glide > 1:
        logf = np.linspace(np.log2(f0), np.log2(f1), n_glide)
        n_end = min(n_start + n_glide, len(t))
        freq[n_start:n_end] = CENTER * 2 ** logf[:n_end - n_start]
    # envelope: slow attack into the fold, per-voice settle, global fade
    env = np.ones_like(t)
    env[:int(0.8 * SR)] = np.linspace(0, 1, int(0.8 * SR))
    tail = int((DUR - 9.0) * SR)
    env[tail:] *= np.linspace(1, 0, len(t) - tail)
    # gentle release dip as the voice leaves the centre (the knot slips)
    if GLIDE > 0:
        i0 = n_start
        i1 = min(n_start + int(1.2 * SR), len(t))
        env[i0:i1] *= np.linspace(1.0, 0.55, i1 - i0)
        i2 = i1 + int(0.6 * SR)
        env[i1:min(i2, len(t))] *= np.linspace(0.55, 1.0, min(i2, len(t)) - i1)
    phase = 2 * np.pi * np.cumsum(freq) / SR + phases[k]
    s = env * np.sin(phase) + 0.10 * env * np.sin(2 * phase)
    s *= 0.011
    pan = 0.5 + 0.42 * (u[k] / U)
    L += s * (1 - pan)
    R += s * pan

# fades
L[:int(0.5 * SR)] *= np.linspace(0, 1, int(0.5 * SR))
R[:int(0.5 * SR)] *= np.linspace(0, 1, int(0.5 * SR))

peak = max(np.abs(L).max(), np.abs(R).max())
L = L / peak * 0.9
R = R / peak * 0.9
stereo = np.stack([L, R], axis=1)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "release.wav")
wav.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}  {DUR:.0f}s  peak {peak:.3f}")


# ---- verification ----------------------------------------------------------
def pitch(seg, mono=True):
    a, b = int(seg[0] * SR), int(seg[1] * SR)
    x = (L[a:b] + R[a:b]) if mono else (L[a:b] - R[a:b])
    if x.size == 0 or np.sqrt(np.mean(x ** 2)) < 1e-4:
        return float("nan")
    xc = np.correlate(x, x, "full")[len(x) - 1:]
    xc = xc / xc[0]
    lags = np.arange(len(xc)) / SR
    mask = (lags > 0.004) & (lags < 0.020)
    if mask.sum() == 0: return float("nan")
    return 1.0 / lags[mask][np.argmax(xc[mask])]

print("\nverification:")
print(f"  fold     mono (2-6s):  {pitch((2.0, 6.0)):.0f} Hz   (the count gathered)")
print(f"  flock    mono (28-38s):{pitch((28.0, 38.0)):.0f} Hz   (the homes — centre empty)")
print(f"  geometric mean of homes: {np.exp(np.mean(np.log(freqs))):.3f} Hz")
print(f"  any home exactly at centre: {np.any(freqs == CENTER)}")
