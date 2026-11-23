// Exporta los 52 episodios de src/ a escenas 3D que lee Blender.
// Uso: node 3d/exportar.mjs [-v]
// Salida:
//   3d/escenas/epNN.json  una escena por episodio (tomas, cámara, zona, objetos, movimiento, voz)
//   3d/assets.json        lista maestra de objetos, agrupados por familia y con prioridad
//   3d/resumen.txt        cifras del año para planificar
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(here, "..");
const verbose = process.argv.includes("-v");

/* ---------- carga de los datos de la guía ---------- */
const ctx = vm.createContext({});
const run = f => vm.runInContext(fs.readFileSync(path.join(root, "src", f), "utf8"), ctx, { filename: f });
run("comun.js");
fs.readdirSync(path.join(root, "src", "episodios")).filter(f => /^ep\d+\.js$/.test(f)).sort()
  .forEach(f => run("episodios/" + f));
const get = n => vm.runInContext(n, ctx);
const EP = get("EP").sort((a, b) => a.n - b.n), BANK = get("BANK"), CAM = get("CAM"), BLOCKS = get("BLOCKS");
const cfg = JSON.parse(fs.readFileSync(path.join(here, "config.json"), "utf8"));

const FPS = cfg.render.fps, PASO = cfg.render.animarDeA;
const pad = n => String(n).padStart(2, "0");
const DUR = { C: 8, R: 8, W: 8, T: 4, F: 4 };

/* ---------- movimientos: la acción en inglés se traduce a la biblioteca ---------- */
const MOV = cfg.movimientos;
const movRe = Object.fromEntries(Object.entries(MOV).map(([k, m]) => [k, new RegExp(m.detecta, "i")]));
function movimientos(accion) {
  return Object.keys(MOV).filter(k => movRe[k].test(accion));
}

/* ---------- zonas del laboratorio ---------- */
const ZONAS = cfg.zonas;
const zonaRe = Object.entries(ZONAS).filter(([, z]) => z.detecta).map(([k, z]) => [k, new RegExp(z.detecta, "i")]);
function zonaBase(ep) {
  const texto = Object.values(ep.objs).map(o => o.en).join(" ") + " " + ep.title;
  for (const [k, re] of zonaRe) if (ZONAS[k].prioridad && re.test(texto)) return k;
  return cfg.zonaPorCategoria[ep.cat];
}
function zonaToma(ep, bloque, base, texto) {
  if (bloque === 3 || bloque === 4) return "zoom";            // dentro de las cosas: cámara de zoom
  for (const [k, re] of zonaRe) if (re.test(texto)) return k;   // el texto de la toma manda
  return base;
}

/* ---------- familias de assets ---------- */
const FAM = Object.entries(cfg.familias).map(([k, f]) => [k, new RegExp(f.detecta, "i")]);
const familia = o => (FAM.find(([, re]) => re.test(o.es + " " + o.en)) || ["objeto"])[0];
const norm = s => s.replace(/\s*\(del Ep\. \d+\)/i, "").trim();
const slug = s => norm(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
  .replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "");

/* ---------- reacciones del banco → acciones animadas + voz inventada ---------- */
const IDIOMA = cfg.idioma.reacciones;

/* ---------- exportación ---------- */
const outDir = path.join(here, "escenas");
fs.mkdirSync(outDir, { recursive: true });
const assets = {};
const total = { tomas: 0, porScript: 0, aMano: 0, titere: 0, banco: 0, laminas: 0, segundos: 0, sinMovimiento: [], zonas: {}, movs: {} };

for (const ep of EP) {
  const id = "ep" + pad(ep.n);
  const star = ep.star, co = star === "P" ? "L" : "P";
  const base = zonaBase(ep);
  for (const [k, o] of Object.entries(ep.objs)) {
    const s = slug(o.es);
    const a = assets[s] ||= { id: s, es: norm(o.es), familia: familia(o), en: o.en, ref: o.p, episodios: [], tomas: 0 };
    if (!a.episodios.includes(ep.n)) a.episodios.push(ep.n);
  }
  const objId = k => slug(ep.objs[k].es);

  let bloque = 0, t = 0, clip = 0;
  const tomas = [];
  for (const r of ep.shots) {
    const k = r[0];
    if (k === "#") { bloque++; continue; }
    const dur = k === "S" ? r[1] : DUR[k];
    const toma = { n: tomas.length + 1, bloque, tipo: null, inicio: t, dur, frames: dur * FPS };
    if ("CRW".includes(k)) toma.clip = ++clip;

    if (k === "C") {
      const [, cam, tags, es, escena, accion, voz, marcas = ""] = r;
      const objs = [...tags].filter(x => x !== star).map(objId);
      const conPersonaje = tags.includes(star);
      const movs = movimientos(accion);
      Object.assign(toma, {
        tipo: conPersonaje ? "personaje" : "objetos",
        camara: { codigo: cam, ...cfg.camaras[cam] },
        zona: zonaToma(ep, bloque, base, escena + " " + accion),
        personajes: conPersonaje ? [star] : [],
        objetos: objs,
        movimientos: movs,
        animacion: conPersonaje ? "a_mano" : objs.some(o => assets[o].familia === "animales") ? "titere"
          : (movs.length ? "script" : "a_mano"),
        enPantalla: es, escena, accion,
        narrador: voz,
        bocaAbierta: marcas.includes("o")
      });
      objs.forEach(o => assets[o].tomas++);
      if (toma.animacion === "script") total.porScript++; else if (toma.animacion === "titere") total.titere++; else total.aMano++;
      if (toma.animacion === "a_mano" && !conPersonaje) total.sinMovimiento.push(`${id} C${pad(clip)}: ${accion}`);
      movs.forEach(m => total.movs[m] = (total.movs[m] || 0) + 1);
    } else if (k === "R" || k === "W") {
      const codigo = k === "W" ? star + "10" : r[1];
      const voz = k === "W" ? (r[1] || "") : r[2];
      const b = BANK[codigo];
      Object.assign(toma, {
        tipo: "reaccion",
        camara: { codigo: b[2], ...cfg.camaras[b[2]] },
        zona: zonaToma(ep, bloque, base, ""),
        personajes: [codigo[0]],
        accion: { codigo, nombre: b[0], direccion: b[4] },
        voz: { personaje: codigo[0], ...IDIOMA[codigo] },
        animacion: "biblioteca",
        enPantalla: b[1],
        narrador: voz
      });
      total.banco++;
    } else if (k === "S") {
      const [, secs, tags, es, imagen, voz, rotulos] = r;
      Object.assign(toma, {
        tipo: "lamina", zona: "pizarra", objetos: [...tags].filter(x => x !== star && ep.objs[x]).map(objId),
        camara: { codigo: "W", ...cfg.camaras.W }, animacion: "script", movimientos: ["acercamiento_lento"],
        enPantalla: es, imagen, narrador: voz, rotulos
      });
      total.laminas++;
    } else if (k === "T" || k === "F") {
      Object.assign(toma, { tipo: k === "T" ? "cortinilla" : "tarjeta_final", zona: "entrada",
        personajes: ["P", "L"], animacion: "canal", reutilizable: true });
    }
    if (toma.zona) total.zonas[toma.zona] = (total.zonas[toma.zona] || 0) + 1;
    total.tomas++;
    t += dur;
    tomas.push(toma);
  }
  total.segundos += t;

  const escena = {
    episodio: ep.n, id, titulo: ep.title, tema: ep.topic, categoria: ep.cat,
    protagonista: star, acompanante: co, zonaBase: base,
    render: { ancho: cfg.render.ancho, alto: cfg.render.alto, fps: FPS, animarDeA: PASO, motor: cfg.render.motor },
    duracion: t, frames: t * FPS, framesUnicos: t * FPS / PASO,
    objetos: Object.keys(ep.objs).map(objId),
    efectos: ep.sfx.map(([es, en]) => ({ es, en })),
    tomas
  };
  fs.writeFileSync(path.join(outDir, id + ".json"), JSON.stringify(escena, null, 1) + "\n");
}

/* ---------- lista maestra de assets ---------- */
const lista = Object.values(assets)
  .map(a => ({ ...a, prioridad: a.episodios.length > 1 ? "alta" : a.tomas >= 8 ? "media" : "normal" }))
  .sort((a, b) => b.episodios.length - a.episodios.length || b.tomas - a.tomas || a.episodios[0] - b.episodios[0]);
const porFamilia = {};
lista.forEach(a => (porFamilia[a.familia] ||= []).push(a.id));
fs.writeFileSync(path.join(here, "assets.json"), JSON.stringify({
  total: lista.length,
  familias: Object.fromEntries(Object.entries(porFamilia).map(([k, v]) => [k, { cantidad: v.length, ...cfg.familias[k] && { tecnica: cfg.familias[k].tecnica } }])),
  objetos: lista
}, null, 1) + "\n");

/* ---------- resumen ---------- */
const fr = total.segundos * FPS / PASO;
const horas = s => (fr * s / 3600).toFixed(0);
const lineas = [
  `Episodios: ${EP.length} · ${(total.segundos / 60).toFixed(0)} minutos en total`,
  `Tomas: ${total.tomas}`,
  `  clips animados por script: ${total.porScript}`,
  `  clips con Pipo o Plop, animados a mano: ${total.aMano - total.sinMovimiento.length}`,
  `  clips con animales (títeres), animados a mano: ${total.titere}`,
  `  clips de objetos sin movimiento de la biblioteca, a mano: ${total.sinMovimiento.length}`,
  `  reacciones de la biblioteca: ${total.banco}`,
  `  láminas: ${total.laminas}`,
  `Objetos distintos: ${lista.length} (${lista.filter(a => a.episodios.length > 1).length} en más de un episodio)`,
  `Familias: ${Object.entries(porFamilia).map(([k, v]) => `${k} ${v.length}`).join(" · ")}`,
  `Fotogramas únicos a ${FPS / PASO} fps: ${fr}`,
  `Render del año: ${horas(2)} h a 2 s/fotograma · ${horas(10)} h a 10 s · ${horas(20)} h a 20 s`,
  `Tomas por zona: ${Object.entries(total.zonas).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k} ${v}`).join(" · ")}`,
  `Movimientos: ${Object.entries(total.movs).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k} ${v}`).join(" · ")}`,
  `Clips de objetos sin movimiento reconocido (se animan a mano): ${total.sinMovimiento.length}`
];
fs.writeFileSync(path.join(here, "resumen.txt"), lineas.join("\n") + "\n");
console.log(lineas.join("\n"));
if (verbose) total.sinMovimiento.forEach(l => console.log("  · " + l));
