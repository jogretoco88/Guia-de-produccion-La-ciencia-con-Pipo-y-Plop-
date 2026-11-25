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
    "X": dict(W=0.088, H=0.0011, S=0.009, L=0.005, A=0.0016, lengua=None),
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
    irregularidad de modelado a mano y, si se pide, base plana con el canto redondeado
    (como un títere apretado contra la mesa), apoyada en z = 0."""
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
    if base_plana:                       # apoyar: el punto más bajo queda en z = 0
        zmin = min(v.co.z for v in ob.data.vertices)
        for v in ob.data.vertices:
            v.co.z -= zmin
            if v.co.z < 0.0008:          # aplana la suela, deja el canto redondeado
                v.co.z = 0.0
    for p in ob.data.polygons:
        p.use_smooth = True


def _superficie(cuerpo, x, z, desde_y=-1.0):
    """Punto y normal de la cara del personaje (rayo desde delante, hacia +Y)."""
    ok, loc, nor, _ = cuerpo.ray_cast(Vector((x, desde_y, z)), Vector((0, 1, 0)))
    if not ok:
        raise RuntimeError(f"El rayo no tocó la cara en x={x}, z={z}")
    return loc, nor


# ---------------------------------------------------------------- piezas de la cara

def _arco(nombre, cuerpo, col, cx, cz, r_in, r_out, ang0, ang1, relieve, mat, n=48):
    """Tira de plastilina en arco alrededor de un punto de la cara (párpado inferior, ceja,
    bolsa), pegada a la superficie y con perfil redondeado."""
    perfil = [0.0, 0.55, 0.95, 1.0, 0.85, 0.45, 0.0]
    anillos = []
    for j in range(len(perfil)):
        rr = r_in + (r_out - r_in) * j / (len(perfil) - 1)
        anillos.append([(rr * math.cos(t), rr * math.sin(t)) for t in
                        (math.radians(ang0 + (ang1 - ang0) * i / (n - 1)) for i in range(n))])
    pesos = [[p * max(0.0, math.sin(math.pi * i / (n - 1))) ** 0.6 for i in range(n)] for p in perfil]
    return _lamina(nombre, anillos, cx, cz, cuerpo, col, mat, hacia_fuera=True,
                   alturas=pesos, relieve=relieve, desfase=0.0001, cerrado=False)


def _ojo(nombre, cuerpo, col, x, z, r, mats, lado=1, estilo="pipo", caida=0.3, cubre=0.34, bolsa=True):
    """Ojo de las láminas del canal, con párpados de tiras de plastilina.

    estilo "pipo": globo blanco brillante con una gran pupila negra en relieve (deja ver
                   el blanco a los lados).
    estilo "plop": botón negro brillante sobre un aro crema ancho.
    Encima: párpado caído (casquete, cae hacia fuera) y una ceja en tira. Debajo: párpado
    inferior en tira y, si bolsa=True, una segunda tira (la bolsa de Pipo)."""
    loc, nor = _superficie(cuerpo, x, z)
    giro = Vector((0, 0, 1)).rotation_difference(nor).to_euler()
    piezas = []
    if estilo == "pipo":
        centro = loc - nor * (0.35 * r)
        bm = bmesh.new()
        _esfera(bm, centro, (r, r, r), segs=96, anillos=64)
        piezas.append(_objeto(f"{nombre}_globo", bm, col, mats["globo"]))
        abajo = (Vector((0, 0, -1)) - nor * nor.dot(Vector((0, 0, -1)))).normalized()
        bm = bmesh.new()                    # pupila: esfera menor adelantada (borde nítido), algo baja
        _esfera(bm, centro + nor * (0.36 * r) + abajo * (0.13 * r), (0.84 * r,) * 3, segs=96, anillos=64)
        piezas.append(_objeto(f"{nombre}_pupila", bm, col, mats["ojo"]))
        r_ext, rl = 1.0 * r, 1.2 * r
    else:
        centro = loc - nor * (0.3 * r)
        bm = bmesh.new()
        _esfera(bm, centro, (r, r, r), segs=96, anillos=64)
        piezas.append(_objeto(f"{nombre}_ojo", bm, col, mats["ojo"]))
        bm = bmesh.new()                    # aro crema: cuenco ovalado detrás del botón
        _esfera(bm, centro, (1.27 * r, 1.27 * r, 0.74 * r), rot=giro, segs=96, anillos=64)
        piezas.append(_objeto(f"{nombre}_esclera", bm, col, mats["esclera"]))
        r_ext, rl = 1.25 * r, 1.2 * r

    # Párpado superior: casquete de esfera cortado por un plano inclinado hacia fuera.
    bm = bmesh.new()
    _esfera(bm, centro, (rl, rl, rl), segs=72, anillos=48)
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

    # Tiras: caen hacia el lado exterior, como los ojos cansados de las láminas.
    g = -12 * lado
    piezas.append(_arco(f"{nombre}_ceja", cuerpo, col, x, z, r_ext * 1.2, r_ext * 1.46, 34 + g, 146 + g,
                        0.4 * r_ext, mats["piel"]))
    piezas.append(_arco(f"{nombre}_parpado_inf", cuerpo, col, x, z, r_ext * 0.98, r_ext * 1.24, 202 + g, 338 + g,
                        0.3 * r_ext, mats["piel"]))
    if bolsa:
        piezas.append(_arco(f"{nombre}_bolsa", cuerpo, col, x, z, r_ext * 1.27, r_ext * 1.5, 216 + g, 324 + g,
                            0.18 * r_ext, mats["piel"]))
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


_BVH = {}


def _bvh_de(cuerpo):
    """Árbol de búsqueda de la superficie del cuerpo (se rehace al crear cada personaje)."""
    if cuerpo.name not in _BVH:
        from mathutils.bvhtree import BVHTree
        _BVH[cuerpo.name] = BVHTree.FromObject(cuerpo, bpy.context.evaluated_depsgraph_get())
    return _BVH[cuerpo.name]


def _lamina(nombre, anillos, cx, cz, cuerpo, col, material, hacia_fuera, alturas=None, relieve=0.0,
            desfase=0.0003, cerrar=False, cerrado=True):
    """Malla que se apoya sobre la cara: cada punto (x, z) se lleva a la superficie con un
    rayo desde delante; si el rayo no toca la cabeza (borde de la silueta), se usa el punto
    más cercano. Después se levanta según `alturas` (0-1) x `relieve` (labios, tiras).
    hacia_fuera: True si los anillos van del interior al exterior."""
    bvh = _bvh_de(cuerpo)
    n = len(anillos[0])

    def peso(j, i):
        if alturas is None:
            return 0.0
        a = alturas[j]
        return a[i] if isinstance(a, (list, tuple)) else a

    bm = bmesh.new()
    capas = []
    for j, pts in enumerate(anillos):
        capa = []
        for i, (x, z) in enumerate(pts):
            loc, nor, _, _ = bvh.ray_cast(Vector((cx + x, -1.0, cz + z)), Vector((0, 1, 0)))
            if loc is None:
                loc, nor, _, _ = bvh.find_nearest(Vector((cx + x, -0.06, cz + z)))
            capa.append(bm.verts.new(loc + nor * (desfase + peso(j, i) * relieve)))
        capas.append(capa)
    for a, b in zip(capas, capas[1:]):
        for i in range(n if cerrado else n - 1):
            if hacia_fuera:
                bm.faces.new((a[i], b[i], b[(i + 1) % n], a[(i + 1) % n]))
            else:
                bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    if cerrar:
        bm.faces.new(list(reversed(capas[-1])) if not hacia_fuera else capas[-1])
    ob = _objeto(nombre, bm, col, material)
    if alturas is not None:
        sub = ob.modifiers.new("suave", "SUBSURF")
        sub.levels = sub.render_levels = 1
    return ob


def _boca(nombre, cuerpo, col, cx, cz, forma, k, mats):
    """Una boca de reemplazo: interior oscuro + labios de plastilina adaptados a la cara.
    k = (ancho, alto): escala la boca a la cara del personaje (Pipo la tiene muy ancha)."""
    kx, kz = k if isinstance(k, (tuple, list)) else (k, k)
    W, H, S = forma["W"] * kx, forma["H"] * kz, forma["S"] * kz
    L, A = forma["L"] * kz, forma["A"] * kz
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
        _esfera(bm, loc - nor * 0.0012, (W * 0.4, 0.0035 * kz, max(H * 0.4, 0.003 * kz)))
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
        "globo": arcilla.brillante("globo ocular blanco", C["globo"], rugosidad=0.22),
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
    """Pipo: cabeza ancha de frijol con orejitas como cuernitos hacia los lados, ojos blancos
    de pupila grande con párpados, cejas y bolsas de tiras, boca muy ancha, cuerpo en pera,
    chaleco mostaza cruzado con dos botones y piernas de pilar (casi un cuarto de su altura).
    Proporciones medidas sobre la lámina aprobada. brazo_izq/der: ángulo en radianes
    (0 = colgando, 2.4 = arriba)."""
    col = _coleccion(coleccion)
    mats = _materiales("pipo", semilla=0.0)
    raiz = _raiz("Pipo", col, ubicacion, giro_z)
    up = 0.011                                                                    # piernas de la lámina

    bm = bmesh.new()
    _esfera(bm, (0, 0, 0.237 + up), (0.125, 0.082, 0.058), potencia=0.82)        # cabeza de frijol
    _esfera(bm, (0, 0.004, 0.13 + up), (0.077, 0.064, 0.072))                     # cuerpo en pera
    _esfera(bm, (0, 0.002, 0.094 + up), (0.079, 0.07, 0.052))                     # barriga redonda
    for lado in (-1, 1):
        _capsula(bm, (lado * 0.098, 0.003, 0.258 + up), (lado * 0.136, 0.004, 0.29 + up), 0.02, 0.0078)  # orejitas
        _capsula(bm, (lado * 0.037, 0.004, 0.01), (lado * 0.037, 0.004, 0.07 + up), 0.0245)        # piernas, pie redondeado
        ang = brazo_der if lado < 0 else brazo_izq   # mirando a cámara, su derecha queda a la izquierda
        hombro = Vector((lado * 0.074, 0.006, 0.17 + up))
        dirb = Vector((lado * math.sin(0.33 + ang), 0, -math.cos(0.33 + ang)))
        _capsula(bm, hombro, hombro + dirb * 0.097, 0.0175, 0.0215, aplanado=0.8)                   # manoplas
    cuerpo = _objeto("Pipo_cuerpo", bm, col, mats["piel"])
    _amasar(cuerpo)
    _BVH.pop(cuerpo.name, None)

    piezas = [cuerpo]
    for lado, nombre in ((-1, "der"), (1, "izq")):
        piezas += _ojo(f"Pipo_{nombre}", cuerpo, col, lado * 0.068, 0.254 + up, 0.0235, mats, lado=lado,
                       estilo="pipo", caida=0.28, cubre=0.3, bolsa=True)

    # Chaleco: banda alrededor del torso y, encima, la solapa del lado izquierdo de Pipo
    # (a la derecha en pantalla), que monta sobre la otra mitad como en la lámina.
    mat_ch = arcilla.plastilina("chaleco mostaza", arcilla.COLORES["chaleco"], semilla=5)

    def banda(nombre, extra, recorte_x=None):
        bm = bmesh.new()
        _esfera(bm, (0, 0.004, 0.13 + up), (0.0782 + extra, 0.0652 + extra, 0.0732 + extra * 0.5), segs=72, anillos=48)
        for co, no, fuera in (((0, 0, 0.187 + up), (0, -0.32, 1), True), ((0, 0, 0.09 + up), (0, 0, 1), False)):
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co, plane_no=no,
                                   clear_outer=fuera, clear_inner=not fuera)
        if recorte_x is not None:
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(recorte_x, 0, 0), plane_no=(1, 0, 0), clear_inner=True)
        ob = _objeto(nombre, bm, col, mat_ch)
        so = ob.modifiers.new("grosor", "SOLIDIFY")
        so.thickness = 0.004
        so.offset = 1.0
        _aplicar(ob)
        _amasar(ob, voxel=0.0009, suavizado=4, irregular=0.0005, base_plana=False)
        return ob

    piezas.append(banda("Pipo_chaleco", 0.0))
    solapa = banda("Pipo_chaleco_solapa", 0.0038, recorte_x=0.009)
    piezas.append(solapa)

    mat_bt = arcilla.plastilina("botón hueso", arcilla.COLORES["boton"], huellas=0.3, boil=0.05, bultos=0.3)
    mat_hueco = arcilla.plastilina("hueco del botón", "#8F8A80", huellas=0.0, boil=0.0, bultos=0.0, poros=0.0)
    for i, z in enumerate((0.16 + up, 0.122 + up)):
        loc, nor = _superficie(solapa, 0.03, z)
        bm = bmesh.new()
        _esfera(bm, loc, (0.0095, 0.0095, 0.0095), segs=40, anillos=24)
        bt = _objeto(f"Pipo_boton_{i}", bm, col, mat_bt)
        bt.data.transform(Matrix.Translation(loc) @ Matrix.Diagonal((1, 0.42, 1, 1)) @ Matrix.Translation(-loc))
        piezas.append(bt)
        for dx in (-0.0027, 0.0027):                     # dos agujeros alargados
            bm = bmesh.new()
            _esfera(bm, loc + Vector((dx, -0.0038, 0.0)), (0.0011, 0.0012, 0.0022), segs=12, anillos=8)
            piezas.append(_objeto(f"Pipo_hueco_{i}_{dx > 0}", bm, col, mat_hueco))

    _bocas("Pipo", raiz, cuerpo, col, 0.0, 0.203 + up, (1.08, 1.0), mats)
    poner_boca(raiz, boca)
    _colocar(raiz, piezas, ubicacion, giro_z)
    return raiz


def crear_plop(ubicacion=(0, 0, 0), giro_z=0.0, brazo_izq=0.0, brazo_der=0.0, boca="X", coleccion="Plop"):
    """Plop: parecido a un tardígrado. Cabeza de frijol que sobresale sobre un torso de tres
    segmentos, ojos de botón con aro crema, párpados y cejas de tiras, dos antenitas con
    bolita, corbatín terracota de lazos planos y piernas cortas de pilar."""
    col = _coleccion(coleccion)
    mats = _materiales("plop", semilla=7.0)
    raiz = _raiz("Plop", col, ubicacion, giro_z)
    up = 0.018                                                                    # piernas de la lámina

    bm = bmesh.new()
    _esfera(bm, (0, 0, 0.24 + up), (0.126, 0.086, 0.07), potencia=0.88)          # cabeza de píldora
    _esfera(bm, (0, 0.004, 0.118 + up), (0.088, 0.072, 0.088))                   # núcleo del torso, rechoncho
    for z, rx, rz in ((0.174, 0.084, 0.044), (0.124, 0.1, 0.05), (0.072, 0.098, 0.047)):
        _esfera(bm, (0, 0.004, z + up), (rx, rx * 0.82, rz))                      # tres segmentos marcados
    for lado in (-1, 1):
        _capsula(bm, (lado * 0.042, 0.004, 0.01), (lado * 0.042, 0.004, 0.06 + up), 0.026)         # piernas, pie redondeado
        ang = brazo_der if lado < 0 else brazo_izq   # mirando a cámara, su derecha queda a la izquierda
        hombro = Vector((lado * 0.092, 0.006, 0.156 + up))
        dirb = Vector((lado * math.sin(0.2 + ang), 0, -math.cos(0.2 + ang)))
        _capsula(bm, hombro, hombro + dirb * 0.098, 0.021, 0.024, aplanado=0.8)
    cuerpo = _objeto("Plop_cuerpo", bm, col, mats["piel"])
    _amasar(cuerpo)
    _BVH.pop(cuerpo.name, None)

    piezas = [cuerpo]
    for lado in (-1, 1):                                                         # antenitas
        bm = bmesh.new()
        _capsula(bm, (lado * 0.026, 0.0, 0.3 + up), (lado * 0.031, 0.0, 0.325 + up), 0.0042, 0.0036)
        _esfera(bm, (lado * 0.031, 0.0, 0.328 + up), (0.0068, 0.0068, 0.0068))
        piezas.append(_objeto(f"Plop_antena_{lado}", bm, col, mats["piel"]))
    for lado, nombre in ((-1, "der"), (1, "izq")):
        piezas += _ojo(f"Plop_{nombre}", cuerpo, col, lado * 0.045, 0.245 + up, 0.0168, mats, lado=lado,
                       estilo="plop", caida=0.22, cubre=0.42, bolsa=False)

    # Corbatín: dos lazos que se ensanchan hacia fuera, acolchados, y un nudo rectangular.
    mat_c = arcilla.plastilina("corbatín terracota", arcilla.COLORES["corbatin"], semilla=9)
    loc, nor = _superficie(cuerpo, 0.0, 0.166 + up)
    bm = bmesh.new()

    def redondear(t, bisel):
        """Bisela la caja: caras planas con cantos redondeados, como plastilina aplanada."""
        tmp = _objeto("_tmp_pieza", t, col)
        m = tmp.modifiers.new("canto", "BEVEL")
        m.width = bisel
        m.segments = 4
        m.limit_method = "NONE"
        _aplicar(tmp)
        bm.from_mesh(tmp.data)
        me = tmp.data
        bpy.data.objects.remove(tmp)
        bpy.data.meshes.remove(me)

    for lado in (-1, 1):
        t = bmesh.new()
        bmesh.ops.create_cube(t, size=1.0)
        for v in t.verts:
            u = v.co.x + 0.5                                  # 0 junto al nudo, 1 en el borde exterior
            alto = 0.027 + (0.053 - 0.027) * u
            v.co = Vector((lado * (0.006 + 0.047 * u), v.co.y * 0.024, v.co.z * alto))
        bmesh.ops.transform(t, matrix=Matrix.Translation(loc + Vector((0, -0.009, 0))), verts=t.verts)
        redondear(t, 0.0095)
    nudo = bmesh.new()
    bmesh.ops.create_cube(nudo, size=1.0)
    bmesh.ops.transform(nudo, matrix=Matrix.Translation(loc + Vector((0, -0.013, 0))) @ Matrix.Diagonal((0.024, 0.026, 0.031, 1)),
                        verts=nudo.verts)
    redondear(nudo, 0.008)
    corbatin = _objeto("Plop_corbatin", bm, col, mat_c)
    _amasar(corbatin, voxel=0.0008, suavizado=3, irregular=0.0006, base_plana=False)
    piezas.append(corbatin)

    _bocas("Plop", raiz, cuerpo, col, 0.0, 0.204 + up, (0.8, 0.9), mats)
    poner_boca(raiz, boca)
    _colocar(raiz, piezas, ubicacion, giro_z)
    return raiz
