// Comprueba que cada episodio cumple el formato. Uso: node validate.mjs [-v]
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const verbose = process.argv.includes("-v");
const ctx = vm.createContext({});
const run = f => vm.runInContext(fs.readFileSync(path.join(root, "src", f), "utf8"), ctx, { filename: f });
run("comun.js");
const files = fs.readdirSync(path.join(root, "src", "episodios")).filter(f => /^ep\d+\.js$/.test(f)).sort();
files.forEach(f => run("episodios/" + f));
const get = n => vm.runInContext(n, ctx);
const EP = get("EP"), CAM = get("CAM"), BANK = get("BANK"), PIPOPLES = get("PIPOPLES"), BLOCKS = get("BLOCKS"), CATS = get("CATS"), MOTORS = get("MOTORS"), CERT = get("CERT");

const words = t => t.replace(/\[[^\]]*\]/g, " ").split(/\s+/).filter(w => /[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]/.test(w)).length;
const pad = n => ("0" + n).slice(-2);
let bad = 0;
const err = m => { bad++; console.log("  ✗ " + m); };

/* Contenido para niños de 5 años en adelante: ninguna parte del cuerpo suelta ni nada que salga de la boca.
   Una palabra de la lista solo se admite cuando pertenece a un personaje o a un animal («Plop's tongue», «its leg»). */
const BODY = /\b(brains?|tongues?|eyeballs?|lungs?|intestines?|guts?|stomachs?|skulls?|bones?|spines?|blood|vessels?|nerves?|jaws?|throats?|muscles?|glands?|saliva|mucus|snot|vomit\w*|scabs?|fingertips?|nostrils?|organs?|hearts?)\b/gi;
const OWNER = /(\b(?:Pipo|Plop|his|its|her|their)\b|'s)\s+(?:[\w,-]+\s+){0,5}$/i;
/* El video se publica en varios idiomas: nada de letras, números ni signos en la imagen. */
const PART = /\b(?:friendly|peach|human)\s+clay\s+(?:eye|ear|nose|hand|arm|leg|foot|finger)s?\b|\bclay\s+(?:eye|ear|nose|foot|finger)s?\b|\b(?:eye|ear|nose|hand|arm|leg|foot|finger)\s+model\b|\bin cross-section\b[^.]*\b(?:caterpillar|cat|dog|bird|animal|person)\b/i;
const GLYPH = /question marks?|exclamation marks?|\bletters?\b|\bnumbers?\b|\bwords?\b/i;
const OPEN = /\btongue\b|\byawn|\bmouth (?:open|wide)|\bopens? (?:his|its) mouth|\bopen mouth/i;
const MOUTH_OUT = /\b(?:out of|from)\s+(?:his|her|its|Pipo's|Plop's|the)\s+mouth\b|\bdrool|\bspit\b|\bspits\b/i;
function safe(id, txt) {
  for (const m of txt.matchAll(BODY)) {
    if (!OWNER.test(txt.slice(Math.max(0, m.index - 60), m.index))) { err(`${id} parte del cuerpo suelta («${m[0]}»): muéstrala unida a Pipo o a Plop, o cámbiala por un juguete`); return; }
  }
  if (PART.test(txt)) err(`${id} parte del cuerpo suelta (ojo, oreja, nariz, mano, pie…): que pertenezca a Pipo, a Plop o a un animal entero`);
  if (GLYPH.test(txt)) err(`${id} pide letras, números o signos: el video no lleva ningún texto`);
  if (MOUTH_OUT.test(txt)) err(`${id} algo sale de la boca: parece que vomita. Que caiga desde arriba`);
}
/* El laboratorio es azul claro: la escena no cambia el color del suelo, y un fondo propio es un panel sobre el set */
function setCheck(id, txt) {
  if (/\b(?:white|grey|gray|black) floor\b/i.test(txt)) err(`${id} pone color al suelo: lo da el fondo del episodio`);
  if (/\bagainst an? [^.]*\bbackdrop\b/i.test(txt)) err(`${id} fondo propio: descríbelo como «backdrop panel standing on the set»`);
}
const note = m => { if (verbose) console.log("  · " + m); };

const SHAPE = "CCCT|CCCCCC|CCCCS6CCC|CCCCCCCCC|CCCCC|S8CCCS6|CF";
const REQ = ["topic", "title", "star", "cat", "mot", "cert", "why", "secret", "thumb", "thumbIdea", "vocab", "syn", "tags", "reto", "objs", "facts", "simpl", "sfx", "shots"];

EP.sort((a, b) => a.n - b.n);
EP.forEach((ep, i) => {
  const E = "Ep." + pad(ep.n);
  const before = bad;
  for (const k of REQ) if (ep[k] == null || ep[k] === "") err(`${E} falta ${k}`);
  if (ep.n !== i + 1) err(`${E} numeración (posición ${i + 1})`);
  if (ep.star !== (ep.n % 2 ? "P" : "L")) err(`${E} protagonista ${ep.star}`);
  if (!CATS[ep.cat]) err(`${E} categoría`);
  for (const k of ep.mot || "") if (!MOTORS[k]) err(`${E} motor ${k}`);
  if (!CERT[ep.cert]) err(`${E} certeza`);
  if (i && EP[i - 1].cat === ep.cat) err(`${E} misma categoría que el anterior (${ep.cat})`);
  if ((ep.title + " | Pipo y Plop").length > 70) err(`${E} título largo`);
  if ((ep.thumb || "").split(" ").length > 3) err(`${E} miniatura larga`);
  if ((ep.facts || []).length < 4) err(`${E} pocos datos en la ficha`);
  if ((ep.simpl || []).length < 1) err(`${E} falta lo que se simplifica`);
  if ((ep.sfx || []).length !== 4) err(`${E} efectos de sonido ≠ 4`);
  const co = ep.star === "P" ? "L" : "P";
  for (const [k, o] of Object.entries(ep.objs || {})) {
    if (!/^[a-k]$/.test(k)) err(`${E} objeto ${k}`);
    for (const f of ["tag", "es", "en", "p"]) if (!o[f]) err(`${E} objeto ${k} sin ${f}`);
    safe(`${E} objeto ${k}`, (o.en || "") + " " + (o.p || ""));
    if (!/^[tsmlxg]$/.test(o.z || "")) err(`${E} objeto ${k} sin tamaño (z: t, s, m, l, x o g)`);
  }
  let c = 0, t = 0, tot = 0, shape = [], cur = "", coN = 0, bankN = 0, last = "", plopN = 0, talk = 0, predict = false;
  const used = {};
  for (const r of ep.shots || []) {
    const k = r[0];
    if (k === "#") { if (cur) shape.push(cur); cur = ""; continue; }
    if (k === "C" || k === "R" || k === "W") {
      c++; cur += "C"; t += 8;
      const id = `${E} C${pad(c)}`;
      let vo;
      if (k === "C") {
        const [, cam, tags, es, scene, act, v, fl] = r; vo = v;
        if (r.length < 7) err(`${id} campos`);
        if (!CAM[cam]) err(`${id} cámara ${cam}`);
        for (const x of tags) if (x !== "P" && x !== "L" && !ep.objs[x]) err(`${id} ingrediente ${x}`);
        if (tags.length > 3) err(`${id} más de 3 referencias`);
        if (!es || !scene || !act) err(`${id} texto vacío`);
        if (/\d\s*[–-]\s*\d\s*s\b|\bthen\b/i.test(act)) err(`${id} acción partida: ${act}`);
        if (/["“”]/.test(scene + act)) err(`${id} comillas en el prompt`);
        if (!/[.!?]$/.test(scene.trim()) || !/[.!?]$/.test(act.trim())) err(`${id} falta punto final`);
        for (const [x, nm] of [["P", /\bPipo\b/], ["L", /\bPlop\b/]]) if (tags.includes(x) !== nm.test(scene + " " + act)) err(`${id} ingrediente y prompt no coinciden (${x})`);
        safe(id, scene + " " + act); setCheck(id, scene);
        /* Lengua fuera o bostezo: la boca se abre, así que el prompt no puede pedir «mouth closed» */
        if (/[PL]/.test(tags) && OPEN.test(scene + " " + act) && !(fl || "").split(" ").includes("o")) err(`${id} boca abierta sin la marca «o»`);
        for (const f of (fl || "").split(" ").filter(Boolean)) {
          if (f[0] === "<") { const n = +f.slice(1); if (!(n >= 1 && n < c)) err(`${id} encadena mal ${f}`); }
          else if (/^[a-e]=[tsmlxg]$/.test(f)) { if (!ep.objs[f[0]] || !tags.includes(f[0])) err(`${id} tamaño para un objeto que no está en la toma: ${f}`); }
          else if (f === "b") { if (!tags.includes("L")) err(`${id} marca «b» (Plop se hace bolita) sin Plop en la toma`); plopN++; }
          else if (!"ko".includes(f)) err(`${id} marca ${f}`);
        }
        last = "";
      } else if (k === "R") {
        vo = r[2];
        if (!BANK[r[1]]) err(`${id} banco ${r[1]}`);
        if (r[1] === last) err(`${id} repite ${r[1]} dos veces seguidas`);
        last = r[1]; used[r[1]] = (used[r[1]] || 0) + 1; bankN++;
        if (r[1][0] === co) coN++;
      } else {
        vo = r[1] || "La próxima pregunta es de X: " + (EP[i + 1] ? EP[i + 1].title : "");
        if (!r[1] && !EP[i + 1]) (EP.length >= 52 ? err : note)(`${id} despedida sin episodio siguiente: escribe la voz`);
        bankN++; last = "";
      }
      if (!vo) err(`${id} sin voz`);
      else {
        const w = words(vo); tot += w;
        if (w > 18) err(`${id} voz de ${w} palabras: ${vo}`); if (w < 8) note(`${id} voz corta (${w})`);
        /* Guion al día con el Lore: la reacción deja sitio a su frase en pipoplés */
        if (ep.lore && k === "R" && w > 15) err(`${id} reacción con ${w} palabras: deja sitio a la frase en pipoplés (15 como máximo)`);
        if (/(^|[¡¿.!?…]\s*)(?:\[[a-z]+\]\s*)?(?:Pipo|Plop),/.test(vo)) talk++;
        if (c >= 26 && c <= 30 && /crees|Piénsalo|piénsalo/.test(vo)) predict = true;
      }
      if (c === 4 && !(k === "R" && r[1] === "P1")) err(`${id} debe ser la idea loca: ["R","P1",…]`);
      if (c === 7 && !(k === "R" && r[1] === "L1")) err(`${id} debe ser la pregunta de Plop: ["R","L1",…]`);
      if (c === 33 && !(k === "R" && r[1] === "L9")) err(`${id} debe ser la invitación al reto: ["R","L9",…]`);
      if (c === 34 && k !== "W") err(`${id} debe ser la despedida: ["W"]`);
      if (c === 9 && !/Piénsalo/.test(vo || "")) err(`${id} falta la pausa «Piénsalo…»`);
      if (c === 10 && !/Hagamos zoom/.test(vo || "")) err(`${id} falta «¡Hagamos zoom!»`);
    } else if (k === "S") {
      cur += "S" + r[1]; t += r[1];
      const id = `${E} lámina`;
      if (r.length < 7) err(`${id} campos`);
      if (r[2].includes("P") && r[2].includes("L")) err(`${id} con Pipo y Plop juntos`);
      for (const [x, nm] of [["P", /\bPipo\b/], ["L", /\bPlop\b/]]) if (r[2].includes(x) !== nm.test(r[4])) err(`${id} ingrediente y prompt no coinciden (${x})`);
      safe(id, r[4]); setCheck(id, r[4]);
      for (const x of r[2]) if (x !== "P" && x !== "L" && !ep.objs[x]) err(`${id} ingrediente ${x}`);
      const w = words(r[5]); tot += w;
      if (w > r[1] * 2.6) err(`${id} voz de ${w} palabras para ${r[1]} s`);
      if (r[1] === 8 && !/^Repasemos/.test(r[5])) err(`${id} de repaso sin «Repasemos»`);
    } else if (k === "T" || k === "F") {
      cur += k; t += 4;
    } else err(`${E} toma desconocida ${k}`);
  }
  if (cur) shape.push(cur);
  if (shape.join("|") !== SHAPE) err(`${E} estructura ${shape.join("|")}`);
  if (c !== 34) err(`${E} ${c} clips`);
  if (t !== 300) err(`${E} dura ${t} s`);
  if (coN < 3) err(`${E} el acompañante aparece ${coN} veces`);
  if (ep.lore) {
    if (!predict) err(`${E} falta la pausa para predecir en la prueba (bloque 5): «¿Qué crees que pasará?»`);
    if (!talk) err(`${E} el narrador no habla nunca con Pipo ni con Plop («Pipo, …»)`);
  }
  for (const [b, n] of Object.entries(used)) if (n > 2) err(`${E} usa ${b} ${n} veces`);
  if (verbose || bad > before) console.log(`${E} ${ep.topic}: ${34 - bankN} clips nuevos + ${bankN} del banco (${coN} del acompañante) · ${tot} palabras`);
});
if (new Set(EP.map(e => e.title)).size !== EP.length) err("títulos repetidos");
for (const k of Object.keys(BANK)) if (!PIPOPLES[k]) err(`reacción ${k} sin frase en pipoplés`);
const lore = EP.filter(e => e.lore).map(e => e.n);
console.log(`Guion al día con el Lore: ${lore.length ? lore.join(", ") : "ninguno"}`);
const cc = {}; EP.forEach(e => { cc[e.cat] = (cc[e.cat] || 0) + 1; });
console.log(`${EP.length} episodios · ` + Object.entries(cc).map(([k, v]) => CATS[k] + " " + v).join(" · "));
console.log(bad ? `\n${bad} errores` : "\nTodo correcto");
process.exit(bad ? 1 : 0);
