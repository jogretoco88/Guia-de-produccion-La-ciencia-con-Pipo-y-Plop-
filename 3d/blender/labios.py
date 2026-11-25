"""Sincronía de labios en Blender con las bocas de reemplazo de personajes.py.

Dos caminos:
  1. Animática (sin audio todavía): tiempos estimados desde el texto en pipoplopés.
         labios.animar(pipo, texto="¡Din-din!", inicio=2.0)
  2. Con la voz grabada: Rhubarb Lip Sync (gratis, github.com/DanielSWolf/rhubarb-lip-sync)
     con el reconocedor fonético, que sirve para cualquier idioma, también el inventado:
         rhubarb -r phonetic -f tsv -o pipo_l01.tsv pipo_l01.wav
         labios.animar(pipo, tsv="pipo_l01.tsv", inicio=2.0, audio="pipo_l01.wav")
     Las bocas de Rhubarb (X, A-H) son las mismas 9 de nuestros personajes.

Todo queda "a dos" (cada boca dura al menos 2 fotogramas) y con la boca un fotograma
por delante del sonido, como se hace en stop-motion.
"""
import os
import sys

_aqui = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _aqui)
sys.path.insert(0, os.path.join(os.path.dirname(_aqui), "idioma"))

import bpy  # noqa: E402

import personajes  # noqa: E402
import pipoplopes  # noqa: E402


def animar(raiz, texto=None, tsv=None, inicio=0.0, audio=None, ritmo=1.0, canal=1):
    """Pone las claves de boca de una línea. Devuelve [(fotograma, boca), ...]."""
    sc = bpy.context.scene
    fps = sc.render.fps / sc.render.fps_base
    if tsv:
        eventos = pipoplopes.rhubarb_a_eventos(tsv, inicio)
    elif texto:
        eventos = pipoplopes.linea_a_eventos(texto, inicio, ritmo)
    else:
        raise ValueError("Hace falta texto o tsv")
    claves = pipoplopes.a_fotogramas(eventos, fps=round(fps))
    for f, boca in claves:
        personajes.poner_boca(raiz, boca, f)
    if audio:
        poner_audio(audio, inicio, canal)
    return claves


def poner_audio(ruta, inicio=0.0, canal=1):
    """Coloca el audio de la línea en la línea de tiempo (para verlo y oírlo en el visor)."""
    sc = bpy.context.scene
    if not sc.sequence_editor:
        sc.sequence_editor_create()
    ed = sc.sequence_editor
    tiras = getattr(ed, "strips", None) or ed.sequences     # Blender 5 usa «strips»
    f = 1 + round(inicio * sc.render.fps / sc.render.fps_base)
    return tiras.new_sound(os.path.basename(ruta), ruta, canal, f)
