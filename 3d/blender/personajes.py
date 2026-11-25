"""Maquetas 3D de Pipo y Plop, a escala real (unos 30 cm), con bocas de reemplazo.

Son maquetas procedurales para layout, animática y pruebas de luz: respetan las
proporciones de las láminas aprobadas del canal (cabeza de frijol, cuerpo en pera o
segmentado, manoplas sin dedos, piernas de pilar con base plana, ojos de botón con
párpados caídos). El modelo final se esculpe a mano (o se escanea un títere real) sobre
estas mismas medidas y conserva la misma jerarquía y las mismas bocas.

Cada personaje es un Empty raíz. poner_boca(raiz, "D", fotograma) muestra una sola de las
9 bocas de reemplazo, como en el stop-motion: no se deforma, se sustituye.
Orden de las bocas (nomenclatura de Rhubarb Lip Sync):
    0 X reposo · 1 A m/b/p · 2 B consonantes · 3 C e/i · 4 D a · 5 E o · 6 F u · 7 G f · 8 H l
"""
import math
import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

import arcilla

BOCAS = ["X", "A", "B", "C", "D", "E", "F", "G", "H"]

# Forma de cada boca: semiancho W, semialto H, sonrisa S (sube las comisuras),
# grosor del labio L, alto del labio A, lengua (None, "abajo", "arriba"). En metros,
# para la cara de Pipo; Plop usa las mismas proporciones escaladas.
FORMA_BOCA = {
    "X": dict(W=0.088, H=0.0011, S=0.016, L=0.005, A=0.0016, lengua=None),
    "A": dict(W=0.062, H=0.0009, S=0.007, L=0.0075, A=0.0032, lengua=None),
    "B": dict(W=0.078, H=0.0055, S=0.013, L=0.005, A=0.002, lengua=None),
    "C": dict(W=0.074, H=0.0135, S=0.011, L=0.0055, A=0.0022, lengua="abajo"),
    "D": dict(W=0.068, H=0.025, S=0.006, L=0.006, A=0.0026, lengua="abajo"),
    "E": dict(W=0.046, H=0.019, S=0.0, L=0.0065, A=0.003, lengua="abajo"),
    "F": dict(W=0.026, H=0.014, S=0.0, L=0.0075, A=0.0038, lengua=None),
    "G": dict(W=0.07, H=0.0045, S=0.01, L=0.0075, A=0.0034, lengua=None),
    "H": dict(W=0.07, H=0.0145, S=0.009, L=0.0055, A=0.0022, lengua="arriba"),
}


# ---------------------------------------------------------------- utilidades de malla

def _coleccion(nombre):
    col = bpy.data.collections.get(nombre)
    if col is None:
        col = bpy.data.collections.new(nombre)
        bpy.context.scene.collection.children.link(col)
    return col


def _objeto(nombre, bm, col, material=None):
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(nombre, me)
    col.objects.link(ob)
    if material is not None:
        me.materials.append(material)
    return ob


def _esfera(bm_dest, centro, radios, rot=(0, 0, 0), potencia=1.0, segs=40, anillos=28):
    """Elipsoide (o superelipsoide si potencia < 1: más 'de frijol') dentro de un bmesh."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=anillos, radius=1.0)
    if potencia != 1.0:
        for v in bm.verts:
            v.co = Vector(math.copysign(abs(c) ** potencia, c) for c in v.co)
    M = Matrix.Translation(centro) @ Euler(rot).to_matrix().to_4x4() @ Matrix.Diagonal((*radios, 1.0))
    bmesh.ops.transform(bm, matrix=M, verts=bm.verts)
    _fusionar(bm_dest, bm)


def _capsula(bm_dest, a, b, r0, r1=None, aplanado=1.0, segs=32, anillos=24):
    """Cápsula (cilindro con puntas redondas) de a a b; r0 abajo, r1 arriba (para conos romos)."""
    r1 = r0 if r1 is None else r1
    a, b = Vector(a), Vector(b)
    eje = b - a
    largo = eje.length
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=anillos, radius=1.0)
    for v in bm.verts:
        z = v.co.z
        t = 0.5 + 0.5 * math.copysign(1, z) if abs(z) > 1e-6 else 0.5
        r = r0 + (r1 - r0) * t
        x, y = v.co.x * r, v.co.y * r * aplanado
        zz = z * r + (largo if z > 0 else 0.0)
        v.co = Vector((x, y, zz))
    rot = Vector((0, 0, 1)).rotation_difference(eje.normalized()).to_matrix().to_4x4()
    bmesh.ops.transform(bm, matrix=Matrix.Translation(a) @ rot, verts=bm.verts)
    _fusionar(bm_dest, bm)


def _fusionar(bm_dest, bm):
    me = bpy.data.meshes.new("_tmp")
    bm.to_mesh(me)
    bm.free()
    bm_dest.from_mesh(me)
    bpy.data.meshes.remove(me)


def _aplicar(ob):
    """Aplica todos los modificadores sin depender del contexto de la interfaz."""
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev)
    viejo = ob.data
    ob.modifiers.clear()
    ob.data = me
    if viejo.users == 0:
        bpy.data.meshes.remove(viejo)
    for p in me.polygons:
        p.use_smooth = True


def _amasar(ob, voxel=0.0012, suavizado=6, irregular=0.0012, base_plana=True, semilla=0):
    """Une las piezas como plastilina: remallado por vóxeles, uniones suavizadas,
    irregularidad de modelado a mano y base plana para que apoye en el suelo."""
    m = ob.modifiers.new("vóxeles", "REMESH")
    m.mode = "VOXEL"
    m.voxel_size = voxel
    m.adaptivity = 0.0
    m.use_smooth_shade = True
    s = ob.modifiers.new("suavizado", "SMOOTH")
    s.factor = 0.6
    s.iterations = suavizado
    if irregular > 0:
        tex = bpy.data.textures.new(f"irregular_{ob.name}", "CLOUDS")
        tex.noise_scale = 0.035
        tex.noise_depth = 1
        d = ob.modifiers.new("hecho a mano", "DISPLACE")
        d.texture = tex
        d.texture_coords = "OBJECT"
        d.strength = irregular
        d.mid_level = 0.5
    _aplicar(ob)
    if base_plana:
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, 0.0), plane_no=(0, 0, 1), clear_inner=True)
        borde = [e for e in bm.edges if e.is_boundary]
        if borde:
            bmesh.ops.holes_fill(bm, edges=borde, sides=0)
        bm.to_mesh(ob.data)
        bm.free()
        for p in ob.data.polygons:
            p.use_smooth = True


def _superficie(cuerpo, x, z, desde_y=-1.0):
    """Punto y normal de la cara del personaje (rayo desde delante, hacia +Y)."""
    ok, loc, nor, _ = cuerpo.ray_cast(Vector((x, desde_y, z)), Vector((0, 1, 0)))
    if not ok:
        raise RuntimeError(f"El rayo no tocó la cara en x={x}, z={z}")
    return loc, nor


# ---------------------------------------------------------------- piezas de la cara

def _ojo(nombre, cuerpo, col, x, z, r, mats, caida=0.3, cubre=0.34, lado=1, bolsa=True,
        esclera=(1.22, 0.7)):
    """Ojo de botón: esfera negra brillante sobre un aro crema, párpado de plastilina caído
    (cubre ~42 % del ojo y cae hacia fuera) y una bolsita debajo.
    esclera = (ancho, fondo) del cuenco crema, relativos al radio del ojo: (1.22, 0.7) deja
    un aro fino como Pipo; (1.3, 0.74) deja más crema alrededor, como Plop."""
    loc, nor = _superficie(cuerpo, x, z)
    centro = loc - nor * (0.3 * r)
    piezas = []

    bm = bmesh.new()
    _esfera(bm, centro, (r, r, r), segs=64, anillos=48)
    piezas.append(_objeto(f"{nombre}_ojo", bm, col, mats["ojo"]))

    # Esclera: un cuenco ovalado detrás del botón (no una esfera concéntrica): así la línea
    # entre el negro y el crema es limpia y el aro crema asoma alrededor del botón.
    ancho, fondo = esclera
    giro = Vector((0, 0, 1)).rotation_difference(nor).to_euler()
    bm = bmesh.new()
    _esfera(bm, centro, (ancho * r, ancho * r, fondo * r), rot=giro, segs=64, anillos=48)
    piezas.append(_objeto(f"{nombre}_esclera", bm, col, mats["esclera"]))

    # Párpado: casquete de una esfera algo mayor que el ojo, cortado por un plano inclinado
    # hacia el lado exterior (ojos caídos) y un poco hacia la cámara. Con grosor y borde
    # redondeado, como una tira de plastilina puesta encima del ojo.
    rl = r * 1.16
    bm = bmesh.new()
    _esfera(bm, centro, (rl, rl, rl), segs=64, anillos=48)
    ang = caida * lado
    n_corte = Vector((math.sin(ang), 0.0, math.cos(ang)))
    n_corte.rotate(Matrix.Rotation(0.12, 3, "X"))
    p_corte = centro + n_corte * (rl * (1 - 2 * cubre))
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=p_corte, plane_no=n_corte, clear_inner=True)
    parpado = _objeto(f"{nombre}_parpado", bm, col, mats["piel"])
    so = parpado.modifiers.new("grosor", "SOLIDIFY")
    so.thickness = 0.3 * r
    so.offset = -1.0
    so.use_rim = True
    sub = parpado.modifiers.new("borde redondo", "SUBSURF")
    sub.levels = sub.render_levels = 2
    _aplicar(parpado)
    piezas.append(parpado)

    if bolsa:
        # Relieve en arco bajo el ojo (de 205° a 335°), proyectado sobre la cara.
        n_arco = 40
        perfil = [0.0, 0.6, 1.0, 0.6, 0.0]
        anillos = []
        for j, _ in enumerate(perfil):
            rr = r * (1.02 + 0.32 * j / (len(perfil) - 1))
            anillos.append([(rr * math.cos(t), rr * math.sin(t)) for t in
                            (math.radians(205 + 130 * i / (n_arco - 1)) for i in range(n_arco))])
        pesos = [[p * math.sin(math.pi * i / (n_arco - 1)) ** 0.7 for i in range(n_arco)] for p in perfil]
        b = _lamina(f"{nombre}_bolsa", anillos, x, z, cuerpo, col, mats["piel"], hacia_fuera=True,
                    alturas=pesos, relieve=0.22 * r, desfase=0.0001, cerrado=False)
        piezas.append(b)
    return piezas


def _contorno_boca(W, H, S, n=96):
    """Contorno de la boca en el plano de la cara (x, z): elipse con las comisuras subidas."""
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        c, s = math.cos(t), math.sin(t)
        pts.append((W * c, H * s + S * c * c))
    return pts


def _desplazar_contorno(contorno, desplazamientos):
    """Anillos paralelos al contorno, desplazados hacia fuera (positivo) o hacia dentro."""
    n = len(contorno)
    cx = sum(p[0] for p in contorno) / n
    cz = sum(p[1] for p in contorno) / n
    normales = []
    for i in range(n):
        x0, z0 = contorno[i - 1]
        x1, z1 = contorno[(i + 1) % n]
        nx, nz = (z1 - z0), -(x1 - x0)
        largo = math.hypot(nx, nz) or 1.0
        nx, nz = nx / largo, nz / largo
        if nx * (contorno[i][0] - cx) + nz * (contorno[i][1] - cz) < 0:
            nx, nz = -nx, -nz
        normales.append((nx, nz))
    return [[(x + nx * d, z + nz * d) for (x, z), (nx, nz) in zip(contorno, normales)] for d in desplazamientos]


def _lamina(nombre, anillos, cx, cz, cuerpo, col, material, hacia_fuera, alturas=None, relieve=0.0,
            desfase=0.0003, cerrar=False, cerrado=True):
    """Malla plana delante de la cara (plano XZ) que se proyecta sobre la superficie.
    hacia_fuera: True si los anillos van del interior al exterior (labios)."""
    bm = bmesh.new()
    capas = [[bm.verts.new((cx + x, -0.5, cz + z)) for x, z in pts] for pts in anillos]
    for a, b in zip(capas, capas[1:]):
        n = len(a)
        for i in range(n if cerrado else n - 1):
            if hacia_fuera:
                bm.faces.new((a[i], b[i], b[(i + 1) % n], a[(i + 1) % n]))
            else:
                bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    if cerrar:
        bm.faces.new(list(reversed(capas[-1])) if not hacia_fuera else capas[-1])
    ob = _objeto(nombre, bm, col, material)
    if alturas is not None:
        grupo = ob.vertex_groups.new(name="altura")
        n = len(anillos[0])
        for j, peso in enumerate(alturas):
            if isinstance(peso, (list, tuple)):          # un peso por vértice
                for i, pv in enumerate(peso):
                    grupo.add([j * n + i], pv, "REPLACE")
            else:
                grupo.add(list(range(j * n, (j + 1) * n)), peso, "REPLACE")
    sw = ob.modifiers.new("sobre la cara", "SHRINKWRAP")
    sw.target = cuerpo
    sw.wrap_method = "PROJECT"
    sw.use_project_y = True
    sw.use_negative_direction = True
    sw.use_positive_direction = True
    sw.offset = desfase
    if alturas is not None:
        d = ob.modifiers.new("relieve del labio", "DISPLACE")
        d.direction = "NORMAL"
        d.vertex_group = "altura"
        d.strength = relieve * 2.0
        d.mid_level = 0.5
        sub = ob.modifiers.new("suave", "SUBSURF")
        sub.levels = sub.render_levels = 1
    return ob


def _boca(nombre, cuerpo, col, cx, cz, forma, k, mats):
    """Una boca de reemplazo: interior oscuro + labios de plastilina adaptados a la cara.
    k escala la boca al tamaño de la cara del personaje."""
    W, H, S = forma["W"] * k, forma["H"] * k, forma["S"] * k
    L, A = forma["L"] * k, forma["A"] * k
    raiz = bpy.data.objects.new(nombre, None)
    col.objects.link(raiz)
    piezas = []

    contorno = _contorno_boca(W, H, S)
    # Interior denso (si no, la cara curva asoma entre los triángulos). En bocas abiertas se
    # encoge hacia el centro; en las cerradas (una media luna fina) se desplaza hacia dentro,
    # porque encoger una media luna la sacaría de la boca.
    pasos = [i / 13 for i in range(14)]
    if H > 0.6 * S:
        mx = sum(x for x, _ in contorno) / len(contorno)
        mz = sum(z for _, z in contorno) / len(contorno)
        interior = [[(mx + (x - mx) * (1 - 0.97 * f), mz + (z - mz) * (1 - 0.97 * f)) for x, z in contorno]
                    for f in pasos]
    else:
        interior = _desplazar_contorno(contorno, [-0.95 * H * f for f in pasos])
    ob = _lamina(f"{nombre}_interior", interior, cx, cz, cuerpo, col, mats["interior"],
                 hacia_fuera=False, desfase=0.0002, cerrar=True)
    ob.parent = raiz
    piezas.append(ob)

    perfil = [0.0, 0.55, 0.92, 1.0, 0.82, 0.42, 0.0]
    desps = [-0.2 * L + 1.2 * L * j / (len(perfil) - 1) for j in range(len(perfil))]
    labios = _desplazar_contorno(contorno, desps)
    # Los labios siempre por encima del interior (si se cruzan, salen motas en las comisuras).
    ob = _lamina(f"{nombre}_labios", labios, cx, cz, cuerpo, col, mats["piel"], hacia_fuera=True,
                 alturas=perfil, relieve=A, desfase=0.00035)
    ob.parent = raiz
    piezas.append(ob)

    if forma["lengua"]:
        arriba = forma["lengua"] == "arriba"
        tz = cz + S * 0.25 + (H * 0.3 if arriba else -H * 0.42)
        loc, nor = _superficie(cuerpo, cx, tz)
        bm = bmesh.new()
        _esfera(bm, loc - nor * 0.0012, (W * 0.4, 0.0035 * k, max(H * 0.4, 0.003 * k)))
        lg = _objeto(f"{nombre}_lengua", bm, col, mats["lengua"])
        lg.parent = raiz
        piezas.append(lg)
    return raiz, piezas


def _bocas(prefijo, raiz_personaje, cuerpo, col, cx, cz, k, mats):
    """Crea las 9 bocas de reemplazo. Se cambian con poner_boca() (claves de visibilidad:
    lo más robusto en Blender, en el visor y en el render)."""
    raiz_personaje["boca"] = 0
    ui = raiz_personaje.id_properties_ui("boca")
    ui.update(min=0, max=len(BOCAS) - 1, description="Boca de reemplazo: " + " ".join(BOCAS))
    raiz_personaje["prefijo_bocas"] = prefijo
    for i, clave in enumerate(BOCAS):
        r, piezas = _boca(f"{prefijo}_boca_{clave}", cuerpo, col, cx, cz, FORMA_BOCA[clave], k, mats)
        r.parent = raiz_personaje
    poner_boca(raiz_personaje, "X")


def _piezas_boca(raiz_personaje, clave):
    r = bpy.data.objects[f"{raiz_personaje['prefijo_bocas']}_boca_{clave}"]
    return [r] + list(r.children)


def poner_boca(raiz_personaje, clave, fotograma=None):
    """Muestra solo la boca `clave` (X, A-H). Con `fotograma`, además deja una clave
    constante en ese fotograma (así se anima la sincronía de labios)."""
    if isinstance(clave, int):
        clave = BOCAS[clave]
    raiz_personaje["boca"] = BOCAS.index(clave)
    if fotograma is not None:
        raiz_personaje.keyframe_insert('["boca"]', frame=fotograma)
    for otra in BOCAS:
        for ob in _piezas_boca(raiz_personaje, otra):
            oculto = otra != clave
            ob.hide_render = oculto
            ob.hide_viewport = oculto
            if fotograma is not None:
                for prop in ("hide_render", "hide_viewport"):
                    ob.keyframe_insert(prop, frame=fotograma)
                for fc in _curvas(ob):
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT"


def _curvas(ob):
    ad = ob.animation_data
    if not ad or not ad.action:
        return []
    acc = ad.action
    if hasattr(acc, "fcurves") and len(acc.fcurves):
        return list(acc.fcurves)
    out = []
    for capa in getattr(acc, "layers", []):
        for tira in capa.strips:
            for bolsa in getattr(tira, "channelbags", []):
                out.extend(bolsa.fcurves)
    return out


def _materiales(clave_color, semilla):
    C = arcilla.COLORES
    return {
        "piel": arcilla.plastilina(f"{clave_color} plastilina", C[clave_color], semilla=semilla),
        "ojo": arcilla.brillante("ojo de botón", C["ojo"]),
        "esclera": arcilla.plastilina("esclera crema", C["esclera"], huellas=0.4, boil=0.1, bultos=0.3),
        "interior": arcilla.plastilina("interior de la boca", "#3B1519", huellas=0.3, boil=0.0, rugosidad=0.7),
        "lengua": arcilla.plastilina("lengua rosa", "#E06A7E", huellas=0.5, boil=0.1, semilla=3),
    }


def _raiz(nombre, col, ubicacion, giro_z):
    raiz = bpy.data.objects.new(nombre, None)
    raiz.empty_display_type = "ARROWS"
    raiz.empty_display_size = 0.08
    col.objects.link(raiz)
    raiz["altura_cm"] = 30
    return raiz


def _colocar(raiz, objetos, ubicacion, giro_z):
    for ob in objetos:
        if ob.parent is None:
            ob.parent = raiz
    raiz.location = ubicacion
    raiz.rotation_euler = (0, 0, giro_z)


# ---------------------------------------------------------------- personajes

def crear_pipo(ubicacion=(0, 0, 0), giro_z=0.0, brazo_izq=0.0, brazo_der=0.0, boca="X", coleccion="Pipo"):
    """Pipo: cabeza ancha de frijol con orejitas como cuernitos, cuerpo en pera, chaleco
    mostaza con dos botones. brazo_izq/der: ángulo en radianes (0 = colgando, 2.4 = arriba)."""
    col = _coleccion(coleccion)
    mats = _materiales("pipo", semilla=0.0)
    raiz = _raiz("Pipo", col, ubicacion, giro_z)

    bm = bmesh.new()
    _esfera(bm, (0, 0, 0.237), (0.128, 0.084, 0.058), potencia=0.82)            # cabeza de frijol
    _esfera(bm, (0, 0.004, 0.13), (0.074, 0.064, 0.072))                          # cuerpo en pera
    _esfera(bm, (0, 0.002, 0.098), (0.079, 0.068, 0.05))
    for lado in (-1, 1):
        _capsula(bm, (lado * 0.1, 0.004, 0.266), (lado * 0.128, 0.006, 0.302), 0.0175, 0.0075)   # orejitas
        _capsula(bm, (lado * 0.036, 0.004, -0.01), (lado * 0.036, 0.004, 0.07), 0.0225)            # piernas
        ang = brazo_der if lado < 0 else brazo_izq   # mirando a cámara, su derecha queda a la izquierda
        hombro = Vector((lado * 0.07, 0.006, 0.168))
        dirb = Vector((lado * math.sin(0.2 + ang), 0, -math.cos(0.2 + ang)))
        _capsula(bm, hombro, hombro + dirb * 0.115, 0.0165, 0.019, aplanado=0.8)                    # manoplas
    cuerpo = _objeto("Pipo_cuerpo", bm, col, mats["piel"])
    _amasar(cuerpo)

    piezas = [cuerpo]
    for lado, nombre in ((-1, "der"), (1, "izq")):
        piezas += _ojo(f"Pipo_{nombre}", cuerpo, col, lado * 0.06, 0.256, 0.0195, mats, lado=lado)

    # Chaleco: banda de plastilina alrededor del torso, con solapa y dos botones.
    mat_ch = arcilla.plastilina("chaleco mostaza", arcilla.COLORES["chaleco"], semilla=5)
    bm = bmesh.new()
    _esfera(bm, (0, 0.004, 0.13), (0.0752, 0.0652, 0.0732), segs=64, anillos=40)
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, 0.183), plane_no=(0, 0, 1), clear_outer=True)
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, 0.098), plane_no=(0, 0, 1), clear_inner=True)
    chaleco = _objeto("Pipo_chaleco", bm, col, mat_ch)
    so = chaleco.modifiers.new("grosor", "SOLIDIFY")
    so.thickness = 0.0045
    so.offset = 1.0
    _aplicar(chaleco)
    _amasar(chaleco, voxel=0.0009, suavizado=4, irregular=0.0006, base_plana=False)
    piezas.append(chaleco)

    mat_bt = arcilla.plastilina("botón hueso", arcilla.COLORES["boton"], huellas=0.3, boil=0.05, bultos=0.3)
    mat_hueco = arcilla.plastilina("hueco del botón", "#9C978C", huellas=0.0, boil=0.0, bultos=0.0, poros=0.0)
    for i, z in enumerate((0.158, 0.124)):
        loc, nor = _superficie(chaleco, 0.024, z)
        bm = bmesh.new()
        _esfera(bm, loc, (0.0085, 0.0085, 0.0085))
        bt = _objeto(f"Pipo_boton_{i}", bm, col, mat_bt)
        bt.scale = (1, 1, 1)
        bt.data.transform(Matrix.Translation(loc) @ Matrix.Diagonal((1, 0.45, 1, 1)) @ Matrix.Translation(-loc))
        piezas.append(bt)
        for dx in (-0.0025, 0.0025):
            bm = bmesh.new()
            _esfera(bm, loc + Vector((dx, -0.0038, 0.0)), (0.0014, 0.0014, 0.0014), segs=12, anillos=8)
            piezas.append(_objeto(f"Pipo_hueco_{i}_{dx>0}", bm, col, mat_hueco))

    _bocas("Pipo", raiz, cuerpo, col, 0.0, 0.214, 1.0, mats)
    poner_boca(raiz, boca)
    _colocar(raiz, piezas, ubicacion, giro_z)
    return raiz


def crear_plop(ubicacion=(0, 0, 0), giro_z=0.0, brazo_izq=0.0, brazo_der=0.0, boca="X", coleccion="Plop"):
    """Plop: parecido a un tardígrado. Cabeza de frijol fundida con un torso de tres
    segmentos, dos antenitas con bolita, corbatín terracota."""
    col = _coleccion(coleccion)
    mats = _materiales("plop", semilla=7.0)
    raiz = _raiz("Plop", col, ubicacion, giro_z)

    bm = bmesh.new()
    _esfera(bm, (0, 0, 0.247), (0.12, 0.084, 0.058), potencia=0.93)            # cabeza
    _esfera(bm, (0, 0.004, 0.118), (0.084, 0.07, 0.088))                          # núcleo del torso
    for z, rx, rz in ((0.176, 0.083, 0.05), (0.122, 0.087, 0.052), (0.068, 0.086, 0.048)):
        _esfera(bm, (0, 0.004, z), (rx, rx * 0.82, rz))                           # tres segmentos
    for lado in (-1, 1):
        _capsula(bm, (lado * 0.04, 0.004, -0.01), (lado * 0.04, 0.004, 0.06), 0.021)               # piernas
        ang = brazo_der if lado < 0 else brazo_izq   # mirando a cámara, su derecha queda a la izquierda
        hombro = Vector((lado * 0.08, 0.006, 0.168))
        dirb = Vector((lado * math.sin(0.16 + ang), 0, -math.cos(0.16 + ang)))
        _capsula(bm, hombro, hombro + dirb * 0.112, 0.018, 0.02, aplanado=0.8)
    cuerpo = _objeto("Plop_cuerpo", bm, col, mats["piel"])
    _amasar(cuerpo, semilla=1)

    piezas = [cuerpo]
    for lado in (-1, 1):                                                         # antenitas
        bm = bmesh.new()
        _capsula(bm, (lado * 0.034, 0.0, 0.284), (lado * 0.038, 0.0, 0.309), 0.0032, 0.0026)
        _esfera(bm, (lado * 0.038, 0.0, 0.311), (0.0058, 0.0058, 0.0058))
        piezas.append(_objeto(f"Plop_antena_{lado}", bm, col, mats["piel"]))
    for lado, nombre in ((-1, "der"), (1, "izq")):
        piezas += _ojo(f"Plop_{nombre}", cuerpo, col, lado * 0.05, 0.262, 0.0165, mats, lado=lado, caida=0.22,
                        esclera=(1.3, 0.74))

    mat_c = arcilla.plastilina("corbatín terracota", arcilla.COLORES["corbatin"], semilla=9)
    loc, nor = _superficie(cuerpo, 0.0, 0.18)                    # en el torso, bajo la cabeza
    bm = bmesh.new()
    for lado in (-1, 1):                     # lazos que se ensanchan hacia fuera, como un corbatín
        _capsula(bm, loc + Vector((lado * 0.006, -0.007, 0.0)), loc + Vector((lado * 0.034, -0.005, 0.002)),
                 0.009, 0.021, aplanado=0.5)
    _esfera(bm, loc + Vector((0, -0.011, 0)), (0.011, 0.009, 0.013))
    corbatin = _objeto("Plop_corbatin", bm, col, mat_c)
    _amasar(corbatin, voxel=0.0008, suavizado=4, irregular=0.0006, base_plana=False)
    piezas.append(corbatin)

    _bocas("Plop", raiz, cuerpo, col, 0.0, 0.234, 0.9, mats)
    poner_boca(raiz, boca)
    _colocar(raiz, piezas, ubicacion, giro_z)
    return raiz
