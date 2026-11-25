/* =====================================================================
   LÓGICA DE LA PÁGINA
   ===================================================================== */
(function () {
  "use strict";

  EP.sort(function (a, b) { return a.n - b.n; });

  var $ = function (id) { return document.getElementById(id); };
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function tc(s) { s = Math.round(s); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }
  function pad(n) { return ("0" + n).slice(-2); }
  function words(t) { return t.replace(/\[[^\]]*\]/g, " ").split(/\s+/).filter(function (w) { return /[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]/.test(w); }).length; }
  function ul(a) { return "<ul class='plain'>" + a.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ul>"; }
  function link(u, t) { return "<a href='" + u + "' target='_blank' rel='noopener'>" + t + "</a>"; }
  function plain(s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }

  var store = {
    get: function (k, d) { try { var v = localStorage.getItem("pipoplop3:" + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem("pipoplop3:" + k, JSON.stringify(v)); } catch (e) { /* sin almacenamiento: la página sigue funcionando */ } }
  };

  var TABS = ["guia", "guion", "tomas", "elenco", "prod", "canal", "plan"];
  var ui = store.get("ui", {});
  var cur = Math.min(EP.length - 1, Math.max(0, ui.cur || 0));
  var tab = TABS.indexOf(ui.tab) > -1 ? ui.tab : "guia";
  var blk = -1, pc = "", pm = "", pq = "";
  var bankDone = store.get("bank", []);
  var CP = [];

  /* ---------- Tomas: de las listas de datos a objetos con tiempos ---------- */
  function coOf(ep) { return ep.star === "P" ? "L" : "P"; }
  function bankId(code) { return "B" + code.charAt(0) + pad(+code.slice(1)); }
  function build(ep) {
    if (ep._s) return ep._s;
    var out = [], t = 0, b = -1, c = 0, l = 0, E = "E" + pad(ep.n), nx = EP[EP.indexOf(ep) + 1];
    ep.shots.forEach(function (r) {
      var k = r[0], s;
      if (k === "#") { b++; return; }
      if (k === "C") {
        c++;
        s = {k: "C", id: E + "_C" + pad(c), d: 8, cam: r[1], tags: r[2], es: r[3], scene: r[4], act: r[5], vo: r[6]};
        (r[7] || "").split(" ").forEach(function (f) {
          if (f === "b") s.plop = true;
          else if (f === "o") s.open = true;
          else if (f.charAt(0) === "<") s.from = E + "_C" + pad(+f.slice(1));
          else if (/^[a-e]=[tsmlxg]$/.test(f)) { s.zo = s.zo || {}; s.zo[f.charAt(0)] = f.charAt(2); }
        });
        if (c === 10) s.zuum = true;
      } else if (k === "R" || k === "W") {
        c++;
        var code = k === "W" ? ep.star + "10" : r[1], B = BANK[code];
        var vo = k === "W"
          ? (r[1] || "La próxima pregunta es de " + WHO[coOf(ep)].es + ": " + (nx ? nx.title.replace(/^¿(.)/, function (m, x) { return "¿" + x.toLowerCase(); }) : ""))
          : r[2];
        s = {k: "R", id: E + "_C" + pad(c), d: 8, code: code, bid: bankId(code), name: B[0], es: B[1], cam: B[2], tags: code.charAt(0), scene: B[3], act: B[4], vo: vo};
      } else if (k === "S") {
        l++;
        s = {k: "S", id: E + "_L" + l, d: r[1], tags: r[2], es: r[3], scene: r[4], vo: r[5], lab: r[6]};
      } else {
        var K = CARDS[k];
        s = {k: "K", id: k === "T" ? "CANAL_INICIO" : "CANAL_FINAL", code: k, d: 4, name: K[0], es: K[1], scene: K[2], vo: K[3], lab: K[4], tags: "PL"};
      }
      s.b = b; s.t0 = t; t += s.d; s.t1 = t; out.push(s);
    });
    ep._s = out; ep._dur = t;
    return out;
  }
  function blockSpan(ep, b) {
    var S = build(ep).filter(function (s) { return s.b === b; });
    return [S[0].t0, S[S.length - 1].t1];
  }
  function count(ep) {
    if (ep._c) return ep._c;
    var o = {gen: 0, bank: 0, stills: 0, words: 0};
    build(ep).forEach(function (s) {
      if (s.k === "C") o.gen++; else if (s.k === "R") o.bank++; else if (s.k === "S") o.stills++;
      o.words += words(s.vo);
    });
    o.clips = o.gen + o.bank; o.own = o.gen; o.dur = ep._dur; ep._c = o;
    return o;
  }

  /* ---------- Escala y elenco de cada toma ---------- */
  function zOf(ep, s, k) { var o = ep.objs[k]; return o ? ((s && s.zo && s.zo[k]) || o.z) : ""; }
  /* Quién y qué sale en la toma, en español: «Pipo + Grano de maíz gigante» */
  function cast(ep, tags) {
    var r = (tags || "").split("").map(function (k) { return WHO[k] ? WHO[k].es : ep.objs[k] ? ep.objs[k].es : ""; }).filter(Boolean);
    return r.length ? r.join(" + ") : "solo el set";
  }
  function sizeLine(ep, s) {
    var ob = (s.tags || "").split("").filter(function (k) { return ep.objs[k]; });
    if (!ob.length) return "";
    return "<p class='meta'><b>Tamaños:</b> " + ob.map(function (k) {
      var z = SIZES[zOf(ep, s, k)]; return esc(ep.objs[k].es) + ", " + z[0].toLowerCase() + " (" + z[1].split(",")[0] + ")";
    }).join(" · ") + "</p>";
  }
  function ppLine(s) {
    var P = PIPOPLES[s.code];
    return "<p class='pp'><b>" + WHO[s.code.charAt(0)].es + " en pipoplés:</b> «" + esc(P[0]) + "» <span class='mut'>" + esc(P[1].toLowerCase()) + "</span></p>";
  }
  function animFold(s) {
    if (!s.scene && !s.act) return "";
    return "<details class='alt'><summary>Indicación de animación (en inglés: la lee el proyecto de Blender)</summary><div>" +
      (s.scene ? "<p class='meta'><b>Al empezar:</b> " + esc(s.scene) + "</p>" : "") + (s.act ? "<p class='meta'><b>Acción:</b> " + esc(s.act) + "</p>" : "") + "</div></details>";
  }

  /* ---------- Bloques copiables ---------- */
  function cb(text, label, opt) {
    opt = opt || {};
    CP.push(text);
    return "<div class='cb'>" + (opt.lab ? "<span class='lab'>" + esc(opt.lab) + "</span>" : "") +
      "<pre class='copy" + (opt.txt ? " txt" : "") + "'>" + esc(text) + "</pre>" +
      "<button class='btn" + (opt.ghost ? " ghost" : "") + "' data-k='" + (CP.length - 1) + "'>" + esc(label) + "</button></div>";
  }
  function copyTxt(t, b) {
    var done = function () { var o = b.textContent; b.textContent = "Copiado"; setTimeout(function () { b.textContent = o; }, 1400); };
    var fallback = function () {
      var pre = b.previousElementSibling, r = document.createRange(), sel = window.getSelection();
      r.selectNodeContents(pre); sel.removeAllRanges(); sel.addRange(r);
      try { if (document.execCommand("copy")) { done(); return; } } catch (e) { /* el texto queda seleccionado para copiarlo a mano */ }
      b.textContent = "Seleccionado: copia con Ctrl+C";
    };
    try { navigator.clipboard.writeText(t).then(done, fallback); } catch (e) { fallback(); }
  }

  /* ---------- Textos para YouTube ---------- */
  function ytTitle(ep) { return ep.title + " | Pipo y Plop"; }
  function ytDesc(ep) {
    var ch = BLOCKS.slice(0, 6).map(function (b, i) { return tc(blockSpan(ep, i)[0]) + " " + b[0]; }).join("\n");
    return ep.title + "\n" + ep.secret + "\n\n" +
      "Pipo, un pequeño extraterrestre, tiene una idea loca. Plop, un osito de agua casi indestructible, hace la pregunta correcta. Y juntos se meten dentro de la respuesta.\n\n" +
      "CAPÍTULOS\n" + ch + "\n\n" +
      "RETO EN CASA\n" + ep.reto + "\n\n" +
      "PARA FAMILIAS Y DOCENTES\nIdea central: " + ep.secret + "\nPalabras nuevas: " + ep.vocab + "\nFuentes: (pega aquí tus dos fuentes)\n\n" +
      "También se busca como: " + ep.syn + "\n\n" +
      "Animación de plastilina digital hecha en Blender. Voces generadas con ElevenLabs. Guion y revisión científica hechos por personas.\n\n" +
      "#CienciaParaNiños #PipoYPlop " + ep.tags;
  }

  /* ---------- Pasos de la guía ---------- */
  var STEPS = [
    {t: "1 · Ciencia y guion", i: [
      ["Verifica la ficha científica con dos fuentes", "Pestaña Guion. Un libro de texto, un museo de ciencia o una universidad. Como docente, das el visto bueno. Anota las fuentes: van en la descripción del video."],
      ["Lee el guion en voz alta con cronómetro", "Cada frase cae en una toma de 8 s y dura unos 6. Si una frase pasa de 7 s al leerla, recórtala antes de grabar."]]},
    {t: "2 · Voces", i: [
      ["Narración en los 5 idiomas", "Pestaña Guion. Tu voz de narrador en ElevenLabs, una frase por toma, en español, inglés, francés, portugués de Brasil e hindi. El flujo completo está en la carpeta narracion del repositorio."],
      ["Frases de Pipo y Plop en pipoplés", "Pestaña Guion. Son frases fijas del banco: se graban una sola vez con sus voces y valen para todos los idiomas. Este episodio usa __PP__."],
      ["Exporta y nombra", "__E___VO_ES, __E___VO_EN, __E___VO_FR, __E___VO_PT y __E___VO_HI: una pista de narrador por idioma."]]},
    {t: "3 · Set y utilería en Blender", i: [
      ["Modela los objetos del episodio", "Pestaña Elenco. Cada objeto a su tamaño junto al títere, que mide unos 30 cm. Todo de plastilina mate, con huellas."],
      ["Prepara la zona del laboratorio", "Pestaña Producción 3D. Cada escena pasa en la zona que pide su tema; la cámara de zoom se usa en los bloques 3 y 4."],
      ["Monta el layout del episodio", "En la carpeta blender del proyecto 3D: blender -b -P episodio.py -- --ep __N__ --guardar C:\\pipo_plop\\__EPN___layout.blend --storyboard C:\\pipo_plop\\storyboard___EPN__. Coloca las 39 tomas con su cámara y su duración."]]},
    {t: "4 · Animación", i: [
      ["Anima las tomas en orden", "Pestaña Tomas. Una sola acción por toma, animada de a dos (12 poses por segundo). Este episodio tiene __OWN__ tomas propias."],
      ["Usa las reacciones del banco", "Pestaña Elenco. Las 20 reacciones se animan una sola vez y se reutilizan. Este episodio usa __BANK__."],
      ["Sincroniza las bocas del pipoplés", "Las frases de Pipo y Plop van con las 9 bocas de reemplazo (Rhubarb Lip Sync o idioma.py). Esa animación sirve para todos los idiomas."],
      ["Revisa cada toma", "Manos sin dedos, nada de texto, una sola acción y nada que pueda incomodar a un niño de 5 años (Producción 3D, reglas de contenido)."]]},
    {t: "5 · Render", i: [
      ["Render en EEVEE a 1920×1080", "A 24 fotogramas por segundo y animado de a dos: solo se renderizan los 12 fotogramas únicos de cada segundo. Cycles, solo para la miniatura."],
      ["Láminas sin texto", "Las 3 láminas del episodio se renderizan en la pizarra del laboratorio. La cortinilla y la tarjeta final son las del canal."]]},
    {t: "6 · Montaje y sonido en DaVinci Resolve", i: [
      ["Línea de tiempo 1920×1080 a 24 fps", "Coloca las tomas y las láminas en orden y sin huecos: son ellas las que dan los 5:00."],
      ["Importa los subtítulos de tiempos", "Pestaña Guion, archivo .srt. En DaVinci: File → Import → Subtitle. Cada subtítulo marca dónde empieza una frase del narrador."],
      ["Una frase del narrador sobre cada toma", "Coloca cada frase al comienzo de su subtítulo. Si pasa de su toma, recórtala o acelérala hasta un 110 %, nunca más. Deja 2 s de silencio después de «Piénsalo…»."],
      ["Pista de música y efectos", "Una sola para todos los idiomas: el pipoplés, el «¡Zuuum!», el estribillo, el jingle del zoom, los efectos del episodio y el kit del canal."],
      ["Mezcla de cada idioma", "Cada idioma lleva su narrador sobre la pista de música y efectos. La voz siempre se entiende por encima de todo. Normaliza a −16 LUFS."]]},
    {t: "7 · Publicación en YouTube", i: [
      ["Título, descripción y capítulos", "Cópialos de aquí abajo y añade tus dos fuentes.", "yt"],
      ["Miniatura", "__THUMB__"],
      ["Audiencia: «Sí, es contenido para niños»", "Es obligatorio en un canal dirigido a niños. Desactiva comentarios, tarjetas y pantallas finales: por eso el cierre hablado anuncia el siguiente episodio."],
      ["Pistas de audio y subtítulos", "Si el canal tiene la función de pistas de audio en varios idiomas, sube los 5 narradores al mismo video. Sube también los subtítulos de cada idioma."],
      ["Revisión en televisor", "Míralo completo en una TV: nitidez, volumen de la voz, que no aparezca ningún texto y que nada pueda asustar o incomodar a un niño de 5 años."]]},
    {t: "8 · Después de publicar", i: [
      ["Corta tres Shorts", "El zoom (desde el clip 10), la prueba con el «¡plop!» de Plop (bloque 5) y el dato extra (C31 y C32). Sin texto en pantalla, para usarlos en cualquier idioma."],
      ["Lee la retención a las 48 horas y a los 7 días", "Mira los primeros 30 segundos, el zoom y la prueba. Anota en qué segundo cae la curva y corrige ese bloque en el siguiente episodio."]]}
  ];
  var TOTAL = STEPS.reduce(function (s, p) { return s + p.i.length; }, 0);
  function chk(ep) { return store.get("chk" + ep.n, []); }
  function status(ep) {
    var n = chk(ep).length;
    return n === 0 ? "Sin empezar" : n >= TOTAL ? "Publicado" : "En producción · " + n + "/" + TOTAL;
  }
  function bankUsed(ep) {
    var u = [];
    build(ep).forEach(function (s) { if (s.k === "R" && u.indexOf(s.code) < 0) u.push(s.code); });
    return u;
  }

  /* ---------- Vista: Guía ---------- */
  function vGuia(ep) {
    var c = count(ep), done = chk(ep), pct = Math.round(done.length / TOTAL * 100), E = "E" + pad(ep.n), U = bankUsed(ep);
    var h = "<section class='panel'><h2>Ep. " + ep.n + " · " + esc(ep.title) + "</h2>" +
      "<p class='mut'>Protagonista: " + WHO[ep.star].es + " · lo acompaña " + WHO[coOf(ep)].es + " · " + CATS[ep.cat] + " · " + CERT[ep.cert][0] + "</p>" +
      "<p class='secret'>" + esc(ep.secret) + "</p>" +
      "<ul class='stats'><li>" + tc(c.dur) + " de video</li><li>" + c.clips + " tomas de 8 s</li><li>" + c.gen + " para animar</li><li>" + c.bank + " reacciones del banco</li><li>3 láminas y 2 del canal</li></ul>" +
      (ep.lore ? "" : "<p class='note'><b>Guion pendiente de pasar al Lore.</b> Las voces de este episodio todavía no tienen al narrador cómplice, la pausa para predecir ni a Plop de piloto de pruebas.</p>") +
      "<div class='barp' role='progressbar' aria-valuemin='0' aria-valuemax='100' aria-valuenow='" + pct + "' aria-label='Avance del episodio'><i style='width:" + pct + "%'></i></div>" +
      "<p class='mut'>" + done.length + " de " + TOTAL + " pasos completados" + (done.length === TOTAL ? ". Episodio publicado." : "") + "</p></section>";
    STEPS.forEach(function (p, pi) {
      h += "<h3>" + esc(p.t) + "</h3><div class='steps'>";
      p.i.forEach(function (it, ii) {
        var id = "p" + pi + "i" + ii, on = done.indexOf(id) > -1;
        var det = it[1].replace(/__E__/g, E).replace(/__EPN__/g, "ep" + pad(ep.n)).replace("__N__", ep.n)
          .replace("__PP__", U.map(function (k) { return "«" + PIPOPLES[k][0] + "»"; }).join(", "))
          .replace("__OWN__", c.gen)
          .replace("__BANK__", U.length + " de ellas: " + U.join(", "))
          .replace("__THUMB__", ep.thumbIdea + " Sin palabras, o solo una onomatopeya que se entienda en cualquier idioma: «" + ep.thumb + "».");
        h += "<label class='step" + (on ? " on" : "") + "'><input type='checkbox' id='s-" + ep.n + "-" + id + "' data-id='" + id + "'" + (on ? " checked" : "") + "><div><b>" + esc(it[0]) + "</b><span>" + esc(det) + "</span></div></label>";
        if (it[2] === "yt") h += cb(ytTitle(ep), "Copiar título", {lab: "Título", txt: 1}) + cb(ytDesc(ep), "Copiar descripción", {lab: "Descripción", txt: 1});
      });
      h += "</div>";
    });
    return h + "<p><button class='btn ghost' id='reset'>Reiniciar los pasos de este episodio</button></p>";
  }

  /* ---------- Vista: Guion ---------- */
  /* Segundos que tarda la voz en decir una frase, con la velocidad recomendada */
  function vsec(t) { return words(t) / (VOICE.rate * VOICE.speed); }
  function srtTime(x) {
    var ms = Math.round(x * 1000), h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, sc = Math.floor(ms / 1000) % 60;
    return ("0" + h).slice(-2) + ":" + ("0" + m).slice(-2) + ":" + ("0" + sc).slice(-2) + "," + ("00" + (ms % 1000)).slice(-3);
  }
  function srt(ep) {
    var n = 0;
    return build(ep).filter(function (s) { return s.vo && words(s.vo); }).map(function (s) {
      var a = s.t0 + VOICE.lead, b = Math.min(s.t1 - 0.2, a + Math.max(1.5, vsec(s.vo)));
      return (++n) + "\n" + srtTime(a) + " --> " + srtTime(b) + "\n" + s.vo.replace(/\[[^\]]*\]\s*/g, "").trim() + "\n";
    }).join("\n");
  }
  function vGuion(ep) {
    var S = build(ep), c = count(ep), all = [], marks = [];
    var vt = S.reduce(function (n, s) { return n + (s.vo ? vsec(s.vo) : 0); }, 0);
    var h = "<section class='panel'><h2>Guion · Ep. " + ep.n + "</h2>" +
      "<p class='mut'>" + c.words + " palabras del narrador para " + tc(c.dur) + " de video. Cada línea es la voz de una toma: explica, pregunta y habla con Pipo y Plop. La acción la muestra la imagen.</p>" +
      "<p class='note'><b>La voz dura unos " + tc(vt) + ", no 5:00, y está bien así.</b> Cada frase ocupa unos 6 de los 8 segundos de su toma; el resto es respiro para la imagen, el pipoplés, la música y los efectos. " +
      "En el montaje, cada frase se coloca al comienzo de su toma: el archivo de subtítulos de abajo marca dónde.</p>" +
      ul(["<b>Narrador:</b> tu voz clonada en ElevenLabs, la misma en todo el canal y en los 5 idiomas. Cómplice: habla con el niño y también con Pipo y Plop.",
          "<b>Modelo:</b> Eleven v4, el de la narración de los episodios 1 a 4. Entiende las etiquetas entre corchetes.",
          "<b>Velocidad:</b> 0,9 en los ajustes de la voz. Un ritmo algo más pausado, mejor para niños, que llena más cada toma sin pasarse de los 8 segundos.",
          "<b>Pausas:</b> no estires el audio con pausas: el tiempo se ajusta en el montaje.",
          "<b>Etiquetas:</b> ya vienen puestas, una por frase como máximo. Los efectos de sonido van aparte, no en el texto.",
          "<b>Números y siglas:</b> están escritos como se pronuncian."]) + "</section>";
    var PP = S.filter(function (s) { return s.k === "R" || s.zuum; });
    h += "<section class='panel'><h3>Pipo y Plop en pipoplés</h3>" +
      "<p class='prose'>Son frases fijas: se graban una sola vez con las voces de Pipo y Plop y no se traducen. Van en la pista de música y efectos, al comienzo de su toma; el narrador entra después.</p>" +
      "<div class='scroll'><table><thead><tr><th>Toma</th><th>Tiempo</th><th>Quién</th><th>Frase</th><th>Intención</th></tr></thead><tbody>" +
      PP.map(function (s) {
        if (s.zuum) return "<tr><td>" + s.id + "</td><td>" + tc(s.t0) + "</td><td>Pipo y Plop</td><td>" + esc(ZUUM) + "</td><td>El momento del zoom, con su jingle</td></tr>";
        var P = PIPOPLES[s.code];
        return "<tr><td>" + s.id + "</td><td>" + tc(s.t0) + "</td><td>" + WHO[s.code.charAt(0)].es + "</td><td>" + esc(P[0]) + "</td><td>" + esc(P[1]) + "</td></tr>";
      }).join("") + "</tbody></table></div></section>";
    BLOCKS.forEach(function (b, bi) {
      var L = S.filter(function (s) { return s.b === bi; }), sp = blockSpan(ep, bi);
      var txt = L.map(function (s) { return s.vo; }).join("\n");
      var w = L.reduce(function (n, s) { return n + words(s.vo); }, 0);
      all.push(txt);
      L.forEach(function (s) { marks.push(tc(s.t0) + "  " + (s.k === "R" ? s.id + " (" + s.bid + ")" : s.id) + "  " + s.vo); });
      var bs = L.reduce(function (n, s) { return n + (s.vo ? vsec(s.vo) : 0); }, 0);
      h += "<section class='panel'><h3>Bloque " + (bi + 1) + " · " + esc(b[0]) + " · " + tc(sp[0]) + "–" + tc(sp[1]) + "</h3>" +
        "<p class='mut'>Unos " + Math.round(bs) + " s de voz para " + (sp[1] - sp[0]) + " s de video · " + L.length + " frases, una por toma · " + txt.length + " caracteres</p>" +
        cb(txt, "Copiar bloque " + (bi + 1), {txt: 1}) + "</section>";
    });
    var full = all.join("\n\n");
    h += "<details class='fold'><summary>Guion completo en un solo texto (" + full.length + " caracteres)</summary><div>" +
      "<p class='mut'>Para leerlo de corrido o generar todo de una vez. Por bloques es más fácil de sincronizar.</p>" + cb(full, "Copiar guion completo", {txt: 1}) + "</div></details>" +
      "<section class='panel'><h3>Subtítulos de tiempos para DaVinci (.srt)</h3>" +
      "<p class='prose'>Cada subtítulo empieza donde debe entrar una frase (" + String(VOICE.lead).replace(".", ",") + " s después del comienzo de su clip) y dura lo que tarda la voz en decirla. " +
      "En DaVinci Resolve: <b>File → Import → Subtitle</b>, arrástralo a la línea de tiempo y coloca cada frase de la voz sobre su subtítulo. También sirve como subtítulos para YouTube.</p>" +
      "<p><a class='btn' data-srt='1' download='E" + pad(ep.n) + "_tiempos_voz.srt' href='data:application/x-subrip;charset=utf-8," + encodeURIComponent(srt(ep)) + "'>Descargar E" + pad(ep.n) + "_tiempos_voz.srt</a> <span class='mut' aria-live='polite'></span></p>" +
      "<details class='fold'><summary>Ver o copiar el .srt (si la descarga no funciona, pégalo en un archivo de texto con extensión .srt)</summary><div>" + cb(srt(ep), "Copiar .srt", {txt: 1}) + "</div></details></section>" +
      "<details class='fold'><summary>Guion con tiempos e ID de cada toma, para el montaje</summary><div>" +
      "<p class='mut'>No lo pegues en ElevenLabs. Sirve para colocar cada frase bajo su clip.</p>" + cb(marks.join("\n"), "Copiar guion con tiempos", {txt: 1}) + "</div></details>";
    h += "<section class='panel'><h3>Efectos de sonido de este episodio</h3>" +
      "<p class='mut'>Genera cada uno en Sound Effects de ElevenLabs y colócalo en el montaje. Así la voz queda limpia y controlas el volumen.</p>" +
      ep.sfx.map(function (x) { return cb(x[1], "Copiar", {lab: x[0], ghost: 1}); }).join("") + "</section>" +
      "<details class='fold'><summary>Kit sonoro del canal (se hace una sola vez)</summary><div>" +
      KIT.map(function (x) { return x[1] === "ElevenLabs" ? cb(x[2], "Copiar", {lab: x[0] + " · ElevenLabs", ghost: 1}) : "<div class='rule'><b>" + esc(x[0]) + "<span class='src'>" + esc(x[1]) + "</span></b><span>" + esc(x[2]) + "</span></div>"; }).join("") + "</div></details>";
    h += "<section class='panel'><h3>Ficha científica</h3>" +
      "<p><span class='tag c" + ep.cert + "'>" + CERT[ep.cert][0] + "</span> " + esc(CERT[ep.cert][1]) + "</p>" +
      "<span class='lab'>Lo que afirma el guion</span>" + ul(ep.facts.map(esc)) +
      "<span class='lab'>Lo que simplificamos a propósito</span>" + ul(ep.simpl.map(esc)) +
      "<p class='note'><b>Antes de grabar:</b> confirma estos datos con dos fuentes y cítalas en la descripción. Es lo que separa un canal educativo de un video más.</p></section>";
    return h;
  }

  /* ---------- Vista: Tomas ---------- */
  function rail(s, badge) {
    return "<div class='rail'><b>" + s.id + "</b><span class='badge'>" + badge + "</span><span>" + tc(s.t0) + "–" + tc(s.t1) + "</span></div>";
  }
  function shotCard(ep, s) {
    var h;
    if (s.k === "S") {
      return "<article class='shot still'>" + rail(s, "Lámina · " + s.d + " s") + "<div class='body'>" +
        "<p class='vo'>" + esc(s.vo) + "</p><p class='es'><b>En pantalla:</b> " + esc(s.es) + "</p>" +
        "<p class='meta'><b>En la pizarra:</b> " + esc(cast(ep, s.tags)) + " · <b>La voz nombra:</b> " + esc(s.lab) + "</p>" + sizeLine(ep, s) +
        "<p class='mut'>Sin texto en pantalla: el video se publica en varios idiomas.</p>" + animFold({scene: s.scene}) + "</div></article>";
    }
    if (s.k === "K") {
      return "<article class='shot still'>" + rail(s, "Lámina del canal · 4 s") + "<div class='body'>" +
        "<p class='vo'>" + esc(s.vo) + "</p><p class='es'><b>En pantalla:</b> " + esc(s.es) + "</p>" +
        "<p class='meta'>" + esc(s.lab) + "</p>" +
        "<p class='note'><b>Ya la tienes:</b> es la misma en todos los episodios y se anima una sola vez (Elenco).</p></div></article>";
    }
    if (s.k === "R") {
      return "<article class='shot bank'>" + rail(s, "Reacción del banco · 8 s") + "<div class='body'>" + ppLine(s) +
        "<p class='vo'>" + esc(s.vo) + "</p><p class='es'><b>En pantalla:</b> " + esc(s.es) + "</p>" +
        "<p class='note'><b>Usa la reacción " + s.bid + " («" + esc(s.name) + "») del banco.</b> Ya está animada. Primero suena la frase en pipoplés y después entra el narrador.</p></div></article>";
    }
    h = "<article class='shot'>" + rail(s, "Toma · 8 s") + "<div class='body'>" +
      (s.zuum ? "<p class='pp'><b>Pipo y Plop:</b> «" + esc(ZUUM) + "» <span class='mut'>con el jingle del zoom</span></p>" : "") +
      "<p class='vo'>" + esc(s.vo) + "</p><p class='es'><b>En pantalla:</b> " + esc(s.es) + "</p>" +
      "<p class='meta'><b>En la toma:</b> " + esc(cast(ep, s.tags)) + " · <b>Cámara:</b> " + CAM[s.cam].es + " (" + CAM[s.cam].lente + " mm)</p>" + sizeLine(ep, s);
    if (s.from) h += "<p class='note'><b>Continúa</b> exactamente donde terminó " + s.from + ".</p>";
    if (s.open) h += "<p class='note'><b>La boca se abre</b> en esta toma (bostezo, lengua afuera).</p>";
    if (s.plop) h += "<p class='note'><span class='flag k'>¡plop!</span> Plop se hace bolita y suena el «¡plop!» del kit. Si la prueba es extrema, la voz recuerda que eso solo lo aguanta un tardígrado.</p>";
    return h + animFold(s) + "</div></article>";
  }
  function vTomas(ep) {
    var S = build(ep), c = count(ep);
    var h = "<section class='panel'><h2>Tomas · Ep. " + ep.n + " · " + esc(ep.topic) + "</h2>" +
      "<p class='mut'>" + c.gen + " tomas para animar, " + c.bank + " reacciones del banco y 5 láminas suman " + tc(c.dur) + ". Cada toma entra con la frase del narrador que la acompaña y pide una sola acción continua. Las reacciones del banco traen su frase en pipoplés.</p>" +
      "<div class='tl' aria-hidden='true'>" + BLOCKS.map(function (b, bi) {
        var L = S.filter(function (s) { return s.b === bi; }), sp = blockSpan(ep, bi);
        return "<div class='tb' style='flex:" + (sp[1] - sp[0]) + "'><div class='seg'>" +
          L.map(function (s) { return "<i class='" + (s.k === "C" ? "" : s.k === "R" ? "r" : "s") + "' style='flex:" + s.d + "'></i>"; }).join("") +
          "</div><small>" + tc(sp[0]) + "</small></div>";
      }).join("") + "</div>" +
      "<p class='legend'><span><i></i>Toma para animar</span><span><i class='r'></i>Reacción del banco</span><span><i class='s'></i>Lámina</span></p>" +
      "<div class='row' role='group' aria-label='Filtrar por bloque'>" +
      "<button class='chip' data-b='-1' aria-pressed='" + (blk === -1) + "'>Todos</button>" +
      BLOCKS.map(function (b, bi) { return "<button class='chip' data-b='" + bi + "' aria-pressed='" + (blk === bi) + "'>" + (bi + 1) + " · " + esc(b[0]) + "</button>"; }).join("") +
      "</div></section>";
    BLOCKS.forEach(function (b, bi) {
      if (blk > -1 && blk !== bi) return;
      var sp = blockSpan(ep, bi);
      h += "<h3>Bloque " + (bi + 1) + " · " + esc(b[0]) + " · " + tc(sp[0]) + "–" + tc(sp[1]) + "</h3>";
      S.forEach(function (s) { if (s.b === bi) h += shotCard(ep, s); });
    });
    return h;
  }

  /* ---------- Vista: Elenco y utilería ---------- */
  var BANK_TOTAL = Object.keys(BANK).length + 2;
  function bankItem(code) {
    var B = BANK[code], P = PIPOPLES[code], id = bankId(code), on = bankDone.indexOf(id) > -1;
    return "<div class='bitem'><label class='step" + (on ? " on" : "") + "'><input type='checkbox' id='bk-" + id + "' data-bank='" + id + "'" + (on ? " checked" : "") + "><div><b>" + id + " · " + esc(B[0]) + " · «" + esc(P[0]) + "»</b><span>" + esc(B[1]) + " " + CAM[B[2]].es + ". Etiqueta de voz: " + esc(P[2]) + ".</span></div></label>" +
      animFold({scene: B[3], act: B[4]}) + "</div>";
  }
  function cardItem(k) {
    var K = CARDS[k], id = k === "T" ? "CANAL_INICIO" : "CANAL_FINAL", on = bankDone.indexOf(id) > -1;
    return "<div class='bitem'><label class='step" + (on ? " on" : "") + "'><input type='checkbox' id='bk-" + id + "' data-bank='" + id + "'" + (on ? " checked" : "") + "><div><b>" + id + " · " + esc(K[0]) + "</b><span>" + esc(K[1]) + " " + esc(K[4]) + "</span></div></label>" +
      animFold({scene: K[2]}) + "</div>";
  }
  function who(k, papel) {
    var w = WHO[k];
    return "<section class='panel'><h3>" + w.es + " · " + esc(w.rol) + (papel ? " · " + papel : "") + "</h3><p>" + esc(w.bio) + "</p>" +
      "<p class='meta'><b>Aspecto:</b> " + esc(w.look) + "</p>" +
      "<p class='meta'><b>Voz en ElevenLabs:</b> " + esc(w.voz.es) + " ID " + w.voz.id + ".</p>" +
      "<details class='alt'><summary>Descripción de la lámina aprobada (referencia del modelado)</summary><div>" + cb(w.p, "Copiar descripción", {txt: 1}) + "</div></details></section>";
  }
  function vElenco(ep) {
    var P = [], L = [], S = build(ep);
    Object.keys(BANK).forEach(function (k) { (k.charAt(0) === "P" ? P : L).push(k); });
    var h = "<section class='panel'><h2>Elenco y utilería · Ep. " + ep.n + " · " + esc(ep.topic) + "</h2>" +
      "<p class='secret'>Pipo y Plop están siempre presentes.</p>" +
      "<p class='prose'>" + WHO[ep.star].es + " protagoniza este episodio y " + WHO[coOf(ep)].es + " lo acompaña con sus reacciones del banco. En Blender son siempre los mismos modelos, así que pueden compartir toma cuando la historia lo pide.</p></section>";
    h += who(ep.star, "protagonista") + who(coOf(ep), "acompaña");
    h += "<h2>Objetos del episodio</h2><p class='mut'>Se modelan en plastilina mate, con huellas, a su tamaño junto al títere (unos 30 cm).</p>";
    Object.keys(ep.objs).forEach(function (k) {
      var o = ep.objs[k], z = SIZES[o.z];
      var en = S.filter(function (s) { return (s.k === "C" || s.k === "S") && (s.tags || "").indexOf(k) > -1; }).map(function (s) { return s.id.split("_")[1]; });
      h += "<section class='panel'><h3>" + esc(o.es) + "</h3>" +
        "<p class='meta'><b>Tamaño:</b> " + z[0] + ", " + esc(z[1]) + " de " + WHO[ep.star].es + ". <b>Aparece en:</b> " + (en.join(", ") || "ninguna toma") + ".</p>" +
        "<details class='alt'><summary>Referencia para modelarlo (en inglés)</summary><div>" + cb(o.p, "Copiar referencia", {txt: 1}) + "</div></details></section>";
    });
    h += "<section class='panel'><h2>Banco del canal</h2>" +
      "<p class='prose'>Veinte reacciones y dos láminas. Se animan una sola vez en Blender y sirven para los 52 episodios. Cada reacción tiene su frase fija en pipoplés: el niño la reconoce y la repite. Marca cada pieza cuando esté lista.</p>" +
      "<ul class='stats'><li id='bank-count'>" + bankDone.length + " de " + BANK_TOTAL + " piezas listas</li></ul></section>" +
      "<details class='fold'><summary>Reacciones de Pipo · " + P.length + "</summary><div>" + P.map(bankItem).join("") + "</div></details>" +
      "<details class='fold'><summary>Reacciones de Plop · " + L.length + "</summary><div>" + L.map(bankItem).join("") + "</div></details>" +
      "<details class='fold'><summary>Láminas del canal · cortinilla y tarjeta final</summary><div>" + cardItem("T") + cardItem("F") + "</div></details>";
    return h;
  }

  /* ---------- Vista: Producción 3D ---------- */
  function rule(a) { return "<div class='rule'><b>" + esc(a[0]) + (a[2] ? "<span class='src'>" + a[2] + "</span>" : "") + "</b><span>" + esc(a[1]) + "</span></div>"; }
  var CMDS = [
    "# Mide tu PC: segundos por fotograma y horas por episodio",
    "blender -b -P benchmark.py",
    "",
    "# El laboratorio con la calidad completa de tu tarjeta",
    "blender -b -P escena_demo.py -- --calidad final --salida C:\\pipo_plop\\render\\laboratorio.png",
    "",
    "# Monta un episodio (aquí el 1) y su storyboard de 39 tomas",
    "blender -b -P episodio.py -- --ep 1 --guardar C:\\pipo_plop\\ep01_layout.blend --storyboard C:\\pipo_plop\\storyboard_ep01",
    "",
    "# Lámina de un personaje, para compararla con la aprobada",
    "blender -b -P lamina.py -- --personaje pipo --salida C:\\pipo_plop\\render\\lamina_pipo.png",
    "",
    "# Las 9 bocas de un personaje",
    "blender -b -P hoja_bocas.py -- --personaje plop --carpeta C:\\pipo_plop\\render\\bocas_plop"
  ].join("\n");
  function vProd() {
    var h = "<section class='panel'><h2>Producción 3D en Blender</h2>" +
      "<p class='secret'>Plastilina digital: se hace en 3D, pero tiene que parecer plastilina hecha a mano.</p>" +
      "<p class='prose'>Todo se modela, se anima y se renderiza en Blender, en tu computadora. No se usa video generado por IA. Las voces se generan en ElevenLabs y el montaje se hace en DaVinci Resolve.</p></section>";
    h += "<section class='panel'><h3>Lo que necesitas</h3>" +
      ul(["<b>Blender 5.2 LTS</b> y el NVIDIA Studio Driver.",
          "<b>El proyecto 3D</b> (carpeta pipo_plop_3d): los scripts de Blender, el idioma, la matriz de los 52 episodios y el sonido. Su LEEME explica la instalación en Windows.",
          "<b>Rhubarb Lip Sync</b> para las bocas desde la voz grabada.",
          "<b>DaVinci Resolve</b> para el montaje y <b>ElevenLabs</b> para las voces.",
          "<b>Tu equipo:</b> Intel i7-14700F, RTX 5060 Ti de 8 GB y Windows 11. Amplía la RAM a 32 GB."]) +
      "<p class='mut'>Primeros comandos, desde la carpeta blender del proyecto 3D:</p>" + cb(CMDS, "Copiar comandos", {txt: 1}) + "</section>";
    h += "<section class='panel'><h3>El estilo de plastilina</h3>" +
      ul(["Material mate con huellas dactilares, marcas de herramienta y colores sólidos.",
          "<i>Boiling</i>: la superficie vibra apenas entre fotogramas, como en la plastilina real.",
          "Animado de a dos: 12 poses por segundo dentro de un video de 24 fotogramas por segundo.",
          "Las luces parpadean apenas, como en un set de verdad.",
          "Todo es plastilina: gotas, vapor, luz, sonido y electricidad también son piezas de arcilla, nunca humo ni partículas.",
          "Dentro de las cosas, cada sustancia lleva siempre el mismo color y la misma forma, en una paleta de colores que transmiten calma."]) +
      "<div class='scroll'><table><thead><tr><th>Elemento</th><th>Color</th></tr></thead><tbody>" +
      [["Pipo", "Azul verdoso #096B7C"], ["Chaleco de Pipo", "Mostaza #D08316"], ["Plop", "Verde lima #578B27"], ["Pajarita de Plop", "Naranja terracota #AD410E"],
       ["Paredes y suelo del laboratorio", "Azul claro, para dar calma"], ["Muebles, objetos y luces", "Colores vivos, para llamar la atención"]]
        .map(function (r) { return "<tr><td>" + r[0] + "</td><td>" + r[1] + "</td></tr>"; }).join("") + "</tbody></table></div></section>";
    h += "<section class='panel'><h3>El laboratorio</h3>" +
      "<p class='prose'>Un solo set grande con rincones que se reutilizan todo el año. La imagen es la referencia del azul claro de las paredes y el suelo.</p>" +
      "<img class='fondo' src='" + FONDO_IMG + "' alt='Referencia de color del laboratorio: azul claro, más luminoso en el centro y en el suelo' width='2000' height='1116'>" +
      "<p><a class='btn' download='fondo_canal.jpg' href='" + FONDO_IMG + "'>Descargar la referencia de color</a></p>" +
      "<div class='scroll'><table><thead><tr><th>Zona</th><th>Para qué</th></tr></thead><tbody>" +
      ZONAS.map(function (z) { return "<tr><td>" + z[0] + "</td><td>" + z[1] + "</td></tr>"; }).join("") + "</tbody></table></div></section>";
    h += "<section class='panel'><h3>Cámaras</h3><div class='scroll'><table><thead><tr><th>Código</th><th>Plano</th><th>Lente</th><th>Movimiento</th></tr></thead><tbody>" +
      Object.keys(CAM).map(function (k) { return "<tr><td>" + k + "</td><td>" + CAM[k].es + "</td><td>" + CAM[k].lente + " mm</td><td>" + esc(CAM[k].mov) + "</td></tr>"; }).join("") +
      "</tbody></table></div></section>";
    h += "<section class='panel'><h3>Escala</h3><p class='prose'>Pipo y Plop miden unos 30 cm. Cada objeto tiene su tamaño junto a ellos, y la pestaña Tomas lo recuerda en cada toma.</p>" +
      "<div class='scroll'><table><thead><tr><th>Tamaño</th><th>Medida</th></tr></thead><tbody>" +
      Object.keys(SIZES).map(function (k) { return "<tr><td>" + SIZES[k][0] + "</td><td>" + SIZES[k][1].replace(/\{N\}/g, "el títere") + "</td></tr>"; }).join("") +
      "</tbody></table></div></section>";
    h += "<section class='panel'><h3>Animación</h3>" +
      ul(["<b>Una sola acción por toma,</b> la que dice su indicación de animación. Cámara fija; si la cámara se acerca, el sujeto se queda quieto.",
          "<b>Las reacciones del banco</b> se animan una vez y se reutilizan: son gestos que el niño reconoce.",
          "<b>Las bocas:</b> nueve bocas de reemplazo, solo cuando Pipo y Plop hablan pipoplés. Con el narrador, la boca se queda cerrada.",
          "<b>El «¡plop!»:</b> cuando una toma lo marca, Plop se hace bolita, como los tardígrados reales, y vuelve a su forma.",
          "<b>Tomas encadenadas:</b> algunas continúan exactamente donde terminó otra. La pestaña Tomas lo indica."]) + "</section>";
    h += "<section class='panel'><h3>Contenido para niños de 5 años en adelante</h3>" +
      "<p class='prose'>Los guiones cumplen estas reglas y el validador del repositorio las comprueba. Úsalas para revisar cada toma antes de renderizarla.</p>" +
      SAFE.map(rule).join("") + "</section>";
    h += "<section class='panel'><h3>Render y entrega</h3>" +
      ul(["<b>EEVEE</b> para todas las tomas; <b>Cycles</b> solo para la miniatura y algún plano destacado.",
          "1920×1080 a 24 fotogramas por segundo. Se renderizan solo los fotogramas únicos y se duplican al montar.",
          "Cada toma se nombra con su ID (E01_C01, E01_L1…), igual que en la pestaña Tomas.",
          "La primera vez, mide con benchmark.py cuánto tarda tu tarjeta por episodio, y con el piloto (Ep. 1) cuánto tardas en animarlo."]) + "</section>";
    return h;
  }

  /* ---------- Vista: Canal ---------- */
  function vCanal() {
    var ep = EP[0];
    var h = "<section class='panel'><h2>El canal</h2>" +
      "<p class='secret'>No basta con preguntar por qué: Pipo y Plop se meten dentro de la respuesta.</p>" +
      ul(["<b>Para quién:</b> niños de 6 a 8 años, y cada episodio se escribe para uno de 7. Así llega de 5 a 9: los pequeños ven lo que ven los mayores, y a los mayores no les parece de bebés.",
          "<b>Qué se llevan:</b> entender por qué pasa algo que ven todos los días, reírse mientras lo descubren y un reto para probarlo en casa.",
          "<b>Qué le damos a los padres:</b> ciencia verificada, un ritmo que estimula sin sobreestimular y un reto para hacer juntos."]) + "</section>";
    h += "<section class='panel'><h3>Lo que hace única a la serie</h3>" +
      ul(["<b>Pipo es un extraterrestre:</b> para él todo en la Tierra es un misterio, y eso hace que pregunte lo mismo que el niño.",
          "<b>El zoom:</b> se entra dentro de las cosas para ver por qué pasan, en plastilina.",
          "<b>Plop es indestructible:</b> la prueba puede salir muy mal y ser muy divertida.",
          "<b>Un idioma propio:</b> Pipo y Plop hablan pipoplés, así que el mismo episodio sirve en todos los países. Las canciones también son en pipoplés.",
          "<b>El método científico como ritual:</b> pregunta, idea, prueba y reto, siempre en el mismo orden."]) + "</section>";
    h += "<section class='panel'><h3>Los personajes</h3>" +
      ["P", "L"].map(function (k) { return "<div class='rule'><b>" + WHO[k].es + "<span class='src'>" + esc(WHO[k].rol) + "</span></b><span>" + esc(WHO[k].bio) + "</span></div>"; }).join("") +
      "<div class='rule'><b>El narrador<span class='src'>El creador del canal</span></b><span>De niño descubrió el laboratorio y se hizo amigo de Pipo y Plop. Hoy, de adulto, guarda su secreto, les ayuda a entender la Tierra y explica la ciencia. Nunca sale en pantalla y es la única voz que cambia de idioma.</span></div></section>";
    h += "<section class='panel'><h3>Cómo habla el narrador</h3>" +
      ul(["Suena a cómplice, no a maestro ni a documental: cálido, con humor y con asombro propio.",
          "Habla con el niño y también con Pipo y Plop, y ellos le contestan en pipoplés. A veces le hacen caso y a veces no: «Pipo, no toques eso…».",
          "Pregunta y espera: deja dos o tres segundos para que el niño responda a la pantalla.",
          "La imagen muestra la acción; la voz explica qué significa. No narra lo que ya se ve.",
          "Las ideas de Pipo son hipótesis: se ponen a prueba y se descartan con una razón, nunca con burla. Cuando Pipo cree que algo funciona «como en su planeta», el narrador aclara cómo funciona en la Tierra.",
          "Las preguntas de Plop son las del espectador. La voz las celebra y las responde en la prueba.",
          "Cuando a Plop le pasa algo extremo, recuerda que eso solo lo aguanta un osito de agua.",
          "Habla de tú: mira, fíjate, piénsalo, ¿tú qué crees? Una idea por frase y 18 palabras como máximo.",
          "Toda palabra nueva llega con una comparación conocida: casco, renacuajo, puerta, panal."]) + "</section>";
    h += "<section class='panel'><h3>El pipoplés</h3>" +
      "<p class='prose'>El idioma inventado de Pipo y Plop: no tiene palabras de ningún idioma real, así que la serie nunca se dobla. El sentido lo dan la entonación, la cara y el cuerpo. Pipo usa sílabas con p, b y t, rápidas y con energía; Plop, con pl, l, m y n, suaves y pausadas. El pipoplés nunca explica la ciencia: eso lo hace el narrador.</p>" +
      "<div class='scroll'><table><thead><tr><th>Código</th><th>Intención</th><th>Frase</th></tr></thead><tbody>" +
      Object.keys(PIPOPLES).map(function (k) { return "<tr><td>" + k + "</td><td>" + esc(PIPOPLES[k][1]) + "</td><td>" + esc(PIPOPLES[k][0]) + "</td></tr>"; }).join("") +
      "<tr><td>Zoom</td><td>Los dos, en el momento del zoom</td><td>" + esc(ZUUM) + "</td></tr></tbody></table></div>" +
      "<p class='mut'>Toda palabra nueva pasa por el revisor del proyecto 3D (idioma.py) y por un hablante nativo de cada idioma.</p></section>";
    h += "<section class='panel'><h3>Los momentos firma</h3>" +
      ul(["<b>La llegada del misterio:</b> el objeto aparece en el laboratorio, gigante y misterioso.",
          "<b>La idea loca de Pipo,</b> con su «¡Bipi-ba!»: casi siempre está mal, y eso es lo divertido.",
          "<b>La pausa para pensar:</b> «¿Tú qué crees? Piénsalo…», y el narrador espera de verdad.",
          "<b>«¡Hagamos zoom!»</b> y el «¡Zuuum!» de Pipo y Plop, con su jingle: el momento que solo tiene este canal.",
          "<b>El «¡plop!»:</b> Plop se hace bolita cuando la prueba sale mal.",
          "<b>El reto:</b> el «¡Tu-lu, tu-lu!» de Plop invita a probarlo en casa.",
          "«La ciencia está en todas partes. ¡Hasta el próximo misterio!»"]) +
      "<p class='mut'>Los niños vuelven por lo que reconocen. No se cambian nunca.</p></section>";
    h += "<section class='panel'><h3>Los cinco minutos, bloque por bloque</h3><div class='scroll'><table><thead><tr><th>Bloque</th><th>Tiempo</th><th>Para qué sirve</th><th>Qué sostiene la atención</th></tr></thead><tbody>" +
      BLOCKS.map(function (b, i) { var sp = blockSpan(ep, i); return "<tr><td>" + (i + 1) + " · " + esc(b[0]) + "</td><td>" + tc(sp[0]) + "–" + tc(sp[1]) + "</td><td>" + esc(b[1]) + "</td><td>" + esc(b[2]) + "</td></tr>"; }).join("") +
      "</tbody></table></div></section>";
    h += "<section class='panel'><h3>Título y miniatura</h3>" +
      ul(["<b>Título:</b> la pregunta tal como la diría un niño, con la palabra clave al principio y menos de 60 caracteres. Se traduce en cada idioma.",
          "<b>Miniatura:</b> una sola cara con una expresión exagerada, un objeto gigante y un fondo liso y saturado.",
          "Sin palabras, o solo una onomatopeya que se entienda en cualquier idioma: la misma miniatura se ve en los 5 idiomas.",
          "Pipo o Plop según el protagonista del episodio, para que el niño reconozca a su personaje.",
          "Debe leerse en un móvil pequeño y a tres metros del televisor. Los primeros segundos del video cumplen lo que promete."]) + "</section>";
    h += "<section class='panel'><h3>Publicación</h3>" +
      ul(["<b>Audiencia:</b> «Sí, es contenido para niños». Un canal dirigido a niños debe marcarlo.",
          "Eso desactiva los comentarios, las tarjetas, las pantallas finales, la campana y los anuncios personalizados. El canal crece por búsquedas, recomendaciones, YouTube Kids y Shorts.",
          "Por eso el guion nunca pide comentar ni suscribirse. El cierre anuncia la siguiente pregunta y la lista de la temporada reproduce el siguiente episodio.",
          "<b>Un solo canal con pistas de audio en varios idiomas,</b> si el canal tiene esa función: así todas las vistas se suman en un mismo lugar.",
          "La descripción lleva capítulos, reto, palabras nuevas y fuentes. Es lo que leen padres y docentes, y cada episodio puede tener su hoja imprimible para la escuela.",
          "Di en la descripción que la animación está hecha en Blender y que las voces se generan con ElevenLabs."]) +
      "<p class='mut'>Ayuda de YouTube: " + link("https://support.google.com/youtube/answer/9527654", "audiencia del canal o del video") + " y " + link("https://support.google.com/youtube/answer/10774223", "buenas prácticas para contenido infantil y familiar") + ".</p></section>";
    h += "<div class='two'><section class='panel do'><h3>Lo que YouTube premia en contenido infantil</h3>" +
      ul(["Aprender y despertar la curiosidad.", "Creatividad, juego e imaginación.", "Ser buena persona.", "Conexión con el mundo real.", "Diversidad e inclusión."]) + "</section>" +
      "<section class='panel dont'><h3>Lo que castiga</h3>" +
      ul(["Contenido muy comercial.", "Conductas o actitudes negativas.", "Contenido educativo engañoso.", "Lo que dificulta la comprensión.", "Lo sensacionalista.", "Uso extraño de personajes infantiles."]) + "</section></div>" +
      "<p class='note'><b>Contexto de 2026:</b> más de 200 organizaciones pidieron a YouTube frenar el contenido infantil hecho con IA de baja calidad. Una serie animada a mano en Blender, con ciencia verificada y fuentes a la vista, queda del lado correcto de esa discusión.</p>";
    h += "<section class='panel'><h3>Ritmo de trabajo</h3>" +
      ul(["<b>Antes de estrenar:</b> la canción, el banco de reacciones, de 6 a 8 episodios terminados y unos 20 Shorts. Un canal infantil que falla en su ritmo semanal pierde el impulso.",
          "<b>Después:</b> uno por semana, el mismo día y a la misma hora.",
          "<b>Shorts:</b> 2 o 3 por episodio, de menos de un minuto: el zoom, el «¡plop!» y el dato extra.",
          "<b>Compilaciones</b> de 30 a 60 minutos por temporada o por tema: muchos niños ven YouTube en la tele.",
          "<b>Temporada 1 de 13 episodios.</b> Con lo que enseñe el piloto se decide el ritmo de las siguientes."]) + "</section>";
    h += "<section class='panel'><h3>Qué mirar en YouTube Studio</h3>" +
      ul(["<b>Clics por impresión por debajo del 4 %:</b> cambia la miniatura y el título.",
          "<b>Retención a los 30 s por debajo del 70 %:</b> el misterio no atrapa en los primeros segundos.",
          "<b>Caída en el zoom o en la prueba:</b> el centro del episodio no está funcionando.",
          "<b>Qué Shorts llevan a ver episodios completos,</b> y qué temas y ganchos se ven más, para orientar la temporada siguiente.",
          "<b>Porcentaje visto en televisor:</b> si sube, las familias lo están viendo juntas."]) +
      "<p class='mut'>Son referencias orientativas para un canal nuevo, no reglas de YouTube.</p></section>";
    return h;
  }

  /* ---------- Vista: Plan anual ---------- */
  function planRow(ep) {
    var tags = "<span class='tag'>" + CATS[ep.cat] + "</span>" +
      ep.mot.split("").map(function (k) { return "<span class='tag m'>" + MOTORS[k][0] + "</span>"; }).join("") +
      (ep.anc ? "<span class='tag a'>Ancla</span>" : "") + (ep.cert > 1 ? "<span class='tag c" + ep.cert + "'>" + CERT[ep.cert][0] + "</span>" : "") +
      (ep.lore ? "<span class='tag st'>Guion al día con el Lore</span>" : "") + "<span class='tag st'>" + status(ep) + "</span>";
    var rows = [["Por qué engancha", ep.why], ["Respuesta", ep.secret], ["Reto en casa", ep.reto], ["Conecta con", ep.link], ["Nota de producción", ep.nota],
                ["Certeza", CERT[ep.cert][0] + ". " + CERT[ep.cert][1]]];
    var i = EP.indexOf(ep);
    return "<details class='ep'><summary><span class='num'>" + pad(ep.n) + "</span><span class='q'>" + esc(ep.title) + "</span>" + tags + "</summary><div>" +
      "<p class='mut'>Protagonista: " + WHO[ep.star].es + " · Miniatura: «" + esc(ep.thumb) + "» · " + count(ep).gen + " tomas para animar</p><dl class='ficha'>" +
      rows.filter(function (r) { return r[1]; }).map(function (r) { return "<dt>" + r[0] + "</dt><dd>" + esc(r[1]) + "</dd>"; }).join("") + "</dl>" +
      "<div class='pick'><button class='btn' data-go='" + i + ":guia'>Guía</button><button class='btn ghost' data-go='" + i + ":guion'>Guion</button>" +
      "<button class='btn ghost' data-go='" + i + ":tomas'>Tomas</button><button class='btn ghost' data-go='" + i + ":elenco'>Elenco</button></div></div></details>";
  }
  function planList() {
    var q = plain(pq.trim());
    var show = EP.filter(function (e) {
      return (!pc || (pc === "anc" ? e.anc : e.cat === pc)) && (!pm || e.mot.indexOf(pm) > -1) &&
        (!q || plain(e.title + " " + e.topic + " " + e.secret + " " + e.vocab + " " + e.syn).indexOf(q) > -1);
    });
    var h = (pc || pm || q ? "<p class='mut'>" + show.length + " de " + EP.length + " episodios con este filtro.</p>" : "");
    SEASONS.forEach(function (s) {
      var L = show.filter(function (e) { return e.n >= s[1] && e.n <= s[2]; });
      if (!L.length) return;
      h += "<h3>" + s[0] + " · episodios " + s[1] + " a " + s[2] + "</h3><p class='mut'>" + esc(s[3]) + "</p><div class='eps'>" + L.map(planRow).join("") + "</div>";
    });
    return h || "<p class='mut'>Ningún episodio coincide. Prueba con otra palabra.</p>";
  }
  function vPlan() {
    var nSt = {s: 0, p: 0, d: 0};
    EP.forEach(function (e) { var n = chk(e).length; if (!n) nSt.s++; else if (n >= TOTAL) nSt.d++; else nSt.p++; });
    var nc = {1: [], 2: [], 3: []};
    EP.forEach(function (e) { nc[e.cert].push(e.n); });
    var h = "<section class='panel'><h2>Plan anual: " + EP.length + " episodios</h2>" +
      "<p class='prose'>Un episodio por semana durante un año, en cuatro temporadas de 13. Todos están desarrollados toma por toma: abre cualquiera con sus botones o con el selector de arriba.</p>" +
      "<ul class='stats'><li>Sin empezar: " + nSt.s + "</li><li>En producción: " + nSt.p + "</li><li>Publicados: " + nSt.d + "</li></ul>" +
      "<label class='lab' for='plan-q'>Buscar</label><input id='plan-q' class='search' type='search' placeholder='Tema, palabra o pregunta' value='" + esc(pq) + "'>" +
      "<span class='lab'>Categoría</span><div class='row' role='group' aria-label='Filtrar por categoría'>" +
      "<button class='chip' data-pc='' aria-pressed='" + (pc === "") + "'>Todas</button>" +
      "<button class='chip' data-pc='anc' aria-pressed='" + (pc === "anc") + "'>Anclas</button>" +
      Object.keys(CATS).map(function (k) { return "<button class='chip' data-pc='" + k + "' aria-pressed='" + (pc === k) + "'>" + CATS[k] + "</button>"; }).join("") + "</div>" +
      "<span class='lab'>Motor de interés</span><div class='row' role='group' aria-label='Filtrar por motor de interés'>" +
      "<button class='chip' data-pm='' aria-pressed='" + (pm === "") + "'>Todos</button>" +
      Object.keys(MOTORS).map(function (k) { return "<button class='chip' data-pm='" + k + "' aria-pressed='" + (pm === k) + "'>" + MOTORS[k][0] + "</button>"; }).join("") + "</div></section>";
    h += "<details class='fold'><summary>Evaluación científica de los episodios</summary><div>" +
      "<p>Cada episodio tiene, en su pestaña Guion, una ficha con los datos que afirma, lo que simplifica a propósito y su nivel de certeza.</p>" +
      [1, 2, 3].map(function (k) {
        return "<div class='rule'><b><span class='tag c" + k + "'>" + CERT[k][0] + "</span><span class='src'>" + nc[k].length + " episodios</span></b><span>" + CERT[k][1] +
          (k > 1 && nc[k].length ? " Episodios: " + nc[k].join(", ") + "." : "") + "</span></div>";
      }).join("") +
      "<h3>Correcciones hechas al evaluar</h3>" +
      ul(["<b>Ep. 3:</b> las aves sí tienen el sensor del picante, pero no responde a la capsaicina.",
          "<b>Ep. 4:</b> el «hip» lo produce el cierre de las cuerdas vocales (la glotis), no la epiglotis.",
          "<b>Ep. 5:</b> el agua no es la única sustancia que se expande al congelarse.",
          "<b>Ep. 10:</b> se quitó la edad exacta a la que los gatitos dominan el giro, porque no se pudo confirmar.",
          "<b>Ep. 19:</b> en órbita la gravedad no desaparece. Los astronautas caen todo el tiempo.",
          "<b>Ep. 22:</b> los 300 millones de sensores de olor son de los sabuesos. El guion dice «entre cien y trescientos millones, según la raza».",
          "<b>Ep. 25:</b> el chicle no se queda siete años en el cuerpo.",
          "<b>Ep. 28:</b> las mariposas forman crisálida. El capullo de seda es de las polillas.",
          "<b>Ep. 31:</b> se descarta la explicación de que el aire de arriba del ala «recorre más camino».",
          "<b>Ep. 33:</b> el mecanismo exacto del cerebro congelado sigue en estudio. El guion dice «los científicos creen».",
          "<b>Ep. 38:</b> para qué sirven los dedos arrugados sigue en discusión: hay estudios a favor y en contra del mejor agarre.",
          "<b>Ep. 40:</b> se quitó que el bostezo se contagia más entre quienes se quieren: la relación con la empatía está en discusión.",
          "<b>Ep. 44:</b> se añadió la capa aceitosa de las patas de la araña, descrita en un estudio de 2012.",
          "<b>Ep. 45:</b> la nube no flota por ser «más ligera que el aire»: la sostienen las corrientes que suben y lo despacio que caen sus gotitas.",
          "<b>Ep. 48:</b> el camaleón cambia de color para comunicarse. Que también regule así su temperatura es solo una hipótesis.",
          "<b>Ep. 49:</b> el conflicto entre el oído y la vista es la explicación más aceptada del mareo, no un hecho demostrado. El guion dice «los científicos creen».",
          "<b>Ep. 52:</b> dormir más no hace crecer más. Lo que está demostrado es que gran parte de la hormona del crecimiento se libera en el sueño profundo."]) +
      "<p class='note'><b>Alcance:</b> la evaluación se hizo con conocimiento científico general y comprobaciones puntuales en la web en noviembre de 2026. No sustituye la revisión de un especialista. Verifica cada ficha con dos fuentes antes de grabar.</p></div></details>";
    h += "<details class='fold'><summary>Cómo se eligieron los temas</summary><div><p>Cada tema pasó por siete preguntas:</p>" +
      ul(["<b>¿Es una pregunta que un niño ya hace?</b> Si hay que convencerlo de que es interesante, no sirve.",
          "<b>¿Le pasa a él,</b> en su cuerpo, en su casa o con su mascota?",
          "<b>¿Despierta una emoción fuerte y segura?</b> Risa, asombro, un «¡puaj!» divertido o un poco de suspenso. Nunca miedo de verdad ni una imagen desagradable.",
          "<b>¿La respuesta está escondida dentro de algo?</b> Eso permite el zoom y sostiene la intriga hasta la mitad del video.",
          "<b>¿Deja un dato para contar?</b> Lo que el niño repite en la cena es lo que trae al siguiente espectador.",
          "<b>¿Tiene un reto que se puede hacer hoy,</b> sin riesgo?",
          "<b>¿Se puede mostrar con cuatro objetos de arcilla o menos?</b>"]) +
      "<p>Y un adulto tiene que poder decir que sí: los padres deciden qué se queda en la pantalla.</p>" +
      "<h3>En qué se apoya</h3>" +
      ul(["Los estudios sobre las preguntas que los niños envían por su cuenta a científicos encuentran que la biología, es decir, el cuerpo y los animales, está entre lo que más preguntan. Por eso casi la mitad de los temas son de cuerpo o de animales. " + link("https://informalscience.org/research/using-questions-sent-ask-scientist-site-identify-childrens-interests-science/", "Baram-Tsabari y otros, 2006") + ".",
          "En una encuesta a 2.000 padres, entre las preguntas que más temían estaban por qué el cielo es azul y cómo se sostienen los aviones en el aire. Las dos están en el plan como anclas. " + link("https://www.publico.es/actualidad/cielo-azul-preguntas-padres-temen.html", "Público, 2012") + ".",
          "Un estudio de 2026 sobre 32.000 videos infantiles de YouTube halló que el movimiento en pantalla aumenta las vistas, pero que el movimiento de fondo se lleva la atención sin mejorar el aprendizaje. En este formato el fondo es azul claro, liso y quieto: lo único que se mueve es lo que se explica. " + link("https://digitallearning.eletsonline.com/2026/11/isb-study-visual-motion-children-educational-videos-youtube-attention/", "Estudio de ISB") + ".",
          "Una revisión de más de mil videos educativos encontró que menos de la mitad tenía personajes con los que conectar. Aquí cada episodio tiene dos, con papeles fijos. " + link("https://www.sri.com/press/story/sri-researchers-watched-over-1000-youtube-videos-for-kids-and-this-is-what-they-learned/", "SRI") + ".",
          "Entre los 4 y los 8 años prefieren dibujos y juguetes; a los 9 y 10 empiezan a buscar manualidades y videos educativos. El humor de Pipo habla a los pequeños; los retos, a los mayores. " + link("https://onlinelibrary.wiley.com/doi/10.1155/hbe2/2499878", "Yadav y otros, 2025") + "."]) +
      "<p class='note'><b>Lo que este plan no es:</b> un pronóstico de vistas. Es un criterio editorial apoyado en esos estudios. Tus datos mandan: cada seis episodios, mira en YouTube Studio qué motor retuvo mejor y adelanta dos episodios de ese tipo.</p></div></details>";
    h += "<details class='fold'><summary>Los siete motores de interés</summary><div><p class='mut'>Cada episodio lleva uno o dos. Dicen por qué un niño de esta edad hace clic, se queda y lo cuenta después.</p>" +
      Object.keys(MOTORS).map(function (k) {
        var n = EP.filter(function (e) { return e.mot.indexOf(k) > -1; }).length;
        return "<div class='rule'><b>" + MOTORS[k][0] + "<span class='src'>" + n + " episodios</span></b><span>" + MOTORS[k][1] + "</span></div>";
      }).join("") + "</div></details>";
    h += "<details class='fold'><summary>Cómo está ordenado el año</summary><div>" +
      ul(["Un episodio por semana: 52 semanas, cuatro temporadas de 13.",
          "Nunca hay dos episodios seguidos de la misma categoría. La variedad es lo que mantiene viva la lista de reproducción.",
          "Pipo protagoniza los episodios impares y Plop los pares. El otro siempre lo acompaña: con sus reacciones del banco y, cuando la historia lo pide, en sus propias tomas.",
          "Las preguntas ancla, las que se buscan todo el año, están repartidas en las cuatro temporadas y se concentran al principio, cuando el canal más necesita que lo encuentren.",
          "Los episodios se llaman entre sí. El volcán recuerda a las palomitas; las burbujas, al jabón; el barco, al hielo. El niño siente que ya sabe algo, y eso lo hace volver.",
          "Algunos episodios son de calendario y se pueden mover: murciélagos y arañas para Halloween, el mar para las vacaciones, la Luna antes de un eclipse. Si mueves uno, cuida que no queden juntos dos de la misma categoría.",
          "Dos temas tienen ciencia todavía abierta, los sueños y los bostezos. El guion lo dice: no saberlo todo también es ciencia."]) + "</div></details>";
    return h + "<div id='plan-list'>" + planList() + "</div>";
  }

  /* ---------- Selector de episodio y pintado ---------- */
  function picker() {
    var h = "";
    SEASONS.forEach(function (s) {
      var L = EP.filter(function (e) { return e.n >= s[1] && e.n <= s[2]; });
      if (!L.length) return;
      h += "<optgroup label='" + s[0] + "'>" + L.map(function (e) {
        var n = chk(e).length;
        return "<option value='" + EP.indexOf(e) + "'" + (EP.indexOf(e) === cur ? " selected" : "") + ">" + pad(e.n) + " · " + esc(e.title) + (n >= TOTAL ? " ✓" : "") + "</option>";
      }).join("") + "</optgroup>";
    });
    $("ep-sel").innerHTML = h;
    $("ep-prev").disabled = cur === 0;
    $("ep-next").disabled = cur === EP.length - 1;
  }
  function hashOf() { return tab === "canal" || tab === "plan" || tab === "prod" ? tab : "e" + pad(EP[cur].n) + "-" + tab; }
  function readHash() {
    var h = (location.hash || "").slice(1), m = /^e(\d+)-([a-z]+)$/.exec(h);
    if (m) {
      var i = EP.map(function (e) { return e.n; }).indexOf(+m[1]);
      if (i > -1 && TABS.indexOf(m[2]) > -1) { cur = i; tab = m[2]; return true; }
    } else if (h === "canal" || h === "plan" || h === "prod") { tab = h; return true; }
    return false;
  }
  function render(keepScroll) {
    var ep = EP[cur];
    CP = [];
    [].forEach.call(document.querySelectorAll("#tabs .tab"), function (b) { b.setAttribute("aria-selected", b.dataset.v === tab); });
    $("picker").hidden = tab === "canal" || tab === "plan" || tab === "prod";
    picker();
    $("view").innerHTML = tab === "guion" ? vGuion(ep) : tab === "tomas" ? vTomas(ep) : tab === "elenco" ? vElenco(ep) : tab === "prod" ? vProd() : tab === "canal" ? vCanal() : tab === "plan" ? vPlan() : vGuia(ep);
    store.set("ui", {cur: cur, tab: tab});
    try { if ((location.hash || "").slice(1) !== hashOf()) history.replaceState(null, "", "#" + hashOf()); } catch (e) { /* sin historial: no pasa nada */ }
    if (!keepScroll) window.scrollTo(0, 0);
  }
  function go(i, t) {
    cur = Math.min(EP.length - 1, Math.max(0, i));
    if (t) tab = t;
    blk = -1; render();
  }

  $("tabs").addEventListener("click", function (e) {
    var b = e.target.closest(".tab"); if (!b) return;
    tab = b.dataset.v; render();
  });
  $("ep-sel").addEventListener("change", function (e) { go(+e.target.value); });
  $("ep-prev").addEventListener("click", function () { go(cur - 1); });
  $("ep-next").addEventListener("click", function () { go(cur + 1); });
  $("view").addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    if (b.dataset.k != null) { copyTxt(CP[+b.dataset.k], b); return; }
    if (b.dataset.b != null) { blk = +b.dataset.b; render(true); return; }
    if (b.dataset.pc != null) { pc = b.dataset.pc; render(true); return; }
    if (b.dataset.pm != null) { pm = b.dataset.pm; render(true); return; }
    if (b.dataset.go != null) { var g = b.dataset.go.split(":"); go(+g[0], g[1]); return; }
    if (b.id === "reset") { store.set("chk" + EP[cur].n, []); render(true); }
  });
  $("view").addEventListener("change", function (e) {
    var d = e.target.dataset, a, k;
    if (d.bank != null) {
      k = bankDone.indexOf(d.bank);
      if (e.target.checked && k < 0) bankDone.push(d.bank);
      if (!e.target.checked && k > -1) bankDone.splice(k, 1);
      store.set("bank", bankDone);
      e.target.closest(".step").classList.toggle("on", e.target.checked);
      $("bank-count").textContent = bankDone.length + " de " + BANK_TOTAL + " piezas listas";
      return;
    }
    if (d.id == null) return;
    a = chk(EP[cur]); k = a.indexOf(d.id);
    if (e.target.checked && k < 0) a.push(d.id);
    if (!e.target.checked && k > -1) a.splice(k, 1);
    store.set("chk" + EP[cur].n, a); render(true);
  });
  $("view").addEventListener("input", function (e) {
    if (e.target.id === "plan-q") { pq = e.target.value; $("plan-list").innerHTML = planList(); return; }
  });
  window.addEventListener("hashchange", function () { if (readHash()) render(); });

  /* Descarga del .srt. En una página normal (GitHub Pages) basta el enlace.
     Dentro del visor de Claude, el enlace no descarga: se usa su capacidad
     de descargas, que no admite .srt, así que se guarda como .txt. */
  var DL = null;
  try { if (window.claude && window.claude.use) window.claude.use("downloads").then(function (d) { DL = d; }, function () {}); } catch (e) { /* sin visor */ }
  $("view").addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-srt]");
    if (!a || !DL) return;
    e.preventDefault();
    var name = a.getAttribute("download").replace(/\.srt$/, ".txt");
    DL.save({filename: name, data: srt(EP[cur])}).then(function () {
      a.nextElementSibling.textContent = "Guardado como " + name + ". Cámbiale la extensión a .srt antes de importarlo en DaVinci.";
    }, function (err) {
      a.nextElementSibling.textContent = err && err.code === "declined" ? "Descarga cancelada." : "Aquí no se puede descargar: usa «Copiar .srt» y pégalo en un archivo con extensión .srt.";
    });
  });

  readHash();
  render(true);
})();
