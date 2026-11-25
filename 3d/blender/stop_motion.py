"""Aspecto de stop-motion real en Blender 5.2 LTS.

Las reglas que hacen que un render 3D se lea como plastilina fotografiada cuadro a cuadro:

  1. Animación "a dos": 24 fps de video, pero cada pose dura 2 fotogramas (12 poses por segundo).
     También la cámara, si se mueve (como un riel de control de movimiento).
  2. Sin desenfoque de movimiento: en stop-motion cada foto es de un títere quieto.
  3. Boiling: la superficie cambia un poco entre poses (lo hace el material de arcilla.py).
  4. Escala real: el set se construye en centímetros reales (Pipo mide 30 cm) y la cámara usa
     una lente macro con poca profundidad de campo, como en un estudio de miniatura.
  5. Luz de estudio con un parpadeo mínimo (±1 %), como las lámparas reales entre fotos.
  6. Bocas de reemplazo: se cambian piezas, no se deforman (ver personajes.py).
"""
import bpy


def configurar_render(escena=None, motor="CYCLES", calidad="final", ancho=1920, alto=1080, gpu=True):
    """Ajustes de render del canal.

    calidad: "boceto" (layout rápido), "prueba" o "final".
    En tu PC (RTX 5060 Ti) deja gpu=True: usa OptiX si está disponible.
    """
    s = escena or bpy.context.scene
    r = s.render
    r.engine = motor
    r.resolution_x, r.resolution_y = ancho, alto
    r.resolution_percentage = 100
    r.fps, r.fps_base = 24, 1.0
    r.use_motion_blur = False                       # regla 2
    r.film_transparent = False

    # Color: Khronos PBR Neutral respeta el tono y la saturación de cada plastilina (AgX los
    # lava hacia el pastel). Comprobado en pruebas con los colores del canal.
    s.view_settings.view_transform = "Khronos PBR Neutral"
    s.view_settings.look = "None"
    s.view_settings.exposure = 0.0

    if motor == "CYCLES":
        c = s.cycles
        muestras = {"boceto": 16, "prueba": 48, "final": 160}[calidad]
        c.samples = muestras
        c.use_adaptive_sampling = True
        c.adaptive_threshold = 0.02 if calidad != "final" else 0.01
        c.use_denoising = True
        c.denoiser = "OPENIMAGEDENOISE"
        c.max_bounces = 8
        c.diffuse_bounces = 3
        c.glossy_bounces = 3
        c.transmission_bounces = 8
        c.transparent_max_bounces = 8
        c.caustics_reflective = False
        c.caustics_refractive = False
        c.blur_glossy = 1.0
        r.use_persistent_data = True                # acelera las secuencias: no recarga la escena
        if gpu:
            activar_gpu(s)
    else:  # EEVEE: ideal para animática y para series largas
        e = s.eevee
        e.taa_render_samples = {"boceto": 16, "prueba": 64, "final": 128}[calidad]
        if hasattr(e, "use_raytracing"):
            e.use_raytracing = True
        if hasattr(e, "use_shadows"):
            e.use_shadows = True
    return s


def activar_gpu(escena=None):
    """Usa la tarjeta NVIDIA con OptiX (o CUDA). Si no hay GPU, sigue en CPU sin fallar."""
    s = escena or bpy.context.scene
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
    except KeyError:
        return "CPU"
    for tipo in ("OPTIX", "CUDA"):
        try:
            prefs.compute_device_type = tipo
            prefs.get_devices()
            gpus = [d for d in prefs.devices if d.type == tipo]
            if gpus:
                for d in prefs.devices:
                    d.use = d.type == tipo
                s.cycles.device = "GPU"
                s.cycles.denoiser = "OPTIX" if tipo == "OPTIX" else "OPENIMAGEDENOISE"
                return tipo
        except TypeError:
            continue
    s.cycles.device = "CPU"
    return "CPU"


def a_dos(obj_o_accion, paso=2):
    """Animación a dos: añade el modificador Stepped a todas las curvas de animación.

    Acepta un objeto (usa su acción) o una acción. Repetible: no duplica modificadores.
    """
    accion = obj_o_accion
    if isinstance(obj_o_accion, bpy.types.ID) and not isinstance(obj_o_accion, bpy.types.Action):
        ad = obj_o_accion.animation_data        # objeto, cámara, luz...
        accion = ad.action if ad else None
    if accion is None:
        return 0
    curvas = _curvas_de(accion)
    n = 0
    for fc in curvas:
        if any(m.type == "STEPPED" for m in fc.modifiers):
            continue
        m = fc.modifiers.new("STEPPED")
        m.frame_step = paso
        m.frame_offset = 1          # poses en 1, 3, 5...: alineadas con el boiling y las bocas
        n += 1
    return n


def _curvas_de(accion):
    """Curvas de una acción, en el sistema clásico o en el de capas (Blender 4.4+)."""
    if hasattr(accion, "fcurves") and len(accion.fcurves):
        return list(accion.fcurves)
    curvas = []
    for capa in getattr(accion, "layers", []):
        for tira in capa.strips:
            for bolsa in getattr(tira, "channelbags", []):
                curvas.extend(bolsa.fcurves)
    return curvas


def parpadeo_luces(amplitud=0.012, paso=2):
    """Variación mínima de intensidad en cada luz, cambiando cada `paso` fotogramas."""
    for ob in bpy.data.objects:
        if ob.type != "LIGHT":
            continue
        luz = ob.data
        base = luz.energy
        luz["energia_base"] = base
        fc = luz.driver_add("energy")
        d = fc.driver
        d.type = "SCRIPTED"
        semilla = (hash(ob.name) % 997) / 997.0
        # Ruido determinista por pose: sin(número de pose * constante grande) ~ aleatorio.
        d.expression = f"{base} * (1 + {amplitud} * sin(floor((frame - 1) / {paso}) * 12.9898 + {semilla * 78.233}))"


def camara_macro(cam_obj, focal=50.0, f_stop=4.0, enfoque=None, distancia=None):
    """Lente de estudio de miniatura: poca profundidad de campo a escala real."""
    cam = cam_obj.data
    cam.lens = focal
    cam.sensor_width = 36.0
    cam.dof.use_dof = True
    cam.dof.aperture_fstop = f_stop
    cam.dof.aperture_blades = 7                  # bokeh poligonal suave, de objetivo real
    if enfoque is not None:
        cam.dof.focus_object = enfoque
    elif distancia is not None:
        cam.dof.focus_distance = distancia
    cam.clip_start = 0.01
    cam.clip_end = 50.0
    return cam_obj
