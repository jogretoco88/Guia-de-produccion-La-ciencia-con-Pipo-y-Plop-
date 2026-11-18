# Formato de un episodio

Cada episodio es un archivo `src/episodios/epNN.js` con un solo `EP.push({...})`.
Después de editar: `node validate.mjs && node build.mjs`. `index.html` se genera; no se edita a mano.

## Regla del elenco

- **Nunca Pipo y Plop en la misma toma** (`"C"` ni `"S"`). El protagonista (`star`) lleva el episodio: Pipo en los impares, Plop en los pares.
- El otro personaje aparece con sus **reacciones del banco** (`["R", código, voz]`) y, si el tema lo pide, en una toma propia, siempre solo (la lengua de Plop en el Ep. 3).
- Las láminas (`"S"`) llevan como mucho un personaje. La cortinilla (`["T"]`) y la tarjeta final (`["F"]`) son las únicas imágenes con los dos: láminas fijas, generadas en cada episodio con su fondo.

## Campos del episodio

```js
EP.push({
  n: 6, topic: "Cebolla", title: "¿Por qué lloramos al cortar cebolla?",
  star: "L",                 // P o L
  cat: "co", mot: "M", anc: 0,   // categoría, motores (1 o 2 letras), ancla (0/1)
  cert: 1,                   // 1 consenso · 2 explicación más aceptada · 3 ciencia abierta
  why: "Por qué engancha (una frase).",
  link: "Conecta con otros episodios (opcional).",
  nota: "Nota de producción (opcional).",
  secret: "La respuesta en una o dos frases.",
  bg: ["soft reddish-coral", "rojizo coral"],   // fondo del episodio, en inglés y en español. Opcional: por defecto BG.def (comun.js)
  thumb: "¡BUAAA!", thumbIdea: "Qué se ve en la miniatura y color de fondo.",
  vocab: "palabras nuevas", syn: "términos de búsqueda", tags: "#Uno #Dos",
  reto: "Reto en casa, completo.",
  objs: { a: {tag: "@CEBOLLA", z: "m", es: "Cebolla gigante", en: "the giant onion (…)", p: "Prompt de imagen en inglés."}, … },
                             // z: tamaño junto al títere (unos 30 cm): t diminuto ~2 cm · s pequeño ~6 cm
                             //    m mediano ~12 cm · l grande ~20 cm · x como el títere ~30 cm · g gigante >60 cm
  facts: ["Dato verificable.", …],      // 4 a 6
  simpl: ["Lo que simplificamos.", …],  // 1 a 3
  sfx: [["Nombre", "English sound prompt"], …],   // 4
  shots: [ … ]
});
```

## Tomas

```js
["#"]                                                     // empieza un bloque
["C", cámara, ingredientes, "En pantalla", "Escena inicial (EN)", "Acción única (EN)", "Voz", marcas]
["R", "L1", "Voz"]                                        // clip del banco
["W"]  o  ["W", "Voz"]                                    // despedida del protagonista (banco); la voz anuncia sola el siguiente episodio
["T"]                                                     // cortinilla del canal, 4 s
["S", segundos, ingredientes, "En pantalla", "Imagen (EN)", "Voz", "Lo que nombra la voz"]   // nota para el montaje: nunca va escrito en pantalla
["F"]                                                     // tarjeta final, 4 s
```

- **Cámara**: `W` general · `M` medio · `C` primer plano · `X` macro · `T` cenital · `I` acercamiento lento.
- **Ingredientes**: la letra del protagonista (`P` o `L`) y las letras de los objetos. Tres como máximo.
- **Marcas**: `k` mejor con fotograma clave · `<18` parte del último fotograma del clip 18 · `o` la boca se abre (bostezo, lengua afuera; obligatoria en esas tomas) · `a=t` cambia el tamaño del objeto `a` solo en esta toma.

## Tamaños (escala)

Las imágenes de referencia muestran cada objeto solo y a pantalla completa, así que Flow no sabe cuánto mide. La página escribe el tamaño en cada prompt donde aparecen dos o más elementos, a partir del campo `z` de cada objeto.

- Si el protagonista aparece junto a un objeto diminuto o pequeño (`t` o `s`), la toma se marca sola como **escala crítica**: su tarjeta propone primero el fotograma clave en Nano Banana Pro y deja los ingredientes sueltos como ruta rápida.
- No escribas tamaños en la escena («a giant drop»). Si una toma necesita otro tamaño, usa la marca `a=…`.

## Voz y duración

Cada frase dura unos 6 de los 8 segundos de su clip (ElevenLabs, Eleven v3, velocidad 0,9: unas 2,45 palabras por segundo). La voz completa dura unos 4 minutos y los 5:00 los dan los clips. Por eso cada frase tiene un máximo de 18 palabras, y en el montaje se coloca al comienzo de su clip con el archivo .srt de la pestaña Guion.

## Esqueleto fijo (5:00 = 34 clips de 8 s + láminas de 4, 6, 8, 6 y 4 s)

| Bloque | Tomas |
| --- | --- |
| 1 El misterio | clips 1–3, `T` |
| 2 Las ideas | clips 4–9 · el 4 es `["R","P1",…]` (idea loca) · el 7 es `["R","L1",…]` (pregunta de Plop) · el 9 es un acercamiento con «¿Tú qué crees? Piénsalo…» |
| 3 Zoom al interior | clips 10–13, `S` de 6 s (partes), clips 14–16 · el 10 empieza con «¡Hagamos zoom!» |
| 4 Cómo funciona | clips 17–25 · el 25 termina en suspenso |
| 5 La prueba | clips 26–30 · se responde a Pipo y a Plop |
| 6 Repaso, dato y reto | `S` de 8 s («Repasemos: …»), clips 31–32 (dato extra), clip 33 `["R","L9",…]`, `S` de 6 s (reto) |
| 7 Despedida | clip 34 `["W"]`, `F` |

## Fondo

Cada episodio tiene un solo fondo: un ciclorama mate de un color, con luces suaves y redondas en las paredes (`bg`). La página da el prompt de la foto del fondo vacío (`@FONDO`), y cada fotograma, reacción y lámina lo adjunta como primera referencia. Así el color y la luz no saltan de un clip a otro.

- Si una escena necesita su propio fondo (cielo, espacio, mar), se describe como un panel de arcilla sobre el set: `in front of a dark-blue clay night sky backdrop panel standing on the set`.
- No escribas el color del suelo ni del fondo en la escena («the white floor»): lo pone el estilo.

## Contenido para niños de 5 años en adelante

- Ninguna parte del cuerpo suelta: lengua, ojo, mano o cerebro siempre unidos a Pipo, a Plop o a un animal entero.
- Lo de dentro del cuerpo se cuenta con juguetes (globos, tubos, cordones). El cerebro es la cabeza del personaje: una chispa sube y sus antenitas se encienden.
- Nada sale de la boca: lo que llega a la lengua cae desde arriba.
- Sin sangre ni heridas, sin cortes de seres vivos, sin cables, enchufes, fuego ni cuchillos de verdad.
- Sin texto: ni letras, ni números, ni signos. Relojes en blanco (`blank clock face`), libros de dibujos (`picture book`), reglas con rayas de colores.
- Manos de Pipo y Plop: manoplas lisas, sin dedos.

El validador rechaza las palabras de anatomía que no pertenezcan a un personaje, lo que salga de la boca y los prompts que pidan letras, números o signos.

## Banco

Prompt fijo para que el gesto se reconozca, pero se genera **en cada episodio, con su fondo**. No se reutilizan clips de otros episodios.

Pipo: `P1` idea · `P2` incrédulo · `P3` ni idea · `P4` lo acepta · `P5` impresionado · `P6` curioso · `P7` desconcertado · `P8` lo explica · `P9` celebra · `P10` adiós.

Plop: `L1` pensativo · `L2` sospecha · `L3` ¡eso es! · `L4` asombro · `L5` lo entendió · `L6` no quiere mirar · `L7` ¿listos? · `L8` preocupado · `L9` reto · `L10` adiós.

## Voz

- Una frase por toma, 18 palabras como máximo. Español neutro. Números escritos con letras.
- Explica y pregunta; no narra lo que ya se ve.
- La idea de Pipo es una hipótesis que se pone a prueba. La pregunta de Plop es la del espectador y se responde en el bloque 5.
- Etiquetas de ElevenLabs con moderación: `[curious] [excited] [whispers] [thoughtful] [mischievously] [surprised] [laughs] [gasps] [sighs]`.

## Prompts

- Escena inicial: lo que se ve en el primer fotograma. Acción: un solo movimiento continuo que dura los 8 s (`slowly`, `again and again`). Sin «then», sin tiempos, sin comillas, sin texto en pantalla. Una sola toma, un solo personaje.
- Todo es arcilla sólida: gotas, vapor, luz y sonido son piezas de plastilina.
- Llama a cada objeto siempre igual que en su campo `en`.
