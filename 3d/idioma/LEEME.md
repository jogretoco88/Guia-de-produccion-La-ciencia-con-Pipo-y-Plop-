# El idioma de Pipo y Plop en la producción 3D

El idioma es el tuyo. Esta carpeta solo lo conecta con la animación: convierte lo que dicen Pipo y Plop en claves de boca y revisa que ninguna palabra choque con algo malsonante en los idiomas del canal.

## Por qué conviene que hablen su propio idioma

- **No se doblan nunca.** Sus voces van en la pista de música y efectos (M&E), igual en todas las versiones. Solo cambia de idioma el narrador, que no sale en pantalla.
- **La sincronía de labios se hace una vez** y sirve para el español, el inglés, el francés, el portugués, el hindi y cualquier idioma que se añada.
- **Las frases fijas del formato se convierten en marca.** Por ejemplo, la idea loca de Pipo, la pregunta de Plop, el «¡Hagamos zoom!», el reto o la despedida pueden tener siempre la misma frase en su idioma.

## Cómo cargar tu idioma

Escribe tus palabras y frases en [`vocabulario.json`](vocabulario.json):

```json
{
  "nombre": "el nombre de tu idioma",
  "palabras": { "palabra": "significado" },
  "frases": { "idea_loca": "…", "pregunta_de_plop": "…", "zoom": "…", "despedida": "…" },
  "excepciones": {}
}
```

Después:

```sh
python idioma.py --vocabulario
```

Muestra cada palabra con su secuencia de bocas y avisa si alguna choca con algo malsonante o con habla infantil (pis, caca, partes del cuerpo) en español, inglés, francés, portugués o hindi. Por ejemplo, avisa con «pum», que en portugués de Brasil es un pedo. La lista no está completa: pasa siempre las palabras por un hablante nativo de cada idioma. Las que confirmes van en `excepciones`.

## Bocas

Cada sonido cae en una de las 9 bocas de reemplazo, con la nomenclatura de Rhubarb Lip Sync. La ortografía se lee como en español.

| Sonido | Boca | Cómo se ve |
| --- | --- | --- |
| m, b, p | A | labios cerrados y apretados |
| t, d, k, c, q, g, s, z, n, ñ, h, ch, ll, y, r, j, x | B | entreabierta, dientes juntos |
| e, i | C | abierta media |
| a | D | muy abierta |
| o | E | redonda |
| u, w | F | fruncida |
| f, v | G | labio inferior recogido |
| l | H | lengua arriba |
| (silencio) | X | reposo: la sonrisa cerrada de siempre |

Hoja de las 9 bocas de Pipo: [`../pruebas/hoja_bocas_pipo.jpg`](../pruebas/hoja_bocas_pipo.jpg).

## De la línea grabada a las claves de boca

1. **Animática.** `python idioma.py "línea" --inicio 12.5` da una hoja de exposición estimada, sin audio.
2. **Grabación** de la línea con la voz de Pipo o de Plop.
3. **Rhubarb Lip Sync** (gratuito) con el reconocedor fonético, que sirve para cualquier idioma:
   `rhubarb -r phonetic -f tsv -o linea.tsv linea.wav`
4. **En Blender:** `labios.animar(pipo, tsv="linea.tsv", inicio=12.5, audio="linea.wav")`.

La herramienta aplica tres reglas de oficio:

- **Cada boca dura al menos 2 fotogramas**, como en la animación a dos del stop-motion.
- **La boca se adelanta un fotograma al sonido**, porque si va exactamente sincronizada el ojo la ve tarde.
- **Nunca se pierde un cierre de labios (m, b, p) ni una vocal.** Si no caben todas las bocas, se sacrifican las consonantes que menos se ven.
