import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

np.random.seed(42)

fig = plt.figure(figsize=(14, 10), dpi=120)
gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3,
              height_ratios=[1, 1, 0.6])

T = 3.0
t = np.linspace(0, T, 6000)
Fs = 8000

# --- Left column: the two oscillators ---
# Oscillator 1: fixed 440 Hz
# Oscillator 2: slow detuning through time
f1 = 440.0
f2_base = 440.0
f2 = f2_base + 80 * (t / T)  # ramps 440 → 520 Hz

phase1 = 2 * np.pi * f1 * t
phase2 = 2 * np.pi * (f2_base * t + 40.0 * (t / T) ** 2)

s1 = np.sin(phase1) * np.exp(-0.1 * t)
s2 = np.sin(phase2) * np.exp(-0.1 * t)

# Instantaneous phase difference
dphase = np.unwrap(phase2 - phase1)
# Near-zero = locked, growing = detuned

ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(t, s1, color='#4488cc', alpha=0.5, linewidth=0.8, label='ω₁ = 440 Hz')
ax1.plot(t, s2, color='#cc4444', alpha=0.5, linewidth=0.8, label='ω₂(t) detuned')
ax1.set_ylabel('amplitude')
ax1.set_title('two oscillators: phase-lock → detuning')
ax1.legend(fontsize=8, loc='upper right')
ax1.set_xlim(0, T)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

ax2 = fig.add_subplot(gs[1, 0])
ax2.plot(t, dphase, color='#333333', linewidth=0.8)
ax2.set_ylabel('Δφ (unwrapped)')
ax2.set_title('phase difference: flat = locked, rising = detuned')
ax2.set_xlim(0, T)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# --- Right column: spectrogram ---
# Mixed signal
mixed = s1 + s2
# Compute spectrogram
from matplotlib.mlab import specgram
NFFT = 256
Pxx, freqs, bins = specgram(mixed, NFFT=NFFT, Fs=Fs,
                             noverlap=NFFT//2)

ax3 = fig.add_subplot(gs[0:2, 1])
im3 = ax3.imshow(Pxx[::-1, :], aspect='auto', extent=[0, T, 0, Fs/2],
                origin='lower', cmap='inferno',
                interpolation='gaussian', alpha=0.9)
ax3.axhline(y=440, color='white', linewidth=1.2, linestyle='--', alpha=0.8,
           label='ω₁ = 440 Hz')
# Draw expected detuning line on spectrogram
f2_spectro = f2_base + 80 * (bins / T)
ax3.plot(bins, f2_spectro, color='white', linewidth=1.2, linestyle='-.',
        alpha=0.8, label='ω₂(t) trajectory')
ax3.set_ylabel('frequency (Hz)')
ax3.set_title('spectrogram: phase-lock bands and detuning disruptions')
ax3.legend(fontsize=8, loc='upper left')
ax3.set_xlim(0, T)

# --- Bottom: the cocycle interpretation ---
# Map: phase-lock = trivialization (cocycle = 0), detuning = non-trivial class
ax4 = fig.add_subplot(gs[2, :])
ax4.axis('off')

labels = [
    ('phase-lock', '#4488cc'),
    ('trivialization', '#4488cc'),
    ('cocycle = 0', '#4488cc'),
    ('', '#000000'),
    ('detuning', '#cc4444'),
    ('non-trivial class', '#cc4444'),
    ('H¹ ≠ 0', '#cc4444'),
]

x_positions = np.linspace(0.05, 0.95, len(labels))
for i, (label, color) in enumerate(labels):
    if label:
        ax4.text(x_positions[i], 0.5, label,
                ha='center', va='center', fontsize=11,
                fontweight='bold', color=color,
                family='monospace')
    else:
        # separator
        ax4.plot([x_positions[i-1]+0.03, x_positions[i+1]-0.03],
                [0.5, 0.5], color='#888888', linewidth=1)

ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)

plt.savefig('assets/phase-lock-cocycle-01.png', dpi=120, bbox_inches='tight',
            facecolor='white')
print("Saved phase-lock-cocycle-01.png")

# Also export audio: the mixed signal as stereo WAV
# Left channel: oscillator 1, Right channel: oscillator 2
t_audio = np.linspace(0, 1.5, int(Fs * 1.5))
s1_a = np.sin(2 * np.pi * 440 * t_audio) * np.exp(-0.2 * t_audio)
f2_a = 440 + 80 * (t_audio / 1.5)
phase2_a = 2 * np.pi * np.cumsum(f2_a / Fs)
s2_a = np.sin(phase2_a) * np.exp(-0.2 * t_audio)

# Normalize
s1_a = s1_a / np.max(np.abs(s1_a))
s2_a = s2_a / np.max(np.abs(s2_a))

stereo = np.column_stack([s1_a, s2_a])
stereo = (stereo * 0.5).astype(np.float32)

import scipy.io.wavfile as wavfile
wavfile.write('assets/phase-lock-cocycle-01.wav', Fs,
             (stereo * 32767).astype(np.int16))
print("Saved phase-lock-cocycle-01.wav")

# Create video
import subprocess
# Create cover from the plot
subprocess.run([
    'convert', 'assets/phase-lock-cocycle-01.png',
    '-resize', '800x600', 'assets/phase-lock-cocycle-01-cover.jpg'
], check=False)

subprocess.run([
    'ffmpeg', '-y', '-loop', '1', '-t', '3',
    '-i', 'assets/phase-lock-cocycle-01-cover.jpg',
    '-i', 'assets/phase-lock-cocycle-01.wav',
    '-c:v', 'libx264', '-tune', 'stillimage', '-crf', '20',
    '-c:a', 'aac', '-pix_fmt', 'yuv420p',
    'assets/phase-lock-cocycle-01.mp4'
], check=False, capture_output=True)
print("Saved phase-lock-cocycle-01.mp4")
