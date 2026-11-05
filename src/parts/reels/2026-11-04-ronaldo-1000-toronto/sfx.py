"""Sound effects for the final timeline (timed.json already padded/spliced): heartbeat under the penalty,
crowd roars on the 3D goals, on 1,000 and on the Siuu. Writes sfx.wav."""
import json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
S = json.load(open('timed.json')); i = next(j for j, l in enumerate(S) if l['scene'] == 'siuu')
total = S[-1]['t1'] + 2.5
SR = 48000; n = int(total * SR); sfx = np.zeros(n)
rng = np.random.default_rng(3)


def add(sig, t):
    a = int(t * SR); b = min(n, a + len(sig)); sfx[a:b] += sig[:b - a]


def roar(dur, peak, attack=0.25):
    m = int(dur * SR); x = rng.standard_normal(m)
    x = sosfilt(butter(4, [250, 3500], 'band', fs=SR, output='sos'), x)
    tt = np.arange(m) / SR
    env = np.minimum(1, tt / attack) * np.exp(-np.maximum(0, tt - attack) / (dur / 2.5))
    wob = 1 + 0.25 * np.sin(2 * np.pi * 3.3 * tt) * np.sin(2 * np.pi * 0.7 * tt)
    return x / np.max(np.abs(x)) * env * wob * peak


def thump(f=55, dur=0.18, amp=0.7):
    tt = np.arange(int(dur * SR)) / SR
    return np.sin(2 * np.pi * f * tt * (1 - tt)) * np.exp(-tt / 0.06) * amp


m = [l for l in S if l['scene'] == 'moment']
# heartbeat from the penalty line until the 1,000 shout (lub-dub, 80 bpm)
t = m[0]['t0']
while t < m[1]['t0'] - 0.1:
    add(thump(), t); add(thump(50, amp=0.5), t + 0.22); t += 0.75
add(roar(5.0, 0.55, 0.12), m[1]['t0'])               # goal 1,000
add(roar(4.5, 0.6, 0.08), S[i]['t0'])                # the Siuu landing
add(roar(6.0, 0.18, 1.5), S[i]['t0'] + 2.0)          # crowd stays up into the end card
ic = [l for l in S if l['scene'] == 'iconic']
add(roar(3.5, 0.45, 0.1), ic[0]['t0'] + 3.75)   # bicycle kick GOAL
add(roar(3.5, 0.45, 0.1), ic[2]['t0'] - 0.2 + 4.8)  # Porto GOAL
sf.write('sfx.wav', np.clip(sfx, -1, 1), SR)
print('siuu at', S[i]['t0'], 'total', round(total, 2), 'beats', m[1]['t0'], S[i]['t0'])
