#!/usr/bin/env python3
"""Animate a TNB Result v2 post into a 9:16 Reel.

Usage: python3 animate_result.py full.png bg.png out.mp4 [seconds]

full.png = the finished Canva export (1080x1350).
bg.png   = the same design with every foreground element deleted
           (background, colour halves, watermarks, stripe and footer only).
Each layer is cut out of full.png by its box in the Result v2 template and
animated in: header drops in, crests slide in from each side, the score lands,
the divider grows, each team's scorers reveal line by line, then the context.
"""
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

W, H = 1080, 1350          # post size
RW, RH = 1080, 1920        # reel size
FPS = 30

# name: (x0, y0, x1, y1, start, end, kind)
LAYERS = [
    ("header",   0,   110, 1080, 280, 0.25, 0.75, "drop"),
    ("home",     120, 325, 384,  645, 0.70, 1.30, "left"),
    ("away",     698, 325, 1080, 665, 0.70, 1.30, "right"),
    ("score",    380, 385, 698,  622, 1.30, 1.70, "slam"),
    ("divider",  533, 690, 547,  860, 1.80, 2.20, "wipe"),
    ("homesc",   20,  690, 532,  870, 2.00, 2.90, "wipe"),
    ("awaysc",   548, 690, 1060, 870, 2.20, 3.10, "wipe"),
    ("info",     0,   900, 1080, 1060, 3.20, 3.80, "rise"),
]


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def ease_out_back(t, s=1.4):
    t -= 1
    return t * t * ((s + 1) * t + s) + 1


def clamp01(x):
    return max(0.0, min(1.0, x))


def main():
    full_p, bg_p, out_p = sys.argv[1:4]
    secs = float(sys.argv[4]) if len(sys.argv) > 4 else 8.0
    full = np.asarray(Image.open(full_p).convert("RGB").resize((W, H)), dtype=np.float32)
    bg = np.asarray(Image.open(bg_p).convert("RGB").resize((W, H)), dtype=np.float32)

    # Per-pixel foreground alpha from the difference between the two exports.
    diff = np.abs(full - bg).max(axis=2)
    alpha_all = np.clip((diff - 6) / 40.0, 0, 1)

    layers = []
    for name, x0, y0, x1, y1, t0, t1, kind in LAYERS:
        a = np.zeros((H, W), np.float32)
        a[y0:y1, x0:x1] = alpha_all[y0:y1, x0:x1]
        ys, xs = np.nonzero(a > 0.02)
        if len(ys) == 0:
            continue
        bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        rgba = np.dstack([full[by0:by1, bx0:bx1], a[by0:by1, bx0:bx1, None] * 255]).astype(np.uint8)
        layers.append(dict(name=name, img=Image.fromarray(rgba, "RGBA"), x=bx0, y=by0, t0=t0, t1=t1, kind=kind))

    bg_img = Image.fromarray(bg.astype(np.uint8))
    # 9:16 backdrop: the background plate scaled to cover, blurred and darkened.
    scale = RH / H
    back = bg_img.resize((int(W * scale), RH)).crop(((int(W * scale) - RW) // 2, 0, (int(W * scale) - RW) // 2 + RW, RH))
    back = back.filter(ImageFilter.GaussianBlur(28))
    back = Image.fromarray((np.asarray(back, np.float32) * 0.45).astype(np.uint8))
    top = (RH - H) // 2
    # feather mask so the post blends into the backdrop
    fm = np.ones((H, W), np.float32)
    f = 90
    ramp = np.linspace(0, 1, f)
    fm[:f] *= ramp[:, None]
    fm[-f:] *= ramp[::-1][:, None]
    feather = Image.fromarray((fm * 255).astype(np.uint8), "L")

    n = int(secs * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{RW}x{RH}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium",
           "-crf", "18", "-movflags", "+faststart", out_p]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        frame = bg_img.copy().convert("RGBA")
        for L in layers:
            p = clamp01((t - L["t0"]) / (L["t1"] - L["t0"]))
            if p <= 0:
                continue
            img, x, y = L["img"], L["x"], L["y"]
            k = L["kind"]
            op = 1.0
            if k == "drop":
                e = ease_out_cubic(p); y = int(y - 60 * (1 - e)); op = e
            elif k == "left":
                e = ease_out_back(p); x = int(x - 520 * (1 - e)); op = clamp01(p * 2)
            elif k == "right":
                e = ease_out_back(p); x = int(x + 520 * (1 - e)); op = clamp01(p * 2)
            elif k == "slam":
                e = ease_out_back(p, 2.0); s = 1.0 + 0.7 * (1 - e)
                nw, nh = max(1, int(img.width * s)), max(1, int(img.height * s))
                cx, cy = x + img.width / 2, y + img.height / 2
                img = img.resize((nw, nh), Image.BICUBIC)
                x, y = int(cx - nw / 2), int(cy - nh / 2); op = clamp01(p * 3)
            elif k == "wipe":
                e = ease_out_cubic(p)
                hh = max(1, int(img.height * e))
                img = img.crop((0, 0, img.width, hh)); y = int(y + 18 * (1 - e)); op = clamp01(p * 2)
            elif k == "rise":
                e = ease_out_cubic(p); y = int(y + 40 * (1 - e)); op = e
            if op < 1:
                a = np.asarray(img, np.float32).copy(); a[..., 3] *= op
                img = Image.fromarray(a.astype(np.uint8), "RGBA")
            frame.paste(img, (x, y), img)
        # flash when the score lands
        ts = next((L["t1"] for L in layers if L["kind"] == "slam"), None)
        post = frame.convert("RGB")
        if ts and ts - 0.05 <= t <= ts + 0.25:
            k = 1 - abs(t - (ts + 0.05)) / 0.2
            arr = np.asarray(post, np.float32); arr = arr + (255 - arr) * 0.18 * clamp01(k)
            post = Image.fromarray(arr.astype(np.uint8))
        # slow push-in on the whole post
        z = 1.0 + 0.04 * (t / secs)
        pw, ph = int(W * z), int(H * z)
        post = post.resize((pw, ph), Image.BICUBIC).crop(((pw - W) // 2, (ph - H) // 2, (pw - W) // 2 + W, (ph - H) // 2 + H))
        # fade in from black
        if t < 0.4:
            arr = np.asarray(post, np.float32) * (t / 0.4); post = Image.fromarray(arr.astype(np.uint8))
        canvas = back.copy()
        canvas.paste(post, (0, top), feather)
        proc.stdin.write(canvas.tobytes())
    proc.stdin.close()
    proc.wait()
    print("wrote", out_p)


if __name__ == "__main__":
    main()
