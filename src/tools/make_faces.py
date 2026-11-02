#!/usr/bin/env python3
"""
Build the FACE LIBRARY: hero cut-outs for club regulars so no post goes out without a face.

Input:  src/assets/faces_manifest.tsv (slug, name, club, Commons file, author, licence)
        src/assets/faces_src/<slug>.img (original from Special:FilePath; downloaded separately, paced)
Output: src/assets/cutouts/hero/<slug>.png (rembg isnet-general-use, cropped to bbox, 800 px max)
        src/assets/faces.json (slug -> name, club, credit, commons URL)
        src/assets/faces_contact.jpg (contact sheet to eyeball every cut-out)

Usage: python3 src/tools/make_faces.py [slug ...]
"""
import csv, io, json, sys, urllib.parse
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / 'src/assets'
SRC, OUT = A / 'faces_src', A / 'cutouts/hero'
OUT.mkdir(parents=True, exist_ok=True)

def credit(author, licence):
    return f"{author} / Wikimedia Commons ({licence})"

def main():
    only = set(sys.argv[1:])
    rows = list(csv.DictReader(open(A / 'faces_manifest.tsv', encoding='utf-8'), delimiter='\t'))
    lib_path = A / 'faces.json'
    lib = json.loads(lib_path.read_text()) if lib_path.exists() else {}
    from rembg import remove, new_session
    sess = new_session('isnet-general-use')
    for r in rows:
        s = r['slug']
        if only and s not in only:
            continue
        f = SRC / f'{s}.img'
        if not f.exists() or f.stat().st_size < 5000:
            print('missing', s); continue
        try:
            im = Image.open(f).convert('RGB')
        except Exception as e:
            print('bad image', s, e); continue
        im.thumbnail((1600, 1600))
        cut = remove(im, session=sess)
        bbox = cut.getchannel('A').point(lambda a: 255 if a > 20 else 0).getbbox()
        if not bbox:
            print('empty cut-out', s); continue
        cut = cut.crop(bbox)
        # full-body shot: keep head to waist so the face is big on the post
        if cut.height > 1.5 * cut.width:
            cut = cut.crop((0, 0, cut.width, int(cut.width * 1.35)))
        if cut.width > 800:
            cut = cut.resize((800, round(cut.height * 800 / cut.width)), Image.LANCZOS)
        cut.save(OUT / f'{s}.png')
        lib[s] = {'name': r['name'], 'club': r['club'],
                  'credit': credit(r['author'], r['licence']),
                  'source': 'https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(r['file'].replace(' ', '_')),
                  'size': list(cut.size),
                  'quality': 'ok' if cut.width >= 450 else 'low (small source, use only if nothing better)'}
        print('ok', s, cut.size, flush=True)
    lib_path.write_text(json.dumps(dict(sorted(lib.items())), ensure_ascii=False, indent=1))
    # contact sheet
    items = [k for k in lib if (OUT / f'{k}.png').exists()]
    cols, cw, ch = 8, 220, 280
    sheet = Image.new('RGB', (cols * cw, ((len(items) + cols - 1) // cols) * ch), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for i, k in enumerate(items):
        c = Image.open(OUT / f'{k}.png'); c.thumbnail((cw - 10, ch - 30))
        x, y = (i % cols) * cw, (i // cols) * ch
        sheet.paste(c, (x + 5, y + 5), c)
        d.text((x + 5, y + ch - 20), k, fill=(255, 220, 0))
    sheet.save(A / 'faces_contact.jpg', quality=80)
    print('library', len(lib))

if __name__ == '__main__':
    main()
