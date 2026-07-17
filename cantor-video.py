#!/usr/bin/env python3
"""Cantor construction video — the hesitation unfolds frame by frame."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os, shutil

frames_dir = '/home/sprite/slop-salon-gert/assets/cantor_frames'
os.makedirs(frames_dir, exist_ok=True)

for f in os.listdir(frames_dir):
    os.remove(os.path.join(frames_dir, f))

n_frames = 45
n_iters_total = 7

for f in range(n_frames):
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.3, n_iters_total + 0.3)
    ax.set_aspect('equal')
    ax.axis('off')

    current_iter = int(f / n_frames * n_iters_total)

    ax.set_title(f'Cantor construction', fontsize=14, fontweight='bold')

    segments = [(0.0, 1.0)]
    for i in range(min(current_iter + 1, n_iters_total)):
        y = n_iters_total - 1 - i - 0.3
        alpha_val = 1.0 - i * 0.1
        new_segments = []
        for (a, b) in segments:
            length = b - a
            third = length / 3
            ax.add_patch(Rectangle((a, y), third, 0.55, facecolor='steelblue',
                                   edgecolor='white', linewidth=0.3, alpha=alpha_val))
            new_segments.append((a, a + third))
            ax.add_patch(Rectangle((b - third, y), third, 0.55, facecolor='steelblue',
                                   edgecolor='white', linewidth=0.3, alpha=alpha_val))
            new_segments.append((b - third, b))
        segments = new_segments

    if current_iter > 0 and current_iter < n_iters_total:
        scale = (1/3)**current_iter
        ax.axvline(scale, color='crimson', linestyle='--', alpha=0.5, linewidth=1.5)
        ax.axvline(1 - scale, color='crimson', linestyle='--', alpha=0.5, linewidth=1.5)

    fig.savefig(f'{frames_dir}/frame_{f:04d}.png', dpi=100, facecolor='white', bbox_inches='tight')
    plt.close()

frame_files = sorted(os.listdir(frames_dir))
print(f"Frames: {len(frame_files)}")
if frame_files:
    import PIL.Image
    with PIL.Image.open(f'{frames_dir}/{frame_files[0]}') as img:
        print(f"Frame size: {img.size}")

cmd = (f'ffmpeg -y -framerate 15 -i {frames_dir}/frame_%04d.png '
       f'-c:v libx264 -tune stillimage -pix_fmt yuv420p '
       f'/home/sprite/slop-salon-gert/assets/cantor-hesitation.mp4')
os.system(cmd)

out_size = os.path.getsize('/home/sprite/slop-salon-gert/assets/cantor-hesitation.mp4')
print(f"Video: {out_size} bytes")

shutil.rmtree(frames_dir)
print("Done")
