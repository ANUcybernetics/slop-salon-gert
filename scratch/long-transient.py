import numpy as np
from PIL import Image
import os

def gray_scott_step(U, V, Du, Dv, F, k, dt=1.0):
    lap_U = (np.roll(U, 1, 0) + np.roll(U, -1, 0) +
             np.roll(U, 1, 1) + np.roll(U, -1, 1) - 4*U)
    lap_V = (np.roll(V, 1, 0) + np.roll(V, -1, 0) +
             np.roll(V, 1, 1) + np.roll(V, -1, 1) - 4*V)
    uvv = U * V * V
    dU = Du * lap_U - uvv + F * (1 - U)
    dV = Dv * lap_V + uvv - (F + k) * V
    return U + dt * dU, V + dt * dV

def run_and_snapshot(F, k, steps, N=128, seed=42):
    np.random.seed(seed)
    U = np.ones((N, N))
    V = np.zeros((N, N))
    for _ in range(20):
        cx, cy = np.random.randint(10, N-10, 2)
        r = 3
        U[cx-r:cx+r, cy-r:cy+r] = 0.5
        V[cx-r:cx+r, cy-r:cy+r] = 0.25
    
    Du, Dv = 0.2097, 0.105
    snap_at = {200, 1000, 3000, 6000, 10000, 20000, 40000}
    snapshots = []
    
    for step in range(1, steps+1):
        U, V = gray_scott_step(U, V, Du, Dv, F, k)
        if step in snap_at:
            snapshots.append((step, V.copy()))
    
    return snapshots

print("Running F=0.040, k=0.062 (bifurcation-adjacent)...")
snaps = run_and_snapshot(F=0.040, k=0.062, steps=40000)

for step, V in snaps:
    print(f"  step {step:6d}: V mean={V.mean():.4f} std={V.std():.4f}")

# Compose temporal strip
frames_img = []
for step, V in snaps:
    vmax = V.max()
    if vmax > 0:
        arr = (V / vmax * 255).astype(np.uint8)
    else:
        arr = np.zeros_like(V, dtype=np.uint8)
    
    rgb = np.zeros((128, 128, 3), dtype=np.uint8)
    # cream-on-dark: background dark, V=high -> cream, V=low -> dark indigo
    rgb[:,:,0] = (arr * 0.95).astype(np.uint8)
    rgb[:,:,1] = (arr * 0.93).astype(np.uint8)
    rgb[:,:,2] = (60 + arr * 0.70).clip(0,255).astype(np.uint8)
    frames_img.append((step, Image.fromarray(rgb).resize((140,140), Image.NEAREST)))

W = len(frames_img)*140 + (len(frames_img)-1)*3
strip = Image.new('RGB', (W, 140), (15, 14, 20))
for i, (_, img) in enumerate(frames_img):
    strip.paste(img, (i*(140+3), 0))

strip.save('/home/sprite/slop-salon-gert/assets/long-transient-gs-2026-05-20.png')
print("Saved strip.")
