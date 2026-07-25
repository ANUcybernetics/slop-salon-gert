"""
Character table → audio.

Characters as frequency carriers. Character table structure as rhythm.
- χ(e) = dim → identity pulse
- χ(g≠e) for regular rep = 0 → gaps between pulses
- Complex characters → phase modulation
- Multiple groups = multi-panel piece
"""

import numpy as np
import struct
import wave
import subprocess
from PIL import Image, ImageDraw

sr = 44100
dur = 12.0
t = np.arange(int(sr * dur)) / sr

# Groups: (name, character_table_as_complex_array)
def z4():
    n = 4
    return np.exp(2j * np.pi * np.arange(n)[:, None] * np.arange(n)[None, :] / n), "Z4"

def z6():
    n = 6
    return np.exp(2j * np.pi * np.arange(n)[:, None] * np.arange(n)[None, :] / n), "Z6"

def s3():
    # S3: 3 irreps, 3 classes
    return np.array([
        [1+0j,  1+0j,  1+0j],
        [1+0j, -1+0j,  1+0j],
        [2+0j,  0+0j, -1+0j],
    ]), "S3"

def d4():
    # D4: 5 irreps, 5 classes
    return np.array([
        [1+0j,  1+0j,  1+0j,  1+0j,  1+0j],
        [1+0j,  1+0j,  1+0j, -1+0j, -1+0j],
        [1+0j, -1+0j,  1+0j,  1+0j, -1+0j],
        [1+0j, -1+0j,  1+0j, -1+0j,  1+0j],
        [2+0j,  0+0j, -2+0j,  0+0j,  0+0j],
    ]), "D4"

groups = [z4(), z6(), s3(), d4()]
group_duration = dur / len(groups)  # 3s each

base_freq = 130  # Hz (close to C3)

audio_stereo = np.zeros((int(sr * dur), 2))

for idx, (chars, name) in enumerate(groups):
    n_irreps, n_classes = chars.shape
    t_seg = np.arange(int(sr * group_duration)) / sr

    for i, chi in enumerate(chars):
        degree = np.abs(chi[0])  # χ(e) = dimension
        freq = base_freq * degree

        # Amplitude: stronger characters get louder
        amp = 0.12 / n_irreps

        # Phase: real part → frequency detuning, imag → phase shift
        phases = np.angle(chi)

        for j, (ch, phi) in enumerate(zip(chi, phases)):
            seg_start = int(j * len(t_seg) / n_classes)
            seg_end = int((j + 1) * len(t_seg) / n_classes)
            mask = np.zeros(len(t_seg), dtype=bool)
            mask[seg_start:seg_end] = True

            if not np.any(mask):
                continue

            t_local = t_seg[seg_start:seg_end]
            t_frac = np.arange(len(t_local)) / sr

            # Frequency: detuned by real character value
            detuning = np.real(ch) * 30
            f = freq + detuning

            # Phase accumulation
            phase = 2 * np.pi * f * t_frac + phi * np.sin(np.pi * t_frac / group_duration)

            # Envelope: decay within segment
            env = np.exp(-t_frac * 3.0)

            # Identity class (j=0): full pulse
            if j == 0:
                env = env * np.ones_like(t_local)
                # Add second harmonic
                audio_stereo[seg_start:seg_end, 0] += amp * env * (
                    np.sin(phase) + 0.3 * np.sin(2 * phase)
                )
                audio_stereo[seg_start:seg_end, 1] += amp * env * (
                    np.sin(phase) + 0.25 * np.sin(2 * phase + 0.1)
                )
            else:
                # Non-identity: softer, with character-phase modulation
                audio_stereo[seg_start:seg_end, 0] += amp * 0.4 * env * np.sin(phase)
                audio_stereo[seg_start:seg_end, 1] += amp * 0.35 * env * np.sin(phase + 0.05)

# Normalize
max_val = np.max(np.abs(audio_stereo))
if max_val > 0:
    audio_stereo /= max_val
audio_stereo *= 0.65

# Save WAV
audio_int16 = (audio_stereo * 32767).astype(np.int16)
audio_path = '/home/sprite/slop-salon-gert/assets/character-comb-01.wav'
with wave.open(audio_path, 'w') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(audio_int16.tobytes())

# Create 4-panel cover
def make_char_image(name, chars):
    n_irreps, n_classes = chars.shape
    w, h = 400, 300
    img = Image.new('RGB', (w, h), '#0a0a0f')
    draw = ImageDraw.Draw(img)

    pad = 30
    header_y = pad
    row_h = (h - pad * 2) / (n_irreps + 1)
    col_w = (w - pad * 2 - 50) / n_classes

    draw.text((pad, header_y), name, fill='white')

    # Column headers
    for j in range(n_classes):
        x = pad + col_w * j + col_w / 2
        draw.text((x - 10, header_y + row_h), str(j + 1), fill='#888')

    # Rows
    for i in range(n_irreps):
        y = header_y + row_h * (i + 1) + row_h / 2 - 8
        label = f"χ_{i+1}"
        draw.text((pad - 35, y), label, fill='#aaa')

        for j, val in enumerate(chars[i]):
            x = pad + col_w * j + col_w / 2 - 15
            if np.isclose(np.imag(val), 0):
                text = f"{np.real(val):+.0f}"
            else:
                text = f"{np.real(val):+.0f}{np.imag(val):+.0f}i"
            draw.text((x, y), text, fill='white')

    return img

# Build multi-panel
cover = Image.new('RGB', (800, 600), '#0a0a0f')
for idx, (chars, name) in enumerate(groups):
    panel = make_char_image(name, chars)
    col = idx % 2
    row = idx // 2
    cover.paste(panel, (col * 400, row * 300))

cover_path = '/home/sprite/slop-salon-gert/assets/character-comb-01.png'
cover.save(cover_path)

# Encode video
video_path = '/home/sprite/slop-salon-gert/assets/character-comb-01.mp4'
subprocess.run([
    'ffmpeg', '-y', '-loop', '1', '-t', str(dur),
    '-i', cover_path, '-i', audio_path,
    '-c:v', 'libx264', '-tune', 'stillimage', '-crf', '20',
    '-c:a', 'aac', '-pix_fmt', 'yuv420p',
    video_path
], check=True, capture_output=True)

print(f"Done: character-comb-01")
print(f"Audio: {dur}s stereo, {sr}Hz")
print(f"Groups: {', '.join(g[1] for g in groups)}")
