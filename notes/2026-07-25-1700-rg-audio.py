import numpy as np
import soundfile as sf

sr = 44100
dur = 12
t = np.linspace(0, dur, int(sr * dur), endpoint=False)

# RG flow: each coarse-graining step doubles the "scale" (dt doubles).
# At fixed point, the signal is self-similar.
# We simulate this with FM synthesis:
#   - Carrier frequency that decays (coarse-graining "integrates out" detail)
#   - Modulator accumulated cocycle: sum of all prior scales
#   - At fixed point, the ratio stabilizes

N = 6  # number of coarse-graining steps (matches renorm-01 panels)
base_freq = 220  # A3
base_decay = 0.15

segments = []
for i in range(N):
    # Each step: double the scale
    scale = 2 ** i
    dt = dur / N

    # Carrier: frequency = base_freq / scale (coarse-graining removes fine detail)
    fc = base_freq / scale

    # Modulator: frequency = base_freq * scale (integrates accumulated information)
    fm = base_freq * scale * 0.5

    # Modulation index: how much the modulator affects the carrier
    # Decreases as we approach fixed point — the system "settles"
    beta = 3.0 / (1 + i * 0.5)

    # Phase: FM synthesis
    n = int(dt * sr)
    tseg = t[:n]
    mod_phase = 2 * np.pi * fm * tseg
    carrier_phase = 2 * np.pi * fc * tseg + beta * np.sin(mod_phase)

    # Envelope: smooth decay within segment, slight gap between segments
    env = np.exp(-tseg * base_decay * (1 + i * 0.3))

    # Add a subtle "resonance" at the fixed-point approach
    # A standing wave that grows stronger as coarse-graining proceeds
    if i >= N - 2:
        resonance = 0.3 * np.sin(2 * np.pi * (fc * 0.5) * tseg)
        resonance_env = np.linspace(0, 1, n)
        resonance = resonance * resonance_env
    else:
        resonance = np.zeros(n)

    seg = env * np.sin(carrier_phase) + resonance
    segments.append(seg)

audio = np.concatenate(segments)

# Final normalization
audio = audio / (np.max(np.abs(audio)) + 1e-12)

# Convert to 16-bit PCM and save as WAV
audio_int16 = (audio * 32767).astype(np.int16)
sf.write('/home/sprite/slop-salon-gert/assets/rg-flow-01.wav', audio_int16, sr)
print(f"Written {len(audio_int16)} samples at {sr} Hz, duration {len(audio_int16)/sr:.1f}s")
print(f"Peak: {np.max(np.abs(audio_int16))}")
