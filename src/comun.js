/* =====================================================================
   DATOS COMUNES A TODOS LOS EPISODIOS
   ===================================================================== */

/* Bloques del formato. Todos los episodios usan la misma estructura. */
var BLOCKS = [
  ["El misterio", "Mostrar el fenómeno y plantear la pregunta.", "El resultado se ve en los primeros 8 s. Nada de saludos ni logos antes."],
  ["Las ideas de Pipo y Plop", "Activar lo que el niño ya cree.", "Dos ideas locas puestas a prueba, la pregunta de Plop y la primera pausa para pensar."],
  ["Zoom al interior", "Presentar las piezas del mecanismo.", "El ritual «¡Hagamos zoom!», tres partes y una lámina que las nombra."],
  ["Cómo funciona", "Causa y efecto, paso a paso.", "Una comparación de Pipo, tensión que crece y un final en suspenso."],
  ["La prueba", "Volver al fenómeno, ahora explicado.", "La recompensa visual. Se responde la idea de Pipo y la pregunta de Plop."],
  ["Repaso, dato extra y reto", "Fijar tres ideas y llevarlas a casa.", "Repaso de 8 s, un dato sorpresa como premio y un reto con un adulto."],
  ["Despedida", "Enlazar con el siguiente episodio.", "La próxima pregunta dicha en voz alta: en contenido infantil no hay pantallas finales."]
];

/* Cámaras. v = texto para el clip, k = encuadre del fotograma clave, es = nombre en español. */
var CAM = {
  W: {es: "Plano general fijo", v: "Static wide shot at eye level, locked-off camera, the whole scene visible", k: "Wide shot at eye level, the whole scene visible"},
  M: {es: "Plano medio fijo", v: "Static medium shot at eye level, locked-off camera", k: "Medium shot at eye level"},
  C: {es: "Primer plano fijo", v: "Static close-up at eye level, locked-off camera, shallow depth of field", k: "Close-up at eye level, shallow depth of field"},
  X: {es: "Macro fijo", v: "Static macro extreme close-up, locked-off camera, shallow depth of field", k: "Macro extreme close-up, shallow depth of field"},
  T: {es: "Cenital fijo", v: "Static top-down overhead shot, locked-off camera", k: "Top-down overhead shot"},
  I: {es: "Acercamiento lento", v: "Very slow, smooth camera push-in", k: "Medium shot"}
};

/* Bloques de estilo: se repiten palabra por palabra en todos los prompts. */
var STYLE_V = "Handmade claymation stop-motion look, animated on twos at 12 fps with slightly choppy handmade motion. Matte polymer clay with deep visible fingerprints and solid uniform colors. Seamless matte off-white studio cyclorama, soft diffused top light, gentle contact shadows, plain pure-white background.";
var STYLE_I = "Authentic handmade stop-motion claymation still. Matte polymer clay with deep visible fingerprints and solid uniform colors. Seamless matte off-white studio cyclorama with soft contact shadows right under each base and a plain pure-white background. Bright diffused studio light from above with a strong side rim light, 85 mm macro lens look, shallow depth of field.";
var MOUTH = "The puppet keeps its mouth closed and stays silent the whole time.";
var AUDIO = "Audio: quiet studio room tone and soft clay foley only.";

/* Escenas iniciales que se repiten. */
var P_CENTER = "Pipo stands in the center of the set, facing the camera.";
var L_CENTER = "Plop stands in the center of the set, facing the camera.";
var P_FACE = "Pipo faces the camera, centered in frame.";
var L_FACE = "Plop faces the camera, centered in frame.";

/* Personajes. p = prompt maestro original (no cambiar: la consistencia depende de él). */
var ENV_ES = "De pie sobre un ciclorama de estudio mate blanco roto, sin costuras, con sombras de contacto suaves justo bajo la base y fondo blanco puro y despejado. Iluminación de estudio difusa y brillante desde arriba, con una luz de borde lateral intensa que crea microsombras de alto contraste sobre las profundas huellas dactilares de arcilla y las facetas rugosas sin alisar. Lente macro de 85 mm, poca profundidad de campo, colores mate sólidos y vibrantes.";
var WHO = {
  P: {tag: "@PIPO", es: "Pipo", rol: "El de las ideas locas",
      bio: "Impulsivo y valiente. Siempre propone una explicación disparatada y la pone a prueba con su propio cuerpo. Cuando se equivoca, se ríe y lo vuelve a intentar.",
      en: "Pipo (the teal-blue clay creature in a mustard-yellow vest)",
      p: "Un solo plano frontal de cuerpo completo (formato 16:9, a la altura de los ojos, de la cabeza a los pies) de un auténtico títere táctil de stop-motion de Pipo, una adorable y peculiar criatura de laboratorio de arcilla, no humana. Cabeza ancha horizontal en forma de frijol, sin cuello, directamente sobre un cuerpo en forma de pera, y dos orejitas diminutas y romas como cuernitos a los lados. Párpados caídos de tiras de plastilina, grandes ojos de botón negros brillantes y curiosos, y una boca ancha, simple y cerrada de arcilla. Dos brazos superiores cortos como paletas (manoplas redondeadas y lisas, sin dedos) y dos piernas cortas cilíndricas como pilares que terminan en muñones lisos de base plana (sin dedos de los pies). Arcilla polimérica mate esculpida a mano, 100% de un solo color azul verdoso vibrante y uniforme, con profundas huellas dactilares. Lleva un chaleco sin mangas de arcilla mate amarillo mostaza uniforme y sólido, con dos botones blancos grandes de arcilla. " + ENV_ES},
  L: {tag: "@PLOP", es: "Plop", rol: "El de las preguntas",
      bio: "Observador y paciente. Se fija en el detalle que nadie vio y hace la pregunta que el espectador tiene en la cabeza. Sus preguntas mueven la historia.",
      en: "Plop (the lime-green clay creature with a terracotta-orange bow tie)",
      p: "Un solo plano frontal de cuerpo completo (formato 16:9, a la altura de los ojos, de la cabeza a los pies) de un auténtico títere táctil de stop-motion de Plop, una adorable y peculiar criatura microscópica de arcilla parecida a un tardígrado. Cabeza ancha horizontal en forma de frijol fusionada con un torso regordete y segmentado, con dos diminutos nódulos sensoriales en forma de gota sobre la cabeza. Párpados caídos de tiras de plastilina, grandes ojos de botón negros brillantes con esclerótica color crema, y una boca ancha, simple y cerrada de arcilla. Dos brazos superiores cortos como paletas (manoplas redondeadas y lisas, sin dedos) y dos piernas cortas cilíndricas como pilares que terminan en muñones lisos de base plana (sin dedos de los pies). Arcilla polimérica mate esculpida a mano, 100% de un solo color verde lima vibrante y uniforme, con profundas huellas dactilares. Lleva una pajarita voluminosa de arcilla mate naranja terracota uniforme y sólida. " + ENV_ES}
};

/* =====================================================================
   BANCO DE REACCIONES
   Se genera una sola vez y se usa en los 52 episodios. Gracias a él, en cada episodio solo se
   genera un personaje en Flow: el otro aparece siempre con estos clips ya aprobados.
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
/* Láminas del canal: las dos únicas imágenes donde Pipo y Plop aparecen juntos. Se generan una vez. */
var CARDS = {
  T: ["Cortinilla del canal", "Pipo y Plop a los lados, con espacio para el título.",
      "Pipo stands on the left and Plop on the right, both facing the camera. Wide clean empty white space between them and across the upper third of the image.",
      "[excited] ¡La ciencia con Pipo y Plop!", "Título del episodio y logo del canal. En el centro puedes superponer el objeto del episodio."],
  F: ["Tarjeta final", "Pipo y Plop saludan.",
      "Pipo on the left and Plop on the right, both facing the camera, each with one paddle arm raised in a wave. Wide clean empty white space between them.",
      "La ciencia está en todas partes. ¡Hasta el próximo misterio!", "«Próximo misterio» y el título del siguiente episodio, en el centro."]
};

/* Kit sonoro del canal: se genera una vez y se usa en todos los episodios. */
var KIT = [
  ["Cortinilla del canal (3 s)", "Playful three-second jingle with marimba and ukulele, cheerful, ending on a bright high note"],
  ["La idea loca de Pipo", "Quick comic slide whistle going up"],
  ["¡Hagamos zoom!", "Short soft whoosh, playful cartoon transition"],
  ["Pausa para pensar (2 s)", "Gentle playful ticking clock, two seconds"],
  ["Repaso", "Bright three-note chime"],
  ["Reto en casa", "Short cheerful toy trumpet fanfare"]
];

/* =====================================================================
   PLAN ANUAL: categorías, motores de interés, temporadas y niveles de certeza
   ===================================================================== */
var CATS = {
  cu: "Cuerpo", co: "Cocina", an: "Animales", ci: "Cielo y clima", ti: "Tierra y espacio", ca: "Cosas de casa"
};
var MOTORS = {
  M: ["Me pasa a mí", "Lo viven en su propio cuerpo o en su casa. La pregunta ya es suya antes de ver el video."],
  A: ["Asco divertido", "Entre los 6 y los 9 años lo asqueroso da risa y se comparte. Es lo que más se repite en el recreo."],
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

var EP = [];
