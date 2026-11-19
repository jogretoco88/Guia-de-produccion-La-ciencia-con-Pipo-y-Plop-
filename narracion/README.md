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
- **Documentación:** los tiempos están en `INFORME_SINCRONIZACION.txt` y las instrucciones de uso en `LEEME.md`.
