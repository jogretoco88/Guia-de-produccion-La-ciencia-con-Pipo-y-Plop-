# Ep. 1 · ¿Por qué explotan las palomitas de maíz? — Kit de audio en 5 idiomas

- **Voz:** José Gregorio Torres (voz clonada), con **ElevenLabs Eleven v4**.
- **Efectos:** no se generó ninguno nuevo. Se reutilizaron dos bibliotecas:
  - la de **ElevenLabs Sound Effects v3** creada para el Ep. 3;
  - la de efectos hechos para el Ep. 2.
- **Video:** `E01_palomitas_mudo.mp4` (300,000 s, 24 fps), **sin ningún texto en pantalla**.

## Cómo usarlo (lo más simple)

1. Abre el video mudo en tu editor.
2. Pon `XX/E01_XX_mezcla.wav` en el segundo **0:00**. Ya trae:
   - la voz;
   - los 111 efectos, cada uno en el segundo exacto de su acción;
   - los rellenos de los silencios entre frases.
3. Exporta. Haz una versión por idioma.

Si prefieres ajustar tú el balance, usa dos pistas por separado, ambas en el segundo 0:00:
- `XX/E01_XX_narracion.wav`, la voz sola;
- `XX/E01_XX_efectos.wav`, los efectos de ese idioma: los 111 originales más los rellenos de sus silencios.

Si no quieres los rellenos, usa `efectos/E01_efectos.wav`: son solo los 111 efectos, iguales para los 5 idiomas.

Para YouTube puedes subir `E01_XX_subtitulos.srt` como subtítulos de ese idioma. Los tiempos son los reales de la voz.

## Qué hay en cada carpeta

### Idiomas (ES, EN, FR, PT, HI)

| Archivo | Para qué sirve |
|---|---|
| `E01_XX_mezcla.wav` / `.mp3` | Voz y efectos mezclados. Dura exactamente lo mismo que el video. Está a -16 LUFS. |
| `E01_XX_narracion.wav` / `.mp3` | Solo la voz, 48 kHz / 24 bit, mono, a -16 LUFS. |
| `E01_XX_efectos.wav` / `.mp3` | Los 111 efectos, en su sitio, más los rellenos de ese idioma (300,000 s). |
| `E01_XX_rellenos.csv` | Cada relleno de ese idioma: segundo, toma, entre qué frases suena, tipo de sonido y duración. |
| `E01_XX_subtitulos.srt` | Subtítulos con el tiempo real de cada frase. No se queman en el video. |
| `E01_XX_posiciones.csv` | Toma, archivo, segundo de inicio y de fin de cada frase, y aceleración aplicada. |
| `frases/E01_XX_<toma>.wav` | Cada frase suelta, ya ajustada. Colócala en el segundo `inicio_s` del CSV. |
| `E01_XX_vista_previa_360p.mp4` | El video con la mezcla, para revisar rápido. |

### efectos (común a los 5 idiomas)

| Archivo | Para qué sirve |
|---|---|
| `E01_efectos.wav` / `.mp3` | Los 111 efectos solos, sin rellenos (300,000 s). |
| `E01_hoja_de_efectos.csv` | Las 111 entradas, una por fila: segundo exacto, toma, categoría, efecto, acción en pantalla, de qué biblioteca sale y su descripción. |
| `biblioteca/` | Los 52 sonidos sueltos, ya recortados y nivelados. El prefijo indica la categoría: `F_`, `M_` o `T_`. Los que llevan `h_` salen de la biblioteca del Ep. 2. |
| `rellenos_muestras/` | Los rellenos del español, sueltos, para escucharlos o reutilizarlos. |

## Efectos de sonido: qué se pidió y qué se entregó

| Categoría | Pedido | Entregado | De ElevenLabs (Ep. 3) | Biblioteca del Ep. 2 |
|---|---|---|---|---|
| Foley de movimiento y textura | 45 a 65 | **63** entradas (22 sonidos distintos) | 50 | 13 |
| Acentos de expresión (*mickey mousing*) | 25 a 35 | **31** entradas (21 sonidos distintos) | 21 | 10 |
| Transiciones y refuerzos visuales | 12 a 20 | **17** entradas (9 sonidos distintos) | 15 | 2 |
| **Total** | | **111** entradas (52 sonidos) | **86** (34 sonidos) | **25** (18 sonidos) |

**Créditos de ElevenLabs gastados en efectos: 0.** Todos los efectos se reutilizaron de bibliotecas que ya existían.

Algunos sonidos se repiten, siempre en acciones del mismo tipo: grietas, aterrizajes o brazos que se mueven. Cada repetición está en su propio segundo.

**Los dos estallidos, al fotograma**
- **C01 (4,42 s):** dos grietas (2,62 y 3,21 s) y el grano que se sacude en el plato (3,79 s). En el fotograma 4,42 s suenan juntos el crujido del casco y el «¡pum!», con un *whoosh* de las cáscaras que salen volando. A los 5,00 s caen los pedazos.
- **C26 (212,75 s):** el platillo invertido sube la tensión (211,6 s) y termina justo cuando el casco revienta. En 212,75 s suenan el crujido y el «¡pum!», y en 212,79 s el soplo del vapor que escapa. Después caen las cáscaras (213,3 s) y suena un destello al aparecer la palomita.
- La palabra «¡Pum!» de la voz está anclada a ese momento: en los 5 idiomas, la frase de C26 empieza en 212,65 s.

**Otros ejemplos**
- **Foley:**
  - los **8 saltos de Pipo** sobre el grano (C06). Cada aterrizaje se midió fotograma a fotograma siguiendo la altura de Pipo: 1,08 · 1,92 · 2,75 · 3,75 · 4,58 · 5,54 · 6,58 · 7,42 s de la toma;
  - el corte del grano por la mitad (C10);
  - la bolita que cae sobre el casco (C11);
  - la gota que rebota contra las paredes del casco (C15);
  - el vapor que empuja el casco desde dentro (C21);
  - la gelatina de almidón que tiembla (C22);
  - el grano que se sacude en el plato (C23).
- **Acentos:**
  - la campanita de la idea loca de Pipo (C04);
  - el silbato que baja cuando no se oye nada (C05);
  - la llave que cierra cuando el casco no deja salir el agua (C15);
  - la llamarada al encenderse el calor (C17);
  - el silbido de vapor cuando la gota se vuelve vapor (C18) y cuando el grano es una «mini olla a presión» (C23);
  - el «¡ta-da!» de la respuesta (C29);
  - el grano que se desinfla por su grieta (C31).
- **Transiciones:**
  - el zoom que entra al grano (C09–C10);
  - las cortinillas del canal, con el mismo logo sonoro de los otros episodios;
  - los cambios de lámina (L1–L3), con el carillón de repaso en L1 y L2;
  - una burbuja como guiño al próximo episodio, el del jabón (C34).

Cada efecto está en el segundo exacto de su acción. Ese segundo se midió con el análisis de movimiento fotograma a fotograma del video y con hojas de contacto a 2 fotogramas por segundo.

## Rellenos en los silencios entre frases

Para mantener la atención mientras el narrador no habla, los silencios entre frases que quedaban vacíos llevan un sonido pequeño. **Los 111 efectos no se movieron**: la pista de efectos es idéntica a la original fuera de los rellenos.

- **Hechos aquí, sin ElevenLabs.** Se sintetizaron con código, sin gastar créditos.
- **Según la escena.**
  - Gotitas y burbujas en las escenas de la gota, el vapor y la gelatina.
  - Campanita o tic-tac cuando Pipo y Plop piensan o descubren algo.
  - Blips en las escenas del calor y la presión.
  - Punteos en los momentos de Pipo y Plop.
  - Marimba en los dos estallidos y en la palomita.
  - Campanita en las láminas y cortinillas.
- **Afinados entre sí.** Todos usan la escala pentatónica de do, así que no desentonan entre ellos.
- **Más suaves que los efectos.** Van a -27 dBFS, frente a -20/-22 de los efectos.
- **Solo en el hueco libre.**
  - Empiezan 0,10 s después de la frase y acaban 0,08 s antes de la siguiente.
  - Dejan 0,05 s de margen alrededor de cada efecto original.
- **Uno por idioma.** Cada idioma hace sus pausas en segundos distintos, así que cada uno tiene sus propios rellenos.

| Idioma | Rellenos | Silencios con relleno | Sobre la voz | Sobre los efectos |
|---|---|---|---|---|
| ES | 64 | 38 | ninguno | ninguno |
| EN | 69 | 38 | ninguno | ninguno |
| FR | 73 | 38 | ninguno | ninguno |
| PT | 65 | 38 | ninguno | ninguno |
| HI | 60 | 37 | ninguno | ninguno |

## Cómo se sincronizó la voz

Es el mismo método de los episodios 2, 3 y 4:

- **Una frase por toma**, anclada al segundo exacto de su toma, para que el error no se acumule.
- **Ventanas de tiempo.**
  - Clips: la voz va de 0,3 s a 7,6 s de cada toma.
  - Láminas: igual, con su propia duración.
  - Cortinillas: de 0,2 s al final de la cortinilla.
  - Ninguna frase pisa a la siguiente.
- **Ancla de acción.** En C26 la frase empieza con «¡Pum!», que arranca en 212,65 s, justo antes del estallido en pantalla (212,75 s).
- **Ajuste fino.** Antes de grabar, recorté 6 frases que iban justas de tiempo. Aun así, si una frase se pasaba de su ventana, la aceleré sin cambiar el tono:
  - PT: L2 ×1,071;
  - HI: C23 ×1,016, C26 ×1,024 y C33 ×1,029;
  - ES, EN y FR: ninguna.
- **Verificación.** Transcribí los 5 idiomas completos con ElevenLabs Scribe y los comparé frase por frase con el guion. Resultado: **39/39 en los 5 idiomas**, sin ningún «Pipou» en francés.
  - PT: en C11 la transcripción oye «pericampo» en lugar de «pericarpo». Es una palabra difícil y el sentido se mantiene.
  - FR: en L1 la transcripción oye «Coque est dure». Es cosa de la transcripción y el sentido no cambia.
  - HI: las diferencias son solo de escritura. Scribe escribe en letras latinas las palabras en inglés (*starch*, *helmet*, *pressure cooker*), usa «गर्मी» por «गरमी» y escribe «180» en cifras.
- **Nivel.** Todas las pistas de voz y todas las mezclas quedan a -16 LUFS, con picos de -1,5 dBTP, el estándar para video en línea.

Los detalles están en `INFORME_SINCRONIZACION.txt` (tiempos de cada frase y de cada efecto), en `guion_5_idiomas.txt` y en `qa/`.
