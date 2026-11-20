"""Monta la pista de efectos del Ep. 1 y las mezclas narración + efectos por idioma.
uso: python3 efectos_montar.py            -> out/efectos/ (pista de efectos, biblioteca, hoja de entradas)
     python3 efectos_montar.py es en ...  -> además out/<lg>/E01_XX_mezcla.wav/.mp3
Lee efectos.json (de efectos_e01.py) y sfx_raw/<efecto>.mp3 (ElevenLabs SFX v3 del Ep. 3 + efectos del Ep. 2).
"""
import sys, os, json, subprocess, csv
import numpy as np, soundfile as sf
from medir import load, envelope, SR, HOP

E = json.load(open('efectos.json')); LIB, CUES = E['lib'], E['cues']
DUR = 300.0
N = int(round(DUR * SR))
# nivel de cada categoría (RMS de la parte activa, dBFS) antes de la ganancia de cada entrada.
# La voz queda a -16 LUFS; los efectos van por debajo para no tapar la narración.
NIVEL = dict(F=-22.0, M=-20.0, T=-20.0)
CAT = dict(F='Foley de movimiento y textura', M='Acento de expresión (mickey mousing)', T='Transición / refuerzo visual')
OUT = 'out/efectos'; os.makedirs(OUT + '/biblioteca', exist_ok=True)

def preparar(nombre):
    """Recorta el sonido desde su primer ataque, limita la duración y le pone fundidos."""
    x = load(LIB[nombre]['archivo']); d = LIB[nombre]
    db = envelope(x); thr = max(-60.0, db.max() - 30.0)
    on = np.where(db > thr)[0]
    a = max(0, int((on[0] * HOP - 0.01) * SR)) if len(on) else 0
    y = x[a:a + int(d['max'] * SR)].copy()
    fi = int(0.004 * SR); fo = max(int(0.04 * SR), int(len(y) * 0.25))
    y[:fi] *= np.linspace(0, 1, fi)
    y[-fo:] *= np.linspace(1, 0, fo) ** 1.5
    act = y[np.abs(y) > 10 ** (-40 / 20)]
    rms = 20 * np.log10(np.sqrt(np.mean(act ** 2)) + 1e-9) if len(act) else -60
    y *= 10 ** ((NIVEL[d['cat']] - rms) / 20)
    pk = np.abs(y).max()
    if pk > 0.7: y *= 0.7 / pk          # ningún efecto suelto pasa de -3 dBFS
    return y

def limitar(x, lim):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af',
                        f'alimiter=limit={lim}:attack=2:release=80:level=false', '-f', 'f32le', '-'],
                       input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    y = np.frombuffer(p.stdout, dtype=np.float32).copy()
    return y[:len(x)] if len(y) >= len(x) else np.pad(y, (0, len(x) - len(y)))

def lufs(path):
    m = subprocess.run(['ffmpeg', '-nostats', '-i', path, '-af', 'ebur128=peak=true:framelog=quiet', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    import re
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', m)[-1])

# 1) biblioteca y pista de efectos
S = {k: preparar(k) for k in LIB}
for k, y in S.items():
    sf.write(f"{OUT}/biblioteca/{LIB[k]['cat']}_{k}.wav", y, SR, subtype='PCM_24')
fx = np.zeros(N, dtype=np.float32)
filas = []
for i, c in enumerate(CUES, 1):
    y = S[c['efecto']] * 10 ** (c['db'] / 20)
    a = int(round(c['t'] * SR)); b = min(N, a + len(y))
    fx[a:b] += y[:b - a]
    filas.append([i, f"{c['t']:.3f}", f"{int(c['t']//60)}:{c['t']%60:06.3f}", c['toma'], c['cat'], CAT[c['cat']],
                  c['efecto'], f"{len(y)/SR:.2f}", c['db'], c['accion'], LIB[c['efecto']]['fuente'], LIB[c['efecto']]['prompt']])
fx = limitar(fx, 0.71)                  # pista de efectos con picos <= -3 dBFS
sf.write(f'{OUT}/E01_efectos.wav', fx, SR, subtype='PCM_24')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/E01_efectos.wav', '-c:a', 'libmp3lame', '-b:a', '192k',
                f'{OUT}/E01_efectos.mp3'], check=True)
with open(f'{OUT}/E01_hoja_de_efectos.csv', 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['n', 'segundo', 'tiempo', 'toma', 'cat', 'categoria', 'efecto', 'duracion_s', 'ganancia_db', 'accion_en_pantalla', 'fuente', 'descripcion'])
    w.writerows(filas)
cnt = {k: sum(1 for c in CUES if c['cat'] == k) for k in 'FMT'}
uni = {k: len({c['efecto'] for c in CUES if c['cat'] == k}) for k in 'FMT'}
I, P = lufs(f'{OUT}/E01_efectos.wav')
print(f'efectos: {len(CUES)} entradas (F {cnt["F"]}/{uni["F"]} únicos, M {cnt["M"]}/{uni["M"]}, T {cnt["T"]}/{uni["T"]}) · {I} LUFS · pico {P} dBFS')
json.dump(dict(entradas=cnt, unicos=uni, lufs=I, pico=P), open(f'{OUT}/resumen.json', 'w'))

# 2) mezclas por idioma: la voz manda. Mientras hay voz, los efectos bajan al menos 4 dB y nunca quedan
#    a menos de 9 dB por debajo de la voz (compresión por cadena lateral, ventanas de 10 ms)
MARGEN = 9.0
def duck(voz, fx):
    vdb = envelope(voz); fdb = envelope(fx); n = min(len(vdb), len(fdb)); vdb, fdb = vdb[:n], fdb[:n]
    k = int(0.25 / HOP)                        # la voz «sigue activa» 250 ms tras cada sílaba
    vmax = np.array([vdb[max(0, i - k):i + 7].max() for i in range(n)])   # y 60 ms antes de que empiece
    activo = vmax > -45
    g = np.zeros(n)
    g[activo] = np.minimum(-4.0, (vmax[activo] - MARGEN) - fdb[activo])
    g = np.minimum(g, 0.0)
    g = np.array([g[i:i + 5].min() for i in range(n)])   # mira 50 ms adelante: baja antes del golpe
    out = np.empty(n); v = 0.0
    for i, t in enumerate(g):                 # ataque ~20 ms, salida ~300 ms
        c = 0.6 if t < v else 0.033
        v += (t - v) * c; out[i] = v
    return np.repeat(10 ** (out / 20), int(SR * HOP))

for lg in sys.argv[1:]:
    L = lg.upper()
    voz = sf.read(f'out/{lg}/E01_{L}_narracion.wav', dtype='float32')[0]
    g = duck(voz[:N], fx); g = np.pad(g, (0, max(0, N - len(g))), constant_values=1.0)[:N]
    mix = voz[:N] + fx * g
    tmp = f'out/{lg}/_mix.wav'; sf.write(tmp, mix, SR, subtype='FLOAT')
    m = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', tmp, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
                        '-f', 'null', '-'], capture_output=True, text=True).stderr
    mj = json.loads(m[m.rfind('{'):m.rfind('}') + 1])
    af = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={mj['input_i']}:measured_TP={mj['input_tp']}:"
          f"measured_LRA={mj['input_lra']}:measured_thresh={mj['input_thresh']}:offset={mj['target_offset']}:linear=true,aresample={SR}")
    p = subprocess.run(['ffmpeg', '-v', 'error', '-i', tmp, '-af', af, '-ac', '1', '-f', 'f32le', '-'], capture_output=True, check=True)
    y = np.frombuffer(p.stdout, dtype=np.float32); z = np.zeros(N, dtype=np.float32); z[:min(N, len(y))] = y[:N]
    os.remove(tmp)
    wav = f'out/{lg}/E01_{L}_mezcla.wav'; sf.write(wav, z, SR, subtype='PCM_24')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', wav[:-4] + '.mp3'], check=True)
    I, P = lufs(wav)
    print(f'{lg}: mezcla {len(z)/SR:.3f} s · {I} LUFS · pico {P} dBFS')
