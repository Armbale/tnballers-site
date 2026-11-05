"""Chatterbox voice lines -> vo/<id>.wav (trimmed). Run with the chatterbox venv python. Voice cloned from ref.wav (TNB's Kokoro-derived voice)."""
import json, os, numpy as np, torch, soundfile as sf
from chatterbox.tts import ChatterboxTTS
torch.manual_seed(11); m = ChatterboxTTS.from_pretrained(device='cpu'); os.makedirs('vo', exist_ok=True)
for l in json.load(open('vo_lines.json')):
    w = m.generate(l['say'], audio_prompt_path='ref.wav', exaggeration=0.75, cfg_weight=0.35).squeeze().numpy()
    nz = np.where(np.abs(w) > 0.012)[0]; w = w[max(0, nz[0] - int(.02 * m.sr)):nz[-1] + int(.08 * m.sr)]
    sf.write(f"vo/{l['id']}.wav", w / np.max(np.abs(w)) * 0.9, m.sr); print(l['id'], round(len(w) / m.sr, 2), flush=True)
