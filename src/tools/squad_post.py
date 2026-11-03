#!/usr/bin/env python3
"""Canada squad announcement poster (feed 1080x1350 still + 1080x1920 animated Reel)."""
import pathlib, subprocess, sys, tempfile, shutil
ROOT = pathlib.Path(__file__).resolve().parents[2]
CUT = ROOT / 'src/assets/cutouts/hero'
FONTS = (ROOT / 'site/fonts').as_uri()
SQUAD = [
    ('GK', ['CRÉPEAU', 'GOODMAN', 'ST. CLAIR']),
    ('DEF', ['CHUKWU', 'DAVIES', 'DE FOUGEROLLES', 'IVANISEVIC', 'LARYEA', 'PRISO', 'SIGUR', 'WATERMAN']),
    ('MID', ['BUCHANAN', 'CHOINIÈRE', 'KHAN', 'MILLAR', 'OSORIO', 'SALIBA', 'SHAFFELBURG']),
    ('FWD', ['J. DAVID', 'P. DAVID', 'JEBBISON', 'OLUWASEYI', 'RUSSELL-ROWE']),
]


def page(W, H, reel):
    top = 170 if reel else 60          # header start
    stage_top = 430 if reel else 285   # top of the faces
    face_h = 960 if reel else 660      # Davies height
    list_top = 1330 if reel else 905
    u = lambda s: (CUT / f'{s}.png').as_uri()
    cols = ''.join(
        f'<div class="col" style="animation-delay:{2.0 + i*0.15:.2f}s"><div class="pos">{p}</div>' +
        ''.join(f'<div class="nm{" hi" if n in ("DAVIES",) else ""}">{n}</div>' for n in names) + '</div>'
        for i, (p, names) in enumerate(SQUAD))
    # faces: (slug, x-centre, height factor, z, delay, darken)
    faces = [('buchanan', 145, .66, 1, .55, .55), ('oluwaseyi', 935, .66, 1, .65, .55),
             ('j_david', 300, .80, 2, .40, .8), ('millar', 780, .80, 2, .48, .8),
             ('davies', 540, 1.0, 3, .15, 1)]
    fh = ''
    for s, x, k, z, d, b in faces:
        h = int(face_h * k); y = stage_top + (face_h - h) * 0.35
        fh += (f'<img class="f" src="{u(s)}" style="height:{h}px;left:{x}px;top:{y:.0f}px;z-index:{z};'
               f'filter:brightness({b}) drop-shadow(0 25px 40px #000);animation-delay:{d}s">')
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:Tanker;src:url({FONTS}/tanker/Tanker-Regular.woff2)}}
@font-face{{font-family:Switzer;src:url({FONTS}/switzer/Switzer-Semibold.woff2);font-weight:600}}
@font-face{{font-family:Switzer;src:url({FONTS}/switzer/Switzer-Bold.woff2);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:#07070a;font-family:Switzer;color:#fff;position:relative}}
.bg{{position:absolute;inset:0;background:radial-gradient(ellipse 80% 55% at 50% {stage_top+260}px,#c4061d 0%,#5a0310 38%,#120306 70%,#07070a 100%)}}
.beam{{position:absolute;top:-200px;width:260px;height:{H}px;background:linear-gradient(#ffffff26,transparent 70%);filter:blur(30px);transform-origin:top center}}
.b1{{left:180px;transform:rotate(18deg)}} .b2{{left:440px;transform:rotate(0deg);opacity:.8}} .b3{{left:700px;transform:rotate(-18deg)}}
.slab{{position:absolute;left:-15%;width:130%;height:150px;background:#e30a24;transform:rotate(-9deg);opacity:.9;mix-blend-mode:screen}}
.slab.s1{{top:{stage_top+420}px}} .slab.s2{{top:{stage_top+560}px;height:26px;background:#f4c542;opacity:.85;mix-blend-mode:normal}}
.ghost{{position:absolute;left:0;right:0;top:{stage_top-40}px;text-align:center;font-family:Tanker;font-size:330px;line-height:1;color:transparent;-webkit-text-stroke:3px #ffffff22;letter-spacing:-4px}}
.grain{{position:absolute;inset:0;opacity:.22;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}}
.f{{position:absolute;transform:translateX(-50%);-webkit-mask-image:linear-gradient(#000 58%,transparent 90%),linear-gradient(to right,transparent 0%,#000 14%,#000 86%,transparent 100%);-webkit-mask-composite:source-in;mask-composite:intersect;animation:up .7s cubic-bezier(.2,.9,.2,1) both}}
.shade{{position:absolute;left:0;right:0;top:{list_top-260}px;bottom:0;z-index:5;background:linear-gradient(transparent,#07070aee 45%,#07070a)}}
.hd{{position:absolute;top:{top}px;left:0;right:0;text-align:center;z-index:6}}
.kick{{display:inline-block;font-weight:700;letter-spacing:.2em;font-size:21px;color:#f4c542;border:2px solid #f4c54288;padding:8px 18px;animation:fd .5s .1s both}}
.t{{font-family:Tanker;font-size:{150 if reel else 132}px;line-height:.9;margin-top:16px;text-shadow:0 12px 40px #000;animation:slam .55s .2s cubic-bezier(.2,1.4,.4,1) both}}
.t span{{color:#e30a24;-webkit-text-stroke:0}}
.vs em{{font-style:normal;color:#f4c542}} .vs{{font-family:Tanker;font-size:{58 if reel else 50}px;letter-spacing:.04em;margin-top:6px;animation:fd .5s .45s both}}
.stk{{position:absolute;z-index:7;left:{560}px;top:{stage_top+face_h*0.10:.0f}px;background:#f4c542;color:#0b0b10;font-family:Tanker;font-size:56px;line-height:1;padding:12px 20px 6px;transform:rotate(-7deg);box-shadow:0 12px 30px #000a;animation:pop .5s 1.3s cubic-bezier(.2,1.6,.4,1) both;white-space:nowrap}}
.stk small{{display:block;font-family:Switzer;font-weight:700;font-size:17px;letter-spacing:.14em;margin-top:2px}}
.list{{position:absolute;z-index:6;left:44px;right:44px;top:{list_top}px;display:grid;grid-template-columns:.8fr 1.25fr 1.15fr 1.1fr;gap:18px}}
.col{{border-top:4px solid #e30a24;padding-top:10px;animation:rise .5s both}}
.pos{{font-family:Tanker;font-size:34px;color:#f4c542;margin-bottom:6px}}
.nm{{font-weight:700;font-size:{22 if reel else 19}px;line-height:1.42;letter-spacing:.02em;color:#ededf0;white-space:nowrap}}
.nm.hi{{color:#f4c542}}
.out{{position:absolute;z-index:6;left:44px;right:44px;top:{list_top + (345 if reel else 292)}px;display:flex;align-items:center;gap:16px;animation:rise .5s 2.8s both}}
.out b{{background:#e30a24;font-family:Tanker;font-size:34px;padding:8px 14px 2px;line-height:1}}
.out span{{font-weight:700;font-size:{24 if reel else 21}px;letter-spacing:.04em}}
.out i{{font-style:normal;color:#a9a9b3;font-weight:600}}
.fx{{position:absolute;z-index:6;left:44px;right:44px;top:{list_top + (410 if reel else 350)}px;display:flex;justify-content:space-between;font-family:Tanker;font-size:{34 if reel else 30}px;color:#fff;animation:rise .5s 3.0s both}}
.fx em{{font-style:normal;color:#f4c542}}
.foot{{position:absolute;z-index:6;bottom:{70 if reel else 26}px;left:44px;right:44px;display:flex;justify-content:space-between;align-items:center;font-size:15px;color:#8d8d97;font-weight:600;letter-spacing:.05em}}
.foot img{{width:38px;height:40px;object-fit:contain;vertical-align:middle;margin-left:10px}}
@keyframes up{{from{{transform:translate(-50%,120px);opacity:0}}}}
@keyframes slam{{from{{transform:scale(2.2);opacity:0}}}} @keyframes pop{{from{{transform:rotate(-7deg) scale(0);opacity:0}}}}
@keyframes fd{{from{{opacity:0}}}} @keyframes rise{{from{{transform:translateY(40px);opacity:0}}}}
</style></head><body>
<div class="bg"></div><div class="beam b1"></div><div class="beam b2"></div><div class="beam b3"></div>
<div class="ghost">CANADA</div><div class="slab s1"></div><div class="slab s2"></div>
{fh}
<div class="shade"></div><div class="grain"></div>
<div class="hd"><div class="kick">CONCACAF NATIONS LEAGUE · QUARTER-FINAL</div>
<div class="t">CANADA'S <span>23</span></div><div class="vs">v GUATEMALA · <em>13 &amp; 16 NOV</em></div></div>
<div class="stk">HE'S BACK<small>ALPHONSO DAVIES</small></div>
<div class="list">{cols}</div>
<div class="out"><b>OUT</b><span>EUSTÁQUIO <i>(groin)</i> · LARIN <i>(hamstring)</i></span></div>
<div class="foot"><span>Photos: Bryan Berlin / Wikimedia Commons (CC BY-SA 4.0)</span><span>TNBALLERS.COM<img src="{(ROOT/'src/assets/badge200.png').as_uri()}"></span></div>
</body></html>"""


def main(out_jpg, out_mp4=None, secs=8):
    from playwright.sync_api import sync_playwright
    from PIL import Image
    tmp = pathlib.Path(tempfile.mkdtemp())
    with sync_playwright() as p:
        b = p.chromium.launch()
        for W, H, reel in ((1080, 1350, False), (1080, 1920, True)):
            if reel and not out_mp4: break
            if not reel and out_jpg == "-": continue
            (tmp / 'p.html').write_text(page(W, H, reel), encoding='utf-8')
            pg = b.new_page(viewport={'width': W, 'height': H})
            pg.goto((tmp / 'p.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(600)
            if not reel:
                pg.evaluate('document.getAnimations().forEach(a=>{a.pause();a.currentTime=5000})')
                pg.screenshot(path=str(tmp / 'c.png')); Image.open(tmp / 'c.png').convert('RGB').save(out_jpg, quality=95)
                print('wrote', out_jpg)
            else:
                fr = tmp / 'f'; fr.mkdir(); fps = 30
                for i in range(fps * secs):
                    t = i * 1000 / fps
                    # slow push on the whole frame after the build-up
                    pg.evaluate(f'document.getAnimations().forEach(a=>{{a.pause();a.currentTime={t}}});'
                                f'document.body.style.transform="scale({1 + max(0, t-3500)/1000*0.006:.4f})"')
                    pg.screenshot(path=str(fr / f'{i:04d}.jpg'), type='jpeg', quality=92)
                pg.screenshot(path=str(tmp / 'cover.png'))
                Image.open(tmp / 'cover.png').convert('RGB').save(str(pathlib.Path(out_mp4).with_suffix('.cover.jpg')), quality=95)
                subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(fps), '-i', str(fr / '%04d.jpg'),
                                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', out_mp4], check=True)
                print('wrote', out_mp4)
            pg.close()
        b.close()
    shutil.rmtree(tmp)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
