"""Prueba de rendimiento para tu PC: cuánto tarda un fotograma del laboratorio y cuánto
tardaría un episodio entero de 5:00.

En tu PC (Blender 5.2 LTS, desde una terminal en la carpeta 3d/blender):
    blender -b -P benchmark.py
    blender -b -P benchmark.py -- --ancho 3840 --alto 2160      (4K)

Mide el mismo plano en EEVEE y en Cycles (OptiX en tu RTX 5060 Ti). Un episodio de 5:00
animado a dos tiene unas 3.600 poses distintas (300 s x 12 poses por segundo).
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402

import escena_demo  # noqa: E402
import stop_motion  # noqa: E402

POSES_EPISODIO = 300 * 12


def medir(motor, calidad, ancho, alto, gpu):
    sc = bpy.context.scene
    stop_motion.configurar_render(sc, motor=motor, calidad=calidad, ancho=ancho, alto=alto, gpu=gpu)
    sc.render.filepath = os.path.join(bpy.app.tempdir, f"bench_{motor}.png")
    bpy.ops.render.render(write_still=True)          # el primero compila sombreadores: no cuenta
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    return time.time() - t0


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--ancho", type=int, default=1920)
    p.add_argument("--alto", type=int, default=1080)
    p.add_argument("--cpu", action="store_true")
    a = p.parse_args(argv)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    escena_demo.montar_escena()
    filas = []
    for motor, calidad in (("BLENDER_EEVEE", "final"), ("CYCLES", "prueba"), ("CYCLES", "final")):
        try:
            s = medir(motor, calidad, a.ancho, a.alto, not a.cpu)
        except Exception as e:  # EEVEE necesita GPU con pantalla; en servidores puede fallar
            filas.append(f"{motor:<14} {calidad:<7} no disponible ({e})")
            continue
        horas = s * POSES_EPISODIO / 3600
        filas.append(f"{motor:<14} {calidad:<7} {s:7.1f} s por fotograma  ->  {horas:6.1f} h por episodio de 5:00")
    print("\nRENDIMIENTO", f"{a.ancho}x{a.alto}", "(GPU)" if not a.cpu else "(CPU)")
    print("\n".join(filas))


if __name__ == "__main__":
    main()
