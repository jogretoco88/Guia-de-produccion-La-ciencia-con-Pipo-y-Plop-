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
