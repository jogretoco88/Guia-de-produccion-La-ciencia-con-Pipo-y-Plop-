// Genera index.html a partir de src/. Uso: node build.mjs [archivo-de-artefacto]
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const src = f => fs.readFileSync(path.join(root, "src", f), "utf8");
const eps = fs.readdirSync(path.join(root, "src", "episodios")).filter(f => /^ep\d+\.js$/.test(f)).sort();

const head = src("head.html"), body = src("body.html");
const js = [src("comun.js"), ...eps.map(f => src("episodios/" + f)), src("app.js")].join("\n");
const script = "<script>\n" + js + "</script>\n";

const full = '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n' +
  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' +
  head + "</head>\n<body>\n" + body + script + "</body>\n</html>\n";
fs.writeFileSync(path.join(root, "index.html"), full);
console.log(`index.html: ${eps.length} episodios, ${(full.length / 1024).toFixed(0)} KB`);

// Versión sin <html>/<head>/<body>, para publicarla como artefacto de Claude.
if (process.argv[2]) fs.writeFileSync(process.argv[2], head + body + script);
