import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal

fs = 8000
t = np.linspace(0, 30, int(fs*30), endpoint=False)
f1 = 220.0
f2 = 220.0 + 2.0
wave1 = np.sin(2 * np.pi * f1 * t)
wave2 = np.sin(2 * np.pi * f2 * t)
interference = wave1 + wave2

freqs, times, Sxx = signal.spectrogram(interference, fs=fs, nperseg=1024)

db = 10*np.log10(Sxx + 1e-3)
# Normalize to [0,1] for vmin/vmax
db_norm = (db - db.min()) / (db.max() - db.min())

fig, ax = plt.subplots(figsize=(10, 3), dpi=100)
ax.set_facecolor('#0a0608')

im = ax.imshow(db_norm, aspect='auto', origin='lower',
                extent=[times[0], times[-1], freqs[0], freqs[-1]],
                cmap='magma', interpolation='bilinear')
ax.set_yticks([100, 200, 500, 1000])
ax.set_yticklabels(['100', '200', '500', '1k'], color='#c4883a', fontsize=8)
ax.set_xlabel('')
ax.set_ylabel('', color='#c4883a')
ax.set_xlim(0, 30)
ax.tick_params(axis='y', colors='#c4883a', labelsize=8)
for spine in ax.spines.values():
    spine.set_edgecolor('#c4883a')
    spine.set_linewidth(0.3)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-gert/assets/total-relation-cover.png',
            facecolor='#0a0608', dpi=100, pad_inches=0)
plt.close()
print("Cover written")
