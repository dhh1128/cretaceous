#!/usr/bin/env python3
"""Draw a KDP paperback cover template: a full-wrap canvas with the guides on it.

    uv run --with pillow python3 build/cover-template.py [pages] [out.png]

Defaults: 284 pages (the fifth-draft interior), ~/Downloads/drift/drift-cover-template.png.
Geometry is KDP's (help topic G201953020): 6x9in trim, cream paper at 0.0025in per
page of spine, 0.125in bleed on the outside edges, text kept 0.125in inside trim and
0.0625in from each spine fold. 600 DPI so every guide lands on a whole pixel.

The barcode box is approximate: KDP's page gives no size. 2 x 1.2in at 0.25in
from the spine and bottom trim is the commonly cited area, so treat it as keep-clear.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DPI = 600
TRIM_W, TRIM_H, BLEED = 6.0, 9.0, 0.125
PER_PAGE = 0.0025  # cream
SAFE, SPINE_SAFE = 0.125, 0.0625

pages = int(sys.argv[1]) if len(sys.argv) > 1 else 284
out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.home() / "Downloads/drift/drift-cover-template.png"

spine = pages * PER_PAGE
W = BLEED + TRIM_W + spine + TRIM_W + BLEED
H = BLEED + TRIM_H + BLEED
px = lambda inches: round(inches * DPI)

back_l, back_r = BLEED, BLEED + TRIM_W
front_l, front_r = back_r + spine, back_r + spine + TRIM_W
top, bottom = BLEED, BLEED + TRIM_H

img = Image.new("RGB", (px(W), px(H)), "white")
d = ImageDraw.Draw(img)

def font(size_in):
    for name in ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(name, px(size_in))
        except OSError:
            pass
    return ImageFont.load_default()

BIG, MID, SMALL = font(0.32), font(0.16), font(0.11)
RED, BLUE, GREEN, GREY, ORANGE = (220, 40, 40), (40, 90, 220), (20, 150, 70), (90, 90, 90), (235, 140, 20)

# Bleed: shaded band outside the trim.
shade = (255, 225, 225)
for box in ((0, 0, W, top), (0, bottom, W, H), (0, 0, back_l, H), (front_r, 0, W, H)):
    d.rectangle([px(box[0]), px(box[1]), px(box[2]) - 1, px(box[3]) - 1], fill=shade)
# Spine.
d.rectangle([px(back_r), px(top), px(front_l) - 1, px(bottom) - 1], fill=(235, 235, 245))

def rect(l, t, r, b, colour, width, dash=0):
    if not dash:
        d.rectangle([px(l), px(t), px(r), px(b)], outline=colour, width=width)
        return
    step = px(dash)
    for a, bb, horizontal, fixed in ((l, r, True, t), (l, r, True, b), (t, b, False, l), (t, b, False, r)):
        x = px(a)
        while x < px(bb):
            e = min(x + step, px(bb))
            if horizontal:
                d.line([(x, px(fixed)), (e, px(fixed))], fill=colour, width=width)
            else:
                d.line([(px(fixed), x), (px(fixed), e)], fill=colour, width=width)
            x += 2 * step

# Trim (where the book is cut): red.
rect(back_l, top, front_r, bottom, RED, 6)
# Spine folds: blue.
for x in (back_r, front_l):
    d.line([(px(x), 0), (px(x), px(H))], fill=BLUE, width=5)
# Safe zones: green dashed.
rect(back_l + SAFE, top + SAFE, back_r - SAFE, bottom - SAFE, GREEN, 4, dash=0.08)
rect(front_l + SAFE, top + SAFE, front_r - SAFE, bottom - SAFE, GREEN, 4, dash=0.08)
rect(back_r + SPINE_SAFE, top + SAFE, front_l - SPINE_SAFE, bottom - SAFE, GREEN, 4, dash=0.08)
# Barcode keep-clear (approximate): orange, lower right of the back cover.
bc_r, bc_b = back_r - 0.25, bottom - 0.25
rect(bc_r - 2.0, bc_b - 1.2, bc_r, bc_b, ORANGE, 5, dash=0.06)
d.text((px(bc_r - 1.0), px(bc_b - 0.6)), "barcode\n(keep clear, approx. 2 x 1.2 in)",
       fill=ORANGE, font=SMALL, anchor="mm", align="center")

def label(x, y, text, f=MID, fill=GREY):
    d.multiline_text((px(x), px(y)), text, fill=fill, font=f, anchor="mm", align="center")

label((back_l + back_r) / 2, 3.2, "BACK COVER\n6 x 9 in", BIG)
label((front_l + front_r) / 2, 3.2, "FRONT COVER\n6 x 9 in", BIG)
# Spine label, rotated to read top to bottom.
s = Image.new("RGBA", (px(5.0), px(0.4)), (0, 0, 0, 0))
ImageDraw.Draw(s).text((px(2.5), px(0.2)), f"SPINE {spine:.3f} in ({pages} pp, cream)",
                       fill=GREY, font=SMALL, anchor="mm")
s = s.rotate(-90, expand=True)
img.paste(s, (px((back_r + front_l) / 2) - s.width // 2, px(H / 2) - s.height // 2), s)

legend = (
    f"Drift, KDP paperback cover\n"
    f"{W:.3f} x {H:.3f} in = {px(W)} x {px(H)} px at {DPI} DPI\n\n"
    f"red = trim line\n"
    f"blue = spine folds\n"
    f"green dashed = safe zone (keep text inside)\n"
    f"pink = 0.125 in bleed (run art to the edge)\n"
    f"orange = barcode area (approximate)\n\n"
    f"guides from the left edge:\n"
    f"trim {back_l} in, folds {back_r:.3f} and {front_l:.3f} in, trim {front_r:.3f} in"
)
label((back_l + back_r) / 2, 5.3, legend, SMALL, (60, 60, 60))

out.parent.mkdir(parents=True, exist_ok=True)
img.save(out, dpi=(DPI, DPI))
print(f"{out}: {img.width} x {img.height} px, {W:.3f} x {H:.3f} in, spine {spine:.3f} in")
