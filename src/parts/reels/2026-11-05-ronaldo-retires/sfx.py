import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR=48000; total=38.4; n=int(total*SR); sfx=np.zeros(n); rng=np.random.default_rng(5)
def roar(dur,peak,attack=.25):
    m=int(dur*SR); x=sosfilt(butter(4,[250,3500],'band',fs=SR,output='sos'),rng.standard_normal(m)); tt=np.arange(m)/SR
    env=np.minimum(1,tt/attack)*np.exp(-np.maximum(0,tt-attack)/(dur/2.5)); return x/np.max(np.abs(x))*env*(1+.25*np.sin(2*np.pi*3.3*tt))*peak
def add(s,t): a=int(t*SR); b=min(n,a+len(s)); sfx[a:b]+=s[:b-a]
add(roar(5,.45,.15),22.3)   # champions of Europe
add(roar(6,.4,.6),34.3)     # Obrigado
sf.write('sfx.wav',np.clip(sfx,-1,1),SR)
