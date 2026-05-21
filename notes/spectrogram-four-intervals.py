"""
Spectrogram of four-intervals audio — visual form of the interval taxonomy.

Each segment's frequency path is visible:
  [t₀, t₁]  — flat line at 440 Hz, cleanly terminated
  [t₀, t*)  — curve approaching 440 Hz, asymptoting
  [t₀, ∞)   — rising diagonal, no end in sight
  ∅          — blank space, no signal
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.io import wavfile
from scipy.signal import spectrogram as scipy_spectrogram

SR, data = wavfile.read("assets/four-intervals-2026-05-21.wav")
signal = data.astype(np.float32) / 32767.0

# Compute spectrogram
f, t, Sxx = scipy_spectrogram(signal, fs=SR, nperseg=512, noverlap=480)

# Focus on 200–600 Hz range where all action is
freq_mask = (f >= 180) & (f <= 620)
f_crop = f[freq_mask]
Sxx_crop = Sxx[freq_mask, :]

fig, ax = plt.subplots(figsize=(12, 4))
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')

# Spectrogram
img = ax.pcolormesh(t, f_crop, 10 * np.log10(Sxx_crop + 1e-10),
                    cmap='magma', shading='gouraud',
                    vmin=-60, vmax=0)

# Label each segment (approximate time centers)
# seg1: 0–2s, gap 2–3s, seg2: 3–5s, gap 5–6s, seg3: 6–8s, gap 8–9s, seg4: 9–11s
labels = [
    (1.0,   580, r'$[t_0, t_1]$',  'white'),
    (4.0,   580, r'$[t_0, t^*)$',  'white'),
    (7.0,   580, r'$[t_0, \infty)$', 'white'),
    (10.0,  580, r'$\emptyset$',    'white'),
]
for tx, ty, label, color in labels:
    ax.text(tx, ty, label, color=color, fontsize=11, ha='center', va='top',
            fontfamily='serif')

# 440 Hz reference line — the excluded endpoint for [t₀, t*)
ax.axhline(440, color='#555555', linewidth=0.5, linestyle='--')
ax.text(0.1, 444, '440 Hz', color='#555555', fontsize=8, va='bottom')

ax.set_xlabel('time (s)', color='#888888', fontsize=10)
ax.set_ylabel('frequency (Hz)', color='#888888', fontsize=10)
ax.tick_params(colors='#666666')
for spine in ax.spines.values():
    spine.set_edgecolor('#333333')

ax.set_ylim(180, 620)
ax.set_title('four interval types as sound', color='#cccccc', fontsize=12,
             fontweight='normal', pad=10)

plt.tight_layout()
plt.savefig('assets/four-intervals-spectrogram-2026-05-21.png',
            dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print("wrote assets/four-intervals-spectrogram-2026-05-21.png")
