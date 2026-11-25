"""Monta en Blender la escena de layout de un episodio, directamente desde el archivo matriz.

Lee 3d/matriz/episodios.json (lo genera `node 3d/matriz/exportar.mjs`) y crea:
  - el laboratorio y a Pipo y Plop (el protagonista al centro, el otro a un lado);
  - los objetos del episodio como maquetas de plastilina a su tamaño real;
  - una cámara por toma según su código (W general, M medio, C primer plano, X macro,
    T cenital, I acercamiento lento, este último animado a dos);
  - un marcador por toma en su segundo exacto (las 39 tomas suman 5:00), atado a su
    cámara: al reproducir, Blender cambia de cámara solo, como en una animática;
  - las notas de cada toma en la cámara (qué se ve, la acción y la voz del narrador).

En tu PC (Blender 5.2 LTS, desde 3d/blender):
    blender -b -P episodio.py -- --ep 1 --guardar C:/pipo_plop/ep01_layout.blend
    blender -b -P episodio.py -- --ep 1 --audio C:/pipo_plop/E01_ES_mezcla.wav --guardar ...
Después se abre el .blend y se anima toma a toma sobre la narración.

Mientras se construyen las zonas del laboratorio (cocina, cuerpo, casa...), todo se monta
en la zona central.
"""
import argparse
import json
import math
import os
import sys

_aqui = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _aqui)

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

import arcilla  # noqa: E402
import laboratorio  # noqa: E402
import labios  # noqa: E402
import personajes  # noqa: E402
import stop_motion  # noqa: E402

MATRIZ = os.path.join(os.path.dirname(_aqui), "matriz", "episodios.json")
FPS = 24
# Altura de cada tamaño del archivo matriz (junto al títere de unos 30 cm).
TAM = {"t": 0.02, "s": 0.06, "m": 0.12, "l": 0.2, "x": 0.3, "g": 0.62}
# Cámaras: distancia al objetivo (m), objetivo (mm) y diafragma.
CAMARA = {
    "W": dict(dist=1.15, focal=35, f=4.0),
    "M": dict(dist=0.8, focal=50, f=4.0),
    "C": dict(dist=0.62, focal=85, f=2.8),
    "X": dict(dist=0.34, focal=100, f=4.0),
    "T": dict(dist=0.95, focal=40, f=5.6),
    "I": dict(dist=0.85, focal=50, f=3.5, fin=0.5),
}
COLORES_OBJ = ["#F2C14E", "#E8505B", "#5BC0EB", "#9BC53D", "#B48EE0", "#FF8C42", "#F4EAD3"]


def cargar(n, ruta=MATRIZ):
    with open(ruta, encoding="utf-8") as fh:
        datos = json.load(fh)
    for e in datos["episodios"]:
        if e["n"] == n:
            return e
    raise SystemExit(f"No está el episodio {n} en {ruta}")


def _maqueta_objeto(letra, o, i, col, lado=-1):
    """Maqueta de un objeto del episodio: un bloque de plastilina a su altura real, en el
    lado contrario al acompañante para no taparlo."""
    alto = TAM.get(o["tam"], 0.12)
    gigante = o["tam"] == "g"
    xs = [0.2, 0.38, 0.56, 0.29, 0.47, 0.65]
    pos = Vector((lado * xs[i % len(xs)] * (1.3 if gigante else 1.0), 0.26 if gigante else -0.24, 0))
    mat = arcilla.plastilina(f"objeto {letra}", COLORES_OBJ[i % len(COLORES_OBJ)], boil=0.2)
    ob = laboratorio.esfera(f"{letra} · {o['es']}", pos + Vector((0, 0, alto / 2)),
                            (alto * 0.45, alto * 0.4, alto / 2), mat)
    ob["tag"] = o["tag"]
    ob["descripcion_en"] = o.get("en", "")
    ob["altura_m"] = alto
    ob["centro"] = tuple(pos + Vector((0, 0, alto / 2)))
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    col.objects.link(ob)
    return ob


def _objetivo(t, refs, protagonista):
    """Qué mira la cámara de cada toma: el personaje, el primer objeto o la lámina."""
    if t["tipo"] in ("T", "F"):
        return (refs["Pipo"].location + refs["Plop"].location) / 2 + Vector((0, 0, 0.17)), "los dos"
    if t["tipo"] == "S":
        return Vector(refs["lamina"]["centro"]), "lámina"
    if t["tipo"] == "R":
        quien = "Pipo" if t["banco"].startswith("P") else "Plop"
        return refs[quien].location + Vector((0, 0, 0.22)), quien
    if t["tipo"] == "W":
        return refs[protagonista].location + Vector((0, 0, 0.2)), protagonista
    ing = t.get("ing", "")
    alto = {"W": 0.17, "M": 0.2, "C": 0.24, "T": 0.0, "I": 0.21, "X": 0.24}.get(t["cam"], 0.2)
    if "P" in ing:
        return refs["Pipo"].location + Vector((0, 0, alto)), "Pipo"
    if "L" in ing:
        return refs["Plop"].location + Vector((0, 0, alto)), "Plop"
    for letra in ing:
        if letra in refs:
            ob = refs[letra]
            return Vector(ob["centro"]), ob.name
    return refs[protagonista].location + Vector((0, 0, 0.2)), protagonista


def _camara(nombre, tipo, objetivo, inicio_f, dur_f, frente=None):
    """frente: hacia dónde mira el personaje encuadrado; la cámara se coloca a medio camino
    entre ese frente y el frente del set, para verle la cara."""
    cfg = CAMARA.get(tipo, CAMARA["M"])
    cam = bpy.data.objects.new(nombre, bpy.data.cameras.new(nombre))
    bpy.context.scene.collection.objects.link(cam)
    eje = Vector((0, -1, 0))
    if frente is not None:
        eje = (frente.normalized() * 0.6 + eje * 0.4).normalized()
    if tipo == "T":
        cam.location = objetivo + Vector((0, -0.02, cfg["dist"]))
    else:
        cam.location = objetivo + eje * cfg["dist"] + Vector((0, 0, 0.02))
    cam.rotation_euler = (objetivo - cam.location).to_track_quat("-Z", "Y").to_euler()
    stop_motion.camara_macro(cam, focal=cfg["focal"], f_stop=cfg["f"], distancia=(objetivo - cam.location).length)
    if tipo == "I":                       # acercamiento lento, a dos (como un riel de stop-motion)
        cam.keyframe_insert("location", frame=inicio_f)
        cam.data.dof.keyframe_insert("focus_distance", frame=inicio_f)
        cam.location = objetivo + eje * cfg["fin"] + Vector((0, 0, 0.02))
        cam.data.dof.focus_distance = (objetivo - cam.location).length
        cam.keyframe_insert("location", frame=inicio_f + dur_f - 1)
        cam.data.dof.keyframe_insert("focus_distance", frame=inicio_f + dur_f - 1)
        stop_motion.a_dos(cam)
        stop_motion.a_dos(cam.data)
    return cam


def montar(n, audio=None):
    e = cargar(n)
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = 1, round(e["duracion"] * FPS)
    sc["episodio"] = e["n"]
    sc["titulo"] = e["titulo"]
    sc["zona"] = e["zona"]

    laboratorio.crear_laboratorio()
    laboratorio.iluminar()
    estrella = e["protagonista"]
    otro_x = 0.3 if estrella == "Pipo" else -0.3
    pipo = personajes.crear_pipo(ubicacion=(0.0, -0.06, 0) if estrella == "Pipo" else (otro_x, -0.08, 0),
                                 giro_z=0.0 if estrella == "Pipo" else 0.5)
    plop = personajes.crear_plop(ubicacion=(0.0, -0.06, 0) if estrella == "Plop" else (otro_x, -0.08, 0),
                                 giro_z=0.0 if estrella == "Plop" else -0.5)
    refs = {"Pipo": pipo, "Plop": plop}

    col = bpy.data.collections.new(f"Ep{n:02d} objetos")
    sc.collection.children.link(col)
    lado_objetos = -1 if estrella == "Pipo" else 1           # el acompañante está al otro lado
    for i, (letra, o) in enumerate(e["objetos"].items()):
        refs[letra] = _maqueta_objeto(letra, o, i, col, lado_objetos)
    lamina = laboratorio.caja("lámina (panel de plastilina)", (-0.22, 0.535, 0.46), (0.26, 0.012, 0.17),
                              arcilla.plastilina("panel de lámina", "#F4EAD3", huellas=0.5, boil=0.1), bisel=0.006)
    lamina["centro"] = (-0.22, 0.535, 0.46)
    refs["lamina"] = lamina

    sc.timeline_markers.clear()
    for i, t in enumerate(e["tomas"], 1):
        inicio_f = 1 + round(t["inicio"] * FPS)
        dur_f = round(t["duracion"] * FPS)
        tipo_cam = t.get("cam") or ("W" if t["tipo"] in ("T", "F") else "M")
        objetivo, quien = _objetivo(t, refs, estrella)
        etiqueta = {"C": f"clip {t.get('clip')}", "R": f"banco {t.get('banco')}", "W": "despedida",
                    "S": "lámina", "T": "cortinilla", "F": "tarjeta final"}[t["tipo"]]
        frente = None
        if quien in ("Pipo", "Plop"):
            frente = refs[quien].matrix_world.to_3x3() @ Vector((0, -1, 0))
        cam = _camara(f"T{i:02d} {etiqueta} · {tipo_cam}", tipo_cam, objetivo, inicio_f, dur_f, frente)
        cam["pantalla"] = t.get("pantalla", "")
        cam["accion_en"] = t.get("accion", "")
        cam["voz"] = t.get("voz", "")
        cam["mira_a"] = quien
        m = sc.timeline_markers.new(f"{i:02d} {etiqueta} {tipo_cam} · {t.get('pantalla', '')[:38]}", frame=inicio_f)
        m.camera = cam
        if i == 1:
            sc.camera = cam
    if audio:
        labios.poner_audio(audio, 0.0)
    return e


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--ep", type=int, required=True)
    p.add_argument("--audio", default="", help="mezcla del episodio (por ejemplo E01_ES_mezcla.wav)")
    p.add_argument("--guardar", default="", help="ruta del .blend de layout")
    a = p.parse_args(argv)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    e = montar(a.ep, a.audio or None)
    stop_motion.configurar_render(bpy.context.scene, motor="BLENDER_EEVEE", calidad="boceto", ancho=1280, alto=720)
    print(f"Ep. {e['n']} · {e['titulo']} · zona {e['zona']} · {len(e['tomas'])} tomas · "
          f"{bpy.context.scene.frame_end} fotogramas")
    if a.guardar:
        bpy.ops.wm.save_as_mainfile(filepath=a.guardar)
        print("guardado:", a.guardar)


if __name__ == "__main__":
    main()
