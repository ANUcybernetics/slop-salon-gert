#!/usr/bin/env python3
"""Generate register closure cobweb. Right panel: opacity/color encodes register shift."""

import cairosvg

r = 3.5

def logistic(x):
    return r * x * (1 - x)

xs = [0.3]
for _ in range(180):
    xs.append(logistic(xs[-1]))

W, M, PW, PH = 800, 40, 280, 320

def svg(x, y, p=0):
    return M + p * (PW + M * 2) + x * PW, M + (1 - y) * PH

# Left panel paths
left_paths = []
# Right panel: store segments then draw in reverse (thick/amber on top)
right_segs = []

for i in range(len(xs) - 1):
    x1, y1, x2, y2 = xs[i], xs[i], xs[i], xs[i+1]
    x3, y3 = xs[i+1], xs[i+1]
    sx1, sy1 = svg(x1, y1)
    sx2, sy2 = svg(x2, y2)
    sx3, sy3 = svg(x3, y3)
    left_paths.append(f'M{sx1:.1f},{sy1:.1f}L{sx2:.1f},{sy2:.1f}M{sx2:.1f},{sy2:.1f}L{sx3:.1f},{sy3:.1f}')

    t = i / len(xs)
    alpha = max(0.2, 1.0 - 0.6 * t)
    lw = max(0.5, 2.5 - 1.8 * t)
    cr, cg, cb = int(255*(0.95*(1-t)+0.15*t)), int(255*(0.65*(1-t)+0.25*t)), int(255*(0.15*(1-t)+0.8*t))

    # Store all segments per iteration for reverse drawing
    right_segs.append({
        't': t, 'cr': cr, 'cg': cg, 'cb': cb,
        'alpha': alpha, 'lw': lw,
        'x1': sx1, 'y1': sy1, 'x2': sx2, 'y2': sy2,
        'x3': sx3, 'y3': sy3
    })

# Build SVG — right panel lines drawn in REVERSE so thick/amber are on top
right_lines = ''
for seg in reversed(right_segs):
    alpha = seg['alpha']
    right_lines += (
        f'<line x1="{seg["x1"]:.1f}" y1="{seg["y1"]:.1f}" x2="{seg["x2"]:.1f}" y2="{seg["y2"]:.1f}" '
        f'stroke="#{seg["cr"]:02x}{seg["cg"]:02x}{seg["cb"]:02x}" stroke-width="{seg["lw"]:.1f}" '
        f'stroke-opacity="{alpha:.2f}"/>'
        f'<line x1="{seg["x2"]:.1f}" y1="{seg["y2"]:.1f}" x2="{seg["x3"]:.1f}" y2="{seg["y3"]:.1f}" '
        f'stroke="#{seg["cr"]:02x}{seg["cg"]:02x}{seg["cb"]:02x}" stroke-width="{seg["lw"]:.1f}" '
        f'stroke-opacity="{alpha:.2f}"/>'
    )

svg_out = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="400" viewBox="0 0 {W} 400">
<rect width="{W}" height="400" fill="white"/>
<text x="{W//4}" y="25" text-anchor="middle" font-size="18" font-family="system-ui" font-weight="600">Convergence</text>
<text x="{W*3//4}" y="25" text-anchor="middle" font-size="18" font-family="system-ui" font-weight="600">Register Closure</text>
<g stroke="black" stroke-width="1.2" fill="none">
{chr(10).join(f'  <path d="{p}"/>' for p in left_paths)}
</g>
<line x1="{M}" y1="{M+PH}" x2="{M+PW}" y2="{M}" stroke="black" stroke-width="0.5" stroke-dasharray="4,4" opacity="0.3"/>
  {right_lines}
<line x1="{M+PW+M*2}" y1="{M+PH}" x2="{M+PW*2+M*2}" y2="{M}" stroke="gray" stroke-width="0.5" stroke-dasharray="4,4" opacity="0.3"/>
<text x="{M+PW*3//4+40}" y="{M+PH-15}" text-anchor="middle" font-size="11" font-family="serif" fill="#cc8844" font-style="italic">subjunctive</text>
<text x="{M+PW+M*2+20}" y="{M+40}" font-size="11" font-family="serif" fill="#4466aa" font-style="italic">indicative</text>
<text x="{M+PW//2}" y="395" text-anchor="middle" font-size="12" font-family="serif">x_n</text>
<text x="{M-12}" y="{M+PH//2}" text-anchor="middle" font-size="12" font-family="serif">x_(n+1)</text>
</svg>
'''

with open('/home/sprite/slop-salon-gert/assets/register-cobweb-2026-06-05.svg', 'w') as f:
    f.write(svg_out)

cairosvg.svg2png(url='/home/sprite/slop-salon-gert/assets/register-cobweb-2026-06-05.svg',
                 write_to='/home/sprite/slop-salon-gert/assets/register-cobweb-2026-06-05.png',
                 output_width=1600, output_height=800)

from PIL import Image
img = Image.open('/home/sprite/slop-salon-gert/assets/register-cobweb-2026-06-05.png')
img.save('/home/sprite/slop-salon-gert/assets/register-cobweb-2026-06-05.webp', 'WEBP', quality=85)
print("Done")
