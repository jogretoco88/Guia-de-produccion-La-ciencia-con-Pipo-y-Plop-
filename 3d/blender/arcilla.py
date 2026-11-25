"""Plastilina procedural para Blender 5.2 LTS (Cycles y EEVEE).

Cada material lleva:
  - huellas dactilares: grupos de crestas concéntricas, como pulgares apretados en la arcilla,
    en varias capas con orientaciones distintas;
  - irregularidades de modelado a mano (bultos suaves) y poros diminutos más oscuros;
  - "boiling": una capa de huellas que cambia cada 2 fotogramas, como cuando el animador
    toca el títere entre foto y foto. Se regula con `boil` (0 = sin boiling).

Las medidas están en metros a escala real del títere (Pipo y Plop miden unos 30 cm),
así las huellas tienen el mismo tamaño en todos los planos.

Uso:
    import arcilla
    mat = arcilla.plastilina("Pipo piel", arcilla.COLORES["pipo"])
    objeto.data.materials.append(mat)

Para personajes con esqueleto usa coords="rest" y activa en el objeto
`objeto.add_rest_position_attribute = True`: la textura no "nada" al deformarse.
"""
import math
import bpy

# Paleta del canal (sRGB): calibrada para que el render coincida con las láminas 8K de Pipo y Plop.
COLORES = {
    "pipo": "#096B7C",        # turquesa azulado
    "chaleco": "#D08316",     # mostaza
    "boton": "#F2EEE4",       # blanco hueso
    "plop": "#578B27",        # verde hierba
    "corbatin": "#AD410E",    # naranja terracota
    "ojo": "#0B0D12",         # negro brillante
    "globo": "#ECEAE6",       # blanco de los ojos de Pipo
    "esclera": "#EDE1BF",     # aro crema de los ojos de Plop
}


def hex_a_lineal(h, alpha=1.0):
    """'#RRGGBB' (sRGB) -> RGBA lineal, que es lo que esperan los nodos."""
    h = h.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, alpha)


class _Grafo:
    """Atajos para crear y conectar nodos sin repetir código."""

    def __init__(self, nt):
        self.nt = nt
        self.x = -1400

    def nodo(self, tipo, **props):
        n = self.nt.nodes.new(tipo)
        n.location = (self.x, 0)
        self.x += 40
        for k, v in props.items():
            setattr(n, k, v)
        return n

    def unir(self, salida, entrada):
        self.nt.links.new(salida, entrada)

    def mate(self, op, a, b=None, c=None, clamp=False):
        n = self.nodo("ShaderNodeMath", operation=op, use_clamp=clamp)
        for i, v in enumerate((a, b, c)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = v
            else:
                self.unir(v, n.inputs[i])
        return n.outputs[0]

    def vec(self, op, a, b=None, escala=None):
        n = self.nodo("ShaderNodeVectorMath", operation=op)
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (tuple, list)):
                n.inputs[i].default_value = v
            else:
                self.unir(v, n.inputs[i])
        if escala is not None:
            n.inputs[3].default_value = escala
        return n.outputs[0]

    def suave(self, valor, desde, hasta):
        """Map Range en modo smoothstep: 0 en `desde`, 1 en `hasta`."""
        n = self.nodo("ShaderNodeMapRange", interpolation_type="SMOOTHSTEP", clamp=True)
        self.unir(valor, n.inputs["Value"])
        n.inputs[1].default_value = desde
        n.inputs[2].default_value = hasta
        return n.outputs["Result"]


def _capa_huellas(g, P, *, tam, periodo, aniso, desfase, densidad, w=None):
    """Una capa de huellas: en cada celda de Voronoi, crestas concéntricas alrededor de un
    centro desplazado al azar. Como el centro cae cerca del borde, dentro de la celda se ven
    arcos paralelos (una yema apretada de lado), no dianas perfectas.

    tam      tamaño de cada huella (m)
    periodo  distancia entre crestas (m); en la plastilina real ~0,5 mm, aquí exagerado
             a ~1,3 mm para que se lean en pantalla como en las láminas del canal
    aniso    estiramiento (x, y, z) para que las huellas sean ovaladas
    densidad fracción de celdas que llevan huella (0-1)
    w        socket para el modo 4D (boiling) o None
    """
    q = g.vec("MULTIPLY", P, aniso)
    q = g.vec("ADD", q, desfase)
    vor = g.nodo("ShaderNodeTexVoronoi", voronoi_dimensions="4D" if w is not None else "3D",
                 feature="F1", distance="EUCLIDEAN")
    vor.inputs["Scale"].default_value = 1.0 / tam
    vor.inputs["Randomness"].default_value = 1.0
    g.unir(q, vor.inputs["Vector"])
    if w is not None:
        g.unir(w, vor.inputs["W"])
    rnd = g.nodo("ShaderNodeSeparateColor")
    g.unir(vor.outputs["Color"], rnd.inputs[0])
    # Centro de las crestas: el punto de la celda desplazado hasta ~0,45 del tamaño.
    desp = g.vec("SUBTRACT", vor.outputs["Color"], (0.5, 0.5, 0.5))
    centro = g.vec("ADD", vor.outputs["Position"], g.vec("SCALE", desp, escala=tam * 0.95))
    r = g.vec("DISTANCE", q, centro).node.outputs["Value"]
    fase = g.mate("MULTIPLY", rnd.outputs[2], 6.283)
    anillos = g.mate("MULTIPLY_ADD", r, 2 * math.pi / periodo, fase)
    cresta = g.mate("MULTIPLY_ADD", g.mate("SINE", anillos), 0.5, 0.5)
    # La huella ocupa el interior de su celda y se desvanece hacia el borde.
    borde = g.suave(vor.outputs["Distance"], 0.5, 0.16)
    activa = g.mate("GREATER_THAN", rnd.outputs[0], 1.0 - densidad)
    fuerza = g.mate("MULTIPLY_ADD", rnd.outputs[1], 0.55, 0.45)   # cada huella con su profundidad
    mascara = g.mate("MULTIPLY", g.mate("MULTIPLY", borde, activa), fuerza)
    return g.mate("MULTIPLY", cresta, mascara), mascara


def _capa_alisado(g, P, *, periodo, escala_zonas=14.0, cobertura=0.45):
    """Marcas de alisado: líneas finas onduladas donde el dedo arrastró la plastilina."""
    ond = g.nodo("ShaderNodeTexWave", wave_type="BANDS", bands_direction="DIAGONAL", wave_profile="SIN")
    ond.inputs["Scale"].default_value = 1.0 / (periodo * 20.0)
    ond.inputs["Distortion"].default_value = 6.0
    ond.inputs["Detail"].default_value = 2.0
    ond.inputs["Detail Scale"].default_value = 0.6
    g.unir(P, ond.inputs["Vector"])
    zonas = g.nodo("ShaderNodeTexNoise")
    zonas.inputs["Scale"].default_value = escala_zonas
    zonas.inputs["Detail"].default_value = 1.0
    g.unir(P, zonas.inputs["Vector"])
    m = g.suave(zonas.outputs["Factor"], 0.62 - cobertura * 0.2, 0.7)
    return g.mate("MULTIPLY", ond.outputs["Factor"], m), m


def plastilina(nombre, color, *, huellas=1.0, boil=0.35, rugosidad=0.52, sss=0.06,
               bultos=1.0, poros=1.0, coords="object", semilla=0.0, escala_huella=1.0):
    """Crea (o reemplaza) un material de plastilina.

    color          '#RRGGBB' o RGBA lineal
    huellas        intensidad de las huellas (0 = liso)
    boil           intensidad de la capa que cambia cada 2 fotogramas
    rugosidad      0,45-0,6 es plastilina mate con un brillo suave
    sss            dispersión bajo la superficie (la plastilina es casi opaca: 0,03-0,1)
    coords         "object" para props fijos, "rest" para personajes con esqueleto
    semilla        desplaza el patrón para que dos objetos del mismo color no repitan huellas
    escala_huella  >1 huellas más grandes (para props gigantes), <1 más finas
    """
    rgba = hex_a_lineal(color) if isinstance(color, str) else color
    mat = bpy.data.materials.get(nombre) or bpy.data.materials.new(nombre)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    g = _Grafo(nt)

    # Coordenadas en metros, fijas al objeto.
    if coords == "rest":
        attr = g.nodo("ShaderNodeAttribute", attribute_name="rest_position")
        P0 = attr.outputs["Vector"]
    else:
        P0 = g.nodo("ShaderNodeTexCoord").outputs["Object"]
    P = g.vec("ADD", P0, (semilla * 1.37, semilla * 2.11, semilla * 0.73))

    # Ondulación fina: las crestas de una huella real no son círculos perfectos.
    nd = g.nodo("ShaderNodeTexNoise")
    nd.inputs["Scale"].default_value = 160.0 / escala_huella
    nd.inputs["Detail"].default_value = 2.0
    g.unir(P, nd.inputs["Vector"])
    onda = g.vec("SCALE", g.vec("SUBTRACT", nd.outputs["Color"], (0.5, 0.5, 0.5)), escala=0.0026 * escala_huella)
    Pd = g.vec("ADD", P, onda)

    tam = 0.024 * escala_huella
    per = 0.0015 * escala_huella
    h1, m1 = _capa_huellas(g, Pd, tam=tam, periodo=per, aniso=(1.0, 1.0, 1.7),
                           desfase=(0.0, 0.0, 0.0), densidad=0.85)
    h2, m2 = _capa_huellas(g, Pd, tam=tam * 1.15, periodo=per, aniso=(1.7, 1.0, 1.0),
                           desfase=(3.3, 1.7, 5.1), densidad=0.72)
    h4, m4 = _capa_alisado(g, Pd, periodo=per * 0.85, cobertura=0.65)
    huellas_fijas = g.mate("MAXIMUM", g.mate("MAXIMUM", h1, h2), g.mate("MULTIPLY", h4, 0.55))
    mascara_fija = g.mate("MAXIMUM", g.mate("MAXIMUM", m1, m2), g.mate("MULTIPLY", m4, 0.55))

    # Boiling: capa extra cuyo patrón cambia cada 2 fotogramas (a dos, como el stop-motion).
    drv_node = g.nodo("ShaderNodeValue")
    drv_node.label = "boiling (cada 2 fotogramas)"
    fc = drv_node.outputs[0].driver_add("default_value")
    fc.driver.type = "SCRIPTED"
    fc.driver.expression = "floor((frame - 1) / 2) * 0.618"     # cambia en 1, 3, 5... como las poses
    h3, m3 = _capa_huellas(g, Pd, tam=tam * 0.9, periodo=per, aniso=(1.3, 1.6, 1.0),
                           desfase=(7.7, 2.9, 4.4), densidad=0.45, w=drv_node.outputs[0])
    h3 = g.mate("MULTIPLY", h3, boil)
    m3 = g.mate("MULTIPLY", m3, boil)
    capa_huellas = g.mate("MAXIMUM", huellas_fijas, h3)
    mascara = g.mate("MAXIMUM", mascara_fija, m3)

    # Bultos de modelado a mano.
    nb = g.nodo("ShaderNodeTexNoise")
    nb.inputs["Scale"].default_value = 18.0
    nb.inputs["Detail"].default_value = 3.0
    nb.inputs["Roughness"].default_value = 0.45
    g.unir(P, nb.inputs["Vector"])
    bulto = nb.outputs["Factor"]

    # Poros: puntitos aislados (polvo y burbujas de aire de la plastilina).
    vp = g.nodo("ShaderNodeTexVoronoi", feature="F1")
    vp.inputs["Scale"].default_value = 260.0
    g.unir(P, vp.inputs["Vector"])
    sep = g.nodo("ShaderNodeSeparateColor")
    g.unir(vp.outputs["Color"], sep.inputs[0])
    poro = g.mate("MULTIPLY", g.suave(vp.outputs["Distance"], 0.16, 0.0),
                  g.mate("GREATER_THAN", sep.outputs[0], 0.9))

    # Relieve total -> Bump.
    altura = g.mate("MULTIPLY", bulto, 0.9 * bultos)
    altura = g.mate("MULTIPLY_ADD", capa_huellas, 0.5 * huellas, altura)
    altura = g.mate("MULTIPLY_ADD", poro, -0.45 * poros, altura)
    bump = g.nodo("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 1.0
    bump.inputs["Distance"].default_value = 0.0006
    g.unir(altura, bump.inputs["Height"])

    # Color: variación muy leve, surcos de las huellas y poros algo más oscuros.
    var = g.mate("MULTIPLY_ADD", nb.outputs["Factor"], 0.10, 0.95)
    surco = g.mate("MULTIPLY", g.mate("SUBTRACT", 1.0, capa_huellas), mascara)
    osc = g.mate("SUBTRACT", var, g.mate("MULTIPLY", surco, 0.07 * huellas))
    osc = g.mate("SUBTRACT", osc, g.mate("MULTIPLY", poro, 0.35 * poros))
    mix = g.nodo("ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    mix.inputs["Factor"].default_value = 1.0
    mix.inputs[6].default_value = rgba
    g.unir(osc, mix.inputs[7])
    color_final = mix.outputs[2]

    bsdf = g.nodo("ShaderNodeBsdfPrincipled")
    g.unir(color_final, bsdf.inputs["Base Color"])
    rug = g.mate("MULTIPLY_ADD", surco, 0.08, rugosidad)
    g.unir(rug, bsdf.inputs["Roughness"])
    bsdf.inputs["Specular IOR Level"].default_value = 0.42
    bsdf.inputs["Subsurface Weight"].default_value = sss
    bsdf.inputs["Subsurface Radius"].default_value = (1.0, 0.55, 0.35)
    bsdf.inputs["Subsurface Scale"].default_value = 0.004
    bsdf.inputs["Sheen Weight"].default_value = 0.02
    g.unir(bump.outputs["Normal"], bsdf.inputs["Normal"])

    out = g.nodo("ShaderNodeOutputMaterial")
    g.unir(bsdf.outputs[0], out.inputs["Surface"])
    return mat


def brillante(nombre, color, rugosidad=0.04):
    """Ojos de botón y piezas barnizadas: base oscura con capa transparente."""
    mat = bpy.data.materials.get(nombre) or bpy.data.materials.new(nombre)
    mat.use_nodes = True
    b = mat.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = hex_a_lineal(color) if isinstance(color, str) else color
    b.inputs["Roughness"].default_value = rugosidad
    b.inputs["Coat Weight"].default_value = 0.5
    b.inputs["Coat Roughness"].default_value = 0.03
    b.inputs["Specular IOR Level"].default_value = 0.2
    return mat


def vidrio(nombre, tinte="#EAF6F7", rugosidad=0.03):
    """Vidrio de laboratorio (resina transparente, como en los sets de stop-motion)."""
    mat = bpy.data.materials.get(nombre) or bpy.data.materials.new(nombre)
    mat.use_nodes = True
    b = mat.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = hex_a_lineal(tinte)
    b.inputs["Roughness"].default_value = rugosidad
    b.inputs["Transmission Weight"].default_value = 1.0
    b.inputs["IOR"].default_value = 1.45
    # Pared fina: el vidrio no desvía la imagen de lo que hay detrás (más limpio y legible
    # en tubos y frascos pequeños, y más rápido de renderizar).
    if "Thin Wall" in b.inputs:
        b.inputs["Thin Wall"].default_value = True
    return mat


def emisivo(nombre, color, fuerza=3.0):
    """Bombillas y pilotos del laboratorio."""
    mat = bpy.data.materials.get(nombre) or bpy.data.materials.new(nombre)
    mat.use_nodes = True
    b = mat.node_tree.nodes.get("Principled BSDF")
    c = hex_a_lineal(color) if isinstance(color, str) else color
    b.inputs["Base Color"].default_value = c
    b.inputs["Emission Color"].default_value = c
    b.inputs["Emission Strength"].default_value = fuerza
    return mat
