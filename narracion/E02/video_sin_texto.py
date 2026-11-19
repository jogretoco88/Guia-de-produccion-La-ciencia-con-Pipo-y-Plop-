"""Ep. 2 · Rehace el video mudo sin ningún texto en pantalla.
Las 5 láminas (título, L1, L2, L3 y cierre) se vuelven a renderizar desde sus fondos limpios (img/<lámina>.png), sin los
rótulos que les ponía make_slides.py, con el mismo zoom lento y la misma duración. Los 34 clips (seg/NN.mp4) se reutilizan
tal cual, así que la duración (300,000 s, 7200 fotogramas) y los tiempos de cada toma no cambian y el audio sigue en sincronía.
uso: python3 video_sin_texto.py   -> video_sin_texto.mp4
"""
import json, subprocess, os
from PIL import Image
os.makedirs('slides_sin_texto', exist_ok=True); os.makedirs('seg2', exist_ok=True)
for n in ['T', 'L1', 'L2', 'L3', 'F']:
    Image.open(f'img/{n}.png').convert('RGB').resize((1920, 1080), Image.LANCZOS).save(f'slides_sin_texto/{n}.png')
d = json.load(open('shots.json'))['shots']
STILL = {'CANAL_INICIO': 'T', 'E02_L1': 'L1', 'E02_L2': 'L2', 'E02_L3': 'L3', 'CANAL_FINAL': 'F'}
def ts(x): m, s = x.split(':'); return int(m) * 60 + int(s)
segs = []
for k, s in enumerate(d):
    a, b = [ts(x) for x in s['t'].replace('–', '-').split('-')]; dur = b - a
    if s['id'] in STILL:
        n = dur * 24; out = f"seg2/{k:02d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-loop", "1", "-i", f"slides_sin_texto/{STILL[s['id']]}.png", "-t", str(dur), "-vf",
                        f"scale=3840:2160,zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1920x1080:fps=24,format=yuv420p",
                        "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-an", out], check=True)
        segs.append(os.path.abspath(out))
    else:
        segs.append(os.path.abspath(f"seg/{k:02d}.mp4"))
open('seg2/list.txt', 'w').write("".join(f"file '{x}'\n" for x in segs))
subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "concat", "-safe", "0", "-i", "seg2/list.txt", "-c", "copy", "video_sin_texto.mp4"], check=True)
