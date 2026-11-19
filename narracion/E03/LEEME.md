# Ep. 3 · ¿Por qué pica el ají si no está caliente? — Kit de audio en 5 idiomas

- **Voz:** José Gregorio Torres (voz clonada), con **ElevenLabs Eleven v4**.
- **Efectos:** **ElevenLabs Sound Effects v3**.
- **Video:** `E03_aji_mudo.mp4` (300,000 s, 24 fps). El video no se tocó.

## Cómo usarlo (lo más simple)

1. Abre el video mudo en tu editor.
2. Pon `XX/E03_XX_mezcla.wav` en el segundo **0:00**. Ya trae la voz, los 106 efectos en el segundo exacto de su acción
   y los rellenos de los silencios entre frases.
3. Exporta. Haz una versión por idioma.

Si prefieres ajustar tú el balance, usa dos pistas por separado, ambas en el segundo 0:00:
- `XX/E03_XX_narracion.wav`, la voz sola;
- `XX/E03_XX_efectos.wav`, los efectos de ese idioma: los 106 originales más los rellenos de sus silencios.

Si no quieres los rellenos, usa `efectos/E03_efectos.wav`: son solo los 106 efectos, iguales para los 5 idiomas.

Para YouTube puedes subir `E03_XX_subtitulos.srt` como subtítulos de ese idioma. Los tiempos son los reales de la voz.

## Qué hay en cada carpeta

### Idiomas (ES, EN, FR, PT, HI)

| Archivo | Para qué sirve |
|---|---|
| `E03_XX_mezcla.wav` / `.mp3` | Voz y efectos mezclados. Dura exactamente lo mismo que el video. Está a -16 LUFS. |
| `E03_XX_narracion.wav` / `.mp3` | Solo la voz, 48 kHz / 24 bit, mono, a -16 LUFS. |
| `E03_XX_efectos.wav` / `.mp3` | Los 106 efectos, en su sitio original, más los rellenos de ese idioma (300,000 s). |
| `E03_XX_rellenos.csv` | Cada relleno de ese idioma: segundo, toma, entre qué frases suena, tipo de sonido y duración. |
| `E03_XX_subtitulos.srt` | Subtítulos con el tiempo real de cada frase. No se queman en el video. |
| `E03_XX_posiciones.csv` | Toma, archivo, segundo de inicio y de fin de cada frase, y aceleración aplicada. |
| `frases/E03_XX_<toma>.wav` | Cada frase suelta, ya ajustada. Colócala en el segundo `inicio_s` del CSV. |
| `E03_XX_vista_previa_360p.mp4` | El video con la mezcla, para revisar rápido. |

### efectos (común a los 5 idiomas)

| Archivo | Para qué sirve |
|---|---|
| `E03_efectos.wav` / `.mp3` | Los 106 efectos solos, sin rellenos (300,000 s). |
| `E03_hoja_de_efectos.csv` | Las 106 entradas, una por fila: segundo exacto, toma, categoría, efecto, acción en pantalla y descripción usada para generarlo. |
| `biblioteca/` | Los 55 sonidos sueltos, ya recortados y nivelados. El prefijo indica la categoría: `F_`, `M_` o `T_`. |
| `rellenos_muestras/` | Los rellenos del español, sueltos, para escucharlos o reutilizarlos. |

## Efectos de sonido: qué se pidió y qué se entregó

| Categoría | Pedido | Entregado |
|---|---|---|
| Foley de movimiento y textura | 45 a 65 | **59** entradas (24 sonidos distintos) |
| Acentos de expresión (*mickey mousing*) | 25 a 35 | **33** entradas (23 sonidos distintos) |
| Transiciones y refuerzos visuales | 12 a 20 | **14** entradas (8 sonidos distintos) |

Algunos sonidos se repiten, siempre en acciones del mismo tipo: gotas de sudor, salpicaduras, picotazos o pasos. Cada repetición está en su propio segundo.

**Algunos ejemplos**
- **Foley:** el mordisco del ají (C01); los tragos de agua de la taza azul (C06); las gotas que caen sobre la lengua (C24); los picotazos y saltitos del pájaro (C31–C32).
- **Acentos:** la llamarada cómica tras el mordisco (C01); el «¡ding!» de la idea de Pipo y el rugido del dragón chiquito (C04); la chispa que viaja por el nervio y las alarmas que se encienden (C18); el imán de la caseína (C27); el apagado de los botones (C28).
- **Transiciones:** el corte al abrir el ají y el zoom al interior (C09–C10); las cortinillas del canal; los cambios de lámina (L1–L3).

Cada efecto está en el segundo exacto de su acción. Ese segundo se midió con el análisis de movimiento fotograma a fotograma del video.

## Rellenos en los silencios entre frases

Para mantener la atención mientras el narrador no habla, los silencios entre frases que quedaban vacíos llevan un sonido pequeño. **Los 106 efectos no se movieron**: la pista de efectos es idéntica a la original fuera de los rellenos.

- **Hechos aquí, sin ElevenLabs.** Se sintetizaron con código, sin gastar créditos.
- **Según la escena.**
  - Gotitas y burbujas en las escenas de agua y leche.
  - Campanita o tic-tac cuando Pipo y Plop piensan o descubren algo.
  - Blips en el viaje por los nervios y las alarmas.
  - Punteos en las escenas del pájaro.
  - Campanita en las láminas y cortinillas.
  - Marimba en el resto.
- **Afinados entre sí.** Todos usan la escala pentatónica de do, así que no desentonan entre ellos.
- **Más suaves que los efectos.** Van a -27 dBFS, frente a -20/-22 de los efectos.
- **Solo en el hueco libre.**
  - Empiezan 0,10 s después de la frase y acaban 0,08 s antes de la siguiente.
  - Dejan 0,05 s de margen alrededor de cada efecto original.
  - En un silencio largo puede sonar un segundo relleno, más corto y más suave.
- **Uno por idioma.** Cada idioma hace sus pausas en segundos distintos, así que cada uno tiene sus propios rellenos.

| Idioma | Rellenos | Silencios con relleno | Sobre la voz | Sobre los efectos |
|---|---|---|---|---|
| ES | 55 | 36 | ninguno | ninguno |
| EN | 60 | 37 | ninguno | ninguno |
| FR | 67 | 37 | ninguno | ninguno |
| PT | 55 | 37 | ninguno | ninguno |
| HI | 46 | 35 | ninguno | ninguno |

## Cómo se sincronizó la voz

Es el mismo método del Ep. 4:

- **Una frase por toma**, anclada al segundo exacto de su toma, para que el error no se acumule.
- **Ventanas de tiempo.**
  - Clips: la voz va de 0,3 s a 7,6 s de cada toma.
  - Láminas: igual, con su propia duración.
  - Cortinillas: de 0,2 s al final de la cortinilla.
  - Ninguna frase pisa a la siguiente.
- **Ajuste fino.** Si una frase se pasaba de su ventana, la aceleré un máximo de 5,5 %, sin cambiar el tono; a ese porcentaje no se nota. Los textos se escribieron midiendo la velocidad real de la voz en cada idioma, para que quepan sin forzarlos.
- **Verificación.** Transcribí los 5 idiomas completos con ElevenLabs Scribe y los comparé frase por frase con el guion: **39/39 en los 5 idiomas**.
  - En francés regrabé dos frases (C11 y C33) para que se entendieran sin ambigüedad.
  - En hindi, la voz omitió la palabra «दोहराएँ» («repasemos») al inicio de la lámina L2. La frase queda completa sin ella, así que el guion recoge lo que se oye.
- **Nivel.** Todas las pistas de voz y todas las mezclas quedan a -16 LUFS, con picos de -1,5 dBTP, el estándar para video en línea.

Los detalles están en `INFORME_SINCRONIZACION.txt` (tiempos de cada frase y de cada efecto) y en `guion_5_idiomas.txt`.
