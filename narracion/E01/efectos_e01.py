# Hoja de efectos del Ep. 1 (¿Por qué explotan las palomitas de maíz?).
# Una sola pista de efectos para los 5 idiomas: los efectos no dependen del idioma.
# No se generó ningún efecto nuevo: todos se reutilizan de dos bibliotecas ya existentes
#   EL = ElevenLabs Sound Effects v3, biblioteca del Ep. 3 (ep03/voz/sfx_raw/<nombre>.mp3)
#   HF = efectos generados para el Ep. 2 (ep02/sfx/sNN.mp3)
# Cada efecto se coloca en el segundo exacto de la acción en pantalla (análisis de movimiento
# fotograma a fotograma + hojas de contacto a 2 fps).
# Categorías: F = foley de movimiento y textura · M = acento de expresión (mickey mousing) · T = transición / refuerzo visual
import json

EL = '../../ep03/voz/sfx_raw/{}.mp3'
HF = '../../ep02/sfx/{}.mp3'

# id: (categoría, fuente, archivo, descripción/prompt original, duración máx. en s, modo)
# modo 'hit' = desde el primer ataque; 'bed' = desde el primer ataque, pensado como fondo continuo
LIB = {
 # --- ElevenLabs (Ep. 3) ---
 'plip':       ('F', 'EL', 'plip', "Single tiny water droplet, small plip", 0.3, 'hit'),
 'splash':     ('F', 'EL', 'splash', "Single water drop falling and splashing on a wet surface", 0.6, 'hit'),
 'squish':     ('F', 'EL', 'squish', "Soft squishy modeling clay squeeze, small and short", 0.6, 'hit'),
 'roll':       ('F', 'EL', 'roll', "Small rubber ball rolling slowly across a soft surface", 3.6, 'bed'),
 'roll_corto': ('F', 'EL', 'roll', "Small rubber ball rolling slowly across a soft surface (versión corta)", 1.8, 'bed'),
 'rotate':     ('F', 'EL', 'rotate', "Object slowly turning on a wooden table, soft continuous scraping", 3.5, 'bed'),
 'land':       ('F', 'EL', 'land', "Small soft rubber ball dropping and landing with a gentle thud", 0.4, 'hit'),
 'cheek_rub':  ('F', 'EL', 'cheek_rub', "Clay hands pressing onto cheeks, soft squeaky rub", 0.6, 'hit'),
 'arm_swish':  ('F', 'EL', 'arm_swish', "Quick soft swish of a small arm waving", 0.4, 'hit'),
 'balls_away': ('F', 'EL', 'balls_away', "Handful of small rubber balls tumbling and rolling away", 1.8, 'hit'),
 'uh_oh':      ('M', 'EL', 'uh_oh', "Short descending cartoon worried tones, two notes", 0.8, 'hit'),
 'squint':     ('M', 'EL', 'squint', "Short suspicious cartoon squeak, rising", 0.5, 'hit'),
 'think':      ('M', 'EL', 'think', "Cartoon pondering sound, gentle wooden tick tock", 1.6, 'bed'),
 'boing':      ('M', 'EL', 'boing', "Cartoon boing spring, bouncy", 0.6, 'hit'),
 'sparkle':    ('M', 'EL', 'sparkle', "Short magical sparkle twinkle", 0.9, 'hit'),
 'ding':       ('M', 'EL', 'ding', "Bright cartoon idea ding, single small bell", 0.9, 'hit'),
 'slide_up':   ('M', 'EL', 'slide_up', "Slide whistle going up quickly, comedic surprise", 0.7, 'hit'),
 'slide_down': ('M', 'EL', 'slide_down', "Slide whistle going down, comedic fail", 0.9, 'hit'),
 'magnet':     ('M', 'EL', 'magnet', "Cartoon magnet pull, shimmering zoop", 1.0, 'hit'),
 'pop':        ('M', 'EL', 'pop', "Cartoon pop, cork-like, short", 0.3, 'hit'),
 'power_down': ('M', 'EL', 'power_down', "Cartoon power down, descending electronic tones", 1.2, 'hit'),
 'fire_puff':  ('M', 'EL', 'fire_puff', "Comedic cartoon fire puff whoosh, short flame burst", 1.0, 'hit'),
 'whoosh':     ('T', 'EL', 'whoosh', "Fast airy whoosh, swish transition", 0.8, 'hit'),
 'zoom':       ('T', 'EL', 'zoom', "Short rising whoosh, zoom in transition", 1.4, 'hit'),
 'logo':       ('T', 'EL', 'logo', "Playful short xylophone and glockenspiel flourish jingle, cheerful sound logo", 3.6, 'hit'),
 'swipe':      ('T', 'EL', 'swipe', "Soft swipe swish with a gentle chime, page transition", 1.0, 'hit'),
 'shimmer':    ('T', 'EL', 'shimmer', "Soft magical shimmer swell, rising", 1.6, 'hit'),
 'rev_cymbal': ('T', 'EL', 'rev_cymbal', "Short reverse cymbal swell", 1.2, 'hit'),
 'bubble':     ('T', 'EL', 'bubble', "Bubbly watery swoosh transition", 1.0, 'hit'),
 'outro':      ('T', 'EL', 'outro', "Cheerful short xylophone outro jingle, ending flourish", 3.6, 'hit'),
 'bite':       ('F', 'EL', 'bite', "Single crunchy bite into a crisp fresh pepper, close-up foley", 0.9, 'hit'),
 'step':       ('F', 'EL', 'step', "Single soft rubbery footstep of a small toy on a wooden table", 0.35, 'hit'),
 'shuffle':    ('F', 'EL', 'shuffle', "Small clay puppet shuffling and wiggling in place, soft rubbery rustles", 1.4, 'bed'),
 'plate':      ('F', 'EL', 'plate', "Rubber vegetable rocking gently on a ceramic plate, light rattle and clink", 1.0, 'hit'),
 'slice':      ('F', 'EL', 'slice', "Knife slicing cleanly through a crisp pepper", 0.7, 'hit'),
 'seeds':      ('F', 'EL', 'seeds', "Small dry seeds rattling softly", 0.9, 'hit'),
 'tremble':    ('M', 'EL', 'tremble', "Cartoon wobble rattle, comedic trembling shake", 1.6, 'bed'),
 'steam':      ('M', 'EL', 'steam', "Cartoon steam puff from ears, short hiss whistle", 0.9, 'hit'),
 'key_lock':   ('M', 'EL', 'key_lock', "Small key sliding into a lock and clicking", 0.8, 'hit'),
 'relief':     ('M', 'EL', 'relief', "Gentle soft chime, relaxing, short", 1.5, 'hit'),
 # --- efectos del Ep. 2 ---
 'h_drops':    ('F', 'HF', 's01', "Water drops plinking off a clay blob, small boing", 1.0, 'hit'),
 'h_clayroll': ('F', 'HF', 's02', "Clay ball rolling, squishy bump, jelly wobble", 2.0, 'bed'),
 'h_breeze':   ('F', 'HF', 's06', "Gentle breeze, flower rustle and a light sparkle", 2.5, 'bed'),
 'h_scrub':    ('F', 'HF', 's07', "Squishy clay rubbing and scrubbing", 2.8, 'bed'),
 'h_zip':      ('F', 'HF', 's09', "Quick zip forward and retreat", 1.5, 'hit'),
 'h_tail':     ('F', 'HF', 's11', "Squiggly wobbly boing, tadpole tail wiggle", 1.8, 'hit'),
 'h_poke':     ('F', 'HF', 's14', "Squelchy clay poke", 1.2, 'hit'),
 'h_stretch':  ('F', 'HF', 's17', "Rubbery stretch and snap back", 2.0, 'hit'),
 'h_marbles':  ('F', 'HF', 's19', "Many small marbles rolling toward the center", 2.5, 'bed'),
 'h_pops':     ('F', 'HF', 's20', "Series of small squishy clay pops", 2.5, 'bed'),
 'h_click':    ('F', 'HF', 's21', "Clay pieces clicking into place and a completion chime", 3.0, 'hit'),
 'h_wobble':   ('F', 'HF', 's24', "Jelly wobble bloops", 2.0, 'hit'),
 'h_plink':    ('F', 'HF', 's25', "Water drops plink plink", 2.5, 'bed'),
 'h_rinse':    ('F', 'HF', 's26', "Water rinsing and something rolling away", 3.0, 'hit'),
 'h_foam':     ('F', 'HF', 's28', "Soapy scrubbing with foamy bubbles", 3.0, 'bed'),
 'h_splashroll': ('F', 'HF', 's29', "Splash rinse and a ball rolling away", 3.0, 'hit'),
 'h_pokes':    ('F', 'HF', 's33', "Tiny rubbery pokes and pops", 2.0, 'hit'),
 'h_crumble':  ('F', 'HF', 's34', "Crumbling clay and a deflating sigh", 2.5, 'hit'),
 'h_idea':     ('M', 'HF', 's05', "Slide whistle up, idea", 1.5, 'hit'),
 'h_tick':     ('M', 'HF', 's10', "Ticking clock", 2.5, 'bed'),
 'h_chime2':   ('M', 'HF', 's15', "Two-note xylophone chime", 1.0, 'hit'),
 'h_tada':     ('M', 'HF', 's16', "Ukulele strum, ta-da", 2.5, 'hit'),
 'h_question': ('M', 'HF', 's18', "Question pluck", 1.5, 'hit'),
 'h_claps':    ('M', 'HF', 's23', "Small claps", 1.5, 'hit'),
 'h_shrug':    ('M', 'HF', 's30', "Shrug boop", 1.0, 'hit'),
 'h_whirl':    ('T', 'HF', 's22', "Sparkly whirl shimmer", 2.5, 'hit'),
 'h_recap':    ('T', 'HF', 's32', "Three-note recap chime", 3.0, 'hit'),
 'h_whoosh':   ('T', 'HF', 's38', "Soft whoosh, zoom in", 1.0, 'hit'),
 'h_curious':  ('M', 'HF', 's03', "Curious pizzicato pluck", 1.5, 'hit'),
 'h_ponder':   ('M', 'HF', 's08', "Thoughtful pizzicato", 1.8, 'hit'),
 'h_tiptoe':   ('M', 'HF', 's27', "Suspenseful tiptoe pizzicato build-up", 2.5, 'hit'),
 'h_boing2':   ('M', 'HF', 's31', "Bouncy boing boing", 1.5, 'hit'),
 'h_bloops':   ('F', 'HF', 's13', "Squishy pop and bubbly bloops", 1.8, 'hit'),
}

S = dict(C01=0, C02=8, C03=16, CANAL_INICIO=24, C04=28, C05=36, C06=44, C07=52, C08=60, C09=68, C10=76, C11=84,
         C12=92, C13=100, L1=108, C14=114, C15=122, C16=130, C17=138, C18=146, C19=154, C20=162, C21=170, C22=178,
         C23=186, C24=194, C25=202, C26=210, C27=218, C28=226, C29=234, C30=242, L2=250, C31=258, C32=266, C33=274,
         L3=282, C34=288, CANAL_FINAL=296)

# (toma, segundo dentro de la toma, efecto, ganancia dB, qué se ve)
CUES = [
 # C01 · el grano tiembla, se agrieta y estalla (estallido en el fotograma 4,42 s)
 ('C01', 2.62, 'bite', -6, 'otra grieta'),
 ('C01', 3.21, 'bite', -5, 'la grieta crece'),
 ('C01', 3.79, 'plate', -4, 'el grano se sacude sobre el plato'),
 ('C01', 4.40, 'whoosh', -4, 'las cáscaras salen volando'),
 ('C01', 4.42, 'bite', -1, 'el casco revienta'),
 ('C01', 4.42, 'pop', 0, '¡pum!'),
 ('C01', 5.00, 'balls_away', -4, 'los pedazos de cáscara caen y ruedan'),
 # C02 · Pipo mira la palomita
 ('C02', 2.00, 'shuffle', -4, 'se inclina hacia la palomita'),
 ('C02', 3.29, 'h_question', -4, '¿cómo cabe tanto ahí dentro?'),
 # C03 · Plop, curioso
 ('C03', 0.83, 'boing', -5, 'Plop abre bien los ojos'),
 ('C03', 4.54, 'h_curious', -5, 'Plop sonríe: también quiere saber'),
 # CANAL_INICIO
 ('CANAL_INICIO', -0.25, 'whoosh', -2, 'entra la cortinilla'),
 ('CANAL_INICIO', 0.00, 'logo', 0, 'cortinilla del canal'),
 # C04 · la idea loca de Pipo
 ('C04', 1.45, 'arm_swish', 0, 'Pipo levanta la mano'),
 ('C04', 2.42, 'ding', -4, '¡una idea loca!'),
 # C05 · Pipo pega la oreja al grano
 ('C05', 0.75, 'cheek_rub', -3, 'Pipo pega la oreja al grano'),
 ('C05', 2.33, 'h_tiptoe', -7, 'escucha con atención'),
 ('C05', 6.46, 'slide_down', -5, 'no se oye nada'),
 # C06 · Pipo salta sobre el grano (8 aterrizajes medidos fotograma a fotograma)
 ('C06', 0.50, 'boing', -4, 'Pipo salta'),
 ('C06', 1.08, 'land', -1, 'aterriza sobre el grano'),
 ('C06', 1.92, 'land', -2, 'aterriza otra vez'),
 ('C06', 2.75, 'land', -2, 'otro salto'),
 ('C06', 3.75, 'land', -3, 'otro salto'),
 ('C06', 4.58, 'land', -3, 'otro salto'),
 ('C06', 5.54, 'land', -3, 'otro salto'),
 ('C06', 6.58, 'land', -4, 'otro salto'),
 ('C06', 7.42, 'land', -4, 'último salto: el grano ni se abre'),
 # C07 · Plop piensa, mano en la barbilla
 ('C07', 0.83, 'think', -3, 'Plop se rasca la barbilla'),
 ('C07', 2.33, 'cheek_rub', -4, 'se apoya la mano en la cara'),
 # C08 · Pipo junto al granito
 ('C08', 4.17, 'shuffle', -4, 'se da la vuelta'),
 # C09 · primer plano del grano
 ('C09', 5.40, 'zoom', -3, 'la cámara se acerca al grano'),
 ('C09', 6.80, 'rev_cymbal', -4, '¡vamos a abrirlo!'),
 # C10 · el grano partido por la mitad
 ('C10', 0.00, 'slice', -2, 'el grano aparece partido por la mitad'),
 ('C10', 1.80, 'zoom', -4, 'la cámara entra al grano'),
 ('C10', 5.46, 'plip', -2, 'la gotita escondida'),
 # C11 · la bolita sobre el casco
 ('C11', 0.40, 'roll_corto', -4, 'la bolita rueda sobre el casco'),
 ('C11', 3.00, 'land', -2, 'la bolita cae y rebota'),
 ('C11', 4.71, 'h_chime2', -5, 'primera parte: el casco'),
 # C12 · la gota en el almidón
 ('C12', 0.96, 'h_wobble', -4, 'la gota se mueve'),
 ('C12', 1.96, 'squish', -3, 'el relleno blanco y apretado'),
 ('C12', 6.90, 'h_chime2', -6, 'segunda parte: el almidón'),
 # C13 · primer plano de la gota
 ('C13', 0.67, 'h_wobble', -3, 'la gota tiembla'),
 ('C13', 2.46, 'plip', -2, 'la gota brilla'),
 ('C13', 3.62, 'sparkle', -4, 'agua: ¡la clave!'),
 # L1
 ('L1', 0.00, 'swipe', -1, 'lámina 1: las tres partes'),
 ('L1', 0.40, 'h_recap', -4, 'casco, almidón y agua'),
 # C14 · Pipo no se lo cree
 ('C14', 0.96, 'slide_up', -4, '¿agua?'),
 ('C14', 2.96, 'h_shrug', -5, 'si está sequito por fuera'),
 # C15 · la gota no puede salir del casco
 ('C15', 0.50, 'h_zip', -3, 'la gota corre por dentro'),
 ('C15', 3.12, 'plip', -2, 'choca contra el casco'),
 ('C15', 4.71, 'plip', -3, 'choca otra vez'),
 ('C15', 5.62, 'h_drops', -3, 'rebota de pared en pared'),
 ('C15', 6.46, 'key_lock', -5, 'el casco está cerrado: no puede escapar'),
 # C16 · Plop sospecha
 ('C16', 1.12, 'squint', -3, 'Plop entrecierra los ojos'),
 ('C16', 6.12, 'uh_oh', -5, 'algo va a pasar'),
 # C17 · el calor se enciende
 ('C17', 0.50, 'fire_puff', -3, 'se enciende el calor'),
 ('C17', 1.67, 'h_stretch', -4, 'los zarcillos de calor crecen'),
 ('C17', 5.50, 'h_tail', -5, 'los zarcillos se menean'),
 # C18 · la gota se vuelve vapor
 ('C18', 1.90, 'bubble', -4, 'la gota empieza a cambiar'),
 ('C18', 2.30, 'steam', -3, '¡se vuelve vapor!'),
 ('C18', 4.00, 'h_bloops', -4, 'la nube burbujea'),
 # C19 · la nube de vapor crece
 ('C19', 1.12, 'h_foam', -5, 'la nube crece'),
 ('C19', 4.33, 'squish', -3, 'la nube choca con el casco'),
 # C20 · Pipo infla los cachetes
 ('C20', 0.46, 'cheek_rub', -3, 'Pipo toma aire'),
 ('C20', 1.08, 'h_stretch', -3, 'infla los cachetes como un globo'),
 # C21 · el vapor empuja el casco
 ('C21', 1.60, 'h_pokes', -4, 'el vapor empuja desde dentro'),
 ('C21', 3.67, 'squish', -3, 'otro empujón'),
 # C22 · el almidón se vuelve gelatina
 ('C22', 1.83, 'h_wobble', -3, 'el almidón se vuelve gelatina'),
 ('C22', 3.08, 'squish', -3, 'la gelatina se estira'),
 ('C22', 4.25, 'h_wobble', -4, 'tiembla otra vez'),
 # C23 · olla a presión
 ('C23', 4.00, 'plate', -4, 'se sacude sobre el plato'),
 ('C23', 5.79, 'plate', -3, 'se sacude más fuerte'),
 ('C23', 6.29, 'steam', -4, 'una mini olla a presión'),
 # C24 · Plop no quiere mirar
 ('C24', 0.42, 'uh_oh', -4, 'Plop no quiere mirar'),
 ('C24', 1.00, 'cheek_rub', -3, 'se tapa los ojos'),
 ('C24', 6.58, 'arm_swish', -3, 'abre los brazos'),
 # C25 · el grano se agrieta
 ('C25', 1.12, 'bite', -6, 'aparece una grieta'),
 ('C25', 2.29, 'bite', -5, 'la grieta crece'),
 ('C25', 4.29, 'seeds', -5, 'crujidos por dentro'),
 # C26 · ¡pum! (estallido medido en 212,75 s)
 ('C26', 1.50, 'bite', -4, 'el casco se abre'),
 ('C26', 1.60, 'rev_cymbal', -3, 'la presión llega al máximo'),
 ('C26', 2.75, 'bite', -1, 'el casco revienta'),
 ('C26', 2.75, 'pop', 0, '¡pum!'),
 ('C26', 2.79, 'fire_puff', -3, 'el vapor escapa de golpe'),
 ('C26', 3.30, 'balls_away', -4, 'las cáscaras caen y ruedan'),
 ('C26', 4.20, 'sparkle', -6, 'nace la palomita'),
 # C27 · la espuma blanca y crujiente
 ('C27', 0.00, 'shimmer', -4, 'la palomita en primer plano'),
 ('C27', 5.58, 'bite', -4, 'crujiente'),
 # C28 · Pipo abraza la palomita
 ('C28', 1.12, 'shuffle', -4, 'Pipo abraza la palomita'),
 ('C28', 5.83, 'cheek_rub', -3, 'apoya la cara en la palomita'),
 # C29 · la respuesta
 ('C29', 0.96, 'arm_swish', -1, 'Pipo abre los brazos'),
 ('C29', 1.10, 'h_tada', -4, '¡esa es tu respuesta!'),
 # C30 · Plop da saltitos de alegría
 ('C30', 0.60, 'shuffle', -4, 'Plop se mueve contento'),
 ('C30', 0.75, 'h_boing2', -5, 'da saltitos'),
 ('C30', 3.00, 'step', -4, 'otro saltito'),
 # L2 · repaso
 ('L2', 0.00, 'swipe', -1, 'lámina 2: repaso'),
 ('L2', 0.40, 'h_recap', -4, 'agua, vapor y ¡pum!'),
 # C31 · grano con fuga
 ('C31', 0.50, 'steam', -4, 'el vapor se escapa por la grieta'),
 ('C31', 2.00, 'h_breeze', -6, 'sale despacito'),
 ('C31', 6.29, 'power_down', -6, 'se desinfla sin estallar'),
 # C32 · Pipo explica la fuga
 ('C32', 0.46, 'arm_swish', -2, 'Pipo señala el grano'),
 ('C32', 4.00, 'h_ponder', -5, 'no son perezosos: tienen una fuga'),
 # C33 · el reto
 ('C33', 1.12, 'step', -3, 'Plop da un pasito'),
 ('C33', 3.30, 'arm_swish', -1, 'Plop señala'),
 ('C33', 3.50, 'slide_up', -5, '¡un reto!'),
 # L3 · reto en casa
 ('L3', 0.00, 'swipe', -1, 'lámina 3: reto en casa'),
 ('L3', 0.40, 'h_tiptoe', -6, 'ojos de detective'),
 # C34 · próxima pregunta
 ('C34', 0.62, 'arm_swish', 0, 'Pipo saluda'),
 ('C34', 5.50, 'bubble', -5, 'guiño al próximo episodio: el jabón'),
 # CANAL_FINAL
 ('CANAL_FINAL', -0.25, 'whoosh', -2, 'entra la cortinilla final'),
 ('CANAL_FINAL', 0.00, 'outro', 0, 'cortinilla final'),
]

CAT = dict(F='Foley de movimiento y textura', M='Acentos de expresión (mickey mousing)', T='Transiciones y refuerzos visuales')
FUENTE = dict(EL='ElevenLabs SFX v3 (biblioteca Ep. 3)', HF='Efectos del Ep. 2 (biblioteca Ep. 2)')

def ruta(k):
    _, src, f, *_ = LIB[k]
    return (EL if src == 'EL' else HF).format(f)

def cues():
    out = []
    for shot, t, snd, g, what in CUES:
        out.append(dict(toma=shot, t=round(S[shot] + t, 3), efecto=snd, cat=LIB[snd][0], db=g, accion=what))
    return sorted(out, key=lambda c: c['t'])

if __name__ == '__main__':
    C = cues()
    used = sorted({c['efecto'] for c in C})
    for k in 'FMT':
        n = [c for c in C if c['cat'] == k]
        print(k, CAT[k], len(n), 'colocaciones de', len({c['efecto'] for c in n}), 'sonidos únicos')
    for s in ('EL', 'HF'):
        print(s, FUENTE[s], sum(1 for c in C if LIB[c['efecto']][1] == s), 'colocaciones')
    print('total', len(C), 'colocaciones ·', len(used), 'sonidos únicos · sin usar:', sorted(set(LIB) - set(used)))
    json.dump(dict(lib={k: dict(cat=v[0], fuente=FUENTE[v[1]], archivo=ruta(k), prompt=v[3], max=v[4], modo=v[5])
                        for k, v in LIB.items() if k in used}, cues=C),
              open('efectos.json', 'w'), ensure_ascii=False, indent=1)
