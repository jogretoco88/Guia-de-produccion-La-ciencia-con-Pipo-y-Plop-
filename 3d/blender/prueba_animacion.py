"""Prueba de animación: Pipo dice una línea de prueba con bocas de reemplazo, boiling y
parpadeo de luz, todo a dos (12 poses por segundo). Renderiza solo las poses (fotogramas
impares) y el montaje repite cada una dos veces, como en stop-motion.

    blender -b -P prueba_animacion.py -- --carpeta C:/render/anim
    ffmpeg -framerate 12 -i C:/render/anim/pose_%03d.png -vf "fps=24" -c:v libx264 -pix_fmt yuv420p pipo_habla.mp4
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

import arcilla  # noqa: E402
import labios  # noqa: E402
import personajes  # noqa: E402
import stop_motion  # noqa: E402


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--carpeta", default=os.path.join(bpy.app.tempdir, "anim"))
    p.add_argument("--linea", default="Pipo, Plop... ¡Pipo!", help="línea en el idioma de Pipo y Plop")
    p.add_argument("--ancho", type=int, default=1280)
    p.add_argument("--alto", type=int, default=720)
    p.add_argument("--muestras", type=int, default=48)
    p.add_argument("--cpu", action="store_true")
    a = p.parse_args(argv)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    pipo = personajes.crear_pipo(giro_z=0.12)
    claves = labios.animar(pipo, texto=a.linea, inicio=0.25)
    fin = claves[-1][0] + 6
    sc.frame_start, sc.frame_end = 1, fin
    # Un gesto: Pipo se inclina un poco hacia delante a mitad de la línea (también a dos).
    pipo.rotation_euler = (0, 0, 0.12)
    pipo.keyframe_insert("rotation_euler", frame=1)
    pipo.rotation_euler = (0.06, 0, 0.0)
    pipo.keyframe_insert("rotation_euler", frame=claves[len(claves) // 2][0])
    pipo.rotation_euler = (0.0, 0, 0.08)
    pipo.keyframe_insert("rotation_euler", frame=fin)
    stop_motion.a_dos(pipo)

    bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0))
    bpy.context.active_object.data.materials.append(
        arcilla.plastilina("suelo del estudio", "#BFDDF2", huellas=0.3, boil=0.0, escala_huella=2.0))
    bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0.7, 0), rotation=(math.pi / 2, 0, 0))
    bpy.context.active_object.data.materials.append(
        arcilla.plastilina("fondo del canal", "#8CC6EA", huellas=0.0, boil=0.0, bultos=0.2, poros=0.0))

    def luz(nombre, loc, mira, energia, tam):
        d = bpy.data.lights.new(nombre, "AREA")
        d.energy, d.size, d.shape = energia, tam, "DISK"
        ob = bpy.data.objects.new(nombre, d)
        sc.collection.objects.link(ob)
        ob.location = loc
        ob.rotation_euler = (Vector(mira) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()

    luz("clave", (-0.35, -0.6, 0.75), (0, 0, 0.2), 16, 0.5)
    luz("borde", (0.7, 0.15, 0.4), (0, 0, 0.22), 14, 0.25)
    luz("relleno", (0.3, -0.9, 0.25), (0, 0, 0.2), 3, 0.8)
    mundo = bpy.data.worlds.new("estudio")
    sc.world = mundo
    mundo.node_tree.nodes["Background"].inputs[1].default_value = 0.05
    stop_motion.parpadeo_luces()

    cam = bpy.data.objects.new("cámara", bpy.data.cameras.new("cámara"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.location = (0.02, -0.72, 0.232)
    cam.rotation_euler = (Vector((0, 0, 0.216)) - cam.location).to_track_quat("-Z", "Y").to_euler()
    stop_motion.camara_macro(cam, focal=60, f_stop=4.0, distancia=0.66)
    stop_motion.configurar_render(sc, calidad="prueba", ancho=a.ancho, alto=a.alto, gpu=not a.cpu)
    sc.cycles.samples = a.muestras

    os.makedirs(a.carpeta, exist_ok=True)
    for i, f in enumerate(range(1, fin + 1, 2)):          # solo las poses: 1, 3, 5...
        sc.frame_set(f)
        sc.render.filepath = os.path.join(a.carpeta, f"pose_{i:03d}.png")
        bpy.ops.render.render(write_still=True)
    print("poses:", (fin + 1) // 2, "en", a.carpeta)


if __name__ == "__main__":
    main()
