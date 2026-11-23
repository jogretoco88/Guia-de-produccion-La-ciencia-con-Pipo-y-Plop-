# La ciencia con Pipo y Plop en 3D

Especificación de la versión 3D del canal. Se modela, se anima y se renderiza en Blender, en la computadora del estudio. No hay video generado por IA. Las voces se generan en ElevenLabs: el narrador en cada idioma, y Pipo y Plop en su idioma inventado.

Los guiones, las tomas y los objetos salen de la guía (`src/`). El exportador los convierte en escenas que Blender lee:

```sh
node 3d/exportar.mjs        # escribe 3d/escenas/epNN.json, 3d/assets.json y 3d/resumen.txt
node 3d/exportar.mjs -v     # además lista los clips de objetos que no tienen movimiento de la biblioteca
```

Las reglas que se pueden cambiar (cámaras, movimientos, zonas, familias, idioma de los personajes) están en `3d/config.json`. Después de cambiar la guía o la configuración, vuelve a correr el exportador.

## Estilo

- **Todo es plastilina.** Material mate con huellas dactilares, marcas de herramienta y colores sólidos. Gotas, vapor, luz, sonido y electricidad también son piezas de arcilla, nunca humo, partículas ni luz real.
- **Animación de stop-motion.** Se anima «de a dos»: cada pose dura 2 fotogramas de 24 fps, como en el stop-motion de estudio. Solo se renderizan los fotogramas únicos (12 por segundo) y se duplican al montar. El render tarda la mitad.
- **Cámaras de estudio.** Casi todas fijas, como un trípode en un set real. Solo el acercamiento lento (`I`) se mueve.
- **Salida:** 1920×1080, 24 fps.
- **Motor:** Eevee para todas las tomas. Cycles solo para miniaturas y planos destacados.
- **Contenido para niños.** Lo de dentro del cuerpo se muestra siempre como juguete o maqueta, de colores planos y formas redondas.

## Personajes

| | Pipo | Plop |
|---|---|---|
| Rol | El de las ideas locas | El de las preguntas |
| Color | Azul verdoso, chaleco amarillo mostaza con dos botones blancos | Verde lima, pajarita naranja terracota |
| Forma | Cabeza de frijol sin cuello, cuerpo de pera, dos orejitas romas | Cabeza de frijol unida a un torso segmentado, dos nódulos en forma de gota |
| Común | Ojos de botón negros, párpados de tira, brazos de manopla sin dedos, piernas de pilar sin dedos | |

La descripción completa está en `src/comun.js` (`WHO.P.p` y `WHO.L.p`) y es la referencia del modelado.

**En 3D, Pipo y Plop pueden estar juntos en cualquier toma.** La regla de «un solo personaje por episodio» existía para que la IA no mezclara sus rasgos; en 3D son siempre los mismos modelos. El protagonista sigue llevando el episodio (Pipo en los impares, Plop en los pares).

Cada personaje necesita: modelo esculpido, esqueleto (Rigify), formas de boca para el idioma inventado, párpados que parpadean y el material de plastilina.

**Hay más títeres.** El exportador marca 119 clips con animales (21 animales distintos) y varios episodios usan figuras humanas pequeñas: un niño, un bebé, una figura con bata de laboratorio. Conviene hacer **una figura humana genérica** con variaciones de ropa y pelo, en el mismo estilo de Pipo y Plop.

## Voces

- **El narrador** explica la ciencia, en cada idioma. Su texto es la columna «Voz» de la guía.
- **Pipo y Plop hablan entre ellos en pipoplés**, un idioma inventado sin palabras de ningún idioma real. El sentido lo dan la entonación, la cara y el cuerpo. Como no hay palabras, **la misma animación y el mismo render sirven para todos los idiomas**. Solo cambia la pista del narrador.
- Pipo usa sílabas con p, b y t, rápidas y con energía. Plop usa pl, l, m y n, suaves y pausadas.
- Cada reacción del banco tiene su frase fija, por ejemplo: la idea de Pipo es «¡Pipi-ba!»; Plop invitando al reto, «¡Tu-lu, tu-lu!». Los niños la aprenden y la repiten. Las 20 frases están en `config.json` → `idioma.reacciones`.
- Las voces de Pipo y Plop están diseñadas y guardadas en ElevenLabs (noviembre de 2026). Sus identificadores están en `config.json` → `idioma.voces`:
  - **Pipo:** `PykNIA7IVxUBZpRkQ3cS`. Aguda, brillante y rápida, con risa fácil (tono medio de unos 400 Hz).
  - **Plop:** `M46kPfoaSFdeaL0sLmqQ`. Suave, redonda y pausada, con murmullos pensativos (unos 133 Hz).
- La sincronía de labios se hace con Rhubarb Lip Sync, que analiza el audio y da las formas de boca fotograma a fotograma.

## El laboratorio

Un solo set grande con rincones que se reutilizan todo el año. Las paredes y el suelo son azul claro y transmiten calma. Los objetos, el mobiliario y las luces de colores vivos lo hacen llamativo.

| Zona | Para qué | Tomas en el año |
|---|---|---|
| Cámara de zoom | Bloques 3 y 4: dentro de las cosas. La pieza que identifica al canal: Pipo y Plop entran y todo crece a su alrededor | 832 |
| Rincón del cuerpo | Maquetas del cuerpo, esqueleto de juguete, espejo | 214 |
| Ventana-planetario | Cielo, clima, Tierra y espacio | 196 |
| Cocinita | Comida y calor | 167 |
| Terrario | Animales | 167 |
| Pizarra | Las cinco láminas de cada episodio | 156 |
| Rincón de casa | Cama, sofá, baño | 133 |
| Puerta del laboratorio | Cortinilla y tarjeta final | 104 |
| Tina y acuario | Lo que flota, se hunde o pasa en el agua | 59 |
| Mesa central | La prueba y los experimentos | se usa dentro de las demás zonas |

El exportador asigna la zona de cada toma por la categoría del episodio y por las palabras de la escena. Las tomas de los bloques 3 y 4 van siempre a la cámara de zoom.

## Animación

| Cómo se anima | Clips del año | Qué hace falta |
|---|---|---|
| **Por script**, con la biblioteca de movimientos | 814 | Un script que aplica el movimiento al objeto |
| A mano, con Pipo o Plop | 261 | Tu tiempo de animación |
| A mano, con animales (títeres) | 119 | Un esqueleto simple por animal |
| A mano, objetos con un movimiento especial | 35 | El exportador los lista con `-v` |
| Reacciones de la biblioteca | 539 | Se animan una vez (20 acciones) y se reutilizan |
| Láminas | 156 | Acercamiento lento por script |

**La biblioteca de movimientos** traduce la acción en inglés de cada toma a uno de estos 15 movimientos: flota, cae, rueda o se desliza, gira, crece, se encoge, tiembla, revienta, ondula, se balancea, empuja, aparece, rebota, late y acercamiento de cámara. Cada uno se programa una vez en Blender. La descripción de cada movimiento está en `config.json` → `movimientos`.

**El banco de reacciones** pasa a ser una biblioteca de 20 acciones de Blender (P1–P10, L1–L10). Se animan una vez y sirven con cualquier cámara, en cualquier zona y con los dos personajes juntos.

## Objetos

`assets.json` tiene los 183 objetos distintos del año, con sus episodios, cuántas tomas los usan y su prioridad. **Alta:** salen en más de un episodio. **Media:** 8 tomas o más.

| Familia | Cantidad | Técnica |
|---|---|---|
| Maquetas en corte | 36 | Un solo método: el objeto entero se corta con un plano y la cara del corte lleva su propio material |
| Partículas | 34 | Formas simples (esfera, gota, anillo) repartidas con instancias |
| Animales | 21 | Títeres con esqueleto simple, en el estilo de Pipo y Plop |
| Comida | 17 | Esculpido sólido |
| Cielo y espacio | 16 | Esferas y discos; nubes y rayos de arcilla |
| Cuerpo | 11 | Siempre como juguete o maqueta |
| Otros objetos | 48 | Uno por uno |

El tamaño de cada objeto respecto al títere está en su descripción (`en` y `ref`), por ejemplo «about knee-high to a puppet». Pipo y Plop miden unos 30 cm en el mundo del set.

## Render

| | Por episodio | Año (52) |
|---|---|---|
| Duración | 5:00 | 260 min |
| Fotogramas únicos (12 por segundo) | 3 600 | 187 200 |
| Render a 2 s por fotograma | 2 h | 104 h |
| Render a 10 s por fotograma | 10 h | 520 h |
| Render a 20 s por fotograma | 20 h | 1 040 h |

Los tiempos por fotograma son hipotéticos: el piloto da el real. Si cabe en una noche por episodio, no hace falta la nube.

## Formato de una escena (`escenas/epNN.json`)

```jsonc
{
  "episodio": 1, "titulo": "¿Por qué explotan las palomitas de maíz?",
  "protagonista": "P", "zonaBase": "cocina",
  "render": { "ancho": 1920, "alto": 1080, "fps": 24, "animarDeA": 2 },
  "duracion": 300, "framesUnicos": 3600,
  "objetos": ["grano_de_maiz_gigante", "grano_partido_por_la_mitad", "palomita_gigante"],
  "tomas": [
    {
      "n": 2, "bloque": 1, "tipo": "personaje", "inicio": 8, "dur": 8, "frames": 192,
      "camara": { "codigo": "M", "focal": 50, "movimiento": "fija" },
      "zona": "cocina", "personajes": ["P"], "objetos": ["palomita_gigante"],
      "movimientos": ["balancea"], "animacion": "a_mano",
      "escena": "Pipo stands on the left beside the popcorn…",
      "accion": "Pipo slowly leans toward the popcorn…",
      "narrador": "¿Cómo cabe algo tan grande y esponjoso dentro de algo tan pequeño y tan duro?"
    }
  ]
}
```

Tipos de toma: `objetos`, `personaje`, `reaccion` (con `accion` del banco y `voz` en pipoplés), `lamina`, `cortinilla` y `tarjeta_final`. Las dos últimas son del canal: se hacen una vez.

Por ahora cada clip dura 8 s, como en la guía. En 3D un plano puede durar lo que pida el montaje: cuando se reescriba un episodio para 3D, `dur` se ajusta toma por toma.

## Siguientes pasos

1. **En la computadora nueva:** instalar Blender, comprobar que usa la RTX 5060 Ti y probar el material de plastilina con un render 1080p.
2. **Pipo y Plop:** esculpido, esqueleto, formas de boca y material.
3. **Voces:** grabar con las voces ya guardadas las 20 frases de las reacciones.
4. **El laboratorio:** primero la cámara de zoom y la cocinita, que son las que necesita el piloto.
5. **Piloto, Ep. 1 (Palomitas):** escena completa a partir de `escenas/ep01.json`. Mide el tiempo de animación y de render.
6. **Scripts de Blender** que leen `escenas/epNN.json`: montan la zona, colocan objetos y cámara, aplican los movimientos y renderizan.
