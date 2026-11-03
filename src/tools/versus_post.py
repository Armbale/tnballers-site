#!/usr/bin/env python3
"""Two-player VERSUS matchday post (Canadian v Canadian), 1080x1920 Reel + cover JPG.

python3 src/tools/versus_post.py out.jpg --reel out.mp4 \
  --left davies --left-name "Davies" --left-club "Bayern" --left-colour "#DC052D" --left-status "STARTS" --left-stat "11 apps · 3 G · 3 A" \
  --right j_david --right-name "David" --right-club "Atlético" --right-colour "#272E61" --right-status "BENCH" --right-stat "6 LaLiga apps · 3 G · 2 A" \
  --kicker "CHAMPIONS LEAGUE · MATCHDAY 4" --title "CANADA v CANADA" --when "ATLÉTICO v BAYERN · TONIGHT 20:00 UK / 15:00 ET" \
  --credit "Bryan Berlin / Wikimedia Commons (CC BY-SA 4.0)"
Faces: src/assets/cutouts/hero/<slug>.png (see faces.json), partners site/players/<key>.png.
"""
import argparse, pathlib, shutil, subprocess, tempfile, html

ROOT = pathlib.Path(__file__).resolve().parents[2]


def face(slug):
    p = ROOT / 'src/assets/cutouts/hero' / f'{slug}.png'
    return p if p.exists() else ROOT / 'site/players' / f'{slug}.png'


def page(a, W, H):
    e = html.escape
    fonts = (ROOT / 'site/fonts').as_uri()
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:Tanker;src:url({fonts}/tanker/Tanker-Regular.woff2)}}
@font-face{{font-family:Switzer;src:url({fonts}/switzer/Switzer-Semibold.woff2);font-weight:600}}
@font-face{{font-family:Switzer;src:url({fonts}/switzer/Switzer-Bold.woff2);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:#07070a;font-family:Switzer;color:#fff;position:relative}}
.half{{position:absolute;top:0;bottom:0;width:60%}}
.hl{{left:0;background:linear-gradient(160deg,{a.left_colour} 0%,#0b0b10 78%);clip-path:polygon(0 0,100% 0,72% 100%,0 100%);animation:inL .5s cubic-bezier(.2,.9,.2,1) both}}
.hr{{right:0;background:linear-gradient(200deg,{a.right_colour} 0%,#0b0b10 78%);clip-path:polygon(28% 0,100% 0,100% 100%,0 100%);animation:inR .5s cubic-bezier(.2,.9,.2,1) both}}
.seam{{position:absolute;left:50%;top:17%;width:10px;height:90%;background:linear-gradient(#f4c542,#b8860b);transform:translateX(-50%) rotate(9.5deg);box-shadow:0 0 40px #f4c54299;animation:fade .3s .35s both}}
.beam{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%,#ffffff22,transparent 55%)}}
.ghost{{position:absolute;top:{int(H*.25)}px;font-family:Tanker;font-size:{int(W*.36)}px;line-height:.8;color:#ffffff10;white-space:nowrap}}
.gl{{left:-30px}} .gr{{right:-30px}}
.pl{{position:absolute;bottom:{int(H*.20)}px;height:{int(H*.56)}px;filter:drop-shadow(0 30px 40px #000c)}}
.pL{{left:-40px;animation:slideL .7s .15s cubic-bezier(.2,.9,.2,1) both, push 9s .8s linear both}}
.pR{{right:-40px;animation:slideR .7s .3s cubic-bezier(.2,.9,.2,1) both, push 9s .9s linear both}}
.shade{{position:absolute;left:0;right:0;bottom:0;height:46%;background:linear-gradient(transparent,#07070aee 45%,#07070a)}}
.top{{position:absolute;top:{int(H*.055)}px;left:0;right:0;text-align:center}}
.kick{{font-weight:700;letter-spacing:.32em;font-size:28px;color:#f4c542;animation:drop .5s .1s both}}
.title{{font-family:Tanker;font-size:150px;line-height:.95;margin-top:16px;letter-spacing:.01em;text-shadow:0 8px 30px #000;animation:punch .55s .25s cubic-bezier(.2,1.4,.4,1) both}}
.vs{{position:absolute;left:50%;top:{int(H*.47)}px;transform:translate(-50%,-50%);width:170px;height:170px;border-radius:50%;background:#0b0b10;border:6px solid #f4c542;display:flex;align-items:center;justify-content:center;font-family:Tanker;font-size:96px;color:#f4c542;box-shadow:0 0 60px #f4c54277;animation:slam .5s .75s cubic-bezier(.2,1.6,.4,1) both}}
.names{{position:absolute;bottom:{int(H*.13)}px;left:56px;right:56px;display:flex;justify-content:space-between}}
.n{{width:46%}} .n.r{{text-align:right}}
.nm{{font-family:Tanker;font-size:118px;line-height:.9}}
.club{{font-weight:700;letter-spacing:.2em;font-size:26px;color:#cfcfd6;margin-top:6px}}
.chip{{display:inline-block;margin-top:14px;padding:8px 16px;font-weight:700;font-size:24px;letter-spacing:.14em;background:#f4c542;color:#0b0b10}}
.chip.alt{{background:transparent;color:#fff;border:2px solid #ffffffaa}}
.stat{{font-weight:600;font-size:27px;margin-top:12px;color:#e6e6e6}}
.nL{{animation:rise .5s 1.0s both}} .nR{{animation:rise .5s 1.15s both}}
.when{{position:absolute;bottom:{int(H*.072)}px;left:0;right:0;text-align:center;font-weight:700;font-size:30px;letter-spacing:.08em;animation:rise .5s 1.35s both}}
.foot{{position:absolute;bottom:{int(H*.03)}px;left:56px;right:56px;display:flex;justify-content:space-between;font-size:19px;color:#9a9aa5;font-weight:600;letter-spacing:.06em}}
@keyframes inL{{from{{transform:translateX(-100%)}}}} @keyframes inR{{from{{transform:translateX(100%)}}}}
@keyframes slideL{{from{{transform:translateX(-60%);opacity:0}}}} @keyframes slideR{{from{{transform:translateX(60%);opacity:0}}}}
@keyframes push{{to{{scale:1.06}}}}
@keyframes fade{{from{{opacity:0}}}} @keyframes drop{{from{{transform:translateY(-40px);opacity:0}}}}
@keyframes punch{{from{{transform:scale(1.8);opacity:0}}}}
@keyframes slam{{from{{transform:translate(-50%,-50%) scale(3);opacity:0}}}}
@keyframes rise{{from{{transform:translateY(40px);opacity:0}}}}
</style></head><body>
<div class="half hl"></div><div class="half hr"></div><div class="beam"></div><div class="seam"></div>
<div class="ghost gl">{e(a.left_name.upper())}</div><div class="ghost gr">{e(a.right_name.upper())}</div>
<img class="pl pL" src="{face(a.left).as_uri()}"><img class="pl pR" src="{face(a.right).as_uri()}">
<div class="shade"></div>
<div class="top"><div class="kick">{e(a.kicker)}</div><div class="title">{e(a.title)}</div></div>
<div class="vs">V</div>
<div class="names">
 <div class="n nL"><div class="nm">{e(a.left_name.upper())}</div><div class="club">{e(a.left_club.upper())}</div><div class="chip">{e(a.left_status)}</div><div class="stat">{e(a.left_stat)}</div></div>
 <div class="n r nR"><div class="nm">{e(a.right_name.upper())}</div><div class="club">{e(a.right_club.upper())}</div><div class="chip alt">{e(a.right_status)}</div><div class="stat">{e(a.right_stat)}</div></div>
</div>
<div class="when">{e(a.when)}</div>
<div class="foot"><span>Photos: {e(a.credit)}</span><span>TNBALLERS.COM</span></div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    for s in ('left', 'right'):
        ap.add_argument(f'--{s}', required=True); ap.add_argument(f'--{s}-name', required=True)
        ap.add_argument(f'--{s}-club', required=True); ap.add_argument(f'--{s}-colour', default='#C8102E')
        ap.add_argument(f'--{s}-status', default=''); ap.add_argument(f'--{s}-stat', default='')
    ap.add_argument('--kicker', default=''); ap.add_argument('--title', default='CANADA v CANADA')
    ap.add_argument('--when', default=''); ap.add_argument('--credit', required=True)
    ap.add_argument('--reel'); ap.add_argument('--secs', type=int, default=7)
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    from PIL import Image
    tmp = pathlib.Path(tempfile.mkdtemp())
    W, H = 1080, 1920
    (tmp / 'p.html').write_text(page(a, W, H), encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
        pg.goto((tmp / 'p.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
        pg.evaluate('document.getAnimations().forEach(a=>{a.pause();a.currentTime=2500})')
        pg.screenshot(path=str(tmp / 'c.png'))
        Image.open(tmp / 'c.png').convert('RGB').save(a.out, quality=95); print('wrote', a.out)
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
