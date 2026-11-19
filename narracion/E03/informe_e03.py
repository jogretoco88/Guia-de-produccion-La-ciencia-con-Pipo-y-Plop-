"""Genera INFORME_SINCRONIZACION.txt y guion_5_idiomas.txt a partir de out/<lg>/informe.json, qa/ y guion.json."""
import json, re, os, subprocess
G = json.load(open('guion.json'))['lines']
LG = dict(es='Español', en='English', fr='Français', pt='Português (BR)', hi='हिन्दी (Hindi)')
spoken = lambda t: re.sub(r'\[[^\]]*\]\s*', '', t).strip()
def tc(t): return f"{int(t//60)}:{t%60:06.3f}"

out = ["INFORME DE SINCRONIZACIÓN · Ep. 3 · ¿Por qué pica el ají si no está caliente?",
       "Voz: José Gregorio Torres (clonada) · Modelo: Eleven v4 · Video: 300,000 s", ""]
for lg, name in LG.items():
    rep = json.load(open(f'out/{lg}/informe.json'))
    L = lg.upper()
    m = subprocess.run(['ffmpeg', '-nostats', '-i', f'out/{lg}/E03_{L}_narracion.wav', '-af',
                        'ebur128=peak=true:framelog=quiet', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]; P = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', m)[-1]
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                f'out/{lg}/E03_{L}_narracion.wav'], capture_output=True, text=True).stdout)
    fuera = [r['id'] for r in rep if not r['dentro']]
    over = 0
    for a, b in zip(rep, rep[1:]):
        if b['inicio'] < a['fin']: over += 1
    acel = [f"{r['id'].replace('E03_','')} ×{r['tempo']}" for r in rep if r['tempo'] > 1]
    anc = json.load(open(f'anclas/{lg}.json')) if os.path.exists(f'anclas/{lg}.json') else {}
    out += [f"── {name} ({L}) " + "─" * 40,
            f"Frases: {len(rep)} · fuera de ventana: {len(fuera)} · solapes: {over} · duración pista: {dur:.3f} s",
            f"Nivel: {I} LUFS integrados · pico verdadero {P} dBTP",
            f"Aceleradas (máx. 8 %): {', '.join(acel) or 'ninguna'}",
            *([f"Anclas de acción: " + ', '.join(f"{k.replace('E03_','')} {v}" for k, v in anc.items())] if anc else []),
            "Toma            inicio      fin        ventana                 tempo"]
    for r in rep:
        out.append(f"{r['id'].replace('E03_',''):<14}  {tc(r['inicio'])}  {tc(r['fin'])}  [{tc(r['ventana'][0])} – {tc(r['ventana'][1])}]  {r['tempo']}"
                   + ("" if r['dentro'] else "  ¡FUERA!"))
    qa = open(f'qa/{lg}_qa.txt').read()
    out += ["", "Verificación por transcripción (guion vs. lo que se oye):", qa, ""]
# efectos de sonido: reubicados en los silencios entre frase y frase de cada idioma (efectos_silencios.py)
import csv
R0 = json.load(open('out/es/efectos_resumen.json'))
out += ["── EFECTOS DE SONIDO EN LOS SILENCIOS " + "─" * 30,
        "Generados con ElevenLabs Sound Effects v3 (no se generó ningún sonido nuevo al reubicarlos).",
        f"Foley de movimiento y textura: {R0['entradas']['F']} entradas ({R0['unicos']['F']} sonidos distintos)",
        f"Acentos de expresión (mickey mousing): {R0['entradas']['M']} entradas ({R0['unicos']['M']} sonidos distintos)",
        f"Transiciones y refuerzos visuales: {R0['entradas']['T']} entradas ({R0['unicos']['T']} sonidos distintos)",
        "Cada efecto suena en un silencio entre dos frases, dentro de su propia toma (desde 0,15 s antes del corte que la abre",
        "hasta 0,35 s después del que la cierra), lo más cerca posible de su acción. Deja 0,08 s tras la voz y 0,06 s antes",
        "de la siguiente frase. Si el silencio es más corto que el sonido, el sonido se recorta con un fundido.",
        "Como cada idioma tiene sus propios silencios, hay una pista de efectos por idioma. Cada mezcla queda a -16 LUFS, pico -1,5 dBTP.", ""]
for lg, name in LG.items():
    L = lg.upper(); R = json.load(open(f'out/{lg}/efectos_resumen.json'))
    out += [f"── Efectos · {name} ({L}) " + "─" * 30,
            f"Silencios usados: {R['silencios_usados']} de {R['silencios']} ({R['silencio_total_s']} s de silencio entre frases)",
            f"Distancia a la acción en pantalla: media {R['desplazamiento_medio_s']} s · máxima {R['desplazamiento_max_s']} s (siempre dentro de su toma)",
            f"Sonidos recortados para caber en su silencio: {R['recortados']} de 106",
            f"Energía de efectos mientras habla el narrador: {R['energia_bajo_voz_pct']} % · pista de efectos {R['lufs_efectos']} LUFS, pico {R['pico_efectos']} dBFS", "",
            "  n  suena en    acción en   toma          silencio                 cat  efecto        dur.   acción en pantalla"]
    for f in csv.DictReader(open(f'out/{lg}/E03_{L}_hoja_de_efectos.csv')):
        out.append(f"{f['n']:>3}  {f['tiempo']:<9}  {float(f['segundo_accion']):>7.2f} s  {f['toma']:<12}  {f['silencio']:<24} {f['cat']:^3}  "
                   f"{f['efecto']:<12}  {f['duracion_s']} s  {f['accion_en_pantalla']}")
    out.append("")
open('INFORME_SINCRONIZACION.txt', 'w').write('\n'.join(out))

g = ["GUION DE NARRACIÓN · Ep. 3 · 5 idiomas",
     "Entre corchetes: dirección de voz para Eleven v4 (no se pronuncia).", ""]
for o in G:
    g.append(f"■ {o['id']}  ({o['t0']//60}:{o['t0']%60:02d}–{int(o['t1'])//60}:{int(o['t1'])%60:02d})")
    for lg in LG: g.append(f"  {lg.upper()}: {o[lg]}")
    g.append("")
open('guion_5_idiomas.txt', 'w').write('\n'.join(g))
print('ok')
