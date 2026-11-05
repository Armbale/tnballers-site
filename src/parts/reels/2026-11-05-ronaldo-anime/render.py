#!/usr/bin/env python3
"""Render anime.html (+ pre-rendered 3D frames in G3 dir) to MP4. Usage: render.py out.mp4 --g3 DIR [--frames 1,5.2]"""
import argparse, pathlib, subprocess, sys
from playwright.sync_api import sync_playwright
D = pathlib.Path(__file__).resolve().parent; ROOT = D.parents[3]
ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('--g3', required=True); ap.add_argument('--frames'); ap.add_argument('--secs', type=float, default=58.5)
a = ap.parse_args()
html = (D / 'anime.html').read_text().replace('FONTS/', (ROOT / 'site/fonts').as_uri() + '/').replace("'IMG/'", repr((D / 'img').as_uri() + '/')).replace("'G3F/'", repr(pathlib.Path(a.g3).resolve().as_uri() + '/'))
import json
vo = json.load(open(D / 'vo_timed.json')) if (D / 'vo_timed.json').exists() else []
html = html.replace('__VO__', json.dumps(vo))
(D / '_built.html').write_text(html)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--allow-file-access-from-files']); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('pageerror', lambda e: print('pageerror:', e))
    pg.goto((D / '_built.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
    if a.frames:
        for f in a.frames.split(','):
            pg.evaluate(f'renderAt({f})'); pg.wait_for_function('[...document.images].every(i=>i.complete)'); pg.screenshot(path=str(pathlib.Path(a.out).parent / f'prev_{f}.jpg'), type='jpeg', quality=82)
        b.close(); sys.exit()
    fps = 30; n = int(a.secs * fps); tmp = a.out + '.part.mp4'
    ff = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        pg.evaluate(f'renderAt({i / fps})'); pg.wait_for_function('[...document.images].every(i=>i.complete)', timeout=10000)
        ff.stdin.write(pg.screenshot(type='jpeg', quality=88))
        if i % 300 == 0: print('frame', i, '/', n, flush=True)
    ff.stdin.close(); ff.wait(); b.close(); pathlib.Path(tmp).rename(a.out); print('wrote', a.out)
