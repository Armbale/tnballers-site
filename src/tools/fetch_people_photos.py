#!/usr/bin/env python3
"""
Download Wikimedia-licensed photos for TNB people (Canada's Best + sidelined + legends).

Rules:
  - Only free commercial-use licences: CC BY, CC BY-SA, CC0, Public Domain.
  - Resize to <= 800 px wide, save as JPG, quality 82.
  - Record author + licence + file-page URL in CREDITS.md.
  - If a licence isn't allowed, skip (we keep the placeholder) and list in CREDITS.md.
"""
import json, re, sys, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image
import io

UA = 'tnballers-photo-fetcher/1.0 (https://tnballers.com)'

# slug -> (search title on en.wikipedia.org, display name)
PEOPLE = {
    'millar':         ('Liam Millar',           'Liam Millar'),
    'davies':         ('Alphonso Davies',       'Alphonso Davies'),
    'j_david':        ('Jonathan David',        'Jonathan David'),
    'oluwaseyi':      ('Tani Oluwaseyi',        'Tani Oluwaseyi'),
    'eustaquio':      ('Stephen Eustáquio',     'Stephen Eustáquio'),
    'buchanan':       ('Tajon Buchanan',        'Tajon Buchanan'),
    'larin':          ('Cyle Larin',            'Cyle Larin'),
    'saliba':         ('Nathan Saliba',         'Nathan Saliba'),
    'kone':           ('Ismaël Koné',           'Ismaël Koné'),
    'johnston':       ('Alistair Johnston',     'Alistair Johnston'),
    'bombito':        ('Moïse Bombito',         'Moïse Bombito'),
    'ahmed':          ('Ali Ahmed (soccer)',    'Ali Ahmed'),
    'cornelius':      ('Derek Cornelius',       'Derek Cornelius'),
    'p_david':        ('Promise David',         'Promise David'),
    'muller':         ('Thomas Müller',         'Thomas Müller'),
    'sanchez':        ('Alexis Sánchez',        'Alexis Sánchez'),
    'giovinco':       ('Sebastian Giovinco',    'Sebastian Giovinco'),
    'drogba':         ('Didier Drogba',         'Didier Drogba'),
    'henry':          ('Thierry Henry',         'Thierry Henry'),
    'nesta':          ('Alessandro Nesta',      'Alessandro Nesta'),
    'insigne':        ('Lorenzo Insigne',       'Lorenzo Insigne'),
    # Legends slider (display = the name used on the homepage slide)
    'ronaldo':        ('Cristiano Ronaldo',     'Cristiano Ronaldo'),
    'messi':          ('Lionel Messi',          'Lionel Messi'),
    'ronaldinho':     ('Ronaldinho',            'Ronaldinho'),
    'rooney':         ('Wayne Rooney',          'Wayne Rooney'),
    'maradona':       ('Diego Maradona',        'Diego Maradona'),
    'platini':        ('Michel Platini',        'Michel Platini'),
    'pele':           ('Pelé',                  'Pelé, Cruyff, Beckenbauer'),
    'aguero':         ('Sergio Agüero',         'Agüero, Di María, Suárez, Piqué'),
    # Canada's women
    'o_smith':        ('Olivia Smith (soccer)', 'Olivia Smith'),
    'fleming':        ('Jessie Fleming',        'Jessie Fleming'),
    'sonis':          ('Janine Sonis',          'Janine Sonis'),
    'lawrence':       ('Ashley Lawrence',       'Ashley Lawrence'),
    'k_buchanan':     ('Kadeisha Buchanan',     'Kadeisha Buchanan'),
    'rose':           ('Jade Rose',             'Jade Rose'),
    'defilippo':      ('Jessica De Filippo',    'Jessica De Filippo'),
    'hunter':         ('Kaylee Hunter',         'Kaylee Hunter'),
    'pridham':        ('Delaney Baie Pridham',  'Delaney Baie Pridham'),
    'alidou':         ('Marie-Yasmine Alidou',  'Marie-Yasmine Alidou'),
    'viens':          ('Évelyne Viens',         'Evelyne Viens'),
    'sheridan':       ('Kailen Sheridan',       'Kailen Sheridan'),
}
ONLY = set(sys.argv[1:])  # optional: only fetch these slugs and keep the rest

ALLOWED = ('cc-by-sa', 'cc by-sa', 'cc-by', 'cc by', 'cc0', 'cc-pd', 'public domain', 'pd', 'attribution')
BANNED  = ('getty', 'imago', 'shutter', 'reuters', 'ap ', 'associated press')
OUT = Path('site/img/people'); OUT.mkdir(parents=True, exist_ok=True)

def http(url, tries=10):
    import time, urllib.error
    for i in range(tries):
        try:
            r = urllib.request.Request(url, headers={'User-Agent': UA})
            return urllib.request.urlopen(r, timeout=25)
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == tries - 1: raise
            time.sleep(int(e.headers.get('retry-after') or 10) + 2 + i * 3)

import time
def jget(url):
    time.sleep(0.6)
    with http(url) as r: return json.load(r)

def resolve_wiki(title):
    """Follow redirects, return canonical title + the Commons filename of the page image (if any)."""
    url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode({
        'action':'query','format':'json','titles':title,
        'prop':'pageimages','piprop':'original|name','redirects':1,
    })
    d = jget(url)
    pages = d.get('query',{}).get('pages',{})
    for pid, p in pages.items():
        if pid == '-1': return None, None
        name = p.get('title', title)
        orig = p.get('original', {}).get('source')
        img = p.get('pageimage')
        return (name, img) if (orig and img) else (name, None)
    return title, None

def search_title(q):
    url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode({
        'action':'query','format':'json','list':'search','srsearch':q + ' soccer','srlimit':1})
    hits = jget(url).get('query',{}).get('search',[])
    return hits[0]['title'] if hits else None

def commons_info(filename):
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({
        'action':'query','format':'json','titles':'File:'+filename,
        'prop':'imageinfo','iiprop':'url|user|extmetadata','iiurlwidth':960,
    })
    d = jget(url)
    pages = d.get('query',{}).get('pages',{})
    for pid, p in pages.items():
        ii = (p.get('imageinfo') or [{}])[0]
        return ii
    return {}

def strip_html(s):
    s = re.sub(r'<[^>]+>', ' ', s or '')
    return re.sub(r'\s+', ' ', s).strip()

def resize(src_bytes, out_path, max_w=800):
    im = Image.open(io.BytesIO(src_bytes))
    if im.mode in ('RGBA','P','LA'):
        bg = Image.new('RGB', im.size, (11,11,11))
        if im.mode == 'P': im = im.convert('RGBA')
        bg.paste(im, mask=im.split()[-1] if im.mode in ('RGBA','LA') else None)
        im = bg
    elif im.mode != 'RGB':
        im = im.convert('RGB')
    if im.width > max_w:
        h = round(im.height * max_w / im.width)
        im = im.resize((max_w, h), Image.LANCZOS)
    im.save(out_path, 'JPEG', quality=82, optimize=True, progressive=True)
    return im.size

def pick(info):
    md = info.get('extmetadata') or {}
    lic_s = (md.get('LicenseShortName',{}).get('value','') or '').lower()
    lic_url = md.get('LicenseUrl',{}).get('value','') or ''
    author  = strip_html(md.get('Artist',{}).get('value',''))
    credit  = strip_html(md.get('Credit',{}).get('value',''))
    descurl = info.get('descriptionurl','')
    thumb   = info.get('thumburl') or info.get('url','')
    source  = (strip_html(credit) + ' ' + strip_html(author)).lower()
    # ban watermarked agency sources
    if any(b in source for b in BANNED):
        return {'ok':False,'reason':f'agency source ({credit[:60]})'}
    if not any(a in lic_s for a in ALLOWED):
        return {'ok':False,'reason':f'licence not allowed ({lic_s})'}
    return {'ok':True,'thumb':thumb,'author':author or 'Unknown','licence':md.get('LicenseShortName',{}).get('value','') or 'Free licence','licence_url':lic_url,'descurl':descurl,'credit':credit}

prev = OUT / '_results.json'
results = json.loads(prev.read_text()) if (ONLY and prev.exists()) else {}
for slug, (title, display) in PEOPLE.items():
    if ONLY and slug not in ONLY: continue
    print(f'[{slug}] {title!r}')
    try:
        name, img = resolve_wiki(title)
        if not img:
            alt = search_title(display.split(',')[0])
            if alt and alt != name:
                name, img = resolve_wiki(alt)
        if not img:
            print('  no infobox image on Wikipedia')
            results[slug] = {'display':display,'ok':False,'reason':'no infobox image'}
            continue
        info = commons_info(img)
        picked = pick(info)
        if not picked.get('ok'):
            print('  skip:', picked.get('reason'))
            results[slug] = {'display':display,'ok':False,'reason':picked.get('reason')}
            continue
        with http(picked['thumb']) as r: raw = r.read()
        out = OUT / f'{slug}.jpg'
        size = resize(raw, out, 800)
        print(f'  OK  -> {out.name}  {size[0]}x{size[1]}  {picked["licence"]}  by {picked["author"][:40]}')
        results[slug] = {'display':display,'ok':True,'file':out.name,'author':picked['author'],'licence':picked['licence'],'licence_url':picked['licence_url'],'descurl':picked['descurl']}
    except Exception as e:
        print('  ERROR', e)
        results[slug] = {'display':display,'ok':False,'reason':str(e)}

# Markdown credits
lines = ['# TNB people photos: Wikimedia Commons credits',
         '',
         'Every photo below is self-hosted at `site/img/people/<slug>.jpg`. Sourced from Wikimedia Commons under a commercial-use licence (CC BY, CC BY-SA, CC0 or Public Domain). Follow the file-page link for the full licence text and any attribution requirements.',
         '',
         '## In use',
         '']
for slug, r in results.items():
    if r.get('ok'):
        lines.append(f"- **{r['display']}** . `{r['file']}` . Photo: {r['author']}, {r['licence']} . [Commons file]({r['descurl']})")
lines += ['', '## Not yet sourced (placeholder still shown)', '']
for slug, r in results.items():
    if not r.get('ok'):
        lines.append(f"- **{r['display']}** . reason: {r.get('reason','?')}")
(OUT / 'CREDITS.md').write_text('\n'.join(lines) + '\n')
(OUT / '_results.json').write_text(json.dumps(results, indent=2))
print('\nDone. Credits -> site/img/people/CREDITS.md')
