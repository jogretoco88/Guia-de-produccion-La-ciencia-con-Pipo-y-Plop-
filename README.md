# Guía de producción · La ciencia con Pipo y Plop

Guía interactiva para producir un año del canal: ciencia en plastilina para niños de 6 años en adelante, con Google Flow (Veo), Nano Banana Pro, ElevenLabs y DaVinci Resolve.

Todo está en un solo archivo: [`index.html`](index.html). Ábrelo en el navegador o publícalo con GitHub Pages.

## Qué incluye

- **52 episodios de 5:00** en 16:9, uno por semana. Los episodios 1 a 5 están desarrollados toma por toma. Los episodios 6 a 52 tienen su ficha de desarrollo.
- **Guía**: los pasos de producción con casillas, el título, la descripción con capítulos y la idea de miniatura.
- **Guion**: la voz para ElevenLabs, bloque por bloque. Una frase por toma. Incluye efectos de sonido y la ficha científica de cada episodio.
- **Tomas**: las 39 tomas de cada episodio (34 clips de 8 s y 5 láminas) con su frase, lo que debe verse y el prompt listo para copiar. Cada prompt pide una sola acción continua para los 8 segundos. Cada clip trae un Plan B con fotograma clave.
- **Elenco**: los prompts maestros de Pipo, Plop y los objetos de cada episodio.
- **Reglas de Flow**: qué hacer y qué evitar para reducir alucinaciones, soluciones a los fallos comunes y una calculadora de créditos.
- **Canal**: el formato fijo, cómo habla la voz, título y miniatura, publicación como contenido para niños y ritmo de trabajo.
- **Plan anual**: los 52 episodios en cuatro temporadas de 13, con filtros por categoría y por motor de interés, estado de cada episodio y un encargo listo para copiar que desarrolla cada ficha en un episodio completo.

## Formato de cada episodio

| Bloque | Tiempo | Tomas |
| --- | --- | --- |
| 1 · El misterio | 0:00–0:28 | 3 clips + cortinilla |
| 2 · Las ideas de Pipo y Plop | 0:28–1:16 | 6 clips |
| 3 · Zoom al interior | 1:16–2:18 | 7 clips + lámina de partes |
| 4 · Cómo funciona | 2:18–3:30 | 9 clips |
| 5 · La prueba | 3:30–4:10 | 5 clips |
| 6 · Repaso, dato extra y reto | 4:10–4:48 | lámina de repaso + 3 clips + lámina de reto |
| 7 · Despedida | 4:48–5:00 | 1 clip + tarjeta final |

## El plan anual

| Temporada | Episodios | Cierra con |
| --- | --- | --- |
| 1 | 1 a 13 | ¿Por qué explotan los volcanes? |
| 2 | 14 a 26 | ¿Por qué desaparecieron los dinosaurios? |
| 3 | 27 a 39 | ¿Qué es un agujero negro? |
| 4 | 40 a 52 | ¿Es verdad que creces mientras duermes? |

Reglas del orden: nunca dos episodios seguidos de la misma categoría, Pipo protagoniza los impares y Plop los pares, y los episodios se llaman entre sí (el volcán recuerda a las palomitas; las burbujas, al jabón; el barco, al hielo).

Cada tema lleva uno o dos motores de interés: Me pasa a mí, Asco divertido, Superpoder animal, Antojo, Miedo seguro, Parece magia, Gigante y récord. El plan es un criterio editorial apoyado en estudios sobre lo que preguntan y ven los niños, no un pronóstico de vistas: ajústalo con los datos de YouTube Studio.

## Publicarla con GitHub Pages

1. Lleva `index.html` a la rama principal del repositorio.
2. En **Settings → Pages**, elige **Deploy from a branch**, la rama principal y la carpeta raíz.
3. La guía queda en `https://<tu-usuario>.github.io/<nombre-del-repositorio>/`.

## Cómo editarla

Los datos están dentro de `index.html`, en el bloque `<script>`, antes de la lógica de la página:

- `BLOCKS`, `CAM`, `STYLE_V`, `STYLE_I`, `WHO`, `KIT`: datos comunes a todos los episodios.
- `EP.push({...})`: un bloque por episodio desarrollado, con sus objetos, ficha científica, efectos y tomas.
- `CATS`, `MOTORS`, `SEASONS`, `PLAN`: el plan anual. Cada elemento de `PLAN` es la ficha de un episodio por desarrollar.

Formato de una toma:

```js
// Clip de 8 s
["C", cámara, ingredientes, "En pantalla (español)", "Escena inicial (inglés)", "Acción única (inglés)", "Voz (español)", marcas]
// Lámina fija
["S", segundos, ingredientes, "En pantalla (español)", "Imagen (inglés)", "Voz (español)", "Rótulos para DaVinci"]
```

- **Cámara**: `W` general, `M` medio, `C` primer plano, `X` macro, `T` cenital, `I` acercamiento lento.
- **Ingredientes**: `P` Pipo, `L` Plop y las letras de los objetos del episodio. Nunca `P` y `L` juntos, y tres como máximo.
- **Marcas**: `k` mejor con fotograma clave · `r` sirve para otros episodios · `<18` parte del último fotograma del clip 18 · `=E1_C33` reutiliza ese clip.

El prompt completo se arma solo a partir de esos campos, así que el estilo se repite palabra por palabra en todas las tomas.

### Pasar una ficha a episodio completo

1. En **Plan anual**, abre la ficha y copia el **encargo para desarrollar este episodio**.
2. Pégalo en una conversación nueva junto con esta guía y pide el episodio en el formato de `EP.push({...})`.
3. Añade ese bloque después del último episodio desarrollado. La ficha de `PLAN` se sustituye sola: no hace falta borrarla.

## Vigencia de los datos

Modelos, precios y políticas se consultaron en noviembre de 2026. Flow retira Veo 3.1 Fast y Quality el 5 de diciembre de 2026; la guía usa Veo 3.1 Lite. Confirma siempre en Flow, ElevenLabs y YouTube Studio antes de producir.
