# Guía de producción · La ciencia con Pipo y Plop

Guía interactiva para producir la Temporada 1 del canal: ciencia en plastilina para niños de 6 años en adelante, con Google Flow (Veo), Nano Banana Pro, ElevenLabs y DaVinci Resolve.

Todo está en un solo archivo: [`index.html`](index.html). Ábrelo en el navegador o publícalo con GitHub Pages.

## Qué incluye

- **5 episodios de 5:00** en 16:9. Cada uno tiene 34 clips de 8 segundos y 5 láminas fijas.
- **Guía**: los pasos de producción con casillas, el título, la descripción con capítulos y la idea de miniatura.
- **Guion**: la voz para ElevenLabs, bloque por bloque. Una frase por toma. Incluye efectos de sonido y la ficha científica de cada episodio.
- **Tomas**: las 39 tomas de cada episodio con su frase, lo que debe verse y el prompt listo para copiar. Cada prompt pide una sola acción continua para los 8 segundos. Cada clip trae un Plan B con fotograma clave.
- **Elenco**: los prompts maestros de Pipo, Plop y los objetos de cada episodio.
- **Reglas de Flow**: qué hacer y qué evitar para reducir alucinaciones, soluciones a los fallos comunes y una calculadora de créditos.
- **Canal**: el formato fijo, cómo habla la voz, título y miniatura, publicación como contenido para niños, ritmo de trabajo y próximas preguntas.

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

## Publicarla con GitHub Pages

1. Lleva `index.html` a la rama principal del repositorio.
2. En **Settings → Pages**, elige **Deploy from a branch**, la rama principal y la carpeta raíz.
3. La guía queda en `https://<tu-usuario>.github.io/<nombre-del-repositorio>/`.

## Cómo editarla

Los datos están dentro de `index.html`, en el bloque `<script>`, antes de la lógica de la página:

- `BLOCKS`, `CAM`, `STYLE_V`, `STYLE_I`, `WHO`, `KIT`, `IDEAS`: datos comunes a toda la temporada.
- `EP.push({...})`: un bloque por episodio, con sus objetos, ficha científica, efectos y tomas.

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

## Vigencia de los datos

Modelos, precios y políticas se consultaron en noviembre de 2026. Flow retira Veo 3.1 Fast y Quality el 5 de diciembre de 2026; la guía usa Veo 3.1 Lite. Confirma siempre en Flow, ElevenLabs y YouTube Studio antes de producir.
