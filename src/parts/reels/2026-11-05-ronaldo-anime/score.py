#!/usr/bin/env python3
"""Original emotional score for the Ronaldo anime tribute: piano -> strings + taiko build -> choir climax -> piano alone.
Writes score.mid and renders score.wav with FluidSynth (FluidR3 GM soundfont). Hits are placed at exact seconds."""
import mido, subprocess
BPM = 70; TPB = 480; SPB = 60 / BPM
FK, HD = 13.7, 24.5
HITS = {'fk_contact': FK + 2.455, 'fk_goal': FK + 5.54, 'hd_contact': HD + 4.075, 'hd_goal': HD + 5.825, 'paris': 36.4, 'end': 50.1}
TOTAL = 58.5
mid = mido.MidiFile(ticks_per_beat=TPB)
def tk(sec): return int(round(sec / SPB * TPB))
ev = []   # (tick, channel, msg)
def note(ch, n, t0, dur, vel):
    ev.append((tk(t0), mido.Message('note_on', channel=ch, note=n, velocity=max(1, min(127, int(vel))))))
    ev.append((tk(t0 + dur), mido.Message('note_off', channel=ch, note=n, velocity=0)))
def prog(ch, p, t=0): ev.append((tk(t), mido.Message('program_change', channel=ch, program=p)))
def cc(ch, c, v, t): ev.append((tk(t), mido.Message('control_change', channel=ch, control=c, value=int(max(0, min(127, v))))))
# channels: 0 piano, 1 strings, 2 slow strings (high), 3 choir, 4 horns, 5 timpani, 6 taiko, 7 cello/contrabass, 9 drums
for ch, p in [(0, 0), (1, 48), (2, 49), (3, 52), (4, 60), (5, 47), (6, 116), (7, 42)]: prog(ch, p)
for ch in range(8): cc(ch, 91, 100, 0); cc(ch, 93, 30, 0)   # reverb / chorus
cc(9, 91, 90, 0)
# progression (A minor): Am F C G | Am F C E | F G Am Am
A = {'Am': [57, 60, 64], 'F': [53, 57, 60], 'C': [48, 55, 64], 'G': [55, 59, 62], 'E': [52, 56, 59], 'Dm': [50, 57, 62], 'Fmaj7': [53, 57, 64]}
ROOT = {'Am': 45, 'F': 41, 'C': 36, 'G': 43, 'E': 40, 'Dm': 38, 'Fmaj7': 41}
bar = 4 * SPB
seq = ['Am', 'F', 'C', 'G', 'Am', 'F', 'C', 'E', 'Am', 'F', 'C', 'G', 'F', 'G', 'Am', 'E', 'F', 'Fmaj7']
def section(t):  # intensity 0..1 over time
    if t < 10.3: return 0.0
    if t < FK: return .3
    if t < 33: return .7
    if t < 36.4: return .55
    if t < 43.3: return 1.0
    if t < 50.1: return .6
    return 0.1
melody = {0: [76, 74, 72, 71], 1: [72, 69, 72, 74], 2: [76, 79, 76, 74], 3: [74, 71, 74, 76]}
for i, ch_name in enumerate(seq):
    t0 = i * bar
    if t0 > TOTAL - 1: break
    ch = A[ch_name]; r = ROOT[ch_name]; inten = section(t0 + .1)
    # piano: broken-chord arpeggio in 8ths, always present (softer in the big sections), melody on top
    arp = [r, ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12, ch[0] + 12, ch[2], ch[1] + 12]
    for k, n in enumerate(arp): note(0, n, t0 + k * SPB / 2, SPB * 1.6, 52 + 14 * (k == 0) - 8 * inten)
    if inten <= .3 or t0 >= 50.1:
        m = melody[i % 4]
        for k, n in enumerate(m): note(0, n, t0 + k * SPB, SPB * 1.4, 70 - 6 * (k % 2))
    if inten >= .3:
        for n in ch: note(1, n, t0, bar * .98, 50 + 40 * inten)            # strings pad
        note(7, r - 12, t0, bar * .98, 60 + 40 * inten); note(7, r, t0, bar * .98, 50 + 30 * inten)
    if inten >= .7:
        for k, n in enumerate(melody[i % 4]): note(2, n + 12 if inten >= 1 else n, t0 + k * SPB, SPB * 1.05, 70 + 30 * inten)   # high strings melody
        for n in ch[:2]: note(4, n - 12, t0, bar * .95, 55 + 30 * inten)    # horns
        for k in range(4): note(6, 50, t0 + k * SPB, .4, 70 + 45 * inten * (1 if k % 2 == 0 else .6))   # taiko pulse
    if inten >= 1:
        for n in ch: note(3, n + 12, t0, bar * .98, 85)                      # choir
# timpani roll building into the free kick, and into Paris
for start, end in [(10.3, FK), (33.0, 36.4)]:
    t = start
    while t < end:
        k = (t - start) / (end - start); note(5, 45, t, .09, 30 + 90 * k); t += .09 - .04 * k
# big hits: crash + timpani + bass on goals; a soft swell on contacts (the slow-mo), silence-then-hit feel
for key in ['fk_goal', 'hd_goal', 'paris']:
    t = HITS[key]; note(9, 49, t, 1.5, 120); note(9, 57, t, 1.5, 110); note(5, 45, t, 1.2, 127); note(5, 33, t, 1.2, 127); note(7, 33, t, 2.5, 120); note(6, 48, t, .6, 127)
for key in ['fk_contact', 'hd_contact']:
    t = HITS[key]; note(5, 40, t, .6, 110); note(9, 55, t, 1.0, 90)
    note(9, 119 if False else 52, t - .9, .9, 60)   # china cymbal swish into the strike
# ending: hold the last chord in piano + soft strings to the end
note(0, 45, 54.9, 3.6, 70); [note(0, n + 12, 54.9, 3.6, 60) for n in A['Fmaj7']]; [note(1, n, 54.9, 3.6, 40) for n in A['Fmaj7']]
ev.sort(key=lambda e: (e[0], 0 if e[1].type == 'program_change' else (1 if e[1].type == 'control_change' else (2 if e[1].type == 'note_off' else 3))))
tr = mido.MidiTrack(); mid.tracks.append(tr); tr.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM)))
last = 0
for t, m in ev: tr.append(m.copy(time=t - last)); last = t
mid.save('score.mid')
subprocess.run(['fluidsynth', '-ni', '-g', '0.9', '-r', '48000', '-F', 'score_raw.wav', '/usr/share/sounds/sf2/FluidR3_GM.sf2', 'score.mid'], check=True, capture_output=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'score_raw.wav', '-af', f'atrim=0:{TOTAL},afade=t=out:st={TOTAL-2.5}:d=2.5', '-ar', '48000', 'score.wav'], check=True)
print('score.wav', HITS)
