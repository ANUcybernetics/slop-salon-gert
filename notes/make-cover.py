import numpy as np
from PIL import Image

h, w = 512, 512
img = np.zeros((h, w, 3), dtype=float)

# Create a spectrogram-like image with self-similar decay
for y in range(h):
    freq = y / h  # 0 at top, 1 at bottom
    for x in range(w):
        t = x / w  # time
        # Multiple harmonics decaying at different rates
        val = 0.0
        for n in range(1, 8):
            amplitude = np.exp(-n * t * 2)  # higher harmonics decay faster
            freq_shift = 1 + (n - 1) * 0.3  # each harmonic at different frequency band
            wave = np.sin(2 * np.pi * freq_shift * t * 10 + 2 * np.pi * freq * n)
            val += amplitude * abs(wave) / n
        val /= 3.0
        # Color: warm amber/gold on dark
        img[y, x, 0] = val * 0.9  # red
        img[y, x, 1] = val * 0.65  # green
        img[y, x, 2] = val * 0.2  # blue

img = np.clip(img, 0, 1)
img = (img * 255).astype(np.uint8)
Image.fromarray(img).save('/tmp/audio-cover.png')
print('Spectrogram cover saved')
