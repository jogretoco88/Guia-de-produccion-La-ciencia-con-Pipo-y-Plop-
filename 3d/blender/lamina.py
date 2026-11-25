"""Lámina de un personaje: de frente, en un estudio liso, con el mismo encuadre que las
láminas aprobadas del canal. Sirve para comparar el modelo 3D con la lámina y para
calibrar los colores.

    blender -b -P lamina.py -- --personaje pipo --salida C:/render/lamina_pipo.png
    blender -b -P lamina.py -- --personaje plop --salida C:/render/lamina_plop.png
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

# Fondo, tamaño y encuadre de cada lámina aprobada (tamaño en píxeles de la lámina,
# fracción del alto que ocupa el personaje y centro del encuadre).
LAMINAS = {
    "pipo": dict(fondo="#7FC1F3", ancho=1287, alto=1222, ocupa=0.7, centro_z=0.156, cam_z=0.165),
    "plop": dict(fondo="#E9DED4", ancho=1402, alto=1122, ocupa=0.8, centro_z=0.165, cam_z=0.17),
}


def montar(personaje):
    sc = bpy.context.scene
    L = LAMINAS[personaje]
    raiz = (personajes.crear_pipo if personaje == "pipo" else personajes.crear_plop)()

    # Ciclorama: suelo que sube en curva hasta la pared, del color del fondo de la lámina.
    import bmesh
    fondo = arcilla.plastilina(f"ciclorama {personaje}", L["fondo"], huellas=0.0, boil=0.0, bultos=0.15, poros=0.0)
    perfil = [(-2.0, 0.0), (0.3, 0.0)]
    r = 0.5
    perfil += [(0.3 + r * math.sin(a), r * (1 - math.cos(a))) for a in (math.pi / 2 * k / 16 for k in range(1, 17))]
    perfil += [(0.3 + r, 2.5)]
    bm = bmesh.new()
    filas = [[bm.verts.new((x, y, z)) for y, z in perfil] for x in (-3.0, 3.0)]
    for i in range(len(perfil) - 1):
        bm.faces.new((filas[0][i], filas[0][i + 1], filas[1][i + 1], filas[1][i]))
    me = bpy.data.meshes.new("ciclorama")
    bm.to_mesh(me)
    bm.free()
    for poly in me.polygons:
        poly.use_smooth = True
    ob = bpy.data.objects.new("ciclorama", me)
    sc.collection.objects.link(ob)
    me.materials.append(fondo)

    def luz(nombre, loc, mira, energia, tam):
        d = bpy.data.lights.new(nombre, "AREA")
        d.energy, d.size, d.shape = energia, tam, "DISK"
        o = bpy.data.objects.new(nombre, d)
        sc.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = (Vector(mira) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()

    # Luz de estudio de producto: caja grande arriba y al frente, relleno suave, contraluz.
    luz("clave", (-0.45, -0.9, 0.9), (0, 0, 0.17), 26, 0.9)
    luz("relleno", (0.7, -0.8, 0.3), (0, 0, 0.15), 6, 1.0)
    luz("contra", (0.25, 0.45, 0.75), (0, 0, 0.2), 10, 0.5)
    mundo = bpy.data.worlds.new("estudio")
    sc.world = mundo
    mundo.node_tree.nodes["Background"].inputs[0].default_value = arcilla.hex_a_lineal(L["fondo"])
    mundo.node_tree.nodes["Background"].inputs[1].default_value = 0.25

    # Cámara de bodegón: teleobjetivo corto, poca perspectiva, como las láminas.
    focal = 85.0
    sensor_alto = 36.0 * L["alto"] / L["ancho"]
    alto_figura = 0.34 if personaje == "plop" else 0.31
    distancia = (alto_figura / L["ocupa"]) * focal / sensor_alto
    cam = bpy.data.objects.new("cámara", bpy.data.cameras.new("cámara"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.location = (0, -distancia, L["cam_z"])
    cam.rotation_euler = (Vector((0, 0, L["centro_z"])) - cam.location).to_track_quat("-Z", "Y").to_euler()
    stop_motion.camara_macro(cam, focal=focal, f_stop=11.0, distancia=distancia)
    return raiz, L


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--personaje", default="pipo", choices=["pipo", "plop"])
    p.add_argument("--salida", default=os.path.join(bpy.app.tempdir, "lamina.png"))
    p.add_argument("--escala", type=float, default=1.0, help="tamaño respecto a la lámina (0.5 = mitad)")
    p.add_argument("--muestras", type=int, default=64)
    p.add_argument("--cpu", action="store_true")
    a = p.parse_args(argv)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    raiz, L = montar(a.personaje)
    stop_motion.configurar_render(sc, calidad="prueba", ancho=round(L["ancho"] * a.escala),
                                  alto=round(L["alto"] * a.escala), gpu=not a.cpu)
    sc.cycles.samples = a.muestras
    sc.render.filepath = a.salida
    bpy.ops.render.render(write_still=True)
    print("lámina ->", a.salida)


if __name__ == "__main__":
    main()
