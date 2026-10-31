#!/usr/bin/env python3
"""TNB goal breakdown edit: turn a short goal clip into a 9:16 commentary Reel / TikTok.

Built to sit inside fair dealing for news reporting and criticism/review (Canada Copyright Act
s.29.1/29.2, UK CDPA s.30): a SHORT excerpt of the goal (default max 12 s), substantial TNB
commentary on top (breakdown cards, freeze-frame with analysis, slow-motion replay), the source
credited on screen and in the caption, and a TNB end card. It is not a substitute for the
broadcaster's highlights. This is a risk-reduction approach, not legal advice: platforms can
still mute or remove clips on a rights-holder claim.

Usage:
  python3 src/tools/goal_edit.py clip.mp4 out.mp4 --start 3.2 --end 11 \
      --player "Kaylee Hunter" --minute "66'" --match "AFC Toronto 4–2 Ottawa Rapid" \
      --comp "NSL semi-final · 1st leg" --source "CBC Sports / NSL" \
      --freeze 7.4 --take "Near-post run, first touch across her body, finish before the keeper sets." \
      [--slowmo 6.5-8.5] [--endcard hero.jpg] [--music track.mp3]

Layout: 1080x1920. The clip sits in the middle (blurred copy fills the frame), a TNB header on
top (player, minute, match), a credit line under the clip, a freeze-frame with a gold ring
and the TNB "take" card, then a slow-motion replay of the finish and the hero end card.
Needs ffmpeg, Pillow and the self-hosted fonts in site/fonts (via Playwright for text cards).
"""
import argparse, pathlib, shutil, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
FONTS = ROOT / 'site' / 'fonts'


def run(*a):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *a], check=True)


def card_png(path, w, h, html_body, css=''):
    """Render a transparent overlay PNG with Playwright (Tanker + Switzer)."""
    from playwright.sync_api import sync_playwright
    page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Tanker;src:url({(FONTS/'tanker/Tanker-Regular.woff2').as_uri()})}}
@font-face{{font-family:Switzer;src:url({(FONTS/'switzer/Switzer-Bold.woff2').as_uri()});font-weight:700}}
@font-face{{font-family:Switzer;src:url({(FONTS/'switzer/Switzer-Semibold.woff2').as_uri()});font-weight:600}}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{w}px;height:{h}px;background:transparent;overflow:hidden;font-family:Switzer;color:#fff}}
{css}</style></head><body>{html_body}</body></html>'''
    tmp = pathlib.Path(tempfile.mkdtemp()); f = tmp / 'c.html'; f.write_text(page, encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': w, 'height': h})
        pg.goto(f.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
        pg.screenshot(path=str(path), omit_background=True); b.close()
    shutil.rmtree(tmp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('clip'); ap.add_argument('out')
    ap.add_argument('--start', type=float, default=0); ap.add_argument('--end', type=float)
    ap.add_argument('--max-len', type=float, default=12)
    ap.add_argument('--player', required=True); ap.add_argument('--minute', default='')
    ap.add_argument('--match', required=True); ap.add_argument('--comp', default='')
    ap.add_argument('--source', required=True, help='credit shown on screen, e.g. "OneSoccer / CPL"')
    ap.add_argument('--freeze', type=float, help='time (in the original clip) to freeze for the breakdown')
    ap.add_argument('--freeze-secs', type=float, default=2.6)
    ap.add_argument('--take', default='', help='TNB analysis line shown on the freeze-frame')
    ap.add_argument('--slowmo', help='replay window in the original clip, e.g. 6.5-8.5 (played at 0.4x)')
    ap.add_argument('--endcard', help='hero JPG/PNG (1080x1350) shown for the last 2.5 s')
    ap.add_argument('--music', help='licensed/royalty-free track to lay under (original audio is ducked)')
    a = ap.parse_args()

    end = a.end if a.end is not None else a.start + a.max_len
    end = min(end, a.start + a.max_len)
    t = pathlib.Path(tempfile.mkdtemp())

    # overlays
    first, _, last = a.player.partition(' ')
    card_png(t / 'top.png', 1080, 420, f'''
<div style="position:absolute;left:56px;top:110px">
 <div style="font-weight:700;font-size:24px;letter-spacing:.3em;color:#f0c255">⚽ GOAL {a.minute} · {a.comp.upper()}</div>
 <div style="font-family:Tanker;font-size:120px;line-height:.86;margin-top:12px;text-transform:uppercase;text-shadow:0 8px 30px rgba(0,0,0,.8)">
  <span style="color:transparent;-webkit-text-stroke:2.5px #fff">{first}</span> {last}</div>
 <div style="font-weight:700;font-size:28px;letter-spacing:.12em;margin-top:14px;text-shadow:0 2px 12px #000">{a.match.upper()}</div>
</div>''')
    card_png(t / 'credit.png', 1080, 200, f'''
<div style="position:absolute;left:56px;right:56px;top:20px;display:flex;justify-content:space-between;align-items:center;
 border-top:2px solid rgba(240,194,85,.7);padding-top:14px">
 <span style="font-weight:600;font-size:20px;color:#cfcfcf">🎥 Clip: {a.source} · TNB breakdown</span>
 <span style="font-weight:700;font-size:22px;letter-spacing:.24em">TNBALLERS.COM</span></div>''')
    if a.take:
        card_png(t / 'take.png', 1080, 520, f'''
<div style="position:absolute;left:56px;right:56px;bottom:40px;background:rgba(8,8,9,.86);border-left:8px solid #d40f1f;padding:26px 30px">
 <div style="font-weight:700;font-size:22px;letter-spacing:.3em;color:#f0c255">TNB BREAKDOWN</div>
 <div style="font-weight:700;font-size:40px;line-height:1.25;margin-top:12px">{a.take}</div></div>''')

    def framed(src, dst, extra_vf=''):
        # clip centred at 1080 wide, blurred copy fills 1080x1920, header + credit on top
        vf = ('[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.25[bg];'
              f'[0:v]scale=1080:-2{extra_vf}[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[v1];'
              '[v1][1:v]overlay=0:0[v2];[v2][2:v]overlay=0:1640[v]')
        run('-i', str(src), '-i', str(t / 'top.png'), '-i', str(t / 'credit.png'), '-filter_complex', vf,
            '-map', '[v]', '-map', '0:a?', '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
            '-c:a', 'aac', '-ar', '44100', '-ac', '2', str(dst))

    parts = []
    # 1) the goal (short excerpt)
    run('-ss', str(a.start), '-to', str(end), '-i', a.clip, '-c:v', 'libx264', '-c:a', 'aac', '-ar', '44100', '-ac', '2', str(t / 'cut.mp4'))
    framed(t / 'cut.mp4', t / 'p1.mp4'); parts.append(t / 'p1.mp4')
    # 2) freeze-frame breakdown
    if a.freeze is not None:
        run('-ss', str(a.freeze), '-i', a.clip, '-frames:v', '1', str(t / 'f.png'))
        run('-loop', '1', '-t', str(a.freeze_secs), '-i', str(t / 'f.png'), '-f', 'lavfi', '-t', str(a.freeze_secs),
            '-i', 'anullsrc=r=44100:cl=stereo', '-vf', "zoompan=z='min(zoom+0.0025,1.18)':d=1:s=1920x1080:fps=30,scale=1920:-2",
            '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', str(t / 'fr.mp4'))
        framed(t / 'fr.mp4', t / 'p2a.mp4')
        if a.take:
            run('-i', str(t / 'p2a.mp4'), '-i', str(t / 'take.png'), '-filter_complex', '[0:v][1:v]overlay=0:1100[v]',
                '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'copy', str(t / 'p2.mp4'))
        else:
            shutil.copy(t / 'p2a.mp4', t / 'p2.mp4')
        parts.append(t / 'p2.mp4')
    # 3) slow-motion replay
    if a.slowmo:
        s0, s1 = (float(x) for x in a.slowmo.split('-'))
        run('-ss', str(s0), '-to', str(s1), '-i', a.clip, '-vf', 'setpts=2.5*PTS,minterpolate=fps=30', '-af', 'atempo=0.5,atempo=0.8',
            '-c:v', 'libx264', '-c:a', 'aac', '-ar', '44100', '-ac', '2', str(t / 'sm.mp4'))
        framed(t / 'sm.mp4', t / 'p3.mp4'); parts.append(t / 'p3.mp4')
    # 4) end card
    if a.endcard:
        run('-loop', '1', '-t', '2.5', '-i', a.endcard, '-f', 'lavfi', '-t', '2.5', '-i', 'anullsrc=r=44100:cl=stereo',
            '-vf', 'scale=1080:1350,pad=1080:1920:0:285:color=0x070708,fps=30', '-shortest', '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p', '-c:a', 'aac', str(t / 'p4.mp4'))
        parts.append(t / 'p4.mp4')

    lst = t / 'list.txt'; lst.write_text(''.join(f"file '{p}'\n" for p in parts))
    run('-f', 'concat', '-safe', '0', '-i', str(lst), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-c:a', 'aac', str(t / 'joined.mp4'))
    if a.music:
        run('-i', str(t / 'joined.mp4'), '-i', a.music, '-filter_complex',
            '[0:a]volume=0.35[o];[1:a]volume=0.9[m];[o][m]amix=inputs=2:duration=first[a]',
            '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', a.out)
    else:
        run('-i', str(t / 'joined.mp4'), '-c', 'copy', '-movflags', '+faststart', a.out)
    shutil.rmtree(t)
    print('wrote', a.out)


if __name__ == '__main__':
    main()
