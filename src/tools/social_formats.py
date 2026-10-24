#!/usr/bin/env python3
"""Make the Story (1080x1920 JPG) and Reel (1080x1920 MP4, ~8 s) versions of a finished TNB feed post.

Usage: python3 src/tools/social_formats.py <feed.jpg> <slug>
  <feed.jpg>  the 1080x1350 post exported from Canva
  <slug>      e.g. 2026-10-24-montreal-roses-shield (lowercase, hyphens)

Writes site/social/<slug>/{feed.jpg,story.jpg,reel.mp4}. After pushing to main, Netlify serves them at
https://tnballers.com/social/<slug>/<file> (give it about a minute), which is the URL to hand to Metricool.
Also deletes site/social folders older than 14 days so the repo stays small.
"""
import os, re, shutil, subprocess, sys, datetime
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
RED, GOLD = (200, 16, 46), (212, 175, 55)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def background(post):
    """Black canvas with a blurred, darkened copy of the post behind, the red diagonal stripe and a gold rule."""
    bg = post.resize((int(post.width * H / post.height), H)).filter(ImageFilter.GaussianBlur(40))
    left = (bg.width - W) // 2
    bg = bg.crop((left, 0, left + W, H))
    bg = Image.blend(Image.new('RGB', (W, H), (0, 0, 0)), bg, 0.28)
    d = ImageDraw.Draw(bg, 'RGBA')
    d.polygon([(0, 1560), (W, 1300), (W, 1380), (0, 1640)], fill=RED + (235,))
    d.rectangle([(90, 255), (W - 90, 261)], fill=GOLD + (255,))
    return bg


def place(post, scale):
    w = int(1000 * scale)
    return post.resize((w, int(w * post.height / post.width)), Image.LANCZOS)


def main(src, slug):
    if not re.fullmatch(r'[a-z0-9-]+', slug):
        sys.exit('slug must be lowercase letters, digits and hyphens')
    post = Image.open(src).convert('RGB')
    out = os.path.join(ROOT, 'site', 'social', slug)
    os.makedirs(out, exist_ok=True)
    post.save(os.path.join(out, 'feed.jpg'), quality=92)
    bg = background(post)

    # Story: the post centred on the background
    p = place(post, 1.0)
    story = bg.copy()
    story.paste(p, ((W - p.width) // 2, (H - p.height) // 2))
    story.save(os.path.join(out, 'story.jpg'), quality=92)

    # Reel: 8 s, slow push-in from 0.94 to 1.0 with a quick fade from black
    frames = os.path.join(out, '_frames')
    os.makedirs(frames, exist_ok=True)
    n = 8 * 30
    for i in range(n):
        t = i / (n - 1)
        e = 1 - (1 - t) ** 3
        p = place(post, 0.94 + 0.06 * e)
        f = bg.copy()
        f.paste(p, ((W - p.width) // 2, (H - p.height) // 2))
        if i < 12:
            f = Image.blend(Image.new('RGB', (W, H)), f, i / 12)
        f.save(os.path.join(frames, f'{i:04d}.jpg'), quality=90)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', os.path.join(frames, '%04d.jpg'),
                    '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '23', '-preset', 'medium', '-movflags', '+faststart',
                    '-c:a', 'aac', '-b:a', '64k', os.path.join(out, 'reel.mp4')], check=True)
    shutil.rmtree(frames)

    # Clean up anything older than 14 days
    cutoff = datetime.date.today() - datetime.timedelta(days=14)
    base = os.path.join(ROOT, 'site', 'social')
    for d in os.listdir(base):
        m = re.match(r'(\d{4}-\d{2}-\d{2})', d)
        if m and datetime.date.fromisoformat(m.group(1)) < cutoff:
            shutil.rmtree(os.path.join(base, d))

    for f in ('feed.jpg', 'story.jpg', 'reel.mp4'):
        size = os.path.getsize(os.path.join(out, f)) // 1024
        print(f'https://tnballers.com/social/{slug}/{f}  ({size} KB)')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
