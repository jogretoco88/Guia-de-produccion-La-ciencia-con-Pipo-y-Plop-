"""Plano de presentación: Pipo y Plop juntos en su laboratorio.

Muestra en un solo fotograma lo que el video con IA no permitía: los dos personajes en la
misma toma, un set con fondo y profundidad, bocas que hablan (Pipo dice algo con la boca
D, Plop se sorprende con la E) y escala real (los frascos, el microscopio y las palomitas
miden lo que deben).

En tu PC (Blender 5.2 LTS):
    blender -b -P escena_demo.py -- --calidad final --salida C:/render/lab.png
    blender -b -P escena_demo.py -- --calidad prueba --guardar C:/render/lab.blend
o ábrelo en la pestaña Scripting y pulsa Ejecutar (usa los valores por defecto).
"""
import argparse
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

import laboratorio  # noqa: E402
import personajes  # noqa: E402
import stop_motion  # noqa: E402


def _args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--calidad", default="prueba", choices=["boceto", "prueba", "final"])
    p.add_argument("--ancho", type=int, default=1920)
    p.add_argument("--alto", type=int, default=1080)
    p.add_argument("--muestras", type=int, default=0, help="0 = las de la calidad elegida")
    p.add_argument("--salida", default="")
    p.add_argument("--guardar", default="", help="ruta .blend para guardar la escena")
    p.add_argument("--cpu", action="store_true", help="no usar la tarjeta gráfica")
    p.add_argument("--plano", default="general", choices=["general", "primer_plano"])
    return p.parse_args(argv)


def luz(nombre, loc, mira, energia, tam, color, forma="DISK"):
    d = bpy.data.lights.new(nombre, "AREA")
    d.energy, d.size, d.color, d.shape = energia, tam, color, forma
    ob = bpy.data.objects.new(nombre, d)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    ob.rotation_euler = (Vector(mira) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return ob


def montar_escena(plano="general"):
    sc = bpy.context.scene
    laboratorio.crear_laboratorio()
    pipo = personajes.crear_pipo(ubicacion=(-0.15, -0.06, 0), giro_z=0.34, brazo_izq=2.25,
                                 boca="D" if plano == "general" else "C")
    plop = personajes.crear_plop(ubicacion=(0.17, -0.01, 0), giro_z=-0.42, boca="E")

    laboratorio.iluminar()

    cam = bpy.data.objects.new("cámara", bpy.data.cameras.new("cámara"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.location = (0.0, -1.2, 0.235)
    cam.rotation_euler = (Vector((0.0, 0.2, 0.3)) - cam.location).to_track_quat("-Z", "Y").to_euler()
    foco = bpy.data.objects.new("foco", None)
    sc.collection.objects.link(foco)
    if plano == "general":
        foco.location = (0.0, -0.04, 0.22)
        stop_motion.camara_macro(cam, focal=35, f_stop=2.2, enfoque=foco)
    else:
        # Primer plano de Pipo: la cámara mira su cara de frente; el laboratorio queda desenfocado.
        foco.parent = pipo
        foco.location = (0.0, -0.085, 0.256)
        bpy.context.view_layer.update()
        cara = foco.matrix_world.translation.copy()
        frente = (pipo.matrix_world.to_3x3() @ Vector((0, -1, 0))).normalized()
        cam.location = cara + frente * 0.56 + Vector((0.03, 0, 0.012))
        cam.rotation_euler = (cara - cam.location).to_track_quat("-Z", "Y").to_euler()
        stop_motion.camara_macro(cam, focal=70, f_stop=2.8, enfoque=foco)
    stop_motion.parpadeo_luces()
    return pipo, plop


def main():
    a = _args()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    t0 = time.time()
    montar_escena(a.plano)
    print(f"escena montada en {time.time() - t0:.1f} s")
    sc = bpy.context.scene
    stop_motion.configurar_render(sc, calidad=a.calidad, ancho=a.ancho, alto=a.alto, gpu=not a.cpu)
    if a.muestras:
        sc.cycles.samples = a.muestras
    if a.guardar:
        bpy.ops.wm.save_as_mainfile(filepath=a.guardar)
    if a.salida:
        sc.render.filepath = a.salida
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        print(f"render en {time.time() - t0:.1f} s -> {a.salida}")


if __name__ == "__main__":
    main()
