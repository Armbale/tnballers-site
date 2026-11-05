#!/usr/bin/env python3
"""Render anime3d.html for one MODE to JPEG frames. Usage: render3d.py freekick|header outdir [--frames 1,2.5] [--fps 30]"""
import argparse, functools, http.server, pathlib, shutil, socketserver, tempfile, threading
from playwright.sync_api import sync_playwright
D = pathlib.Path(__file__).resolve().parent; ROOT = D.parents[3]
ap = argparse.ArgumentParser(); ap.add_argument('mode'); ap.add_argument('out'); ap.add_argument('--frames'); ap.add_argument('--fps', type=int, default=30)
a = ap.parse_args()
t = pathlib.Path(tempfile.mkdtemp()); shutil.copytree(ROOT / 'src/vendor/three', t / 'three'); shutil.copytree(ROOT / 'src/vendor/models', t / 'models')
(t / 'index.html').write_text((D / 'anime3d.html').read_text().replace('%%MODE%%', a.mode))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(t)); H.log_message = lambda *x: None
srv = socketserver.TCPServer(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('pageerror', lambda e: print('pageerror:', e)); pg.on('console', lambda m: m.type == 'error' and print('console:', m.text))
    pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/index.html'); pg.wait_for_function('window.ready===true', timeout=120000)
    total = pg.evaluate('window.TOTAL'); n = int(total * a.fps)
    want = [float(x) for x in a.frames.split(',')] if a.frames else None
    for i in range(n):
        tt = i / a.fps; pg.evaluate(f'renderAt({tt})')   # every frame, so the ball trail history stays right
        if want is None: pg.screenshot(path=str(out / f'{i + 1:04d}.jpg'), type='jpeg', quality=88)
        elif any(abs(tt - w) < .5 / a.fps for w in want): pg.screenshot(path=str(out / f'prev_{tt:.2f}.jpg'), type='jpeg', quality=85)
        if want and tt > max(want): break
        if i % 60 == 0: print(a.mode, i, '/', n, flush=True)
    b.close()
shutil.rmtree(t); print('done', a.mode, n)
