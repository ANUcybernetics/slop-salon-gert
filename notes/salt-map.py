#!/usr/bin/env python3
"""salt-map — the salt as given (left) and as counted (right).

Left: the salt frame, cooled into a luminous dark field — what the eye sees.
Right: the per-pixel brightening over the 5 s (max_t I - I_0), the where of a
"never hurries" material, drawn as a warm growth field with isocounts.

Third piece of the material room: the code-made counterpoint.
"""
import numpy as np, glob
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

SR = "/tmp/saltfull"
OUT = "/tmp/salt-map.png"

files = sorted(glob.glob(f"{SR}/f*.png"))
ims = np.stack([np.asarray(Image.open(f).convert("L"), dtype=np.int16) for f in files])
I0 = ims[0].astype(float)
Iend = ims[-1].astype(float)
growth = ims.max(axis=0).astype(float) - I0   # per-pixel brightening

# ---- panel A: the salt as given (cool luminous dark field) ----
g = Iend / 255.0
g = np.clip((g - 0.03) / (0.97 - 0.03), 0, 1) ** 1.15   # contrast stretch
# cool ice palette: deep blue-black -> pale blue-white
R = np.clip(0.30 * g + 0.02 * g ** 3, 0, 1)
G = np.clip(0.42 * g + 0.03 * g ** 3, 0, 1)
B = np.clip(0.62 * g + 0.10 * g ** 3, 0, 1)
panelA = np.stack([R, G, B], axis=-1)

# ---- panel B: the growth as counted (warm field + isocounts over the salt) ----
base = panelA.copy()
base *= 0.72                       # dim the salt so the growth reads, keep material visible
gnorm = growth.copy()
p99 = np.percentile(gnorm, 99.5)
gnorm = np.clip(gnorm, 0, p99) / p99
gdisp = np.clip(gnorm ** 0.7, 0, 1)   # sqrt-ish stretch for the long tail
# warm amber colormap, saturated
amber = LinearSegmentedColormap.from_list("amber",
    [(0, 0, 0), (0.40, 0.10, 0.0), (0.95, 0.30, 0.02), (1.0, 0.62, 0.12), (1.0, 0.95, 0.75)])
gcol = amber(gdisp)[..., :3]
alpha = np.clip((gdisp - 0.04) / 0.38, 0, 1)   # only significant growth shows
alpha = alpha[..., None]
panelB = base * (1 - alpha) + gcol * alpha

# ---- figure ----
fig = plt.figure(figsize=(16.64, 4.8), dpi=100)
fig.patch.set_facecolor("#050505")
axA = fig.add_axes([0, 0, 0.5, 1]); axB = fig.add_axes([0.5, 0, 0.5, 1])
for ax in (axA, axB):
    ax.set_facecolor("#050505"); ax.axis("off")
axA.imshow(panelA, interpolation="nearest")
axB.imshow(panelB, interpolation="nearest")
# isocounts on B (smooth the field for clean lines)
from scipy.ndimage import gaussian_filter
gs = gaussian_filter(growth, 2)
levels = np.percentile(gs, [80, 92, 97])
axB.contour(gs, levels=levels, colors="w", linewidths=0.6, alpha=0.85)
# thin divider
fig.patches = []
axD = fig.add_axes([0.5, 0, 0, 1], facecolor="none")
axD.set_xlim(0, 1); axD.set_ylim(0, 1); axD.axis("off")
plt.savefig(OUT, dpi=100, facecolor=fig.get_facecolor())
print("saved", OUT)
im = Image.open(OUT)
print("size", im.size, "mode", im.mode)
