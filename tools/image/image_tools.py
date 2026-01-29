#!/usr/bin/env python3
"""Minimal local image tools.

1) Procedural tree generator (square + portrait) in a pixel-art style.
2) Pixelate an input photo to a target size (square/portrait) and optionally upscale with nearest-neighbor.

Dependencies: pillow

Usage:
  python3 image_tools.py tree --square 128 --portrait 128x192 --outdir ./out
  python3 image_tools.py pixelate --in photo.jpg --square 128 --portrait 128x192 --grid 64 --outdir ./out
"""

import argparse
import os
import random
from PIL import Image, ImageOps
from datetime import datetime


def clamp(x):
    return max(0, min(255, int(x)))

def lerp(a, b, t):
    return a + (b - a) * t


def make_tree(w, h, seed=11):
    random.seed(seed)
    img = Image.new('RGB', (w, h), (0, 0, 0))
    px = img.load()

    # sky gradient
    for y in range(h):
        t = y / (h - 1)
        r = lerp(120, 40, t)
        g = lerp(200, 110, t)
        b = lerp(255, 160, t)
        for x in range(w):
            px[x, y] = (clamp(r), clamp(g), clamp(b))

    # subtle clouds
    for _ in range(6):
        cx = random.randint(0, w - 1)
        cy = random.randint(0, int(h * 0.35))
        rad = random.randint(max(6, w // 10), max(10, w // 6))
        for yy in range(cy - rad, cy + rad + 1):
            for xx in range(cx - rad, cx + rad + 1):
                if 0 <= xx < w and 0 <= yy < h:
                    if (xx - cx) ** 2 + (yy - cy) ** 2 <= rad * rad and random.random() < 0.35:
                        r, g, b = px[xx, yy]
                        px[xx, yy] = (clamp(r + 20), clamp(g + 20), clamp(b + 20))

    # ground
    ground_y = int(h * 0.72)
    for y in range(ground_y, h):
        t = (y - ground_y) / (h - ground_y - 1 if h - ground_y > 1 else 1)
        base = (lerp(40, 25, t), lerp(140, 95, t), lerp(45, 35, t))
        for x in range(w):
            n = random.randint(-10, 10)
            px[x, y] = (clamp(base[0] + n), clamp(base[1] + n), clamp(base[2] + n))

    # trunk (tapered)
    cx = w // 2
    trunk_h = int(h * 0.30)
    trunk_top = ground_y - trunk_h
    base_w = max(10, w // 7)
    top_w = max(6, w // 10)
    bark = (115, 78, 45)

    for y in range(trunk_top, ground_y):
        t = (y - trunk_top) / (ground_y - trunk_top - 1 if ground_y - trunk_top > 1 else 1)
        tw = int(lerp(top_w, base_w, t))
        for x in range(cx - tw // 2, cx + tw // 2 + 1):
            if 0 <= x < w:
                n = random.randint(-10, 10)
                px[x, y] = (clamp(bark[0] + n), clamp(bark[1] + n), clamp(bark[2] + n))

    # branches
    for d in (-1, 1):
        bx, by = cx, trunk_top + trunk_h // 3
        for _ in range(max(6, w // 10)):
            bx += d
            by -= 1
            if 0 <= bx < w and 0 <= by < h:
                px[bx, by] = (95, 65, 38)
                if 0 <= by + 1 < h:
                    px[bx, by + 1] = (95, 65, 38)

    # canopy blobs
    green1, green2 = (50, 165, 70), (35, 135, 55)
    cy = trunk_top - int(h * 0.02)

    blobs = []
    for _ in range(18):
        ox = cx + random.randint(-w // 6, w // 6)
        oy = cy + random.randint(-h // 10, h // 12)
        rad = random.randint(max(8, w // 9), max(12, w // 6))
        blobs.append((ox, oy, rad))

    for ox, oy, rad in blobs:
        for y in range(oy - rad, oy + rad + 1):
            for x in range(ox - rad, ox + rad + 1):
                if 0 <= x < w and 0 <= y < h:
                    if (x - ox) ** 2 + (y - oy) ** 2 <= rad * rad:
                        shade = ((x - cx) + (y - cy)) / (w + h)
                        base = green1 if random.random() < 0.55 else green2
                        n = random.randint(-18, 18)
                        r = base[0] + n - 30 * shade
                        g = base[1] + n - 20 * shade
                        b = base[2] + n - 30 * shade
                        if random.random() < 0.93:
                            px[x, y] = (clamp(r), clamp(g), clamp(b))

    return img


def parse_dim(s):
    if 'x' in s:
        a, b = s.lower().split('x', 1)
        return int(a), int(b)
    n = int(s)
    return n, n


def pixelate(in_path, out_square, out_portrait, grid=64, outdir='out'):
    img = Image.open(in_path).convert('RGB')
    os.makedirs(outdir, exist_ok=True)

    sq = ImageOps.fit(img, (out_square, out_square), method=Image.Resampling.LANCZOS, centering=(0.5, 0.4))
    sq.save(os.path.join(outdir, f'square_{out_square}.png'))

    pw, ph = out_portrait
    pt = ImageOps.fit(img, (pw, ph), method=Image.Resampling.LANCZOS, centering=(0.5, 0.4))
    pt.save(os.path.join(outdir, f'portrait_{pw}x{ph}.png'))

    # pixel style
    sq_small = ImageOps.fit(img, (grid, grid), method=Image.Resampling.BILINEAR, centering=(0.5, 0.4))
    sq_pix = sq_small.resize((out_square, out_square), Image.Resampling.NEAREST)
    sq_pix.save(os.path.join(outdir, f'square_{out_square}_pixel.png'))

    # portrait grid keeps aspect
    pgrid = (grid, int(grid * (ph / pw)))
    pt_small = ImageOps.fit(img, pgrid, method=Image.Resampling.BILINEAR, centering=(0.5, 0.4))
    pt_pix = pt_small.resize((pw, ph), Image.Resampling.NEAREST)
    pt_pix.save(os.path.join(outdir, f'portrait_{pw}x{ph}_pixel.png'))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)

    ap_tree = sub.add_parser('tree')
    ap_tree.add_argument('--square', default='128')
    ap_tree.add_argument('--portrait', default='128x192')
    ap_tree.add_argument('--outdir', default='out')

    ap_pix = sub.add_parser('pixelate')
    ap_pix.add_argument('--in', dest='in_path', required=True)
    ap_pix.add_argument('--square', default='128')
    ap_pix.add_argument('--portrait', default='128x192')
    ap_pix.add_argument('--grid', type=int, default=64)
    ap_pix.add_argument('--outdir', default='out')

    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    if args.cmd == 'tree':
        s = int(args.square)
        pw, ph = parse_dim(args.portrait)
        make_tree(s, s).save(os.path.join(args.outdir, f'tree_square_{s}.png'))
        make_tree(pw, ph).save(os.path.join(args.outdir, f'tree_portrait_{pw}x{ph}.png'))
        return

    if args.cmd == 'pixelate':
        s = int(args.square)
        pw, ph = parse_dim(args.portrait)
        pixelate(args.in_path, s, (pw, ph), grid=args.grid, outdir=args.outdir)


if __name__ == '__main__':
    main()
