"""Ajusta y monta la narración de un idioma sobre los tiempos del video.
uso: python3 montar.py es
Lee guion.json, raw/<lg>/*.mp3 y (si existe) anclas/<lg>.json = {id: [t_hic1, t_hic2...]}
(segundos dentro del mp3 original, medidos con la transcripción palabra a palabra).
Escribe out/<lg>/: frases/*.wav, pista WAV+MP3, SRT, informe.json
"""
import sys, json, os, re, subprocess
import numpy as np
from medir import analyse, load, SR

LG = sys.argv[1]
G = json.load(open('guion.json'))['lines']
VIDEO_END = 300.0
ANC = json.load(open(f'anclas/{LG}.json')) if os.path.exists(f'anclas/{LG}.json') else {}
MAXT = 1.08          # aceleración máxima permitida (imperceptible)
GAP = 0.15           # silencio mínimo entre frases
TARGET_LUFS = -15.3  # nivel de cada frase -> pista ≈ -16 LUFS integrados
OUT = f'out/{LG}'; os.makedirs(OUT + '/frases', exist_ok=True)
spoken = lambda t: re.sub(r'\[[^\]]*\]\s*', '', t).strip()

def lufs_gain(x):
    # loudness aproximada (K-weighting omitido; RMS de tramos activos) -> ganancia lineal
    n = int(SR * 0.4); h = n // 4
    blocks = [x[i:i + n] for i in range(0, max(1, len(x) - n), h)]
    e = np.array([np.mean(b ** 2) for b in blocks if len(b)])
    e = e[e > 1e-7]
    if not len(e): return 1.0
    l = 10 * np.log10(np.mean(e[e > np.mean(e) * 0.1]))
    return 10 ** ((TARGET_LUFS - l) / 20)

def atempo(x, f):
    if abs(f - 1) < 1e-3: return x
    p = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-',
                        '-af', f'atempo={f:.4f}', '-f', 'f32le', '-'], input=x.tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.float32).copy()

def limit(x):
    # limitador suave a -1.5 dBFS (sin recortar picos de golpe)
    p = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-',
                        '-af', 'alimiter=limit=0.84:attack=3:release=60:level=false', '-f', 'f32le', '-'],
                       input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    y = np.frombuffer(p.stdout, dtype=np.float32).copy()
    return y[:len(x)] if len(y) >= len(x) else np.pad(y, (0, len(x) - len(y)))

def fade(x, ms=12):
    n = int(SR * ms / 1000); x = x.copy()
    if len(x) > 2 * n:
        x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
    return x

track = np.zeros(int(round(VIDEO_END * SR)), dtype=np.float32)
rep = []; prev_end = 0.0; srt = []
for o in G:
    sid = o['id']; t0 = o['t0']; lo, hi = o['win']
    f = f'raw/{LG}/{sid}.mp3'
    a = analyse(f); x = load(f)
    s0, s1 = a['start'], a['end']
    clip = x[int(s0 * SR):int(s1 * SR)]
    g = lufs_gain(clip); clip = limit(clip * g)
    anchors = o['anchors']; hics = ANC.get(sid, [])
    pieces = []  # (audio, onset absoluto)
    if anchors and anchors[0][0] == 'START':
        pieces.append([clip, t0 + anchors[0][1] - 0.03])
    elif anchors and len(anchors) == 2 and len(hics) >= 2:
        # dos anclas (C25): se corta en el silencio entre el 1er hip y lo que sigue
        h1, h2 = hics[0] - s0, hics[1] - s0
        segs = [(b - s0, e - s0) for b, e in a['segs']]
        cut = next(e for b, e in segs if e >= h1 + 0.05)  # fin del tramo que contiene el 1er hip
        nxt = next(b for b, e in segs if b > cut)
        ca, cb = cut + 0.06, nxt - 0.03   # se quita la pausa sobrante entre los dos hip
        A, B = clip[:int(ca * SR)], clip[int(cb * SR):]
        pieces.append([A, t0 + anchors[0][1] - h1])
        pieces.append([B, t0 + anchors[1][1] - (h2 - cb)])
    elif anchors and hics:
        pieces.append([clip, t0 + anchors[0][1] - (hics[0] - s0)])
    else:
        pieces.append([clip, t0 + lo])
    win_end = t0 + hi
    status = 'ok'; tempo = 1.0
    # no pisar la frase anterior
    if pieces[0][1] < prev_end + GAP:
        pieces[0][1] = prev_end + GAP; status = 'desplazada'
    end = pieces[-1][1] + len(pieces[-1][0]) / SR
    if end > win_end:
        if len(pieces) == 1 and not anchors:
            tempo = len(clip) / SR / (win_end - pieces[0][1])
        elif len(pieces) == 1:
            tempo = (end - pieces[0][1]) / (win_end - pieces[0][1])
        else:
            tempo = len(pieces[-1][0]) / SR / (win_end - pieces[-1][1])
        if tempo > MAXT:
            status = f'LARGA (necesita {tempo:.3f}x)'; tempo = MAXT
        pieces[-1][0] = atempo(pieces[-1][0], tempo)
        lim = int((win_end - pieces[-1][1]) * SR)   # el redondeo de atempo no debe salirse ni 1 ms
        if len(pieces[-1][0]) > lim > 0: pieces[-1][0] = pieces[-1][0][:lim]
    if len(pieces) == 2 and pieces[1][1] < pieces[0][1] + len(pieces[0][0]) / SR + 0.08:
        pieces[1][1] = pieces[0][1] + len(pieces[0][0]) / SR + 0.08; status = 'ancla2 desplazada'
    out_parts = []
    for au, on in pieces:
        au = fade(au); i = int(round(on * SR))
        track[i:i + len(au)] += au[:max(0, len(track) - i)]
        out_parts.append((round(on, 3), round(on + len(au) / SR, 3)))
    on0, endN = out_parts[0][0], out_parts[-1][1]
    # archivo suelto: la frase lista (con el corte/aceleración ya aplicados), y su posición
    prev_end = endN
    rep.append(dict(id=sid, inicio=on0, fin=endN, ventana=[round(t0 + lo, 3), round(win_end, 3)],
                    tempo=round(tempo, 3), estado=status, partes=out_parts,
                    dentro=bool(endN <= win_end + 0.01 and on0 >= t0 - 1e-3)))
    srt.append((on0, endN, spoken(o[LG])))

# nivel final: loudnorm EBU R128 en dos pasadas -> -16 LUFS, pico verdadero <= -1.5 dBTP (no cambia tiempos)
import soundfile as sf
tmp = f'{OUT}/_tmp.wav'; sf.write(tmp, track, SR, subtype='FLOAT')
m = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', tmp, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
                    '-f', 'null', '-'], capture_output=True, text=True).stderr
mj = json.loads(m[m.rfind('{'):m.rfind('}') + 1])
af = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={mj['input_i']}:measured_TP={mj['input_tp']}:"
      f"measured_LRA={mj['input_lra']}:measured_thresh={mj['input_thresh']}:offset={mj['target_offset']}:linear=true,"
      f"aresample={SR}")
p = subprocess.run(['ffmpeg', '-v', 'error', '-i', tmp, '-af', af, '-ac', '1', '-f', 'f32le', '-'], capture_output=True, check=True)
y = np.frombuffer(p.stdout, dtype=np.float32)
track = np.zeros_like(track); track[:min(len(y), len(track))] = y[:len(track)]
os.remove(tmp)
for r in rep:                                   # archivos sueltos = cortes exactos de la pista final
    seg = track[int(round(r['inicio'] * SR)):int(round(r['fin'] * SR))]
    sf.write(f"{OUT}/frases/E03_{LG.upper()}_{r['id'].replace('E03_','')}.wav", seg, SR, subtype='PCM_24')
wav = f'{OUT}/E03_{LG.upper()}_narracion.wav'
sf.write(wav, track, SR, subtype='PCM_24')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', wav[:-4] + '.mp3'], check=True)
def tc(t):
    ms = int(round(t * 1000)); return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
open(f'{OUT}/E03_{LG.upper()}_subtitulos.srt', 'w').write(
    '\n'.join(f'{i+1}\n{tc(a)} --> {tc(b)}\n{t}\n' for i, (a, b, t) in enumerate(srt)))
with open(f'{OUT}/E03_{LG.upper()}_posiciones.csv', 'w') as fh:
    fh.write('toma,archivo,inicio_s,fin_s,tempo\n')
    for r in rep: fh.write(f"{r['id']},E03_{LG.upper()}_{r['id'].replace('E03_','')}.wav,{r['inicio']:.3f},{r['fin']:.3f},{r['tempo']}\n")
json.dump(rep, open(f'{OUT}/informe.json', 'w'), ensure_ascii=False, indent=1)
bad = [r for r in rep if not r['dentro'] or r['estado'].startswith('LARGA')]
sped = [f"{r['id']}x{r['tempo']}" for r in rep if r['tempo'] > 1]
print(LG, 'frases', len(rep), '| fuera de ventana:', [(r['id'], r['estado']) for r in bad] or 'ninguna',
      '| aceleradas:', sped or 'ninguna', '| duración pista %.3f s' % (len(track) / SR))
