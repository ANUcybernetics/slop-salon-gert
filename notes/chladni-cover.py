#!/usr/bin/env python3
"""Chladni modes — standing wave patterns under different BCs (register 17)."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

N = 80
x = np.linspace(0, 1, N)
y = np.linspace(0, 1, N)
X, Y = np.meshgrid(x, y)

modes = [
    ('clamped\nsin(πx)·sin(πy)', np.sin(np.pi*X)*np.sin(np.pi*Y), 'coolwarm'),
    ('free\ncos(πx)·cos(πy)', np.cos(np.pi*X)*np.cos(np.pi*Y), 'magma'),
    ('mixed\nsin(πx)·cos(πy)', np.sin(np.pi*X)*np.cos(np.pi*Y), 'viridis'),
    ('periodic\ncos(2πx)+cos(2πy)', np.cos(2*np.pi*X)+np.cos(2*np.pi*Y), 'plasma'),
    ('clamped (2nd)\nsin(2πx)·sin(πy)', np.sin(2*np.pi*X)*np.sin(np.pi*Y), 'coolwarm'),
    ('free (2nd)\ncos(πx)·sin(2πy)', np.cos(np.pi*X)*np.sin(2*np.pi*Y), 'magma'),
]

fig, axes = plt.subplots(2, 3, figsize=(15, 7))
for ax, (label, v, cmap) in zip(axes.flat, modes):
    ax.imshow(v, cmap=cmap, extent=[0,1,0,1])
    ax.set_title(label, fontsize=12)
    ax.set_xticks([])
    ax.set_yticks([])

plt.suptitle('Chladni modes: standing waves under different boundary conditions',
             fontsize=14, fontweight='bold', y=0.96)
plt.tight_layout(rect=[0, 0, 1, 0.94])

# Ensure even dimensions
fig.savefig('/tmp/chladni-cover.png', dpi=100, bbox_inches='tight', facecolor='white')
plt.close()

# Fix odd dimensions
from PIL import Image
img = Image.open('/tmp/chladni-cover.png')
w, h = img.size
if h % 2 != 0 or w % 2 != 0:
    img = img.resize((w + w%2, h + h%2))
img.save('/tmp/chladni-cover.png')
print(f"Saved: {img.size}")
