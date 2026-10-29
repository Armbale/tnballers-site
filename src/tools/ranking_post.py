#!/usr/bin/env python3
"""Render the "Canada's Best Right Now" Instagram post (1080x1350 JPG).

Reads the top 5 of BEST in src/parts/make_canada.py, the photo credits in
site/img/people/_results.json and the cut-outs in src/assets/cutouts/<slug>.png
(made from the same Wikimedia photos; missing ones are cut out with rembg).
Design: src/parts/post_ranking.html (Tanker + Switzer, self-hosted fonts).

Usage:
  python3 src/tools/ranking_post.py out.jpg \
      --hero-line "Goal and assist off the bench vs Magdeburg." \
      --moves '{"Alphonso Davies": 1, "Liam Millar": -1}' \
      --stat "Tani Oluwaseyi=2 UCL|+1 COPA" --stat "Stephen Eustáquio=1G 1A|CHAMP."

--moves: places gained (+) or lost (-) since the last ranking post; a player
         missing from the dict shows "–", "new" shows NEW.
--stat:  override a card's stat line "Name=LEFT|RIGHT" (default "<g>G <a>A" and
         the competition, or "<apps> GAMES" for all comps).
Needs: playwright (pre-installed), Pillow; rembg only for new cut-outs.
"""
import argparse, datetime, html, importlib.util, json, pathlib, shutil, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1].parent
PARTS, SITE = ROOT / 'src' / 'parts', ROOT / 'site'
CUTS = ROOT / 'src' / 'assets' / 'cutouts'


def load_best():
    spec = importlib.util.spec_from_file_location('make_canada', PARTS / 'make_canada.py')
    mc = importlib.util.module_from_spec(spec); spec.loader.exec_module(mc)
    return mc.BEST


def photos():
    data = json.loads((SITE / 'img' / 'people' / '_results.json').read_text(encoding='utf-8'))
    return {r['display']: dict(slug=s, **r) for s, r in data.items() if r.get('ok')}


def cutout(slug, src):
    out = CUTS / f'{slug}.png'
    if not out.exists():
        try:
            from rembg import remove, new_session
        except ImportError:
            sys.exit('rembg missing: pip install --break-system-packages "rembg[cpu]"')
        from PIL import Image
        im = remove(Image.open(src), session=new_session('isnet-general-use'))
        im = im.resize((640, round(im.height * 640 / im.width)), Image.LANCZOS)
        CUTS.mkdir(parents=True, exist_ok=True); im.save(out, optimize=True)
        print('new cut-out:', out, '(check it before posting)')
    return out


def e(s): return html.escape(str(s))


def two_lines(name):
    first, _, rest = name.partition(' ')
    return f'{e(first)}<br>{e(rest)}' if rest else e(name)


def move_html(m, hero=False):
    if m == 'new': return '<b>NEW</b>' if hero else '<div class="mv">NEW</div>'
    if not m: return '' if hero else '<div class="mv">–</div>'
    arrow = '▲' if m > 0 else '▼'
    if hero: return f'<b>{arrow}{abs(m)}</b>'
    return f'<div class="mv{"" if m > 0 else " dn"}">{arrow}{abs(m)}</div>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--hero-line', default='')
    ap.add_argument('--moves', default='{}')
    ap.add_argument('--stat', action='append', default=[])
    ap.add_argument('--date', default=datetime.date.today().strftime('%-d %b %Y').upper())
    a = ap.parse_args()
    moves = json.loads(a.moves)
    stats = {k: v.split('|', 1) for k, v in (s.split('=', 1) for s in a.stat)}

    best, ph = load_best()[:5], photos()
    if len(best) < 5: sys.exit('BEST needs 5 players')
    tmp = pathlib.Path(tempfile.mkdtemp())
    credits = []
    for row in best:
        p = ph.get(row[0])
        if not p: sys.exit(f'No photo for {row[0]} in _results.json: run fetch_people_photos.py')
        shutil.copy(cutout(p['slug'], SITE / 'img' / 'people' / p['file']), tmp / f"{p['slug']}.png")
        c = f"{p['author'].split('/')[0].strip()} / Wikimedia Commons, {p['licence']}"
        if c not in credits: credits.append(c)
    shutil.copy(SITE / 'players' / 'badge.png', tmp / 'badge.png')

    def club(r): return r[2].split(' (')[0]

    def stat(r):
        if r[0] in stats: return stats[r[0]]
        return [f'{r[5]}G {r[6]}A', f'{r[4]} GAMES' if r[3] == 'All comps' else r[3].upper()]

    h = best[0]
    m0 = moves.get(h[0])
    badge = ('New No. 1 ' if m0 else 'No. 1 ') + move_html(m0, hero=True)
    extra = ' · Captain' if h[10].startswith('Captain') else ''
    body = [
        '<div class="post"><div class="stripe"></div><div class="stripe thin"></div>',
        f'<div class="hero-img"><img src="{ph[h[0]]["slug"]}.png"></div>',
        f'<div class="kicker"><i></i>TNB RANKING · {e(a.date)}</div>',
        '<div class="title">Canada\'s best<span class="out">right now</span></div>',
        f'<div class="hero-txt"><div class="badge">{badge}</div>',
        f'<div class="hero-name">{two_lines(h[0])}</div>',
        f'<div class="hero-club">{e(club(h))}{extra}</div>',
        f'<div class="hero-line">{e(a.hero_line)}</div>' if a.hero_line else '',
        '<div class="chips">',
        f'<div class="chip hot"><div class="n">{h[5]}</div><div class="l">GOALS</div></div>',
        f'<div class="chip hot"><div class="n">{h[6]}</div><div class="l">ASSISTS</div></div>',
        f'<div class="chip"><div class="n">{h[4]}</div><div class="l">GAMES</div></div>',
        '</div></div><div class="grid">']
    for i, r in enumerate(best[1:], start=2):
        s1, s2 = stat(r)
        body.append(
            f'<div class="card"><div class="glow"></div><div class="num">{i}</div>{move_html(moves.get(r[0]))}'
            f'<div class="ph"><img src="{ph[r[0]]["slug"]}.png" style="top:-10px"></div>'
            f'<div class="info"><div class="nm">{two_lines(r[0])}</div><div class="cl">{e(club(r))}</div>'
            f'<div class="st"><span class="a">{e(s1)}</span><span class="b">{e(s2)}</span></div></div></div>')
    body.append(f'</div><div class="foot"><span class="c">📸 {e(" · ".join(credits))}</span>'
                '<span class="r">TNBALLERS.COM <img src="badge.png"></span></div><div class="grain"></div></div>')

    tpl = (PARTS / 'post_ranking.html').read_text(encoding='utf-8')
    page = tpl.replace('%%FONTS%%', (SITE / 'fonts').as_uri()).replace('%%BODY%%', '\n'.join(body))
    (tmp / 'index.html').write_text(page, encoding='utf-8')

    from playwright.sync_api import sync_playwright
    from PIL import Image
    png = tmp / 'post.png'
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
        pg.goto((tmp / 'index.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
        pg.screenshot(path=str(png)); b.close()
    Image.open(png).convert('RGB').save(a.out, quality=95)
    shutil.rmtree(tmp)
    print('wrote', a.out, '| credit:', ' · '.join(credits))


if __name__ == '__main__':
    main()
