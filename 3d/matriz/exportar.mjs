// Exporta los 52 episodios del archivo matriz (src/) para la producción 3D.
//   node 3d/matriz/exportar.mjs
// Escribe:
//   3d/matriz/episodios.json  todo lo que Blender necesita para montar cada episodio
//                             (tomas con su segundo de inicio, cámara, ingredientes, voz y objetos)
//   3d/matriz/plan_52.csv     una fila por episodio para seguir la producción 3D
// Vuelve a ejecutarlo cada vez que cambie el archivo matriz.
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const raiz = path.resolve(aqui, "..", "..");
const ctx = {};
vm.createContext(ctx);
const leer = f => fs.readFileSync(path.join(raiz, "src", f), "utf8");
vm.runInContext(leer("comun.js"), ctx);
for (const f of fs.readdirSync(path.join(raiz, "src", "episodios")).filter(f => /^ep\d+\.js$/.test(f)).sort())
  vm.runInContext(leer("episodios/" + f), ctx);
const g = n => vm.runInContext(n, ctx);
const EP = g("EP"), CATS = g("CATS"), SEASONS = g("SEASONS"), BANK = g("BANK"), CARDS = g("CARDS"), CAM = g("CAM"), SIZES = g("SIZES");

const temporada = n => SEASONS.findIndex(([, a, b]) => n >= a && n <= b) + 1;
const episodios = EP.slice().sort((a, b) => a.n - b.n).map(e => {
  let t = 0, bloque = 0, clip = 0;
  const tomas = [];
  for (const s of e.shots) {
    const tipo = s[0];
    if (tipo === "#") { bloque++; continue; }
    let d = 8, x = { tipo, bloque, inicio: t };
    if (tipo === "C") {
      clip++;
      Object.assign(x, { clip, cam: s[1], ing: s[2] || "", pantalla: s[3], escena: s[4], accion: s[5], voz: s[6] || "", marcas: s[7] || "" });
    } else if (tipo === "R") {
      clip++;
      const b = BANK[s[1]] || [];
      Object.assign(x, { clip, banco: s[1], cam: b[2] || "M", pantalla: b[1] || "", accion: b[4] || "", voz: s[2] || "" });
    } else if (tipo === "W") {
      clip++;
      Object.assign(x, { clip, cam: "M", pantalla: "Despedida del protagonista", voz: s[1] || "" });
    } else if (tipo === "S") {
      d = s[1];
      Object.assign(x, { ing: s[2] || "", pantalla: s[3], imagen: s[4], voz: s[5] || "", nombra: s[6] || "" });
    } else if (tipo === "T" || tipo === "F") {
      d = 4;
      const c = CARDS[tipo];
      Object.assign(x, { pantalla: c[0] + ": " + c[1], voz: c[3] || "" });
    }
    x.duracion = d;
    t += d;
    tomas.push(x);
  }
  const objetos = {};
  for (const [k, o] of Object.entries(e.objs || {}))
    objetos[k] = { tag: o.tag, tam: o.z, es: o.es, en: o.en };
  return { n: e.n, tema: e.topic, titulo: e.title, protagonista: e.star === "P" ? "Pipo" : "Plop",
           categoria: e.cat, zona: CATS[e.cat], temporada: temporada(e.n), duracion: t, objetos, tomas };
});

const tam = Object.fromEntries(Object.entries(SIZES).map(([k, v]) => [k, { nombre: v[0], es: v[1] }]));
const camaras = Object.fromEntries(Object.entries(CAM).map(([k, v]) => [k, v.es]));
fs.writeFileSync(path.join(aqui, "episodios.json"),
  JSON.stringify({ generado: "node 3d/matriz/exportar.mjs", camaras, tamanos: tam, episodios }, null, 1));

const cab = ["episodio", "titulo", "temporada", "zona", "protagonista", "clips_con_personaje", "clips_solo_objetos",
  "reacciones_banco", "laminas", "objetos_nuevos", "layout", "animacion", "render", "mezcla_5_idiomas", "publicado"];
const SEGUIMIENTO = cab.slice(10);
// Conserva lo que ya esté marcado en las columnas de seguimiento.
const rutaCsv = path.join(aqui, "plan_52.csv");
const previo = {};
if (fs.existsSync(rutaCsv)) {
  const lineas = fs.readFileSync(rutaCsv, "utf8").replace(/^\ufeff/, "").split(/\r?\n/).filter(Boolean);
  const campos = l => (l.match(/("([^"]|"")*"|[^,]*)(,|$)/g) || []).map(c => c.replace(/,$/, ""));
  const cabPrevia = campos(lineas[0]);
  for (const l of lineas.slice(1)) {
    const v = campos(l);
    previo[v[0]] = Object.fromEntries(SEGUIMIENTO.map(k => [k, v[cabPrevia.indexOf(k)] ?? ""]));
  }
}
const csv = [cab.join(",")];
for (const e of episodios) {
  const c = e.tomas.filter(x => x.tipo === "C");
  const conPj = c.filter(x => /[PL]/.test(x.ing)).length;
  csv.push([e.n, `"${e.titulo.replace(/"/g, '""')}"`, e.temporada, e.zona, e.protagonista, conPj, c.length - conPj,
    e.tomas.filter(x => x.tipo === "R").length, e.tomas.filter(x => x.tipo === "S").length,
    Object.keys(e.objetos).length, ...SEGUIMIENTO.map(k => (previo[String(e.n)] || {})[k] || "")].join(","));
}
fs.writeFileSync(path.join(aqui, "plan_52.csv"), "﻿" + csv.join("\n") + "\n");
const mal = episodios.filter(e => e.duracion !== 300);
console.log(`${episodios.length} episodios exportados · ${mal.length ? "duración distinta de 5:00 en " + mal.map(e => e.n).join(", ") : "todos duran 5:00"}`);
