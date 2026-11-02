#!/usr/bin/env python3
"""TNB clip edit: turn an interview / presser / club clip into a 9:16 commentary Reel / TikTok.

The format other football accounts use (a short quote, big hook title, word captions), with TNB
commentary added so it stays on the fair-dealing side (news reporting, criticism and review:
Canada Copyright Act s.29.1/29.2, UK CDPA s.30): a SHORT excerpt (default max 30 s), the source
credited on screen and in the caption, and a TNB take card at the end. Not legal advice and not a
licence: rights holders can still claim, mute or remove. Never feed it a full interview or a
highlights package, never crop out a watermark or logo.

Usage:
  python3 src/tools/interview_edit.py clip.mp4 out.mp4 --start 12 --end 34 \
      --hook "DAVIES ON FACING JONATHAN DAVID" --speaker "Alphonso Davies" --role "Bayern Munich · Canada" \
      --source "FC Bayern TV" --take "Two Canadians, one Champions League night. Who wins it?" \
      [--captions captions.srt | --lines "0-3.2|First line" "3.2-6|Second line"] [--cover hero.jpg]

Caption times are relative to --start. Without captions the edit still works (hook + lower third).
Output: 1080x1920 H.264 + AAC, original audio kept. Needs ffmpeg and Playwright (Chromium).
"""
import argparse, html, pathlib, re, shutil, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
FONTS = ROOT / 'site' / 'fonts'
CSS_FONTS = f'''
@font-face{{font-family:Tanker;src:url({(FONTS/'tanker/Tanker-Regular.woff2').as_uri()})}}
@font-face{{font-family:Switzer;src:url({(FONTS/'switzer/Switzer-Bold.woff2').as_uri()});font-weight:700}}
@font-face{{font-family:Switzer;src:url({(FONTS/'switzer/Switzer-Semibold.woff2').as_uri()});font-weight:600}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;background:transparent;overflow:hidden;font-family:Switzer;color:#fff}}
'''
GOLD, RED = '#E8B84A', '#D7262E'


def ff(*a):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *a], check=True)


def probe_dur(p):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def has_audio(p):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index',
                          '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout
    return bool(out.strip())


def parse_srt(text):
    def t(s):
        h, m, rest = s.strip().replace(',', '.').split(':')
        return int(h) * 3600 + int(m) * 60 + float(rest)
    cues = []
    for block in re.split(r'\n\s*\n', text.strip()):
        lines = [l for l in block.splitlines() if l.strip()]
        for i, l in enumerate(lines):
            if '-->' in l:
                a, b = l.split('-->')
                cues.append((t(a), t(b), ' '.join(lines[i + 1:])))
                break
    return cues


def render(pages, tmp):
    """pages: list of (filename, body_html, extra_css). One browser for all PNGs."""
    from playwright.sync_api import sync_playwright
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for name, body, css in pages:
            f = tmp / (name + '.html')
            f.write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS_FONTS}{css}</style>'
                         f'</head><body>{body}</body></html>', encoding='utf-8')
            pg.goto(f.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(120)
            png = tmp / (name + '.png'); pg.screenshot(path=str(png), omit_background=True); out.append(png)
        b.close()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('clip'); ap.add_argument('out')
    ap.add_argument('--start', type=float, default=0); ap.add_argument('--end', type=float)
    ap.add_argument('--max-len', type=float, default=30)
    ap.add_argument('--hook', required=True, help='big title on top, e.g. "DAVIES ON JONATHAN DAVID"')
    ap.add_argument('--speaker', required=True); ap.add_argument('--role', default='')
    ap.add_argument('--source', required=True, help='on-screen credit, e.g. "FC Bayern TV"')
    ap.add_argument('--take', required=True, help='TNB take shown on the end card')
    ap.add_argument('--captions', help='SRT file (times relative to --start)')
    ap.add_argument('--lines', nargs='*', default=[], help='"a-b|text" caption cues (relative to --start)')
    ap.add_argument('--end-secs', type=float, default=2.8)
    ap.add_argument('--cover', help='optional image (e.g. hero JPG) shown behind the take card')
    a = ap.parse_args()

    src = pathlib.Path(a.clip)
    end = a.end if a.end is not None else probe_dur(src)
    dur = min(end - a.start, a.max_len)
    if dur <= 1:
        raise SystemExit('excerpt too short')
    if end - a.start > a.max_len:
        print(f'note: excerpt trimmed to {a.max_len:.0f} s (fair-dealing limit)')

    cues = parse_srt(pathlib.Path(a.captions).read_text(encoding='utf-8')) if a.captions else []
    for l in a.lines:
        span, text = l.split('|', 1); x, y = span.split('-'); cues.append((float(x), float(y), text))
    cues = [(max(0, x), min(dur, y), t) for x, y, t in cues if x < dur]

    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        e = html.escape
        pages = [('header', f'''
<div class="top"><div class="tag">TNB · CLIP</div><h1>{e(a.hook)}</h1></div>
<div class="lt"><div class="nm">{e(a.speaker)}</div><div class="rl">{e(a.role)}</div></div>
<div class="cr">🎥 {e(a.source)}</div><div class="ft">TNBALLERS.COM</div>''', f'''
.top{{position:absolute;left:60px;right:60px;top:150px}}
.tag{{display:inline-block;background:{RED};font-weight:700;font-size:30px;letter-spacing:3px;padding:8px 18px;margin-bottom:22px}}
h1{{font-family:Tanker;font-weight:400;font-size:112px;line-height:.95;text-transform:uppercase;text-shadow:0 6px 30px rgba(0,0,0,.6)}}
.lt{{position:absolute;left:60px;top:1330px;border-left:8px solid {GOLD};padding:6px 0 6px 22px}}
.nm{{font-family:Tanker;font-size:66px;text-transform:uppercase;line-height:1}}
.rl{{font-weight:600;font-size:32px;color:#E6E6E6;margin-top:6px}}
.cr{{position:absolute;left:60px;bottom:250px;font-weight:600;font-size:28px;color:#cfcfcf}}
.ft{{position:absolute;right:60px;bottom:250px;font-weight:700;font-size:26px;letter-spacing:3px;color:{GOLD}}}''')]
        for i, (_, _, t) in enumerate(cues):
            pages.append((f'cap{i}', f'<div class="c"><span>{e(t)}</span></div>', f'''
.c{{position:absolute;left:70px;right:70px;top:1480px;text-align:center}}
.c span{{font-weight:700;font-size:58px;line-height:1.18;background:rgba(0,0,0,.72);
-webkit-box-decoration-break:clone;box-decoration-break:clone;padding:6px 16px}}'''))
        pages.append(('take', f'''<div class="w"><div class="tag">TNB TAKE</div><p>{e(a.take)}</p>
<div class="sp">{e(a.speaker)} · 🎥 {e(a.source)}</div><div class="ft">TNBALLERS.COM</div></div>''', f'''
.w{{position:absolute;inset:0;background:linear-gradient(160deg,rgba(10,10,10,.82),rgba(60,8,12,.88));
display:flex;flex-direction:column;justify-content:center;padding:0 80px}}
.tag{{align-self:flex-start;background:{GOLD};color:#111;font-weight:700;font-size:34px;letter-spacing:4px;padding:10px 22px;margin-bottom:40px}}
p{{font-family:Tanker;font-size:104px;line-height:1;text-transform:uppercase}}
.sp{{margin-top:44px;font-weight:600;font-size:32px;color:#E6E6E6}}
.ft{{position:absolute;right:80px;bottom:120px;font-weight:700;font-size:28px;letter-spacing:3px;color:{GOLD}}}'''))
        pngs = render(pages, tmp)
        header, caps, take = pngs[0], pngs[1:-1], pngs[-1]

        # 1) main excerpt: blurred cover background + clip at full width + overlays
        inputs = ['-ss', f'{a.start}', '-t', f'{dur}', '-i', str(src), '-i', str(header)]
        for c in caps:
            inputs += ['-i', str(c)]
        fc = ('[0:v]fps=30,split[a][b];'
              '[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.18,setsar=1[bg];'
              '[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-40[v0];[v0][1:v]overlay=0:0[v1]')
        last = 'v1'
        for i, (x, y, _) in enumerate(cues):
            fc += f';[{last}][{i + 2}:v]overlay=0:0:enable=\'between(t,{x:.2f},{y:.2f})\'[c{i}]'; last = f'c{i}'
        fc += f';[{last}]format=yuv420p[vout]'
        audio = ['-map', '0:a:0', '-c:a', 'aac', '-ar', '48000', '-ac', '2'] if has_audio(src) else []
        main_mp4 = tmp / 'main.mp4'
        ff(*inputs, '-filter_complex', fc, '-map', '[vout]', *audio, '-c:v', 'libx264', '-preset', 'medium',
           '-crf', '20', '-r', '30', *([] if audio else ['-an']), str(main_mp4))
        if not audio:  # add silence so concat has an audio track
            ff('-i', str(main_mp4), '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest',
               '-c:v', 'copy', '-c:a', 'aac', str(tmp / 'm2.mp4')); main_mp4 = tmp / 'm2.mp4'

        # 2) TNB take card (over a still of the last frame or the cover image)
        bgimg = tmp / 'bg.png'
        if a.cover:
            ff('-i', a.cover, '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920', str(bgimg))
        else:
            ff('-sseof', '-0.1', '-i', str(main_mp4), '-frames:v', '1', str(bgimg))
        end_mp4 = tmp / 'end.mp4'
        ff('-loop', '1', '-t', f'{a.end_secs}', '-i', str(bgimg), '-loop', '1', '-t', f'{a.end_secs}', '-i', str(take),
           '-f', 'lavfi', '-t', f'{a.end_secs}', '-i', 'anullsrc=r=48000:cl=stereo',
           '-filter_complex', "[0:v]scale=1080:1920,setsar=1[b];[1:v]format=rgba,fade=in:st=0:d=0.3:alpha=1[t];"
           "[b][t]overlay=0:0,fps=30,format=yuv420p[v]", '-map', '[v]', '-map', '2:a',
           '-c:v', 'libx264', '-crf', '20', '-c:a', 'aac', '-ar', '48000', '-ac', '2', str(end_mp4))

        # 3) join
        ff('-i', str(main_mp4), '-i', str(end_mp4), '-filter_complex',
           '[0:v]setsar=1[m];[1:v]setsar=1[n];[m][0:a][n][1:a]concat=n=2:v=1:a=1[v][a]', '-map', '[v]', '-map', '[a]',
           '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-movflags', '+faststart', a.out)
        print(f'wrote {a.out} ({dur + a.end_secs:.1f} s)')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
