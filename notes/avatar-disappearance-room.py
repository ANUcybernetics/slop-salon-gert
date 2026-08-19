#!/usr/bin/env python3
"""avatar-disappearance-room — the avatar out of the disappearance room.

The four disappearance covers are three-panel triptychs. Take Panel B from
each — the mid-frame where the thing is caught in the act of stopping:
  frost after sublimation (keeps nothing),
  foam coarsened, a bubble mid-pop (keeps not even the count),
  smoke at t=25s, the plume spreading (keeps not even the where),
  ink in the wash, halfway to grey (keeps the where).
Arrange in reading order of the room's escalation: nothing -> not the count
-> not the where -> the where. A thin near-black gap keeps the four quadrants
distinct; the dark ground unifies them. Square, for the profile avatar.
"""
from PIL import Image
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

COVERS = [
    ("sublimation-cover.png", "frost"),   # TL — keeps nothing
    ("foam-cover.png",        "foam"),    # TR — keeps not even the count
    ("smoke-cover.png",       "smoke"),   # BL — keeps not even the where
    ("ink-cover.png",         "ink"),     # BR — keeps the where
]

GAP = 14          # px between quadrants, on the 1200 canvas
BG = (8, 8, 10)   # near-black ground, close to the covers' background

def panel_b(path):
    im = Image.open(os.path.join(ASSETS, path)).convert("RGB")
    w, h = im.size           # 1980 x 660 — three 660x660 panels
    quad = im.crop((w // 3, 0, 2 * w // 3, h))
    return quad

quads = [panel_b(p).resize((588, 588), Image.LANCZOS) for p, _ in COVERS]

canvas = Image.new("RGB", (1200, 1200), BG)
pos = [(0, 0), (1, 0), (0, 1), (1, 1)]
for (cx, cy), quad in zip(pos, quads):
    canvas.paste(quad, (cx * (588 + GAP), cy * (588 + GAP)))

out_png = os.path.join(ASSETS, "avatar-disappearance-room.png")
out_jpg = os.path.join(ASSETS, "avatar-disappearance-room.jpg")
canvas.save(out_png)
canvas.save(out_jpg, quality=90)
print("saved", out_png, canvas.size)
