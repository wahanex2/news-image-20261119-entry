#!/usr/bin/env python3
"""news-image-20261119: one-page broadsheet of Thursday 19 November 2026.
Draws entry.png (1024x1024, deterministic, no network)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (245, 238, 218)
CARD_BG = (252, 250, 242)
CARD_LINE = (205, 195, 170)
INK = (30, 30, 30)
RED = (179, 38, 30)
NAVY = (27, 42, 74)
TAN = (222, 200, 160)
GOLD = (212, 175, 55)
GREY = (110, 105, 90)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_M = "/usr/share/fonts/truetype/noto/NotoSans-Medium.ttf"
SANS_I = "/usr/share/fonts/truetype/noto/NotoSans-Italic.ttf"

_fonts = {}


def font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# extra palette for the illustrations
WHITE = (255, 255, 255)
YELLOW = (240, 200, 60)
SKY = (135, 180, 220)
SKY_DARK = (70, 90, 140)
GREEN = (46, 125, 60)
DARK_GREEN = (20, 90, 40)
LIGHT_GREEN = (225, 240, 220)
ORANGE = (230, 120, 40)
PURPLE = (90, 60, 140)
PINK = (220, 120, 160)
BROWN = (120, 80, 40)
LIGHT_BLUE = (200, 220, 240)


def _mix(c1, c2, t):
    return (int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t))


def scene_summit(d, x, y, w, h):
    horizon = y + h * 0.70
    top, mid, low = (10, 15, 40), (90, 60, 140), (230, 120, 40)
    n = 14
    for i in range(n):
        t = (i + 0.5) / n
        col = _mix(top, mid, t / 0.62) if t < 0.62 else _mix(mid, low, (t - 0.62) / 0.38)
        y0 = y + (horizon - y) * i / n
        y1 = y + (horizon - y) * (i + 1) / n
        d.rectangle([x, y0, x + w - 1, y1], fill=col)
    sr = min(w, h) * 0.09
    scx, scy = x + w * 0.78, horizon - h * 0.02
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=(240, 170, 90))
    d.rectangle([x, horizon, x + w - 1, y + h - 1], fill=(18, 24, 48))
    sol = (14, 18, 42)
    pat = [0.55, 0.85, 0.40, 0.70, 1.0, 0.50, 0.75, 0.35, 0.90, 0.62, 0.45, 0.82]
    nb = len(pat)
    unit = w / nb
    maxbh = h * 0.42
    for i, p in enumerate(pat):
        bx = x + i * unit
        bw = unit * 0.86
        bh = maxbh * p
        ty = horizon - bh
        d.rectangle([bx, ty, bx + bw, horizon + 1], fill=sol)
        ww = max(1.0, bw * 0.16)
        wh = max(1.0, bh * 0.07)
        gapx, gapy = ww * 1.8, wh * 2.0
        cols = max(1, int(bw / gapx))
        rows = max(1, int(bh / gapy))
        for r in range(rows):
            for c in range(cols):
                if (i * 5 + r * 3 + c * 7) % 4 == 0:
                    continue
                wx = bx + gapx * 0.5 + c * gapx
                wy = ty + gapy * 0.6 + r * gapy
                d.rectangle([wx, wy, wx + ww, wy + wh], fill=YELLOW)
    for fx, flag in ((0.20, "cn"), (0.50, "us"), (0.80, "ru")):
        px = x + w * fx
        d.line([(px, horizon), (px, y + h * 0.18)], fill=GREY, width=2)
        fw, fh = w * 0.11, h * 0.11
        fx0, fy0 = px + 1, y + h * 0.18
        if flag == "cn":
            d.rectangle([fx0, fy0, fx0 + fw, fy0 + fh], fill=RED)
            d.ellipse([fx0 + fw * 0.15, fy0 + fh * 0.2, fx0 + fw * 0.35, fy0 + fh * 0.45], fill=YELLOW)
        elif flag == "us":
            for s in range(5):
                col = RED if s % 2 == 0 else WHITE
                d.rectangle([fx0, fy0 + fh * s / 5, fx0 + fw, fy0 + fh * (s + 1) / 5], fill=col)
            d.rectangle([fx0, fy0, fx0 + fw * 0.45, fy0 + fh * 0.5], fill=NAVY)
        else:
            for s, col in enumerate((WHITE, (60, 110, 200), RED)):
                d.rectangle([fx0, fy0 + fh * s / 3, fx0 + fw, fy0 + fh * (s + 1) / 3], fill=col)


def scene_gta(d, x, y, w, h):
    horizon = y + h * 0.72
    top, mid, low = (60, 30, 110), (180, 60, 140), (240, 130, 50)
    n = 14
    for i in range(n):
        t = (i + 0.5) / n
        col = _mix(top, mid, t / 0.55) if t < 0.55 else _mix(mid, low, (t - 0.55) / 0.45)
        y0 = y + (horizon - y) * i / n
        y1 = y + (horizon - y) * (i + 1) / n
        d.rectangle([x, y0, x + w - 1, y1], fill=col)
    for sx, sy in ((0.12, 0.12), (0.30, 0.07), (0.68, 0.10), (0.88, 0.06)):
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1], fill=WHITE)
    sr = min(w, h) * 0.16
    scx, scy = x + w * 0.62, horizon - h * 0.24
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=ORANGE)
    d.rectangle([x, horizon, x + w - 1, y + h - 1], fill=(40, 20, 60))
    sil = (45, 25, 70)
    base = horizon
    for i, (bx0, bw, bh) in enumerate(((0.00, 0.16, 0.42), (0.15, 0.12, 0.60),
                                      (0.26, 0.18, 0.50), (0.43, 0.12, 0.68),
                                      (0.54, 0.16, 0.46), (0.69, 0.13, 0.58),
                                      (0.81, 0.19, 0.44))):
        bx = x + w * bx0
        bwpx = w * bw
        ty = base - h * bh
        d.rectangle([bx, ty, bx + bwpx, base + 1], fill=sil)
        for r in range(4):
            for c in range(3):
                if (i + r + c) % 3 == 0:
                    continue
                wx = bx + bwpx * 0.15 + c * bwpx * 0.28
                wy = ty + h * 0.06 + r * h * 0.10
                d.rectangle([wx, wy, wx + 2, wy + 2], fill=YELLOW if (r + c) % 2 else PINK)
    for px in (0.08, 0.36, 0.93):
        tx = x + w * px
        d.line([(tx, base), (tx, base - h * 0.30)], fill=sil, width=2)
        for ang in (-0.9, -0.45, 0.0, 0.45, 0.9):
            ex = tx + 14 * ang
            ey = base - h * 0.30 - 6 * abs(ang)
            d.line([(tx, base - h * 0.30), (ex, ey)], fill=sil, width=2)


def scene_anthropic(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=LIGHT_GREEN)
    fnt = ImageFont.truetype(SANS_B, int(h * 0.40))
    d.text((x + w * 0.04, y + h * 0.04), "$83", font=fnt, fill=DARK_GREEN)
    base = y + h * 0.86
    top = y + h * 0.30
    heights = [0.22, 0.34, 0.46, 0.60, 0.78]
    cw = w * 0.11
    gap = w * 0.055
    x0 = x + w * 0.08
    tops = []
    for i, hh in enumerate(heights):
        cx = x0 + i * (cw + gap)
        ch = h * hh
        cy = base - ch
        tops.append((cx + cw / 2, cy))
        d.line([(cx + cw / 2, cy - h * 0.06), (cx + cw / 2, base + h * 0.02)], fill=DARK_GREEN, width=2)
        d.rectangle([cx, cy, cx + cw, base], fill=GREEN)
    d.line([tops[0], tops[-1]], fill=RED, width=3)
    d.polygon([(tops[-1][0], tops[-1][1]), (tops[-1][0] - 8, tops[-1][1] + 2),
               (tops[-1][0] - 2, tops[-1][1] + 9)], fill=RED)


def scene_court(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=LIGHT_BLUE)
    for cx, cy, r in ((0.15, 0.16, 0.10), (0.85, 0.12, 0.08)):
        d.ellipse([x + w * (cx - r), y + h * (cy - r * 0.5),
                   x + w * (cx + r), y + h * (cy + r * 0.5)], fill=WHITE)
    bx, by, bw, bh = x + w * 0.18, y + h * 0.30, w * 0.64, h * 0.42
    d.rectangle([bx, by + bh, bx + bw, by + bh + h * 0.08], fill=(200, 200, 200))
    d.rectangle([bx, by + bh + h * 0.08, bx + bw, by + bh + h * 0.16], fill=(180, 180, 180))
    for i in range(4):
        cx = bx + bw * (0.12 + i * 0.25)
        d.rectangle([cx, by + h * 0.14, cx + w * 0.03, by + bh], fill=WHITE)
    d.rectangle([bx, by + h * 0.14, bx + bw, by + h * 0.20], fill=WHITE)
    d.polygon([(bx - w * 0.02, by + h * 0.14), (bx + bw + w * 0.02, by + h * 0.14),
               (bx + bw / 2, by - h * 0.06)], fill=WHITE)
    d.rectangle([bx + bw * 0.42, by + bh - h * 0.16, bx + bw * 0.58, by + bh], fill=(90, 70, 50))
    for tx in (0.06, 0.94):
        d.ellipse([x + w * tx - w * 0.05, by + bh - h * 0.10,
                   x + w * tx + w * 0.05, by + bh + h * 0.10], fill=GREEN)


def scene_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(250, 240, 190))
    d.ellipse([x + w * 0.78, y + h * 0.06, x + w * 0.94, y + h * 0.06 + w * 0.16], fill=YELLOW)
    d.rectangle([x, y + h * 0.78, x + w - 1, y + h - 1], fill=(120, 160, 90))
    for px, py, s in ((0.12, 0.55, 1.0), (0.42, 0.60, 0.9), (0.70, 0.52, 1.0)):
        x0, y0 = x + w * px, y + h * py
        d.polygon([(x0, y0), (x0 + w * 0.20 * s, y0 - h * 0.06),
                   (x0 + w * 0.24 * s, y0 + h * 0.10),
                   (x0 + w * 0.04 * s, y0 + h * 0.16)], fill=(40, 80, 160))
        d.line([(x0 + w * 0.10 * s, y0 + h * 0.02), (x0 + w * 0.14 * s, y0 + h * 0.02)], fill=WHITE, width=1)
    for tx in (0.30, 0.88):
        px = x + w * tx
        py = y + h * 0.42
        d.line([(px, py), (px, y + h * 0.78)], fill=WHITE, width=2)
        for ang in (0.0, 2.1, 4.2):
            import math
            ex = px + 15 * math.cos(ang)
            ey = py + 15 * math.sin(ang)
            d.line([(px, py), (ex, ey)], fill=WHITE, width=2)


def scene_akvan(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(170, 190, 210))
    for cx, cy, r in ((0.25, 0.18, 0.16), (0.60, 0.12, 0.20), (0.85, 0.22, 0.13)):
        d.ellipse([x + w * (cx - r), y + h * cy, x + w * (cx + r), y + h * cy + h * 0.14], fill=(90, 105, 125))
    for i in range(9):
        rx = x + w * (0.05 + i * 0.10)
        ry = y + h * (0.34 + (i % 3) * 0.06)
        d.line([(rx, ry), (rx - 3, ry + 10)], fill=(220, 230, 240), width=1)
    d.rectangle([x, y + h * 0.72, x + w - 1, y + h - 1], fill=(40, 90, 140))
    for i in range(3):
        wx = x + w * (0.10 + i * 0.30)
        wy = y + h * (0.78 + (i % 2) * 0.05)
        d.arc([wx, wy, wx + w * 0.22, wy + h * 0.10], 180, 360, fill=WHITE, width=2)
    for hx in (0.18, 0.62):
        hx0 = x + w * hx
        hy0 = y + h * 0.58
        d.rectangle([hx0, hy0, hx0 + w * 0.16, hy0 + h * 0.14], fill=(240, 230, 210))
        d.polygon([(hx0 - w * 0.02, hy0), (hx0 + w * 0.18, hy0),
                   (hx0 + w * 0.08, hy0 - h * 0.10)], fill=RED)


def scene_apec(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(238, 228, 205))
    for fx, flag in ((0.18, "cn"), (0.50, "us"), (0.82, "ru")):
        px = x + w * fx
        d.line([(px, y + h * 0.42), (px, y + h * 0.10)], fill=GREY, width=2)
        fw, fh = w * 0.13, h * 0.13
        fx0, fy0 = px + 1, y + h * 0.10
        if flag == "cn":
            d.rectangle([fx0, fy0, fx0 + fw, fy0 + fh], fill=RED)
            d.ellipse([fx0 + fw * 0.15, fy0 + fh * 0.2, fx0 + fw * 0.35, fy0 + fh * 0.45], fill=YELLOW)
        elif flag == "us":
            for s in range(5):
                col = RED if s % 2 == 0 else WHITE
                d.rectangle([fx0, fy0 + fh * s / 5, fx0 + fw, fy0 + fh * (s + 1) / 5], fill=col)
            d.rectangle([fx0, fy0, fx0 + fw * 0.45, fy0 + fh * 0.5], fill=NAVY)
        else:
            for s, col in enumerate((WHITE, (60, 110, 200), RED)):
                d.rectangle([fx0, fy0 + fh * s / 3, fx0 + fw, fy0 + fh * (s + 1) / 3], fill=col)
    d.ellipse([x + w * 0.04, y + h * 0.44, x + w * 0.96, y + h * 0.86], fill=(120, 75, 40))
    d.ellipse([x + w * 0.04, y + h * 0.44, x + w * 0.96, y + h * 0.72], fill=(150, 95, 50))
    for px in (0.22, 0.50, 0.78):
        d.ellipse([x + w * px - w * 0.06, y + h * 0.52, x + w * px + w * 0.06, y + h * 0.52 + h * 0.10], fill=WHITE)
    d.ellipse([x + w * 0.44, y + h * 0.30, x + w * 0.56, y + h * 0.30 + h * 0.12], fill=(90, 140, 90))


def scene_bogota(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(190, 220, 240))
    d.ellipse([x + w * 0.78, y + h * 0.08, x + w * 0.92, y + h * 0.08 + w * 0.14], fill=YELLOW)
    for cx, cy, r in ((0.20, 0.14, 0.12), (0.55, 0.10, 0.10)):
        d.ellipse([x + w * (cx - r), y + h * cy, x + w * (cx + r), y + h * cy + h * 0.08], fill=WHITE)
    d.polygon([(x, y + h), (x + w * 0.30, y + h * 0.30), (x + w * 0.62, y + h)], fill=(60, 120, 70))
    d.polygon([(x + w * 0.38, y + h), (x + w * 0.68, y + h * 0.22), (x + w * 1.0, y + h)], fill=(40, 95, 55))
    d.polygon([(x + w * 0.24, y + h * 0.42), (x + w * 0.30, y + h * 0.30),
               (x + w * 0.36, y + h * 0.42)], fill=WHITE)
    d.polygon([(x + w * 0.63, y + h * 0.34), (x + w * 0.68, y + h * 0.22),
               (x + w * 0.73, y + h * 0.34)], fill=WHITE)
    d.rectangle([x, y + h * 0.86, x + w - 1, y + h - 1], fill=(90, 140, 80))
    for mx in (0.25, 0.55, 0.80):
        d.ellipse([x + w * mx - 2, y + h * 0.90, x + w * mx + 2, y + h * 0.90 + 4], fill=(30, 30, 30))


def scene_florida(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(150, 165, 180))
    for cx, cy, r in ((0.22, 0.14, 0.15), (0.62, 0.10, 0.18), (0.88, 0.18, 0.12)):
        d.ellipse([x + w * (cx - r), y + h * cy, x + w * (cx + r), y + h * cy + h * 0.12], fill=(95, 105, 120))
    for i in range(8):
        rx = x + w * (0.06 + i * 0.11)
        ry = y + h * (0.28 + (i % 3) * 0.05)
        d.line([(rx, ry), (rx - 3, ry + 9)], fill=(220, 230, 240), width=1)
    d.rectangle([x, y + h * 0.55, x + w - 1, y + h - 1], fill=(50, 110, 160))
    for i in range(3):
        wx = x + w * (0.06 + i * 0.30)
        wy = y + h * (0.62 + (i % 2) * 0.07)
        d.arc([wx, wy, wx + w * 0.24, wy + h * 0.10], 180, 360, fill=WHITE, width=2)
    for hx in (0.14, 0.58):
        hx0 = x + w * hx
        hy0 = y + h * 0.42
        d.rectangle([hx0, hy0, hx0 + w * 0.18, hy0 + h * 0.20], fill=(240, 230, 210))
        d.polygon([(hx0 - w * 0.02, hy0), (hx0 + w * 0.20, hy0),
                   (hx0 + w * 0.09, hy0 - h * 0.10)], fill=RED)
        d.rectangle([hx0 + w * 0.06, hy0 + h * 0.08, hx0 + w * 0.12, hy0 + h * 0.20], fill=(90, 70, 50))


def scene_suneung(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(235, 230, 215))
    fnt = ImageFont.truetype(SANS_B, int(h * 0.16))
    d.text((x + w * 0.32, y + h * 0.04), "SUNEUNG", font=fnt, fill=INK)
    d.ellipse([x + w * 0.82, y + h * 0.05, x + w * 0.94, y + h * 0.05 + w * 0.12], fill=WHITE)
    d.ellipse([x + w * 0.82, y + h * 0.05, x + w * 0.94, y + h * 0.05 + w * 0.12], outline=INK, width=1)
    d.line([(x + w * 0.88, y + h * 0.05 + w * 0.06), (x + w * 0.88, y + h * 0.05 + w * 0.02)], fill=INK, width=1)
    d.line([(x + w * 0.88, y + h * 0.05 + w * 0.06), (x + w * 0.91, y + h * 0.05 + w * 0.08)], fill=INK, width=1)
    d.rectangle([x + w * 0.06, y + h * 0.28, x + w * 0.94, y + h * 0.34], fill=(120, 90, 60))
    for r in range(3):
        for c in range(4):
            dx = x + w * (0.08 + c * 0.22)
            dy = y + h * (0.42 + r * 0.20)
            d.rectangle([dx, dy, dx + w * 0.16, dy + h * 0.07], fill=(150, 110, 70))
            d.ellipse([dx + w * 0.06, dy - h * 0.09, dx + w * 0.10, dy - h * 0.05], fill=(60, 60, 60))
            d.rectangle([dx + w * 0.02, dy + h * 0.09, dx + w * 0.14, dy + h * 0.11], fill=(200, 200, 200))


def scene_canberra(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(240, 238, 228))
    fnt = ImageFont.truetype(SANS_B, int(h * 0.30))
    d.text((x + w * 0.06, y + h * 0.04), "4.9%", font=fnt, fill=RED)
    base = y + h * 0.88
    d.line([(x + w * 0.08, base), (x + w * 0.94, base)], fill=INK, width=2)
    heights = [0.30, 0.38, 0.34, 0.46, 0.52]
    bw = w * 0.11
    gap = w * 0.05
    x0 = x + w * 0.10
    for i, hh in enumerate(heights):
        cx = x0 + i * (bw + gap)
        ch = h * hh
        d.rectangle([cx, base - ch, cx + bw, base], fill=(90, 120, 170) if i < 4 else RED)
    d.line([(x + w * 0.10, y + h * 0.52), (x + w * 0.90, y + h * 0.30)], fill=RED, width=2)


def scene_tokyo(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(215, 230, 240))
    d.ellipse([x + w * 0.80, y + h * 0.06, x + w * 0.94, y + h * 0.06 + w * 0.14], fill=YELLOW)
    tx, ty, tw = x + w * 0.30, y + h * 0.22, w * 0.40
    d.rectangle([tx, ty, tx + tw, ty + h * 0.06], fill=RED)
    d.rectangle([tx + tw * 0.08, ty + h * 0.12, tx + tw * 0.92, ty + h * 0.17], fill=RED)
    d.rectangle([tx + tw * 0.10, ty + h * 0.17, tx + tw * 0.20, ty + h * 0.72], fill=RED)
    d.rectangle([tx + tw * 0.80, ty + h * 0.17, tx + tw * 0.90, ty + h * 0.72], fill=RED)
    d.rectangle([tx - tw * 0.04, ty + h * 0.72, tx + tw * 1.04, ty + h * 0.76], fill=RED)
    for fx, flag in ((0.06, "jp"), (0.86, "in")):
        fx0, fy0 = x + w * fx, y + h * 0.60
        fw, fh = w * 0.12, h * 0.14
        if flag == "jp":
            d.rectangle([fx0, fy0, fx0 + fw, fy0 + fh], fill=WHITE)
            d.ellipse([fx0 + fw * 0.32, fy0 + fh * 0.22, fx0 + fw * 0.68, fy0 + fh * 0.78], fill=RED)
        else:
            for s, col in enumerate(((255, 153, 51), WHITE, (19, 136, 8))):
                d.rectangle([fx0, fy0 + fh * s / 3, fx0 + fw, fy0 + fh * (s + 1) / 3], fill=col)
            d.ellipse([fx0 + fw * 0.42, fy0 + fh * 0.38, fx0 + fw * 0.58, fy0 + fh * 0.62], fill=NAVY)


def scene_jakarta(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(235, 225, 200))
    d.rectangle([x + w * 0.08, y + h * 0.62, x + w * 0.92, y + h * 0.70], fill=(150, 110, 60))
    for i, (mx, my) in enumerate(((0.16, 0.50), (0.34, 0.54), (0.52, 0.50), (0.70, 0.54))):
        d.rectangle([x + w * mx, y + h * my, x + w * mx + w * 0.16, y + h * my + h * 0.10], fill=(70, 140, 70))
        d.ellipse([x + w * mx + w * 0.06, y + h * my + h * 0.02,
                   x + w * mx + w * 0.10, y + h * my + h * 0.08], fill=(220, 230, 200))
    for cx, cy in ((0.22, 0.44), (0.80, 0.40)):
        d.ellipse([x + w * cx - w * 0.05, y + h * cy - h * 0.04,
                   x + w * cx + w * 0.05, y + h * cy + h * 0.04], fill=GOLD)
        d.ellipse([x + w * cx - w * 0.05, y + h * cy - h * 0.04,
                   x + w * cx + w * 0.05, y + h * cy + h * 0.04], outline=(150, 110, 20), width=1)
    gx, gy = x + w * 0.55, y + h * 0.28
    d.polygon([(gx, gy), (gx + w * 0.22, gy - h * 0.10), (gx + w * 0.26, gy - h * 0.02),
               (gx + w * 0.04, gy + h * 0.08)], fill=(90, 60, 30))
    d.rectangle([gx + w * 0.02, gy + h * 0.06, gx + w * 0.24, gy + h * 0.10], fill=(90, 60, 30))


def _star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-60, 62), (-55, 47),
     (-70, 42), (-80, 32), (-90, 21), (-97, 16), (-105, 20), (-115, 30), (-125, 40),
     (-150, 60), (-168, 66)],
    [(-55, 60), (-40, 65), (-30, 70), (-45, 76), (-60, 74), (-55, 60)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5), (-35, -10), (-40, -20),
     (-48, -28), (-58, -35), (-65, -45), (-70, -54), (-73, -40), (-75, -25), (-80, -5),
     (-80, 10)],
    [(-10, 36), (-5, 44), (0, 48), (5, 55), (10, 58), (18, 56), (25, 60), (30, 70),
     (40, 68), (45, 60), (40, 50), (30, 45), (25, 40), (15, 38), (5, 38), (-10, 36)],
    [(-18, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15),
     (48, 11), (51, 10), (45, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -30),
     (12, -18), (10, -5), (8, 4), (-8, 5), (-18, 15)],
    [(40, 70), (60, 72), (80, 73), (100, 76), (120, 73), (140, 72), (160, 70),
     (178, 66), (170, 60), (160, 55), (150, 45), (140, 40), (130, 35), (122, 30),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 10),
     (75, 8), (70, 20), (60, 25), (55, 26), (50, 30), (45, 30), (42, 40), (40, 50),
     (40, 70)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (135, -12), (130, -13), (122, -17), (113, -22)],
]

PINS = [
    (1, 114.1, 22.5), (2, 174.8, -36.8), (3, -74.0, 40.7), (4, 4.3, 52.1),
    (5, 30.7, 36.9), (6, 85.8, 20.3), (7, 117.5, 22.5), (8, -74.1, 4.7),
    (9, -81.7, 27.9), (10, 127.0, 37.6), (11, 149.1, -35.3), (12, 139.7, 35.7),
    (13, 106.8, -6.2),
]
STAR_LONLAT = (56.3, 26.5)


def scene_map(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=1)

    def proj(lon, lat):
        px = x + (lon + 180.0) / 360.0 * w
        py = y + (90.0 - lat) / 150.0 * h
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=TAN)
    for lon in range(-180, 181, 30):
        px = x + (lon + 180.0) / 360.0 * w
        d.line([(px, y), (px, y + h - 1)], fill=(35, 52, 88), width=1)
    fnt = ImageFont.truetype(SANS_B, 10)
    for num, lon, lat in PINS:
        px, py = proj(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=WHITE, width=1)
        tw = d.textlength(str(num), font=fnt)
        d.text((px - tw / 2, py - 5), str(num), font=fnt, fill=WHITE)
    sx, sy = proj(*STAR_LONLAT)
    _star(d, sx, sy, 9, GOLD)
    cap = "Red numbers mark stories 1-13; star marks the Hormuz energy story."
    cfnt = ImageFont.truetype(SANS, 10)
    tw = d.textlength(cap, font=cfnt)
    d.text((x + (w - tw) / 2, y + h - 14), cap, font=cfnt, fill=WHITE)


CARDS = [
    (1, "SHENZHEN", "POLITICS", "Xi hosts Trump and Putin in Shenzhen",
     "First three-way summit opens APEC: an hour on nuclear arms, Iran, trade. Ukraine is off the agenda.",
     "scene_summit", True),
    (2, "WORLDWIDE", "CULTURE", "GTA VI goes on sale worldwide",
     "Midnight worldwide, New Zealand first. Metacritic 99/100; analysts see $1.65bn in early sales.",
     "scene_gta", True),
    (3, "NEW YORK", "TECH", "Anthropic lists on Nasdaq as ANT",
     "Priced at $83, it raises $81.3bn — the largest IPO ever, worth about $1.5tn.",
     "scene_anthropic", True),
    (4, "THE HAGUE", "LAW", "World court rules on Myanmar",
     "Judgment read at 10:00 CET; 700,000+ Rohingya fled in 2017.",
     "scene_court", False),
    (5, "ANTALYA", "CLIMATE", "COP31 enters its final stretch",
     "Drafts due Thursday; Africa seeks $120bn a year by 2035.",
     "scene_cop31", False),
    (6, "ODISHA", "WEATHER", "Odisha evacuates 47,000 as Akvan nears",
     "Landfall by noon Friday; winds 90–100 kmph, 448 shelters open.",
     "scene_akvan", False),
    (7, "SHENZHEN", "POLITICS", "APEC opens; Xi pledges $20m",
     "Xi pledges $20m for APEC; Putin backs the draft declaration.",
     "scene_apec", False),
    (8, "BOGOTÁ", "POLITICS", "Paro Nacional: Colombia strikes",
     "Unions strike over the Rescue bill; marches in five cities.",
     "scene_bogota", False),
    (9, "FLORIDA", "WEATHER", "Florida floods: rain is not done",
     "14–17 inches fell; 300+ calls for help; more rain expected.",
     "scene_florida", False),
    (10, "SEOUL", "SOCIETY", "Korea's college exam stops a nation",
     "551,864 sit the Suneung; flights pause 13:05–13:40.",
     "scene_suneung", False),
    (11, "CANBERRA", "ECONOMY", "Australia's jobless rate hits 4.9%",
     "Jobless 4.9%, highest since October 2021; 43,500 jobs lost.",
     "scene_canberra", False),
    (12, "TOKYO", "DEFENCE", "India and Japan meet on defence",
     "Fourth 2+2 in Tokyo: defence tech, chips, critical minerals.",
     "scene_tokyo", False),
    (13, "JAKARTA", "LAW", "Indonesia passes asset-forfeiture law",
     "Corruption assets seized without conviction first.",
     "scene_jakarta", False),
]

BRIEFS = [
    (14, "PARIS", "IEA: the Iran war cost 2.8bn barrels of oil and 60bcm of gas."),
    (15, "SHENZHEN", "Trump and Putin to meet one-on-one after the summit."),
    (16, "TOKYO", "Japan's AI stocks lose their premium."),
    (17, "WASHINGTON", "Traders price a December Fed hike at 96%."),
    (18, "WELLINGTON", "Bumrah removes Latham for a two-ball duck in the first over."),
    (19, "TATARSTAN", "Ukrainian drones hit the Kaleykino oil pumping station."),
    (20, "GLOBAL", "Bitcoin falls to a four-month low near $62,000."),
    (21, "ARIZONA", "Criminal probe into OpenAI over rogue AI agents; announced Wednesday."),
    (22, "LONDON", "Japanese investors put about $3bn into Anthropic's IPO."),
    (23, "LONDON", "Cyber incidents reported to Britain's financial watchdog hit 38 in October."),
    (24, "LONDON", "Traders trim bets on a December Bank of England hike to 70%."),
    (25, "GAUTENG", "Civic groups say voters are shut out of coalition talks."),
    (26, "PRETORIA", "17 South Africans lured to Russia's front lines begin returning."),
    (27, "BRASÍLIA", "Brazil's football body drops the 2027 South-Southeast Cup."),
    (28, "SÃO PAULO", "Brazil's sugar mills face their weakest margins in a decade."),
    (29, "PARIS", "France's parliament examines a bill banning trade with settlements."),
    (30, "PARIS", "France's space sector scores 705/1000 on cyber maturity."),
    (31, "BERLIN", "Europe's \"Coalition of the Willing\" meets today to answer Shenzhen."),
    (32, "LUDWIGSHAFEN", "BASF's bid for Evonik stalls; Jefferies cuts to Underperform."),
    (33, "PASADENA", "Voyager 1 sends only a carrier signal; NASA briefs at noon."),
    (34, "FLORIDA", "SpaceX Dragon's ISS return retargeted for Thursday noon."),
    (35, "LAS VEGAS", "Formula 1 returns to the Strip; Alonso sits out first practice."),
    (36, "ABUJA", "Nigeria's National Assembly sends the state-police bill to President Tinubu."),
    (37, "ABUJA", "Governments share 2.44 trillion naira in October revenue."),
    (38, "ABUJA", "Electoral body rules out uploading ward results to IReV for 2027."),
]

NUMBERS = [
    ("$81.3bn", "Anthropic IPO, largest ever"),
    ("551,864", "Suneung candidates in Korea"),
    ("47,000+", "evacuated in Odisha as Akvan nears"),
    ("96%", "odds of a December Fed hike"),
    ("$62,000", "Bitcoin, a four-month low"),
    ("4.9%", "Australia jobless, a five-year high"),
    ("2.8bn", "barrels of oil lost, says the IEA"),
]

REGIONS = [
    ("ASIA-PACIFIC", 10, (30, 120, 70)), ("EUROPE", 7, (40, 90, 170)),
    ("NORTH AMERICA", 7, (180, 60, 50)), ("AFRICA", 5, (200, 140, 40)),
    ("GLOBAL", 4, (90, 60, 140)), ("LATIN AMERICA", 3, (60, 140, 120)),
    ("OCEANIA", 2, (200, 100, 160)),
]

DATE_CHECK = (
    "Voyager 1 one-light-day — 18 Nov · Iran/Gulf drone strikes — 18 Nov · "
    "EU €45bn Ukraine loan — 18 Nov · Kerch Bridge strike — 17 Nov · "
    "Gaza Yellow Line incursion — 18 Nov · UK inflation 3.6% — 18 Nov · "
    "Peltola's Alaska win — 17 Nov · Nvidia's $115.8bn quarter — 17 Nov · "
    "Van Gogh $190.4m sale — 18 Nov · Pew Islam-2035 projection — 18 Nov · "
    "Mélenchon \"could win\" — 18 Nov · Derna drug seizure — 17 Nov · "
    "Bangladesh wage protests — 18 Nov · Sudan cholera — 18 Nov · "
    "Australia under-16 ban — 18 Nov · US measles-free status loss — 17 Nov · "
    "Pattinson as James Bond — 16 Nov · Jeffries 251–11 nomination — 18 Nov · "
    "Dow −561 — 18 Nov"
)

FOOTER = ("Every story here happened or was first reported on Thursday 19 November 2026. "
          "Contested claims are attributed. Sources: Reuters, AP, AFP, Al Jazeera, Bloomberg.")


def draw_card(d, x, y, w, h, num, place, field, headline, deck, scene_fn, large):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=CARD_BG, outline=CARD_LINE, width=1)
    illo_h = 88 if large else 60
    scene_fn(d, x + 1, y + 1, w - 2, illo_h)
    tx = x + 8
    tag = "%d · %s · %s" % (num, place, field)
    tfnt = font(SANS_B, 11 if large else 10)
    d.text((tx, y + illo_h + 5), tag, font=tfnt, fill=RED)
    hfnt = font(SANS_B, 16 if large else 12)
    hl = wrap(d, headline, hfnt, w - 16)[:2]
    hy = text_lines(d, tx, y + illo_h + 20, hl, hfnt, INK, leading=int(hfnt.size * 1.2))
    dfnt = font(SANS, 11 if large else 10)
    dl = wrap(d, deck, dfnt, w - 16)[:2 if large else 3]
    text_lines(d, tx, hy + 2, dl, dfnt, INK, leading=int(dfnt.size * 1.25))


def build_page():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # kicker
    kfnt = font(SANS_B, 13)
    d.text((16, 10), "THE WORLD IN ONE DAY", font=kfnt, fill=RED)
    right = "THURSDAY'S NEWS · ONE PAGE · 38 STORIES"
    d.text((W - 16 - d.textlength(right, font=kfnt), 10), right, font=kfnt, fill=INK)
    # masthead
    mfnt = font(SERIF_B, 54)
    title = "Thursday 19 November 2026"
    d.text(((W - d.textlength(title, font=mfnt)) / 2, 26), title, font=mfnt, fill=INK)
    # subhead
    sfnt = font(SANS_I, 19)
    sub = "Three leaders meet in Shenzhen · A court rules on Myanmar · The biggest IPO ever debuts"
    d.text(((W - d.textlength(sub, font=sfnt)) / 2, 90), sub, font=sfnt, fill=RED)
    # region strip
    seg_w = (W - 32) / len(REGIONS)
    rfnt = font(SANS_B, 11)
    for i, (name, count, col) in enumerate(REGIONS):
        sx = 16 + i * seg_w
        d.rectangle([sx, 112, sx + seg_w - 4, 116], fill=col)
        label = "%s %d" % (name, count)
        d.text((sx + (seg_w - d.textlength(label, font=rfnt)) / 2, 120), label,
               font=rfnt, fill=INK)
    # numbers strip
    nfnt = font(SANS_B, 12)
    head = "THE DAY IN NUMBERS"
    d.text(((W - d.textlength(head, font=nfnt)) / 2, 138), head, font=nfnt, fill=INK)
    col_w = (W - 32) / len(NUMBERS)
    vfnt = font(SANS_B, 28)
    cfnt = font(SANS, 11)
    for i, (val, cap) in enumerate(NUMBERS):
        cx = 16 + i * col_w + col_w / 2
        d.text((cx - d.textlength(val, font=vfnt) / 2, 154), val, font=vfnt, fill=RED)
        lines = wrap(d, cap, cfnt, col_w - 8)[:2]
        ly = 186
        for ln in lines:
            d.text((cx - d.textlength(ln, font=cfnt) / 2, ly), ln, font=cfnt, fill=INK)
            ly += 13
    # cards row 1 (large)
    large_w = (W - 32 - 20) // 3
    for i, card in enumerate(CARDS[:3]):
        num, place, field, headline, deck, scene_name, _lg = card
        draw_card(d, 16 + i * (large_w + 10), 216, large_w, 168,
                  num, place, field, headline, deck, globals()[scene_name], True)
    # cards rows 2 and 3 (small)
    small_w = (W - 32 - 40) // 5
    for row, cards in enumerate((CARDS[3:8], CARDS[8:13])):
        cy = 392 + row * 158
        for i, card in enumerate(cards):
            num, place, field, headline, deck, scene_name, _lg = card
            draw_card(d, 16 + i * (small_w + 10), cy, small_w, 150,
                      num, place, field, headline, deck, globals()[scene_name], False)
    # map + date check
    scene_map(d, 16, 708, 470, 120)
    d.rectangle([496, 708, 1007, 827], fill=CARD_BG, outline=RED, width=2)
    hfnt = font(SANS_B, 13)
    d.text((508, 714), "DATE CHECK — NOT THURSDAY", font=hfnt, fill=RED)
    bfnt = font(SANS, 10)
    blines = wrap(d, DATE_CHECK, bfnt, 488)
    text_lines(d, 508, 734, blines, bfnt, INK, leading=12)
    # briefs
    bf_head = font(SANS_B, 13)
    d.text((16, 836), "ALSO ON THURSDAY — 25 MORE STORIES", font=bf_head, fill=INK)
    pfnt = font(SANS_B, 10)
    tfnt = font(SANS, 10)
    left = BRIEFS[:13]
    right = BRIEFS[13:]
    for col_i, col in enumerate((left, right)):
        bx = 16 + col_i * 504
        by = 856
        for num, place, text in col:
            pre = "%d. %s — " % (num, place)
            d.text((bx, by), pre, font=pfnt, fill=INK)
            d.text((bx + d.textlength(pre, font=pfnt), by), text, font=tfnt, fill=INK)
            by += 11
    # footer
    ffnt = font(SANS, 10)
    d.text(((W - d.textlength(FOOTER, font=ffnt)) / 2, 1004), FOOTER, font=ffnt, fill=GREY)
    return img


def main():
    img = build_page()
    if os.path.isdir("/output"):
        out = "/output/entry.png"
    else:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("saved", out, img.size)


if __name__ == "__main__":
    main()
