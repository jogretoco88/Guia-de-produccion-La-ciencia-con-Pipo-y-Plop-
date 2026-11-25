/* =====================================================================
   DATOS COMUNES A TODOS LOS EPISODIOS
   ===================================================================== */

/* Bloques del formato. Todos los episodios usan la misma estructura. */
var BLOCKS = [
  ["El misterio", "Mostrar el fenómeno y plantear la pregunta.", "El resultado se ve en los primeros 8 s. Nada de saludos ni logos antes."],
  ["Las ideas de Pipo y Plop", "Activar lo que el niño ya cree.", "La idea loca de Pipo, la pregunta de Plop y la primera pausa para pensar."],
  ["Zoom al interior", "Presentar las piezas del mecanismo.", "«¡Hagamos zoom!», el «¡Zuuum!» de Pipo y Plop, tres partes y una lámina que las nombra."],
  ["Cómo funciona", "Causa y efecto, paso a paso.", "Una comparación de Pipo, tensión que crece y un final en suspenso."],
  ["La prueba", "Volver al fenómeno, ahora explicado.", "Una pausa para predecir, la prueba (con Plop de piloto de pruebas si la ciencia lo permite) y la respuesta a Pipo y a Plop."],
  ["Repaso, dato extra y reto", "Fijar tres ideas y llevarlas a casa.", "Repaso de 8 s, un dato sorpresa como premio y un reto con un adulto."],
  ["Despedida", "Enlazar con el siguiente episodio.", "La próxima pregunta dicha en voz alta: en contenido infantil no hay pantallas finales."]
];

/* Cámaras del laboratorio (Blender). es = nombre, lente = distancia focal, mov = movimiento.
   Son fijas, como en un set de plastilina: solo el acercamiento lento se mueve. */
var CAM = {
  W: {es: "Plano general fijo", lente: 35, mov: "Fija, a la altura de los ojos del títere. Se ve toda la escena."},
  M: {es: "Plano medio fijo", lente: 50, mov: "Fija, a la altura de los ojos del títere."},
  C: {es: "Primer plano fijo", lente: 85, mov: "Fija, con el fondo suave (poca profundidad de campo)."},
  X: {es: "Macro fijo", lente: 100, mov: "Fija, a la altura del detalle, con el fondo muy desenfocado."},
  T: {es: "Cenital fijo", lente: 35, mov: "Fija, encima de la escena, mirando hacia abajo."},
  I: {es: "Acercamiento lento", lente: 50, mov: "Avanza despacio hacia el sujeto durante toda la toma. El sujeto se queda quieto."}
};

/* Las acciones de cada toma (escena inicial y acción, en inglés) son indicaciones de animación:
   las lee el exportador del proyecto de Blender, que detecta con ellas el movimiento de cada toma. */

/* Escenas iniciales que se repiten. */
var P_CENTER = "Pipo stands in the center of the set, facing the camera.";
var L_CENTER = "Plop stands in the center of the set, facing the camera.";
var P_FACE = "Pipo faces the camera, centered in frame.";
var L_FACE = "Plop faces the camera, centered in frame.";

/* Personajes. p = prompt maestro original (no cambiar: la consistencia depende de él). */
var ENV_ES = "De pie sobre un ciclorama de estudio mate blanco roto, sin costuras, con sombras de contacto suaves justo bajo la base y fondo blanco puro y despejado. Iluminación de estudio difusa y brillante desde arriba, con una luz de borde lateral intensa que crea microsombras de alto contraste sobre las profundas huellas dactilares de arcilla y las facetas rugosas sin alisar. Lente macro de 85 mm, poca profundidad de campo, colores mate sólidos y vibrantes.";
var WHO = {
  P: {tag: "@PIPO", es: "Pipo", rol: "El de las ideas locas",
      bio: "Un pequeño extraterrestre que vino a estudiar la Tierra. Impulsivo, valiente y optimista: siempre propone una explicación disparatada, porque cree que todo funciona como en su planeta, y la pone a prueba. Cuando se equivoca, se ríe y lo vuelve a intentar.",
      look: "Azul verdoso #096B7C, chaleco mostaza #D08316 con dos botones blancos. Cabeza de frijol sin cuello, cuerpo de pera, dos orejitas romas, ojos de botón, manoplas sin dedos y piernas de pilar.",
      voz: {id: "PykNIA7IVxUBZpRkQ3cS", es: "Aguda, brillante y rápida, con risa fácil (tono medio de unos 400 Hz). Sílabas con p, b y t."},
      en: "Pipo (the teal-blue clay creature in a mustard-yellow vest)",
      p: "Un solo plano frontal de cuerpo completo (formato 16:9, a la altura de los ojos, de la cabeza a los pies) de un auténtico títere táctil de stop-motion de Pipo, una adorable y peculiar criatura de laboratorio de arcilla, no humana. Cabeza ancha horizontal en forma de frijol, sin cuello, directamente sobre un cuerpo en forma de pera, y dos orejitas diminutas y romas como cuernitos a los lados. Párpados caídos de tiras de plastilina, grandes ojos de botón negros brillantes y curiosos, y una boca ancha, simple y cerrada de arcilla. Dos brazos superiores cortos como paletas (manoplas redondeadas y lisas, sin dedos) y dos piernas cortas cilíndricas como pilares que terminan en muñones lisos de base plana (sin dedos de los pies). Arcilla polimérica mate esculpida a mano, 100% de un solo color azul verdoso vibrante y uniforme, con profundas huellas dactilares. Lleva un chaleco sin mangas de arcilla mate amarillo mostaza uniforme y sólido, con dos botones blancos grandes de arcilla. " + ENV_ES},
  L: {tag: "@PLOP", es: "Plop", rol: "El de las preguntas",
      bio: "Un osito de agua (un tardígrado) que salió de una gota del terrario la primera vez que Pipo encendió la cámara de zoom. Prudente y pensativo: hace la pregunta que el espectador tiene en la cabeza. Es el más miedoso y el más indestructible: se hace bolita, aguanta casi todo y vuelve con un «¡plop!». Dentro de las cosas, él es el guía.",
      look: "Verde lima #578B27, pajarita naranja terracota #AD410E. Cabeza de frijol unida a un torso segmentado, dos nódulos sensoriales en forma de gota, ojos de botón y manoplas sin dedos.",
      voz: {id: "M46kPfoaSFdeaL0sLmqQ", es: "Suave, redonda y pausada, con murmullos pensativos (tono medio de unos 133 Hz). Sílabas con pl, l, m y n."},
      en: "Plop (the lime-green clay creature with a terracotta-orange bow tie)",
      p: "Un solo plano frontal de cuerpo completo (formato 16:9, a la altura de los ojos, de la cabeza a los pies) de un auténtico títere táctil de stop-motion de Plop, una adorable y peculiar criatura microscópica de arcilla parecida a un tardígrado. Cabeza ancha horizontal en forma de frijol fusionada con un torso regordete y segmentado, con dos diminutos nódulos sensoriales en forma de gota sobre la cabeza. Párpados caídos de tiras de plastilina, grandes ojos de botón negros brillantes con esclerótica color crema, y una boca ancha, simple y cerrada de arcilla. Dos brazos superiores cortos como paletas (manoplas redondeadas y lisas, sin dedos) y dos piernas cortas cilíndricas como pilares que terminan en muñones lisos de base plana (sin dedos de los pies). Arcilla polimérica mate esculpida a mano, 100% de un solo color verde lima vibrante y uniforme, con profundas huellas dactilares. Lleva una pajarita voluminosa de arcilla mate naranja terracota uniforme y sólida. " + ENV_ES}
};

/* =====================================================================
   BANCO DE REACCIONES
   Veinte reacciones de Pipo y Plop que se animan una sola vez en Blender y se reutilizan en
   los 52 episodios. Cada una tiene su frase fija en pipoplés (PIPOPLES): el niño la reconoce.
   Formato: código: [nombre, en pantalla, cámara, escena inicial (EN), acción única (EN)]
   ===================================================================== */
var BANK = {
  P1: ["Idea", "Pipo levanta un brazo: ¡tiene una idea!", "M", P_CENTER,
       "Pipo slowly raises one paddle arm high above his head with wide, excited eyes, as if he just had an idea."],
  P2: ["Incrédulo", "Pipo se echa atrás y niega con la cabeza.", "M", P_CENTER,
       "Pipo leans back with wide eyes and slowly shakes his head from side to side in disbelief."],
  P3: ["Ni idea", "Pipo se encoge de hombros.", "M", P_CENTER,
       "Pipo slowly lifts both paddle arms in a big shrug and tilts his head."],
  P4: ["Lo acepta", "Pipo se encoge de hombros y asiente con ojos sonrientes.", "M", P_CENTER,
       "Pipo shrugs with both paddle arms and nods slowly with smiling eyes."],
  P5: ["Impresionado", "Pipo asiente despacio y aplaude con las manoplas.", "M", P_CENTER,
       "Pipo nods slowly, impressed, and gently claps his paddle arms together."],
  P6: ["Curioso", "Pipo se inclina hacia la cámara, curioso.", "C", P_FACE,
       "Pipo leans slowly toward the camera with curious eyes and tilts his head."],
  P7: ["Desconcertado", "Pipo mira a un lado y al otro, sin entender.", "C", P_FACE,
       "Pipo looks slowly from one side to the other and back, completely baffled."],
  P8: ["Lo explica", "Pipo abre los brazos y asiente, como quien explica algo.", "M", P_CENTER,
       "Pipo slowly opens both paddle arms wide to the sides and nods."],
  P9: ["Celebra", "Pipo salta con los brazos en alto.", "M", P_CENTER,
       "Pipo hops in place with both paddle arms raised, again and again, celebrating."],
  P10: ["Adiós", "Pipo se despide con la manopla.", "M", P_CENTER,
        "Pipo waves one paddle arm at the camera, slowly and happily."],
  L1: ["Pensativo", "Plop ladea la cabeza, pensativo.", "C", "Plop faces the camera with one paddle arm resting on his chin.",
       "Plop slowly tilts his head from one side to the other, thinking, again and again."],
  L2: ["Sospecha", "Plop entrecierra los ojos y asiente: sospecha algo.", "C", L_FACE,
       "Plop narrows his eyes and nods slowly, as if he suspects what is about to happen."],
  L3: ["¡Eso es!", "Plop asiente contento, con saltitos.", "C", L_FACE,
       "Plop nods happily and bounces lightly in place, again and again."],
  L4: ["Asombro", "Plop abre mucho los ojos y se lleva las manoplas a la cara.", "C", L_FACE,
       "Plop's eyes grow wide and he slowly raises both paddle arms to his cheeks."],
  L5: ["Lo entendió", "Plop abre los ojos y levanta un brazo: ¡lo entendió!", "C", L_FACE,
       "Plop's eyes grow wide and he slowly raises one paddle arm, as if he just understood something."],
  L6: ["No quiere mirar", "Plop se tapa los ojos y espía entre las manoplas.", "C", "Plop faces the camera with both paddle arms covering his eyes.",
       "Plop peeks out from behind his paddle arms and hides again, over and over."],
  L7: ["¿Listos?", "Plop mira a cámara y asiente con ganas.", "C", L_FACE,
       "Plop blinks, leans slightly toward the camera and nods eagerly, again and again."],
  L8: ["Preocupado", "Plop se inclina hacia la cámara, preocupado.", "C", L_FACE,
       "Plop leans slowly toward the camera with worried eyes."],
  L9: ["Reto", "Plop se acerca a cámara e invita al reto.", "M", L_CENTER,
       "Plop takes one small step toward the camera and slowly raises one paddle arm, as if inviting the viewer."],
  L10: ["Adiós", "Plop se despide con la manopla.", "M", L_CENTER,
        "Plop waves one paddle arm at the camera, slowly and happily."]
};

/* Frases fijas en pipoplés: [frase, intención, etiqueta de ElevenLabs]. Ya pasaron el revisor de idioma
   (idioma.py) en español, inglés, francés, portugués de Brasil e hindi. */
var PIPOPLES = {
  P1: ["¡Bipi-ba!", "Tiene una idea", "[excited]"],
  P2: ["¿Nooo-bo?", "No se lo cree", "[surprised]"],
  P3: ["Mmm… ¿bo-ti?", "No tiene ni idea", "[curious]"],
  P4: ["Okibo, okibo.", "Lo acepta", "[thoughtful]"],
  P5: ["Oooh… ¡tiba!", "Impresionado", "[gasps]"],
  P6: ["¿Mm? ¿Pibo?", "Curioso", "[curious]"],
  P7: ["¿Ba? ¿Bo? ¿Bi?", "Desconcertado", "[surprised]"],
  P8: ["Pa-ti, pa-to… ¡tiba-po!", "Lo explica", "[excited]"],
  P9: ["¡Bipi-bipi-ba!", "Celebra", "[laughs]"],
  P10: ["¡Bai-bai-po!", "Se despide", "[excited]"],
  L1: ["Mmmm… ¿plu-ni?", "Pensativo", "[thoughtful]"],
  L2: ["Mmm-hm… plo-plo.", "Sospecha algo", "[mischievously]"],
  L3: ["¡Plin! ¡Plin-lu!", "¡Eso es!", "[excited]"],
  L4: ["¡Oh! Oh-lu-lu…", "Asombro", "[gasps]"],
  L5: ["¡Aaah, nilú!", "Lo entendió", "[surprised]"],
  L6: ["Uy, uy, uy… mu-mu.", "No quiere mirar", "[whispers]"],
  L7: ["¿Lu-ni? ¡Lu-ni!", "¿Listos?", "[excited]"],
  L8: ["Ay… plo-mu…", "Preocupado", "[sighs]"],
  L9: ["¡Tu-lu, tu-lu!", "Invita al reto", "[excited]"],
  L10: ["¡Chau-lú!", "Se despide", "[excited]"]
};
/* Lo que gritan Pipo y Plop juntos en el momento del zoom (clip 10 de cada episodio). */
var ZUUM = "¡Zuuum!";

/* Láminas del canal: la cortinilla y la tarjeta final. Se animan una vez y son iguales en todos los episodios.
   Sin texto en pantalla: el video se publica en varios idiomas. */
var CARDS = {
  T: ["Cortinilla del canal", "Pipo y Plop, uno a cada lado, contentos, en la puerta del laboratorio.",
      "Pipo stands on the left and Plop on the right, both facing the camera with happy eyes and smooth fingerless paddle arms.",
      "[excited] ¡La ciencia con Pipo y Plop!", "Suena el estribillo de la canción de apertura. La voz dice el nombre del canal. Sin título ni logo en pantalla."],
  F: ["Tarjeta final", "Pipo y Plop saludan en la puerta del laboratorio.",
      "Pipo on the left and Plop on the right, both facing the camera, each with one smooth fingerless paddle arm raised in a wave.",
      "La ciencia está en todas partes. ¡Hasta el próximo misterio!", "La voz anuncia el próximo misterio. Sin texto en pantalla."]
};

/* Kit sonoro del canal: se hace una vez y se usa en todos los episodios.
   [nombre, quién lo hace, indicación]. Los efectos siguen el criterio realista del canal:
   la fuente física real, la perspectiva de grabación y una sola fuente por efecto. */
var KIT = [
  ["Estribillo de la canción de apertura (4 s)", "Compositor", "Estribillo en pipoplés, con pocas notas y fácil de cantar. Marimba, ukelele, palmas y cuerdas punteadas. Va en la cortinilla y es igual en todos los idiomas."],
  ["Jingle del zoom (5 s)", "Compositor", "Acompaña el «¡Zuuum!» de Pipo y Plop en el clip 10. Siempre el mismo."],
  ["La idea de Pipo", "ElevenLabs", "A real incandescent light bulb switching on with a soft click and a faint filament hum, close-up"],
  ["El «¡plop!» de Plop", "ElevenLabs", "A soft ball of modeling clay dropped onto a wooden table, a single muffled thud, close-up"],
  ["Pausa para pensar (2 s)", "ElevenLabs", "Quiet small room ambience with a wall clock ticking softly in the distance, two seconds"],
  ["Repaso", "ElevenLabs", "Three soft ascending notes played on a real wooden marimba, close-up"],
  ["Reto en casa", "ElevenLabs", "A short cheerful fanfare played on a real plastic toy trumpet, close-up"]
];

/* Zonas del laboratorio: un solo set que se reutiliza todo el año. Paredes y suelo azul claro, para dar
   calma; muebles, objetos y luces de colores vivos, para llamar la atención. */
var ZONAS = [
  ["Cámara de zoom", "Entrar dentro de las cosas (bloques 3 y 4). Es la pieza que identifica al canal."],
  ["Mesa central", "La prueba y los experimentos."],
  ["Cocinita", "Comida y calor."],
  ["Rincón del cuerpo", "Maquetas del cuerpo, esqueleto de juguete y espejo."],
  ["Terrario", "Animales y plantas. De aquí salió Plop."],
  ["Tina y acuario", "Lo que flota, se hunde o pasa en el agua."],
  ["Ventana-planetario", "Cielo, clima, la Tierra y el espacio."],
  ["Rincón de casa", "Cama, sofá, baño y cosas de casa."],
  ["Pizarra", "Las láminas de cada episodio, sin texto."],
  ["Puerta del laboratorio", "La cortinilla y la tarjeta final."]
];

/* =====================================================================
   ESCALA: tamaño real de cada objeto junto al títere (unos 30 cm de alto).
   Las imágenes de referencia muestran cada objeto solo, sin nada que dé su
   tamaño; por eso el tamaño se escribe en cada prompt donde aparece con
   otro elemento. Código en el campo z de cada objeto.
   ===================================================================== */
var SIZES = {
  t: ["Diminuto", "unos 2 cm, más pequeño que la manopla", "tiny, about 2 cm", "much smaller than {N}'s paddle hand"],
  s: ["Pequeño", "unos 6 cm, como la manopla", "small, about 6 cm", "about the size of {N}'s paddle hand"],
  m: ["Mediano", "unos 12 cm, como la cabeza", "medium-sized, about 12 cm", "about the size of {N}'s head"],
  l: ["Grande", "unos 20 cm, le llega al pecho", "large, about 20 cm", "reaching up to {N}'s chest"],
  x: ["Como el títere", "unos 30 cm, igual de alto", "about 30 cm", "as tall as {N}"],
  g: ["Gigante", "más de 60 cm, más grande que el títere", "very large, more than 60 cm", "much bigger than {N}"]
};

/* =====================================================================
   VOZ: ritmo medido en ElevenLabs (Eleven v3, velocidad 1,0): el guion
   del Ep. 2, de unas 570 palabras, dio 3:30. Son unas 2,7 palabras por
   segundo. Con la velocidad en 0,9 baja a unas 2,45.
   ===================================================================== */
var VOICE = {rate: 2.7, speed: 0.9, lead: 0.4};

/* =====================================================================
   PLAN ANUAL: categorías, motores de interés, temporadas y niveles de certeza
   ===================================================================== */
var CATS = {
  cu: "Cuerpo", co: "Cocina", an: "Animales", ci: "Cielo y clima", ti: "Tierra y espacio", ca: "Cosas de casa"
};
var MOTORS = {
  M: ["Me pasa a mí", "Lo viven en su propio cuerpo o en su casa. La pregunta ya es suya antes de ver el video."],
  A: ["Asco divertido", "Entre los 5 y los 9 años lo asqueroso da risa y se comparte. Se cuenta con humor y con juguetes de arcilla: nunca se muestra nada desagradable."],
  S: ["Superpoder animal", "Un animal hace algo imposible para nosotros. Alimenta el gusto por coleccionar datos."],
  C: ["Antojo", "Comida que desean. El episodio vuelve a la memoria cada vez que la comen."],
  F: ["Miedo seguro", "Algo que asusta, visto a salvo y explicado. Entender da sensación de control."],
  G: ["Parece magia", "Un truco que sí tiene explicación y que pueden mostrar a otros."],
  R: ["Gigante y récord", "Lo más grande, lo más lejano, lo más fuerte. A esta edad los extremos fascinan."]
};
var SEASONS = [
  ["Temporada 1", 1, 13, "Presentación del canal. Un episodio de cada tipo y varias preguntas ancla. Cierra con el volcán, que reúne lo aprendido sobre el gas a presión en las palomitas y el refresco."],
  ["Temporada 2", 14, 26, "Abre con asco divertido y alterna con trucos que se pueden repetir en casa. Cierra con los dinosaurios."],
  ["Temporada 3", 27, 39, "Cosas gigantes y misterios del cuerpo. Varias respuestas contradicen lo que cree la mayoría. Cierra con el agujero negro."],
  ["Temporada 4", 40, 52, "Animales con superpoderes y episodios que se pueden mover según el calendario. Cierra el año con «¿creces mientras duermes?» y la invitación a medirse otra vez dentro de un año."]
];
var CERT = {
  1: ["Consenso científico", "La explicación está bien establecida y aparece en libros de texto."],
  2: ["Explicación más aceptada", "El mecanismo principal está respaldado, pero quedan detalles en discusión. El guion lo dice con «los científicos creen»."],
  3: ["Ciencia abierta", "Todavía no hay una respuesta definitiva. El guion presenta la idea mejor apoyada y dice claramente que se sigue investigando."]
};

/* =====================================================================
   CONTENIDO PARA NIÑOS DE 5 AÑOS EN ADELANTE
   El validador comprueba las palabras en inglés de las indicaciones de animación; estas reglas explican el porqué.
   ===================================================================== */
var SAFE = [
  ["Ninguna parte del cuerpo suelta", "Una lengua, un ojo, una mano o un cerebro sin su dueño pueden catalogarse como contenido sensible. Si hace falta, se muestran unidos a Pipo o a Plop: la lengua de Plop, su manopla, su rodilla."],
  ["Lo de dentro del cuerpo, con juguetes", "Pulmones, intestino, nervios o huesos se cuentan con piezas que no parecen anatomía: globos, un tubo de juegos, un cordón, una varita. La voz dice el nombre científico."],
  ["El cerebro es la cabeza del personaje", "Cuando una señal llega al cerebro, se ve una chispa que sube a la cabeza de Plop y sus antenitas se encienden como luces de alarma. Nada de cerebros sueltos ni cables pegados al cuerpo."],
  ["Nada sale de la boca", "Gotas, bolitas o líquidos que salen de la boca parecen vómito. Lo que llega a la lengua cae desde arriba, como lluvia. Un estornudo es una ráfaga de aire, no gotas."],
  ["Sin sangre ni heridas", "Un raspón es una mancha rosada que se oscurece. Lo que corre por dentro son discos o bolitas en un tubo, nunca sangre."],
  ["Sin cortes de seres vivos", "Ni personas, ni animales, ni personajes cortados por la mitad. Se corta un ají, una manzana o una semilla, no una oruga."],
  ["Nada que un niño pueda imitar y le haga daño", "Los personajes no tocan cables, enchufes, fuego ni cuchillos. Si algo se corta, es con un cuchillo de juguete y sin manos. El reto en casa siempre es con un adulto."],
  ["Lo que aguanta Plop, solo lo aguanta un tardígrado", "Cuando Plop se congela, sale volando o cae y se hace bolita, la voz recuerda que eso solo lo resiste un osito de agua. Pipo nunca lo imita, y el reto en casa nunca lo pide."],
  ["Sin texto en la imagen", "Ni rótulos, ni letras, ni números, ni signos de interrogación. El video se publica en varios idiomas: todo lo dice la voz."]
];

var EP = [];
