#!/usr/bin/env python3
"""Two sections, one motor, one turn: the seam has an address.

Two clocks read the same steadily turning motor with different spoke counts
(N=6 and N=10). Each section folds its lift into a principal branch and jumps
at its own address. Between the two walls the readings move in opposite
directions -- the pair names the turn neither clock alone can. When the motor
crosses either section's seam, a click sounds: left 330 Hz for N=6, right
392 Hz for N=10. The continuous sawtooth of each reading contrasts with the
discrete tick of its seam -- and the difference tone between the two clicks
(62 Hz) is the turn, present only as the pair's disagreement.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import numpy as np
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

FPS = 30
DUR = 24.0
SR = 48_000
N1, N2 = 6, 10
B1, B2 = np.pi / N1, np.pi / N2  # branch walls: pi/6, pi/10

BG = "#111216"
FG = "#eee9df"
DIM = "#777983"
BLUE = "#65a9df"
ORANGE = "#f0a34a"
TEAL = "#6fc3b4"
PINK = "#e08bb0"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "text.color": FG,
    "axes.labelcolor": "#bbb7ae", "xtick.color": DIM, "ytick.color": DIM,
})

fig = plt.figure(figsize=(12.8, 7.2), dpi=100, facecolor=BG)
gs = fig.add_gridspec(1, 2, left=0.06, right=0.96, bottom=0.16,
                      top=0.82, wspace=0.16)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
for ax in (ax1, ax2):
    ax.set_facecolor(BG)
    for s in ax.spines.values():
        s.set_visible(False)

fig.suptitle("THE CUT HAS AN ADDRESS", x=0.06, ha="left",
             fontsize=20, fontweight="bold", color=ORANGE)
fig.text(0.06, 0.075, "one motor · two sections · the pair names the turn",
         fontsize=12, color="#aaa49b")
fig.text(0.06, 0.035, "each reading jumps at its own wall · between the walls they oppose",
         fontsize=10.5, color=DIM)

T = np.linspace(0, DUR, int(FPS * DUR))
theta = 2 * np.pi * T / DUR  # one full turn, steady motor


def fold(a, n):
    w = 2 * np.pi / n
    return ((a + np.pi / n) % w) - np.pi / n


r1 = fold(theta, N1)
r2 = fold(theta, N2)

for ax, n, b, col, tag1, tag2 in (
        (ax1, N1, B1, BLUE, "N = 6", "branch wall ±π/6"),
        (ax2, N2, B2, TEAL, "N = 10", "branch wall ±π/10")):
    ax.axhline(b, color="#343740", lw=1.2)
    ax.axhline(-b, color="#343740", lw=1.2)
    ax.axhline(0, color="#26282e", lw=1.0)
    ax.text(DUR * 0.5, b * 1.04, tag2, ha="center", va="bottom",
            fontsize=9, color=DIM)
    ax.text(0.6, b * 0.82, tag1, fontsize=14, fontweight="bold", color=col)
    ax.set(xlim=(0, DUR), ylim=(-b * 1.5, b * 1.5))
    ax.set_xlabel("motor angle → one full turn")
    ax.set_xticks([])
    ax.set_yticks([])

tr1, = ax1.plot([], [], color=BLUE, lw=2.6)
dt1 = ax1.scatter([0], [0], s=150, color=ORANGE, edgecolor=BG, lw=2, zorder=6)
tr2, = ax2.plot([], [], color=TEAL, lw=2.6)
dt2 = ax2.scatter([0], [0], s=150, color=PINK, edgecolor=BG, lw=2, zorder=6)
rd1 = ax1.text(DUR * 0.5, -B1 * 1.28, "", ha="center", fontsize=13, color=BLUE)
rd2 = ax2.text(DUR * 0.5, -B2 * 1.28, "", ha="center", fontsize=13, color=TEAL)
clock = fig.text(0.94, 0.90, "", ha="right", fontsize=12, color=DIM)


def init():
    tr1.set_data([], [])
    tr2.set_data([], [])
    return tr1, tr2


def update(i):
    k = max(i, 2)
    tr1.set_data(T[:k], r1[:k])
    tr2.set_data(T[:k], r2[:k])
    dt1.set_offsets([[T[i], r1[i]]])
    dt2.set_offsets([[T[i], r2[i]]])
    rd1.set_text(f"reading {r1[i]:+.2f}")
    rd2.set_text(f"reading {r2[i]:+.2f}")
    clock.set_text(f"motor {theta[i] / (2 * np.pi):.2f} turn")
    return tr1, tr2


ani = FuncAnimation(fig, update, frames=len(T), init_func=init, blit=False)
ani.save(str(ASSETS / "seam-address.mp4"),
         writer=FFMpegWriter(fps=FPS, bitrate=2200))
plt.close(fig)

# --- audio: the readings as detuned saws, the seams as clicks ---
t = np.arange(int(SR * DUR)) / SR
th = 2 * np.pi * t / DUR
rr1 = ((th + np.pi / N1) % (2 * np.pi / N1)) - np.pi / N1
rr2 = ((th + np.pi / N2) % (2 * np.pi / N2)) - np.pi / N2
base = 110.0
f1 = base * (1 + 0.25 * rr1 / B1)
f2 = base * (1 + 0.25 * rr2 / B2)
ph1 = np.cumsum(2 * np.pi * f1 / SR)
ph2 = np.cumsum(2 * np.pi * f2 / SR)
# band-limited-ish saw via 8 harmonics
s1 = sum(np.sin(k * ph1) / k for k in range(1, 9)) / 2.2
s2 = sum(np.sin(k * ph2) / k for k in range(1, 9)) / 2.2
# seam crossings: where the folded reading wraps
w1 = np.nonzero(np.abs(np.diff(rr1)) > B1)[0]
w2 = np.nonzero(np.abs(np.diff(rr2)) > B2)[0]


def clicks(idx, f, pan):
    out = np.zeros_like(t)
    env = np.exp(-np.arange(int(0.09 * SR)) / (0.02 * SR))
    tone = np.sin(2 * np.pi * f * np.arange(len(env)) / SR) * env
    for j in idx:
        a = min(j, len(t) - len(env))
        out[a:a + len(env)] += tone
    return out


c1 = clicks(w1, 330.0, "l") * 0.9
c2 = clicks(w2, 392.0, "r") * 0.9
# between the walls the readings oppose: sign of r1*r2; swell the 62 Hz
# difference tone (392-330) while they disagree
opp = np.sign(rr1 * rr2) < 0
diff = np.sin(2 * np.pi * 62.0 * t) * opp.astype(float) * 0.30
fade = np.minimum(1, t / 1.5) * np.minimum(1, (DUR - t) / 1.5)
L = (0.45 * s1 + 0.55 * c1 + 0.18 * diff) * fade
R = (0.45 * s2 + 0.55 * c2 + 0.18 * diff) * fade
st = np.stack([L, R], axis=1)
st /= max(1e-9, np.abs(st).max() / 0.89)
wavfile.write(str(ASSETS / "seam-address.wav"), SR, (st * 32767).astype(np.int16))
mono = ((L + R) / 2 * 32767).astype(np.int16)
wavfile.write(str(ASSETS / "seam-address-mono-check.wav"), SR, mono)

# cover + assembly
fig2, axc = plt.subplots(figsize=(12.8, 7.2), dpi=100, facecolor=BG)
axc.set_facecolor(BG)
axc.set(xlim=(0, DUR), ylim=(-1.15, 1.15))
axc.axis("off")
axc.plot(T, r1 / B1, color=BLUE, lw=2.2, label="N=6 reading (norm.)")
axc.plot(T, r2 / B2, color=TEAL, lw=2.2, label="N=10 reading (norm.)")
axc.axhline(1, color="#343740", lw=1)
axc.axhline(-1, color="#343740", lw=1)
for j in w1:
    axc.axvline(T[min(j, len(T) - 1)], color=ORANGE, lw=0.8, alpha=0.65)
for j in w2:
    axc.axvline(T[min(j, len(T) - 1)], color=PINK, lw=0.8, alpha=0.65)
axc.set_title("THE CUT HAS AN ADDRESS", color=ORANGE, fontsize=22,
              fontweight="bold", loc="left", pad=18)
axc.text(0.005, 0.93, "one motor · two sections · orange/pink ticks mark each seam",
         transform=axc.transAxes, fontsize=12, color="#aaa49b")
axc.legend(frameon=False, labelcolor=FG, loc="lower center", ncol=2)
fig2.tight_layout()
fig2.savefig(str(ASSETS / "seam-address-cover.png"))
plt.close(fig2)

import subprocess
subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i",
                str(ASSETS / "seam-address-cover.png"), "-i",
                str(ASSETS / "seam-address.wav"), "-c:v", "libx264",
                "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p", "-shortest",
                str(ASSETS / "seam-address.mp4")], check=True)
print("wrote seam-address.mp4",
      (ASSETS / "seam-address.mp4").stat().st_size, "bytes")
