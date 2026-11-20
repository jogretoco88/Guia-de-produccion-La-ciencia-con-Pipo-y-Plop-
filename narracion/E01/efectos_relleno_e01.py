"""Ep. 1 · Rellena con sonidos pequeños los silencios entre frases que la pista de efectos deja vacíos.
- Los 111 efectos colocados (ElevenLabs del Ep. 3 + efectos del Ep. 2) quedan EXACTAMENTE donde estaban
  (out/efectos/E01_efectos.wav, sin tocar).
- Los rellenos se sintetizan aquí mismo con numpy (no usan ElevenLabs ni gastan créditos): marimba, gotitas,
  burbujas, campanitas, blips, madera (tic-tac) y punteos, todos en la escala pentatónica de do para que suenen
  amables y no choquen entre sí.
- Solo suenan en silencios entre frases, en tramos donde ni la voz ni los efectos originales suenan.

uso: python3 efectos_relleno.py es en fr pt hi
salida por idioma: out/<lg>/E01_XX_efectos.wav/.mp3 (originales + rellenos), E01_XX_rellenos.csv,
                   E01_XX_mezcla.wav/.mp3, relleno_resumen.json; y out/efectos/rellenos/*.wav (muestras)
"""
import sys, os, json, subprocess, csv, re
import numpy as np, soundfile as sf
from medir import envelope, SR, HOP

DUR = 300.0; N = int(round(DUR * SR))
TRAS_VOZ, ANTES_VOZ = 0.10, 0.08      # márgenes respecto a la voz
UMBRAL_VOZ = -50.0
UMBRAL_FX = -42.0                      # por debajo de esto el tramo se considera vacío de efectos
MIN_HUECO = 0.40                       # hueco libre mínimo para poner un relleno
NIVEL = -27.0                          # dBFS RMS de la parte activa: por debajo de los efectos (-20/-22)
rng = np.random.default_rng(3)

# ── sintetizador ────────────────────────────────────────────────────────────────
PENTA = [523.25, 587.33, 659.26, 783.99, 880.00, 1046.5, 1174.7, 1318.5]   # do pentatónica (C5–E6)
def t_(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.003, dec=0.2):
    t = np.arange(n) / SR
    e = np.exp(-t / dec); na = max(1, int(a * SR)); e[:na] *= np.linspace(0, 1, na)
    return e
def fade(y, f=0.02):
    n = min(len(y), int(f * SR)); y[-n:] *= np.linspace(1, 0, n); return y

def marimba(f, d=0.45):
    t = t_(d); n = len(t)
    y = (np.sin(2*np.pi*f*t) * env(n, 0.002, 0.18) + 0.35*np.sin(2*np.pi*3.93*f*t) * env(n, 0.001, 0.04)
         + 0.12*np.sin(2*np.pi*9.2*f*t) * env(n, 0.001, 0.015))
    return fade(y)
def gotita(f=900, d=0.18):             # gota: seno con barrido hacia arriba
    t = t_(d); fr = f * (1 + 1.4 * (1 - np.exp(-t / 0.025)))
    return fade(np.sin(2*np.pi*np.cumsum(fr)/SR) * env(len(t), 0.001, 0.045))
def burbujas(k=3, d=0.5):
    y = np.zeros(int(d * SR))
    for i in range(k):
        g = gotita(rng.uniform(350, 650), 0.12) * rng.uniform(0.6, 1.0)
        a = int((0.02 + i * (d - 0.15) / k + rng.uniform(0, 0.04)) * SR); y[a:a+len(g)] += g[:len(y)-a]
    return fade(y)
def campanita(notas, d=0.7, paso=0.07):
    y = np.zeros(int(d * SR)); t = t_(d)
    for i, f in enumerate(notas):
        a = int(i * paso * SR); n = len(y) - a; tt = t[:n]
        y[a:] += (np.sin(2*np.pi*2*f*tt) + 0.4*np.sin(2*np.pi*5.4*f*tt)*env(n, 0.001, 0.05)) * env(n, 0.002, 0.25) * 0.8**i
    return fade(y)
def blip(f, d=0.14, sube=True):
    t = t_(d); fr = f * (1.0 + (0.5 if sube else -0.35) * t / d)
    y = np.sign(np.sin(2*np.pi*np.cumsum(fr)/SR)) * 0.35 + np.sin(2*np.pi*np.cumsum(fr)/SR) * 0.65   # algo «electrónico»
    return fade(y * env(len(t), 0.002, 0.06))
def madera(f=1100, d=0.09):
    t = t_(d); return fade((np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*2.7*f*t)) * env(len(t), 0.0005, 0.018))
def punteo(f, d=0.5):                  # cuerda pulsada (Karplus-Strong)
    p = int(SR / f); buf = rng.uniform(-1, 1, p); y = np.zeros(int(d * SR))
    for i in range(len(y)):
        y[i] = buf[i % p]; buf[i % p] = 0.996 * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return fade(y * env(len(y), 0.001, 0.15))
def secuencia(partes, sep):
    y = np.zeros(int((sep * (len(partes) - 1)) * SR) + max(len(p) for p in partes))
    for i, p in enumerate(partes):
        a = int(i * sep * SR); y[a:a+len(p)] += p
    return y

# temas por toma: el relleno se parece a lo que pasa en la escena
TEMA = {**{k: 'agua' for k in ['C10', 'C12', 'C13', 'C15', 'C18', 'C19', 'C21', 'C22']},
        **{k: 'idea' for k in ['C03', 'C04', 'C07', 'C09', 'C16', 'C24', 'C33']},
        **{k: 'molecula' for k in ['C11', 'C17', 'C23', 'C25', 'C31']},
        **{k: 'personaje' for k in ['C02', 'C05', 'C06', 'C08', 'C14', 'C20', 'C28', 'C29', 'C30', 'C32', 'C34']},
        **{k: 'lamina' for k in ['L1', 'L2', 'L3', 'CANAL_INICIO', 'CANAL_FINAL']}}   # C01, C26, C27: marimba
def relleno(tema, largo, k):
    """Devuelve (nombre, señal) que dure como mucho `largo` s. k varía las notas."""
    nota = lambda i: PENTA[(k * 3 + i) % len(PENTA)]
    dos = largo >= 0.75
    if tema == 'agua':
        return ('burbujas', burbujas(3 if dos else 2, min(0.55, largo))) if k % 2 else ('gotitas', secuencia([gotita(800), gotita(1100)], 0.16) if dos else gotita(900))
    if tema == 'idea':
        return ('tic-tac', secuencia([madera(1100), madera(800)], 0.22)) if k % 2 else ('campanita', campanita([nota(0), nota(2), nota(4)] if dos else [nota(2)], min(0.7, largo)))
    if tema == 'molecula':
        return ('blips', secuencia([blip(nota(0)), blip(nota(2))], 0.13) if dos else blip(nota(1)))
    if tema == 'personaje':
        return ('punteo', secuencia([punteo(nota(3)), punteo(nota(5))], 0.15) if dos else punteo(nota(4), 0.35))
    if tema == 'lamina':
        return ('campanita', campanita([nota(0), nota(2), nota(4), nota(5)] if dos else [nota(1), nota(3)], min(0.8, largo)))
    return ('marimba', secuencia([marimba(nota(0)), marimba(nota(2))], 0.17) if dos else marimba(nota(1), 0.35))

def nivelar(y):
    act = y[np.abs(y) > 10 ** (-40 / 20) * np.abs(y).max()]
    rms = 20 * np.log10(np.sqrt(np.mean(act ** 2)) + 1e-9)
    y = y * 10 ** ((NIVEL - rms) / 20)
    pk = np.abs(y).max()
    return y * (0.35 / pk) if pk > 0.35 else y   # ningún relleno pasa de -9 dBFS

# ── utilidades de mezcla (iguales a efectos_montar.py) ──────────────────────────
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
MARGEN = 9.0
def duck(voz, fx):
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
def tc(t): return f"{int(t//60)}:{t%60:06.3f}"

TOMAS = [(o['id'].replace('E01_', ''), o['t0'], o['t1']) for o in json.load(open('guion.json'))['lines']]
def toma_en(t): return next(k for k, a, b in TOMAS if a <= t < b) if t < DUR else TOMAS[-1][0]

FX0 = sf.read('out/efectos/E01_efectos.wav', dtype='float32')[0][:N]       # efectos originales, intactos
fx_act = envelope(FX0) > UMBRAL_FX
os.makedirs('out/efectos/rellenos', exist_ok=True)

for lg in sys.argv[1:]:
    L = lg.upper(); D = f'out/{lg}'
    rep = json.load(open(f'{D}/informe.json'))
    voz = sf.read(f'{D}/E01_{L}_narracion.wav', dtype='float32')[0][:N]
    v_act = envelope(voz) > UMBRAL_VOZ; n = min(len(v_act), len(fx_act))
    # silencios entre frases (del final de una frase al inicio de la siguiente, medidos sobre la voz)
    bordes = [(a['fin'], b['inicio'], a['id'].replace('E01_', ''), b['id'].replace('E01_', '')) for a, b in zip(rep, rep[1:])]
    bordes.append((rep[-1]['fin'], DUR, rep[-1]['id'].replace('E01_', ''), 'fin'))
    R = np.zeros(N, dtype=np.float32); filas = []; k = 0; vacios = 0
    for f_, i_, A, B in bordes:
        m = int(((f_ + i_) / 2) / HOP)
        if v_act[min(m, n - 1)]: continue
        l = m
        while l > 0 and not v_act[l - 1]: l -= 1
        r = m
        while r < n and not v_act[r]: r += 1
        a = l * HOP + TRAS_VOZ; b = (r * HOP - ANTES_VOZ) if r < n else DUR - 0.3
        # tramos libres de efectos dentro del silencio (con 0,05 s de colchón alrededor de cada efecto)
        libre = ~fx_act[int(a / HOP):int(b / HOP)]
        libre = np.array([libre[max(0, j - 5):j + 6].all() for j in range(len(libre))]) if len(libre) else libre
        tramos = []; j = 0
        while j < len(libre):
            if libre[j]:
                s = j
                while j < len(libre) and libre[j]: j += 1
                tramos.append((a + s * HOP, a + j * HOP))
            else: j += 1
        tramos = [t for t in tramos if t[1] - t[0] >= MIN_HUECO]
        if not tramos: continue
        vacios += 1
        for ta, tb in tramos[:2]:
            p = ta + 0.02
            while tb - p >= MIN_HUECO - 0.02:        # en un hueco largo, un segundo sonido más corto y algo más suave
                primero = p == ta + 0.02
                largo = tb - p - 0.04 if primero else min(0.5, tb - p - 0.04)
                toma = toma_en(p + 0.03)
                nom, y = relleno(TEMA.get(toma, 'general'), largo, k); k += 1
                y = nivelar(y[:int(largo * SR)].copy()) * (1.0 if primero else 0.7); fade(y, 0.03)
                s0 = int(p * SR); R[s0:s0 + len(y)] += y[:N - s0]
                filas.append([len(filas) + 1, f"{p:.3f}", tc(p), toma, f"{A}→{B}", nom, f"{len(y)/SR:.2f}", f"{ta:.2f}-{tb:.2f}"])
                if lg == 'es': sf.write(f'out/efectos/rellenos/{len(filas):02d}_{toma}_{nom}.wav', y, SR, subtype='PCM_24')
                if not primero: break
                p = p + len(y) / SR + 0.35
                if tb - p < 0.55: break
    fx = FX0 + R          # sin limitador: no se suman nunca sobre un efecto (pico de rellenos <= -9 dBFS) y así nada se desplaza
    assert np.abs(fx).max() <= 0.75, np.abs(fx).max()
    sf.write(f'{D}/E01_{L}_efectos.wav', fx, SR, subtype='PCM_24')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/E01_{L}_efectos.wav', '-c:a', 'libmp3lame', '-b:a', '192k',
                    f'{D}/E01_{L}_efectos.mp3'], check=True)
    with open(f'{D}/E01_{L}_rellenos.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['n', 'segundo', 'tiempo', 'toma', 'silencio_entre', 'sonido', 'duracion_s', 'hueco_libre_s']); w.writerows(filas)
    # comprobaciones: rellenos sobre la voz y sobre los efectos originales
    rdb = envelope(R); m2 = min(len(rdb), n)
    sobre_voz = int(((rdb[:m2] > -60) & v_act[:m2]).sum()); sobre_fx = int(((rdb[:m2] > -60) & fx_act[:m2]).sum())
    # mezcla
    g = duck(voz, fx); g = np.pad(g, (0, max(0, N - len(g))), constant_values=1.0)[:N]
    mix = voz + fx * g
    tmp = f'{D}/_mix.wav'; sf.write(tmp, mix, SR, subtype='FLOAT')
    mm = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', tmp, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
                         '-f', 'null', '-'], capture_output=True, text=True).stderr
    mj = json.loads(mm[mm.rfind('{'):mm.rfind('}') + 1])
    af = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={mj['input_i']}:measured_TP={mj['input_tp']}:"
          f"measured_LRA={mj['input_lra']}:measured_thresh={mj['input_thresh']}:offset={mj['target_offset']}:linear=true,aresample={SR}")
    pr = subprocess.run(['ffmpeg', '-v', 'error', '-i', tmp, '-af', af, '-ac', '1', '-f', 'f32le', '-'], capture_output=True, check=True)
    y = np.frombuffer(pr.stdout, dtype=np.float32); z = np.zeros(N, dtype=np.float32); z[:min(N, len(y))] = y[:N]
    os.remove(tmp)
    wav = f'{D}/E01_{L}_mezcla.wav'; sf.write(wav, z, SR, subtype='PCM_24')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', wav[:-4] + '.mp3'], check=True)
    I, P = lufs(wav)
    tipos = {}
    for f in filas: tipos[f[5]] = tipos.get(f[5], 0) + 1
    Rs = dict(rellenos=len(filas), silencios_con_relleno=vacios, tipos=tipos, tramos_10ms_sobre_voz=sobre_voz,
              tramos_10ms_sobre_efectos=sobre_fx, lufs_mezcla=I, pico_mezcla=P, dur_mezcla=round(len(z) / SR, 3))
    json.dump(Rs, open(f'{D}/relleno_resumen.json', 'w'), ensure_ascii=False, indent=1)
    print(lg, json.dumps(Rs, ensure_ascii=False))
