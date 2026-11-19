"""Ep. 3 · Reubica los 106 efectos en los silencios entre frase y frase de cada idioma.
No genera sonidos nuevos: usa los mismos sfx_raw/<efecto>.mp3 (ElevenLabs Sound Effects v3) y la misma
narración out/<lg>/E03_XX_narracion.wav. Solo cambia el segundo en que suena cada efecto (y, si el silencio
es más corto que el sonido, lo recorta con un fundido).

uso: python3 efectos_silencios.py es en fr pt hi
salida por idioma: out/<lg>/E03_XX_efectos.wav/.mp3, E03_XX_hoja_de_efectos.csv, E03_XX_mezcla.wav/.mp3, efectos_resumen.json

Reglas
- Silencio útil = hueco entre el final de una frase y el inicio de la siguiente (más el inicio y el final del video),
  medido sobre la voz real (envolvente de 10 ms, umbral -50 dBFS), dejando 0,08 s tras la voz y 0,06 s antes de la siguiente.
- Cada efecto solo puede ir a un silencio de su propia toma: desde 0,15 s antes del corte que la abre hasta 0,35 s
  después del corte que la cierra. Así nunca suena sobre otra escena.
- Va al silencio más cercano a su acción. Si en un silencio no caben todos, el que menos se aleja pasa al otro silencio
  de su toma; si tampoco cabe, se juntan más (capas) y se recortan con fundido, sin bajar de 0,15 s.
- Dentro de un silencio, los efectos conservan su orden; si su acción ocurrió durante la frase anterior suenan nada más
  terminar la voz, si ocurre durante la siguiente suenan justo antes de que vuelva la voz.
"""
import sys, os, json, subprocess, csv, re
import numpy as np, soundfile as sf
from medir import load, envelope, SR, HOP

E = json.load(open('efectos.json')); LIB, CUES = E['lib'], E['cues']
DUR = 300.0; N = int(round(DUR * SR))
NIVEL = dict(F=-22.0, M=-20.0, T=-20.0)
CAT = dict(F='Foley de movimiento y textura', M='Acento de expresión (mickey mousing)', T='Transición / refuerzo visual')
TRAS_VOZ, ANTES_VOZ = 0.08, 0.06      # márgenes respecto a la voz
PASO_MIN = 0.12                       # separación mínima entre dos ataques
UMBRAL = -50.0

def preparar(nombre):                 # idéntico a efectos_montar.py
    x = load(f'sfx_raw/{nombre}.mp3'); d = LIB[nombre]
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
    if pk > 0.7: y *= 0.7 / pk
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
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', m)[-1])

def tc(t): return f"{int(t//60)}:{t%60:06.3f}"

S = {k: preparar(k) for k in LIB}
DLEN = {k: len(v) / SR for k, v in S.items()}
TOMA = {o['id'].replace('E03_', ''): (o['t0'], o['t1']) for o in json.load(open('guion.json'))['lines']}
ANTICIPO, ARRASTRE = 0.15, 0.35       # un efecto puede sonar 0,15 s antes del corte de su toma y hasta 0,35 s después de que acabe
def dmin(c, w=9.0, piso=0.22, frac=0.4):        # lo mínimo que puede durar un efecto si hay que recortarlo
    d = DLEN[c['efecto']]
    return min(d, max(piso, min(1.0, frac * d)), w)

def silencios(lg):
    rep = json.load(open(f'out/{lg}/informe.json'))
    voz = sf.read(f'out/{lg}/E03_{lg.upper()}_narracion.wav', dtype='float32')[0]
    act = envelope(voz) > UMBRAL; n = len(act)
    bordes = [(0.0, rep[0]['inicio'])] + [(a['fin'], b['inicio']) for a, b in zip(rep, rep[1:])] + [(rep[-1]['fin'], DUR)]
    nombres = ['inicio'] + [f"{a['id'].replace('E03_','')}→{b['id'].replace('E03_','')}" for a, b in zip(rep, rep[1:])] + ['final']
    G = []
    for (f, i), nom in zip(bordes, nombres):
        m = int(((f + i) / 2) / HOP)
        if act[min(m, n - 1)]: continue
        l = m
        while l > 0 and not act[l - 1]: l -= 1
        r = m
        while r < n and not act[r]: r += 1
        a = 0.0 if l == 0 else l * HOP + TRAS_VOZ
        b = DUR if r >= n else r * HOP - ANTES_VOZ
        if b - a >= 0.2: G.append(dict(a=round(a, 3), b=round(b, 3), nombre=nom))
    return G, voz

def ventana(c, g):
    s0, s1 = TOMA[c['toma']]
    return max(g['a'], s0 - ANTICIPO), min(g['b'], s1 + ARRASTRE)

def programar(cs, paso=PASO_MIN, piso=0.22, frac=0.4):
    """cs: [(efecto, lo, hi)] ordenados. Ataques dentro de sus ventanas, en orden; None si no caben."""
    if not cs: return []
    p = []
    for k, (c, lo, hi) in enumerate(cs):
        want = min(max(c['t'], lo), hi - dmin(c, hi - lo, piso, frac))
        if k: want = max(want, p[-1] + max(paso, min(DLEN[cs[k-1][0]['efecto']], 0.45)))
        p.append(want)
    for k in range(len(cs) - 1, -1, -1):          # hacia atrás: que todo termine antes de la voz
        c, lo, hi = cs[k]
        lim = hi - dmin(c, hi - lo, piso, frac)
        if k < len(cs) - 1: lim = min(lim, p[k + 1] - paso)
        p[k] = min(p[k], lim)
    return p if all(p[k] >= cs[k][1] - 1e-6 for k in range(len(cs))) else None

def coste(c, lo, hi): return max(lo - c['t'], c['t'] - (hi - dmin(c, hi - lo)), 0.0)

# (separación mínima entre ataques, duración mínima, fracción mínima del sonido que se conserva).
# Primero se intenta conservar el 75 % de cada sonido; solo si no cabe ni moviéndolo al otro silencio de su toma se aprieta más.
COMPRESION = [(0.15, 0.25, 0.75), (PASO_MIN, 0.22, 0.4), (0.08, 0.18, 0.25), (0.05, 0.15, 0.15)]
def asignar(G):
    cand = []
    for c in CUES:
        op = [(j,) + ventana(c, g) for j, g in enumerate(G)]
        op = [o for o in op if o[2] - o[1] >= 0.15]
        cand.append(sorted(op, key=lambda o: coste(c, o[1], o[2])))
        assert cand[-1], c
    sel = [0] * len(CUES); nivel = [0] * len(G)
    def grupo(j):
        idx = sorted([i for i in range(len(CUES)) if cand[i][sel[i]][0] == j], key=lambda i: (CUES[i]['t'], i))
        return idx, [(CUES[i],) + cand[i][sel[i]][1:] for i in idx]
    while True:
        cambio = False
        for j in range(len(G)):
            idx, cs = grupo(j)
            if programar(cs, *COMPRESION[nivel[j]]) is not None: continue
            movibles = [i for i in idx if sel[i] + 1 < len(cand[i])]
            if movibles:                           # sale el que menos se aleja al pasar a otro silencio de su toma
                i = min(movibles, key=lambda i: coste(CUES[i], *cand[i][sel[i] + 1][1:]) - coste(CUES[i], *cand[i][sel[i]][1:]))
                sel[i] += 1
            elif nivel[j] + 1 < len(COMPRESION):   # si nadie puede salir, se juntan más (capas)
                nivel[j] += 1
            else:
                raise SystemExit(f"no caben en {G[j]['nombre']}: {[c[0]['efecto'] for c in cs]}")
            cambio = True
        if not cambio: break
    plan = []
    for j in range(len(G)):
        idx, cs = grupo(j)
        for i, p, (c, lo, hi) in zip(idx, programar(cs, *COMPRESION[nivel[j]]), cs):
            plan.append((i, j, p, hi))
    return sorted(plan, key=lambda x: x[2])

MARGEN = 9.0
def duck(voz, fx):                    # misma red de seguridad que antes (ya casi no actúa: no hay solapes)
    vdb = envelope(voz); fdb = envelope(fx); n = min(len(vdb), len(fdb)); vdb, fdb = vdb[:n], fdb[:n]
    k = int(0.25 / HOP)
    vmax = np.array([vdb[max(0, i - k):i + 7].max() for i in range(n)])
    activo = vmax > -45
    g = np.zeros(n)
    g[activo] = np.minimum(-4.0, (vmax[activo] - MARGEN) - fdb[activo])
    g = np.minimum(g, 0.0)
    g = np.array([g[i:i + 5].min() for i in range(n)])
    out = np.empty(n); v = 0.0
    for i, t in enumerate(g):
        c = 0.6 if t < v else 0.033
        v += (t - v) * c; out[i] = v
    return np.repeat(10 ** (out / 20), int(SR * HOP))

for lg in sys.argv[1:]:
    L = lg.upper(); D = f'out/{lg}'
    G, voz = silencios(lg)
    plan = asignar(G)
    assert len(plan) == len(CUES), (lg, len(plan))
    fx = np.zeros(N, dtype=np.float32); filas = []; despl = []; recortes = 0
    for n_, (i, j, p, hi) in enumerate(plan, 1):
        c = CUES[i]; g = G[j]
        y = S[c['efecto']] * 10 ** (c['db'] / 20)
        largo = min(len(y), int((hi - p) * SR))
        if largo < len(y):                      # recorte con fundido para que acabe antes de la voz
            recortes += 1; y = y[:largo].copy()
            fo = max(int(0.05 * SR), int(largo * 0.3)); y[-fo:] *= np.linspace(1, 0, fo) ** 1.5
        a = int(round(p * SR)); b = min(N, a + len(y))
        fx[a:b] += y[:b - a]
        despl.append(p - c['t'])
        filas.append([n_, f"{p:.3f}", tc(p), f"{c['t']:.3f}", f"{p - c['t']:+.2f}", c['toma'], g['nombre'],
                      f"{g['a']:.2f}-{g['b']:.2f}", c['cat'], CAT[c['cat']], c['efecto'], f"{len(y)/SR:.2f}",
                      c['db'], c['accion'], LIB[c['efecto']]['prompt']])
    fx = limitar(fx, 0.71)
    sf.write(f'{D}/E03_{L}_efectos.wav', fx, SR, subtype='PCM_24')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/E03_{L}_efectos.wav', '-c:a', 'libmp3lame', '-b:a', '192k',
                    f'{D}/E03_{L}_efectos.mp3'], check=True)
    with open(f'{D}/E03_{L}_hoja_de_efectos.csv', 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['n', 'segundo', 'tiempo', 'segundo_accion', 'desplazamiento_s', 'toma', 'silencio', 'silencio_s',
                    'cat', 'categoria', 'efecto', 'duracion_s', 'ganancia_db', 'accion_en_pantalla', 'prompt_sfx_v3'])
        w.writerows(filas)
    # comprobación: energía de efectos que cae mientras habla el narrador
    vact = envelope(voz[:N]) > UMBRAL; fdb = envelope(fx); m = min(len(vact), len(fdb))
    fe = 10 ** (fdb[:m] / 10); solape = float(fe[vact[:m]].sum() / fe.sum() * 100)
    fr_solape = int(((fdb[:m] > -50) & vact[:m]).sum())
    # mezcla
    g = duck(voz[:N], fx); g = np.pad(g, (0, max(0, N - len(g))), constant_values=1.0)[:N]
    mix = voz[:N] + fx * g
    tmp = f'{D}/_mix.wav'; sf.write(tmp, mix, SR, subtype='FLOAT')
    mm = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', tmp, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
                         '-f', 'null', '-'], capture_output=True, text=True).stderr
    mj = json.loads(mm[mm.rfind('{'):mm.rfind('}') + 1])
    af = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={mj['input_i']}:measured_TP={mj['input_tp']}:"
          f"measured_LRA={mj['input_lra']}:measured_thresh={mj['input_thresh']}:offset={mj['target_offset']}:linear=true,aresample={SR}")
    pr = subprocess.run(['ffmpeg', '-v', 'error', '-i', tmp, '-af', af, '-ac', '1', '-f', 'f32le', '-'], capture_output=True, check=True)
    y = np.frombuffer(pr.stdout, dtype=np.float32); z = np.zeros(N, dtype=np.float32); z[:min(N, len(y))] = y[:N]
    os.remove(tmp)
    wav = f'{D}/E03_{L}_mezcla.wav'; sf.write(wav, z, SR, subtype='PCM_24')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', wav[:-4] + '.mp3'], check=True)
    I, P = lufs(wav); Ie, Pe = lufs(f'{D}/E03_{L}_efectos.wav')
    usados = sorted({x[1] for x in plan})
    ad = np.abs(despl)
    R = dict(entradas={k: sum(1 for c in CUES if c['cat'] == k) for k in 'FMT'},
             unicos={k: len({c['efecto'] for c in CUES if c['cat'] == k}) for k in 'FMT'},
             silencios=len(G), silencios_usados=len(usados), silencio_total_s=round(sum(g['b'] - g['a'] for g in G), 1),
             desplazamiento_medio_s=round(float(ad.mean()), 2), desplazamiento_mediana_s=round(float(np.median(ad)), 2),
             desplazamiento_max_s=round(float(ad.max()), 2), recortados=recortes,
             energia_bajo_voz_pct=round(solape, 3), tramos_10ms_con_solape=fr_solape,
             lufs_efectos=Ie, pico_efectos=Pe, lufs_mezcla=I, pico_mezcla=P, dur_mezcla=round(len(z) / SR, 3))
    json.dump(R, open(f'{D}/efectos_resumen.json', 'w'), ensure_ascii=False, indent=1)
    print(lg, json.dumps(R, ensure_ascii=False))
