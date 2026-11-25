# Guía de producción · La ciencia con Pipo y Plop

Guía interactiva para producir un año completo del canal: ciencia en plastilina digital para niños de 6 a 8 años (de 5 a 9), animada en Blender, con voces de ElevenLabs y montaje en DaVinci Resolve.

> No basta con preguntar por qué: Pipo, un pequeño extraterrestre, y Plop, un osito de agua casi indestructible, se meten dentro de la respuesta.

La guía es un solo archivo: [`index.html`](index.html). Ábrelo en el navegador o publícalo con GitHub Pages (instrucciones abajo). El universo de la serie (personajes, mundo, tono y reglas) está en el Lore del proyecto.

## Qué incluye

- **52 episodios completos de 5:00**, uno por semana, en cuatro temporadas de 13, desarrollados toma por toma: guion, indicaciones de animación, láminas, efectos, ficha científica, título, miniatura y reto.
- **Navegación pensada para 52 episodios**: selector agrupado por temporada, botones de episodio anterior y siguiente, buscador en el Plan anual y enlaces directos a cualquier pestaña de cualquier episodio (por ejemplo `index.html#e31-tomas`).
- **Pipo y Plop siempre presentes.** El protagonista lleva el episodio (Pipo en los impares, Plop en los pares) y el otro lo acompaña con un **banco de 20 reacciones** que se animan una sola vez. Cada reacción tiene su frase fija en **pipoplés**, el idioma inventado de los dos.
- **Un narrador cómplice.** El creador del canal, que de niño descubrió el laboratorio, explica la ciencia y habla con Pipo y Plop. Es la única voz que cambia de idioma: la serie nunca se dobla.
- **Sin texto en pantalla.** El video se publica en 5 idiomas: ni rótulos, ni letras, ni números, ni signos en la imagen. Todo lo dice la voz.
- **Contenido para niños de 5 años en adelante.** Ninguna parte del cuerpo suelta, lo de dentro del cuerpo se cuenta con juguetes, nada sale de la boca, sin sangre ni heridas, sin cortes de seres vivos, nada peligroso que se pueda imitar, y lo que aguanta Plop solo lo aguanta un tardígrado. Las reglas están en la pestaña Producción 3D y el validador las comprueba.
- **Pestañas por episodio**
  - **Guía**: los pasos de producción en Blender con casillas que se guardan, el título, la descripción con capítulos y la idea de miniatura.
  - **Guion**: la voz del narrador bloque por bloque, las frases en pipoplés del episodio, el archivo .srt de tiempos, los efectos de sonido y la ficha científica.
  - **Tomas**: las 39 piezas del episodio (34 tomas de 8 s y 5 láminas), cada una con su voz, lo que se ve, el elenco, la cámara, los tamaños y su indicación de animación.
  - **Elenco**: Pipo y Plop con su aspecto y sus voces, los objetos del episodio con su tamaño y las tomas donde aparecen, y el banco del canal con casillas de «ya animado».
- **Pestañas del canal**: Producción 3D (programas, comandos de Blender, estilo, laboratorio, cámaras, escala y reglas de contenido), Canal (personajes, narrador, pipoplés, momentos firma, títulos, miniaturas y publicación) y Plan anual (los 52 episodios con filtros, buscador, estado de producción y evaluación científica).

## Cifras del año

| | |
| --- | --- |
| Episodios | 52 (5:00 cada uno) |
| Tomas para animar por episodio | entre 23 y 26 (1.229 en total) |
| Banco del canal | 20 reacciones y 2 láminas, animadas una sola vez (cubren 539 tomas del año) |
| Objetos de plastilina | 196, cada uno con su tamaño junto al títere |
| Láminas por episodio | 5 |
| Nivel de certeza | 45 de consenso · 5 de explicación más aceptada · 2 de ciencia abierta |
| Preguntas ancla | 14 episodios con temas que se buscan todo el año |

## Guiones al día con el Lore

Los episodios marcados con `lore: 1` ya tienen al narrador cómplice, la pausa para predecir antes de la prueba, a Pipo extraterrestre y a Plop de piloto de pruebas cuando la ciencia lo permite. El validador comprueba esas reglas en ellos. Los demás muestran en su pestaña Guía que el guion está pendiente de pasar al Lore.

## Voz y duración

El guion de cada episodio dura unos 4 minutos de voz. Es lo correcto: cada frase ocupa unos 6 de los 8 segundos de su toma, y el resto es respiro para la imagen, el pipoplés, la música y los efectos. **Los 5:00 los dan las tomas**, no la voz.

Por eso la pestaña Guion incluye un archivo **.srt de tiempos**: se importa en DaVinci Resolve (File → Import → Subtitle) y marca dónde empieza cada frase. La carpeta [`narracion/`](narracion/) tiene el flujo de narración sincronizada en 5 idiomas que se usó en los episodios 1 a 4.

## Formato de cada episodio

| Bloque | Tiempo | Piezas |
| --- | --- | --- |
| 1 · El misterio | 0:00–0:28 | 3 tomas + cortinilla |
| 2 · Las ideas de Pipo y Plop | 0:28–1:16 | 6 tomas |
| 3 · Zoom al interior | 1:16–2:18 | 7 tomas + lámina de partes |
| 4 · Cómo funciona | 2:18–3:30 | 9 tomas |
| 5 · La prueba | 3:30–4:10 | 5 tomas |
| 6 · Repaso, dato extra y reto | 4:10–4:48 | lámina de repaso + 3 tomas + lámina de reto |
| 7 · Despedida | 4:48–5:00 | 1 toma + tarjeta final |

En todos los episodios se repiten los momentos firma: la idea loca de Pipo («¡Bipi-ba!», toma 4), la pregunta de Plop (toma 7), el «Piénsalo» (toma 9), el «¡Hagamos zoom!» con el «¡Zuuum!» de los dos (toma 10), la prueba con el «¡plop!» de Plop, el reto («¡Tu-lu, tu-lu!», toma 33) y la despedida que anuncia el episodio siguiente (toma 34).

## El plan anual

| Temporada | Episodios | Cierra con |
| --- | --- | --- |
| 1 | 1 a 13 | ¿Por qué explotan los volcanes? |
| 2 | 14 a 26 | ¿Por qué desaparecieron los dinosaurios? |
| 3 | 27 a 39 | ¿Qué es un agujero negro? |
| 4 | 40 a 52 | ¿Es verdad que creces mientras duermes? |

Nunca hay dos episodios seguidos de la misma categoría, y los episodios se llaman entre sí. Cada tema lleva uno o dos motores de interés: Me pasa a mí, Asco divertido, Superpoder animal, Antojo, Miedo seguro, Parece magia, Gigante y récord.

## Evaluación científica

Cada episodio declara su nivel de certeza y lo que simplifica a propósito. Los temas con la ciencia todavía abierta (sueños, bostezos) o con detalles en discusión lo dicen en el guion con «los científicos creen» o «todavía se investiga». El creador del canal, que es docente, revisa cada ficha con dos fuentes antes de publicar.

## Publicarla con GitHub Pages

1. En el repositorio, ve a **Settings → Pages**.
2. En **Build and deployment**, elige **Deploy from a branch**.
3. Elige la rama donde está la guía y la carpeta **/ (root)**. Guarda.
4. En uno o dos minutos la guía queda en `https://<tu-usuario>.github.io/<nombre-del-repositorio>/`.

El archivo `.nojekyll` evita que GitHub procese el sitio con Jekyll: se sirve tal cual.

## Cómo editarla

`index.html` se genera a partir de la carpeta `src/`. No lo edites a mano.

```
src/
  head.html, body.html   estilos y estructura de la página
  comun.js               datos comunes: bloques, cámaras, personajes, banco, pipoplés, kit sonoro, zonas, plan anual
  episodios/epNN.js      un archivo por episodio (EP.push({...}))
  app.js                 la lógica de la página
  FORMATO.md             especificación completa del formato de episodio
validate.mjs             comprueba todas las reglas de formato
build.mjs                arma index.html
fondo_canal.jpg          referencia de color del laboratorio (azul claro)
```

Después de cualquier cambio:

```sh
node validate.mjs && node build.mjs
```

El proyecto de Blender lee esta misma carpeta `src/` con su exportador (`matriz/exportar.mjs`): si cambias un episodio, vuelve a exportarlo.

## Vigencia de los datos

Programas, voces y políticas se consultaron en noviembre de 2026. Confirma siempre en Blender, ElevenLabs y YouTube Studio antes de producir.
