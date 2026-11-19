"""Genera INFORME_SINCRONIZACION.txt y guion_5_idiomas.txt a partir de out/<lg>/informe.json, qa/ y guion.json."""
import json, re, os, subprocess
G = json.load(open('guion.json'))['lines']
LG = dict(es='Español', en='English', fr='Français', pt='Português (BR)', hi='हिन्दी (Hindi)')
spoken = lambda t: re.sub(r'\[[^\]]*\]\s*', '', t).strip()
def tc(t): return f"{int(t//60)}:{t%60:06.3f}"

out = ["INFORME DE SINCRONIZACIÓN · Ep. 2 · ¿Por qué el jabón quita la grasa y el agua no?",
       "Voz: José Gregorio Torres (clonada) · Modelo: Eleven v4 · Video: 300,000 s", ""]
for lg, name in LG.items():
    rep = json.load(open(f'out/{lg}/informe.json'))
    L = lg.upper()
    m = subprocess.run(['ffmpeg', '-nostats', '-i', f'out/{lg}/E02_{L}_narracion.wav', '-af',
                        'ebur128=peak=true:framelog=quiet', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]; P = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', m)[-1]
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                f'out/{lg}/E02_{L}_narracion.wav'], capture_output=True, text=True).stdout)
    fuera = [r['id'] for r in rep if not r['dentro']]
    over = 0
    for a, b in zip(rep, rep[1:]):
        if b['inicio'] < a['fin']: over += 1
    acel = [f"{r['id'].replace('E02_','')} ×{r['tempo']}" for r in rep if r['tempo'] > 1]
    anc = json.load(open(f'anclas/{lg}.json')) if os.path.exists(f'anclas/{lg}.json') else {}
    out += [f"── {name} ({L}) " + "─" * 40,
            f"Frases: {len(rep)} · fuera de ventana: {len(fuera)} · solapes: {over} · duración pista: {dur:.3f} s",
            f"Nivel: {I} LUFS integrados · pico verdadero {P} dBTP",
            f"Aceleradas (máx. 8 %): {', '.join(acel) or 'ninguna'}",
            *([f"Anclas de acción: " + ', '.join(f"{k.replace('E02_','')} {v}" for k, v in anc.items())] if anc else []),
            "Toma            inicio      fin        ventana                 tempo"]
    for r in rep:
        out.append(f"{r['id'].replace('E02_',''):<14}  {tc(r['inicio'])}  {tc(r['fin'])}  [{tc(r['ventana'][0])} – {tc(r['ventana'][1])}]  {r['tempo']}"
                   + ("" if r['dentro'] else "  ¡FUERA!"))
    qa = open(f'qa/{lg}_qa.txt').read()
    out += ["", "Verificación por transcripción (guion vs. lo que se oye):", qa, ""]
# efectos de sonido
import csv
R = json.load(open('out/efectos/resumen.json'))
out += ["── EFECTOS DE SONIDO (una sola pista para los 5 idiomas) " + "─" * 20,
        "No se generó ningún efecto nuevo: se reutilizaron la biblioteca de ElevenLabs Sound Effects v3 del Ep. 3 y los efectos propios del Ep. 2.",
        "Cada uno está colocado en el segundo exacto de su acción en pantalla.",
        f"Foley de movimiento y textura: {R['entradas']['F']} entradas ({R['unicos']['F']} sonidos distintos)",
        f"Acentos de expresión (mickey mousing): {R['entradas']['M']} entradas ({R['unicos']['M']} sonidos distintos)",
        f"Transiciones y refuerzos visuales: {R['entradas']['T']} entradas ({R['unicos']['T']} sonidos distintos)",
        f"Pista de efectos: {R['lufs']} LUFS integrados · pico {R['pico']} dBTP",
        "Mezcla: mientras hay voz, los efectos bajan como mínimo 4 dB y se mantienen 9 dB por debajo del pico de la voz;",
        "en las pausas suenan completos. Cada mezcla queda a -16 LUFS con pico de -1,5 dBTP.", "",
        "  n  tiempo     toma          cat  efecto        orig acción en pantalla   (EL = ElevenLabs Ep. 3 · E2 = propio del Ep. 2)"]
for f in csv.DictReader(open('out/efectos/E02_hoja_de_efectos.csv')):
    out.append(f"{f['n']:>3}  {f['tiempo']:<9}  {f['toma']:<12}  {f['cat']:^3}  {f['efecto']:<12}  {'EL' if f['fuente'].startswith('Eleven') else 'E2'}  {f['accion_en_pantalla']}")
# rellenos sintetizados en los silencios que los efectos dejan vacíos (efectos_relleno.py)
out += ["", "── RELLENOS EN LOS SILENCIOS (sintetizados, sin ElevenLabs) " + "─" * 20,
        "Los 102 efectos de arriba no se movieron. En los silencios entre frases donde no suena ningún efecto se añadió",
        "un sonido pequeño sintetizado (marimba, gotitas, burbujas, campanita, blips, tic-tac o punteo, según la escena),",
        "a -27 dBFS RMS, en la escala pentatónica de do. Empieza 0,10 s después de la voz y acaba 0,08 s antes de la siguiente frase,",
        "sin tocar los efectos (0,05 s de colchón). Como cada idioma hace sus pausas en segundos distintos, hay una pista por idioma.", ""]
for lg, name in LG.items():
    L = lg.upper(); R = json.load(open(f'out/{lg}/relleno_resumen.json'))
    out += [f"── Rellenos · {name} ({L}): {R['rellenos']} sonidos en {R['silencios_con_relleno']} silencios · "
            f"sobre la voz: {R['tramos_10ms_sobre_voz']} · sobre los efectos: {R['tramos_10ms_sobre_efectos']} · "
            f"mezcla {R['lufs_mezcla']} LUFS, pico {R['pico_mezcla']} dBTP",
            "  n  suena en   toma          silencio entre            sonido      dur."]
    for f in csv.DictReader(open(f'out/{lg}/E02_{L}_rellenos.csv')):
        out.append(f"{f['n']:>3}  {f['tiempo']:<9}  {f['toma']:<12}  {f['silencio_entre']:<24}  {f['sonido']:<10}  {f['duracion_s']} s")
    out.append("")
open('INFORME_SINCRONIZACION.txt', 'w').write('\n'.join(out))

g = ["GUION DE NARRACIÓN · Ep. 2 · 5 idiomas",
     "Entre corchetes: dirección de voz para Eleven v4 (no se pronuncia).", ""]
for o in G:
    g.append(f"■ {o['id']}  ({o['t0']//60}:{o['t0']%60:02d}–{int(o['t1'])//60}:{int(o['t1'])%60:02d})")
    for lg in LG: g.append(f"  {lg.upper()}: {o[lg]}")
    g.append("")
open('guion_5_idiomas.txt', 'w').write('\n'.join(g))
print('ok')
