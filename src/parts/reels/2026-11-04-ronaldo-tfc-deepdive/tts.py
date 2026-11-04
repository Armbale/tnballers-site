import json, wave, sys, numpy as np
from kokoro_onnx import Kokoro
V='/tmp/claude-0/-home-claude-tnballers-site/c129652d-45e1-5911-85e0-170a45e12e8c/scratchpad/voices/'
k=Kokoro(V+'kokoro-v1.0.onnx',V+'voices-v1.0.bin')
S=json.load(open('script.json')); voice=sys.argv[1]; sp=float(sys.argv[2])
out=[];t=0.6;sr0=24000;gap=0.12
out.append(np.zeros(int(0.6*sr0),dtype=np.float32))
for l in S:
    a,sr=k.create(l['say'],voice=voice,speed=sp,lang='en-us')
    nz=np.where(np.abs(a)>0.01)[0]; a=a[max(0,nz[0]-int(.02*sr)):nz[-1]+int(.05*sr)]
    d=len(a)/sr; l['t0']=round(t,3); l['t1']=round(t+d,3); t+=d+gap
    out.append(a.astype(np.float32)); out.append(np.zeros(int(gap*sr),dtype=np.float32))
x=np.concatenate(out); x=np.clip(x/np.max(np.abs(x))*0.9,-1,1)
w=wave.open('vo.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr0); w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
json.dump(S,open('timed.json','w'),indent=1,ensure_ascii=False)
print('total',round(t,2))
