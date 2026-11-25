# Formato de un episodio

Cada episodio es un archivo `src/episodios/epNN.js` con un solo `EP.push({...})`.
Después de editar: `node validate.mjs && node build.mjs`. `index.html` se genera; no se edita a mano.

La serie se produce en Blender (plastilina digital). Las tomas no son prompts: son indicaciones de animación que lee el exportador del proyecto 3D (`matriz/exportar.mjs`).

## Elenco

- El protagonista (`star`) lleva el episodio: Pipo en los impares, Plop en los pares. El otro siempre lo acompaña.
- El acompañante aparece con sus **reacciones del banco** (`["R", código, voz]`) y, cuando la historia lo pide, en sus propias tomas.
- En Blender son siempre los mismos modelos, así que **Pipo y Plop pueden compartir toma** (`"C"` con `P` y `L`). Las láminas (`"S"`) llevan como mucho un personaje.
- La cortinilla (`["T"]`) y la tarjeta final (`["F"]`) son las del canal: se animan una vez.

## Campos del episodio

```js
EP.push({
  n: 6, topic: "Cebolla", title: "¿Por qué lloramos al cortar cebolla?",
  star: "L",                 // P o L
  lore: 1,                   // el guion ya sigue el Lore (narrador cómplice, pausa para predecir…)
  cat: "co", mot: "M", anc: 0,   // categoría, motores (1 o 2 letras), ancla (0/1)
  cert: 1,                   // 1 consenso · 2 explicación más aceptada · 3 ciencia abierta
  why: "Por qué engancha (una frase).",
  link: "Conecta con otros episodios (opcional).",
  nota: "Nota de producción (opcional).",
  secret: "La respuesta en una o dos frases.",
  thumb: "¡BUAAA!", thumbIdea: "Qué se ve en la miniatura y color de fondo.",
  vocab: "palabras nuevas", syn: "términos de búsqueda", tags: "#Uno #Dos",
  reto: "Reto en casa, completo.",
  objs: { a: {tag: "@CEBOLLA", z: "m", es: "Cebolla gigante", en: "the giant onion (…)", p: "Referencia para modelarlo, en inglés."}, … },
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
["C", cámara, elenco, "En pantalla", "Escena inicial (EN)", "Acción única (EN)", "Voz", marcas]
["R", "L1", "Voz"]                                        // reacción del banco, con su frase en pipoplés
["W"]  o  ["W", "Voz"]                                    // despedida del protagonista (banco); la voz anuncia sola el siguiente episodio
["T"]                                                     // cortinilla del canal, 4 s
["S", segundos, elenco, "En pantalla", "Imagen (EN)", "Voz", "Lo que nombra la voz"]   // lámina en la pizarra; nunca lleva texto
["F"]                                                     // tarjeta final, 4 s
```

- **Cámara**: `W` general (35 mm) · `M` medio (50 mm) · `C` primer plano (85 mm) · `X` macro (100 mm) · `T` cenital (35 mm) · `I` acercamiento lento (50 mm).
- **Elenco**: `P`, `L` y las letras de los objetos. Tres como máximo.
- **Marcas**: `<18` continúa exactamente donde terminó la toma 18 · `o` la boca se abre (bostezo, lengua afuera; obligatoria en esas tomas) · `b` Plop se hace bolita y suena el «¡plop!» (la toma debe llevar a Plop) · `a=t` cambia el tamaño del objeto `a` solo en esta toma. La marca `k` de las versiones anteriores se ignora.

## Tamaños

Pipo y Plop miden unos 30 cm. Cada objeto lleva su tamaño en el campo `z`, y la guía lo muestra en cada toma donde aparece. No escribas tamaños en la escena («a giant drop»): si una toma necesita otro tamaño, usa la marca `a=…`.

## Voz y duración

Cada frase dura unos 6 de los 8 segundos de su toma (velocidad 0,9: unas 2,45 palabras por segundo). La voz completa dura unos 4 minutos y los 5:00 los dan las tomas. Por eso cada frase tiene un máximo de 18 palabras, y en el montaje se coloca al comienzo de su toma con el archivo .srt de la pestaña Guion.

## Esqueleto fijo (5:00 = 34 tomas de 8 s + láminas de 4, 6, 8, 6 y 4 s)

| Bloque | Tomas |
| --- | --- |
| 1 El misterio | tomas 1–3, `T` |
| 2 Las ideas | tomas 4–9 · la 4 es `["R","P1",…]` (idea loca, «¡Bipi-ba!») · la 7 es `["R","L1",…]` (pregunta de Plop) · la 9 es un acercamiento con «¿Tú qué crees? Piénsalo…» |
| 3 Zoom al interior | tomas 10–13, `S` de 6 s (partes), tomas 14–16 · la 10 empieza con «¡Hagamos zoom!» y Pipo y Plop gritan «¡Zuuum!» |
| 4 Cómo funciona | tomas 17–25 · la 25 termina en suspenso |
| 5 La prueba | tomas 26–30 · pausa para predecir · se responde a Pipo y a Plop |
| 6 Repaso, dato y reto | `S` de 8 s («Repasemos: …»), tomas 31–32 (dato extra), toma 33 `["R","L9",…]`, `S` de 6 s (reto) |
| 7 Despedida | toma 34 `["W"]`, `F` |

## Guion al día con el Lore (`lore: 1`)

Los episodios marcados con `lore: 1` cumplen además estas reglas, y el validador las comprueba:

- **El narrador es cómplice:** habla con el niño y también con Pipo y Plop («Pipo, no toques eso…»). Al menos una frase se dirige a uno de ellos.
- **Pausa para predecir** en la prueba (tomas 26 a 30): «¿Qué crees que pasará?».
- **Las reacciones dejan sitio al pipoplés:** la voz de una toma `"R"` tiene 15 palabras como máximo, porque antes suena la frase fija del personaje.
- **Pipo es un pequeño extraterrestre.** Cuando cree que algo funciona «como en su planeta», el narrador aclara cómo funciona en la Tierra. Del planeta de Pipo no se enseña ciencia.
- **Plop es el piloto de pruebas** cuando la ciencia lo permite: se congela, sale volando o cae, se hace bolita (marca `b`) y vuelve. La voz recuerda que eso solo lo aguanta un osito de agua.

## El laboratorio

Un solo set con paredes y suelo azul claro (`fondo_canal.jpg` es la referencia de color) y rincones que se reutilizan todo el año: cámara de zoom, mesa central, cocinita, rincón del cuerpo, terrario, tina y acuario, ventana-planetario, rincón de casa, pizarra y puerta del laboratorio.

- Si una escena necesita su propio fondo (cielo, espacio, mar), se describe como un panel de arcilla sobre el set: `in front of a dark-blue clay night sky backdrop panel standing on the set`.
- No escribas el color del suelo ni del fondo en la escena («the white floor»).

## Contenido para niños de 5 años en adelante

- Ninguna parte del cuerpo suelta: lengua, ojo, mano o cerebro siempre unidos a Pipo, a Plop o a un animal entero.
- Lo de dentro del cuerpo se cuenta con juguetes (globos, tubos, cordones). El cerebro es la cabeza del personaje: una chispa sube y sus antenitas se encienden.
- Nada sale de la boca: lo que llega a la lengua cae desde arriba.
- Sin sangre ni heridas, sin cortes de seres vivos, sin cables, enchufes, fuego ni cuchillos de verdad.
- Lo que aguanta Plop, solo lo aguanta un tardígrado: Pipo nunca lo imita y el reto en casa nunca lo pide.
- Sin texto: ni letras, ni números, ni signos. Relojes en blanco (`blank clock face`), libros de dibujos (`picture book`), reglas con rayas de colores.
- Manos de Pipo y Plop: manoplas lisas, sin dedos.

El validador rechaza las palabras de anatomía que no pertenezcan a un personaje, lo que salga de la boca y las indicaciones que pidan letras, números o signos.

## Banco

Las 20 reacciones se animan **una sola vez** en Blender y sirven para los 52 episodios. Cada una tiene su frase fija en pipoplés (`PIPOPLES` en `comun.js`), que se graba una vez y no se traduce.

Pipo: `P1` idea «¡Bipi-ba!» · `P2` incrédulo · `P3` ni idea · `P4` lo acepta · `P5` impresionado · `P6` curioso · `P7` desconcertado · `P8` lo explica · `P9` celebra · `P10` adiós.

Plop: `L1` pensativo · `L2` sospecha · `L3` ¡eso es! · `L4` asombro · `L5` lo entendió · `L6` no quiere mirar · `L7` ¿listos? · `L8` preocupado · `L9` reto «¡Tu-lu, tu-lu!» · `L10` adiós.

## Voz

- Una frase por toma, 18 palabras como máximo. Español neutro. Números escritos con letras.
- Explica y pregunta; no narra lo que ya se ve.
- La idea de Pipo es una hipótesis que se pone a prueba. La pregunta de Plop es la del espectador y se responde en el bloque 5.
- Etiquetas de ElevenLabs con moderación: `[curious] [excited] [whispers] [thoughtful] [mischievously] [surprised] [laughs] [gasps] [sighs]`.

## Indicaciones de animación

- Escena inicial: lo que se ve al empezar la toma. Acción: un solo movimiento continuo que dura los 8 s (`slowly`, `again and again`). Sin «then», sin tiempos, sin comillas.
- Todo es arcilla sólida: gotas, vapor, luz y sonido son piezas de plastilina.
- Llama a cada objeto siempre igual que en su campo `en`, y nombra a Pipo y a Plop solo si están en el elenco de la toma.
