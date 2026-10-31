#!/usr/bin/env python3
"""TNB animated goal breakdown (no match footage): a 9:16 Reel that redraws how a goal happened
on a tactics board, built from match reports. Fully original TNB content.

Usage:
  python3 src/tools/goal_anim.py out.mp4 --spec goal.json [--still out.jpg]

goal.json:
{
 "player": "Alphonso Davies", "cutout": "davies", "club_colour": "#DC052D",
 "minute": "35'", "comp": "Champions League", "match": "Bayern v Arsenal",
 "score_after": "1–1", "home": "Bayern", "away": "Arsenal", "final": "2–2",
 "assist": "Kane", "keeper": "Raya",
 "players": [                         # pitch coords: x 0-100 (left-right), y 0-100 (own half -> goal line)
   {"id":"assist","label":"KANE","x":52,"y":58},
   {"id":"scorer","label":"DAVIES","x":12,"y":52},
   {"id":"gk","label":"RAYA","x":50,"y":95,"team":"opp"},
   {"id":"d1","label":"","x":38,"y":78,"team":"opp"}, ...],
 "run":   [[12,52],[22,66],[34,80]],  # scorer's run
 "pass":  [[52,58],[33,79]],          # assist pass (from, to)
 "carry": [[33,79],[38,86]],          # optional touch/carry
 "shot":  [[38,86],[58,99.5]],        # finish (to a point on the goal line, goal spans x 44-56)
 "beats": ["Kane drops deep and looks up", "Davies bursts from the left", "Through ball splits the line", "Tucked past Raya"],
 "credit": "Photo: Bryan Berlin / Wikimedia Commons (CC BY-SA 4.0)",
 "source_note": "Illustration based on match reports"
}
"""
import argparse, json, pathlib, shutil, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
FONTS = ROOT / 'site' / 'fonts'

PITCH = dict(x=60, y=560, w=960, h=980)   # pitch box on the 1080x1920 canvas (attacking upwards)
Y0 = 45


def px(x, y):
    """pitch % -> canvas px. y=100 is the goal line at the TOP of the board."""
    # the board shows the attacking final ~55% of the pitch (y 45 -> 100), zoomed in
    yy = (y - Y0) / (100 - Y0)
    return PITCH['x'] + PITCH['w'] * x / 100, PITCH['y'] + PITCH['h'] * (1 - yy)


def path_d(pts):
    p = [px(*q) for q in pts]
    return 'M' + ' L'.join(f'{a:.1f} {b:.1f}' for a, b in p)


def build_html(s, still=False):
    goal_l, goal_r = px(44, 100)[0], px(56, 100)[0]
    gy = px(0, 100)[1]
    fx, fy = PITCH['x'], PITCH['y']; W, H = PITCH['w'], PITCH['h']
    box_l, box_r = px(21, 100)[0], px(79, 100)[0]; box_b = px(0, 84)[1]
    six_l, six_r = px(37, 100)[0], px(63, 100)[0]; six_b = px(0, 94.5)[1]
    spot = px(50, 89)
    arc_r = W * 0.1
    dots = ''
    for p in s['players']:
        x, y = px(p['x'], p['y'])
        opp = p.get('team') == 'opp'
        role = p['id']
        cls = 'opp' if opp else ('scorer' if role == 'scorer' else 'mate')
        dots += f'<g class="pl {cls} pl-{role}" style="transform:translate({x:.1f}px,{y:.1f}px)"><circle r="{24 if role=="scorer" else 20}"/>' \
                f'<text y="-34">{p.get("label","")}</text></g>'
    run_d, pass_d, shot_d = path_d(s['run']), path_d(s['pass']), path_d(s['shot'])
    carry_d = path_d(s['carry']) if s.get('carry') else ''
    first, _, last = s['player'].partition(' ')
    beats = s['beats']
    beat_html = ''.join(f'<div class="beat b{i}"><b>{i+1}</b>{t}</div>' for i, t in enumerate(beats))
    end_x, end_y = px(*s['run'][-1])
    run_len = 1600
    anim = '' if still else 'anim'
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Tanker;src:url({(FONTS/'tanker/Tanker-Regular.woff2').as_uri()})}}
@font-face{{font-family:Switzer;src:url({(FONTS/'switzer/Switzer-Bold.woff2').as_uri()});font-weight:700}}
@font-face{{font-family:Switzer;src:url({(FONTS/'switzer/Switzer-Semibold.woff2').as_uri()});font-weight:600}}
:root{{--club:{s['club_colour']};--gold:#f0c255;--red:#d40f1f}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#060607;font-family:Switzer;color:#fff}}
.bg{{position:absolute;inset:0;background:radial-gradient(900px 900px at 70% 30%,color-mix(in srgb,var(--club) 55%,transparent),transparent 70%),linear-gradient(180deg,#151517,#060607)}}
.stripe{{position:absolute;width:140px;height:3000px;background:linear-gradient(180deg,var(--red),#8a0712);transform:rotate(28deg);top:-700px;left:930px;opacity:.85}}
/* hook: player + score on frame 0 */
.hero{{position:absolute;right:-40px;top:40px;width:620px;z-index:2;filter:drop-shadow(-6px 0 0 color-mix(in srgb,var(--club) 70%,white 10%)) drop-shadow(0 30px 60px rgba(0,0,0,.7));
 -webkit-mask-image:linear-gradient(180deg,#000 55%,transparent 88%)}}
.hero img{{width:100%;display:block}}
.head{{position:absolute;left:56px;top:150px;z-index:5;width:620px}}
.k{{font-weight:700;font-size:24px;letter-spacing:.3em;color:var(--gold)}}
.nm{{font-family:Tanker;font-size:140px;line-height:.84;text-transform:uppercase;margin-top:10px;text-shadow:0 10px 40px rgba(0,0,0,.85)}}
.nm span{{display:block;color:transparent;-webkit-text-stroke:2.5px #fff}}
.vs{{margin-top:16px;display:inline-flex;align-items:center;gap:16px;background:rgba(0,0,0,.6);border:2px solid var(--gold);border-radius:14px;padding:10px 18px}}
.vs .sc{{font-family:Tanker;font-size:56px;line-height:1}}
.vs .t{{font-weight:700;font-size:22px;letter-spacing:.14em;text-transform:uppercase}}
/* board */
svg{{position:absolute;inset:0;z-index:4}}
.turf{{fill:rgba(255,255,255,.035);stroke:rgba(255,255,255,.55);stroke-width:3}}
.ln{{fill:none;stroke:rgba(255,255,255,.55);stroke-width:3}}
.goal{{fill:rgba(255,255,255,.12);stroke:#fff;stroke-width:4}}
.pl circle{{stroke-width:4}}
.pl text{{font-family:Switzer;font-weight:700;font-size:26px;letter-spacing:.12em;text-anchor:middle;fill:#fff;paint-order:stroke;stroke:#000;stroke-width:6px}}
.mate circle{{fill:var(--club);stroke:#fff}}
.scorer circle{{fill:var(--gold);stroke:#fff}}
.scorer text{{fill:var(--gold)}}
.opp circle{{fill:#2a2a2e;stroke:#9a9a9a}}
.run{{fill:none;stroke:var(--gold);stroke-width:6;stroke-dasharray:14 12;stroke-linecap:round}}
.pass{{fill:none;stroke:#fff;stroke-width:6;stroke-linecap:round}}
.carry{{fill:none;stroke:var(--gold);stroke-width:5;stroke-dasharray:4 10;stroke-linecap:round}}
.shot{{fill:none;stroke:var(--red);stroke-width:9;stroke-linecap:round}}
.ball{{fill:#fff;stroke:#000;stroke-width:3}}
.goalfx{{font-family:Tanker;font-size:190px;fill:#fff;text-anchor:middle;paint-order:stroke;stroke:var(--red);stroke-width:14px}}
.beats{{position:absolute;left:56px;right:56px;bottom:150px;z-index:6;height:120px}}
.beat{{position:absolute;left:0;right:0;bottom:0;background:rgba(8,8,9,.9);border-left:8px solid var(--red);padding:22px 26px;font-weight:700;font-size:36px;opacity:0;display:flex;gap:18px;align-items:center}}
.beat b{{font-family:Tanker;font-weight:normal;font-size:52px;color:var(--gold)}}
.foot{{position:absolute;left:44px;right:44px;bottom:70px;display:flex;justify-content:space-between;z-index:6;border-top:2px solid rgba(240,194,85,.7);padding-top:14px}}
.foot .c{{font-size:17px;font-weight:600;color:#9d9d9d}} .foot .r{{font-weight:700;font-size:21px;letter-spacing:.24em}}
/* timeline (10 s) */
@keyframes draw{{from{{stroke-dashoffset:var(--len)}}to{{stroke-dashoffset:0}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes out{{from{{opacity:1}}to{{opacity:0}}}}
@keyframes pop{{0%{{transform:scale(2.2);opacity:0}}60%{{transform:scale(.92);opacity:1}}100%{{transform:scale(1);opacity:1}}}}
@keyframes punch{{0%{{transform:scale(1.12)}}100%{{transform:scale(1)}}}}
@keyframes shrink{{to{{transform:translate(120px,-30px) scale(.62);opacity:.9}}}}
@keyframes moveScorer{{to{{transform:translate({end_x:.1f}px,{end_y:.1f}px)}}}}
.anim .hero{{animation:punch .7s ease-out 0s both, shrink .8s ease-in-out 1.4s both;transform-origin:100% 0}}
.anim .head{{animation:out .4s 1.6s forwards}}
.anim .board{{animation:fade .5s 1.6s both}}
.anim .run{{stroke-dasharray:{run_len};--len:{run_len};animation:draw 1.3s ease-in-out 2.8s both}}
.anim .pl-scorer{{animation:moveScorer 1.3s ease-in-out 2.8s both}}
.anim .pass{{stroke-dasharray:1200;--len:1200;animation:draw .7s ease-out 3.6s both}}
.anim .carry{{stroke-dasharray:600;--len:600;animation:draw .5s ease-out 4.6s both}}
.anim .shot{{stroke-dasharray:800;--len:800;animation:draw .35s ease-in 5.6s both}}
.anim .goalfx{{animation:pop .5s ease-out 6.0s both;transform-box:fill-box;transform-origin:center}}
.anim .b0{{animation:fade .3s 1.9s both, out .3s 3.4s forwards}}
.anim .b1{{animation:fade .3s 3.4s both, out .3s 4.4s forwards}}
.anim .b2{{animation:fade .3s 4.4s both, out .3s 5.6s forwards}}
.anim .b3{{animation:fade .3s 5.6s both}}
body:not(.anim) .goalfx,body:not(.anim) .beat:not(.b3){{opacity:0}}
body:not(.anim) .b3{{opacity:1}} body:not(.anim) .head{{opacity:0}}
body:not(.anim) .hero{{transform:translate(120px,-30px) scale(.62);transform-origin:100% 0}}
body:not(.anim) .pl-scorer{{transform:translate({end_x:.1f}px,{end_y:.1f}px)!important}}
</style></head><body class="{anim}">
<div class="bg"></div><div class="stripe"></div>
<div class="hero"><img src="player.png"></div>
<div class="head"><div class="k">⚽ GOAL {s['minute']} · {s['comp'].upper()}</div>
<div class="nm"><span>{first}</span>{last}</div>
<div class="vs"><span class="t">{s['home']}</span><span class="sc">{s['score_after']}</span><span class="t">{s['away']}</span></div></div>
<svg class="board" width="1080" height="1920">
 <rect class="turf" x="{fx}" y="{fy}" width="{W}" height="{H}" rx="10"/>
 <path class="ln" d="M{fx+W/2-90:.0f} {box_b:.0f} A90 90 0 0 0 {fx+W/2+90:.0f} {box_b:.0f}"/>
 <rect class="ln" x="{box_l:.0f}" y="{gy:.0f}" width="{box_r-box_l:.0f}" height="{box_b-gy:.0f}"/>
 <rect class="ln" x="{six_l:.0f}" y="{gy:.0f}" width="{six_r-six_l:.0f}" height="{six_b-gy:.0f}"/>
 <circle cx="{spot[0]:.0f}" cy="{spot[1]:.0f}" r="5" fill="rgba(255,255,255,.6)"/>
 <rect class="goal" x="{goal_l:.0f}" y="{gy-34:.0f}" width="{goal_r-goal_l:.0f}" height="34"/>
 <path class="run" d="{run_d}"/>
 <path class="pass" d="{pass_d}"/>
 {f'<path class="carry" d="{carry_d}"/>' if carry_d else ''}
 <path class="shot" d="{shot_d}"/>
 {dots}
 <text class="goalfx" x="540" y="{fy+H-90:.0f}">GOAL</text>
</svg>
<div class="beats">{beat_html}</div>
<div class="foot"><span class="c">{s['source_note']} · 📸 {s['credit']}</span><span class="r">TNBALLERS.COM</span></div>
</body></html>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('--spec', required=True); ap.add_argument('--still')
    ap.add_argument('--secs', type=float, default=9)
    a = ap.parse_args()
    s = json.loads(pathlib.Path(a.spec).read_text(encoding='utf-8'))
    t = pathlib.Path(tempfile.mkdtemp())
    cut = ROOT / 'src/assets/cutouts/hero' / f"{s['cutout']}.png"
    shutil.copy(cut, t / 'player.png')
    # the scorer starts at the run's first point; the CSS animation moves it to the last
    for p in s['players']:
        if p['id'] == 'scorer':
            p['x'], p['y'] = s['run'][0]
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        if a.still:
            (t / 's.html').write_text(build_html(s, still=True), encoding='utf-8')
            pg.goto((t / 's.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
            pg.screenshot(path=str(t / 's.png'))
            from PIL import Image; Image.open(t / 's.png').convert('RGB').save(a.still, quality=95)
        (t / 'a.html').write_text(build_html(s), encoding='utf-8')
        pg.goto((t / 'a.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        fr = t / 'fr'; fr.mkdir(); fps = 30
        for i in range(int(fps * a.secs)):
            pg.evaluate(f'document.getAnimations().forEach(x=>{{x.pause();x.currentTime={i*1000/fps}}})')
            pg.screenshot(path=str(fr / f'{i:04d}.jpg'), type='jpeg', quality=92)
        b.close()
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', '30', '-i', str(fr / '%04d.jpg'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', a.out], check=True)
    shutil.rmtree(t); print('wrote', a.out)


if __name__ == '__main__':
    main()
