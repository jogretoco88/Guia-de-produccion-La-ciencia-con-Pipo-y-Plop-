"""Mide cada frase: inicio y fin reales de la voz (sin silencios) y los tramos de sonido.
uso: python3 medir.py raw/es/E04_C01.mp3 [...]   -> imprime JSON por archivo
"""
import sys, json, subprocess
import numpy as np

SR = 48000
HOP = 0.01  # 10 ms

def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()

def envelope(x):
    n = int(SR * HOP)
    m = len(x) // n
    fr = x[:m * n].reshape(m, n)
    rms = np.sqrt((fr ** 2).mean(axis=1) + 1e-12)
    return 20 * np.log10(rms)

def analyse(path, gap=0.12):
    x = load(path)
    db = envelope(x)
    thr = max(-48.0, db.max() - 38.0)
    on = np.where(db > thr)[0]
    if len(on) == 0:
        return dict(file=path, error='silencio')
    a = max(0.0, on[0] * HOP - 0.03)
    b = min(len(x) / SR, (on[-1] + 1) * HOP + 0.08)
    # tramos de sonido separados por pausas >= gap
    segs = []
    s = on[0]; p = on[0]
    for i in on[1:]:
        if (i - p) * HOP >= gap:
            segs.append((round(s * HOP, 3), round((p + 1) * HOP, 3))); s = i
        p = i
    segs.append((round(s * HOP, 3), round((p + 1) * HOP, 3)))
    return dict(file=path, total=round(len(x) / SR, 3), start=round(a, 3), end=round(b, 3),
                speech=round(b - a, 3), segs=segs)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(json.dumps(analyse(p), ensure_ascii=False))
