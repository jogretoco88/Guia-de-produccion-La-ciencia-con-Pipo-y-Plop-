# Ep. 3 · ¿Por qué pica el ají si no está caliente? — Kit de audio en 5 idiomas

- **Voz:** José Gregorio Torres (voz clonada), con **ElevenLabs Eleven v4**.
- **Efectos:** **ElevenLabs Sound Effects v3**.
- **Video:** `E03_aji_mudo.mp4` (300,000 s, 24 fps). El video no se tocó.

## Cómo usarlo (lo más simple)

1. Abre el video mudo en tu editor.
2. Pon `XX/E03_XX_mezcla.wav` en el segundo **0:00**. Ya trae la voz y los 106 efectos, sincronizados.
   Los efectos suenan **en los silencios entre frase y frase**, nunca encima de la voz.
3. Exporta. Haz una versión por idioma.

Si prefieres ajustar tú el balance, usa dos pistas por separado, ambas en el segundo 0:00:
- `XX/E03_XX_narracion.wav`, la voz sola;
- `XX/E03_XX_efectos.wav`, los efectos solos de ese idioma.

Cada idioma tiene su propia pista de efectos, porque cada idioma hace sus pausas en segundos distintos.

Para YouTube puedes subir `E03_XX_subtitulos.srt` como subtítulos de ese idioma. Los tiempos son los reales de la voz.

## Qué hay en cada carpeta

### Idiomas (ES, EN, FR, PT, HI)

| Archivo | Para qué sirve |
|---|---|
| `E03_XX_mezcla.wav` / `.mp3` | Voz y efectos mezclados. Dura exactamente lo mismo que el video. Está a -16 LUFS. |
| `E03_XX_narracion.wav` / `.mp3` | Solo la voz, 48 kHz / 24 bit, mono, a -16 LUFS. |
| `E03_XX_efectos.wav` / `.mp3` | Solo los efectos de ese idioma, colocados en sus silencios (300,000 s). |
| `E03_XX_hoja_de_efectos.csv` | Las 106 entradas de ese idioma: segundo en que suena, segundo de la acción en pantalla, distancia entre ambos, silencio que ocupa, duración, categoría y acción. |
| `E03_XX_subtitulos.srt` | Subtítulos con el tiempo real de cada frase. No se queman en el video. |
| `E03_XX_posiciones.csv` | Toma, archivo, segundo de inicio y de fin de cada frase, y aceleración aplicada. |
| `frases/E03_XX_<toma>.wav` | Cada frase suelta, ya ajustada. Colócala en el segundo `inicio_s` del CSV. |
| `E03_XX_vista_previa_360p.mp4` | El video con la mezcla, para revisar rápido. |

### efectos (común a los 5 idiomas)

| Archivo | Para qué sirve |
|---|---|
| `biblioteca/` | Los 55 sonidos sueltos, completos, ya recortados desde su ataque y nivelados. El prefijo indica la categoría: `F_`, `M_` o `T_`. |

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

## Dónde suena cada efecto

Los efectos van **en los silencios entre frase y frase**, para mantener la atención mientras el narrador no habla. No se generó ningún sonido ni narración nuevos: son los mismos 106 efectos, solo cambiaron de segundo.

- **Silencios.** Se midieron sobre la voz real de cada idioma. Cada efecto empieza al menos 0,08 s después de que termina una frase y acaba 0,06 s antes de que empiece la siguiente.
- **Siempre en su toma.** Un efecto solo puede sonar dentro de su propia toma: desde 0,15 s antes del corte que la abre hasta 0,35 s después del que la cierra. Así nunca cae sobre otra escena.
- **Lo más cerca posible de su acción.** Si la acción ocurre mientras habla el narrador, el efecto suena nada más terminar la frase, o justo antes de la siguiente si queda más cerca. Dentro de un silencio, los efectos conservan su orden.
- **Recortes.** Cuando un silencio es más corto que el sonido, el sonido se recorta con un fundido. Si en un silencio no caben todos, alguno pasa al otro silencio de su toma.
- **Resultado** (detalle en `INFORME_SINCRONIZACION.txt` y en cada `E03_XX_hoja_de_efectos.csv`):

| Idioma | Silencios usados | Distancia media a la acción | Distancia máxima | Efectos sobre la voz |
|---|---|---|---|---|
| ES | 40 de 40 | 3,23 s | 7,42 s | ninguno |
| EN | 40 de 40 | 3,17 s | 7,2 s | ninguno |
| FR | 40 de 40 | 2,88 s | 7,04 s | ninguno |
| PT | 40 de 40 | 3,27 s | 7,56 s | ninguno |
| HI | 40 de 40 | 3,97 s | 7,62 s | ninguno |

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
