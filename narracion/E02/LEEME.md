# Ep. 2 · ¿Por qué el jabón quita la grasa y el agua no? — Kit de audio en 5 idiomas

- **Voz:** José Gregorio Torres (voz clonada), con **ElevenLabs Eleven v4**.
- **Efectos:** no se generó ninguno nuevo. Se reutilizaron dos bibliotecas:
  - la de **ElevenLabs Sound Effects v3** creada para el Ep. 3;
  - los efectos que ya se habían hecho para este Ep. 2.
- **Video:** `E02_jabon_mudo.mp4` (300,000 s, 24 fps), **sin ningún texto en pantalla**.
  - Se quitaron los rótulos de las 5 láminas: título, L1, L2, L3 y cierre.
  - Los 34 clips animados no llevaban texto y son idénticos fotograma a fotograma.
  - La duración y los tiempos de cada toma no cambiaron, así que el audio sigue sincronizado.

## Cómo usarlo (lo más simple)

1. Abre el video mudo en tu editor.
2. Pon `XX/E02_XX_mezcla.wav` en el segundo **0:00**. Ya trae:
   - la voz;
   - los 102 efectos, cada uno en el segundo exacto de su acción;
   - los rellenos de los silencios entre frases.
3. Exporta. Haz una versión por idioma.

Si prefieres ajustar tú el balance, usa dos pistas por separado, ambas en el segundo 0:00:
- `XX/E02_XX_narracion.wav`, la voz sola;
- `XX/E02_XX_efectos.wav`, los efectos de ese idioma: los 102 originales más los rellenos de sus silencios.

Si no quieres los rellenos, usa `efectos/E02_efectos.wav`: son solo los 102 efectos, iguales para los 5 idiomas.

Para YouTube puedes subir `E02_XX_subtitulos.srt` como subtítulos de ese idioma. Los tiempos son los reales de la voz.

## Qué hay en cada carpeta

### Idiomas (ES, EN, FR, PT, HI)

| Archivo | Para qué sirve |
|---|---|
| `E02_XX_mezcla.wav` / `.mp3` | Voz y efectos mezclados. Dura exactamente lo mismo que el video. Está a -16 LUFS. |
| `E02_XX_narracion.wav` / `.mp3` | Solo la voz, 48 kHz / 24 bit, mono, a -16 LUFS. |
| `E02_XX_efectos.wav` / `.mp3` | Los 102 efectos, en su sitio original, más los rellenos de ese idioma (300,000 s). |
| `E02_XX_rellenos.csv` | Cada relleno de ese idioma: segundo, toma, entre qué frases suena, tipo de sonido y duración. |
| `E02_XX_subtitulos.srt` | Subtítulos con el tiempo real de cada frase. No se queman en el video. |
| `E02_XX_posiciones.csv` | Toma, archivo, segundo de inicio y de fin de cada frase, y aceleración aplicada. |
| `frases/E02_XX_<toma>.wav` | Cada frase suelta, ya ajustada. Colócala en el segundo `inicio_s` del CSV. |
| `E02_XX_vista_previa_360p.mp4` | El video con la mezcla, para revisar rápido. |

### efectos (común a los 5 idiomas)

| Archivo | Para qué sirve |
|---|---|
| `E02_efectos.wav` / `.mp3` | Los 102 efectos solos, sin rellenos (300,000 s). |
| `E02_hoja_de_efectos.csv` | Las 102 entradas, una por fila: segundo exacto, toma, categoría, efecto, acción en pantalla, de qué biblioteca sale y su descripción. |
| `biblioteca/` | Los 57 sonidos sueltos, ya recortados y nivelados. El prefijo indica la categoría: `F_`, `M_` o `T_`. Los que empiezan por `h_` son los propios del Ep. 2. |
| `rellenos_muestras/` | Los rellenos del español, sueltos, para escucharlos o reutilizarlos. |

## Efectos de sonido: qué se pidió y qué se entregó

| Categoría | Pedido | Entregado | De ElevenLabs (Ep. 3) | Propios del Ep. 2 |
|---|---|---|---|---|
| Foley de movimiento y textura | 45 a 65 | **59** entradas (27 sonidos distintos) | 35 | 24 |
| Acentos de expresión (*mickey mousing*) | 25 a 35 | **27** entradas (19 sonidos distintos) | 18 | 9 |
| Transiciones y refuerzos visuales | 12 a 20 | **16** entradas (11 sonidos distintos) | 13 | 3 |
| **Total** | | **102** entradas (57 sonidos) | **66** (30 sonidos) | **36** (27 sonidos) |

**Créditos de ElevenLabs gastados en efectos: 0.** Todos los efectos se reutilizaron de bibliotecas que ya existían.

Algunos sonidos se repiten, siempre en acciones del mismo tipo: gotas, colas que se clavan o brazos que se mueven. Cada repetición está en su propio segundo.

**Algunos ejemplos**
- **Foley:**
  - las gotas que caen y resbalan sobre la grasa de Plop (C01);
  - el jabón que entra rodando y choca con la grasa (C02);
  - el frotado y la espuma en la panza (C06 y C26);
  - las colas que se clavan una a una (C13 y C18);
  - las piezas que encajan alrededor de la grasa (C19);
  - el agua que se lleva la micela rodando (C24 y C27);
  - el abrigo del microbio que se desarma (C32).
- **Acentos:**
  - el «¡ups!» (C01);
  - el silbato de la idea loca de Pipo (C04);
  - el silbato que baja cuando la grasa ni se mueve con la flor (C05);
  - el imán cuando la cabeza se pega al agua (C12);
  - el «¡ta-da!» de la panza limpia (C28);
  - el microbio que se desinfla (C32);
  - una llamarada pequeña como guiño al próximo episodio del ají (C34).
- **Transiciones:**
  - el zoom al mundo diminuto (C09–C10);
  - el brillo cuando aparecen millones de jabones (C17);
  - las cortinillas del canal, con el mismo logo sonoro del Ep. 3;
  - los cambios de lámina (L1–L3), con el carillón de repaso en L2.

Cada efecto está en el segundo exacto de su acción. Ese segundo se midió con el análisis de movimiento fotograma a fotograma del video y con hojas de contacto a 2 fotogramas por segundo.

## Rellenos en los silencios entre frases

Para mantener la atención mientras el narrador no habla, los silencios entre frases que quedaban vacíos llevan un sonido pequeño. **Los 102 efectos no se movieron**: la pista de efectos es idéntica bit a bit a la original fuera de los rellenos.

- **Hechos aquí, sin ElevenLabs.** Se sintetizaron con código, sin gastar créditos.
- **Según la escena.**
  - Gotitas y burbujas en las escenas de agua.
  - Campanita o tic-tac cuando Pipo y Plop piensan o descubren algo.
  - Blips en las escenas de moléculas y micelas.
  - Punteos en los momentos de Pipo y Plop.
  - Campanita en las láminas y cortinillas.
- **Afinados entre sí.** Todos usan la escala pentatónica de do, así que no desentonan entre ellos.
- **Más suaves que los efectos.** Van a -27 dBFS, frente a -20/-22 de los efectos.
- **Solo en el hueco libre.**
  - Empiezan 0,10 s después de la frase y acaban 0,08 s antes de la siguiente.
  - Dejan 0,05 s de margen alrededor de cada efecto original.
- **Uno por idioma.** Cada idioma hace sus pausas en segundos distintos, así que cada uno tiene sus propios rellenos.

| Idioma | Rellenos | Silencios con relleno | Sobre la voz | Sobre los efectos |
|---|---|---|---|---|
| ES | 63 | 38 | ninguno | ninguno |
| EN | 66 | 38 | ninguno | ninguno |
| FR | 73 | 38 | ninguno | ninguno |
| PT | 62 | 38 | ninguno | ninguno |
| HI | 58 | 37 | ninguno | ninguno |

## Cómo se sincronizó la voz

Es el mismo método de los episodios 3 y 4:

- **Una frase por toma**, anclada al segundo exacto de su toma, para que el error no se acumule.
- **Ventanas de tiempo.**
  - Clips: la voz va de 0,3 s a 7,6 s de cada toma.
  - Láminas: igual, con su propia duración.
  - Cortinillas: de 0,2 s al final de la cortinilla.
  - Ninguna frase pisa a la siguiente.
- **Ajuste fino.** Si una frase se pasaba de su ventana, la aceleré sin cambiar el tono:
  - ES: L1 ×1,032;
  - PT: L1 ×1,06 y C21 ×1,003;
  - HI: C01 ×1,001 y C05 ×1,012;
  - EN y FR: ninguna.
- **Correcciones del guion para que cuadre con la imagen.**
  - C34: en pantalla se despide Plop, así que la próxima pregunta la deja Plop.
  - C27: «el agua ya no resbala… ¡se lleva la grasa!».
- **Verificación.** Transcribí los 5 idiomas completos con ElevenLabs Scribe y los comparé frase por frase con el guion.
  - ES, EN, PT y HI: **39/39**.
  - FR: en la primera toma, la voz decía «Pipou» en lugar de «Pipo». Regrabé CANAL_INICIO, C04, C14, C21 y C29, y en las 5 tomas nuevas se oye «Pipo».
  - **C03 en francés todavía dice «Pipou»**: su regrabación no se hizo.
  - En L3 (FR), «Frotte tes mains» suena igual que «Frottez main»: es cosa de la transcripción, no de la voz.
- **Nivel.** Todas las pistas de voz y todas las mezclas quedan a -16 LUFS, con picos de -1,5 dBTP, el estándar para video en línea.

Los detalles están en `INFORME_SINCRONIZACION.txt` (tiempos de cada frase y de cada efecto), en `guion_5_idiomas.txt` y en `qa/`.
