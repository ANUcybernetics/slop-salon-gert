#!/usr/bin/env python3
"""One completed loop, two witnesses, two incompatible decisions."""

from pathlib import Path
import subprocess

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import numpy as np
from scipy.io import wavfile


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

FPS = 30
DURATION = 18.0
SR = 48_000
BG = "#111216"
FG = "#eee9df"
DIM = "#777983"
BLUE = "#65a9df"
ORANGE = "#f0a34a"
OPEN = "#79c98d"
CLOSED = "#ef6a67"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": FG,
    "axes.labelcolor": "#bbb7ae",
    "xtick.color": DIM,
    "ytick.color": DIM,
})

fig = plt.figure(figsize=(12.8, 7.2), dpi=100, facecolor=BG)
gs = fig.add_gridspec(1, 2, left=0.055, right=0.96, bottom=0.14,
                      top=0.84, wspace=0.12)
ax_q = fig.add_subplot(gs[0, 0])
ax_l = fig.add_subplot(gs[0, 1])
for ax in (ax_q, ax_l):
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.suptitle("THE WITNESS OPERATES THE GATE", x=0.055, ha="left",
             fontsize=20, fontweight="bold", color=ORANGE)
fig.text(0.055, 0.065, "same completed path · opposite return decisions",
         fontsize=12, color="#aaa49b")

# Quotient observer: height is forgotten, so one turn returns to zero.
phi = np.linspace(0, 2 * np.pi, 600)
ax_q.plot(np.cos(phi), np.sin(phi), color="#343740", lw=3)
q_trail, = ax_q.plot([], [], color=BLUE, lw=5, solid_capstyle="round")
q_dot = ax_q.scatter([1], [0], s=170, color=ORANGE, edgecolor=BG, lw=2, zorder=6)
ax_q.scatter([1], [0], s=260, facecolor="none", edgecolor=FG, lw=1.3, zorder=5)
ax_q.text(0, 1.28, "SHADOW / θ mod 2π", ha="center", fontsize=15, fontweight="bold")
ax_q.text(0, 1.11, "kernel identifies every whole turn with zero",
          ha="center", fontsize=10.5, color="#aaa49b")
q_read = ax_q.text(0, -1.35, "θ = 0.00 turns", ha="center", fontsize=14)
q_gate = ax_q.text(0, -1.62, "RETURN PENDING", ha="center", fontsize=16,
                    fontweight="bold", color=DIM)
ax_q.set(xlim=(-1.45, 1.45), ylim=(-1.78, 1.48), aspect="equal")
ax_q.axis("off")

# Lift observer: one turn ends on another sheet.
z = np.linspace(0, 1, 600)
xh = 0.34 * np.sin(2 * np.pi * z)
ax_l.plot(xh, z, color="#343740", lw=3)
for level in (0, 1):
    ax_l.plot([-0.72, 0.72], [level, level], color="#343740", lw=1.4)
    ax_l.text(-0.80, level, f"level {level}", ha="right", va="center",
              fontsize=10, color="#aaa49b")
l_trail, = ax_l.plot([], [], color=ORANGE, lw=5, solid_capstyle="round")
l_dot = ax_l.scatter([0], [0], s=170, color=BLUE, edgecolor=BG, lw=2, zorder=6)
ax_l.scatter([0], [0], s=260, facecolor="none", edgecolor=FG, lw=1.3, zorder=5)
ax_l.text(0, 1.28, "LIFT / θ ÷ 2π", ha="center", fontsize=15, fontweight="bold")
ax_l.text(0, 1.11, "kernel keeps the accumulated level",
          ha="center", fontsize=10.5, color="#aaa49b")
l_read = ax_l.text(0, -0.22, "height = 0.00", ha="center", fontsize=14)
l_gate = ax_l.text(0, -0.40, "RETURN PENDING", ha="center", fontsize=16,
                    fontweight="bold", color=DIM)
ax_l.set(xlim=(-1.25, 1.25), ylim=(-0.55, 1.48))
ax_l.axis("off")


def progress(frame):
    t = frame / FPS
    if t <= 2.5:
        return 0.0
    if t >= 13.5:
        return 1.0
    x = (t - 2.5) / 11.0
    return x * x * (3 - 2 * x)


def update(frame):
    u = progress(frame)
    j = max(1, min(len(phi) - 1, int(round(u * (len(phi) - 1)))))
    q_trail.set_data(np.cos(phi[:j + 1]), np.sin(phi[:j + 1]))
    q_dot.set_offsets([[np.cos(phi[j]), np.sin(phi[j])]])
    l_trail.set_data(xh[:j + 1], z[:j + 1])
    l_dot.set_offsets([[xh[j], z[j]]])
    wrapped = u % 1.0 if u < 0.9995 else 0.0
    q_read.set_text(f"θ = {wrapped:.2f} turns")
    l_read.set_text(f"height = {u:.2f}")
    if frame / FPS >= 14.0:
        q_gate.set_text("RETURN ACCEPTED · GATE OPEN")
        q_gate.set_color(OPEN)
        l_gate.set_text("RETURN REFUSED · GATE SHUT")
        l_gate.set_color(CLOSED)
    else:
        q_gate.set_text("RETURN PENDING")
        q_gate.set_color(DIM)
        l_gate.set_text("RETURN PENDING")
        l_gate.set_color(DIM)
    return q_trail, q_dot, l_trail, l_dot, q_read, l_read, q_gate, l_gate


cover = ASSETS / "witness-gate-cover.png"
update(int(FPS * 15.0))
fig.savefig(cover, facecolor=BG)

silent = ASSETS / "witness-gate-silent.mp4"
anim = FuncAnimation(fig, update, frames=int(FPS * DURATION),
                     interval=1000 / FPS, blit=False)
anim.save(silent, writer=FFMpegWriter(fps=FPS, codec="libx264", bitrate=2200,
                                     extra_args=["-pix_fmt", "yuv420p"]))
plt.close(fig)

# During the shared path, a centered 110 Hz tone rises with the lift. At the
# decision, the quotient releases a bright left-hand bell; the lift holds a
# low, pulsing right-hand tone behind the shut gate.
t = np.arange(int(SR * DURATION)) / SR
u = np.array([progress(int(tt * FPS)) for tt in t])
move = ((t >= 2.5) & (t <= 13.5)).astype(float)
edge = np.minimum(np.clip((t - 2.5) / 0.7, 0, 1), np.clip((13.5 - t) / 0.7, 0, 1))
shared = 0.16 * move * edge * np.sin(2 * np.pi * (110 + 18 * u) * t)
audio_l = shared.copy()
audio_r = shared.copy()
after = np.clip(t - 14.0, 0, None)
bell_env = np.exp(-1.6 * after) * (t >= 14.0)
bell = 0.24 * bell_env * (np.sin(2 * np.pi * 220 * after) +
                          0.45 * np.sin(2 * np.pi * 440 * after))
hold_env = (t >= 14.0) * (0.62 + 0.38 * np.sin(2 * np.pi * 1.25 * after) ** 2)
held = 0.18 * hold_env * np.sin(2 * np.pi * 55 * after)
audio_l += bell
audio_r += held
audio = np.column_stack([audio_l, audio_r])
audio /= max(1.0, np.max(np.abs(audio)) / 0.92)
wav = ASSETS / "witness-gate.wav"
wavfile.write(wav, SR, (audio * 32767).astype(np.int16))

out = ASSETS / "witness-gate.mp4"
subprocess.run([
    "ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(wav),
    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", str(out)
], check=True)
print(out)
