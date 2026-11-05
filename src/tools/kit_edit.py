#!/usr/bin/env python3
"""Fan-concept kit edit: repaint a player's shirt (cut-out PNG with alpha) in a Canadian club's colours.

Keeps the photo's own folds and lighting (blurred luminance as a shade map), replaces the old
pattern, crest and sponsor with a flat new design, adds a collar/cuff trim, an optional front
wordmark + generic badge, or a back name + number. Always label the result as a fan concept.

  python3 src/tools/kit_edit.py in.png out.png --view front --wordmark TORONTO --number 7
  python3 src/tools/kit_edit.py in.png out.png --view back --name RONALDO --number 7
Debug: --debug writes <out>_mask.png.
"""
import argparse, pathlib
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parents[2]
TANKER = str(ROOT / 'site/fonts/tanker/Tanker-Regular.woff2')


def hexrgb(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255


def font(size):
    # PIL can't read woff2; Tanker ships as woff2 only, so fall back to a TTF copy if one exists.
    for f in [ROOT / 'src/assets/fonts/Tanker-Regular.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']:
        if pathlib.Path(f).exists():
            return ImageFont.truetype(str(f), size)
    return ImageFont.load_default()


def shirt_mask(rgb, alpha, y_max_frac, extra_exclude=None):
    hsv = cv2.cvtColor((rgb * 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    H, S, V = hsv[..., 0] * 2, hsv[..., 1] / 255, hsv[..., 2] / 255
    person = alpha > 0.5
    white = (S < 0.22) & (V > 0.52)
    teal = (H > 150) & (H < 199) & (S > 0.12) & (V > 0.25)
    skin = ((H < 45) | (H > 340)) & (S > 0.18) & (S < 0.75) & (V > 0.25)
    hair = V < 0.22
    # only big skin blobs (face, neck, arms) and hair above the shirt count: small red/dark marks
    # inside the shirt are the old crest, number and sponsor and must be painted over
    def big(mask, frac):
        n, lab, st, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8))
        out = np.zeros(mask.shape, bool)
        for i in range(1, n):
            if st[i, cv2.CC_STAT_AREA] > frac * mask.size:
                out |= lab == i
        return out
    skin = big(skin & person, 0.004)
    hair = big(hair & person, 0.004)
    m = (white | teal) & person & ~skin
    h = m.shape[0]
    m[int(h * y_max_frac):] = False
    m = m.astype(np.uint8)
    # close holes left by the old crest, number and sponsor, but never eat skin
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    mc = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
    # fill enclosed holes
    ff = mc.copy(); hh, ww = ff.shape; fm = np.zeros((hh + 2, ww + 2), np.uint8)
    cv2.floodFill(ff, fm, (0, 0), 1)
    holes = (ff == 0)
    mc = (mc.astype(bool) | holes) & person & ~skin & ~hair
    if extra_exclude is not None:
        mc &= ~extra_exclude
    mc = cv2.morphologyEx(mc.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    # keep big components only
    n, lab, st, _ = cv2.connectedComponentsWithStats(mc)
    keep = np.zeros_like(mc, bool)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 0.01 * mc.size:
            keep |= lab == i
    return keep, skin & person


def text_layer(size, items):
    """items: list of (text, cx, cy, height_px, fill, stroke, stroke_w). Rendered in the browser with the
    self-hosted Tanker woff2 (PIL can't read woff2 and the FFL bans converting it). Returns RGBA float array."""
    from playwright.sync_api import sync_playwright
    import io
    css = lambda c: f'rgba({c[0]},{c[1]},{c[2]},{c[3] / 255:.3f})'
    spans = ''
    for txt, cx, cy, hpx, fill, stroke, sw in items:
        st = f'-webkit-text-stroke:{sw * 1.5}px {css(stroke)};paint-order:stroke fill;' if stroke and sw else ''
        spans += (f'<div style="position:absolute;left:{cx}px;top:{cy}px;transform:translate(-50%,-50%);'
                  f'font-family:Tanker;font-size:{hpx * 1.32:.0f}px;line-height:1;letter-spacing:.02em;white-space:nowrap;color:{css(fill)};{st}">{txt}</div>')
    html = (f'<!doctype html><html><head><style>@font-face{{font-family:Tanker;src:url({(ROOT / "site/fonts/tanker/Tanker-Regular.woff2").as_uri()})}}'
            f'html,body{{margin:0;background:transparent}}</style></head><body><div style="position:relative;width:{size[0]}px;height:{size[1]}px">{spans}</div></body></html>')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': size[0], 'height': size[1]})
        import tempfile
        tf = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False); tf.write(html); tf.close()
        pg.goto(pathlib.Path(tf.name).as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
        png = pg.screenshot(omit_background=True); b.close()
    return np.asarray(Image.open(io.BytesIO(png)).convert('RGBA')).astype(np.float32) / 255


def badge_layer(size, cx, cy, s, red, trim):
    im = Image.new('RGBA', size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w, h = s, s * 1.18
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h * .1), (cx, cy + h / 2), (cx - w / 2, cy + h * .1)]
    d.polygon(pts, fill=tuple(int(c * 255) for c in trim) + (255,))
    inner = [(x * .78 + cx * .22, y * .78 + cy * .22) for x, y in pts]
    d.polygon(inner, fill=tuple(int(c * 255) for c in red) + (255,))
    # simple maple-leaf-ish star mark (generic, not a club crest)
    r = s * .2; star = []
    for i in range(10):
        a = -np.pi / 2 + i * np.pi / 5; rr = r if i % 2 == 0 else r * .45
        star.append((cx + rr * np.cos(a), cy - s * .05 + rr * np.sin(a)))
    d.polygon(star, fill=(255, 255, 255, 255))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(.6))).astype(np.float32) / 255


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('inp'); ap.add_argument('out')
    ap.add_argument('--view', choices=['front', 'back'], default='front')
    ap.add_argument('--colour', default='#C8102E'); ap.add_argument('--trim', default='#1B2A3A')
    ap.add_argument('--wordmark', default=''); ap.add_argument('--name', default=''); ap.add_argument('--number', default='')
    ap.add_argument('--ymax', type=float, default=1.0, help='ignore shirt pixels below this fraction of the height (shorts)')
    ap.add_argument('--chest', type=float, default=0.33, help='wordmark centre as a fraction down the shirt box')
    ap.add_argument('--badge', type=float, default=1.0)
    ap.add_argument('--hoops', type=float, default=0.055, help='tonal hoop strength (0 = plain shirt)')
    ap.add_argument('--texture', type=float, default=0.0, help='knit texture strength, e.g. 0.04')
    ap.add_argument('--blur', type=float, default=0.018, help='shade blur as a fraction of the width (bigger hides more of the old print)')
    ap.add_argument('--contrast', type=float, default=1.7, help='fold shading exponent (higher = deeper folds)')
    ap.add_argument('--debug', action='store_true')
    a = ap.parse_args()

    im = Image.open(a.inp).convert('RGBA'); arr = np.asarray(im).astype(np.float32) / 255
    rgb, al = arr[..., :3], arr[..., 3]
    m, skin = shirt_mask(rgb, al, a.ymax)
    ys, xs = np.where(m); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    # neck centre: skin pixels just above the shirt top
    sk = np.where(skin[max(0, y0 - 40):y0 + 120, x0:x1])
    ncx = int(np.median(sk[1]) + x0) if len(sk[1]) else (x0 + x1) // 2

    # shade map from the photo: blurred luminance keeps folds, drops the old pattern
    L = (0.3 * rgb[..., 0] + 0.59 * rgb[..., 1] + 0.11 * rgb[..., 2])
    # flatten the old print: scale each colour class (white / teal / dark marks) to the white level
    hsv = cv2.cvtColor((rgb * 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    Sx = hsv[..., 1] / 255
    wht = m & (Sx < 0.2)
    lw = np.median(L[wht]) if wht.any() else 0.8
    for cls in [m & (Sx >= 0.2), m & (L < 0.35)]:
        if cls.sum() > 50:
            L = np.where(cls, np.clip(L * lw / max(np.median(L[cls]), 1e-3), 0, 1), L)
    sig = max(6, a.blur * m.shape[1])
    Lm = np.where(m, L, 0); W = cv2.GaussianBlur(m.astype(np.float32), (0, 0), sig) + 1e-4
    Lb = cv2.GaussianBlur(Lm, (0, 0), sig) / W
    ref = np.percentile(Lb[m], 85)
    shade = np.clip(Lb / ref, 0.25, 1.15)
    shade = 0.18 + 0.82 * shade ** a.contrast  # compress so red never goes black
    red, trim = hexrgb(a.colour), hexrgb(a.trim)

    # base colour + subtle tonal diagonal pinstripes
    yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
    # tonal hoops: slightly darker bands, like a modern home shirt
    band = (np.sin(yy / (0.045 * m.shape[0]) * np.pi) > 0.55).astype(np.float32)
    band = cv2.GaussianBlur(band, (0, 0), 1.5) * a.hoops
    base = red[None, None, :] * (1 - band[..., None])
    if a.texture > 0:  # fine knit: tiny diagonal mesh + noise so the shirt doesn't look like plastic
        rng = np.random.default_rng(1)
        knit = (np.sin((xx + yy) * 1.9) * np.sin((xx - yy) * 1.9)) * 0.5 + rng.standard_normal(m.shape) * 0.5
        knit = cv2.GaussianBlur(knit.astype(np.float32), (0, 0), 0.6)
        base = base * (1 + a.texture * knit[..., None])
    # collar + cuff trim: shirt pixels that touch skin
    sk_d = cv2.dilate(skin.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(0.035 * (x1 - x0)) | 1,) * 2)).astype(bool)
    trimz = m & sk_d
    base = np.where(trimz[..., None], trim[None, None, :], base)

    # decorations (flat, then shaded with the same map so they sit in the cloth)
    deco = np.zeros(arr.shape, np.float32)
    sw = x1 - x0
    items = []
    if a.view == 'front':
        cy = int(y0 + a.chest * (y1 - y0))
        if a.wordmark:
            items.append((a.wordmark, ncx, cy, int(sw * 0.075), (255, 255, 255, 240), (int(trim[0] * 255), int(trim[1] * 255), int(trim[2] * 255), 255), 2))
        if a.number:
            items.append((a.number, ncx, cy + int(sw * 0.15), int(sw * 0.11), (255, 255, 255, 235), (int(trim[0] * 255), int(trim[1] * 255), int(trim[2] * 255), 255), 3))
    else:
        cy = int(y0 + 0.17 * (y1 - y0))
        if a.name:
            items.append((a.name, ncx, cy, int(sw * 0.075), (255, 255, 255, 245), None, 0))
        if a.number:
            items.append((a.number, ncx, cy + int(sw * 0.27), int(sw * 0.34), (255, 255, 255, 245), (int(trim[0] * 255), int(trim[1] * 255), int(trim[2] * 255), 255), 6))
    if items:
        deco = text_layer(im.size, items)
    if a.view == 'front' and a.badge > 0:
        bx = int(ncx + sw * 0.17); by = int(y0 + (a.chest - 0.13) * (y1 - y0))
        b = badge_layer(im.size, bx, by, sw * 0.085 * a.badge, red, np.array([.82, .82, .85]))
        deco = deco * (1 - b[..., 3:]) + b * b[..., 3:]
        deco[..., 3] = np.maximum(deco[..., 3], b[..., 3])
    da = deco[..., 3:] * m[..., None]
    col = base * (1 - da) + deco[..., :3] * da
    out_rgb = col * shade[..., None]
    # specular sheen from the original highlights
    hi = np.clip((L - Lb) * 1.0, 0, 0.15)[..., None] * wht[..., None]
    out_rgb = np.clip(out_rgb + hi * 0.25, 0, 1)
    # feather the mask edge
    mf = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.2)[..., None]
    res = rgb * (1 - mf) + out_rgb * mf
    out = np.dstack([res, al])
    Image.fromarray((out * 255).astype(np.uint8)).save(a.out)
    if a.debug:
        Image.fromarray((m * 255).astype(np.uint8)).save(a.out.replace('.png', '_mask.png'))
    print('wrote', a.out, 'shirt box', (x0, y0, x1, y1))


if __name__ == '__main__':
    main()
