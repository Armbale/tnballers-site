"""After tts_cb.py: give the Siuu scene room (run-up before the shout, hold after), then build the
sound design: heartbeat under the penalty, crowd roar on 1,000 and on the Siuu, music bed ducked under
the voice. Writes timed.json (shifted), vo_padded.wav, sfx.wav. Times in seconds."""
import json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

PRE, POST = 1.6, 1.4      # silence before / after the Siuu line
S = json.load(open('timed.json'))
vo, sr = sf.read('vo.wav')
i = next(j for j, l in enumerate(S) if l['scene'] == 'siuu')
cut0 = int((S[i]['t0'] - 0.05) * sr); cut1 = int((S[i]['t1'] + 0.05) * sr)
vo = np.concatenate([vo[:cut0], np.zeros(int(PRE * sr)), vo[cut0:cut1], np.zeros(int(POST * sr)), vo[cut1:]])
for j, l in enumerate(S):
    if j >= i:
        l['t0'] = round(l['t0'] + PRE, 3); l['t1'] = round(l['t1'] + PRE, 3)
    if j > i:
        l['t0'] = round(l['t0'] + POST, 3); l['t1'] = round(l['t1'] + POST, 3)
json.dump(S, open('timed.json', 'w'), indent=1, ensure_ascii=False)
sf.write('vo_padded.wav', vo, sr)

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
sf.write('sfx.wav', np.clip(sfx, -1, 1), SR)
print('siuu at', S[i]['t0'], 'total', round(total, 2), 'beats', m[1]['t0'], S[i]['t0'])
