#!/usr/bin/env python3
"""Render a TNB "player hero" result post: the Canadian player dominates the graphic.

Writes a 1080x1350 JPG (feed) and, with --reel, an animated 1080x1920 MP4 (8 s):
surname slides in, the player rises in, name, scoreboard, score pop, scorers, context.

Usage:
  python3 src/tools/hero_post.py out.jpg --player millar --name "Liam Millar" \
      --club-colour "#1C3E94" --home "Lincoln" --away "Birmingham" --score "1-3" \
      --home-colour "#D71920" --away-colour "#1C3E94" \
      --home-scorers "Bayliss 63'" --away-scorers "Priske 16', 60'|Cochrane 73'" \
      --comp "Championship · Matchday 13" --tag "Started · Away win" \
      --context "Birmingham win at Lincoln." --credit "Bryan Berlin / Wikimedia Commons (CC BY-SA 4.0)" \
      [--side away] [--reel out.mp4]

--player: a cut-out PNG path, or a slug in src/assets/cutouts/hero/<slug>.png (800 px, rembg)
          falling back to src/assets/cutouts/<slug>.png, then site/players/<slug>.png (partners).
--side:   which team the player plays for (home|away); the other team's name is dimmed if it lost.
Scorer lists use "|" between lines. Fonts: self-hosted Tanker + Switzer.
"""
import argparse, html, pathlib, shutil, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
PARTS, SITE = ROOT / 'src' / 'parts', ROOT / 'site'


def e(s): return html.escape(str(s))


def find_cutout(p):
    q = pathlib.Path(p)
    if q.suffix and q.exists(): return q
    for c in (ROOT / 'src/assets/cutouts/hero' / f'{p}.png', ROOT / 'src/assets/cutouts' / f'{p}.png', SITE / 'players' / f'{p}.png'):
        if c.exists(): return c
    raise SystemExit(f'no cut-out for {p}')


def build(a, tmp, anim, vw, vh):
    from PIL import Image
    cut = find_cutout(a.player)
    shutil.copy(cut, tmp / 'player.png'); shutil.copy(SITE / 'players' / 'badge.png', tmp / 'badge.png')
    w, h = Image.open(cut).size
    pw = a.player_width
    ph = pw * h / w
    px = 1080 - pw + a.player_shift
    py = max(70, 1350 - 120 - ph) if ph < 1200 else 110
    first, _, last = a.name.partition(' ')
    hs, as_ = (int(x) for x in a.score.replace('–', '-').split('-'))
    dim_h = 'dim' if hs < as_ else ''
    dim_a = 'dim' if as_ < hs else ''
    surname = last or first
    ghost = max(150, min(330, int(1700 / max(len(surname), 1))))
    namesize = 160 if max(len(first), len(last)) <= 7 else 120 if max(len(first), len(last)) <= 9 else 100
    lines = lambda s: '<br>'.join(e(x.strip()) for x in s.split('|') if x.strip())
    nsc = max(len([x for x in a.home_scorers.split('|') if x.strip()]), len([x for x in a.away_scorers.split('|') if x.strip()]), 1)
    body = f'''<div class="post{' reel' if vh > 1350 else ''}">
<div class="beams"></div><div class="dots"></div>
<div class="stripe"></div><div class="stripe thin"></div>
<div class="ghost">{e(surname)}</div><div class="ghost2">{e(surname)}</div>
<div class="echo"><img src="player.png"></div>
<div class="player"><img src="player.png"></div>
<div class="kicker"><i></i>{e(a.comp)}</div>
<div class="ft">{e(a.badge)}</div>
<div class="who"><div class="flag">🇨🇦 {e(a.flag)}</div>
<div class="name"><span class="f">{e(first)}</span><span class="l">{e(last)}</span></div>
{f'<div class="tag">{e(a.tag)}</div>' if a.tag else ''}</div>
<div class="board">
<div class="plate"></div><div class="score">{hs}–{as_}</div>
<div class="team h {dim_h}">{e(a.home)}<i></i></div><div class="team a {dim_a}">{e(a.away)}<i></i></div>
<div class="sc h">{lines(a.home_scorers)}</div><div class="sc a">{lines(a.away_scorers)}</div>
<div class="ctx" style="top:calc(var(--rowTop) + {max(252, 160 + 33*nsc + 22)}px)">{e(a.context)}</div>
</div>
<div class="foot"><span class="c">📸 {e(a.credit)}</span><span class="r">TNBALLERS.COM <img src="badge.png"></span></div>
<div class="vig"></div><div class="grain"></div><div class="flashl"></div></div>'''
    rep = {'%%FONTS%%': (SITE / 'fonts').as_uri(), '%%BODY%%': body, '%%CLUB%%': a.club_colour, '%%HOMEC%%': a.home_colour,
           '%%AWAYC%%': a.away_colour, '%%VH%%': str(vh), '%%GHOSTSIZE%%': str(ghost), '%%PX%%': f'{px:.0f}',
           '%%PW%%': f'{pw:.0f}', '%%NAMESIZE%%': str(namesize), '%%ANIM%%': 'anim' if anim else ''}
    page = (PARTS / 'post_hero.html').read_text(encoding='utf-8')
    for k, v in rep.items(): page = page.replace(k, v)
    (tmp / 'index.html').write_text(page, encoding='utf-8')
    return tmp / 'index.html'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('--player', required=True); ap.add_argument('--name', required=True)
    ap.add_argument('--flag', default='Canada'); ap.add_argument('--club-colour', default='#d40f1f')
    ap.add_argument('--home', required=True); ap.add_argument('--away', required=True); ap.add_argument('--score', required=True)
    ap.add_argument('--home-colour', default='#ffffff'); ap.add_argument('--away-colour', default='#ffffff')
    ap.add_argument('--home-scorers', default=''); ap.add_argument('--away-scorers', default='')
    ap.add_argument('--comp', required=True); ap.add_argument('--tag', default=''); ap.add_argument('--context', default=''); ap.add_argument('--badge', default='FULL TIME')
    ap.add_argument('--credit', required=True); ap.add_argument('--reel')
    ap.add_argument('--player-width', type=float, default=720); ap.add_argument('--player-shift', type=float, default=60)
    ap.add_argument('--who-top', type=int, default=330)
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    from PIL import Image
    tmp = pathlib.Path(tempfile.mkdtemp())
    with sync_playwright() as p:
        b = p.chromium.launch()
        page_file = build(a, tmp, False, 1080, 1350)
        pg = b.new_page(viewport={'width': 1080, 'height': 1350})
        pg.goto(page_file.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
        pg.screenshot(path=str(tmp / 'post.png'))
        Image.open(tmp / 'post.png').convert('RGB').save(a.out, quality=95)
        print('wrote', a.out)
        if a.reel:
            fr = tmp / 'frames'; fr.mkdir()
            page_file = build(a, tmp, True, 1080, 1920)
            pg = b.new_page(viewport={'width': 1080, 'height': 1920})
            pg.goto(page_file.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
            fps, secs = 30, 8
            for i in range(fps * secs):
                t = i * 1000 / fps
                pg.evaluate(f'document.getAnimations().forEach(a=>{{a.pause();a.currentTime={t}}})')
                pg.screenshot(path=str(fr / f'{i:04d}.jpg'), type='jpeg', quality=92)
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(fps), '-i', str(fr / '%04d.jpg'),
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', a.reel], check=True)
            print('wrote', a.reel)
        b.close()
    shutil.rmtree(tmp)


if __name__ == '__main__':
    main()
