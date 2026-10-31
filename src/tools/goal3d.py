#!/usr/bin/env python3
"""Render a TNB 3D goal recreation Reel (1080x1920, ~10 s) from a JSON spec, no match footage.

  python3 src/tools/goal3d.py spec.json out.mp4 [--still out.jpg --still-at 6.1] [--three path/to/three.min.js]

The scene is src/parts/goal3d.html (Three.js r160, vendored at src/vendor/three.min.js): night stadium, stylised
players, ball with trail, camera cuts (broadcast, behind the passer, follow cam, behind the goal in slow motion,
orbit replay, aerial), net ripple, GOAL slam and an end card. Spec example: src/assets/goal_specs/*-3d.json.
Positions are on a 0-100 pitch (x left->right, y own goal -> attacking goal) and come from match reports
(shot location from FotMob's shot map when available); label the Reel "Recreation based on match reports".
"""
import argparse, functools, http.server, json, pathlib, shutil, socketserver, subprocess, tempfile, threading

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('spec'); ap.add_argument('out')
    ap.add_argument('--still'); ap.add_argument('--still-at', type=float, default=6.2)
    ap.add_argument('--three', default=str(ROOT / 'src/vendor/three.min.js'))
    ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--frames', help='comma list of seconds: render only these stills (preview), e.g. 2,4.1,5.2')
    a = ap.parse_args()
    s = json.loads(pathlib.Path(a.spec).read_text(encoding='utf-8'))
    t = pathlib.Path(tempfile.mkdtemp())
    shutil.copytree(ROOT / 'src/vendor/three', t / 'three'); shutil.copytree(ROOT / 'src/vendor/models', t / 'models')
    shutil.copy(ROOT / 'src/assets/cutouts/hero' / f"{s['cutout']}.png", t / 'player.png')
    html = (ROOT / 'src/parts/goal3d.html').read_text(encoding='utf-8')
    shutil.copytree(ROOT / 'site/fonts', t / 'fonts'); html = html.replace('%%FONTS%%', 'fonts').replace('%%CLUB%%', s['club_colour']).replace('%%SPEC%%', json.dumps(s))
    (t / 'index.html').write_text(html, encoding='utf-8')
    secs = s['timeline']['total']
    # ES modules + GLB need http:// (file:// blocks module scripts): serve the temp dir locally
    H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(t))
    H.log_message = lambda *x: None
    srv = socketserver.TCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{port}/index.html'
    from playwright.sync_api import sync_playwright
    fr = t / 'fr'; fr.mkdir()
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist', '--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.on('console', lambda m: m.type in ('error','warning') and print('page:', m.text)); pg.on('pageerror', lambda e: print('pageerror:', e))
        pg.goto(url); pg.wait_for_function('window.ready===true', timeout=120000); pg.evaluate('document.fonts.ready')
        if a.frames:
            want = [float(x) for x in a.frames.split(',')]
            outs = []
            for i in range(int(max(want) * a.fps) + 1):
                tt = i / a.fps; pg.evaluate(f'renderAt({tt})')
                for w in want:
                    if abs(tt - w) < 0.5 / a.fps:
                        o = pathlib.Path(a.out).with_name(f'{pathlib.Path(a.out).stem}_{w}.jpg'); pg.screenshot(path=str(o), type='jpeg', quality=90); outs.append(str(o))
            b.close(); shutil.rmtree(t); print('previews', outs); return
        n = int(secs * a.fps)
        for i in range(n):
            tt = i / a.fps
            pg.evaluate(f'renderAt({tt})')
            pg.screenshot(path=str(fr / f'{i:04d}.jpg'), type='jpeg', quality=90)
            if a.still and abs(tt - a.still_at) < 0.5 / a.fps:
                shutil.copy(fr / f'{i:04d}.jpg', a.still)
        b.close()
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(a.fps), '-i', str(fr / '%04d.jpg'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', a.out], check=True)
    shutil.rmtree(t); print('wrote', a.out)


if __name__ == '__main__':
    main()
