#!/usr/bin/env python3
"""Crop a single incoming message bubble out of an Instagram DM screenshot (dark mode),
with transparent rounded corners, for use as a social-proof pop-in.

Only the bubble is kept: no avatar, name, handle or timestamp. Give a rough box around the
bubble (in screenshot pixels); the exact bubble edges are found from its colour.

usage: crop_dm.py screenshot.png x0 y0 x1 y1 out.png
"""
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

BUBBLE = (37, 40, 46)  # Instagram dark-mode incoming bubble


def crop(src, box, out):
    im = Image.open(src).convert("RGB").crop(box)
    w, h = im.size
    px = im.load()

    def is_bubble(p):
        return all(abs(p[k] - BUBBLE[k]) <= 6 for k in range(3))

    cols = [x for x in range(w) if sum(is_bubble(px[x, y]) for y in range(0, h, 3)) > h // 9]
    rows = [y for y in range(h) if sum(is_bubble(px[x, y]) for x in range(0, w, 3)) > w // 9]
    x0, x1, y0, y1 = cols[0], cols[-1], rows[0], rows[-1]
    b = im.crop((x0, y0, x1 + 1, y1 + 1))
    bw, bh = b.size
    r = min(62, bh // 2)
    mask = Image.new("L", (bw * 4, bh * 4), 0)  # supersampled for smooth corners
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw * 4 - 1, bh * 4 - 1), r * 4, fill=255)
    mask = mask.resize((bw, bh), Image.LANCZOS)
    b = b.convert("RGBA")
    b.putalpha(mask)
    pad = 22
    canvas = Image.new("RGBA", (bw + 2 * pad, bh + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 110), (pad, pad + 6), mask)
    canvas = Image.alpha_composite(canvas, sh.filter(ImageFilter.GaussianBlur(10)))
    canvas.alpha_composite(b, (pad, pad))
    canvas.save(out)
    return canvas.size


if __name__ == "__main__":
    s, x0, y0, x1, y1, o = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
    print(o, crop(s, (x0, y0, x1, y1), o))
