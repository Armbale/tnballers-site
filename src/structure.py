import re
s = open('work.html').read()
P = lambda f: open('parts/'+f).read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n >= 1, 'MISSING: ' + old[:90]
    if count == 1: assert n == 1, 'NOT UNIQUE (%d): %s' % (n, old[:90])
    s = s.replace(old, new) if count != 1 else s.replace(old, new, 1)

def cut(start_marker, end_marker):
    """remove s[start:end] (end exclusive) and return removed text"""
    global s
    i = s.index(start_marker); j = s.index(end_marker, i)
    chunk = s[i:j]; s = s[:i] + s[j:]
    return chunk

# ---------- head ----------
rep('<meta name="theme-color" content="#CC0000">', '<meta name="theme-color" content="#F6F3EE">')
rep('<html lang="en">', '<html lang="en-CA">')
rep('</style>', P('extra.css') + P('nine.css') + '\n</style>\n</head>')
rep('<body>\n', '<body>\n<a class="skip-link" href="#main-content">Skip to content</a>\n')

# ---------- preloader / logos alt ----------
rep('<img src="True_North_Ballers_Badge.png" alt="TNB" width="44" height="44" loading="eager">',
    '<img src="True_North_Ballers_Badge.png" alt="" width="44" height="44" loading="eager">')
rep('<a href="#hero" class="sidebar-logo">', '<a href="#home" class="sidebar-logo" aria-label="True North Ballers, home">')
rep('<img src="True_North_Ballers_Badge.png" alt="True North Ballers" width="100" height="100" loading="eager">',
    '<img src="True_North_Ballers_Badge.png" alt="True North Ballers crest" width="100" height="100" loading="eager">')
rep('<img src="True_North_Ballers_Badge.png" alt="TNB" loading="lazy" width="42" height="42">',
    '<img src="True_North_Ballers_Badge.png" alt="" loading="lazy" width="42" height="42">')

# ---------- tickers ----------
rep('<span>NEW KIT DROP COMING SOON</span><span class="ts">//</span>\n', '<span>CICCARELLI · 6 CPL GOALS IN 2026</span><span class="ts">//</span>\n', count=2)
rep('<span>TNB x SPORTIRA KIT  -  AVAILABLE NOW</span><span class="dot">◆</span>', '<span>BIBISHKOV: CANADA U-20 AT CONCACAF</span><span class="dot">◆</span>', count=2)
rep('<span>GRECO-TAYLOR: CONFIRMED LB</span>', '<span>DAVIES SCORES vs ARSENAL ⚽</span>', count=2)
rep('<span>STARTING XI  -  INAUGURAL CLASS 2026</span>', '<span>8 PLAYERS · ONE SEASON · EVERY MOMENT</span>', count=2)
rep('<span>STARTING XI · INAUGURAL CLASS 2026</span>', '<span>8 CPL PROS · COVERED ALL SEASON</span>', count=2)
rep('    <span>BRAMPTON · TORONTO · CANADA · WORLD</span><span class="ts">//</span>\n', '    <span>OLGUIN: FIRST PRO GOAL ⚽</span><span class="ts">//</span>\n', count=2)
rep('<span>TAVERNIER · BRUNO · BIBISHKOV · CICCARELLI · PAVELA</span>', '<span>LEAD SPONSORS: SHOBHIT BANWAIT × TRIXAFA</span>', count=2)
rep('<a href="#starting-xi" class="btn-primary">View the XI</a>', '<a href="#nine" class="btn-primary">Meet the Players</a>')
rep('<a href="#recruit" class="btn-ghost">Get Scouted</a>', '<a href="#scouted" class="btn-ghost">Get Scouted</a>')
rep('BELONG IN THE <span class="accent">XI?</span>', 'COULD BE <span class="accent">NEXT?</span>')
rep('Documenting Canada\'s soccer culture - from Brampton to the world.', 'Documenting Canada\'s soccer culture, one player at a time.')
rep('</div>\n\n<aside class="site-sidebar"', '</div>\n<button class="motion-toggle" id="motionToggle" type="button" aria-pressed="false" aria-label="Pause animations">❚❚</button>\n\n<aside class="site-sidebar"')


# ---------- Forge FC: 2026 Canadian Champions (23 Oct 2026) ----------
rep('<span>20M+ MONTHLY VIEWS</span><span class="ts">//</span>', '<span>FORGE FC: 2026 CANADIAN CHAMPIONS 🏆</span><span class="ts">//</span>', count=2)
rep('<span>🍁 THE NORTH IS RISING</span><span class="dot">◆</span>', '<span>🏆 FORGE FC: FIRST CPL CLUB TO WIN THE CANADIAN CHAMPIONSHIP</span><span class="dot">◆</span>', count=2)
rep('<span>THE NORTH IS RISING 🍁</span><span class="ts">//</span>', '<span>DAVIES SCORES VS ARSENAL ⚽</span><span class="ts">//</span><span>MILLAR: 5 GOALS, 4 ASSISTS</span><span class="ts">//</span>', count=2)
rep('<div class="red-ticker-wrap" aria-hidden="true">', P('news_banner.html') + '\n<div class="red-ticker-wrap" aria-hidden="true">')

# ---------- sidebar + mobile nav ----------
old_nav = s[s.index('<nav class="sidebar-nav">'):s.index('</nav>', s.index('<nav class="sidebar-nav">'))+6]
s = s.replace(old_nav, '''<nav class="sidebar-nav" aria-label="Main">
    <a href="#home" data-view-link="home">Home</a>
    <a href="#nine" data-view-link="nine">The Players</a>
    <a href="#canada" data-view-link="canada">Canada</a>
    <a href="#studios" data-view-link="studios">Studios</a>
    <a href="#about" data-view-link="about">About</a>
    <a href="#book" data-view-link="book" class="nav-book">Book a Shoot</a>
    <a href="#scouted" data-view-link="scouted" class="nav-cta">Get Scouted</a>
  </nav>''')
rep('<aside class="site-sidebar" role="navigation" aria-label="Main navigation">', '<aside class="site-sidebar">')
old_m = s[s.index('<nav class="mobile-nav"'):s.index('</nav>', s.index('<nav class="mobile-nav"'))+6]
s = s.replace(old_m, '''<nav class="mobile-nav" id="mobileNav" aria-label="Mobile">
  <button class="mobile-nav-close" type="button" onclick="closeMobileNav()" aria-label="Close menu">✕</button>
  <a href="#home" data-view-link="home">Home</a>
  <a href="#nine" data-view-link="nine">The Players</a>
  <a href="#canada" data-view-link="canada">Canada</a>
  <a href="#studios" data-view-link="studios">Studios</a>
  <a href="#about" data-view-link="about">About</a>
  <a href="#book" data-view-link="book">Book a Shoot</a>
  <a href="#scouted" data-view-link="scouted">Get Scouted</a>
</nav>''')
rep('<button class="hamburger" onclick="openMobileNav()" aria-label="Open menu" aria-expanded="false">',
    '<button class="hamburger" type="button" onclick="openMobileNav()" aria-label="Open menu" aria-expanded="false" aria-controls="mobileNav">')

# ---------- remove sponsors / kit / partners ----------
cut('<section id="apparel"', '<section id="recruit"')   # also drops partners + separators between
# credibility strip: partners -> XI confirmed
rep('<div class="cred-item"><div class="cred-num" id="credPartners">0</div><div class="cred-label">Brand Partners</div></div>',
    '<div class="cred-item"><div class="cred-num" id="credXI">0</div><div class="cred-label">Partner Players</div></div>')
# metrics: replace media units + brand partners blocks
i = s.index('<div class="countup-num" data-target="3" data-suffix="" data-label="units">')
blk_start = s.rfind('<div class="countup-block">', 0, i); blk_end = s.index('</div>\n      </div>', i) + len('</div>\n      </div>')
s = s[:blk_start] + '''<div class="countup-block">
        <div class="countup-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm0 3.3l2.2 1.6-.8 2.6h-2.8l-.8-2.6L12 5.3zM6.3 8.6l2.6.1.9 2.7-2 1.6-2.4-1.1.9-3.3zm11.4 0l.9 3.3-2.4 1.1-2-1.6.9-2.7 2.6-.1zM9.6 14.4h4.8l1.3 2.3-1.4 2.2a7 7 0 01-4.6 0l-1.4-2.2 1.3-2.3z"/></svg></div>
        <div><div class="countup-num" data-label="xi">8</div><div class="countup-label">Partner Players</div><div class="countup-desc">Covered until the end of the 2026 season</div></div>
      </div>''' + s[blk_end:]
i = s.index('<div class="countup-num" data-target="4" data-suffix="" data-label="partners">')
blk_start = s.rfind('<div class="countup-block">', 0, i); blk_end = s.index('</div>\n      </div>', i) + len('</div>\n      </div>')
s = s[:blk_start] + '''<div class="countup-block">
        <div class="countup-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 1l9 4v6c0 5.5-3.8 10.7-9 12-5.2-1.3-9-6.5-9-12V5l9-4zm0 6a3 3 0 100 6 3 3 0 000-6z"/></svg></div>
        <div><div class="countup-num" data-label="clubs">5</div><div class="countup-label">CPL Clubs Represented</div><div class="countup-desc">Forge · HFX · Vancouver · Pacific · Inter Toronto</div></div>
      </div>''' + s[blk_end:]
# social card YouTube label
rep('<div class="social-label">Documentary · Docs</div>', '<div class="social-label">Player Features</div>')

# ---------- media engine: TNB Studios only ----------
i = s.index('<section id="media-engine"'); j = s.index('</section>', i) + len('</section>')
studio_panel = re.search(r'<div class="dossier-panel">\s*<div class="dossier-number" aria-hidden="true">01</div>.*?</p>\s*</div>', s[i:j], re.S).group(0)
s = s[:i] + '''<section id="media-engine" aria-labelledby="media-engine-h">
  <div class="max-width">
    <p class="section-eyebrow">TNB Studios</p>
    <h2 class="section-title" id="media-engine-h">ONE STUDIO.<br><span class="accent">EVERY FRAME.</span></h2>
    <p class="section-subtitle">Vertical-first, cinematic storytelling built for social. The athlete is always the story.</p>
    <div class="media-engine-grid studio-grid reveal">
      ''' + studio_panel + '''
      <div class="dossier-panel">
        <div class="dossier-number" aria-hidden="true">02</div>
        <div class="dossier-tag">WHAT WE MAKE</div>
        <h3 class="dossier-title">CONTENT PILLARS</h3>
        <ul class="studio-list">
          <li><span>🎥</span>Player profiles of Canada's top young talent</li>
          <li><span>⚽</span>Match highlights from the CPL and youth national teams</li>
          <li><span>🍁</span>Canadian soccer stories, grassroots to pro</li>
          <li><span>🌍</span>Canadian athletes abroad</li>
        </ul>
      </div>
      <div class="dossier-panel studio-soon">
        <div class="dossier-number" aria-hidden="true">03</div>
        <div class="dossier-reveal-badge"><span>Coming Soon</span></div>
        <h3 class="dossier-title">UNIT 4</h3>
        <p class="dossier-reveal-text">A new unit is assembling. Details drop when it's ready.</p>
      </div>
      <div class="dossier-panel studio-soon">
        <div class="dossier-number" aria-hidden="true">04</div>
        <div class="dossier-reveal-badge"><span>Coming Soon</span></div>
        <h3 class="dossier-title">UNIT 5</h3>
        <p class="dossier-reveal-text">More to be revealed. The roster isn't complete yet.</p>
      </div>
    </div>
  </div>
</section>''' + s[j:]

# ---------- recruit copy ----------
rep('TNB has direct relationships with Forge FC, CPL scouts, and coaches across the Canadian pyramid.',
    'Our network runs through CPL clubs, scouts and coaches across the Canadian pyramid.')

# ---------- STARTING XI: node numbers, a11y attributes ----------
numfix = [
          ('x="330" y="204" text-anchor="middle" dominant-baseline="middle" fill="#fff" font-family="\'Bebas Neue\',Impact,sans-serif" font-size="7.5">11<', '20'),
          ('x="130" y="359" text-anchor="middle" dominant-baseline="middle" fill="#fff" font-family="\'Bebas Neue\',Impact,sans-serif" font-size="7.5">8<', '32'),
          ('x="118" y="504" text-anchor="middle" dominant-baseline="middle" fill="#fff" font-family="\'Bebas Neue\',Impact,sans-serif" font-size="7.5">3<', '15'),
          ('x="342" y="504" text-anchor="middle" dominant-baseline="middle" fill="#fff" font-family="\'Bebas Neue\',Impact,sans-serif" font-size="7.5">RB<', '3'),
          ('x="230" y="549" text-anchor="middle" dominant-baseline="middle" fill="#050505" font-family="\'Bebas Neue\',Impact,sans-serif" font-size="9">1<', '12')]
for old, n in numfix:
    rep(old, old.rsplit('>',1)[0] + '>' + n + '<')
rep('fill="rgba(120,200,255,0.9)" font-family="\'Barlow Condensed\',sans-serif" font-size="7" font-weight="700" letter-spacing="2">CONTENTION<',
    'fill="rgba(120,200,255,0.95)" font-family="\'Barlow Condensed\',sans-serif" font-size="6.5" font-weight="700" letter-spacing="1.5">IN CONTENTION<', count=1)
names = ['Marsel Bibishkov, left wing, confirmed','Tavio Ciccarelli, centre forward, confirmed','Kevaughn Tavernier, right wing, confirmed',
         'Zayne Bruno, central midfield, confirmed','Lucas Olguin, right centre midfield, confirmed','Sami Keshavarz, left centre midfield, confirmed',
         'Christian Greco-Taylor, left back, confirmed','Matteo Campagna, centre back, confirmed','Marko Stojadinovic, centre back, confirmed',
         'Thomas LeBeuf, right back, in contention','Ivan Pavela, goalkeeper, confirmed']
for k, nm in enumerate(names):
    rep('<g onclick="xiSelect(%d)" pointer-events="bounding-box" style="cursor:pointer">' % k,
        '<g class="xi-node" data-idx="%d" tabindex="0" role="button" aria-label="%s. Open player card">' % (k, nm))
# drop duplicate inner hit-rect on Tavio
rep('\n              <rect x="208" y="143" width="44" height="68" fill="transparent"/>', '')
rep('<svg id="xiSvg" viewBox="0 0 460 580" preserveAspectRatio="xMidYMid meet">',
    '<svg id="xiSvg" viewBox="0 0 460 580" preserveAspectRatio="xMidYMid meet" role="group" aria-label="TNB Starting XI in a 4-3-3 formation. Each player opens a card.">')
rep('<p class="section-eyebrow xi-eyebrow-anim">', '<p class="section-eyebrow xi-eyebrow-anim">', 1)
rep('<h2 class="section-title xi-title-anim" id="starting-xi-h" style=', '<h2 class="section-title xi-title-anim view-title" id="starting-xi-h" tabindex="-1" style=')
rep('<div class="xi-ctrl-title">Click a <span>player</span></div>', '<div class="xi-ctrl-title">Hover, tap or tab to a <span>player</span></div>')
rep('<span class="xi-mkt-note">combined estimated squad value · 2026</span>', '<span class="xi-mkt-note">combined estimated squad value · Oct 2026</span>')
rep('<button class="xi-lines-btn on" id="xiLinesBtn" onclick="xiToggleLines()">Lines On</button>', '<button class="xi-lines-btn on" id="xiLinesBtn" type="button" aria-pressed="true" onclick="xiToggleLines()">Lines On</button>')
rep('<div class="xi-info-panel" id="xiInfoPanel">', '<div class="xi-info-panel" id="xiInfoPanel" aria-live="polite">')
rep('<div class="xi-footer-hint">Click any player node to view details</div>', '<div class="xi-footer-hint">Press Enter on a player to open their card · Esc to close · <a href="#players">See the stats table</a></div>')
rep('          <div class="xi-legend-item"><div class="xi-legend-dot pending"></div>Reviewing</div>\n', '')

rep('font-size="8.5" font-weight="900" letter-spacing="0.8">GRECO-TAYLOR<', 'font-size="7.6" font-weight="900" letter-spacing="0.4">GRECO-TAYLOR<')
rep('x="183" y="527" text-anchor="middle" fill="#fff" font-family="\'Barlow Condensed\',sans-serif" font-size="10" font-weight="900" letter-spacing="0.8">CAMPAGNA<', 'x="186" y="527" text-anchor="middle" fill="#fff" font-family="\'Barlow Condensed\',sans-serif" font-size="9.4" font-weight="900" letter-spacing="0.6">CAMPAGNA<')
# ---------- Culture: redacted svg text colour, hint text ----------
rep('font-size="24" fill="#fff" letter-spacing="3">████ ████████</text>', 'font-size="24" fill="#121212" letter-spacing="3">████ ████████</text>')
rep('<article class="ambassador-card-reveal" id="ambCard">', '<article class="ambassador-card-reveal" id="ambCard" tabindex="0" aria-label="Second ambassador, identity revealed soon. 110K plus combined reach.">')
rep('>Hover to scan</p>', '>Hover or focus to scan</p>')

# ---------- RECRUIT FORM ----------
i = s.index('<form name="recruit"'); j = s.index('</form>', i) + len('</form>')
s = s[:i] + '''<form name="recruit" method="POST" enctype="multipart/form-data" data-netlify="true" netlify-honeypot="bot-field" id="recruitForm" novalidate>
          <input type="hidden" name="form-name" value="recruit">
          <p class="visually-hidden"><label>Leave this field empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
          <div id="formStep1" class="form-step active" role="group" aria-labelledby="step1-title">
            <h3 class="form-title" id="step1-title">Player Profile <span class="step-indicator">STEP 1/2</span></h3>
            <div class="form-row">
              <div class="form-group"><label class="form-label" for="first-name">First Name *</label><input type="text" id="first-name" name="first-name" class="form-input" placeholder="Marcus" autocomplete="given-name" required></div>
              <div class="form-group"><label class="form-label" for="last-name">Last Name *</label><input type="text" id="last-name" name="last-name" class="form-input" placeholder="Thompson" autocomplete="family-name" required></div>
            </div>
            <div class="form-group"><label class="form-label" for="email">Email Address *</label><input type="email" id="email" name="email" class="form-input" placeholder="you@email.com" autocomplete="email" required></div>
            <div class="form-row">
              <div class="form-group"><label class="form-label" for="position">Position *</label>
                <select id="position" name="position" class="form-select" required>
                  <option value="">Select Position</option>
                  <option>Goalkeeper</option><option>Defender</option><option>Midfielder</option><option>Winger</option><option>Forward / Striker</option>
                </select>
              </div>
              <div class="form-group"><label class="form-label" for="club">Current Club</label><input type="text" id="club" name="club" class="form-input" placeholder="e.g. Brampton YSC" autocomplete="organization"></div>
            </div>
            <fieldset class="form-group">
              <legend class="form-label">Your Age *</legend>
              <div class="form-radio-row">
                <label><input type="radio" name="age-group" value="13-15" required> 13 to 15</label>
                <label><input type="radio" name="age-group" value="16-17"> 16 to 17</label>
                <label><input type="radio" name="age-group" value="18+"> 18 or older</label>
              </div>
            </fieldset>
            <div class="form-group" id="guardianWrap" hidden>
              <label class="form-label" for="guardian-email">Parent / Guardian Email *</label>
              <input type="email" id="guardian-email" name="guardian-email" class="form-input" placeholder="parent@email.com" aria-describedby="guardian-help">
              <p class="form-help" id="guardian-help">You're under 18, so we'll contact your parent or guardian before following up or publishing anything.</p>
            </div>
            <div class="form-group"><label class="form-label" for="about">Tell Us About Yourself *</label><textarea id="about" name="about" class="form-textarea" placeholder="Your level, achievements, what you're working towards..." required></textarea></div>
            <button type="button" class="btn-primary" onclick="nextFormStep()" style="width:100%;text-align:center">Next: Upload Footage →</button>
            <div class="form-error" id="step1Error" role="alert" hidden></div>
          </div>
          <div id="formStep2" class="form-step" role="group" aria-labelledby="step2-title">
            <h3 class="form-title" id="step2-title" tabindex="-1">The Tape <span class="step-indicator">STEP 2/2</span></h3>
            <p style="font-size:0.85rem;color:#3A3A3A;margin-bottom:15px;">Upload a short clip, or paste a link to your highlights. One of the two is required.</p>
            <div class="file-drop-zone" id="dropZone">
              <input type="file" id="raw-footage" name="raw-footage" accept="video/mp4,video/quicktime,.mp4,.mov" onchange="updateFileName(this)" aria-describedby="file-help">
              <div class="file-drop-icon" aria-hidden="true">📁</div>
              <div class="file-drop-text" id="fileText">Drag &amp; Drop MP4/MOV</div>
              <div class="file-drop-sub" id="file-help">Up to 8MB. For longer tape, paste a link below.</div>
            </div>
            <div class="form-group"><label class="form-label" for="footage-link">Or Paste a Link (YouTube / IG / TikTok / Drive / Hudl)</label><input type="url" id="footage-link" name="footage-link" class="form-input" placeholder="https://..." inputmode="url"></div>
            <div class="form-group"><label class="form-check"><input type="checkbox" id="consent" name="consent" value="yes" required> <span>I agree to the <a href="#privacy">Privacy Policy</a> and <a href="#terms">Terms</a>. TNB will ask me (and my parent or guardian if I'm under 18) before publishing my footage. *</span></label></div>
            <div style="display:flex;gap:10px;margin-top:20px;">
              <button type="button" class="btn-ghost" onclick="prevFormStep()" style="padding:13px 20px;">← Back</button>
              <button type="submit" class="btn-primary" id="submitBtn" style="flex:1;text-align:center">Submit Profile</button>
            </div>
            <div class="form-error" id="step2Error" role="alert" hidden></div>
            <div class="form-success" id="formSuccess" role="status" hidden></div>
            <p class="form-note">We review every submission personally. Fields marked * are required.</p>
          </div>
        </form>''' + s[j:]

# ---------- footer ----------
i = s.index('<div class="footer-col-title">Navigate</div>'); j = s.index('<div class="footer-col-title">Connect</div>')
col_end = s.rfind('<div>', 0, j)
s = s[:i] + '''<div class="footer-col-title">Navigate</div>
      <ul class="footer-links">
        <li><a href="#home">Home</a></li>
        <li><a href="#nine">The Players</a></li>
        <li><a href="#canada">Canada &amp; Legends</a></li>
        <li><a href="#book">Book a Shoot</a></li>
        <li><a href="#studios">Studios</a></li>
        <li><a href="#about">About</a></li>
      </ul>
    </div>
    <div>
      <div class="footer-col-title">Legal</div>
      <ul class="footer-links">
        <li><a href="#privacy">Privacy Policy</a></li>
        <li><a href="#terms">Terms of Use</a></li>
        <li><a href="#cookies">Cookies</a></li>
        <li><a href="#accessibility">Accessibility</a></li>
      </ul>
    </div>
    ''' + s[col_end:]
rep('<li><a href="#recruit">Get Scouted</a></li>\n      </ul>', '<li><a href="#scouted">Get Scouted</a></li>\n        <li><a href="mailto:contact@tnballers.com">Email Us</a></li>\n      </ul>')
rep('<p class="footer-copy">© 2026 True North Ballers · Brampton, Ontario · 🍁 Made in Canada</p>',
    '<p class="footer-copy">© 2026 True North Ballers · Brampton, Ontario, Canada · Independent media, not affiliated with the CPL or Canada Soccer</p>')
rep('<div class="timezone-bar" aria-label="Global office times">', '<div class="timezone-bar" aria-label="Local times">')

# ---------- assemble VIEWS inside main ----------
mi = s.index('<main>') + len('<main>'); me = s.index('</main>')
main = s[mi:me]
def take(start, end=None):
    global main
    i = main.index(start)
    j = main.index(end, i) if end else len(main)
    chunk = main[i:j]; main = main[:i] + main[j:]
    return chunk
hero_block = take('<section id="hero"', '<section id="pipeline"')
pipeline = take('<section id="pipeline"', '<div class="section-sep"')
culture = take('<section id="culture"', '<div class="section-sep"')
metrics = take('<section id="metrics"', '<!-- ══')
xi = take('<!-- ══', '<section id="social-metrics"')
social = take('<section id="social-metrics"', '<section id="media-engine"')
media = take('<section id="media-engine"', '<section id="recruit"')
recruit = take('<section id="recruit"')
SEP = '\n<div class="section-sep" aria-hidden="true"></div>\n'
views = ''
IGS, YTS = P('_ig.svg'), P('_yt.svg')
def sec(f, sfx, view_title, after=''):
    h = P(f).replace('{{SFX}}', sfx).replace('{{IG}}', IGS).replace('{{YT}}', YTS).replace('{{AFTER}}', after)
    return h.replace('{{TITLECLS}}', ' view-title' if view_title else '').replace('{{TITLEATTR}}', ' tabindex="-1"' if view_title else '')
TEASER = '<div class="leg-teaser"><p>Messi, Ronaldo, Müller, Sánchez: <span>the greats who\'ve played in Canada.</span></p><a href="#legends" class="btn-primary">See the legends</a></div>'
more = '<div class="nine-more"><a href="#nine" class="btn-primary">Full stats table</a><a href="#book" class="btn-ghost">Book a shoot</a></div>'
views += '\n<div class="view" data-view="home">\n' + hero_block + sec('sponsors.html','-home',False) + SEP + sec('nine_sec.html','-home',False,more) + SEP + P('feed.html') + SEP + P('services.html') + SEP + P('canada.html').replace('<p class="can-note">', TEASER + '<p class="can-note">',1) + SEP + metrics + '</div>\n'
views += '\n<div class="view" data-view="nine" hidden>\n' + sec('nine_sec.html','',True,P('nine_table.html')) + '</div>\n'
views += '\n<div class="view" data-view="canada" hidden>\n' + P('canada_view.html') + SEP + P('feed_view.html') + SEP + P('legends.html') + '</div>\n'
views += '\n<div class="view" data-view="book" hidden>\n' + P('book.html') + '</div>\n'
views += '\n<div class="view" data-view="studios" hidden>\n' + media + SEP + social + '</div>\n'
views += '\n<div class="view" data-view="scouted" hidden>\n' + recruit + '</div>\n'
la = P('about_legal.html')
for vid in ['about','privacy','terms','cookies','accessibility']:
    a = la.index('<section id="%s"' % vid); b = la.index('</section>', a) + len('</section>')
    views += '\n<div class="view" data-view="%s" hidden>\n' % vid + la[a:b] + '\n</div>\n'
s = s[:mi] + views + s[me:]
rep('<main>', '<main id="main-content" tabindex="-1">')

# view titles for focus
for hid in ['media-engine-h', 'recruit-h']:
    rep('class="section-title" id="%s"' % hid, 'class="section-title view-title" id="%s" tabindex="-1"' % hid)
rep('<h1 class="hero-headline">', '<h1 class="hero-headline view-title" tabindex="-1">')
rep('<section id="social-metrics" aria-label="Social Teaser">', '<section id="social-metrics" aria-label="Platforms">')

open('work2.html', 'w').write(s)
print('structure ok', len(s))
