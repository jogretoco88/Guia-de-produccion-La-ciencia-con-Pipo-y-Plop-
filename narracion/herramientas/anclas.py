"""De la transcripción del concatenado (frases + 2 s de silencio, en orden) saca:
 - anclas/<lg>.json: tiempo de cada palabra-ancla (hip/hic) dentro del mp3 de su frase
 - qa/<lg>_qa.txt: comparación guion vs. lo que se oye, frase por frase
uso: python3 anclas.py lg qa/<lg>_words.json"""
import sys, os, json, re, subprocess, unicodedata, difflib
lg, wf = sys.argv[1], sys.argv[2]
G = json.load(open('guion.json')); L = G['lines']
W = json.load(open(wf)); W = W.get('words', W) if isinstance(W, dict) else W
W = [w for w in W if w.get('type', 'word') == 'word']
def dur(f):
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
def norm(s):
    s = unicodedata.normalize('NFKD', s.lower()); s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^\w\s\u0900-\u0963\u0966-\u097F]', ' ', s, flags=re.U).split()
# offsets: igual que en el sandbox (decodificado a 44.1 kHz + 2 s)
off = {}; t = 0.0
for o in L:
    off[o['id']] = t
    OV = json.load(open(f'qa/{lg}_dur_override.json')) if os.path.exists(f'qa/{lg}_dur_override.json') else {}
    if o['id'] in OV: t += OV[o['id']] + 2.0; continue
    n = int(subprocess.run(['ffmpeg','-v','error','-i',f"raw/{lg}/{o['id']}.mp3",'-ac','1','-ar','44100','-f','f32le','-'],capture_output=True).stdout.__len__()/4)
    t += n/44100 + 2.0
HIC = norm(G['hic'][lg])[0]
anc = {}; qa = []; worst = []
ids = [o['id'] for o in L]
for k, o in enumerate(L):
    a = off[o['id']]; b = off[ids[k+1]] - 1.0 if k+1 < len(L) else 1e9
    ws = [w for w in W if a - 0.3 <= w['start'] < b]
    heard = ' '.join(w['text'] for w in ws)
    want = re.sub(r'\[[^\]]*\]\s*', '', o[lg])
    r = difflib.SequenceMatcher(None, norm(want), norm(heard)).ratio()
    qa.append(f"{o['id']}  {r:.2f}\n  guion: {want}\n  oído : {heard}\n")
    worst.append((r, o['id']))
    if o['anchors'] and o['anchors'][0][0] != 'START':
        hs = [w['start'] - a for w in ws if HIC in norm(w['text']) or norm(w['text'])[:1] == [HIC]]
        need = len(o['anchors'])
        if len(hs) < need:
            # el transcriptor a veces no escribe el hipo: se toma el tramo de sonido corto
            # que no queda cubierto por ninguna palabra transcrita
            from medir import analyse
            seg = analyse(f"raw/{lg}/{o['id']}.mp3")['segs']
            spoken = [(w['start'] - a, w['end'] - a) for w in ws if norm(w['text'])]
            free = [s for s in seg if (s[1] - s[0]) < 0.8 and
                    not any(min(s[1], e) - max(s[0], b) > 0.06 for b, e in spoken)]
            hs = sorted(set(round(h, 3) for h in hs) | set(round(s[0], 3) for s in free))[:need]
            qa.append(f"  ** {o['id']}: hipo no transcrito, ancla por tramo de sonido {hs}")
        anc[o['id']] = [round(h, 3) for h in hs]
json.dump(anc, open(f'anclas/{lg}.json', 'w'), indent=1)
open(f'qa/{lg}_qa.txt', 'w').write('\n'.join(qa))
print(lg, 'anclas', anc)
print('peores coincidencias:', sorted(worst)[:6])
