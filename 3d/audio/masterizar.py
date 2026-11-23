# Recorta silencios, iguala el nivel y exporta WAV 48 kHz / 24 bit mono.
# Uso: python3 3d/audio/masterizar.py carpeta_con_mp3 carpeta_de_salida
# Deja en la carpeta padre de la salida un niveles.csv con las medidas de cada toma.
import sys, os, subprocess, numpy as np, csv
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
SR = 48000; PAD = int(0.06 * SR); TARGET = -20.0; CEIL = -1.5   # dBFS RMS de la voz; techo de pico
def load(f):
    raw = subprocess.run(["ffmpeg","-v","quiet","-i",f,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()
def db(x): return 20*np.log10(max(x,1e-9))
rows=[]
for f in sorted(os.listdir(src)):
    if not f.endswith(".mp3"): continue
    x = load(os.path.join(src,f))
    w = int(0.01*SR); env = np.sqrt(np.convolve(x**2, np.ones(w)/w, "same"))
    thr = max(env.max()*10**(-40/20), 10**(-55/20))
    idx = np.where(env > thr)[0]
    a, b = max(idx[0]-PAD,0), min(idx[-1]+PAD, len(x))
    y = x[a:b]
    ey = env[a:b]; voiced = y[ey > env.max()*10**(-25/20)]
    rms = db(np.sqrt(np.mean(voiced**2)))
    g = TARGET - rms
    peak = db(np.abs(y).max()) + g
    if peak > CEIL: g -= peak - CEIL            # el pico manda si se pasa
    y = y * 10**(g/20)
    fi = int(0.005*SR); y[:fi] *= np.linspace(0,1,fi); y[-fi:] *= np.linspace(1,0,fi)
    name = f[:-4] + ".wav"
    subprocess.run(["ffmpeg","-v","quiet","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-c:a","pcm_s24le",os.path.join(out,name)],input=y.astype(np.float32).tobytes())
    rows.append([f[:-4], round(len(x)/SR,2), round(len(y)/SR,2), round(rms,1), round(g,1), round(db(np.abs(y).max()),1), round(db(np.sqrt(np.mean(y[np.abs(y)>0]**2))),1)])
with open(os.path.join(out,"..","niveles.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["toma","dur_original_s","dur_final_s","rms_voz_dbfs","ganancia_db","pico_dbfs","rms_final_dbfs"]); w.writerows(rows)
for r in rows: print(*r, sep="\t")
