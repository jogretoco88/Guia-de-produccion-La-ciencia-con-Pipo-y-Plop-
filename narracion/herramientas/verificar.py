"""Compara lo que se oye (transcripción Scribe de la pista de verificación) con el guion, frase por frase.
uso: python3 verificar.py lg   (lee qa/<lg>_words.json; escribe qa/<lg>_qa.txt)"""
import sys, json, re, difflib, subprocess
lg = sys.argv[1]
G = json.load(open('guion.json'))['lines']
# Scribe escribe en alfabeto latino las palabras prestadas del inglés al hindi; se igualan antes de comparar
HI_LAT = dict(plop='प्लॉप', capsaicin='कैप्सेसिन', button='बटन', sensor='सेंसर', alarm='अलार्म', dragon='ड्रैगन',
              zoom='ज़ूम', plate='प्लेट', soup='सूप', robot='रोबोट', casein='केसीन', protein='प्रोटीन')
def norm(s):
    s = re.sub(r'\[[^\]]*\]', ' ', s).lower()
    s = ' '.join(HI_LAT.get(re.sub(r'\W', '', w), w) for w in s.split())
    s = s.replace('\u093c', '').replace('\u0901', '\u0902')   # nukta y chandrabindu: variantes de escritura
    s = re.sub(r'[^\w\sऀ-ॣ०-ॿ]', ' ', s)
    return s.split()
def dur(p):
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
W = json.load(open(f'qa/{lg}_words.json'))
W = W.get('words', W) if isinstance(W, dict) else W
W = [w for w in W if w.get('type', 'word') == 'word']
import os
OV = json.load(open(f'qa/{lg}_dur_override.json')) if os.path.exists(f'qa/{lg}_dur_override.json') else {}
t = 0.0; out = []; ok = 0
for o in G:
    d = subprocess.run(['ffmpeg','-v','error','-i',f'raw/{lg}/{o["id"]}.mp3','-ac','1','-ar','44100','-f','s16le','-'],capture_output=True).stdout
    dd = len(d) / 2 / 44100
    if o['id'] in OV: dd = OV[o['id']]   # la pista de verificación se hizo con la toma anterior
    heard = ' '.join(w['text'] for w in W if t - 0.3 <= w['start'] < t + dd + 1.0)
    a, b = norm(o[lg]), norm(heard)
    if lg == 'hi':  # «सेंसरों» / «सेंसर», «न» / «ना», «बटनों» / «बटन»: misma palabra, distinta terminación
        a = [{'सेंसरों': 'सेंसर', 'न': 'ना', 'मिलें': 'मिले'}.get(x, x) for x in a]
    if o['id'] == 'E03_C14':  # el nombre del receptor se dice deletreado; Scribe lo escribe «TRPV1»
        a = [x for x in a if x not in ('te','erre','pe','uve','uno','t','r','p','v','one','un','tê','pê','vê','um','टी','आर','पी','वी','वन')]
        b = [x for x in b if x not in ('trpv1','t','r','p','v','1','one','un','um','टी','आर','पी','वी','वन')]
    r = difflib.SequenceMatcher(None, a, b).ratio()
    flag = 'OK ' if r >= 0.85 else 'REVISAR'
    ok += r >= 0.85
    dif = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if op != 'equal': dif.append(f"guion «{' '.join(a[i1:i2])}» → oído «{' '.join(b[j1:j2])}»")
    out.append(f"{flag} {o['id']:<13} {r:.2f}  oído: {heard}" + (f"\n      diferencias: {'; '.join(dif)}" if dif else '')
               + (f"\n      (frase en la pista de verificación desde {t:.2f} s)" if dif else ''))
    t += dd + 2.0
out.insert(0, f"{lg}: {ok}/{len(G)} frases coinciden con el guion (similitud ≥ 0,85)")
open(f'qa/{lg}_qa.txt', 'w').write('\n'.join(out))
print('\n'.join(l for l in out if not l.startswith('OK ')))
