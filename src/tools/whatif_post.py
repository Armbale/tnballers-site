#!/usr/bin/env python3
"""WHAT IF concept post: a star's real (licensed) photo + real stats + a Canadian club's real numbers.
Never edit a player into a kit he never wore; the real photo plus a clear "WHAT IF" banner keeps it an honest concept.

python3 src/tools/whatif_post.py out.jpg --reel out.mp4 --player ronaldo --line1 "RONALDO" --line2 "PLAYED FOR TFC?" \
  --colour "#B81137" --left-k "RONALDO 2025-26" --left-v "28" --left-s "Saudi Pro League goals · champions" \
  --right-k "TORONTO FC 2026" --right-v "51" --right-s "goals in 33 games · 12th in the East" \
  --hook "4 POINTS OFF THE PLAYOFFS" --credit "Bryan Berlin / Wikimedia Commons (CC BY-SA 4.0)"
"""
import argparse, pathlib, shutil, subprocess, tempfile, html

ROOT = pathlib.Path(__file__).resolve().parents[2]


def page(a, W, H):
    e = html.escape
    fonts = (ROOT / 'site/fonts').as_uri()
    face = ROOT / 'src/assets/cutouts/hero' / f'{a.player}.png'
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:Tanker;src:url({fonts}/tanker/Tanker-Regular.woff2)}}
@font-face{{font-family:Switzer;src:url({fonts}/switzer/Switzer-Semibold.woff2);font-weight:600}}
@font-face{{font-family:Switzer;src:url({fonts}/switzer/Switzer-Bold.woff2);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:#08080b;font-family:Switzer;color:#fff;position:relative}}
.bg{{position:absolute;inset:0;background:radial-gradient(ellipse at 70% 30%,{a.colour} 0%,#3a0612 45%,#08080b 80%);animation:fade .4s both}}
.stripe{{position:absolute;left:-10%;top:30%;width:120%;height:200px;background:{a.colour};opacity:.55;transform:rotate(-14deg);animation:wipe .6s .1s cubic-bezier(.2,.9,.2,1) both}}
.ghost{{position:absolute;top:150px;left:-20px;font-family:Tanker;font-size:430px;line-height:.8;color:#ffffff12;white-space:nowrap}}
.pl{{position:absolute;right:-60px;bottom:{int(H*.33)}px;height:{int(H*.52)}px;filter:drop-shadow(0 30px 50px #000);animation:slide .7s .15s cubic-bezier(.2,.9,.2,1) both, push 9s .8s linear both}}
.shade{{position:absolute;left:0;right:0;bottom:0;height:48%;background:linear-gradient(transparent,#08080bf2 30%,#08080b)}}
.top{{position:absolute;top:110px;left:60px}}
.wi{{display:inline-block;background:#f4c542;color:#0b0b10;font-family:Tanker;font-size:96px;line-height:1;padding:10px 26px 4px;transform:rotate(-3deg);animation:punch .5s .2s cubic-bezier(.2,1.5,.4,1) both}}
.l1{{font-family:Tanker;font-size:150px;line-height:.9;margin-top:30px;text-shadow:0 10px 30px #000;animation:rise .5s .45s both}}
.l2{{font-family:Tanker;font-size:96px;line-height:.95;color:#fff;text-shadow:0 10px 30px #000;animation:rise .5s .6s both;max-width:640px}}
.cards{{position:absolute;left:50px;right:50px;bottom:{int(H*.14)}px;display:flex;gap:26px}}
.c{{flex:1;background:#14141a;border-top:6px solid #f4c542;padding:26px 26px 30px}}
.c.r{{border-top-color:{a.colour}}}
.k{{font-weight:700;letter-spacing:.16em;font-size:22px;color:#cfcfd6}}
.v{{font-family:Tanker;font-size:150px;line-height:.95;margin-top:8px}}
.s{{font-weight:600;font-size:25px;color:#e6e6e6;line-height:1.25}}
.cL{{animation:rise .5s 1.0s both}} .cR{{animation:rise .5s 1.2s both}}
.hook{{position:absolute;bottom:{int(H*.075)}px;left:0;right:0;text-align:center;font-family:Tanker;font-size:64px;color:#f4c542;animation:punch .5s 1.6s cubic-bezier(.2,1.5,.4,1) both}}
.foot{{position:absolute;bottom:{int(H*.03)}px;left:50px;right:50px;display:flex;justify-content:space-between;font-size:19px;color:#9a9aa5;font-weight:600;letter-spacing:.06em}}
@keyframes fade{{from{{opacity:0}}}} @keyframes wipe{{from{{transform:rotate(-14deg) translateX(-100%)}}}}
@keyframes slide{{from{{transform:translateX(50%);opacity:0}}}} @keyframes push{{to{{scale:1.06}}}}
@keyframes punch{{from{{transform:scale(1.8) rotate(-3deg);opacity:0}}}} @keyframes rise{{from{{transform:translateY(40px);opacity:0}}}}
</style></head><body>
<div class="bg"></div><div class="stripe"></div><div class="ghost">{e(a.line1)}</div>
<img class="pl" src="{face.as_uri()}"><div class="shade"></div>
<div class="top"><div class="wi">{e(a.banner)}</div><div class="l1">{e(a.line1)}</div><div class="l2">{e(a.line2)}</div></div>
<div class="cards">
 <div class="c cL"><div class="k">{e(a.left_k)}</div><div class="v">{e(a.left_v)}</div><div class="s">{e(a.left_s)}</div></div>
 <div class="c r cR"><div class="k">{e(a.right_k)}</div><div class="v">{e(a.right_v)}</div><div class="s">{e(a.right_s)}</div></div>
</div>
<div class="hook">{e(a.hook)}</div>
<div class="foot"><span>{e(a.foot_label)}{e(a.credit)}</span><span>TNBALLERS.COM</span></div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('--reel'); ap.add_argument('--secs', type=int, default=7)
    for k in ('player', 'line1', 'line2', 'left-k', 'left-v', 'left-s', 'right-k', 'right-v', 'right-s', 'hook', 'credit'):
        ap.add_argument(f'--{k}', required=True)
    ap.add_argument('--colour', default='#B81137')
    ap.add_argument('--banner', default='WHAT IF')  # e.g. 'CALLED UP' for real news cards
    ap.add_argument('--foot-label', default='Fan concept · Photo: ')  # use 'Photo: ' for real news
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    from PIL import Image
    tmp = pathlib.Path(tempfile.mkdtemp()); W, H = 1080, 1920
    (tmp / 'p.html').write_text(page(a, W, H), encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
        pg.goto((tmp / 'p.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
        pg.evaluate('document.getAnimations().forEach(a=>{a.pause();a.currentTime=3000})')
        pg.screenshot(path=str(tmp / 'c.png')); Image.open(tmp / 'c.png').convert('RGB').save(a.out, quality=95); print('wrote', a.out)
        if a.reel:
            fr = tmp / 'f'; fr.mkdir(); fps = 30
            for i in range(fps * a.secs):
                pg.evaluate(f'document.getAnimations().forEach(a=>{{a.pause();a.currentTime={i*1000/fps}}})')
                pg.screenshot(path=str(fr / f'{i:04d}.jpg'), type='jpeg', quality=92)
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(fps), '-i', str(fr / '%04d.jpg'),
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', a.reel], check=True)
            print('wrote', a.reel)
        b.close()
    shutil.rmtree(tmp)


if __name__ == '__main__':
    main()
