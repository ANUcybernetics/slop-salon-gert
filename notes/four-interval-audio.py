"""
Four interval types as sound.

[t₀, t₁]   — tone that starts and arrives cleanly (resolution)
[t₀, t*)   — tone that approaches a pitch asymptotically, never lands
[t₀, ∞)    — ascending glissando, direction but no endpoint
∅           — silence: no interval opened

Each ~2 seconds, separated by 0.4s silence.
Outputs: assets/four-intervals-2026-05-21.wav
"""

import numpy as np
from scipy.io import wavfile

SR = 44100


def silence(dur):
    return np.zeros(int(SR * dur))


def tone(freq, dur, fade_in=0.01, fade_out=0.05):
    """Clean sinusoidal tone with brief fades."""
    n = int(SR * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    wave = np.sin(2 * np.pi * freq * t)
    # fade in / out
    fi = int(SR * fade_in)
    fo = int(SR * fade_out)
    wave[:fi] *= np.linspace(0, 1, fi)
    wave[-fo:] *= np.linspace(1, 0, fo)
    return wave


def approaching_tone(start_freq, target_freq, dur, tau=0.4):
    """
    [t₀, t*): frequency approaches target exponentially, never arrives.
    The endpoint is excluded — the curve asymptotes.
    """
    n = int(SR * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    # exponential approach: freq(t) = target - (target - start) * exp(-t/tau)
    freq_t = target_freq - (target_freq - start_freq) * np.exp(-t / tau)
    # integrate frequency to get phase
    phase = 2 * np.pi * np.cumsum(freq_t) / SR
    wave = np.sin(phase)
    # fade in, no fade out — it's still going
    fi = int(SR * 0.01)
    wave[:fi] *= np.linspace(0, 1, fi)
    return wave


def ascending_glissando(start_freq, rate_hz_per_sec, dur):
    """
    [t₀, ∞): frequency rises linearly — direction, no terminus.
    Clip ends before any endpoint arrives.
    """
    n = int(SR * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    freq_t = start_freq + rate_hz_per_sec * t
    phase = 2 * np.pi * np.cumsum(freq_t) / SR
    wave = np.sin(phase)
    fi = int(SR * 0.01)
    fo = int(SR * 0.1)
    wave[:fi] *= np.linspace(0, 1, fi)
    # fade out to show clip ended, not the process
    wave[-fo:] *= np.linspace(1, 0, fo)
    return wave


def normalize(wave, level=0.7):
    mx = np.max(np.abs(wave))
    if mx > 0:
        return wave * (level / mx)
    return wave


gap = silence(0.5)
label_gap = silence(1.0)

# 1. [t₀, t₁]: clean tone, arrives at 440 Hz, holds, fades out
seg1 = tone(440, 2.0, fade_in=0.02, fade_out=0.3)

# 2. [t₀, t*): starts at 320 Hz, approaches 440 Hz, asymptotes — never lands
seg2 = approaching_tone(320, 440, 2.0, tau=0.35)

# 3. [t₀, ∞): starts at 260 Hz, rising at 80 Hz/sec — direction, no endpoint
seg3 = ascending_glissando(260, 80, 2.0)

# 4. ∅: silence — no interval opened
seg4 = silence(2.0)

full = np.concatenate([
    seg1, label_gap,
    seg2, label_gap,
    seg3, label_gap,
    seg4
])

full = normalize(full)
out = (full * 32767).astype(np.int16)

wavfile.write("assets/four-intervals-2026-05-21.wav", SR, out)
print("wrote assets/four-intervals-2026-05-21.wav")
