#!/usr/bin/env python3
"""Render an animated HTML scene file (CSS animations only) to a 1080x1920 MP4 Reel + a cover JPG.

python3 src/tools/render_reel.py src/parts/reels/<slug>.html out.mp4 --secs 40 --cover-ms 2500 --cover out.jpg
In the HTML, use %%ROOT%% for the repo root (file URI) so fonts/cut-outs resolve. Every animation must be a
CSS animation/transition (the renderer pauses them all and seeks frame by frame), so the output is deterministic.
"""
import argparse, pathlib, shutil, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html'); ap.add_argument('out')
    ap.add_argument('--secs', type=float, required=True); ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--cover'); ap.add_argument('--cover-ms', type=int, default=2500)
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    tmp = pathlib.Path(tempfile.mkdtemp())
    src = pathlib.Path(a.html).read_text(encoding='utf-8').replace('%%ROOT%%', ROOT.as_uri())
    (tmp / 'p.html').write_text(src, encoding='utf-8')
    fr = tmp / 'f'; fr.mkdir()
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto((tmp / 'p.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(600)
        seek = 'ms=>document.getAnimations().forEach(x=>{x.pause();x.currentTime=ms})'
        if a.cover:
            pg.evaluate(seek, a.cover_ms); pg.screenshot(path=a.cover, type='jpeg', quality=95)
        n = int(a.secs * a.fps)
        for i in range(n):
            pg.evaluate(seek, i * 1000 / a.fps)
            pg.screenshot(path=str(fr / f'{i:05d}.jpg'), type='jpeg', quality=90)
        b.close()
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(a.fps), '-i', str(fr / '%05d.jpg'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-movflags', '+faststart', a.out], check=True)
    shutil.rmtree(tmp); print('wrote', a.out)


if __name__ == '__main__':
    main()
