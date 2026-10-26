#!/usr/bin/env python3
"""
Build site/index.html from src/parts/home.html (template) + the data files.

Dynamic blocks replaced from data:
  - STATS_ASOF date         <- src/parts/nine_data.js
  - window.ninePlayers      <- src/parts/nine_data.js (array literal, verbatim)
  - window.peoplePhotos     <- site/img/people/_results.json
  - window.feedPosts        <- site/social/*/feed.jpg
  - Ticker items            <- src/parts/feed.json  (newest 6, duplicated for seamless loop)
  - "Live events, last 7d"  <- feed.json (count within 7 days of STATS_ASOF)
  - Metrics band counts     <- computed from the data files
  - Canada's Best scoreboard<- make_canada.BEST
  - Sidelined list          <- make_canada.SIDE
  - Legends teaser (NOW)    <- make_canada.NOW
  - Legends full section    <- make_canada.NOW + HOME + MOMENTS
  - Preview banner          -> removed
"""
import datetime
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PARTS = ROOT / 'src' / 'parts'
SITE  = ROOT / 'site'

def esc(s):
    s = str(s)
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;').replace("'", '&#39;'))

def jsesc(s):
    return (str(s).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n'))

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------
nine_js_text = (PARTS / 'nine_data.js').read_text(encoding='utf-8')
m = re.search(r"var STATS_ASOF = '([^']+)';", nine_js_text)
if not m:
    sys.exit('STATS_ASOF not found in nine_data.js')
STATS_ASOF = m.group(1)

# Pull the ninePlayers array literal verbatim
m = re.search(r"var ninePlayers = (\[.*?\]);\s*\nwindow\.ninePlayers", nine_js_text, re.DOTALL)
if not m:
    sys.exit('ninePlayers array not found in nine_data.js')
nine_array = m.group(1)

# Expand IMG.<key> placeholders used in the live site (they point to /players/<key>.png)
# But the preview inlines paths as strings. The current nine_data.js uses `IMG.<key>` tokens.
# Replace IMG.<key> → "/players/<key>.png".
_IMG_FILE = {'greco': 'greco-taylor'}  # nine_data key -> file name in site/players/
nine_array = re.sub(r"IMG\.([a-z\-]+)", lambda m: f"'/players/{_IMG_FILE.get(m.group(1), m.group(1))}.png'", nine_array)

# Load feed.json
feed_all = json.loads((PARTS / 'feed.json').read_text(encoding='utf-8'))
feed_all.sort(key=lambda i: i['date'], reverse=True)

# Pick the "today" from the STATS_ASOF text, then compute live events in last 7 days
def parse_date(s):
    for fmt in ('%d %b %Y', '%Y-%m-%d'):
        try: return datetime.datetime.strptime(s, fmt).date()
        except Exception: pass
    return datetime.date.today()
asof_date = parse_date(STATS_ASOF)
cutoff = asof_date - datetime.timedelta(days=7)
feed_last7 = [i for i in feed_all if datetime.date.fromisoformat(i['date']) >= cutoff]
LIVE7 = len(feed_last7)

# People photos
PEOPLE = {}
pres = SITE / 'img' / 'people' / '_results.json'
if pres.exists():
    data = json.loads(pres.read_text(encoding='utf-8'))
    for slug, r in data.items():
        if r.get('ok'):
            PEOPLE[r['display']] = {
                'f': '/img/people/' + r['file'],
                'a': r['author'].split('/')[0].strip()[:42] if r.get('author') else 'Unknown',
                'l': r['licence'],
                'u': r.get('descurl', ''),
            }

# make_canada module (BEST, SIDE, NOW, HOME, MOMENTS live there)
spec = importlib.util.spec_from_file_location('make_canada', PARTS / 'make_canada.py')
mc = importlib.util.module_from_spec(spec); spec.loader.exec_module(mc)

# ------------------------------------------------------------------
# Render dynamic blocks
# ------------------------------------------------------------------
# Ticker items
_TAG_FALLBACKS = {'TNB':'TNB','Goal':'Goal','Trophy':'Trophy','Award':'Award','Injury':'Injury',
                  'Transfer':'Transfer','Call-up':'Call-up','Matchday':'Matchday','Signing':'Signing'}
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
def date_short(iso):
    try:
        d = datetime.date.fromisoformat(iso)
        return f'{d.day} {MONTHS[d.month-1]}'
    except Exception: return iso
def ticker_items():
    items = feed_all[:6]
    def render_one(it, dup=False):
        href = it.get('link') or 'https://instagram.com/tnballers'
        hid = ' aria-hidden="true"' if dup else ''
        tx = ' tabindex="-1"' if dup else ''
        head = esc(it['headline']).replace('–','-')  # keep an en-dash out of ticker heads too; prefer "to"
        return (f'<span class="ticker-item"{hid}>'
                f'<span class="t-tag">{esc(_TAG_FALLBACKS.get(it["tag"], it["tag"]))}</span>'
                f'<span class="t-date">{esc(date_short(it["date"]))}</span>'
                f'<a href="{esc(href)}" target="_blank" rel="noopener noreferrer"{tx}>'
                f'<span class="t-head">{head}</span></a></span>')
    out = []
    for it in items: out.append(render_one(it))
    out.append('')  # new line
    for it in items: out.append(render_one(it, dup=True))
    return '\n        '.join(out)

# Canada scoreboard rows
POS_SHORT = {'Winger':'WG','Striker':'ST','Centre-back':'CB','Full-back':'FB','Left Back':'LB',
             'Right Back':'RB','Left Back / Winger':'LB','Central Midfield':'CM','Defensive midfield':'DM',
             'Attacking midfield':'AM','Goalkeeper':'GK','Centre Forward':'ST'}
def pos_abbr(pos):
    return POS_SHORT.get(pos, ''.join([w[0] for w in pos.split()[:2]]).upper()[:3])

def canada_rows():
    rows = []
    for i, (n, pos, club, comp, apps, g, a, caps, intlg, no, hl, fm) in enumerate(mc.BEST):
        # Keep the ticker/form note free of en-dashes.
        hl_clean = hl.replace('–','-')
        hl_short = hl_clean.split('.')[0]  # first sentence as short form
        if len(hl_short) > 60: hl_short = hl_short[:58] + '…'
        rows.append(
            f'<button type="button" class="score-row" role="row" data-can-i="{i}" '
            f'data-form="{esc(hl_clean)}">'
            f'<span class="rank">{i+1}</span><span class="pos">{esc(pos_abbr(pos))}</span>'
            f'<div class="name"><span class="n">{esc(n)}</span><span class="c">{esc(club)}</span></div>'
            f'<span class="hl">{esc(hl_short)}</span>'
            f'<span class="n-stat">{apps}<span class="u">GP</span></span>'
            f'<span class="n-stat">{g}<span class="u">G</span></span>'
            f'<span class="n-stat">{a}<span class="u">A</span></span>'
            f'</button>')
    return '\n        '.join(rows)

def canada_js_data():
    """JSON array for the Canada profile modal."""
    out = []
    for n, pos, club, comp, apps, g, a, caps, intlg, no, hl, fm in mc.BEST:
        out.append({'name':n, 'pos':pos, 'club':club, 'apps':apps, 'g':g, 'a':a,
                    'caps':caps, 'intl':intlg, 'no':no, 'form':hl.replace('–','-'), 'fm':fm,
                    'ig':getattr(mc,'IG',{}).get(n,'')})
    return json.dumps(out, ensure_ascii=False)

def sidelined_rows():
    rows = []
    for i, (n, club, reason, back) in enumerate(mc.SIDE):
        rows.append(
            f'<li tabindex="0" role="button" data-side-i="{i}" aria-label="{esc(n)}, open profile">'
            f'<div><div class="pname">{esc(n)}</div><div class="pclub">{esc(club)}</div></div>'
            f'<div class="why">{esc(reason)}. Back: {esc(back)}</div></li>')
    return '\n          '.join(rows)

def sidelined_js_data():
    out = []
    for n, club, reason, back in mc.SIDE:
        out.append({'name':n, 'club':club, 'reason':reason, 'date':STATS_ASOF, 'back':back,
                    'note':f'{reason}. Expected back: {back}.',
                    'ig':getattr(mc,'IG',{}).get(n,'')})
    return json.dumps(out, ensure_ascii=False)

# Legends teaser (NOW)
def legend_pic(name):
    ph = PEOPLE.get(name)
    if not ph:
        return '<div class="leg-pic" aria-hidden="true"></div>'
    return (f'<div class="leg-pic"><img src="{esc(ph["f"])}" alt="{esc(name)}" loading="lazy">'
            f'<span class="leg-credit">Photo: {esc(ph["a"])}, '
            f'<a href="{esc(ph["u"])}" target="_blank" rel="noopener noreferrer">{esc(ph["l"])} / Wikimedia</a>'
            f'</span></div>')

def legend_now_cards():
    cards = []
    for n, c, y, flag, d, tag in mc.NOW:
        cards.append(
            f'<article class="leg-card" tabindex="0">'
            f'{legend_pic(n)}'
            f'<span class="flag" aria-hidden="true">{flag}</span>'
            f'<span class="tag">{esc(tag)}</span>'
            f'<h3>{esc(n)}</h3>'
            f'<p class="club">{esc(c)} · {esc(y)}</p>'
            f'<p class="desc">{esc(d)}</p>'
            + (f'<a class="leg-ig" href="https://www.instagram.com/{esc(getattr(mc,"IG",{})[n])}/" target="_blank" rel="noopener noreferrer">Follow @{esc(getattr(mc,"IG",{})[n])}</a>' if getattr(mc,'IG',{}).get(n) else '')
            + f'</article>')
    return '\n      '.join(cards)

def legend_full():
    now = []
    for n, c, y, flag, d, tag in mc.NOW:
        now.append(
            f'<article class="leg-card">{legend_pic(n)}'
            f'<span class="flag" aria-hidden="true">{flag}</span><span class="tag">{esc(tag)}</span>'
            f'<h3>{esc(n)}</h3><p class="club">{esc(c)} · {esc(y)}</p>'
            f'<p class="desc">{esc(d)}</p></article>')
    home = []
    for n, c, y, flag, d in mc.HOME:
        home.append(
            f'<article class="leg-card">{legend_pic(n)}'
            f'<span class="flag" aria-hidden="true">{flag}</span><span class="tag">{esc(y)}</span>'
            f'<h3>{esc(n)}</h3><p class="club">{esc(c)}</p>'
            f'<p class="desc">{esc(d)}</p></article>')
    moments = []
    for y, n, d in mc.MOMENTS:
        moments.append(f'<li><span class="tl-year">{esc(y)}</span>'
                       f'<div><b>{esc(n)}</b><p>{esc(d)}</p></div></li>')
    return {
        'now': '\n      '.join(now),
        'home': '\n      '.join(home),
        'moments': '\n      '.join(moments),
    }

# Feed strip from site/social/*/feed.jpg
def feed_posts():
    social = SITE / 'social'
    if not social.exists():
        return []
    out = []
    for d in sorted(social.iterdir(), reverse=True):
        f = d / 'feed.jpg'
        if f.exists():
            out.append({'img': f'/social/{d.name}/feed.jpg',
                        'url': 'https://instagram.com/tnballers',
                        'cap': d.name})
        if len(out) >= 6: break
    return out

# Partner-club count (CPL)
def partner_club_count():
    clubs = set(re.findall(r"club:'([^']+)'", nine_js_text))
    return len(clubs)

PARTNER_CLUBS = partner_club_count()
PARTNER_PLAYERS = len(re.findall(r"\bfirst:'", nine_js_text))

# ------------------------------------------------------------------
# Patch the template
# ------------------------------------------------------------------
tpl = (PARTS / 'home.html').read_text(encoding='utf-8')

# 1. STATS_ASOF (in the inline <script> that defines window.STATS_ASOF)
tpl = re.sub(r"window\.STATS_ASOF = '[^']+';", f"window.STATS_ASOF = '{STATS_ASOF}';", tpl, count=1)

# 1b. Canada's Best "as of" date follows the can-note in make_canada.py (updated by the tracker)
_mc = (PARTS / 'make_canada.py').read_text(encoding='utf-8')
_m = re.search(r'caps as of (\d{1,2} \w+ \d{4})', _mc)
if _m:
    tpl = re.sub(r'caps as of \d{1,2} \w+ \d{4}', 'caps as of ' + _m.group(1), tpl)

# 2. window.ninePlayers array literal (replace the preview's inline array with the live nine_data.js one)
tpl = re.sub(r"window\.ninePlayers = \[.*?\];",
             f"window.ninePlayers = {nine_array};",
             tpl, count=1, flags=re.DOTALL)

# 3. window.peoplePhotos (if present)
photos_js = json.dumps(PEOPLE, ensure_ascii=False)
tpl = re.sub(r"window\.peoplePhotos = \{.*?\};",
             f"window.peoplePhotos = {photos_js};",
             tpl, count=1, flags=re.DOTALL)

# 4. Inject window.canadaBest / window.sideList / window.feedPosts next to STATS_ASOF (replaces the hard-coded canadaProfile data in the preview)
inject = (f"window.canadaBest = {canada_js_data()};\n"
          f"window.sideList = {sidelined_js_data()};\n"
          f"window.feedPosts = {json.dumps(feed_posts(), ensure_ascii=False)};\n")
tpl = re.sub(r"(window\.STATS_ASOF = '[^']+';)",
             r"\1\n" + inject, tpl, count=1)

# 4b. Rewrite canadaProfile JS to use window.canadaBest / window.sideList instead of inline literals.
tpl = re.sub(r"var canBest = \[.*?\];\s*\n\s*var sideList = \[.*?\];",
             "var canBest = window.canadaBest || []; var sideList = window.sideList || [];",
             tpl, count=1, flags=re.DOTALL)

# 5. Replace ticker items
ticker_block_re = re.compile(r'(<div class="ticker-track" id="tickerTrack">)(.*?)(</div>)', re.DOTALL)
tpl = ticker_block_re.sub(
    lambda m: m.group(1) + '\n        ' + ticker_items() + '\n      ' + m.group(3),
    tpl, count=1)

# 6. Replace Canada's Best scoreboard rows (after the scoreboard-head div, before the closing scoreboard </div>)
scoreboard_re = re.compile(
    r'(<div class="scoreboard" role="table" aria-label="Canada\'s in-form players, ranked" id="canScoreboard">\s*<div class="scoreboard-head" role="row">\s*<div>#</div><div>Pos</div><div>Player / Club</div><div>Form</div>\s*<div class="r-stat">Apps</div><div class="r-stat">G</div><div class="r-stat">A</div>\s*</div>)(.*?)(</div>\s*(?=<aside class="sidelined"))',
    re.DOTALL)
tpl = scoreboard_re.sub(
    lambda m: m.group(1) + '\n        ' + canada_rows() + '\n      ' + m.group(3),
    tpl, count=1)

# 7. Replace sidelined list
sidelined_re = re.compile(r'(<ul id="sidelinedList">)(.*?)(</ul>)', re.DOTALL)
tpl = sidelined_re.sub(
    lambda m: m.group(1) + '\n          ' + sidelined_rows() + '\n        ' + m.group(3),
    tpl, count=1)

# 8. Replace Legends teaser cards (<div class="leg-grid reveal">...</div>, first match in legends-teaser section)
teaser_re = re.compile(r'(<section class="legends grain" aria-label="Legends teaser">[^<]*<div class="wrap">.*?<div class="leg-grid reveal">)(.*?)(</div>\s*<div class="leg-foot">)', re.DOTALL)
tpl = teaser_re.sub(
    lambda m: m.group(1) + '\n      ' + legend_now_cards() + '\n    ' + m.group(3),
    tpl, count=1)

# 9. Replace Legends full section
lf = legend_full()
# Find NOW / HOME / MOMENTS blocks in the full chronicle section by their H3 labels
full_re = re.compile(r'(<section id="legends" class="legal-stub".*?<h3 class="pm-h">Playing here now</h3>\s*<div class="legends-grid">)(.*?)(</div>\s*<h3 class="pm-h">They called Canada home</h3>\s*<div class="legends-grid">)(.*?)(</div>\s*<h3 class="pm-h">One night only</h3>\s*<ol class="leg-tl">)(.*?)(</ol>)', re.DOTALL)
tpl = full_re.sub(
    lambda m: (m.group(1) + '\n      ' + lf['now'] + '\n    ' +
               m.group(3) + '\n      ' + lf['home'] + '\n    ' +
               m.group(5) + '\n      ' + lf['moments'] + '\n    ' + m.group(7)),
    tpl, count=1)

# 10. Metrics band data-count values
def set_metric(label, value):
    global tpl
    tpl = re.sub(
        r'(<div class="mlbl">' + re.escape(label) + r'</div>\s*<div class="mval"><span data-count=")\d+(">)',
        lambda m: m.group(1) + str(value) + m.group(2), tpl, count=1)
set_metric('Partner players', PARTNER_PLAYERS)
set_metric('Live events, last 7 days', LIVE7)
set_metric('Partner clubs (CPL)', PARTNER_CLUBS)
set_metric("Canada's Best, tracked", len(mc.BEST))
tpl = re.sub(r'(Plus\s*<span data-count=")\d+(">0</span>\s*on the sidelined list\.)',
             lambda m: m.group(1) + str(len(mc.SIDE)) + m.group(2), tpl, count=1)

# 11. Hero live-events-last-7-days value
tpl = re.sub(r'<span class="lbl">Live events, last 7 days</span>\s*<span class="val" data-count="\d+">',
             f'<span class="lbl">Live events, last 7 days</span>\n          <span class="val" data-count="{LIVE7}">',
             tpl, count=1)

# 12. Remove the preview banner (if present)
tpl = re.sub(r'<div class="preview-banner".*?</div>\s*', '', tpl, count=1)
# And its CSS .preview-banner rule is harmless if left in; keep it (CSS cost ~160 bytes).

# 13. Change preview <title> back to the production title + robots content.
tpl = re.sub(r'<title>TNB · homepage preview</title>', '<title>True North Ballers · Canadian football, unfiltered.</title>', tpl, count=1)
tpl = re.sub(r'<meta name="robots" content="noindex,nofollow">\s*', '', tpl, count=1)

# ------------------------------------------------------------------
# Write it
# ------------------------------------------------------------------
out = SITE / 'index.html'
out.write_text(tpl, encoding='utf-8')
print(f'wrote {out}  ({len(tpl):,} chars)')
print(f'  STATS_ASOF={STATS_ASOF}  LIVE7={LIVE7}  PARTNER_PLAYERS={PARTNER_PLAYERS}  PARTNER_CLUBS={PARTNER_CLUBS}')
