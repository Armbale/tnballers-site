import sys,pathlib
from playwright.sync_api import sync_playwright
D=pathlib.Path(__file__).resolve().parent;R=pathlib.Path('/home/claude/tnballers-site')
html=(D/sys.argv[1]).read_text().replace('FONTS/',(R/'site/fonts').as_uri()+'/').replace("'IMG/'",repr((D/'img').as_uri()+'/')).replace('src="hall.js"','src="'+(D/'hall.js').as_uri()+'"')
(D/'_b.html').write_text(html)
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page(viewport={'width':1080,'height':int(sys.argv[3])});pg.goto((D/'_b.html').as_uri());pg.evaluate('document.fonts.ready');pg.wait_for_timeout(800)
  pg.screenshot(path=sys.argv[2],type='jpeg',quality=93);b.close()
