import json, numpy as np, torch, soundfile as sf, sys
from chatterbox.tts import ChatterboxTTS
from faster_whisper import WhisperModel
import scipy.signal as ss
m = ChatterboxTTS.from_pretrained(device='cpu'); wm = WhisperModel('base.en', device='cpu', compute_type='int8')
for vid, text, want in [('v4', 'A hat-trick... against Spain.', 'spain'), ('v5', 'Then... Lee-on. He rose above everyone.', 'lyon|leon|lee')]:
    for seed in range(4):
        torch.manual_seed(20 + seed)
        w = m.generate(text, audio_prompt_path='ref.wav', exaggeration=0.75, cfg_weight=0.35).squeeze().numpy()
        nz = np.where(np.abs(w) > 0.012)[0]; w = w[max(0, nz[0] - int(.02 * m.sr)):nz[-1] + int(.08 * m.sr)]
        tr = ' '.join(s.text for s in wm.transcribe(ss.resample_poly(w, 16000, m.sr).astype(np.float32))[0]).lower()
        print(vid, seed, tr, flush=True)
        if any(x in tr for x in want.split('|')):
            sf.write(f'vo/{vid}.wav', w / np.max(np.abs(w)) * 0.9, m.sr); break
