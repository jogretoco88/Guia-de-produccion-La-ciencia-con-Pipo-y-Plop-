"""Hoja de bocas: renderiza las 9 bocas de reemplazo de Pipo (o de Plop), una imagen por boca.

    blender -b -P hoja_bocas.py -- --personaje pipo --carpeta C:/render/bocas
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

import arcilla  # noqa: E402
import personajes  # noqa: E402
import stop_motion  # noqa: E402


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--personaje", default="pipo", choices=["pipo", "plop"])
    p.add_argument("--carpeta", default=os.path.join(bpy.app.tempdir, "bocas"))
    p.add_argument("--ancho", type=int, default=960)
    p.add_argument("--alto", type=int, default=540)
    p.add_argument("--muestras", type=int, default=64)
    p.add_argument("--cpu", action="store_true")
    a = p.parse_args(argv)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    crear = personajes.crear_pipo if a.personaje == "pipo" else personajes.crear_plop
    raiz = crear()
    zc = 0.235 if a.personaje == "pipo" else 0.243

    bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0.6, 0), rotation=(math.pi / 2, 0, 0))
    bpy.context.active_object.data.materials.append(
        arcilla.plastilina("fondo del canal", "#8CC6EA", huellas=0.0, boil=0.0, bultos=0.2, poros=0.0))

    def luz(nombre, loc, mira, energia, tam):
        d = bpy.data.lights.new(nombre, "AREA")
        d.energy, d.size, d.shape = energia, tam, "DISK"
        ob = bpy.data.objects.new(nombre, d)
        sc.collection.objects.link(ob)
        ob.location = loc
        ob.rotation_euler = (Vector(mira) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()

    luz("clave", (-0.3, -0.6, 0.65), (0, 0, zc), 14, 0.5)
    luz("borde", (0.6, 0.1, 0.35), (0, 0, zc), 12, 0.2)
    luz("relleno", (0.25, -0.8, 0.2), (0, 0, zc), 2.5, 0.8)
    mundo = bpy.data.worlds.new("estudio")
    sc.world = mundo
    mundo.node_tree.nodes["Background"].inputs[1].default_value = 0.05

    cam = bpy.data.objects.new("cámara", bpy.data.cameras.new("cámara"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.location = (0, -0.58, zc + 0.005)
    cam.rotation_euler = (math.radians(90), 0, 0)
    stop_motion.camara_macro(cam, focal=85, f_stop=8.0, distancia=0.5)
    stop_motion.configurar_render(sc, calidad="prueba", ancho=a.ancho, alto=a.alto, gpu=not a.cpu)
    sc.cycles.samples = a.muestras

    os.makedirs(a.carpeta, exist_ok=True)
    for clave in personajes.BOCAS:
        personajes.poner_boca(raiz, clave)
        sc.render.filepath = os.path.join(a.carpeta, f"{a.personaje}_boca_{clave}.png")
        bpy.ops.render.render(write_still=True)
        print("boca", clave, "->", sc.render.filepath)


if __name__ == "__main__":
    main()
