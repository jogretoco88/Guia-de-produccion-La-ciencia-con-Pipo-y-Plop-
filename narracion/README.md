# Narración sincronizada en 5 idiomas

Flujo usado en el Ep. 4 (voz clonada «José Gregorio Torres», ElevenLabs Eleven v4). El audio no se guarda en git: solo los guiones, las anclas, el informe y las herramientas.

## Pasos por episodio

1. **Tiempos del video.** Se toman los tiempos de cada toma del video montado (`shots.json`). Ventanas de voz:
   - clips de 8 s: de 0,3 s a 7,6 s;
   - láminas: lo mismo, con su propia duración;
   - tarjeta final: termina 0,12 s antes del fin del video.
2. **Anclas de acción.** Se mide el movimiento fotograma a fotograma y se marcan las tomas cuya frase nombra una acción puntual (un «¡hip!» o un «¡clac!»):
   - `('START', t)`: la frase arranca en el instante t;
   - `('HIC1', t)`: la palabra-ancla cae en el instante t.
3. **Guion por idioma.** Adaptado a la ventana de cada toma, no traducido literal. Velocidades medidas con esta voz en v4, en caracteres por segundo: es 12,6 · en 13,3 · fr 15,3 · pt 12,8 · hi 10,9.
4. **Generación.** Una frase por toma, 1 toma, modelo `eleven_v4`, voz `axKTBvcu9eOvYwDNgwC4`.
5. **Medición** (`herramientas/medir.py`). Se recortan los silencios y se mide la voz real. Si una frase supera su ventana en más de un 8 %, se acorta el texto y se regenera.
6. **Verificación.** Las frases de cada idioma se concatenan con 2 s de silencio y se transcriben con Scribe (palabra a palabra). `herramientas/anclas.py` hace dos cosas:
   - ubica cada palabra-ancla dentro de su frase;
   - compara el guion con lo que se oye.
7. **Montaje** (`herramientas/montar.py`):
   - coloca cada frase en su segundo o en su ancla;
   - acelera hasta un 8 % si hace falta;
   - divide C25 en dos para clavar los dos «¡hip!»;
   - normaliza a -16 LUFS y -1,5 dBTP;
   - exporta la pista WAV/MP3, el SRT, el CSV de posiciones y las frases sueltas.
8. **Informe** (`herramientas/informe.py`). Por idioma: ventanas, solapes, aceleraciones, anclas y verificación.

## Ep. 3 · ¿Por qué pica el ají si no está caliente? (voz + efectos)

Mismo flujo de voz: 39 frases × 5 idiomas, todas dentro de su ventana, aceleración máxima de 5,5 % y verificación con Scribe de 39/39 en los 5 idiomas. Este episodio no tiene anclas de acción. Además lleva **106 efectos de sonido** generados con ElevenLabs Sound Effects v3: 55 sonidos distintos, comunes a los 5 idiomas.

| Categoría | Pedido | Entregado |
|---|---|---|
| Foley de movimiento y textura (`F`) | 45–65 | 59 |
| Acentos de expresión / *mickey mousing* (`M`) | 25–35 | 33 |
| Transiciones y refuerzos visuales (`T`) | 12–20 | 14 |

Archivos en `E03/`:
- **Guion:** `guion_e03.py` → `guion_5_idiomas.json`.
- **Efectos:** `efectos_e03.py` → `efectos.json`, con la biblioteca de sonidos, la descripción de cada uno y cada entrada con su segundo, toma y acción en pantalla. La hoja legible es `E03_hoja_de_efectos.csv`.
- **Rellenos en los silencios:** los silencios entre frases que la pista de efectos deja vacíos llevan un sonido pequeño sintetizado con código, sin ElevenLabs ni créditos: marimba, gotitas, burbujas, campanita, blips, tic-tac o punteo, según la escena. Los 106 efectos siguen exactamente donde estaban. Hay una lista por idioma en `rellenos_por_idioma/`.
- **Montaje e informe:** `montar_e03.py` e `informe_e03.py` son las versiones de este episodio. Los tiempos están en `INFORME_SINCRONIZACION.txt`, la verificación de cada idioma en `qa/` y las instrucciones de uso en `LEEME.md`.

Herramientas nuevas:
- **`herramientas/efectos_montar.py`:**
  - recorta cada sonido desde su ataque y lo nivela por categoría;
  - arma la pista de efectos, limitada a -3 dBFS;
  - mezcla cada idioma con compresión por cadena lateral: mientras hay voz, los efectos bajan al menos 4 dB y quedan como mínimo 9 dB por debajo de ella;
  - normaliza la mezcla a -16 LUFS y -1,5 dBTP.
- **`herramientas/efectos_relleno.py`:** sintetiza los rellenos con numpy, en la escala pentatónica de do y a -27 dBFS.
  - los coloca solo donde no suenan ni la voz ni los efectos;
  - arma una pista de efectos y una mezcla por idioma, a -16 LUFS y -1,5 dBTP;
  - comprueba que la pista original quede idéntica fuera de los rellenos.
- **`herramientas/verificar.py`:** compara la transcripción de Scribe con el guion, frase por frase. Para el hindi admite préstamos escritos en alfabeto latino.

## Ep. 2 · ¿Por qué el jabón quita la grasa y el agua no? (voz + efectos reutilizados)

Mismo flujo de voz que el Ep. 3: 39 frases × 5 idiomas, todas dentro de su ventana y sin anclas de acción.

- **Aceleraciones:** la mayor es de 6 % (PT L1).
- **Verificación con Scribe:**
  - ES, EN, PT y HI: 39/39.
  - FR: la voz decía «Pipou». Se regrabaron 5 frases, que ya dicen «Pipo». C03 sigue diciendo «Pipou» porque su regrabación no se hizo (ver `qa/fr_qa.txt`).

**Efectos: 102 entradas sin generar ninguno nuevo** (0 créditos de ElevenLabs):
- 66 salen de la biblioteca de ElevenLabs Sound Effects v3 del Ep. 3;
- 36 son los efectos propios que ya existían para este Ep. 2.

Todos están colocados en el segundo exacto de su acción en pantalla, medido con el análisis de movimiento y hojas de contacto a 2 fps.

| Categoría | Pedido | Entregado |
|---|---|---|
| Foley de movimiento y textura (`F`) | 45–65 | 59 |
| Acentos de expresión / *mickey mousing* (`M`) | 25–35 | 27 |
| Transiciones y refuerzos visuales (`T`) | 12–20 | 16 |

Archivos en `E02/`:
- **Guion:** `guion_e02.py` → `guion_5_idiomas.json`. Incluye dos correcciones para que cuadre con la imagen, en C27 y C34.
- **Efectos:** `efectos_e02.py` → `efectos.json`. Cada sonido indica su biblioteca de origen (`fuente`) y su archivo. La hoja legible es `E02_hoja_de_efectos.csv`.
- **Rellenos en los silencios:** sintetizados con código, igual que en el Ep. 3, con temas propios de este episodio: agua, idea, molécula, personaje y lámina. Hay una lista por idioma en `rellenos_por_idioma/`.
- **Scripts de este episodio:**
  - `montar_e02.py` y `verificar_e02.py`;
  - `efectos_montar_e02.py`, que lee cada sonido de la ruta indicada en `efectos.json` y por eso admite varias bibliotecas;
  - `efectos_relleno_e02.py`;
  - `informe_e02.py`;
  - `qa_fr_extra.py`.
- **Video sin texto:** `video_sin_texto.py` rehace el video mudo sin ningún rótulo. Las 5 láminas se renderizan desde sus fondos limpios y los clips no cambian, así que la duración y los tiempos siguen iguales.
- **Documentación:** los tiempos están en `INFORME_SINCRONIZACION.txt` y las instrucciones de uso en `LEEME.md`.

## Ep. 1 · ¿Por qué explotan las palomitas de maíz? (voz + efectos reutilizados)

Mismo flujo de voz: 39 frases × 5 idiomas, todas dentro de su ventana.

- **Ancla de acción:** C26 arranca con «¡Pum!» en 212,65 s, justo antes del estallido en pantalla (212,75 s), en los 5 idiomas (`('START', 2.68)` en `guion_e01.py`).
- **Aceleraciones:** la mayor es de 7,1 % (PT L2). ES, EN y FR no tienen ninguna.
- **Verificación con Scribe:** 39/39 en los 5 idiomas, sin ningún «Pipou» en francés. `verificar_e01.py` añade equivalencias de escritura para el hindi: préstamos en alfabeto latino, «गर्मी/गरमी» y «180» en cifras.

**Efectos: 111 entradas sin generar ninguno nuevo** (0 créditos de ElevenLabs):
- 86 salen de la biblioteca de ElevenLabs Sound Effects v3 del Ep. 3;
- 25 salen de la biblioteca del Ep. 2.

Todos están colocados en el segundo exacto de su acción en pantalla:
- los dos estallidos del grano (C01 a 4,42 s y C26 a 212,75 s);
- los 8 aterrizajes de Pipo sobre el grano (C06), medidos fotograma a fotograma siguiendo su altura;
- el resto, con el análisis de movimiento y hojas de contacto a 2 fps.

| Categoría | Pedido | Entregado |
|---|---|---|
| Foley de movimiento y textura (`F`) | 45–65 | 63 |
| Acentos de expresión / *mickey mousing* (`M`) | 25–35 | 31 |
| Transiciones y refuerzos visuales (`T`) | 12–20 | 17 |

Archivos en `E01/`:
- **Guion:** `guion_e01.py` → `guion_5_idiomas.json`.
- **Efectos:** `efectos_e01.py` → `efectos.json`. La hoja legible es `E01_hoja_de_efectos.csv`.
- **Rellenos en los silencios:** sintetizados con código, con temas de este episodio: agua (gota, vapor y gelatina), idea, calor y presión, personaje y lámina. Hay una lista por idioma en `rellenos_por_idioma/`.
- **Scripts de este episodio:** `montar_e01.py`, `verificar_e01.py`, `efectos_montar_e01.py`, `efectos_relleno_e01.py` e `informe_e01.py`.
- **Documentación:** los tiempos están en `INFORME_SINCRONIZACION.txt` y las instrucciones de uso en `LEEME.md`.

## Ep. 4 · Efectos de sonido (añadidos después de la narración)

La narración del Ep. 4 no cambia. Se le añadieron **112 efectos sin generar ninguno nuevo** (0 créditos de ElevenLabs):
- 80 salen de la biblioteca de ElevenLabs Sound Effects v3 del Ep. 3;
- 32 salen de la biblioteca del Ep. 2.

Todos están colocados en el segundo exacto de su acción en pantalla:
- cada salto de hipo (C01, C02, C23, C25 y el perrito en C31), con su despegue y su aterrizaje medidos fotograma a fotograma. En C23 y C25, el «pop» del hipo coincide con el «¡hip!» de la voz;
- el tirón del diafragma de C20 («¡zas!», 0,54 s) y el cierre de las cuerdas vocales de C22 («¡clac!», 0,83 s);
- el resto, con el análisis de movimiento y hojas de contacto a 2 fps.

| Categoría | Pedido | Entregado |
|---|---|---|
| Foley de movimiento y textura (`F`) | 45–65 | 64 |
| Acentos de expresión / *mickey mousing* (`M`) | 25–35 | 33 |
| Transiciones y refuerzos visuales (`T`) | 12–20 | 15 |

Archivos nuevos en `E04/`:
- **Efectos:** `efectos_e04.py` → `efectos.json`. La hoja legible es `E04_hoja_de_efectos.csv`.
- **Rellenos en los silencios:** sintetizados con código, con temas de este episodio: aire y pulmones, idea, nervio y señales, personaje y lámina. Hay una lista por idioma en `rellenos_por_idioma/`.
- **Scripts:** `efectos_montar_e04.py`, `efectos_relleno_e04.py` e `informe_e04.py`. Usan la duración exacta del video, 299,958 s.
- **Documentación:** `INFORME_SINCRONIZACION.txt` ahora incluye los efectos y los rellenos. Las instrucciones de uso están en `LEEME.md` y la verificación de cada idioma en `qa/`.
