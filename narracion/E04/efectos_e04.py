# Hoja de efectos del Ep. 4 (¿Por qué nos da hipo?).
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
 'zap':        ('M', 'EL', 'zap', "Cartoon electric spark zipping along a wire, traveling zap", 2.5, 'hit'),
 'alarm':      ('M', 'EL', 'alarm', "Small toy alarm beeping, cartoon, fast beeps", 1.4, 'hit'),
 'frost':      ('M', 'EL', 'frost', "Light frosty ice twinkle, cold shimmer", 1.0, 'hit'),
 'hop':        ('F', 'EL', 'hop', "Tiny bird hopping on a table, one soft light patter", 0.3, 'hit'),
 'flutter':    ('F', 'EL', 'flutter', "Small bird wings fluttering, quick takeoff", 1.0, 'hit'),
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
 'h_twinkle':  ('M', 'HF', 's37', "Warm twinkle goodbye", 2.0, 'hit'),
 'h_bloops':   ('F', 'HF', 's13', "Squishy pop and bubbly bloops", 1.8, 'hit'),
}

S = dict(C01=0, C02=8, C03=16, CANAL_INICIO=24, C04=28, C05=36, C06=44, C07=52, C08=60, C09=68, C10=76, C11=84,
         C12=92, C13=100, L1=108, C14=114, C15=122, C16=130, C17=138, C18=146, C19=154, C20=162, C21=170, C22=178,
         C23=186, C24=194, C25=202, C26=210, C27=218, C28=226, C29=234, C30=242, L2=250, C31=258, C32=266, C33=274,
         L3=282, C34=288, CANAL_FINAL=296)

# (toma, segundo dentro de la toma, efecto, ganancia dB, qué se ve)
# Cada hipo se midió fotograma a fotograma: despegue (primer fotograma con movimiento brusco) y aterrizaje.
CUES = [
 # C01 · Plop tiene hipo y tumba la torre de bloques
 ('C01', 0.88, 'pop', -1, '¡hip! Plop da un salto'),
 ('C01', 1.21, 'land', -2, 'cae sobre sus pies'),
 ('C01', 1.50, 'plate', -3, 'empuja la torre de bloques'),
 ('C01', 2.04, 'land', -2, 'los bloques caen al suelo'),
 ('C01', 3.40, 'uh_oh', -5, '¿qué fue eso?'),
 # C02 · cuatro hipos seguidos
 ('C02', 1.04, 'pop', -1, '¡hip!'),
 ('C02', 1.33, 'land', -2, 'aterriza'),
 ('C02', 3.04, 'hop', -2, 'otro hipo'),
 ('C02', 3.29, 'land', -3, 'aterriza'),
 ('C02', 4.96, 'hop', -2, 'otro hipo'),
 ('C02', 5.29, 'land', -3, 'aterriza'),
 ('C02', 7.04, 'hop', -2, 'otro hipo'),
 ('C02', 7.29, 'land', -3, 'aterriza'),
 # C03 · Pipo se acerca a la cámara
 ('C03', 0.88, 'shuffle', -4, 'Pipo se inclina hacia la cámara'),
 ('C03', 2.21, 'h_curious', -5, 'también quiere saberlo'),
 # CANAL_INICIO
 ('CANAL_INICIO', -0.25, 'whoosh', -2, 'entra la cortinilla'),
 ('CANAL_INICIO', 0.00, 'logo', 0, 'cortinilla del canal'),
 # C04 · la idea loca: una ranita
 ('C04', 0.83, 'arm_swish', 0, 'Pipo levanta la mano'),
 ('C04', 2.67, 'ding', -4, '¡la idea loca!'),
 ('C04', 4.80, 'boing', -5, 'la ranita salta en la panza'),
 # C05 · ¿una rana?
 ('C05', 0.83, 'cheek_rub', -3, 'Plop se tapa la boca'),
 ('C05', 4.92, 'h_shrug', -5, 'Plop no ha comido ranas… creo'),
 # C06 · aguantar la respiración
 ('C06', 1.50, 'h_stretch', -3, 'Plop infla los cachetes'),
 ('C06', 3.17, 'tremble', -5, 'aguanta y aguanta'),
 ('C06', 5.00, 'plip', -3, 'le cae una gota de sudor'),
 # C07 · Plop piensa
 ('C07', 1.96, 'think', -3, 'Plop ladea la cabeza'),
 ('C07', 4.33, 'shuffle', -5, 'se toca la cara'),
 # C08 · la pregunta correcta
 ('C08', 0.71, 'cheek_rub', -4, 'Plop se agarra la panza'),
 ('C08', 1.46, 'h_chime2', -5, '¡esa es la pregunta correcta!'),
 # C09 · piénsalo
 ('C09', 1.00, 'h_tick', -7, '¿tú qué crees? Piénsalo…'),
 ('C09', 6.40, 'zoom', -3, 'vamos a mirar dentro del pecho'),
 ('C09', 6.90, 'rev_cymbal', -5, 'entramos al pecho'),
 # C10 · los pulmones
 ('C10', 0.00, 'shimmer', -4, 'aparecen los pulmones'),
 ('C10', 1.00, 'h_breeze', -6, 'los pulmones se llenan de aire'),
 # C11 · el músculo en forma de cúpula
 ('C11', 1.04, 'squish', -4, 'el diafragma se mueve'),
 ('C11', 2.54, 'h_wobble', -5, 'los pulmones se balancean'),
 # C12 · el diafragma baja
 ('C12', 2.38, 'h_stretch', -4, 'el diafragma baja'),
 ('C12', 3.46, 'h_breeze', -5, 'entra el aire, los pulmones crecen'),
 # C13 · baja y sube
 ('C13', 0.96, 'h_wobble', -4, 'el diafragma sube'),
 ('C13', 2.46, 'h_stretch', -5, 'baja'),
 ('C13', 4.25, 'h_wobble', -5, 'sube'),
 # L1
 ('L1', 0.00, 'swipe', -1, 'lámina 1: pulmones y diafragma'),
 ('L1', 0.40, 'h_recap', -4, 'el jefe de tu respiración'),
 # C14 · Pipo se encoge de hombros
 ('C14', 0.67, 'arm_swish', -1, 'Pipo abre los brazos'),
 ('C14', 1.71, 'h_question', -4, '¿quién le da la orden?'),
 # C15 · el cerebro manda la orden por el nervio
 ('C15', 1.00, 'zap', -5, 'la orden viaja por el nervio'),
 # C16 · Plop sospecha
 ('C16', 2.25, 'squint', -3, 'Plop entrecierra los ojos'),
 ('C16', 5.71, 'uh_oh', -5, '¿y si la orden llega con un error?'),
 # C17 · ataque de risa
 ('C17', 1.04, 'shuffle', -3, 'Plop se ríe a carcajadas'),
 ('C17', 2.62, 'h_pops', -5, 'traga aire'),
 # C18 · el estómago se infla
 ('C18', 2.00, 'h_stretch', -4, 'el estómago se infla'),
 ('C18', 4.88, 'h_clayroll', -5, 'empuja el nervio hacia arriba'),
 ('C18', 5.96, 'squish', -3, 'le hace cosquillas al nervio'),
 # C19 · la orden equivocada
 ('C19', 0.62, 'h_zip', -3, 'la señal corre por el nervio'),
 ('C19', 4.50, 'alarm', -7, '¡aprieta ya!'),
 # C20 · ¡zas! el tirón del diafragma (0,54 s)
 ('C20', 0.54, 'boing', -2, '¡zas! el diafragma da un tirón'),
 ('C20', 0.62, 'land', -2, 'golpea abajo'),
 ('C20', 1.00, 'slide_up', -5, 'el aire entra de golpe'),
 ('C20', 1.25, 'h_breeze', -3, 'los pulmones se llenan'),
 # C21 · el chorro de aire en la garganta
 ('C21', 0.30, 'whoosh', -5, 'el chorro de aire sube'),
 ('C21', 1.04, 'h_breeze', -4, 'el aire sale por la garganta'),
 ('C21', 3.50, 'flutter', -5, 'las cuerdas vocales aletean'),
 # C22 · ¡clac! las cuerdas vocales se cierran (0,83 s)
 ('C22', 0.00, 'zoom', -5, 'primer plano de las cuerdas vocales'),
 ('C22', 0.83, 'key_lock', -2, '¡clac! se cierran de golpe'),
 ('C22', 0.83, 'land', -2, 'el portazo'),
 ('C22', 1.62, 'flutter', -6, 'las cuerdas tiemblan'),
 # C23 · Plop con hipo: cuatro saltos
 ('C23', 1.04, 'hop', -2, 'Plop da un salto de hipo'),
 ('C23', 1.38, 'land', -2, 'aterriza'),
 ('C23', 3.00, 'pop', -1, '¡hip! (el mismo instante en que la voz dice «¡hip!»)'),
 ('C23', 3.38, 'land', -3, 'aterriza'),
 ('C23', 5.00, 'hop', -2, 'otro hipo'),
 ('C23', 5.38, 'land', -3, 'aterriza'),
 ('C23', 7.04, 'hop', -2, 'otro hipo'),
 ('C23', 7.38, 'land', -3, 'aterriza'),
 # C24 · Pipo pregunta por qué se repite
 ('C24', 1.29, 'h_ponder', -5, 'Pipo parpadea, pensativo'),
 # C25 · tirón, portazo, ¡hip! (tres saltos y Plop se sienta)
 ('C25', 2.08, 'pop', -1, '¡hip!'),
 ('C25', 2.33, 'land', -2, 'aterriza'),
 ('C25', 4.17, 'pop', -2, '¡hip!'),
 ('C25', 4.46, 'land', -2, 'aterriza'),
 ('C25', 6.08, 'hop', -2, 'otro hipo'),
 ('C25', 6.50, 'land', -2, 'Plop se sienta, agotado'),
 # C26 · respirar lento
 ('C26', 0.50, 'relief', -6, 'Plop respira muy lento'),
 # C27 · se junta el dióxido de carbono
 ('C27', 0.00, 'zoom', -5, 'primer plano entre los pulmones'),
 ('C27', 0.25, 'land', -3, 'cae la primera bolita de gas'),
 ('C27', 0.92, 'h_marbles', -4, 'caen más bolitas'),
 ('C27', 3.00, 'h_pops', -5, 'se van amontonando'),
 ('C27', 5.50, 'h_click', -4, 'la última bolita encaja'),
 # C28 · las órdenes vuelven a salir en calma
 ('C28', 0.50, 'relief', -5, 'el cerebro se calma'),
 ('C28', 3.00, 'h_zip', -6, 'la señal viaja tranquila'),
 # C29 · el diafragma recupera su ritmo
 ('C29', 0.92, 'h_wobble', -6, 'sube suavecito'),
 ('C29', 2.42, 'h_stretch', -6, 'baja suavecito'),
 ('C29', 6.00, 'sparkle', -5, 'la puerta deja de dar portazos'),
 # C30 · ¡se fue!
 ('C30', 1.00, 'h_tada', -3, '¡se fue!'),
 ('C30', 2.25, 'cheek_rub', -3, 'Plop se toca la panza, contento'),
 ('C30', 5.21, 'h_claps', -5, '¡misterio resuelto!'),
 # L2 · repaso
 ('L2', 0.00, 'swipe', -1, 'lámina 2: repaso'),
 ('L2', 0.40, 'h_recap', -4, 'nervio, diafragma y cuerdas vocales'),
 # C31 · el perrito también tiene hipo
 ('C31', 0.88, 'pop', -2, '¡hip! el perrito salta'),
 ('C31', 1.21, 'land', -2, 'aterriza'),
 ('C31', 2.96, 'hop', -2, 'otro hipo'),
 ('C31', 3.30, 'land', -3, 'aterriza'),
 ('C31', 4.75, 'flutter', -5, 'le aletean las orejas'),
 ('C31', 6.71, 'flutter', -6, 'otra vez las orejas'),
 # C32 · el bebé
 ('C32', 0.50, 'h_twinkle', -6, 'un bebé antes de nacer'),
 # C33 · el reto
 ('C33', 0.83, 'arm_swish', -1, 'Plop levanta el brazo'),
 ('C33', 2.33, 'slide_up', -5, '¡un reto!'),
 # L3 · reto en casa
 ('L3', 0.00, 'swipe', -1, 'lámina 3: reto en casa'),
 ('L3', 0.40, 'h_tick', -6, 'el reloj: cuenta los hip'),
 # C34 · próxima pregunta
 ('C34', 0.92, 'arm_swish', 0, 'Plop saluda'),
 ('C34', 6.20, 'frost', -5, 'guiño al próximo episodio: el hielo'),
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
