# Guía de producción · La ciencia con Pipo y Plop

Guía interactiva para producir un año completo del canal: ciencia en plastilina para niños de 5 años en adelante, hecha con Google Flow (Veo), Nano Banana Pro, ElevenLabs y DaVinci Resolve.

La guía es un solo archivo: [`index.html`](index.html). Ábrelo en el navegador o publícalo con GitHub Pages (instrucciones abajo).

## Qué incluye

- **52 episodios completos de 5:00**, uno por semana, en cuatro temporadas de 13. Todos están desarrollados toma por toma, con el mismo nivel de detalle: guion, prompts, láminas, efectos, ficha científica, título, miniatura y reto.
- **Navegación pensada para 52 episodios**: selector agrupado por temporada, botones de episodio anterior y siguiente, buscador en el Plan anual y enlaces directos a cualquier pestaña de cualquier episodio (por ejemplo `index.html#e31-tomas`).
- **Nunca Pipo y Plop en la misma toma.** Para evitar que se mezclen colores y rasgos, cada toma lleva un solo personaje. El protagonista lleva el episodio (Pipo en los impares, Plop en los pares) y el otro aparece con un **banco de 20 reacciones** que se genera una sola vez y sirve para todo el año. Solo aparecen juntos en la cortinilla y en la tarjeta final, dos láminas fijas.
- **Un solo fondo para todo el canal.** La imagen [`fondo_canal.jpg`](fondo_canal.jpg), un estudio azul claro que transmite calma, es la primera referencia de cada fotograma, lámina, objeto y reacción. Los prompts no describen el fondo: solo piden usar la imagen adjunta tal cual. Como nunca cambia, los clips del banco encajan en todos los episodios.
- **Sin texto en pantalla.** El video se publica en varios idiomas: ni rótulos, ni letras, ni números, ni signos en la imagen. Todo lo dice la voz.
- **Contenido para niños de 5 años en adelante.** Ninguna parte del cuerpo suelta (la lengua siempre es la de Plop), lo de dentro del cuerpo se cuenta con juguetes, nada sale de la boca, sin sangre ni heridas, sin cortes de seres vivos y nada peligroso que se pueda imitar. Las reglas están en la pestaña Reglas de Flow y el validador las comprueba.
- **Pestañas por episodio**
  - **Guía**: los pasos de producción con casillas que se guardan, el título, la descripción con capítulos y la idea de miniatura.
  - **Guion**: la voz para ElevenLabs bloque por bloque, los efectos de sonido y la ficha científica (datos, simplificaciones y nivel de certeza).
  - **Tomas**: las 39 piezas del episodio (34 clips de 8 s y 5 láminas). Cada clip trae el prompt del fotograma (con `@FONDO`, en Nano Banana Pro) y el del movimiento (en Flow), con una sola acción continua de 8 segundos, más una ruta rápida con ingredientes.
  - **Elenco**: el fondo del canal (para ver y descargar), el protagonista, sus objetos de arcilla, la hoja de escala y el banco del canal con casillas de «ya generado».
- **Pestañas del canal**: Reglas de Flow (qué hacer y qué evitar, fallos comunes y calculadora de créditos), Canal (formato, voz, títulos, miniaturas y publicación como contenido para niños) y Plan anual (los 52 episodios con filtros, buscador, estado de producción y evaluación científica).

## Cifras del año

| | |
| --- | --- |
| Episodios | 52 (5:00 cada uno) |
| Clips por generar por episodio | entre 23 y 26 (1.229 en total) |
| Banco del canal | 20 reacciones y 2 láminas, generadas una sola vez (cubren 539 tomas del año) |
| Fondo | el mismo en todos los episodios: `fondo_canal.jpg` |
| Láminas por episodio | 5 (máximo pedido: 5) |
| Nivel de certeza | 45 de consenso · 5 de explicación más aceptada · 2 de ciencia abierta |
| Preguntas ancla | 14 episodios con temas que se buscan todo el año |

## Voz de ElevenLabs y duración

El guion de cada episodio dura unos 4 minutos de voz (unas 570 palabras con la velocidad de la voz en 0,9). Es lo correcto: cada frase ocupa unos 6 de los 8 segundos de su clip, y el resto es respiro para la imagen, la música y los efectos. **Los 5:00 los dan los clips**, no la voz. Si se monta al ritmo de una voz generada de corrido, el episodio se queda en unos 3:30.

Por eso la pestaña Guion incluye un archivo **.srt de tiempos**: se importa en DaVinci Resolve (File → Import → Subtitle) y marca dónde empieza cada frase. Se colocan primero los clips, después cada frase sobre su subtítulo.

## Tamaño de los objetos

Una imagen de referencia muestra el objeto solo y a pantalla completa, así que Flow no sabe si es una gota diminuta o una roca enorme, y tiende a hacerlo tan grande como el personaje. Cada uno de los 196 objetos tiene un tamaño fijado respecto al títere (unos 30 cm), y la guía lo escribe en cada prompt donde aparece con otro elemento. Además:

- Cada episodio tiene una **hoja de escala** (pestaña Elenco): una imagen del protagonista junto a todos sus objetos en su tamaño real, para comprobar antes de gastar créditos de video.
- Las tomas en las que el protagonista aparece junto a algo pequeño están marcadas como **escala crítica**: se compone primero el fotograma en Nano Banana Pro, se comprueba el tamaño y después se anima.

## Formato de cada episodio

| Bloque | Tiempo | Piezas |
| --- | --- | --- |
| 1 · El misterio | 0:00–0:28 | 3 clips + cortinilla |
| 2 · Las ideas de Pipo y Plop | 0:28–1:16 | 6 clips |
| 3 · Zoom al interior | 1:16–2:18 | 7 clips + lámina de partes |
| 4 · Cómo funciona | 2:18–3:30 | 9 clips |
| 5 · La prueba | 3:30–4:10 | 5 clips |
| 6 · Repaso, dato extra y reto | 4:10–4:48 | lámina de repaso + 3 clips + lámina de reto |
| 7 · Despedida | 4:48–5:00 | 1 clip + tarjeta final |

En todos los episodios se repiten los mismos momentos: la idea loca de Pipo (clip 4), la pregunta de Plop (clip 7), el «Piénsalo» (clip 9), el «¡Hagamos zoom!» (clip 10), el reto (clip 33) y la despedida que anuncia el episodio siguiente (clip 34). La voz explica; las acciones de los personajes no se narran.

## El plan anual

| Temporada | Episodios | Cierra con |
| --- | --- | --- |
| 1 | 1 a 13 | ¿Por qué explotan los volcanes? |
| 2 | 14 a 26 | ¿Por qué desaparecieron los dinosaurios? |
| 3 | 27 a 39 | ¿Qué es un agujero negro? |
| 4 | 40 a 52 | ¿Es verdad que creces mientras duermes? |

Nunca hay dos episodios seguidos de la misma categoría, y los episodios se llaman entre sí. Cada tema lleva uno o dos motores de interés: Me pasa a mí, Asco divertido, Superpoder animal, Antojo, Miedo seguro, Parece magia, Gigante y récord. El plan es un criterio editorial, no un pronóstico de vistas: ajústalo con los datos de YouTube Studio.

## Evaluación científica

Cada episodio declara su nivel de certeza y lo que simplifica a propósito. Los temas con la ciencia todavía abierta (sueños, bostezos) o con detalles en discusión (hipo, cosquillas, cerebro congelado, dedos arrugados, mareo) lo dicen en el guion con «los científicos creen» o «todavía se investiga». El panel **Evaluación científica** del Plan anual lista las correcciones hechas al revisar los temas.

La revisión se hizo con conocimiento científico general y comprobaciones puntuales en noviembre de 2026. No sustituye la revisión de un especialista: verifica cada ficha con dos fuentes antes de publicar.

## Publicarla con GitHub Pages

1. En el repositorio, ve a **Settings → Pages**.
2. En **Build and deployment**, elige **Deploy from a branch**.
3. Elige la rama donde está la guía (la principal, o esta rama de trabajo si aún no se ha fusionado) y la carpeta **/ (root)**. Guarda.
4. En uno o dos minutos la guía queda en `https://<tu-usuario>.github.io/<nombre-del-repositorio>/`.

El archivo `.nojekyll` evita que GitHub procese el sitio con Jekyll: se sirve tal cual.

## Cómo editarla

`index.html` se genera a partir de la carpeta `src/`. No lo edites a mano.

```
src/
  head.html, body.html   estilos y estructura de la página
  comun.js               datos comunes: bloques, cámaras, estilo, personajes, banco, plan anual
  episodios/epNN.js      un archivo por episodio (EP.push({...}))
  app.js                 la lógica de la página
  FORMATO.md             especificación completa del formato de episodio
validate.mjs             comprueba todas las reglas de formato
build.mjs                arma index.html
```

Después de cualquier cambio:

```sh
node validate.mjs && node build.mjs
```

El validador comprueba, entre otras cosas, que la estructura de cada episodio sea la del formato, que ninguna frase supere 18 palabras por clip, que las láminas quepan en su tiempo, que los prompts no partan la acción ni nombren al personaje que no protagoniza, que el acompañante aparezca al menos tres veces con sus reacciones del banco, que Pipo y Plop nunca compartan toma, y las reglas de contenido: ninguna parte del cuerpo suelta, nada que salga de la boca, ninguna letra, número o signo pedido en la imagen, y la marca de boca abierta en bostezos y lenguas.

## Vigencia de los datos

Modelos, precios y políticas se consultaron en noviembre de 2026. Flow retira Veo 3.1 Fast y Quality el 5 de diciembre de 2026; la guía usa Veo 3.1 Lite. Confirma siempre en Flow, ElevenLabs y YouTube Studio antes de producir.
