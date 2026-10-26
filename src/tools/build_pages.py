#!/usr/bin/env python3
"""
Build the standalone pages: /about/, /scouted/, /submit/, /book/, /privacy/, /terms/, /cookies/, /accessibility/.
Each page shares the same topbar + theme-toggle + footer as the homepage.
Also writes site/404.html.
Preview-level implementation; the final build.sh will eventually fold this in.
"""
from pathlib import Path

STATS_ASOF = '26 Oct 2026'
EFFECTIVE  = '26 Oct 2026'

PAGES = {
    'about':        ('About', 'True North Ballers: an independent Canadian soccer platform built in Brampton.'),
    'scouted':      ('Get Scouted', 'How scouting works at TNB: upload a clip, we watch it, standouts may be shared with CPL and League1 coaches and scouts in our network. Free for players.'),
    'submit':       ('Submit your footage', 'Upload a reel or paste a link. Up to 8 MB on direct upload; longer videos go in as a link.'),
    'book':         ('Book a shoot', 'TNB videography: highlight reels, matchday coverage, training sessions, player profiles and campaigns.'),
    'privacy':      ('Privacy policy', 'How True North Ballers handles your personal data under PIPEDA.'),
    'terms':        ('Terms', 'Terms for using tnballers.com and for booking True North Ballers services.'),
    'cookies':      ('Cookies', 'What cookies tnballers.com sets, and what it does not.'),
    'accessibility':('Accessibility', 'TNB targets WCAG 2.1 AA. How to report accessibility issues.'),
}

NAV = '''<header class="topbar">
  <div class="wrap topbar-row">
    <a class="brand" href="/" aria-label="True North Ballers home">
      <img class="logo" src="/players/badge.png" alt="TNB crest">
      <span class="word">True North Ballers<small>Independent · Brampton</small></span>
    </a>
    <nav class="nav" aria-label="Primary">
      <a href="/#tracker"><span class="live-dot" aria-hidden="true"></span>Live</a>
      <a href="/#players">The Players</a>
      <a href="/#canada">Canada</a>
      <a href="/#services">What TNB does</a>
      <a href="/submit/">Get Scouted</a>
      <a href="/about/">About</a>
    </nav>
    <div class="topbar-right">
      <div class="social-row">
        <a href="https://instagram.com/tnballers" target="_blank" rel="noopener noreferrer" aria-label="TNB on Instagram"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.07 1.2.06 2 .25 2.5.42.6.24 1.1.5 1.6 1s.78 1 1 1.6c.2.5.4 1.3.4 2.5.1 1.2.1 1.6.1 4.8s0 3.6-.1 4.8c-.06 1.2-.25 2-.42 2.5-.24.6-.5 1.1-1 1.6s-1 .78-1.6 1c-.5.2-1.3.4-2.5.4-1.2.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.06-2-.25-2.5-.42-.6-.24-1.1-.5-1.6-1s-.78-1-1-1.6c-.2-.5-.4-1.3-.4-2.5-.1-1.2-.1-1.6-.1-4.8s0-3.6.1-4.8c.06-1.2.25-2 .42-2.5.24-.6.5-1.1 1-1.6s1-.78 1.6-1c.5-.2 1.3-.4 2.5-.4C8.4 2.2 8.8 2.2 12 2.2zm0 3.1a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 1.8a3.2 3.2 0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4zm5.4-2.1a1.2 1.2 0 1 1-2.4 0 1.2 1.2 0 0 1 2.4 0z"/></svg></a>
        <a href="https://www.tiktok.com/@truenorthballers" target="_blank" rel="noopener noreferrer" aria-label="TNB on TikTok"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M19.6 7.3a7 7 0 0 1-4.1-1.3 7 7 0 0 1-1.9-2V15a5.5 5.5 0 1 1-5.5-5.5c.3 0 .6 0 .9.1v2.9a2.6 2.6 0 1 0 1.8 2.5V2h2.9a4.5 4.5 0 0 0 4.6 4.4h1.3v2.9z"/></svg></a>
      </div>
      <button type="button" class="theme-toggle" id="themeToggle" aria-label="Switch theme" title="Switch theme">
        <svg class="moon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.5 14.5A9 9 0 1 1 9.5 2.5a7 7 0 0 0 12 12Z"/></svg>
        <svg class="sun" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10Zm0-5a1 1 0 0 1 1 1v2a1 1 0 1 1-2 0V3a1 1 0 0 1 1-1Zm0 17a1 1 0 0 1 1 1v2a1 1 0 1 1-2 0v-2a1 1 0 0 1 1-1ZM4.2 4.2a1 1 0 0 1 1.4 0l1.5 1.5a1 1 0 1 1-1.4 1.4L4.2 5.6a1 1 0 0 1 0-1.4Zm13.3 13.3a1 1 0 0 1 1.4 0l1.5 1.5a1 1 0 1 1-1.4 1.4l-1.5-1.5a1 1 0 0 1 0-1.4ZM2 12a1 1 0 0 1 1-1h2a1 1 0 1 1 0 2H3a1 1 0 0 1-1-1Zm17 0a1 1 0 0 1 1-1h2a1 1 0 1 1 0 2h-2a1 1 0 0 1-1-1ZM4.2 19.8a1 1 0 0 1 0-1.4l1.5-1.5a1 1 0 1 1 1.4 1.4l-1.5 1.5a1 1 0 0 1-1.4 0Zm13.3-13.3a1 1 0 0 1 0-1.4l1.5-1.5a1 1 0 1 1 1.4 1.4L19 6.5a1 1 0 0 1-1.5 0Z"/></svg>
      </button>
      <button type="button" class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false" aria-controls="navSheet">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16" stroke-linecap="round"/></svg>
      </button>
    </div>
  </div>
</header>
<div class="nav-sheet" id="navSheet" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="nav-sheet-inner">
    <button type="button" class="close" id="navClose" aria-label="Close menu">✕</button>
    <a href="/#tracker">Live</a>
    <a href="/#players">The Players</a>
    <a href="/#canada">Canada</a>
    <a href="/#services">What TNB does</a>
    <a href="/scouted/">Get Scouted</a>
    <a href="/submit/">Submit footage</a>
    <a href="/book/">Book a shoot</a>
    <a href="/about/">About</a>
  </div>
</div>'''

FOOTER = f'''<footer class="footer">
  <div class="wrap">
    <div class="footer-row">
      <div class="footer-brand">
        <img src="/players/badge.png" alt="TNB crest">
        <div>
          <div class="name">True North Ballers</div>
          <span class="sub">Brampton · Ontario · Canada</span>
        </div>
      </div>
      <nav class="footer-links" aria-label="Footer">
        <a href="/about/">About</a>
        <a href="/privacy/">Privacy</a>
        <a href="/terms/">Terms</a>
        <a href="/cookies/">Cookies</a>
        <a href="/accessibility/">Accessibility</a>
      </nav>
      <div class="footer-socials">
        <a href="https://instagram.com/tnballers" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.07 1.2.06 2 .25 2.5.42.6.24 1.1.5 1.6 1s.78 1 1 1.6c.2.5.4 1.3.4 2.5.1 1.2.1 1.6.1 4.8s0 3.6-.1 4.8c-.06 1.2-.25 2-.42 2.5-.24.6-.5 1.1-1 1.6s-1 .78-1.6 1c-.5.2-1.3.4-2.5.4-1.2.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.06-2-.25-2.5-.42-.6-.24-1.1-.5-1.6-1s-.78-1-1-1.6c-.2-.5-.4-1.3-.4-2.5-.1-1.2-.1-1.6-.1-4.8s0-3.6.1-4.8c.06-1.2.25-2 .42-2.5.24-.6.5-1.1 1-1.6s1-.78 1.6-1c.5-.2 1.3-.4 2.5-.4C8.4 2.2 8.8 2.2 12 2.2zm0 3.1a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 1.8a3.2 3.2 0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4zm5.4-2.1a1.2 1.2 0 1 1-2.4 0 1.2 1.2 0 0 1 2.4 0z"/></svg></a>
        <a href="https://www.tiktok.com/@truenorthballers" target="_blank" rel="noopener noreferrer" aria-label="TikTok"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M19.6 7.3a7 7 0 0 1-4.1-1.3 7 7 0 0 1-1.9-2V15a5.5 5.5 0 1 1-5.5-5.5c.3 0 .6 0 .9.1v2.9a2.6 2.6 0 1 0 1.8 2.5V2h2.9a4.5 4.5 0 0 0 4.6 4.4h1.3v2.9z"/></svg></a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 True North Ballers. Independent. Not affiliated with Canada Soccer or any club.</p>
      <p><a href="mailto:contact@tnballers.com">contact@tnballers.com</a> · <a href="mailto:contact@tnballers.com?subject=Data%20request">Request or delete my data</a></p>
    </div>
  </div>
</footer>'''

SHARED_CSS = '''
:root{
  --c-ink:#0b0b0b; --c-ink-2:#141414; --c-ink-3:#1f1f1f;
  --c-red:#CC0000; --c-gold:#C9A227; --c-gold-l:#F3D27A;
  --c-white:#ffffff; --c-dim:#c9c9c9; --c-muted:#9a9a9a; --c-faint:#6a6a6a;
  --c-border:rgba(255,255,255,.08); --c-border-s:rgba(255,255,255,.14);
  --f-display:'Tanker',Impact,sans-serif;
  --f-body:'Switzer',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
}
:root[data-theme="light"]{
  --c-ink:#F6F3EE; --c-ink-2:#ECE6DC; --c-ink-3:#DED3C1;
  --c-gold:#8A6B00; --c-gold-l:#C9A227;
  --c-white:#0b0b0b; --c-dim:#2a2a2a; --c-muted:#5a5a5a; --c-faint:#767676;
  --c-border:rgba(0,0,0,.10); --c-border-s:rgba(0,0,0,.20);
}
@font-face{font-family:'Tanker';src:url('/fonts/tanker/Tanker-Regular.woff2') format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:'Switzer';src:url('/fonts/switzer/Switzer-Regular.woff2') format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:'Switzer';src:url('/fonts/switzer/Switzer-Semibold.woff2') format('woff2');font-weight:600;font-display:swap}
@font-face{font-family:'Switzer';src:url('/fonts/switzer/Switzer-Bold.woff2') format('woff2');font-weight:700;font-display:swap}
*,*::before,*::after{box-sizing:border-box}
html,body{margin:0;padding:0;overflow-x:hidden}
body{background:var(--c-ink);color:var(--c-white);font-family:var(--f-body);font-weight:400;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,56px)}
a{color:inherit;text-decoration:none}
a:focus-visible,button:focus-visible{outline:2px solid var(--c-red);outline-offset:3px}
/* Topbar */
.topbar{position:sticky;top:0;z-index:60;background:var(--c-ink);border-bottom:1px solid var(--c-border)}
.topbar-row{display:flex;align-items:center;justify-content:space-between;gap:16px;height:68px}
.brand{display:flex;align-items:center;gap:12px}
.brand .logo{width:40px;height:40px;flex:none}
.brand .word{font-family:var(--f-body);font-weight:700;font-size:12px;letter-spacing:.28em;text-transform:uppercase;line-height:1.1;color:var(--c-white)}
.brand .word small{display:block;font-weight:400;font-size:10px;letter-spacing:.22em;color:var(--c-muted);margin-top:2px}
.nav{display:flex;gap:4px}
.nav a{font-family:var(--f-body);font-weight:600;font-size:12px;letter-spacing:.2em;text-transform:uppercase;padding:8px 12px;color:var(--c-dim);border-bottom:2px solid transparent;transition:color .18s,border-color .18s}
.nav a:hover{color:var(--c-white);border-color:var(--c-red)}
.nav .live-dot{display:inline-block;width:7px;height:7px;background:var(--c-red);border-radius:50%;margin-right:6px;vertical-align:1px}
.topbar-right{display:flex;align-items:center;gap:14px}
.social-row{display:flex;gap:4px}
.social-row a{width:36px;height:36px;display:inline-flex;align-items:center;justify-content:center;color:var(--c-dim);border:1px solid var(--c-border-s);border-radius:50%;transition:color .18s,border-color .18s,background .18s}
.social-row a:hover{color:#fff;border-color:var(--c-red);background:var(--c-red)}
@media (max-width:1200px){.nav{display:none}.nav-toggle{display:inline-flex}}
@media (max-width:900px){.social-row{display:none}.brand .word small{display:none}}
.nav a{white-space:nowrap}
.nav-toggle{all:unset;cursor:pointer;width:40px;height:40px;display:none;align-items:center;justify-content:center;border:1px solid var(--c-border-s);border-radius:50%;color:var(--c-white);transition:color .18s ease,border-color .18s ease}
.nav-toggle:hover,.nav-toggle:focus-visible{border-color:var(--c-red);color:var(--c-red)}
.nav-toggle svg{width:18px;height:18px}
.nav-sheet{position:fixed;inset:0;z-index:70;background:rgba(0,0,0,.78);display:none;justify-content:flex-end}
.nav-sheet[open]{display:flex}
.nav-sheet-inner{width:min(360px,86vw);height:100%;background:var(--c-ink);border-left:1px solid var(--c-border-s);padding:28px 24px;display:flex;flex-direction:column;gap:4px;overflow:auto}
.nav-sheet-inner .close{align-self:flex-end;all:unset;cursor:pointer;color:var(--c-dim);font-size:22px;padding:4px 10px;border:1px solid var(--c-border-s)}
.nav-sheet-inner .close:hover{color:#fff;border-color:var(--c-red)}
.nav-sheet-inner a{font-family:var(--f-body);font-weight:700;font-size:16px;letter-spacing:.14em;text-transform:uppercase;padding:14px 10px;color:var(--c-white);border-bottom:1px solid var(--c-border)}
.nav-sheet-inner a:hover,.nav-sheet-inner a:focus-visible{color:var(--c-red)}
.mobile-bar{position:fixed;left:0;right:0;bottom:0;z-index:55;display:none;grid-template-columns:1fr 1fr;background:#0b0b0b;border-top:1px solid var(--c-border-s)}
.mobile-bar a{all:unset;cursor:pointer;text-align:center;padding:14px 10px;font-family:var(--f-body);font-weight:700;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:#fff}
.mobile-bar a:first-child{border-right:1px solid var(--c-border-s)}
.mobile-bar a:hover,.mobile-bar a:focus-visible{background:var(--c-red)}
.mobile-bar .gold{color:var(--c-gold-l)}
@media (max-width:720px){.mobile-bar{display:grid}body{padding-bottom:60px}}
.theme-toggle{all:unset;cursor:pointer;width:36px;height:36px;display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--c-border-s);border-radius:50%;color:var(--c-dim);transition:color .18s,border-color .18s,background .18s}
.theme-toggle:hover,.theme-toggle:focus-visible{color:var(--c-white);border-color:var(--c-red)}
.theme-toggle svg{width:16px;height:16px}
.theme-toggle .sun{display:none}
.theme-toggle .moon{display:block}
:root[data-theme="light"] .theme-toggle .sun{display:block}
:root[data-theme="light"] .theme-toggle .moon{display:none}

/* Page body */
.page{padding:72px 0 56px}
.page .eyebrow{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--c-gold);font-weight:600;margin:0 0 10px}
.page h1{font-family:var(--f-display);font-size:clamp(44px,6vw,88px);line-height:.95;letter-spacing:-.005em;text-transform:uppercase;color:var(--c-white);margin:0 0 20px}
.page h2{font-family:var(--f-display);font-size:clamp(28px,3vw,40px);color:var(--c-white);margin:40px 0 12px;line-height:1}
.page h3{font-family:var(--f-body);font-weight:700;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--c-gold);margin:28px 0 10px}
.page p,.page ul,.page li{color:var(--c-dim);line-height:1.7;max-width:72ch}
.page ul{padding-left:22px}
.page code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--c-ink-2);padding:1px 6px;border-radius:3px;font-size:.9em;color:var(--c-gold-l)}
.page a{color:var(--c-gold);border-bottom:1px solid var(--c-border-s)}
.page a:hover{color:var(--c-red);border-color:var(--c-red)}
.page .asof{margin-top:40px;font-size:11px;color:var(--c-faint);letter-spacing:.08em;text-transform:uppercase}

/* Footer */
.footer{padding:48px 0 36px;background:var(--c-ink);border-top:1px solid var(--c-border)}
.footer-row{display:grid;grid-template-columns:1.3fr 2fr auto;gap:28px;align-items:start;padding-bottom:28px;border-bottom:1px solid var(--c-border)}
.footer-brand{display:flex;align-items:center;gap:14px}
.footer-brand img{width:46px;height:46px}
.footer-brand .name{font-family:var(--f-body);font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--c-white);font-size:13px}
.footer-brand .sub{font-size:11px;color:var(--c-muted);letter-spacing:.1em;text-transform:uppercase}
.footer-links{display:flex;gap:12px;flex-wrap:wrap}
.footer-links a{font-family:var(--f-body);font-weight:600;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--c-muted);padding:6px 10px;border:1px solid var(--c-border-s);border-radius:2px;transition:color .18s,border-color .18s}
.footer-links a:hover{color:var(--c-white);border-color:var(--c-red)}
.footer-socials{display:flex;gap:6px}
.footer-socials a{width:38px;height:38px;display:inline-flex;align-items:center;justify-content:center;color:var(--c-dim);border:1px solid var(--c-border-s);border-radius:50%;transition:color .18s,border-color .18s,background .18s}
.footer-socials a:hover{color:#fff;background:var(--c-red);border-color:var(--c-red)}
.footer-bottom{display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;padding-top:20px;font-size:12px;color:var(--c-muted)}
.footer-bottom a{color:var(--c-dim);border-bottom:1px solid var(--c-border-s)}
.footer-bottom a:hover{color:var(--c-white)}
@media (max-width:900px){.footer-row{grid-template-columns:1fr}.footer-links{gap:6px}}
'''

THEME_PRESCRIPT = '''<script>
(function(){try{var t=localStorage.getItem('tnb-theme');if(!t){t=window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';}document.documentElement.setAttribute('data-theme',t);var mc=document.querySelector('meta[name="theme-color"]');if(mc)mc.setAttribute('content',t==='light'?'#F6F3EE':'#0b0b0b');}catch(_){document.documentElement.setAttribute('data-theme','dark');}})();
</script>'''

FORMS_CSS = '''
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.form-group{display:flex;flex-direction:column;gap:6px}
.form-group.full{grid-column:1/-1}
.form-group label{font-family:var(--f-body);font-weight:700;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--c-dim)}
.form-group input,.form-group select,.form-group textarea{background:var(--c-ink-2);color:var(--c-white);border:1px solid var(--c-border-s);padding:12px 14px;font:inherit;border-radius:4px}
:root[data-theme="light"] .form-group input,:root[data-theme="light"] .form-group select,:root[data-theme="light"] .form-group textarea{background:#fff;color:#0b0b0b;border-color:rgba(0,0,0,.2)}
:root[data-theme="light"] .form-group label{color:#2a2a2a}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{outline:2px solid var(--c-red);outline-offset:2px}
.checks{display:flex;flex-wrap:wrap;gap:12px 16px}
.checks label{text-transform:none;letter-spacing:0;font-weight:400;font-size:14px;color:var(--c-white);display:inline-flex;align-items:center;gap:6px}
:root[data-theme="light"] .checks label{color:#0b0b0b}
.checks label input{accent-color:var(--c-red)}
.form-check{grid-column:1/-1;display:flex;gap:10px;align-items:flex-start;font-size:13px;color:var(--c-dim);line-height:1.5}
:root[data-theme="light"] .form-check label{color:#2a2a2a}
.btn-cta{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:8px;padding:14px 20px;background:var(--c-red);color:#fff;font-family:var(--f-body);font-weight:700;font-size:12px;letter-spacing:.22em;text-transform:uppercase;border-radius:4px;transition:background .18s ease,transform .18s ease}
.btn-cta:hover,.btn-cta:focus-visible{background:#e60000;transform:translateY(-1px)}
.btn-back{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:8px;padding:10px 14px;color:var(--c-dim);font-family:var(--f-body);font-weight:700;font-size:11px;letter-spacing:.22em;text-transform:uppercase;border:1px solid var(--c-border-s);border-radius:4px;margin-bottom:28px;transition:color .18s,border-color .18s}
.btn-back:hover,.btn-back:focus-visible{color:var(--c-white);border-color:var(--c-red)}
.file-input{position:relative}
.file-input input[type=file]{position:absolute;inset:0;opacity:0;cursor:pointer}
.file-input .fake{display:flex;align-items:center;gap:12px;padding:12px 14px;background:var(--c-ink-2);border:1px dashed var(--c-border-s);border-radius:4px}
.file-input .pick{margin-left:auto;padding:4px 10px;background:var(--c-red);color:#fff;border-radius:2px;font-size:10px;letter-spacing:.22em;text-transform:uppercase;font-weight:700}
@media (max-width:720px){.form-grid{grid-template-columns:1fr}}
'''

TOGGLE_SCRIPT = '''<script>
(function(){var b=document.getElementById('themeToggle');if(!b)return;var mc=document.querySelector('meta[name="theme-color"]');function cur(){return document.documentElement.getAttribute('data-theme')||'dark';}function set(t){document.documentElement.setAttribute('data-theme',t);if(mc)mc.setAttribute('content',t==='light'?'#F6F3EE':'#0b0b0b');b.setAttribute('aria-label',t==='light'?'Switch to dark theme':'Switch to light theme');try{localStorage.setItem('tnb-theme',t);}catch(_){}}b.addEventListener('click',function(){set(cur()==='light'?'dark':'light');});set(cur());})();
</script>'''

# Page content
CONTENT = {
    'scouted': '''
<a class="btn-back" href="/">← Back to home</a>
<p class="eyebrow">What TNB does · 01</p>
<h1>Get Scouted.</h1>
<p>Upload a clip. We watch it, write it up. Standouts may be shared with CPL and League1 coaches and scouts in our network. Free for players.</p>
<h2>How it works</h2>
<ul>
  <li><b>Upload or link.</b> Direct upload is capped at 8 MB. For longer games or reels, paste a link to YouTube, Instagram, TikTok, Google Drive or Hudl.</li>
  <li><b>We watch it.</b> One of our coaches sits with the footage. We don't just skim: we write it up with a scouting view, honest and specific.</li>
  <li><b>Decision.</b> If it's a standout, we may share your profile with coaches and scouts in our network at Canadian Premier League and League1 clubs. We'll ask you (and your parent or guardian if you're under 18) before sending anything.</li>
  <li><b>Free for players.</b> No fees. No agency contracts.</li>
</ul>
<h2>Who it's for</h2>
<ul>
  <li>Players aged 13 and up.</li>
  <li>Any position. Any level. Pitch us the footage you're proud of.</li>
</ul>
<p style="margin-top:36px"><a class="btn-cta" href="/submit/">Submit your footage <span class="arrow">→</span></a></p>
<p class="asof">Last updated: {EFFECTIVE}.</p>
''',

    'submit': '''
<a class="btn-back" href="/">← Back to home</a>
<p class="eyebrow">What TNB does · 02</p>
<h1>Submit your footage.</h1>
<p>Upload a reel or paste a link. We'll reply after we have watched it. If you're under 18 we'll also ask your parent or guardian before sharing or publishing anything.</p>

<form class="scout-form" name="recruit" method="POST" enctype="multipart/form-data" data-netlify="true" netlify-honeypot="bot-field" id="recruitForm" novalidate action="/submit/">
  <input type="hidden" name="form-name" value="recruit">
  <p class="visually-hidden" style="position:absolute;left:-9999px"><label>Leave this field empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>

  <h2>Your details</h2>
  <div class="form-grid">
    <div class="form-group"><label for="first-name">First name *</label><input type="text" id="first-name" name="first-name" placeholder="Marcus" autocomplete="given-name" required></div>
    <div class="form-group"><label for="last-name">Last name *</label><input type="text" id="last-name" name="last-name" placeholder="Thompson" autocomplete="family-name" required></div>
    <div class="form-group full"><label for="email">Email *</label><input type="email" id="email" name="email" placeholder="you@email.com" autocomplete="email" required></div>
    <div class="form-group"><label for="position">Position *</label><select id="position" name="position" required>
      <option value="">Choose</option>
      <option>Goalkeeper</option><option>Centre-back</option><option>Full-back / Wing-back</option><option>Defensive midfield</option><option>Central midfield</option><option>Attacking midfield</option><option>Winger</option><option>Striker</option>
    </select></div>
    <div class="form-group"><label for="club">Current club</label><input type="text" id="club" name="club" placeholder="e.g. Brampton YSC" autocomplete="organization"></div>
    <div class="form-group full">
      <label>Age group *</label>
      <div class="checks" role="radiogroup">
        <label><input type="radio" name="age-group" value="13-15" required> 13 to 15</label>
        <label><input type="radio" name="age-group" value="16-17"> 16 to 17</label>
        <label><input type="radio" name="age-group" value="18+"> 18 or older</label>
      </div>
    </div>
    <div class="form-group full" id="guardian-wrap" hidden>
      <label for="guardian-email">Parent or guardian email</label>
      <input type="email" id="guardian-email" name="guardian-email" placeholder="parent@email.com">
      <p style="font-size:12px;color:var(--c-muted);margin:4px 0 0">We'll ask them before anything is published.</p>
    </div>
  </div>

  <h2>The footage</h2>
  <div class="form-grid">
    <div class="form-group full"><label for="about">Tell us about yourself *</label><textarea id="about" name="about" rows="4" placeholder="Your level, achievements, what you're working towards..." required></textarea></div>
    <div class="form-group full">
      <label for="raw-footage">Upload footage</label>
      <div class="file-input">
        <div class="fake"><span id="file-name">No file chosen</span><span class="pick">Choose file</span></div>
        <input type="file" id="raw-footage" name="raw-footage" accept="video/mp4,video/quicktime,.mp4,.mov">
      </div>
      <p style="font-size:12px;color:var(--c-muted);margin:4px 0 0">Up to <b>8 MB</b>. For longer videos, paste a link below.</p>
    </div>
    <div class="form-group full"><label for="footage-link">Or paste a link</label><input type="url" id="footage-link" name="footage-link" placeholder="YouTube / IG / TikTok / Drive / Hudl" inputmode="url"></div>
    <div class="form-check full">
      <input type="checkbox" id="consent" name="consent" value="yes" required>
      <label for="consent">I agree to the <a href="/privacy/">Privacy Policy</a> and <a href="/terms/">Terms</a>. TNB will ask me (and my parent or guardian if I'm under 18) before publishing my footage. *</label>
    </div>
    <div class="form-group full"><button type="submit" class="btn-cta">Submit <span class="arrow">→</span></button></div>
  </div>
</form>
<p class="asof">Last updated: {EFFECTIVE}.</p>
''',

    'book': '''
<a class="btn-back" href="/">← Back to home</a>
<p class="eyebrow">What TNB does · 03</p>
<h1>Book a shoot.</h1>
<p>Highlight reels, matchday coverage, training sessions, player profiles and campaigns. Delivered as feed, story and reel. 50% deposit books the date. See the <a href="/terms/">bookings terms</a>.</p>

<form class="book-form" name="booking" method="POST" data-netlify="true" netlify-honeypot="bot-field" id="bookForm" novalidate action="/book/">
  <input type="hidden" name="form-name" value="booking">
  <p class="visually-hidden" style="position:absolute;left:-9999px"><label>Leave this field empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>

  <div class="form-grid">
    <div class="form-group"><label for="b-name">Your name *</label><input type="text" id="b-name" name="name" autocomplete="name" required></div>
    <div class="form-group"><label for="b-email">Email *</label><input type="email" id="b-email" name="email" autocomplete="email" required></div>
    <div class="form-group"><label for="b-phone">Phone</label><input type="tel" id="b-phone" name="phone" autocomplete="tel" placeholder="Optional"></div>
    <div class="form-group"><label for="b-who">Who's booking? *</label><select id="b-who" name="who" required>
      <option value="">Choose one</option>
      <option>Player</option><option>Parent/guardian</option><option>Club</option><option>Brand</option><option>Other</option>
    </select></div>
    <div class="form-group full"><label>What do you need? (tick any)</label>
      <div class="checks">
        <label><input type="checkbox" name="service" value="Highlight reel"> Highlight reel</label>
        <label><input type="checkbox" name="service" value="Matchday coverage"> Matchday coverage</label>
        <label><input type="checkbox" name="service" value="Training session"> Training session</label>
        <label><input type="checkbox" name="service" value="Player profile"> Player profile</label>
        <label><input type="checkbox" name="service" value="Brand or club campaign"> Brand / club campaign</label>
        <label><input type="checkbox" name="service" value="Other"> Something else</label>
      </div>
    </div>
    <div class="form-group"><label for="b-date">Preferred date</label><input type="date" id="b-date" name="date"></div>
    <div class="form-group"><label for="b-loc">Location *</label><input type="text" id="b-loc" name="location" placeholder="City or venue" required></div>
    <div class="form-group full"><label for="b-budget">Rough budget (CAD)</label><select id="b-budget" name="budget">
      <option value="">Pick a range</option>
      <option>Under $500</option><option>$500 to $1,500</option><option>$1,500 to $5,000</option><option>$5,000+</option><option>Let's discuss</option>
    </select></div>
    <div class="form-group full"><label for="b-details">Tell us about it *</label><textarea id="b-details" name="details" rows="4" placeholder="Who's being filmed, the occasion, how you'll use the video..." required></textarea></div>
    <div class="form-check full">
      <input type="checkbox" id="b-consent" name="consent" value="yes" required>
      <label for="b-consent">I agree to the <a href="/privacy/">Privacy Policy</a>, the <a href="/terms/">bookings terms</a>, and (if anyone under 18 is being filmed) that a parent or guardian will approve. *</label>
    </div>
    <div class="form-group full"><button type="submit" class="btn-cta">Send booking <span class="arrow">→</span></button></div>
  </div>
</form>

<script>
(function(){
  var age = document.getElementsByName('age-group');
  var w = document.getElementById('guardian-wrap');
  Array.prototype.forEach.call(age, function(r){ r.addEventListener('change', function(){
    var u18 = (r.value === '13-15' || r.value === '16-17') && r.checked;
    if(w) w.hidden = !u18;
  })});
  var f = document.getElementById('raw-footage'), fn = document.getElementById('file-name');
  if(f && fn) f.addEventListener('change', function(){
    var x = f.files && f.files[0];
    if(!x) return fn.textContent = 'No file chosen';
    var mb = Math.round(x.size/1024/1024*10)/10;
    fn.textContent = x.size > 8*1024*1024 ? (x.name + ' . too large (' + mb + ' MB). Paste a link below.') : (x.name + ' . ' + mb + ' MB');
  });
})();
</script>
<p class="asof">Last updated: {EFFECTIVE}.</p>
''',

    'about': '''
<p class="eyebrow">About TNB</p>
<h1>Independent. Built in Brampton.</h1>
<p>True North Ballers is an independent Canadian soccer platform. We cover eight partner players day by day, track Canada's best in Europe and the MLS, and film what Canadian clubs and families need: match tapes, highlight reels, and short videos that make a scout stop scrolling.</p>
<h2>What we do</h2>
<ul>
  <li><b>Scouting coverage.</b> Live stats, match reports, injury notes and transfer calls for our eight partner players.</li>
  <li><b>Canada's standard.</b> A ranked list of Canada's in-form players right now, plus a running sidelined list.</li>
  <li><b>Videography.</b> Game-day filming, highlight packages, and short-form content made for Instagram and TikTok.</li>
  <li><b>Instagram and TikTok.</b> Short, verified posts on <a href="https://instagram.com/tnballers" target="_blank" rel="noopener noreferrer">@tnballers</a> and <a href="https://www.tiktok.com/@truenorthballers" target="_blank" rel="noopener noreferrer">@truenorthballers</a>. Every post is reviewed before it goes out.</li>
</ul>
<h2>What we don't do</h2>
<ul>
  <li>Agency-style player representation. We are media and video, not an agent.</li>
  <li>Analytics, trackers or ad cookies. See <a href="/cookies/">Cookies</a>.</li>
  <li>Rumours. See <a href="/terms/">Terms</a>: TNB posts facts only.</li>
</ul>
<h2>Contact</h2>
<p><a href="mailto:contact@tnballers.com">contact@tnballers.com</a>. Based in Brampton, Ontario, Canada.</p>
<p class="asof">Last updated: {EFFECTIVE}.</p>
''',

    'privacy': '''
<p class="eyebrow">Legal</p>
<h1>Privacy policy.</h1>
<p>True North Ballers (TNB) is a Canadian independent publication based in Brampton, Ontario. We follow PIPEDA (the Personal Information Protection and Electronic Documents Act).</p>
<h2>What we collect</h2>
<ul>
  <li><b>Only what you give us.</b> On the booking form and the "Get Scouted" form, we collect your name, email, and whatever you type in the message / about / position fields. If you upload footage, we hold the file. If you paste a footage link, we hold the link.</li>
  <li><b>Netlify log data.</b> Our host (Netlify) keeps standard access logs with IP address and user-agent for security. Those logs are retained by Netlify under their policy.</li>
  <li><b>No analytics.</b> We don't use Google Analytics, Facebook Pixel, Hotjar, or any similar tracker.</li>
</ul>
<h2>What we don't do</h2>
<ul>
  <li>We don't sell or share your data with advertisers or data brokers.</li>
  <li>We don't fetch third-party fonts or scripts. Everything is self-hosted, so your IP doesn't leak to a font or script CDN.</li>
  <li>We don't profile you.</li>
</ul>
<h2>Form protection</h2>
<p>Our forms use a honeypot field (<code>bot-field</code>) rather than a Captcha. We don't send your IP or form data to a third-party anti-bot service.</p>
<h2>Your rights</h2>
<p>Under PIPEDA you can ask for a copy of the data we hold on you, or ask us to delete it. Email <a href="mailto:contact@tnballers.com?subject=Data%20request">contact@tnballers.com</a> and we'll respond within 30 days.</p>
<p class="asof">Effective: {EFFECTIVE}.</p>
''',

    'terms': '''
<p class="eyebrow">Legal</p>
<h1>Terms.</h1>
<h2>Bookings, payment and cancellations</h2>
<ul>
  <li>A 50% deposit books the date. The balance is due on delivery.</li>
  <li>Full refund if you cancel 7 or more days before the shoot.</li>
  <li>If you cancel inside 7 days, we keep the deposit to cover planning and lost dates.</li>
  <li>Free reschedule if the game is moved, or if the weather makes the shoot unsafe.</li>
  <li>Two rounds of edits are included in every edit package. Extra rounds are billed at our day rate.</li>
</ul>
<h2>Stats, ratings and photos</h2>
<ul>
  <li>Season stats come from FotMob and the clubs' own announcements, cross-checked by us. If a number can't be confirmed in two sources, we leave the old one and say so.</li>
  <li><b>TNB scout ratings (the FIN, PAC, DRI numbers on the FUT cards) are our editorial opinion, not an official data product.</b> They're based on footage we have watched and the writer's judgement. Don't use them as recruiting or valuation data.</li>
  <li>Photos are either supplied by partner players, licensed from the player's own channels, or sourced from Wikimedia Commons under a free licence with credit. We never use agency-watermarked photos.</li>
</ul>
<h2>Social posts and collaborator tags</h2>
<ul>
  <li>Every Instagram post is reviewed by TNB before it goes out. We don't auto-publish.</li>
  <li>For posts about a partner player, we add that player as an Instagram collaborator using the handle they confirmed with us.</li>
  <li>Live-mode posts are only enabled when Baller sends an explicit "live" message for a specific game. There is a cap of six posts per game, and goals are confirmed from two live sources (we wait out VAR).</li>
</ul>
<h2>Content and liability</h2>
<p>Content on tnballers.com is editorial, not advice. We don't guarantee that stats, transfer notes or injury dates are up to date at the moment you read them. We correct errors as fast as we can; email <a href="mailto:contact@tnballers.com">contact@tnballers.com</a> to report one.</p>
<p>TNB isn't affiliated with Canada Soccer, any club, or any player. Logos, names and trademarks belong to their owners.</p>
<p class="asof">Effective: {EFFECTIVE}.</p>
''',

    'cookies': '''
<p class="eyebrow">Legal</p>
<h1>Cookies.</h1>
<h2>What we set</h2>
<ul>
  <li><b>No tracking cookies.</b> No analytics cookie, no advertising cookie, no social-media pixel.</li>
  <li><b>Netlify session cookie.</b> When you submit a form, our host (Netlify) sets a small session cookie so it can show the thank-you page and block spam. It doesn't carry user tracking data.</li>
  <li><b>Local storage.</b> Your theme choice (dark or light) is saved in <code>localStorage</code> under the key <code>tnb-theme</code>. That's it. No personal data goes into local storage. You can clear it from your browser at any time.</li>
</ul>
<h2>What we don't set</h2>
<ul>
  <li>No third-party cookies. No cross-site tracking.</li>
  <li>No fonts or scripts loaded from a CDN; everything is served from tnballers.com.</li>
  <li>No consent banner, because there's nothing to consent to.</li>
</ul>
<p class="asof">Effective: {EFFECTIVE}.</p>
''',

    'accessibility': '''
<p class="eyebrow">Legal</p>
<h1>Accessibility.</h1>
<p>We target WCAG 2.1 AA on tnballers.com, in both the dark and light themes.</p>
<h2>What that means in practice</h2>
<ul>
  <li>Body-text contrast is 4.5:1 or higher against its background, in both themes.</li>
  <li>Every interactive element is keyboard-reachable with a visible focus ring.</li>
  <li>Images have alt text. Decorative icons are marked <code>aria-hidden="true"</code>.</li>
  <li>Animations and the live ticker respect your system's "Reduce motion" preference and switch to a static layout when it is on.</li>
  <li>Player cards and profile pop-ups are reachable by Tab, open on Enter and Space, close on Escape, and move between players with the Left and Right arrow keys.</li>
  <li>Forms have proper labels, visible focus states, and don't rely on colour alone to signal state.</li>
  <li>The theme toggle lives in the top bar; it also respects your system <code>prefers-color-scheme</code> on first visit.</li>
</ul>
<h2>Report a problem</h2>
<p>If any part of the site is hard to use with your assistive tech, email <a href="mailto:contact@tnballers.com?subject=Accessibility">contact@tnballers.com</a> and we'll fix it.</p>
<p class="asof">Effective: {EFFECTIVE}.</p>
''',
}

def page_html(slug, title, desc, body_html):
    og_image = 'https://tnballers.com/players/badge.png'
    return f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} · True North Ballers</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0b0b0b">
<link rel="icon" href="/players/badge.png" type="image/png">
<link rel="canonical" href="https://tnballers.com/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="True North Ballers">
<meta property="og:title" content="{title} · True North Ballers">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://tnballers.com/{slug}/">
<meta property="og:image" content="{og_image}">
<meta property="og:image:alt" content="True North Ballers crest">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} · True North Ballers">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<link rel="preload" as="font" type="font/woff2" href="/fonts/tanker/Tanker-Regular.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/fonts/switzer/Switzer-Regular.woff2" crossorigin>
{THEME_PRESCRIPT}
<style>{SHARED_CSS}{FORMS_CSS}</style>
</head>
<body>
{NAV}
<main class="page">
  <div class="wrap">
{body_html.strip()}
  </div>
</main>
{FOOTER}
<nav class="mobile-bar" aria-label="Quick actions"><a href="/submit/">Get Scouted</a><a class="gold" href="/book/">Book a shoot</a></nav>
{TOGGLE_SCRIPT}
<script>
// Mobile bar + sheet nav + view transitions (shared with homepage behaviour)
(function(){{var b=document.getElementById('navToggle'),s=document.getElementById('navSheet'),c=document.getElementById('navClose');if(!b)return;function o(){{s.setAttribute('open','true');b.setAttribute('aria-expanded','true');}}function sh(){{s.removeAttribute('open');b.setAttribute('aria-expanded','false');}}b.addEventListener('click',o);c&&c.addEventListener('click',sh);s.addEventListener('click',function(e){{if(e.target===s)sh();}});s.querySelectorAll('a').forEach(function(a){{a.addEventListener('click',sh)}});document.addEventListener('keydown',function(e){{if(s.hasAttribute('open')&&e.key==='Escape'){{e.preventDefault();sh();}}}});}})();
(function(){{if(!document.startViewTransition)return;document.addEventListener('click',function(e){{var a=e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href');if(!h||h.startsWith('#')||h.startsWith('mailto:')||a.target==='_blank'||a.hasAttribute('download'))return;var u;try{{u=new URL(h,window.location.href);}}catch(_){{return;}}if(u.origin!==window.location.origin)return;e.preventDefault();document.startViewTransition(function(){{window.location.href=u.href;}});}});}})();
</script>
</body>
</html>
'''

for slug, (title, desc) in PAGES.items():
    body = CONTENT[slug].replace('{EFFECTIVE}', EFFECTIVE)
    html = page_html(slug, title, desc, body)
    out = Path(f'site/{slug}/index.html')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f'wrote {out}  ({len(html)} chars)')

# Branded 404
_404 = '''
<a class="btn-back" href="/">← Back to home</a>
<p class="eyebrow">404</p>
<h1>Wrong pitch.</h1>
<p>That page doesn't exist, or it moved to its own address. Try one of these:</p>
<ul>
  <li><a href="/">Home</a>: live tracker, the eight, Canada's best.</li>
  <li><a href="/scouted/">Get Scouted</a>: how we review footage.</li>
  <li><a href="/book/">Book a shoot</a>: videography and matchday.</li>
  <li><a href="/about/">About</a>, <a href="/privacy/">Privacy</a>, <a href="/terms/">Terms</a>.</li>
</ul>
'''
html_404 = page_html('404', 'Not found', 'That page does not exist. Head back to the TNB home.', _404.strip())
# 404 lives at site/404.html, not site/404/index.html
Path('site/404.html').write_text(html_404.replace('canonical" href="https://tnballers.com/404/"','canonical" href="https://tnballers.com/"'), encoding='utf-8')
print('wrote site/404.html')

print('done.')
