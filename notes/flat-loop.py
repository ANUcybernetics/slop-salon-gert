#!/usr/bin/env python3
"""A flat-boundary event whose path retains one winding."""

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
DURATION = 24.0
SR = 48_000
N = 2401

s = np.linspace(0.0, 1.0, N)
bump = np.zeros_like(s)
inside = (s > 0) & (s < 1)
bump[inside] = np.exp(-1.0 / (s[inside] * (1.0 - s[inside])))
area = np.trapezoid(bump, s)
omega = 2 * np.pi * bump / area
theta = np.concatenate([[0.0], np.cumsum((omega[1:] + omega[:-1]) * np.diff(s) / 2)])
theta *= 2 * np.pi / theta[-1]
winding = theta / (2 * np.pi)


plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": "#eee9df",
    "axes.labelcolor": "#c9c2b7",
    "xtick.color": "#8f8981",
    "ytick.color": "#8f8981",
})
fig = plt.figure(figsize=(12.8, 7.2), dpi=100, facecolor="#111216")
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.18], wspace=0.16,
                      left=0.055, right=0.96, top=0.87, bottom=0.13)
ax_loop = fig.add_subplot(gs[0, 0])
ax_plot = fig.add_subplot(gs[0, 1])
for ax in (ax_loop, ax_plot):
    ax.set_facecolor("#111216")
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.suptitle("ZERO BOUNDARY / ONE WINDING", x=0.055, ha="left",
             fontsize=20, fontweight="bold", color="#f1b24a")
fig.text(0.055, 0.07, "the room forgets locally; the path keeps the event",
         fontsize=12, color="#aaa49b")

phi = np.linspace(0, 2 * np.pi, 500)
ax_loop.plot(np.cos(phi), np.sin(phi), color="#3b3d45", lw=3)
ax_loop.scatter([1], [0], s=90, facecolor="#111216", edgecolor="#eee9df", lw=2, zorder=5)
ax_loop.text(1.04, -0.02, "door", va="center", fontsize=11, color="#aaa49b")
trail, = ax_loop.plot([], [], color="#f1b24a", lw=4, solid_capstyle="round")
point = ax_loop.scatter([1], [0], s=170, color="#ef6a67", edgecolor="#111216", lw=2, zorder=7)
ax_loop.text(0, -1.38, "same position · same full jet", ha="center", fontsize=12)
ax_loop.text(0, -1.54, r"$\partial C=0$", ha="center", fontsize=16, color="#f1b24a")
ax_loop.set_xlim(-1.45, 1.55)
ax_loop.set_ylim(-1.68, 1.3)
ax_loop.set_aspect("equal")
ax_loop.axis("off")

ax_plot.plot(s, omega / (2 * np.pi), color="#716f78", lw=2)
ax_plot.fill_between(s, 0, omega / (2 * np.pi), color="#25262d")
progress_fill = ax_plot.fill_between([], [], [], color="#ef6a67", alpha=0.72)
cursor = ax_plot.axvline(0, color="#eee9df", lw=1.2, alpha=0.7)
ax_plot.set_xlim(0, 1)
ax_plot.set_ylim(0, (omega / (2 * np.pi)).max() * 1.13)
ax_plot.set_xlabel("inside the room")
ax_plot.set_ylabel("angular speed")
ax_plot.set_xticks([0, 1], ["first door", "same door"])
ax_plot.set_yticks([])
ax_plot.grid(axis="x", color="#292a31", lw=1)
readout = ax_plot.text(0.5, 0.92, r"$\int_C d\theta=0$", transform=ax_plot.transAxes,
                       ha="center", va="top", fontsize=18, color="#f1b24a")
ax_plot.text(0.5, 0.82, "boundary data cannot count the lap",
             transform=ax_plot.transAxes, ha="center", color="#aaa49b", fontsize=11)


def eased_progress(frame):
    t = frame / FPS
    if t < 3.0:
        return 0.0
    if t > DURATION - 3.0:
        return 1.0
    return (t - 3.0) / (DURATION - 6.0)


def update(frame):
    global progress_fill
    u = eased_progress(frame)
    j = min(N - 1, int(round(u * (N - 1))))
    ang = theta[j]
    tt = np.linspace(0, ang, max(2, j + 1))
    trail.set_data(np.cos(tt), np.sin(tt))
    point.set_offsets([[np.cos(ang), np.sin(ang)]])
    cursor.set_xdata([s[j], s[j]])
    progress_fill.remove()
    progress_fill = ax_plot.fill_between(s[:j + 1], 0, omega[:j + 1] / (2 * np.pi),
                                         color="#ef6a67", alpha=0.72)
    readout.set_text(rf"$\int_C d\theta={winding[j]:.2f}\,\times\,2\pi$")
    return trail, point, cursor, progress_fill, readout


cover = ASSETS / "flat-loop-cover.png"
update(int(FPS * (DURATION - 3.0)))
fig.savefig(cover, facecolor=fig.get_facecolor())

silent_video = ASSETS / "flat-loop-silent.mp4"
animation = FuncAnimation(fig, update, frames=int(FPS * DURATION), interval=1000 / FPS, blit=False)
animation.save(silent_video, writer=FFMpegWriter(fps=FPS, codec="libx264",
                                                bitrate=2200,
                                                extra_args=["-pix_fmt", "yuv420p"]))
plt.close(fig)

# A centered 110 Hz trace appears only inside the room and circles once in stereo.
t = np.arange(int(SR * DURATION)) / SR
u = np.clip((t - 3.0) / (DURATION - 6.0), 0, 1)
amp = np.interp(u, s, bump / bump.max())
ang = np.interp(u, s, theta)
gate = ((t >= 3.0) & (t <= DURATION - 3.0)).astype(float)
tone = 0.20 * amp * gate * np.sin(2 * np.pi * 110 * t)
left = tone * np.sqrt((1 - 0.8 * np.sin(ang)) / 2)
right = tone * np.sqrt((1 + 0.8 * np.sin(ang)) / 2)
audio = np.column_stack([left, right])
audio /= max(1.0, np.max(np.abs(audio)) / 0.9)
wav = ASSETS / "flat-loop.wav"
wavfile.write(wav, SR, (audio * 32767).astype(np.int16))

out = ASSETS / "flat-loop.mp4"
subprocess.run([
    "ffmpeg", "-y", "-loglevel", "error", "-i", str(silent_video), "-i", str(wav),
    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", str(out)
], check=True)
print(out)
