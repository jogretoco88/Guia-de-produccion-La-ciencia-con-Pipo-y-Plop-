# Ep. 4 · ¿Qué es el hipo? — Kit de audio en 5 idiomas

- **Voz:** José Gregorio Torres (voz clonada), con **ElevenLabs Eleven v4**. Es la misma narración que ya se había entregado, sin cambios.
- **Efectos:** no se generó ninguno nuevo. Se reutilizaron dos bibliotecas:
  - la de **ElevenLabs Sound Effects v3** creada para el Ep. 3;
  - la de efectos hechos para el Ep. 2.
- **Video:** `E04_hipo_mudo.mp4` (299,958 s, 24 fps), **sin ningún texto en pantalla**.

## Cómo usarlo (lo más simple)

1. Abre el video mudo en tu editor.
2. Pon `XX/E04_XX_mezcla.wav` en el segundo **0:00**. Ya trae:
   - la voz;
   - los 112 efectos, cada uno en el segundo exacto de su acción;
   - los rellenos de los silencios entre frases.
3. Exporta. Haz una versión por idioma.

Si prefieres ajustar tú el balance, usa dos pistas por separado, ambas en el segundo 0:00:
- `XX/E04_XX_narracion.wav`, la voz sola;
- `XX/E04_XX_efectos.wav`, los efectos de ese idioma: los 112 originales más los rellenos de sus silencios.

Si no quieres los rellenos, usa `efectos/E04_efectos.wav`: son solo los 112 efectos, iguales para los 5 idiomas.

Para YouTube puedes subir `E04_XX_subtitulos.srt` como subtítulos de ese idioma. Los tiempos son los reales de la voz.

## Qué hay en cada carpeta

### Idiomas (ES, EN, FR, PT, HI)

| Archivo | Para qué sirve |
|---|---|
| `E04_XX_mezcla.wav` / `.mp3` | Voz y efectos mezclados. Dura exactamente lo mismo que el video (299,958 s). Está a -16 LUFS. |
| `E04_XX_narracion.wav` / `.mp3` | Solo la voz, 48 kHz / 24 bit, mono, a -16 LUFS. |
| `E04_XX_efectos.wav` / `.mp3` | Los 112 efectos, en su sitio, más los rellenos de ese idioma. |
| `E04_XX_rellenos.csv` | Cada relleno de ese idioma: segundo, toma, entre qué frases suena, tipo de sonido y duración. |
| `E04_XX_subtitulos.srt` | Subtítulos con el tiempo real de cada frase. No se queman en el video. |
| `E04_XX_posiciones.csv` | Toma, archivo, segundo de inicio y de fin de cada frase, y aceleración aplicada. |
| `frases/E04_XX_<toma>.wav` | Cada frase suelta, ya ajustada. Colócala en el segundo `inicio_s` del CSV. |
| `E04_XX_vista_previa_360p.mp4` | El video con la mezcla, para revisar rápido. |

### efectos (común a los 5 idiomas)

| Archivo | Para qué sirve |
|---|---|
| `E04_efectos.wav` / `.mp3` | Los 112 efectos solos, sin rellenos. |
| `E04_hoja_de_efectos.csv` | Las 112 entradas, una por fila: segundo exacto, toma, categoría, efecto, acción en pantalla, de qué biblioteca sale y su descripción. |
| `biblioteca/` | Los 48 sonidos sueltos, ya recortados y nivelados. El prefijo indica la categoría: `F_`, `M_` o `T_`. Los que llevan `h_` salen de la biblioteca del Ep. 2. |
| `rellenos_muestras/` | Los rellenos del español, sueltos, para escucharlos o reutilizarlos. |

## Efectos de sonido: qué se pidió y qué se entregó

| Categoría | Pedido | Entregado | De ElevenLabs (Ep. 3) | Biblioteca del Ep. 2 |
|---|---|---|---|---|
| Foley de movimiento y textura | 45 a 65 | **64** entradas (17 sonidos distintos) | 44 | 20 |
| Acentos de expresión (*mickey mousing*) | 25 a 35 | **33** entradas (23 sonidos distintos) | 23 | 10 |
| Transiciones y refuerzos visuales | 12 a 20 | **15** entradas (8 sonidos distintos) | 13 | 2 |
| **Total** | | **112** entradas (48 sonidos) | **80** (30 sonidos) | **32** (18 sonidos) |

**Créditos de ElevenLabs gastados en efectos: 0.** Todos los efectos se reutilizaron de bibliotecas que ya existían.

Algunos sonidos se repiten, siempre en acciones del mismo tipo: los saltos del hipo, los aterrizajes o el diafragma que sube y baja. Cada repetición está en su propio segundo.

**Los hipos, al fotograma**

Cada hipo se midió fotograma a fotograma: el despegue lleva un «pop» o un saltito, y el aterrizaje un golpe suave.

| Toma | Quién | Saltos (segundo dentro de la toma) |
|---|---|---|
| C01 | Plop tumba la torre de bloques | despega a 0,88 · aterriza a 1,21 · los bloques caen a 2,04 |
| C02 | Plop, 4 hipos seguidos | 1,04 · 3,04 · 4,96 · 7,04 (aterrizajes 0,25–0,33 s después) |
| C23 | Plop, 4 hipos | 1,04 · **3,00** · 5,00 · 7,04. El «pop» fuerte va en 3,00, el mismo instante en que la voz dice «¡hip!». |
| C25 | Plop, 3 hipos y se sienta | **2,08** · **4,17** · 6,08. Los dos primeros coinciden con los dos «¡hip!» de la voz. |
| C31 | el perrito | 0,88 · 2,96, y luego le aletean las orejas (4,75 y 6,71) |

**Otros momentos clave**
- **C20 «¡Zas!» (0,54 s):** el diafragma da el tirón hacia abajo. Suenan un *boing* y un golpe, y luego el aire que entra de golpe.
- **C22 «¡Clac!» (0,83 s):** las cuerdas vocales se cierran como una puerta. Suenan una cerradura que encaja y un portazo suave.
- **C27:** las bolitas de dióxido de carbono caen entre los pulmones y se amontonan. Cuando encaja la última, suena una campanita.

**Otros ejemplos**
- **Foley:**
  - la torre de bloques que se cae (C01);
  - los cachetes inflados y la gota de sudor al aguantar la respiración (C06);
  - el diafragma que sube y baja (C11, C13 y C29);
  - el estómago que se infla y empuja el nervio (C18);
  - el aire que sube por la garganta y las cuerdas vocales que aletean (C21).
- **Acentos:**
  - la campanita de la idea loca y el *boing* de la ranita (C04);
  - el reloj de «piénsalo» (C09);
  - la chispa eléctrica que viaja por el nervio (C15);
  - la alarma de «¡aprieta ya!» (C19);
  - el «¡ta-da!» y los aplausos de «¡se fue!» (C30);
  - un destello de hielo como guiño al próximo episodio (C34).
- **Transiciones:**
  - el zoom que entra al pecho (C09–C10);
  - los primeros planos de las cuerdas vocales y los pulmones (C22 y C27);
  - las cortinillas del canal, con el mismo logo sonoro de los otros episodios;
  - los cambios de lámina (L1–L3).

Cada efecto está en el segundo exacto de su acción. Ese segundo se midió con el análisis de movimiento fotograma a fotograma del video y con hojas de contacto a 2 fotogramas por segundo.

## Rellenos en los silencios entre frases

Para mantener la atención mientras el narrador no habla, los silencios entre frases que quedaban vacíos llevan un sonido pequeño. **Los 112 efectos no se movieron**: la pista de efectos es idéntica a la original fuera de los rellenos.

- **Hechos aquí, sin ElevenLabs.** Se sintetizaron con código, sin gastar créditos.
- **Según la escena.**
  - Gotitas y burbujas en las escenas del aire, los pulmones y el diafragma.
  - Campanita o tic-tac cuando Pipo y Plop piensan o descubren algo.
  - Blips en las escenas del nervio y sus señales.
  - Punteos en los momentos de Pipo, Plop, el perrito y el bebé.
  - Campanita en las láminas y cortinillas.
- **Afinados entre sí.** Todos usan la escala pentatónica de do, así que no desentonan entre ellos.
- **Más suaves que los efectos.** Van a -27 dBFS, frente a -20/-22 de los efectos.
- **Solo en el hueco libre.**
  - Empiezan 0,10 s después de la frase y acaban 0,08 s antes de la siguiente.
  - Dejan 0,05 s de margen alrededor de cada efecto original.
- **Uno por idioma.** Cada idioma hace sus pausas en segundos distintos, así que cada uno tiene sus propios rellenos.

| Idioma | Rellenos | Silencios con relleno | Sobre la voz | Sobre los efectos |
|---|---|---|---|---|
| ES | 61 | 38 | ninguno | ninguno |
| EN | 66 | 38 | ninguno | ninguno |
| FR | 70 | 39 | ninguno | ninguno |
| PT | 61 | 37 | ninguno | ninguno |
| HI | 58 | 37 | ninguno | ninguno |

Cada mezcla queda a -16 LUFS, con picos de -1,5 dBTP. Mientras hay voz, los efectos bajan al menos 4 dB y quedan como mínimo 9 dB por debajo de ella; en las pausas suenan completos.

## Cómo se sincronizó la voz

La narración es la misma que ya se entregó para este episodio:

- **Una frase por toma**, anclada al segundo exacto de su toma, para que el error no se acumule.
- **Ventanas de tiempo.** En los clips, la voz va de 0,3 s a 7,6 s; en las láminas, igual, con su propia duración. Ninguna frase pisa a la siguiente.
- **Anclas de acción.** Las onomatopeyas caen en el instante exacto de la acción en pantalla:
  - C01 «¡hip!», a 1,05 s;
  - C02 «¡hip!», a 1,18 s;
  - C20 «¡zas!», a 0,5 s;
  - C22 «¡clac!», a 0,8 s;
  - C23 «¡hip!», a 2,95 s;
  - C25, los dos «¡hip!», a 2,05 s y 4,10 s.
- **Ajuste fino.** Si una frase se pasaba de su ventana, la aceleré sin cambiar el tono (máximo 7,1 %, HI C30).
- **Verificación.** Transcribí los 5 idiomas completos con ElevenLabs Scribe y los comparé frase por frase con el guion.
- **Nivel.** Todas las pistas de voz quedan a -16 LUFS, con picos de -1,5 dBTP.

Los detalles están en `INFORME_SINCRONIZACION.txt` (tiempos de cada frase, de cada efecto y de cada relleno), en `guion_5_idiomas.txt` y en `qa/`.
