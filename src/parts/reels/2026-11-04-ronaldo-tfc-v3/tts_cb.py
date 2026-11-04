"""Chatterbox voiceover for script.json -> vo.wav + timed.json. Run with the chatterbox venv python.
Voice: Chatterbox (MIT) cloned from a Kokoro (Apache-2.0) bm_george reference, so no real person's voice is copied."""
import json, sys, numpy as np, torch, torchaudio as ta, soundfile as sf
from chatterbox.tts import ChatterboxTTS
ref = sys.argv[1]; ex = float(sys.argv[2]); cfg = float(sys.argv[3])
torch.manual_seed(7)
m = ChatterboxTTS.from_pretrained(device='cpu')
S = json.load(open('script.json')); sr = m.sr; gap = 0.16; t = 0.35
out = [np.zeros(int(0.35 * sr), np.float32)]
for l in S:
    w = m.generate(l['say'], audio_prompt_path=ref, exaggeration=ex, cfg_weight=cfg).squeeze().numpy()
    nz = np.where(np.abs(w) > 0.012)[0]; w = w[max(0, nz[0] - int(.02 * sr)):nz[-1] + int(.06 * sr)]
    d = len(w) / sr; l['t0'] = round(t, 3); l['t1'] = round(t + d, 3); t += d + gap
    out += [w.astype(np.float32), np.zeros(int(gap * sr), np.float32)]
    print(l['scene'], round(d, 2), flush=True)
x = np.concatenate(out); x = x / np.max(np.abs(x)) * 0.9
sf.write('vo.wav', x, sr); json.dump(S, open('timed.json', 'w'), indent=1, ensure_ascii=False); print('total', round(t, 2))
