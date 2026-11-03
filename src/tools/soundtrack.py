#!/usr/bin/env python3
"""TNB's own soundtrack generator: a synthesised trap/drill-style beat + hit SFX synced to the edit.
100% generated here, so no music licence or Content ID issues, and it works on TikTok too (the API can't add music there).

python3 src/tools/soundtrack.py out.wav --secs 42 --bpm 140 --mood hype \
   --impacts 0.15,5,10.5,16,21.5,27,33,38.5 --whooshes 4.7,10.2,15.7 --risers 26,32.4 --drop 27 --end 42
Mux: ffmpeg -i reel.mp4 -i out.wav -c:v copy -c:a aac -b:a 192k -shortest reel_audio.mp4
Moods: hype (minor, hard drums), dark (slower, sparse, for losses), anthem (major pad, for trophies).
"""
import argparse, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(7)


def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
    return e


def kick808(dur=0.55, f0=150, f1=42):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t / 0.32)
    click = rng.standard_normal(n) * np.exp(-t / 0.004) * 0.3
    return np.tanh(2.2 * (x + click)) * 0.9


def snare(dur=0.25):
    n = int(dur * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    noise = np.convolve(noise, np.ones(3) / 3, 'same') - np.convolve(noise, np.ones(40) / 40, 'same')
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05)
    return (noise * np.exp(-t / 0.09) * 0.8 + body * 0.5)


def hat(dur=0.05, open_=False):
    n = int((0.25 if open_ else dur) * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n); x = x - np.convolve(x, np.ones(6) / 6, 'same')
    return x * np.exp(-t / (0.09 if open_ else 0.015)) * 0.35


def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, 'same')


def saw(f, n):
    t = np.arange(n) / SR
    return 2 * ((t * f) % 1) - 1


def pad(freqs, dur, amp=0.12):
    n = int(dur * SR); out = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0, 0.13):
            out += saw(f * (1 + det / 100), n)
    out = lowpass(lowpass(out, 40), 40)
    t = np.arange(n) / SR
    fade = np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4)
    return out / len(freqs) / 3 * amp * fade


def boom(dur=1.6):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 30 + 90 * np.exp(-t * 6)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.6)
    crack = rng.standard_normal(n) * np.exp(-t / 0.03) * 0.6
    return np.tanh(1.8 * (x + lowpass(crack, 4))) * 0.95


def whoosh(dur=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    k = (4 + 40 * (1 - t / dur)).astype(int)
    y = np.array([0.0] * n)
    # crude sweeping filter: mix of two lowpasses with moving weight
    a, b = lowpass(x, 4), lowpass(x, 40)
    w = t / dur
    y = a * w + b * (1 - w)
    e = np.sin(np.pi * t / dur) ** 2
    return y * e * 0.6


def riser(dur=1.2):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    y = lowpass(x, 30) * (1 - t / dur) + lowpass(x, 3) * (t / dur)
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / dur) ** 2) / SR) * 0.15
    return (y * 0.5 + tone) * (t / dur) ** 2


def add(buf, x, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(x)); buf[i:j] += x[:j - i] * g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('--secs', type=float, required=True)
    ap.add_argument('--bpm', type=float, default=140); ap.add_argument('--mood', default='hype')
    fl = lambda s: [float(v) for v in s.split(',') if v.strip()]
    ap.add_argument('--impacts', type=fl, default=[]); ap.add_argument('--whooshes', type=fl, default=[])
    ap.add_argument('--risers', type=fl, default=[]); ap.add_argument('--drop', type=float, default=0)
    ap.add_argument('--start-beat', type=float, default=0.15)
    a = ap.parse_args()
    n = int(a.secs * SR); music = np.zeros(n); sfx = np.zeros(n)
    beat = 60 / a.bpm; bar = beat * 4
    root = {'hype': 55.0, 'dark': 49.0, 'anthem': 65.41}.get(a.mood, 55.0)  # A1 / G1 / C2
    minor = a.mood != 'anthem'
    prog = [0, -4, -2, -5] if minor else [0, 5, -3, 7]   # semitone offsets per bar
    chord = (lambda r: [r * 4, r * 4 * 2 ** ((3 if minor else 4) / 12), r * 4 * 2 ** (7 / 12)])
    kpat = [0, 0.75, 1.5, 2.5, 3.25] if a.mood != 'dark' else [0, 1.75, 2.5]
    t0 = a.start_beat; b = 0
    while t0 + b * bar < a.secs:
        bt = t0 + b * bar; r = root * 2 ** (prog[b % 4] / 12)
        intro = bt < 4.8 and a.drop  # lighter before first drop
        add(music, pad(chord(r), bar + 0.3), bt, 2.2)
        for k in kpat:
            if intro and k not in (0, 2.5): continue
            add(music, kick808(f1=r if r > 35 else r * 2), bt + k * beat, 0.85)
        if not intro:
            for s in (1, 3): add(music, snare(), bt + s * beat, 0.55)
            steps = 16 if a.mood == 'hype' else 8
            for h in range(steps):
                ht = bt + h * bar / steps
                add(music, hat(open_=(h % 8 == 6)), ht, 0.18 if h % 2 else 0.3)
            if a.mood == 'hype' and b % 2 == 1:   # hat roll
                for h in range(6): add(music, hat(), bt + 3.5 * beat + h * beat / 12, 0.2)
        b += 1
    for t in a.impacts: add(sfx, boom(), t, 0.9)
    for t in a.whooshes: add(sfx, whoosh(), t, 0.8)
    for t in a.risers: add(sfx, riser(), t, 0.7)
    # duck the music a touch under impacts
    duck = np.ones(n)
    for t in a.impacts:
        i = int(t * SR); m = int(0.35 * SR)
        duck[i:i + m] = np.minimum(duck[i:i + m], np.linspace(0.45, 1, len(duck[i:i + m])))
    mix = music * duck * 0.8 + sfx
    tt = np.arange(n) / SR
    mix *= np.minimum(1, tt / 0.05) * np.minimum(1, (a.secs - tt) / 1.2)
    mix = np.tanh(1.4 * mix / (np.max(np.abs(mix)) + 1e-9)) * 0.92
    st = np.stack([mix, np.roll(mix, 12)], 1)  # tiny stereo width
    pcm = (st * 32767).astype('<i2')
    with wave.open(a.out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print('wrote', a.out)


if __name__ == '__main__':
    main()
