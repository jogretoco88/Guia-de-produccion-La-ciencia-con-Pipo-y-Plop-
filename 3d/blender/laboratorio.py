"""El Laboratorio de Pipo y Plop: set modular a escala real del títere (Pipo mide 30 cm).

Todo es plastilina (como dice la guía: gotas, vapor y luz son piezas de arcilla), salvo el
vidrio de los frascos, que es resina transparente como en un set de stop-motion.

Zona central (esta escena): el banco de experimentos, la ventana, los estantes, el muro
de los descubrimientos (una insignia por episodio terminado), el microscopio gigante del
«¡Hagamos zoom!» y el tubo de las preguntas, por donde llega el misterio de cada episodio.
Las demás zonas (cocina, cuerpo, animales, cielo y clima, tierra y espacio, casa) se
construyen con las mismas piezas: ver 3d/README.md.

Uso:
    import laboratorio
    refs = laboratorio.crear_laboratorio()
"""
import math
import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

import arcilla

COL_SET = "Laboratorio"
_mats = {}


def _m(clave, color, **kw):
    """Material de plastilina cacheado por clave (las piezas del set comparten materiales)."""
    if clave not in _mats:
        _mats[clave] = arcilla.plastilina(f"set {clave}", color, **kw)
    return _mats[clave]


def _col():
    col = bpy.data.collections.get(COL_SET)
    if col is None:
        col = bpy.data.collections.new(COL_SET)
        bpy.context.scene.collection.children.link(col)
    return col


def _nuevo(nombre, bm, mat, suave=True):
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = suave
    ob = bpy.data.objects.new(nombre, me)
    _col().objects.link(ob)
    if mat is not None:
        if isinstance(mat, (list, tuple)):
            for x in mat:
                me.materials.append(x)
        else:
            me.materials.append(mat)
    return ob


def _blando(ob, bisel=0.004, nivel=2, irregular=0.0, tam_irregular=0.05):
    """Bordes redondeados de plastilina: bisel + subdivisión, y si se pide, ondulación a mano."""
    if bisel > 0:
        b = ob.modifiers.new("bisel", "BEVEL")
        b.width = bisel
        b.segments = 2
        b.limit_method = "NONE"
    s = ob.modifiers.new("subdivisión", "SUBSURF")
    s.levels = s.render_levels = nivel
    if irregular > 0:
        tex = bpy.data.textures.new(f"ondulado_{ob.name}", "CLOUDS")
        tex.noise_scale = tam_irregular
        d = ob.modifiers.new("hecho a mano", "DISPLACE")
        d.texture = tex
        d.texture_coords = "GLOBAL"
        d.strength = irregular
    return ob


def caja(nombre, centro, tam, mat, bisel=0.004, rot=(0, 0, 0), irregular=0.0, nivel=2, tam_irregular=0.05):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    M = Matrix.Translation(centro) @ Euler(rot).to_matrix().to_4x4() @ Matrix.Diagonal((*tam, 1))
    bmesh.ops.transform(bm, matrix=M, verts=bm.verts)
    return _blando(_nuevo(nombre, bm, mat), bisel=bisel, irregular=irregular, nivel=nivel,
                   tam_irregular=tam_irregular)


def cilindro(nombre, a, b, radio, mat, bisel=0.003, segs=40, radio2=None, nivel=2):
    """Cilindro (o tronco de cono si radio2) de a a b."""
    a, b = Vector(a), Vector(b)
    eje = b - a
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs,
                          radius1=radio, radius2=radio if radio2 is None else radio2, depth=eje.length)
    rot = Vector((0, 0, 1)).rotation_difference(eje.normalized()).to_matrix().to_4x4()
    bmesh.ops.transform(bm, matrix=Matrix.Translation((a + b) / 2) @ rot, verts=bm.verts)
    return _blando(_nuevo(nombre, bm, mat), bisel=bisel, nivel=nivel)


def esfera(nombre, centro, radios, mat, segs=32, anillos=20, rot=(0, 0, 0)):
    if isinstance(radios, (int, float)):
        radios = (radios,) * 3
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=anillos, radius=1.0)
    M = Matrix.Translation(centro) @ Euler(rot).to_matrix().to_4x4() @ Matrix.Diagonal((*radios, 1))
    bmesh.ops.transform(bm, matrix=M, verts=bm.verts)
    return _nuevo(nombre, bm, mat)


def torno(nombre, perfil, centro, mat, segs=48, grosor=0.0):
    """Pieza de revolución a partir de un perfil [(radio, altura), ...] (frascos, macetas)."""
    bm = bmesh.new()
    vs = [bm.verts.new((r, 0, z)) for r, z in perfil]
    for v0, v1 in zip(vs, vs[1:]):
        bm.edges.new((v0, v1))
    bmesh.ops.spin(bm, geom=bm.verts[:] + bm.edges[:], cent=(0, 0, 0), axis=(0, 0, 1),
                   angle=2 * math.pi, steps=segs, use_duplicate=False)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.translate(bm, vec=Vector(centro), verts=bm.verts)
    ob = _nuevo(nombre, bm, mat)
    if grosor > 0:
        so = ob.modifiers.new("grosor", "SOLIDIFY")
        so.thickness = grosor
        so.offset = 0.0
    s = ob.modifiers.new("subdivisión", "SUBSURF")
    s.levels = s.render_levels = 1
    return ob


def toro(nombre, centro, R, r, mat, rot=(0, 0, 0), aplastar=1.0, segs=64, lados=16):
    """Aro (toro) de radio mayor R y grosor r; aplastar < 1 lo achata a lo largo de su eje."""
    bm = bmesh.new()
    circ = [bm.verts.new((R + r * math.cos(t), 0, r * math.sin(t) * aplastar))
            for t in (2 * math.pi * i / lados for i in range(lados))]
    for a, b in zip(circ, circ[1:] + circ[:1]):
        bm.edges.new((a, b))
    bmesh.ops.spin(bm, geom=bm.verts[:] + bm.edges[:], cent=(0, 0, 0), axis=(0, 0, 1), angle=2 * math.pi, steps=segs)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(centro) @ Euler(rot).to_matrix().to_4x4(), verts=bm.verts)
    return _nuevo(nombre, bm, mat)


# ------------------------------------------------------------------ piezas del set

def suelo_y_paredes():
    crema = _m("baldosa crema", "#F2E4C6", huellas=0.6, boil=0.0, escala_huella=1.4)
    melocoton = _m("baldosa melocotón", "#E7AE86", huellas=0.6, boil=0.0, escala_huella=1.4, semilla=4)
    junta = _m("junta", "#C9B79A", huellas=0.2, boil=0.0, poros=0.3)
    caja("junta del suelo", (0, -0.2, -0.004), (2.6, 1.6, 0.008), junta, bisel=0.0, nivel=0)
    # Baldosas: cada una con un leve desnivel y giro, como cortadas a mano.
    bm = bmesh.new()
    lado = 0.12
    import random
    rnd = random.Random(7)
    for i in range(-11, 11):
        for j in range(-8, 5):
            c = Vector(((i + 0.5) * lado, (j + 0.5) * lado + 0.07, 0.003 + rnd.uniform(-0.0012, 0.0012)))
            t = bmesh.ops.create_cube(bm, size=1.0)
            vs = t["verts"]
            M = (Matrix.Translation(c) @ Matrix.Rotation(rnd.uniform(-0.02, 0.02), 4, "Z")
                 @ Matrix.Diagonal((lado - 0.006, lado - 0.006, 0.01, 1)))
            bmesh.ops.transform(bm, matrix=M, verts=vs)
            idx = (i + j) % 2
            for f in {f for v in vs for f in v.link_faces}:
                f.material_index = idx
    baldosas = _nuevo("baldosas", bm, [crema, melocoton])
    _blando(baldosas, bisel=0.0035, nivel=1)

    pared = _m("pared azul", "#93CBEC", huellas=0.5, boil=0.0, escala_huella=1.8, bultos=1.2)
    zocalo = _m("zócalo", "#4E9BCB", huellas=0.6, boil=0.0, escala_huella=1.5, semilla=2)
    moldura = _m("moldura crema", "#F4EAD3", huellas=0.5, boil=0.0, semilla=6)
    caja("pared del fondo", (0, 0.58, 0.55), (2.6, 0.06, 1.2), pared, bisel=0.01, irregular=0.0015, tam_irregular=0.12)
    caja("zócalo", (0, 0.545, 0.1), (2.6, 0.02, 0.2), zocalo, bisel=0.004, irregular=0.0008)
    cilindro("moldura", (-1.3, 0.54, 0.205), (1.3, 0.54, 0.205), 0.011, moldura, segs=20)


def ventana(centro=(0.02, 0.548, 0.5), radio=0.15):
    """Ventana redonda con cielo de plastilina y dos nubes (un telón pintado, como en un set real)."""
    cx, cy, cz = centro
    cielo = arcilla.emisivo("cielo", "#9ED6F5", fuerza=1.4)
    esfera("cielo", (cx, cy + 0.004, cz), (radio, 0.004, radio), cielo, segs=64, anillos=16)
    nube = _m("nube", "#FFFFFF", huellas=0.5, boil=0.2, rugosidad=0.6)
    for dx, dz, s in ((-0.06, 0.03, 1.0), (0.05, -0.04, 0.8)):
        for k, (ox, oz, r) in enumerate(((0, 0, 0.026), (0.028, 0.006, 0.02), (-0.026, 0.002, 0.018), (0.01, 0.018, 0.019))):
            esfera(f"nube_{dx}_{k}", (cx + dx + ox * s, cy - 0.004, cz + dz + oz * s), (r * s, 0.01 * s, r * s * 0.85), nube)
    marco = _m("marco ventana", "#F08A4B", huellas=0.8, boil=0.2, semilla=3)
    toro("marco de la ventana", centro, radio + 0.012, 0.024, marco, rot=(math.pi / 2, 0, 0), aplastar=0.6)
    for t in (0, math.pi / 2):                                        # cruz del marco
        d = Vector((math.cos(t), 0, math.sin(t))) * radio
        cilindro(f"travesaño_{t:.1f}", Vector(centro) - d + Vector((0, -0.006, 0)), Vector(centro) + d + Vector((0, -0.006, 0)), 0.007, marco, segs=16)


def estantes(x0=-0.82, x1=-0.36, y=0.53):
    """Dos estantes con frascos de colores, una maceta y una molécula de agua de bolitas."""
    madera = _m("madera", "#C27A45", huellas=0.8, boil=0.15, semilla=8)
    vidrio = arcilla.vidrio("vidrio")
    for z in (0.36, 0.54):
        caja(f"estante_{z}", ((x0 + x1) / 2, y - 0.06, z), (x1 - x0, 0.12, 0.018), madera, bisel=0.004)
        for x in (x0 + 0.05, x1 - 0.05):
            caja(f"escuadra_{z}_{x:.2f}", (x, y - 0.015, z - 0.035), (0.014, 0.03, 0.05), madera, bisel=0.003)
    colores = ["#E8505B", "#F7C548", "#5BC0EB", "#9BC53D", "#B48EE0", "#FF8C42"]
    frascos = [(-0.79, 0.36, 0.05, 0.09, 0), (-0.72, 0.36, 0.035, 0.065, 1), (-0.655, 0.36, 0.04, 0.11, 2),
               (-0.585, 0.36, 0.03, 0.07, 3), (-0.79, 0.54, 0.035, 0.08, 4), (-0.735, 0.54, 0.03, 0.06, 5)]
    for i, (x, z, r, h, c) in enumerate(frascos):
        base = z + 0.009
        perfil = [(0.0, 0.0), (r * 0.92, 0.0), (r, r * 0.12), (r, h * 0.82), (r * 0.62, h * 0.92), (r * 0.6, h)]
        torno(f"frasco_{i}", perfil, (x, y - 0.06, base), vidrio, grosor=0.0015)
        liquido = _m(f"líquido {c}", colores[c], huellas=0.25, boil=0.25, rugosidad=0.22, sss=0.2)
        torno(f"líquido_{i}", [(0, 0.002), (r * 0.86, 0.002), (r * 0.9, 0.01), (r * 0.9, h * 0.58), (0, h * 0.6)],
              (x, y - 0.06, base), liquido)
        tapa = _m("tapa corcho", "#B98B5E", huellas=0.7, boil=0.1)
        cilindro(f"tapa_{i}", (x, y - 0.06, base + h - 0.004), (x, y - 0.06, base + h + 0.012), r * 0.62, tapa, segs=24)
    # Molécula de agua: oxígeno rojo y dos hidrógenos blancos (como las de bolitas del colegio).
    ox = Vector((-0.63, y - 0.06, 0.6))
    esfera("oxígeno", ox, 0.03, _m("oxígeno", "#E2463F", huellas=1.0, boil=0.3))
    for s in (-1, 1):
        h = ox + Vector((s * 0.045, -0.005, -0.03))
        cilindro(f"enlace_{s}", ox, h, 0.006, _m("enlace", "#9AA3AB", huellas=0.3, boil=0.1))
        esfera(f"hidrógeno_{s}", h, 0.019, _m("hidrógeno", "#F5F2EA", huellas=1.0, boil=0.3))
    # Maceta con planta.
    maceta = _m("maceta", "#C8643B", huellas=0.9, boil=0.2)
    torno("maceta", [(0, 0), (0.03, 0), (0.038, 0.05), (0.042, 0.055), (0.042, 0.062), (0, 0.062)], (-0.5, y - 0.06, 0.549), maceta)
    hoja = _m("hoja", "#3FA34D", huellas=0.9, boil=0.3)
    for k, (dx, dz, ry) in enumerate(((-0.025, 0.1, -0.5), (0.03, 0.11, 0.6), (0.0, 0.13, 0.0), (-0.012, 0.085, -1.1), (0.02, 0.09, 1.0))):
        esfera(f"hoja_{k}", (-0.5 + dx, y - 0.06, 0.549 + dz), (0.014, 0.006, 0.03), hoja, rot=(0, ry, 0))


def banco(x=-0.48, y=0.14):
    """Banco de experimentos: matraz que burbujea, gradilla con tubos y un tazón de palomitas."""
    madera = _m("madera", "#C27A45", huellas=0.8, boil=0.15, semilla=8)
    tapa_banco = _m("tapa del banco", "#F4EAD3", huellas=0.8, boil=0.15, semilla=11)
    h = 0.165
    caja("tablero", (x, y, h - 0.012), (0.44, 0.25, 0.024), tapa_banco, bisel=0.006, irregular=0.0006)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cilindro(f"pata_{sx}_{sy}", (x + sx * 0.19, y + sy * 0.09, 0), (x + sx * 0.19, y + sy * 0.09, h - 0.02), 0.014, madera, segs=20)
    caja("travesaño del banco", (x, y + 0.09, 0.05), (0.38, 0.012, 0.02), madera, bisel=0.003)

    vidrio = arcilla.vidrio("vidrio")
    top = h
    # Soporte y matraz de fondo redondo.
    metal = _m("soporte", "#5A6B78", huellas=0.4, boil=0.05, rugosidad=0.4)
    mx, my = x - 0.09, y + 0.03
    cilindro("base del soporte", (mx, my + 0.04, top), (mx, my + 0.04, top + 0.008), 0.045, metal, segs=32)
    cilindro("varilla", (mx, my + 0.07, top), (mx, my + 0.07, top + 0.2), 0.0045, metal, segs=12)
    perfil = [(0.0, 0.0)] + [(0.052 * math.sin(a), 0.052 - 0.052 * math.cos(a)) for a in [i * math.pi / 18 for i in range(1, 16)]]
    perfil += [(0.016, 0.104), (0.016, 0.16), (0.019, 0.165)]
    base_m = top + 0.03
    torno("matraz", perfil, (mx, my, base_m), vidrio, grosor=0.0015, segs=48)
    verde = _m("líquido verde", "#7ED957", huellas=0.2, boil=0.4, rugosidad=0.2, sss=0.25)
    perfil_l = [(0.0, 0.003)] + [(0.0485 * math.sin(a), 0.052 - 0.0485 * math.cos(a)) for a in [i * math.pi / 18 for i in range(1, 9)]] + [(0.0, 0.052 - 0.0485 * math.cos(8 * math.pi / 18))]
    torno("líquido del matraz", perfil_l, (mx, my, base_m), verde)
    toro("aro del soporte", (mx, my, base_m + 0.035), 0.05, 0.004, metal)
    cilindro("brazo del aro", (mx, my + 0.05, base_m + 0.035), (mx, my + 0.07, base_m + 0.035), 0.003, metal, segs=10, bisel=0.0)
    # Burbujas de plastilina subiendo del matraz (todo es arcilla: también las burbujas).
    burbuja = _m("burbuja", "#E9FBE0", huellas=0.4, boil=0.5, rugosidad=0.35, sss=0.3)
    for k, (dx, dz, r) in enumerate(((0.004, 0.19, 0.009), (-0.006, 0.215, 0.007), (0.007, 0.24, 0.0055), (-0.002, 0.262, 0.0045), (0.006, 0.282, 0.0035))):
        esfera(f"burbuja_{k}", (mx + dx, my, base_m + dz - 0.01), r, burbuja)
    # Gradilla con tres tubos de ensayo.
    gx = x + 0.1
    caja("gradilla", (gx, y + 0.05, top + 0.035), (0.13, 0.04, 0.012), madera, bisel=0.003)
    for sx in (-1, 1):
        caja(f"gradilla_lado_{sx}", (gx + sx * 0.062, y + 0.05, top + 0.02), (0.008, 0.04, 0.04), madera, bisel=0.002)
    for k, c in enumerate(("#E8505B", "#F7C548", "#5BC0EB")):
        tx = gx - 0.04 + k * 0.04
        torno(f"tubo_{k}", [(0, 0.0), (0.008, 0.002), (0.011, 0.012), (0.011, 0.11), (0.012, 0.112)], (tx, y + 0.05, top + 0.004), vidrio, grosor=0.001, segs=24)
        torno(f"líquido_tubo_{k}", [(0, 0.004), (0.009, 0.012), (0.009, 0.05 + 0.012 * k), (0, 0.05 + 0.012 * k)], (tx, y + 0.05, top + 0.004),
              _m(f"tubo {c}", c, huellas=0.2, boil=0.3, rugosidad=0.22, sss=0.2), segs=24)
    # Tazón de palomitas (guiño al Ep. 1).
    tazon = _m("tazón", "#E8505B", huellas=0.9, boil=0.2)
    bx, by = x + 0.12, y - 0.065
    torno("tazón", [(0, 0), (0.03, 0), (0.05, 0.025), (0.055, 0.038), (0.05, 0.038), (0.045, 0.026), (0.026, 0.006), (0, 0.006)], (bx, by, top), tazon)
    palomita = _m("palomita", "#FFF3D6", huellas=1.0, boil=0.4, semilla=12)
    import random
    rnd = random.Random(3)
    for k in range(16):
        a, rr = rnd.uniform(0, 2 * math.pi), rnd.uniform(0, 0.04)
        esfera(f"palomita_{k}", (bx + rr * math.cos(a), by + rr * math.sin(a), top + 0.036 + rnd.uniform(0, 0.022)),
               (0.011, 0.01, 0.009), palomita, rot=(rnd.uniform(0, 3), rnd.uniform(0, 3), 0), segs=16, anillos=10)
    for k, (px, py) in enumerate(((x + 0.21, y - 0.17), (x + 0.33, y - 0.26), (0.06, -0.32))):
        esfera(f"palomita_suelo_{k}", (px, py, 0.009), (0.011, 0.01, 0.009), palomita, rot=(k, 2 * k, 0), segs=16, anillos=10)


def lampara(x=-0.5, y=0.12, z=0.62):
    """Lámpara colgante sobre el banco: pantalla naranja y bombilla cálida (con luz real)."""
    pantalla = _m("pantalla", "#F08A4B", huellas=0.8, boil=0.2, semilla=13)
    torno("pantalla", [(0.012, 0.075), (0.02, 0.07), (0.075, 0.012), (0.08, 0.0), (0.074, 0.0), (0.069, 0.008), (0.016, 0.064), (0.012, 0.075)], (x, y, z), pantalla, segs=48)
    cilindro("cordón", (x, y, z + 0.07), (x, y, 1.3), 0.0025, _m("cordón", "#3B3B3B", huellas=0.1, boil=0.0), segs=8, bisel=0.0)
    esfera("bombilla", (x, y, z + 0.01), 0.022, arcilla.emisivo("bombilla", "#FFD9A0", fuerza=8.0))
    d = bpy.data.lights.new("luz de la lámpara", "POINT")
    d.energy = 3.0
    d.color = (1.0, 0.82, 0.6)
    d.shadow_soft_size = 0.02
    ob = bpy.data.objects.new("luz de la lámpara", d)
    _col().objects.link(ob)
    ob.location = (x, y, z - 0.005)


def tubo_curvo(nombre, puntos, radio, mat):
    """Tubo liso que sigue una curva (brazos, cables, mangueras)."""
    cu = bpy.data.curves.new(nombre, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radio
    cu.bevel_resolution = 8
    cu.use_fill_caps = True
    sp = cu.splines.new("NURBS")
    sp.points.add(len(puntos) - 1)
    for pt, c in zip(sp.points, puntos):
        pt.co = (*c, 1.0)
    sp.use_endpoint_u = True
    sp.order_u = 3
    sp.resolution_u = 24
    ob = bpy.data.objects.new(nombre, cu)
    _col().objects.link(ob)
    cu.materials.append(mat)
    return ob


def microscopio(x=0.5, y=0.17):
    """El microscopio gigante del «¡Hagamos zoom!»: más alto que Plop. Plop viene del mundo
    microscópico (se parece a un tardígrado), así que este es su portal a casa.
    Se ve de perfil (la silueta clásica), con el ocular inclinado hacia Plop."""
    crema = _m("microscopio crema", "#F4EAD3", huellas=0.9, boil=0.2, semilla=14)
    rojo = _m("microscopio rojo", "#D6453D", huellas=0.9, boil=0.2, semilla=15)
    gris = _m("objetivos", "#8E9AA6", huellas=0.5, boil=0.1, rugosidad=0.35)
    negro = _m("ocular", "#2B2F36", huellas=0.4, boil=0.1)
    caja("base del microscopio", (x, y, 0.024), (0.21, 0.15, 0.048), crema, bisel=0.016, irregular=0.0008)
    # Brazo en C, de la parte trasera de la base hasta el cabezal, curvado hacia Plop.
    tubo_curvo("brazo del microscopio", [(x + 0.075, y, 0.03), (x + 0.085, y, 0.2), (x + 0.07, y, 0.36),
                                         (x + 0.02, y, 0.44)], 0.03, rojo)
    caja("cabezal", (x + 0.005, y, 0.43), (0.075, 0.07, 0.07), rojo, bisel=0.02)
    cilindro("tubo del ocular", (x - 0.02, y, 0.45), (x - 0.075, y, 0.53), 0.021, crema, segs=32)
    cilindro("ocular", (x - 0.075, y, 0.53), (x - 0.083, y, 0.543), 0.024, negro, segs=32)
    cilindro("tubo del cuerpo", (x - 0.025, y, 0.41), (x - 0.035, y, 0.35), 0.025, crema, segs=32)
    cilindro("revólver", (x - 0.033, y, 0.352), (x - 0.036, y, 0.334), 0.036, crema, segs=40)
    for k, ang in enumerate((0.0, 0.5, -0.5)):
        a = Vector((x - 0.036 + 0.012 * math.sin(ang), y + 0.012 * math.sin(ang * 2), 0.334))
        b = a + Vector((0.035 * math.sin(ang), 0.0, -0.045 * math.cos(ang) if k == 0 else -0.032))
        cilindro(f"objetivo_{k}", a, b, 0.0105, gris, segs=20, radio2=0.0078)
    caja("platina", (x - 0.03, y, 0.235), (0.13, 0.13, 0.014), rojo, bisel=0.004)
    caja("soporte de la platina", (x + 0.045, y, 0.235), (0.05, 0.05, 0.014), rojo, bisel=0.004)
    caja("portaobjetos", (x - 0.035, y - 0.01, 0.244), (0.065, 0.024, 0.003), arcilla.vidrio("vidrio"), bisel=0.0005, nivel=1)
    esfera("muestra", (x - 0.035, y - 0.01, 0.2465), (0.007, 0.007, 0.0016), _m("muestra", "#7ED957", huellas=0.2, boil=0.6))
    cilindro("perilla grande", (x + 0.078, y - 0.03, 0.16), (x + 0.078, y - 0.055, 0.16), 0.03, crema, segs=40)
    cilindro("perilla chica", (x + 0.078, y - 0.055, 0.16), (x + 0.078, y - 0.07, 0.16), 0.018, crema, segs=32)
    cilindro("lámpara del zoom", (x - 0.03, y, 0.048), (x - 0.03, y, 0.078), 0.028, crema, segs=32)
    esfera("luz del zoom", (x - 0.03, y, 0.08), (0.022, 0.022, 0.006), arcilla.emisivo("luz del zoom", "#FFF1B8", fuerza=6.0))


def tubo_preguntas(x=0.74, y=0.42):
    """Tubo neumático por donde llega la pregunta de cada episodio: «fsss... ¡plop!»."""
    vidrio = arcilla.vidrio("vidrio")
    amarillo = _m("buzón", "#F7C548", huellas=0.9, boil=0.2, semilla=16)
    naranja = _m("anillos del tubo", "#F08A4B", huellas=0.7, boil=0.2)
    caja("buzón de preguntas", (x, y, 0.1), (0.13, 0.13, 0.2), amarillo, bisel=0.015, irregular=0.0008)
    caja("boca del buzón", (x, y - 0.066, 0.13), (0.08, 0.004, 0.05), _m("hueco", "#3A2A20", huellas=0.2, boil=0.0), bisel=0.004)
    torno("tubo neumático", [(0.0345, 0.0), (0.0365, 0.0), (0.0365, 1.1), (0.0345, 1.1), (0.0345, 0.0)], (x, y, 0.2), vidrio, segs=40)
    for k, z in enumerate((0.22, 0.42, 0.62, 0.82, 1.02)):
        cilindro(f"anillo_tubo_{k}", (x, y, z), (x, y, z + 0.02), 0.042, naranja, segs=40)
    capsula = _m("cápsula", "#E8505B", huellas=0.8, boil=0.3)
    cilindro("cápsula", (x, y, 0.5), (x, y, 0.57), 0.026, capsula, segs=32, bisel=0.012)
    cilindro("banda de la cápsula", (x, y, 0.53), (x, y, 0.54), 0.0272, _m("banda", "#F4EAD3", huellas=0.5, boil=0.2), segs=32)


def muro_descubrimientos(centro=(0.36, 0.548, 0.6), radio=0.13):
    """Muro de los descubrimientos: una insignia por episodio terminado (sin texto: solo
    iconos). Se llena a lo largo de la temporada, como un álbum de cromos."""
    cx, cy, cz = centro
    corcho = _m("corcho", "#D4A373", huellas=0.7, boil=0.1, escala_huella=1.3)
    cilindro("tablero de corcho", (cx, cy + 0.004, cz), (cx, cy - 0.012, cz), radio, corcho, segs=64, bisel=0.005)
    marco = _m("marco del tablero", "#C27A45", huellas=0.7, boil=0.1)
    toro("marco del muro", (cx, cy - 0.012, cz), radio, 0.007, marco, rot=(math.pi / 2, 0, 0))

    insignias = [((-0.05, 0.05), "#E8505B", "palomitas"), ((0.05, 0.05), "#B48EE0", "jabón"),
                 ((-0.05, -0.05), "#F7C548", "ají"), ((0.05, -0.05), "#5BC0EB", "hipo")]
    yb = cy - 0.016
    for (dx, dz), color, tema in insignias:
        p = Vector((cx + dx, yb, cz + dz))
        cilindro(f"insignia {tema}", p + Vector((0, 0.004, 0)), p - Vector((0, 0.004, 0)), 0.034,
                 _m(f"insignia {color}", color, huellas=1.0, boil=0.2), segs=40, bisel=0.003)
        f = p - Vector((0, 0.008, 0))
        if tema == "palomitas":
            m = _m("palomita", "#FFF3D6", huellas=1.0, boil=0.4, semilla=12)
            for ox, oz, r in ((0, 0.004, 0.011), (-0.01, -0.006, 0.009), (0.01, -0.005, 0.009), (0.0, -0.012, 0.008)):
                esfera(f"icono palomita {ox}{oz}", f + Vector((ox, 0, oz)), (r, 0.006, r), m)
        elif tema == "jabón":
            m = _m("pompa", "#E8F6FF", huellas=0.3, boil=0.2, rugosidad=0.15, sss=0.3)
            esfera("icono pompa grande", f + Vector((-0.004, 0, 0.004)), (0.014, 0.008, 0.014), m)
            esfera("icono pompa chica", f + Vector((0.013, 0, -0.012)), (0.007, 0.006, 0.007), m)
        elif tema == "ají":
            m = _m("ají", "#D7263D", huellas=0.9, boil=0.3)
            for k in range(6):
                t = k / 5
                esfera(f"icono ají {k}", f + Vector((-0.014 + 0.028 * t, 0, 0.01 - 0.024 * t * t)), (0.008 * (1 - 0.6 * t), 0.006, 0.008 * (1 - 0.6 * t)), m)
            esfera("icono rabito", f + Vector((-0.017, 0, 0.014)), (0.004, 0.004, 0.006), _m("rabito", "#3FA34D", huellas=0.5, boil=0.2))
        else:
            m = _m("globo", "#FF7EB6", huellas=0.6, boil=0.3, rugosidad=0.3)
            esfera("icono globo", f + Vector((0, 0, 0.006)), (0.012, 0.007, 0.014), m)
            cilindro("icono hilo", f + Vector((0, 0, -0.008)), f + Vector((0.002, 0, -0.022)), 0.0012, _m("hilo", "#F4EAD3", huellas=0.0, boil=0.0), segs=8, bisel=0.0)
    for k, (dx, dz) in enumerate(((0.0, 0.1), (-0.095, 0.0), (0.095, 0.0), (0.0, -0.1))):    # huecos para lo que viene
        p = Vector((cx + dx, yb + 0.006, cz + dz))
        cilindro(f"hueco_{k}", p + Vector((0, 0.002, 0)), p - Vector((0, 0.002, 0)), 0.022,
                 _m("hueco de insignia", "#B8885A", huellas=0.6, boil=0.0), segs=32, bisel=0.002)


def crear_laboratorio():
    """Construye la zona central completa."""
    _mats.clear()
    suelo_y_paredes()
    ventana()
    estantes()
    banco()
    lampara()
    microscopio()
    tubo_preguntas()
    muro_descubrimientos()
    # El vidrio no proyecta sombra: así los líquidos de dentro reciben luz (truco habitual).
    for ob in _col().objects:
        if ob.type == "MESH" and any(m and m.name == "vidrio" for m in ob.data.materials):
            ob.visible_shadow = False
    return _col()
