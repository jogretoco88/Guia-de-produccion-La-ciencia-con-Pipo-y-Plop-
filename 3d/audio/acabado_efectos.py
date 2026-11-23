# Acabado de efectos: golpes (ataque exacto, cola con fundido, filtro de graves, nivel) y ambientes
# en bucle (tope de pico, verificación del empalme y cama de 60 s con fundidos cruzados).
# Uso: python3 3d/audio/acabado_efectos.py carpeta_mp3 carpeta_salida meta.json
import sys, os, subprocess, numpy as np, csv, json
src, out, meta = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
SR = 48000
os.makedirs(out, exist_ok=True)
def load(f):
    raw = subprocess.run(["ffmpeg","-v","quiet","-i",f,"-af","highpass=f=30,aresample=48000:resampler=soxr","-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
def db(v): return 20*np.log10(max(float(v),1e-9))
def save(y, path):
    ch = y.shape[1]
    subprocess.run(["ffmpeg","-v","quiet","-y","-f","f32le","-ar",str(SR),"-ac",str(ch),"-i","-","-c:a","pcm_s24le",path],input=np.ascontiguousarray(y,np.float32).tobytes())
rows=[]
for f in sorted(os.listdir(src)):
    if not f.endswith(".mp3"): continue
    code, var = f[:2], f[3:5]
    m = meta[code]; x = load(os.path.join(src,f))
    raw_peak = np.abs(x).max(); clip = int((np.abs(x)>0.995).sum())
    corr = float(np.corrcoef(x[:,0],x[:,1])[0,1]) if x[:,0].std()>0 and x[:,1].std()>0 else 1.0
    if corr > 0.97: x = x.mean(axis=1, keepdims=True)          # estéreo falso → mono
    mono = x.mean(axis=1)
    w = int(0.005*SR); env = np.sqrt(np.convolve(mono**2, np.ones(w)/w, "same"))
    if m["tipo"] == "oneshot":
        thr = env.max()*10**(-45/20)
        idx = np.where(env>thr)[0]; a = max(idx[0]-int(0.003*SR),0); b = min(idx[-1]+int(0.04*SR), len(x))
        y = x[a:b].copy()
        act = y[np.sqrt(np.convolve(y.mean(axis=1)**2,np.ones(w)/w,"same")) > env.max()*10**(-20/20)]
        rms = db(np.sqrt(np.mean(act**2))); g = m["rms"] - rms
        pk = db(np.abs(y).max()) + g
        if pk > -3: g -= pk + 3
        y *= 10**(g/20)
        fi = int(0.002*SR); fo = min(int(0.03*SR), len(y)//4)
        y[:fi] *= np.linspace(0,1,fi)[:,None]; y[-fo:] *= np.linspace(1,0,fo)[:,None]
        seam = None
    else:
        y = x.copy()
        rms = db(np.sqrt(np.mean(y**2))); g = m["rms"] - rms
        pk = db(np.abs(y).max()) + g
        if pk > -3: g -= pk + 3                                   # tope de pico también en ambientes
        y *= 10**(g/20)
        n = int(0.01*SR)
        seam = db(abs(np.sqrt(np.mean(y[-n:]**2)) - np.sqrt(np.mean(y[:n]**2))) + 1e-9) - db(np.sqrt(np.mean(y**2)))
        jump = float(np.abs(y[-1]-y[0]).max())
        xf = int(0.5*SR); t = np.linspace(0,np.pi/2,xf)[:,None]   # fundido cruzado de igual potencia
        bed = y.copy()
        while len(bed) < 60*SR + xf:
            bed = np.concatenate([bed[:-xf], bed[-xf:]*np.cos(t) + y[:xf]*np.sin(t), y[xf:]])
        bed = bed[:60*SR]
        f2 = int(1.0*SR); bed[:f2] *= np.linspace(0,1,f2)[:,None]; bed[-f2:] *= np.linspace(1,0,f2)[:,None]
        save(bed, os.path.join(out, f"{m['nombre']}_{var}_cama60s.wav"))
    name = f"{m['nombre']}_{var}.wav"
    save(y, os.path.join(out, name))
    rows.append([name, m["tipo"], round(len(y)/SR,2), "mono" if y.shape[1]==1 else "estéreo", round(db(raw_peak),1), clip,
                 round(g,1), round(db(np.abs(y).max()),1), round(db(np.sqrt(np.mean(y**2))),1), "" if seam is None else round(seam,1),
                 "DESCARTADA: casi silencio" if db(raw_peak) < -40 else ("subida fuerte: posible ruido de fondo" if g > 20 else "")])
with open(os.path.join(out,"..","medidas.csv"),"w",newline="") as fh:
    wr=csv.writer(fh); wr.writerow(["archivo","tipo","dur_s","canales","pico_origen_dbfs","muestras_saturadas","ganancia_db","pico_final_dbfs","rms_final_dbfs","salto_empalme_db","revisar"]); wr.writerows(rows)
for r in rows: print(*r, sep="\t")
