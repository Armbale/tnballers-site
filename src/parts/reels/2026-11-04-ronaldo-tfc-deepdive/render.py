#!/usr/bin/env python3
"""Render reel.html (driven by timed.json) to MP4. Usage: render.py out.mp4 [--frames 1.0,5.2,...] [--from S --to E]"""
import json, pathlib, subprocess, sys, argparse
D = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path('/home/claude/tnballers-site')
ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('--frames'); ap.add_argument('--tail', type=float, default=2.0)
a = ap.parse_args()
S = json.load(open(D / 'timed.json'))
total = S[-1]['t1'] + a.tail
g3 = sorted((D / 'g3/frames').glob('*.jpg')) if (D / 'g3/frames').exists() else []
html = (D / 'reel.html').read_text(encoding='utf-8')
html = (html.replace('__SCRIPT__', json.dumps(S, ensure_ascii=False)).replace('__TOTAL__', f'{total:.3f}')
        .replace('__HAS3D__', str(len(g3)) if g3 else '0')
        .replace('FONTS/', (ROOT / 'site/fonts').as_uri() + '/').replace("'CUTS/'", repr((ROOT / 'src/assets/cutouts/hero').as_uri() + '/'))
        .replace('G3/', (D / 'g3/frames').as_uri() + '/'))
(D / 'built.html').write_text(html, encoding='utf-8')
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('pageerror', lambda e: print('pageerror:', e))
    pg.goto((D / 'built.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
    if a.frames:
        for f in a.frames.split(','):
            pg.evaluate(f'renderAt({f})'); pg.wait_for_timeout(120)
            pg.screenshot(path=str(D / f'prev_{f}.jpg'), type='jpeg', quality=85)
        print('previews done'); b.close(); sys.exit()
    fps = 30; n = int(total * fps)
    tmp = a.out + '.part.mp4'
    ff = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        pg.evaluate(f'renderAt({i / fps})')
        if g3 and i / fps < 10: pg.wait_for_function('[...document.images].every(i=>i.complete)', timeout=5000)
        ff.stdin.write(pg.screenshot(type='jpeg', quality=90))
        if i % 300 == 0: print('frame', i, '/', n, flush=True)
    ff.stdin.close(); ff.wait(); b.close()
    pathlib.Path(tmp).rename(a.out); print('wrote', a.out, total)
