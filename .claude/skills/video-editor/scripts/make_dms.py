#!/usr/bin/env python3
"""Render customer DMs as clean, anonymous chat bubbles (PNG with alpha) for ad overlays.

Retype the message text exactly; never include names, handles or profile photos.
Product names in the message (e.g. "Scout") are tinted Rust Brown.

usage: make_dms.py out_dir "message one" "message two" ... [--highlight Scout]
"""
import argparse
import os
import re

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
CREAM, INK, RUST = (252, 250, 240), (20, 20, 20), (178, 61, 46)
MAX_W, SIZE, PAD, RADIUS = 820, 42, 38, 46


def wrap(draw, words, font, width):
    lines, cur = [], []
    for w in words:
        test = " ".join(cur + [w])
        if cur and draw.textlength(test, font=font) > width:
            lines.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(cur)
    return lines


def bubble(text, highlight, path):
    f, fb = ImageFont.truetype(FONT, SIZE), ImageFont.truetype(BOLD, SIZE)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    lines = wrap(tmp, text.split(), f, MAX_W - 2 * PAD)
    lh = int(SIZE * 1.32)
    w = int(max(tmp.textlength(" ".join(l), font=f) for l in lines)) + 2 * PAD
    h = lh * len(lines) + 2 * PAD - (lh - SIZE)
    sh = 24  # room for the soft shadow
    img = Image.new("RGBA", (w + 2 * sh, h + 2 * sh), (0, 0, 0, 0))
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((sh, sh + 6, sh + w, sh + h + 6), RADIUS, fill=(0, 0, 0, 90))
    img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((sh, sh, sh + w, sh + h), RADIUS, fill=CREAM + (255,))
    y = sh + PAD - 4
    hl = {h.lower() for h in highlight}
    for line in lines:
        x = sh + PAD
        for k, word in enumerate(line):
            bare = re.sub(r"[^a-z]", "", word.lower())
            is_hl = bare in hl
            font = fb if is_hl else f
            d.text((x, y), word, font=font, fill=RUST if is_hl else INK)
            x += d.textlength(word + " ", font=font)
        y += lh
    img.save(path)
    return img.size


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("messages", nargs="+")
    ap.add_argument("--highlight", nargs="*", default=["scout"])
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    for i, m in enumerate(a.messages):
        print(f"{a.out_dir}/dm{i:02d}.png", bubble(m, a.highlight, f"{a.out_dir}/dm{i:02d}.png"))
