"""Place the voice lines at their times, add crowd roars on the goals, duck the score under the voice -> final.wav"""
import json, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
SR = 48000; TOTAL = 58.5; n = int(TOTAL * SR)
vo = np.zeros(n); sfx = np.zeros(n); rng = np.random.default_rng(4)
for l, v in zip(json.load(open('vo_lines.json')), json.load(open('vo_timed.json'))):
    x, sr = sf.read('vo/' + l['id'] + '.wav'); x = resample_poly(x, SR, sr); a = int(v['at'] * SR); vo[a:a + len(x)] += x[:n - a]
def roar(dur, peak, attack=.2):
    m = int(dur * SR); x = sosfilt(butter(4, [250, 3500], 'band', fs=SR, output='sos'), rng.standard_normal(m)); tt = np.arange(m) / SR
    env = np.minimum(1, tt / attack) * np.exp(-np.maximum(0, tt - attack) / (dur / 2.5)); return x / np.max(np.abs(x)) * env * (1 + .25 * np.sin(2 * np.pi * 3.3 * tt)) * peak
for t, p in [(13.7 + 5.54, .35), (24.5 + 5.825, .35), (36.4 + 3.3, .3)]:
    r = roar(4.5, p); a = int(t * SR); sfx[a:a + len(r)] += r[:n - a]
sf.write('vo_track.wav', vo, SR); sf.write('sfx_track.wav', np.clip(sfx, -1, 1), SR)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'score.wav', '-i', 'vo_track.wav', '-i', 'sfx_track.wav', '-filter_complex',
  '[1:a]aresample=48000,volume=1.5,asplit=2[v][sc];[0:a]aresample=48000,volume=0.8[m];[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=30:release=500[md];'
  '[v]aecho=0.8:0.6:40:0.15[ve];[2:a]aresample=48000[s];[ve][md][s]amix=inputs=3:normalize=0:duration=first,atrim=0:58.5,volume=1.7,alimiter=limit=0.95[a]',
  '-map', '[a]', '-ac', '2', 'final.wav'], check=True)
print('final.wav')
