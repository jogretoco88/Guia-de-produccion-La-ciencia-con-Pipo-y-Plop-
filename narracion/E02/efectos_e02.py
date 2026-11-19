# Hoja de efectos del Ep. 2 (¿Por qué el jabón quita la grasa y el agua no?).
# Una sola pista de efectos para los 5 idiomas: los efectos no dependen del idioma.
# No se generó ningún efecto nuevo: todos se reutilizan de dos bibliotecas ya existentes
#   EL = ElevenLabs Sound Effects v3, biblioteca del Ep. 3 (ep03/voz/sfx_raw/<nombre>.mp3)
#   HF = efectos generados antes para este mismo Ep. 2 (ep02/sfx/sNN.mp3)
# Cada efecto se coloca en el segundo exacto de la acción en pantalla (análisis de movimiento
# fotograma a fotograma + hojas de contacto a 2 fps).
# Categorías: F = foley de movimiento y textura · M = acento de expresión (mickey mousing) · T = transición / refuerzo visual
import json

EL = '../../ep03/voz/sfx_raw/{}.mp3'
HF = '../sfx/{}.mp3'

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
 # --- efectos propios del Ep. 2 ---
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
}

S = dict(C01=0, C02=8, C03=16, CANAL_INICIO=24, C04=28, C05=36, C06=44, C07=52, C08=60, C09=68, C10=76, C11=84,
         C12=92, C13=100, L1=108, C14=114, C15=122, C16=130, C17=138, C18=146, C19=154, C20=162, C21=170, C22=178,
         C23=186, C24=194, C25=202, C26=210, C27=218, C28=226, C29=234, C30=242, L2=250, C31=258, C32=266, C33=274,
         L3=282, C34=288, CANAL_FINAL=296)

# (toma, segundo dentro de la toma, efecto, ganancia dB, qué se ve)
CUES = [
 # C01 · gotas que caen sobre la grasa de Plop y resbalan
 ('C01', 0.45, 'plip', 0, 'cae una gota sobre la panza de Plop'),
 ('C01', 0.95, 'splash', -2, 'la gota resbala sobre la grasa'),
 ('C01', 1.55, 'uh_oh', -4, '¡ups! la gota no limpia nada'),
 ('C01', 2.35, 'plip', 0, 'otra gota'),
 ('C01', 3.45, 'h_drops', -3, 'la gota rebota y sale despedida'),
 ('C01', 6.95, 'plip', 0, 'la última gota'),
 # C02 · el jabón entra rodando y choca con la grasa
 ('C02', 1.25, 'h_clayroll', -2, 'el jabón entra rodando'),
 ('C02', 3.40, 'squish', 0, 'choca con la grasa'),
 ('C02', 4.10, 'sparkle', -5, 'la grasa se rinde'),
 ('C02', 5.70, 'h_question', -4, '¿qué tiene el jabón?'),
 # C03 · Pipo y su teoría
 ('C03', 1.35, 'squint', -3, 'Pipo ladea la cabeza'),
 ('C03', 5.35, 'boing', -4, 'la ladea otra vez: «bastante loca»'),
 # CANAL_INICIO
 ('CANAL_INICIO', -0.25, 'whoosh', -2, 'entra la cortinilla'),
 ('CANAL_INICIO', 0.00, 'logo', 0, 'cortinilla del canal'),
 # C04 · la idea loca de Pipo
 ('C04', 1.95, 'arm_swish', 0, 'Pipo levanta el brazo'),
 ('C04', 2.45, 'h_idea', -4, '¡la idea loca!'),
 # C05 · la flor huele rico y la grasa ni se mueve
 ('C05', 0.40, 'h_breeze', -3, 'la flor se mece'),
 ('C05', 4.20, 'h_breeze', -5, 'la flor se mece otra vez'),
 ('C05', 6.40, 'slide_down', -4, 'la grasa ni se mueve: no es el olor'),
 # C06 · Plop frota la grasa con fuerza
 ('C06', 0.60, 'h_scrub', -2, 'Plop frota la grasa'),
 ('C06', 6.10, 'squish', -2, 'la grasa se embarra más'),
 ('C06', 6.50, 'uh_oh', -5, 'peor que antes'),
 # C07 · Plop piensa
 ('C07', 1.00, 'think', -3, 'Plop ladea la cabeza, pensativo'),
 # C08 · la gota intenta acercarse a la grasa y rebota
 ('C08', 0.75, 'h_zip', -2, 'la gota corre hacia la grasa'),
 ('C08', 1.75, 'h_drops', -2, 'choca y rebota'),
 ('C08', 4.00, 'h_zip', -3, 'lo intenta otra vez y retrocede'),
 ('C08', 4.50, 'boing', -4, 'rebota de nuevo'),
 ('C08', 5.25, 'plip', -1, 'la gota resbala'),
 # C09 · primer plano del jabón y zoom
 ('C09', 5.00, 'zoom', -2, 'la cámara se acerca al jabón'),
 ('C09', 6.80, 'rev_cymbal', -4, 'entramos al mundo diminuto'),
 # C10 · la molécula de jabón
 ('C10', 0.00, 'bubble', -2, 'aparece la molécula de jabón'),
 ('C10', 0.50, 'h_tail', -3, 'la cola se menea'),
 # C11 · el renacuajo de jabón se da la vuelta
 ('C11', 2.00, 'rotate', -3, 'el jabón gira y muestra cabeza y cola'),
 ('C11', 6.80, 'h_chime2', -4, 'cada parte quiere algo distinto'),
 # C12 · la cabeza ama el agua
 ('C12', 0.50, 'roll_corto', -3, 'el jabón se desliza hacia la gota'),
 ('C12', 2.55, 'plip', -1, 'la cabeza toca la gota'),
 ('C12', 2.70, 'magnet', -4, '¡pegada al agua!'),
 ('C12', 4.50, 'h_tail', -4, 'la cola se menea'),
 # C13 · la cola ama la grasa
 ('C13', 2.50, 'h_poke', -2, 'la cola se clava en la grasa'),
 ('C13', 4.50, 'pop', -3, '¡escondida!'),
 ('C13', 6.50, 'squish', -3, 'la cabeza se apoya en la grasa'),
 # L1
 ('L1', 0.00, 'swipe', -1, 'lámina 1: cabeza y cola'),
 # C14 · Pipo lo resume
 ('C14', 3.40, 'arm_swish', 0, 'Pipo abre los brazos'),
 ('C14', 3.65, 'h_chime2', -4, '¡amigo de los dos equipos!'),
 # C15 · el puente
 ('C15', 1.30, 'cheek_rub', -2, 'el jabón se estira y agarra la grasa'),
 ('C15', 2.10, 'h_stretch', -5, 'la otra punta agarra la gota: un puente'),
 ('C15', 6.00, 'boing', -3, 'el puente se suelta y vuelve a su forma'),
 ('C15', 6.50, 'plip', -2, 'la gota tiembla'),
 # C16 · Plop pregunta
 ('C16', 6.40, 'h_question', -3, 'Plop ladea la cabeza: ¿cómo?'),
 # C17 · millones de jabones
 ('C17', 0.00, 'shimmer', -4, 'se revela el ejército de jabones'),
 ('C17', 0.50, 'h_marbles', -2, 'llegan muchísimos jabones rodando'),
 ('C17', 5.50, 'balls_away', -4, 'se amontonan alrededor de la grasa'),
 # C18 · las colas se clavan
 ('C18', 2.30, 'h_poke', -3, 'una cola se clava en la grasa'),
 ('C18', 3.20, 'squish', -2, 'otra cola se clava'),
 ('C18', 5.30, 'h_pokes', -3, 'muchas colas se clavan a la vez'),
 # C19 · la rodean por completo
 ('C19', 3.50, 'squish', -2, 'otro jabón se une al círculo'),
 ('C19', 4.60, 'h_click', -2, 'las últimas piezas encajan'),
 # C20 · la grasa atrapada
 ('C20', 1.00, 'h_wobble', -3, 'la micela se acomoda'),
 ('C20', 2.70, 'squish', -2, 'una bolita encaja en su sitio'),
 ('C20', 3.00, 'ding', -4, '¡la grasa quedó atrapada!'),
 # C21 · Pipo se ríe: «micela»
 ('C21', 3.00, 'cheek_rub', -3, 'Pipo se agarra la panza de la risa'),
 ('C21', 4.50, 'boing', -5, 'parpadea divertido'),
 # C22 · el superpoder de la micela
 ('C22', 0.80, 'h_whirl', -5, 'la micela luce su superpoder'),
 ('C22', 4.50, 'sparkle', -4, '¡parece amiga del agua!'),
 # C23 · llega el agua y se agarra de las cabezas
 ('C23', 0.00, 'bubble', -4, 'entra el agua'),
 ('C23', 1.40, 'plip', 0, 'una gota se agarra de una cabeza'),
 ('C23', 2.40, 'plip', -1, 'otra gota'),
 ('C23', 4.10, 'h_plink', -3, 'llegan más gotas'),
 ('C23', 5.25, 'splash', -3, 'muchas gotas a la vez'),
 # C24 · el agua se lleva la micela rodando
 ('C24', 0.30, 'h_splashroll', -2, 'el agua arrastra la micela'),
 ('C24', 2.50, 'roll', -4, 'la micela rueda hacia la derecha'),
 ('C24', 6.30, 'whoosh', -4, 'sale de cuadro: ¡adiós, mancha!'),
 # C25 · Plop mira su panza
 ('C25', 1.00, 'squint', -3, 'Plop mira su panza'),
 ('C25', 1.50, 'cheek_rub', -3, 'se toca la panza'),
 # C26 · jabón: frotar bien
 ('C26', 0.50, 'h_foam', -2, 'Plop frota la panza con jabón'),
 ('C26', 3.50, 'h_foam', -3, 'sigue frotando, sale espuma'),
 # C27 · agua: la grasa se va
 ('C27', 0.50, 'h_rinse', -2, 'cae el agua sobre Plop'),
 ('C27', 2.50, 'roll_corto', -3, 'la grasa se va rodando'),
 ('C27', 4.50, 'plip', -2, 'caen las últimas gotas'),
 # C28 · ¡panza limpia!
 ('C28', 0.45, 'arm_swish', -1, 'Plop abre los brazos'),
 ('C28', 0.60, 'h_tada', -3, '¡panza limpia!'),
 ('C28', 1.10, 'cheek_rub', -2, 'se abraza la panza limpia'),
 # C29 · no era el perfume
 ('C29', 1.30, 'arm_swish', 0, 'Pipo abre los brazos'),
 ('C29', 1.60, 'h_shrug', -3, '«no era el perfume»'),
 # C30 · la respuesta
 ('C30', 6.80, 'h_claps', -4, '¡pregunta resuelta!'),
 # L2 · repaso
 ('L2', 0.00, 'swipe', -1, 'lámina 2: repaso'),
 ('L2', 0.40, 'h_recap', -4, 'tres pasos'),
 # C31 · dato extra: microbios con abrigo de grasa
 ('C31', 0.00, 'h_whoosh', -3, 'dato extra'),
 ('C31', 2.50, 'h_zip', -3, 'llegan volando más jabones'),
 ('C31', 3.10, 'land', -2, 'caen junto al microbio'),
 ('C31', 4.00, 'squish', -2, 'se pegan al abrigo de grasa'),
 # C32 · el abrigo se desarma
 ('C32', 1.20, 'h_crumble', -2, 'el abrigo de grasa se desarma'),
 ('C32', 2.50, 'balls_away', -4, 'las bolitas ruedan lejos'),
 ('C32', 3.20, 'power_down', -4, 'el microbio se desinfla'),
 # C33 · el reto
 ('C33', 0.40, 'arm_swish', -1, 'Plop gesticula'),
 ('C33', 6.20, 'slide_up', -4, '¡un reto!'),
 # L3 · reto en casa
 ('L3', 0.00, 'swipe', -1, 'lámina 3: reto en casa'),
 ('L3', 0.40, 'h_tick', -5, 'el reloj de los 20 segundos'),
 # C34 · próxima pregunta
 ('C34', 1.50, 'arm_swish', 0, 'Plop saluda'),
 ('C34', 6.00, 'fire_puff', -6, 'guiño al próximo episodio: el ají'),
 # CANAL_FINAL
 ('CANAL_FINAL', -0.25, 'whoosh', -2, 'entra la cortinilla final'),
 ('CANAL_FINAL', 0.00, 'outro', 0, 'cortinilla final'),
]

CAT = dict(F='Foley de movimiento y textura', M='Acentos de expresión (mickey mousing)', T='Transiciones y refuerzos visuales')
FUENTE = dict(EL='ElevenLabs SFX v3 (biblioteca Ep. 3)', HF='Efectos propios del Ep. 2')

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
