"""Genera INFORME_SINCRONIZACION.txt y guion_5_idiomas.txt a partir de out/<lg>/informe.json, qa/ y guion.json."""
import json, re, os, subprocess
G = json.load(open('guion.json'))['lines']
LG = dict(es='Español', en='English', fr='Français', pt='Português (BR)', hi='हिन्दी (Hindi)')
spoken = lambda t: re.sub(r'\[[^\]]*\]\s*', '', t).strip()
def tc(t): return f"{int(t//60)}:{t%60:06.3f}"

out = ["INFORME DE SINCRONIZACIÓN · Ep. 4 · ¿Qué es el hipo?",
       "Voz: José Gregorio Torres (clonada) · Modelo: Eleven v4 · Video: 299,958 s", ""]
for lg, name in LG.items():
    rep = json.load(open(f'out/{lg}/informe.json'))
    L = lg.upper()
    m = subprocess.run(['ffmpeg', '-nostats', '-i', f'out/{lg}/E04_{L}_narracion.wav', '-af',
                        'ebur128=peak=true:framelog=quiet', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]; P = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', m)[-1]
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                f'out/{lg}/E04_{L}_narracion.wav'], capture_output=True, text=True).stdout)
    fuera = [r['id'] for r in rep if not r['dentro']]
    over = 0
    for a, b in zip(rep, rep[1:]):
        if b['inicio'] < a['fin']: over += 1
    acel = [f"{r['id'].replace('E04_','')} ×{r['tempo']}" for r in rep if r['tempo'] > 1]
    anc = json.load(open(f'anclas/{lg}.json'))
    out += [f"── {name} ({L}) " + "─" * 40,
            f"Frases: {len(rep)} · fuera de ventana: {len(fuera)} · solapes: {over} · duración pista: {dur:.3f} s",
            f"Nivel: {I} LUFS integrados · pico verdadero {P} dBTP",
            f"Aceleradas (máx. 8 %): {', '.join(acel) or 'ninguna'}",
            f"Anclas de hipo medidas en la transcripción: " + ', '.join(f"{k.replace('E04_','')} {v}" for k, v in anc.items()),
            "Toma            inicio      fin        ventana                 tempo"]
    for r in rep:
        out.append(f"{r['id'].replace('E04_',''):<14}  {tc(r['inicio'])}  {tc(r['fin'])}  [{tc(r['ventana'][0])} – {tc(r['ventana'][1])}]  {r['tempo']}"
                   + ("" if r['dentro'] else "  ¡FUERA!"))
    qa = open(f'qa/{lg}_qa.txt').read()
    out += ["", "Verificación por transcripción (guion vs. lo que se oye):", qa, ""]
open('INFORME_SINCRONIZACION.txt', 'w').write('\n'.join(out))

g = ["GUION DE NARRACIÓN · Ep. 4 · 5 idiomas",
     "Entre corchetes: dirección de voz para Eleven v4 (no se pronuncia).", ""]
for o in G:
    g.append(f"■ {o['id']}  ({o['t0']//60}:{o['t0']%60:02d}–{int(o['t1'])//60}:{int(o['t1'])%60:02d})")
    for lg in LG: g.append(f"  {lg.upper()}: {o[lg]}")
    g.append("")
open('guion_5_idiomas.txt', 'w').write('\n'.join(g))
print('ok')
