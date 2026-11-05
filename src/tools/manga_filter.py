#!/usr/bin/env python3
"""Manga-panel treatment for a photo or cut-out (OpenCV only): black ink shadows, halftone screentone
mid-tones, white highlights and DoG ink lines. Keeps alpha.  python3 src/tools/manga_filter.py in out [--dot 7]"""
import argparse, cv2, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('inp'); ap.add_argument('out'); ap.add_argument('--dot', type=int, default=7)
ap.add_argument('--lo', type=float, default=0.30); ap.add_argument('--hi', type=float, default=0.62); ap.add_argument('--max', type=int, default=1600)
a = ap.parse_args()
im = cv2.imread(a.inp, cv2.IMREAD_UNCHANGED); alpha = im[:, :, 3] if im.shape[2] == 4 else None; bgr = im[:, :, :3]
s = min(1.0, a.max / max(bgr.shape[:2]))
if s < 1:
    bgr = cv2.resize(bgr, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    if alpha is not None: alpha = cv2.resize(alpha, (bgr.shape[1], bgr.shape[0]))
g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
g = cv2.createCLAHE(2.0, (8, 8)).apply(g)
sm = cv2.bilateralFilter(g, 9, 30, 9).astype(np.float32) / 255
H, W = g.shape; yy, xx = np.mgrid[0:H, 0:W]
# rotated dot screen (45 degrees)
u = (xx + yy) / np.sqrt(2) / a.dot; v = (xx - yy) / np.sqrt(2) / a.dot
dots = (np.sin(u * np.pi) * np.sin(v * np.pi) + 1) / 2   # 0..1
mid = (sm - a.lo) / (a.hi - a.lo)
tone = np.where(sm < a.lo, 0.0, np.where(sm > a.hi, 1.0, (dots < mid).astype(np.float32) * 0.85 + 0.15 * mid))
dog = cv2.GaussianBlur(sm, (0, 0), 1.0) - cv2.GaussianBlur(sm, (0, 0), 2.0)
ink = np.clip(1 - np.maximum(0, -dog) * 14, 0, 1)
out = np.clip(tone * ink, 0, 1)
out = cv2.GaussianBlur(out, (0, 0), 0.5)
out = (out * 255).astype(np.uint8)
out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
if alpha is not None:
    al = cv2.erode(alpha, np.ones((3, 3), np.uint8)); rim = cv2.dilate(al, np.ones((7, 7), np.uint8)) - al
    out[rim > 40] = 0; out = np.dstack([out, np.maximum(al, rim)])
cv2.imwrite(a.out, out); print('wrote', a.out)
