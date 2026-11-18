# Formato de un episodio

Cada episodio es un archivo `src/episodios/epNN.js` con un solo `EP.push({...})`.
Después de editar: `node validate.mjs && node build.mjs`. `index.html` se genera; no se edita a mano.

## Regla del elenco

- Cada episodio tiene **un solo personaje generado en Flow**: el protagonista (`star`). Pipo en los impares, Plop en los pares.
- El otro personaje aparece **solo con clips del banco** (`["R", código, voz]`). Nunca en un clip propio (`"C"`).
- Las láminas del episodio (`"S"`) no llevan personajes. La cortinilla (`["T"]`) y la tarjeta final (`["F"]`) son del canal.

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
  thumb: "¡BUAAA!", thumbIdea: "Qué se ve en la miniatura y color de fondo.",
  vocab: "palabras nuevas", syn: "términos de búsqueda", tags: "#Uno #Dos",
  reto: "Reto en casa, completo.",
  objs: { a: {tag: "@CEBOLLA", es: "Cebolla gigante", en: "the giant onion (…)", p: "Prompt de imagen en inglés."}, … },
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
["S", segundos, ingredientes, "En pantalla", "Imagen (EN)", "Voz", "Rótulos"]
["F"]                                                     // tarjeta final, 4 s
```

- **Cámara**: `W` general · `M` medio · `C` primer plano · `X` macro · `T` cenital · `I` acercamiento lento.
- **Ingredientes**: la letra del protagonista (`P` o `L`) y las letras de los objetos. Tres como máximo.
- **Marcas**: `k` mejor con fotograma clave · `<18` parte del último fotograma del clip 18 · `o` la boca puede abrirse (bostezo).

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

## Banco

Pipo: `P1` idea · `P2` incrédulo · `P3` ni idea · `P4` lo acepta · `P5` impresionado · `P6` curioso · `P7` desconcertado · `P8` lo explica · `P9` celebra · `P10` adiós.

Plop: `L1` pensativo · `L2` sospecha · `L3` ¡eso es! · `L4` asombro · `L5` lo entendió · `L6` no quiere mirar · `L7` ¿listos? · `L8` preocupado · `L9` reto · `L10` adiós.

## Voz

- Una frase por toma, 18 palabras como máximo. Español neutro. Números escritos con letras.
- Explica y pregunta; no narra lo que ya se ve.
- La idea de Pipo es una hipótesis que se pone a prueba. La pregunta de Plop es la del espectador y se responde en el bloque 5.
- Etiquetas de ElevenLabs con moderación: `[curious] [excited] [whispers] [thoughtful] [mischievously] [surprised] [laughs] [gasps] [sighs]`.

## Prompts

- Escena inicial: lo que se ve en el primer fotograma. Acción: un solo movimiento continuo que dura los 8 s (`slowly`, `again and again`). Sin «then», sin tiempos, sin comillas, sin texto en pantalla.
- Todo es arcilla sólida: gotas, vapor, luz y sonido son piezas de plastilina.
- Llama a cada objeto siempre igual que en su campo `en`.
