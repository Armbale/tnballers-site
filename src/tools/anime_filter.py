#!/usr/bin/env python3
"""Cel-shade / anime-style a photo or transparent cut-out (OpenCV only, no AI model).
   python3 src/tools/anime_filter.py in.(jpg|png) out.(jpg|png) [--colors 14] [--line 1.0] [--sat 1.35]
Steps: edge-preserving smoothing, k-means colour quantisation (flat cel tones), soft shadow banding,
ink outlines from a DoG edge map, saturation/contrast lift and a light bloom. Keeps the alpha channel."""
import argparse, cv2, numpy as np

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('inp'); ap.add_argument('out')
    ap.add_argument('--colors', type=int, default=14); ap.add_argument('--line', type=float, default=1.0)
    ap.add_argument("--sat", type=float, default=1.35); ap.add_argument("--keep", type=float, default=0.3); ap.add_argument('--max', type=int, default=1600)
    a = ap.parse_args()
    im = cv2.imread(a.inp, cv2.IMREAD_UNCHANGED)
    alpha = im[:, :, 3] if im.shape[2] == 4 else None
    bgr = im[:, :, :3]
    s = min(1.0, a.max / max(bgr.shape[:2]))
    if s < 1: bgr = cv2.resize(bgr, None, fx=s, fy=s, interpolation=cv2.INTER_AREA); alpha = None if alpha is None else cv2.resize(alpha, (bgr.shape[1], bgr.shape[0]))
    # 1. smooth while keeping edges
    sm = bgr.copy()
    for _ in range(3): sm = cv2.bilateralFilter(sm, 9, 40, 9)
    sm = cv2.edgePreservingFilter(sm, flags=1, sigma_s=40, sigma_r=0.35)
    # 2. quantise colours (cel tones) in Lab
    lab = cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    mask = (alpha.reshape(-1) > 20) if alpha is not None else np.ones(len(lab), bool)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    samp = lab[mask][:: max(1, mask.sum() // 60000)]
    _, _, C = cv2.kmeans(samp, a.colors, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    d = ((lab[:, None, :] - C[None, :, :]) ** 2).sum(-1); q = C[d.argmin(1)]
    # keep some original luminance detail so faces don't go flat-grey
    q[:, 0] = (1 - a.keep) * q[:, 0] + a.keep * lab[:, 0]
    cel = cv2.cvtColor(q.reshape(sm.shape).astype(np.uint8), cv2.COLOR_LAB2BGR)
    cel = cv2.medianBlur(cel, 5)
    # 3. saturation + contrast
    hsv = cv2.cvtColor(cel, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * a.sat, 0, 255); hsv[:, :, 2] = np.clip((hsv[:, :, 2] - 128) * 1.08 + 136, 0, 255)
    cel = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    # 4. ink lines (difference of Gaussians on the smoothed grey)
    g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY).astype(np.float32)
    dog = cv2.GaussianBlur(g, (0, 0), 1.0) - cv2.GaussianBlur(g, (0, 0), 1.8)
    ink = np.clip(1 - np.maximum(0, -dog) * 0.16 * a.line, 0, 1)
    ink = cv2.GaussianBlur(ink, (0, 0), 0.6)
    out = (cel.astype(np.float32) * ink[:, :, None])
    # 5. bloom
    hi = np.clip(out - 170, 0, 255); out = np.clip(out + cv2.GaussianBlur(hi, (0, 0), 12) * 0.6, 0, 255).astype(np.uint8)
    if alpha is not None:
        al = cv2.erode(alpha, np.ones((3, 3), np.uint8))
        # dark outline around the silhouette, like a cel drawing
        rim = cv2.dilate(al, np.ones((5, 5), np.uint8)) - al
        out[rim > 40] = (20, 14, 12); out = np.dstack([out, np.maximum(al, rim)])
    cv2.imwrite(a.out, out, [cv2.IMWRITE_JPEG_QUALITY, 93])
    print('wrote', a.out, out.shape)

if __name__ == '__main__': main()
