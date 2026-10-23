# Builds the Live Tracker feed (parts/feed.html for home, parts/feed_view.html for the Canada tab) from parts/feed.json.
# Newest first. To add an item: append {"date","tag","headline","detail","link"} to feed.json (tags: TNB, Goal, Trophy, Award, Injury, Transfer, Call-up, Matchday).
import json, datetime, html
items = sorted(json.load(open('parts/feed.json')), key=lambda x: x['date'], reverse=True)
def esc(s): return html.escape(s, quote=True)
def fmt(d): return datetime.date.fromisoformat(d).strftime('%-d %b')
def section(sfx, limit, view_title):
    lis = ''.join(f'''
        <li class="feed-item feed-{esc(i['tag'].lower().replace(' ','-'))}">
          <div class="feed-meta"><span class="feed-tag">{esc(i['tag'])}</span><time datetime="{i['date']}">{fmt(i['date'])}</time></div>
          <h3 class="feed-h">{esc(i['headline'])}</h3>
          <p class="feed-d">{esc(i['detail'])}</p>
          {f'<a class="feed-src" href="{esc(i["link"])}" target="_blank" rel="noopener noreferrer">Source<span class="visually-hidden"> for {esc(i["headline"])} (opens in a new tab)</span> ↗</a>' if i.get('link') else ''}
        </li>''' for i in items[:limit])
    tc = ' view-title' if view_title else ''
    ta = ' tabindex="-1"' if view_title else ''
    return f'''<section id="tracker{sfx}" class="feed-sec" aria-labelledby="tracker-h{sfx}">
  <div class="max-width">
    <p class="section-eyebrow"><span class="feed-live" aria-hidden="true"></span> Live Tracker</p>
    <h2 class="section-title{tc}" id="tracker-h{sfx}"{ta}>CANADIAN FOOTBALL, <span class="accent">AS IT HAPPENS.</span></h2>
    <p class="section-subtitle">Goals, trophies, injuries and big moments for our players and every Canadian worth watching, updated through the day.</p>
    <ol class="feed-list reveal">{lis}
    </ol>
    <p class="can-note">Last updated {fmt(items[0]['date']) if items else ''}. Sources linked on each item.</p>
  </div>
</section>
'''
open('parts/feed.html','w').write(section('', 6, False))
open('parts/feed_view.html','w').write(section('-view', 30, False))
print('feed ok', len(items))
