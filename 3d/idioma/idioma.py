"""El idioma de Pipo y Plop en la sincronía de labios.

El vocabulario es el tuyo: va en vocabulario.json (palabras, frases y en qué momento del
formato se dicen). Esta herramienta no inventa palabras: convierte lo que dicen Pipo y
Plop en claves de boca y revisa que ninguna palabra choque con algo malsonante o con
habla infantil (pis, caca...) en los idiomas del canal.

Cada sonido cae en una de las 9 bocas de reemplazo, con la nomenclatura de Rhubarb Lip
Sync (X, A-H), y el resultado sale "a dos" (cada boca dura al menos 2 fotogramas a
24 fps, como en stop-motion). La ortografía se lee como en español.

Uso en terminal:
    python idioma.py "Pipo, Plop"                 hoja de exposición estimada (sin audio)
    python idioma.py "Pipo, Plop" --inicio 2.5    empezando en el segundo 2,5
    python idioma.py --rhubarb linea.tsv          convierte la salida de Rhubarb
    python idioma.py --revisar "palabra"          revisa una palabra
    python idioma.py --vocabulario                revisa y muestra todo vocabulario.json
"""
import argparse
import json
import os
import re
import sys
import unicodedata

FPS = 24
PASO = 2              # animación a dos
ANTICIPO = 1          # la boca se adelanta 1 fotograma al sonido (práctica habitual)

BOCAS = {
    "X": "reposo: boca cerrada en sonrisa",
    "A": "labios cerrados apretados: m, b, p",
    "B": "entreabierta, dientes juntos: t, d, k, g, s, n, h",
    "C": "abierta media: e, i",
    "D": "muy abierta: a",
    "E": "redonda: o",
    "F": "fruncida: u, w",
    "G": "labio inferior recogido: f",
    "H": "lengua arriba: l",
}

# Sonido -> boca. La ortografía es la del español; «h» es una aspirada suave (como en «hop»).
FONEMA_BOCA = {
    "p": "A", "b": "A", "m": "A",
    "f": "G", "v": "G",
    "l": "H",
    "t": "B", "d": "B", "n": "B", "s": "B", "z": "B", "k": "B", "g": "B", "h": "B",
    "ch": "B", "y": "B", "r": "B", "j": "B", "ñ": "B", "x": "B", "q": "B", "c": "B",
    "a": "D", "e": "C", "i": "C", "o": "E", "u": "F", "w": "F",
}
VOCALES = set("aeiou")

# ------------------------------------------------------------------ vocabulario
VOCABULARIO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocabulario.json")


def cargar_vocabulario(ruta=VOCABULARIO):
    """Lee el vocabulario del idioma de Pipo y Plop (vocabulario.json)."""
    if not os.path.exists(ruta):
        return {"palabras": {}, "frases": {}}
    with open(ruta, encoding="utf-8") as fh:
        datos = json.load(fh)
    datos.setdefault("palabras", {})
    datos.setdefault("frases", {})
    return datos


# ------------------------------------------------------------------ revisión de palabras
# Sonidos que chocan con palabrotas o con habla infantil (pis, caca, partes del cuerpo) en
# los idiomas del canal. Se comparan sobre una forma fonética simplificada. La lista no es
# completa: toda palabra nueva la revisa además un hablante nativo de cada idioma.
PROHIBIDAS = {
    "es": ["caca", "kaka", "kulo", "puta", "puto", "poya", "pija", "pito", "teta", "pedo", "pipi",
           "konsha", "chocho", "mierda", "paja", "berga", "pinga", "kojon", "pene", "popo"],
    "en": ["poo", "pee", "wee", "fart", "but", "bub", "dik", "kok", "tit", "as", "ars", "pis",
           "shit", "fak", "krap", "nob", "wili", "seks", "kil", "dai", "dam"],
    "fr": ["prut", "sisi", "kiki", "bit", "kon", "kul", "merd", "nisho", "fufun", "puten", "salop",
           "shie", "sob", "teb", "kuy", "nik"],
    "pt": ["koko", "shishi", "pum", "peido", "bunda", "rola", "pinto", "piroka", "buseta", "pora",
           "merda", "karalo", "foda", "ku", "pika", "shota", "kusao"],
    "hi": ["tati", "susu", "chut", "lun", "gand", "ben", "chod", "randi", "kuta", "kamina", "sala",
           "harami", "ulu", "luli", "nunu", "papu", "gada"],
}
# Excepciones revisadas a mano: palabras que la revisión marca pero que suenan distinto.
# Añade aquí las tuyas después de confirmarlas con hablantes nativos.
EXCEPCIONES = {}


def fonetica(palabra):
    """Forma fonética simplificada para comparar (k por c/q, s por z, b por v, sin tildes)."""
    p = unicodedata.normalize("NFD", palabra.lower())
    p = "".join(c for c in p if unicodedata.category(c) != "Mn")
    p = re.sub(r"[^a-zñ]", "", p)
    p = p.replace("ch", "§")                # proteger «ch» antes de convertir la c
    for a, b in (("qu", "k"), ("c", "k"), ("z", "s"), ("v", "b"), ("x", "sh"), ("ñ", "ny"),
                 ("ll", "y"), ("ph", "f"), ("kh", "k"), ("oo", "u"), ("ee", "i")):
        p = p.replace(a, b)
    p = re.sub(r"(.)\1+", r"\1", p)        # alargamientos: zuuum -> zum
    return p.replace("§", "ch")


def revisar(palabra):
    """Devuelve la lista de choques posibles (idioma, palabra) de una palabra nueva."""
    base = palabra.lower().strip("¡!¿?.,… ")
    if base in EXCEPCIONES or base in cargar_vocabulario().get("excepciones", {}):
        return []
    choques = []
    for trozo in re.split(r"[-\s]+", base):
        f = fonetica(trozo)
        if not f:
            continue
        for idioma, lista in PROHIBIDAS.items():
            for mala in lista:
                corta = len(mala) <= 3
                if (corta and (f == mala or f.startswith(mala) and len(f) <= len(mala) + 1)) or \
                   (not corta and mala in f):
                    choques.append((idioma, mala, trozo))
    return choques


# ------------------------------------------------------------------ texto -> bocas
def _fonemas(palabra):
    """Lista de (fonema, es_vocal, alargado) a partir de la ortografía."""
    w = unicodedata.normalize("NFD", palabra.lower().replace("ñ", "\u0001"))
    w = "".join(c for c in w if unicodedata.category(c) != "Mn").replace("\u0001", "ñ")
    out = []
    i = 0
    while i < len(w):
        c = w[i]
        if w.startswith("ch", i) or w.startswith("ll", i):
            out.append(["ch", False, 0]); i += 2; continue
        if w.startswith("qu", i):
            out.append(["k", False, 0]); i += 2; continue
        if c == "c":
            out.append(["k", False, 0]); i += 1; continue
        if c in VOCALES:
            n = 1
            while i + n < len(w) and w[i + n] == c:
                n += 1
            out.append([c, True, n - 1]); i += n; continue
        if c in FONEMA_BOCA:
            n = 1
            while i + n < len(w) and w[i + n] == c:
                n += 1
            out.append([c, False, n - 1]); i += n; continue
        i += 1
    return out


def linea_a_eventos(texto, inicio=0.0, ritmo=1.0):
    """Estimación de tiempos sin audio, para la animática: [(segundo, boca), ...].
    Vocal 0,16 s (+0,12 s por letra repetida), consonante 0,06 s, pausa en «...» y «,»."""
    t = inicio
    ev = [(t - 0.1, "X")] if inicio >= 0.1 else []      # reposo justo antes de hablar
    for trozo in re.findall(r"[\wñáéíóúü]+|\.\.\.|…|[,;]|[-\s]", texto.lower()):
        if trozo in ("...", "…", ",", ";"):
            ev.append((t, "X"))
            t += 0.3 * ritmo
            continue
        if trozo in ("-", " "):
            t += 0.04 * ritmo
            continue
        for f, vocal, extra in _fonemas(trozo):
            boca = FONEMA_BOCA.get(f, "B")
            ev.append((t, boca))
            if vocal:
                t += (0.16 + 0.12 * extra) * ritmo
            elif f in ("m", "s", "f", "r", "z") and extra:      # mmm, fsss, brrr
                t += (0.08 + 0.1 * extra) * ritmo
            else:
                t += 0.06 * ritmo
    ev.append((t, "X"))
    return ev


def rhubarb_a_eventos(ruta_tsv, inicio=0.0):
    """Lee la salida de Rhubarb Lip Sync (-f tsv): «segundo<TAB>boca» por línea."""
    ev = []
    with open(ruta_tsv, encoding="utf-8") as fh:
        for linea in fh:
            partes = linea.strip().split("\t")
            if len(partes) == 2 and partes[1] in BOCAS:
                ev.append((inicio + float(partes[0]), partes[1]))
    return ev


def a_fotogramas(eventos, fps=FPS, paso=PASO, anticipo=ANTICIPO):
    """Eventos en segundos -> [(fotograma, boca)] a dos.

    Cada boca ocupa al menos una pose (2 fotogramas). Si un sonido es más corto que una
    pose, se corre a la siguiente; si eso retrasa la línea más de una pose, se sacrifican
    las consonantes que menos se ven (B, H, G) y nunca el cierre de labios (A) ni las
    vocales, que es lo que el ojo usa para leer los labios. La boca se adelanta `anticipo`
    fotogramas al sonido."""
    sacrificables = {"B", "H", "G"}
    poses = []
    ultima = -1
    for t, boca in sorted(eventos, key=lambda e: e[0]):
        ideal = max(0, round((t * fps - anticipo) / paso))
        s = max(ideal, ultima + 1)
        if poses and poses[-1][1] == boca:
            continue
        if s > ideal + 1 and boca in sacrificables:
            continue
        if poses and poses[-1][0] == s:          # no debería ocurrir, por seguridad
            continue
        poses.append((s, boca))
        ultima = s
    if not poses or poses[-1][1] != "X":
        poses.append(((ultima + 1) if poses else 0, "X"))
    return [(1 + s * paso, b) for s, b in poses]


def hoja(fotogramas, fps=FPS):
    filas = ["fotograma  segundo  boca  forma"]
    for f, b in fotogramas:
        filas.append(f"{f:>9}  {(f - 1) / fps:>7.2f}  {b:>4}  {BOCAS[b]}")
    return "\n".join(filas)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("linea", nargs="?", help="línea en el idioma de Pipo y Plop")
    ap.add_argument("--inicio", type=float, default=0.0, help="segundo en que empieza la línea")
    ap.add_argument("--ritmo", type=float, default=1.0, help=">1 más lento, <1 más rápido")
    ap.add_argument("--rhubarb", help="archivo .tsv de Rhubarb Lip Sync")
    ap.add_argument("--json", action="store_true", help="salida en JSON")
    ap.add_argument("--revisar", help="revisa una palabra contra la lista de choques")
    ap.add_argument("--vocabulario", action="store_true", help="revisa y muestra vocabulario.json")
    a = ap.parse_args()

    if a.revisar:
        ch = revisar(a.revisar)
        print("sin choques conocidos (pásala igual por un hablante nativo de cada idioma)" if not ch
              else "\n".join(f"posible choque en {i}: «{m}» (en «{t}»)" for i, m, t in ch))
        return
    if a.vocabulario:
        v = cargar_vocabulario()
        if not v["palabras"] and not v["frases"]:
            print("vocabulario.json está vacío: añade las palabras y frases de Pipo y Plop.")
            return
        for titulo, tabla in (("PALABRAS", v["palabras"]), ("FRASES", v["frases"])):
            print(f"\n{titulo}")
            for clave, valor in tabla.items():
                texto = clave if titulo == "PALABRAS" else valor
                bocas = "".join(b for _, b in a_fotogramas(linea_a_eventos(texto)))
                aviso = "; ".join(f"{i}: «{m}»" for i, m, _ in revisar(texto))
                print(f"  {clave:<16} {str(valor)[:40]:<40} bocas: {bocas}" + (f"   ¡revisar! {aviso}" if aviso else ""))
        return
    if a.rhubarb:
        ev = rhubarb_a_eventos(a.rhubarb, a.inicio)
    elif a.linea:
        ev = linea_a_eventos(a.linea, a.inicio, a.ritmo)
    else:
        ap.print_help()
        return
    fr = a_fotogramas(ev)
    print(json.dumps(fr) if a.json else hoja(fr))


if __name__ == "__main__":
    sys.exit(main())
