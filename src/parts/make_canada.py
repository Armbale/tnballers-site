# Builds parts/canada.html (Canada's best right now) and parts/legends.html (legends on Canadian soil)
def esc(s): return s.replace('&', '&amp;')

# name, pos, club, comp label, apps, goals, assists, caps, intl goals, shirt, highlight, fotmob id
BEST = [
 ('Liam Millar','Winger','Birmingham City (loan, Hull City)','All comps',10,5,4,47,1,'11','5 goals and 4 assists in 10 club games, including a brace vs QPR (17 Oct). Played 70 minutes of the 1–0 loss at Cardiff (24 Oct).','932308/liam-millar'),
 ('Alphonso Davies','Left Back / Winger','Bayern Munich','All comps',10,2,2,59,15,'19','Captain. Scored vs Arsenal in the Champions League (21 Oct, 2–2): his second UCL goal this season.','751202/alphonso-davies'),
 ('Jonathan David','Striker','Atlético Madrid (loan, Juventus)','LaLiga',5,3,2,85,43,'10','3 goals and 2 assists in five LaLiga games. Canada\'s all-time top scorer.','939569/jonathan-david'),
 ('Tani Oluwaseyi','Striker','Villarreal','LaLiga',5,0,0,31,2,'12','Two Champions League goals in a week: at Napoli (13 Oct) and at Anfield vs Liverpool (20 Oct).','1338740/tani-oluwaseyi'),
 ('Stephen Eustáquio','Central Midfield','Swansea City','Championship',8,1,1,63,5,'7','Vice-captain. Back from a shoulder knock; scored in the 2–1 win at Lincoln.','816223/stephen-eustaquio'),
 ('Tajon Buchanan','Winger','Villarreal','LaLiga',8,0,0,67,8,'17','Back from his hamstring injury: started and played 87 minutes of the 2–1 derby win over Valencia (24 Oct).','1026135/tajon-buchanan'),
]
# name, club, reason, expected back
SIDE = [
 ('Cyle Larin','Southampton','Muscle injury (17 Oct)','TBC'),
 ('Nathan Saliba','Villarreal','Muscle injury (missed 24 Oct derby)','TBC'),
 ('Ismaël Koné','Sassuolo','Broken leg','Late Oct'),
 ('Alistair Johnston','Celtic','Hamstring','Late Oct'),
 ('Moïse Bombito','OGC Nice','Tibia surgery','TBC'),
 ('Ali Ahmed','Norwich City','Ligament injury','Early Nov'),
 ('Derek Cornelius','Marseille','Hip injury','Early Jan'),
 ('Promise David','Brighton (loan)','Few Premier League minutes so far','TBC'),
]

def best_section(sfx, view_title):
    cards = ''
    for i, (n, pos, club, comp, apps, g, a, caps, ig, no, hl, fm) in enumerate(BEST):
        first, last = n.split(' ', 1)
        cards += f'''
        <li class="can-card">
          <div class="can-top"><span class="can-rank">#{i+1}</span><span class="can-pos">{esc(pos)}</span></div>
          <h3 class="can-name"><span>{esc(first)}</span>{esc(last)}</h3>
          <p class="can-club">{esc(club)}</p>
          <p class="can-comp">2026–27 · {esc(comp)}</p>
          <div class="can-stats"><div><b>{apps}</b><span>Apps</span></div><div><b>{g}</b><span>Goals</span></div><div><b>{a}</b><span>Assists</span></div></div>
          <p class="can-intl">🍁 Canada: {caps} caps · {ig} goal{'' if ig==1 else 's'}</p>
          <p class="can-hl">{esc(hl)}</p>
          <a class="can-src" href="https://www.fotmob.com/players/{fm}" target="_blank" rel="noopener noreferrer">FotMob<span class="visually-hidden"> stats for {esc(n)} (opens in a new tab)</span> ↗</a>
        </li>'''
    side = ''.join(f'''
          <li><div><b>{esc(n)}</b><span>{esc(c)}</span></div><div class="side-r"><span class="side-why">{esc(r)}</span><span class="side-back">Back: {esc(b)}</span></div></li>''' for n, c, r, b in SIDE)
    tc = ' view-title' if view_title else ''
    ta = ' tabindex="-1"' if view_title else ''
    return f'''<section id="canada{sfx}" class="can-sec" aria-labelledby="canada-h{sfx}">
  <div class="can-leaf" aria-hidden="true">🍁</div>
  <div class="max-width">
    <p class="section-eyebrow">The Standard · In Form Right Now</p>
    <h2 class="section-title{tc}" id="canada-h{sfx}"{ta}>CANADA'S BEST <span class="accent">RIGHT NOW.</span></h2>
    <p class="section-subtitle">Ranked on current form, not reputation. Canada reached the Round of 16 at the 2026 World Cup, its best ever, and this is who's carrying that into the new season.</p>
    <div class="can-wc reveal">
      <div><b>R16</b><span>Best-ever World Cup finish</span></div>
      <div><b>6–0</b><span>vs Qatar, first World Cup win</span></div>
      <div><b>43</b><span>Jonathan David, Canada's record</span></div>
      <div><b>2</b><span>Champions League goals for Davies this season</span></div>
    </div>
    <div class="can-layout">
      <div class="can-rail-wrap">
        <ul class="can-rail reveal" aria-label="Canada's in-form players">{cards}
        </ul>
      </div>
      <aside class="can-side reveal" aria-labelledby="side-h{sfx}">
        <h3 id="side-h{sfx}"><span class="side-dot" aria-hidden="true"></span>On the sidelines</h3>
        <p class="side-sub">Not playing right now. They'll be back in the top list once they're fit and starting.</p>
        <ul class="side-list">{side}
        </ul>
      </aside>
    </div>
    <p class="can-note">Club stats for 2026–27 and Canada caps as of 26 Oct 2026. Source: <a href="https://www.fotmob.com" target="_blank" rel="noopener noreferrer">FotMob</a>; transfers from club announcements. TNB isn't affiliated with these players or Canada Soccer.</p>
  </div>
</section>
'''

# ---------- legends ----------
NOW = [
 ('Thomas Müller','Vancouver Whitecaps','Since Aug 2025','🇩🇪','2014 World Cup winner. 13 Bundesliga titles with Bayern. Now in Vancouver: 9 goals and 6 assists in MLS this season (currently out with a hamstring injury).','Playing here now'),
 ('Alexis Sánchez','CF Montréal','Since Aug 2026','🇨🇱','Chile\'s all-time top scorer (51) and most-capped player (168). Two Copa Américas, and title winner at Barcelona and Inter.','Playing here now'),
]
HOME = [
 ('Sebastian Giovinco','Toronto FC','2015–19','🇮🇹','MLS MVP in his first season. Led TFC to the 2017 treble: MLS Cup, Supporters\' Shield and Canadian Championship.'),
 ('Didier Drogba','Montreal Impact','2015–16','🇨🇮','Chelsea\'s Champions League hero hit a hat-trick on his first start and 11 goals in his first 11 MLS games.'),
 ('Thierry Henry','CF Montréal (head coach)','2019–21','🇫🇷','Arsenal\'s all-time top scorer and a World Cup winner coached Montreal through the 2020 season.'),
 ('Alessandro Nesta','Montreal Impact','2012–13','🇮🇹','2006 World Cup winner and two-time Champions League winner, finishing his career in Montreal.'),
 ('Lorenzo Insigne','Toronto FC','2022–25','🇮🇹','Euro 2020 winner with Italy. Napoli legend turned Toronto FC designated player.'),
]
MOMENTS = [
 ('1970s','Pelé, Cruyff, Beckenbauer','The NASL era brought the world\'s greatest to Toronto, Vancouver and Montreal.'),
 ('1983','Michel Platini','Juventus and the three-time Ballon d\'Or winner faced the Toronto Blizzard.'),
 ('1996','Diego Maradona','Played an exhibition for Toronto Italia alongside his brother.'),
 ('2007','Agüero, Di María, Suárez, Piqué','The U-20 World Cup in Canada. Agüero won the Golden Ball and Golden Boot as Argentina lifted the trophy.'),
 ('2009','Cristiano Ronaldo','Real Madrid beat Toronto FC 5–1 in a friendly at Rogers Centre.'),
 ('May 2026','Lionel Messi','A goal and two assists as Inter Miami won 4–2 at BMO Field, in front of a record 44,828.'),
 ('Jul 2026','Cristiano Ronaldo','Scored a penalty at BMO Field as Portugal beat Croatia 2–1, becoming the oldest scorer in World Cup knockout history (41).'),
]

def legends_section(sfx):
    now = ''.join(f'''
      <article class="leg-now">
        <span class="leg-tag">{t}</span>
        <div class="leg-flag" aria-hidden="true">{f}</div>
        <h3>{esc(n)}</h3>
        <p class="leg-club">{esc(c)} · {esc(y)}</p>
        <p class="leg-desc">{esc(d)}</p>
      </article>''' for n, c, y, f, d, t in NOW)
    home = ''.join(f'''
        <li class="leg-card"><div class="leg-card-top"><span aria-hidden="true">{f}</span><span class="leg-years">{esc(y)}</span></div><h4>{esc(n)}</h4><p class="leg-club">{esc(c)}</p><p class="leg-desc">{esc(d)}</p></li>''' for n, c, y, f, d in HOME)
    mom = ''.join(f'''
        <li><span class="tl-year">{esc(y)}</span><div><b>{esc(n)}</b><p>{esc(d)}</p></div></li>''' for y, n, d in MOMENTS)
    return f'''<section id="legends{sfx}" class="leg-sec" aria-labelledby="legends-h{sfx}">
  <div class="max-width">
    <p class="section-eyebrow">Legends on Canadian Soil</p>
    <h2 class="section-title" id="legends-h{sfx}">THE GREATS PLAYED <span class="accent">HERE.</span></h2>
    <p class="section-subtitle">From Pelé to Messi, the biggest names in the game have played on Canadian grass. Some of them still call it home.</p>
    <div class="leg-now-grid reveal">{now}
    </div>
    <h3 class="leg-h3">They called Canada home</h3>
    <ul class="leg-grid reveal">{home}
    </ul>
    <h3 class="leg-h3">One night only</h3>
    <ol class="leg-tl reveal">{mom}
    </ol>
    <p class="can-note">Sources: club announcements, FotMob, TSN, Sports Illustrated and CPL.</p>
  </div>
</section>
'''

if __name__ == '__main__':
    # Legacy writers for the old build chain. Guarded so build_home.py can import
    # the module safely to read BEST/SIDE/NOW/HOME/MOMENTS without side effects.
    import os
    if os.path.isdir('parts'):
        open('parts/canada.html', 'w').write(best_section('', False))
        open('parts/canada_view.html', 'w').write(best_section('-view', True))
        open('parts/legends.html', 'w').write(legends_section(''))
        print('ok')
