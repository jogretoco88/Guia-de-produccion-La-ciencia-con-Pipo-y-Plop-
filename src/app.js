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

  var TABS = ["guia", "guion", "tomas", "elenco", "flow", "canal", "plan"];
  var ui = store.get("ui", {});
  var cur = Math.min(EP.length - 1, Math.max(0, ui.cur || 0));
  var tab = TABS.indexOf(ui.tab) > -1 ? ui.tab : "guia";
  var blk = -1, pc = "", pm = "", pq = "";
  var calc = store.get("calc", {cr: 10, tk: 1.6, mo: 1000});
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
          if (f === "k") s.key = true;
          else if (f === "o") s.open = true;
          else if (f.charAt(0) === "<") s.from = E + "_C" + pad(+f.slice(1));
          else if (/^[a-e]=[tsmlxg]$/.test(f)) { s.zo = s.zo || {}; s.zo[f.charAt(0)] = f.charAt(2); }
        });
        /* Escala crítica: el protagonista junto a algo mucho más pequeño que él.
           Con ingredientes sueltos el modelo no sabe el tamaño: se compone primero la imagen. */
        if (s.tags.indexOf(ep.star) > -1 && s.tags.split("").some(function (k) { var z = zOf(ep, s, k); return z === "t" || z === "s"; })) { s.sc = true; s.key = true; }
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
    o.clips = o.gen + o.bank; o.dur = ep._dur; ep._c = o;
    return o;
  }

  /* ---------- Escala ---------- */
  function zOf(ep, s, k) { var o = ep.objs[k]; return o ? ((s && s.zo && s.zo[k]) || o.z) : ""; }
  function shortEn(o) { return o.en.split(" (")[0]; }
  function scale(ep, s) {
    var tags = s.tags.split(""), who = tags.filter(function (k) { return WHO[k]; })[0];
    var ob = tags.filter(function (k) { return ep.objs[k]; });
    if (!ob.length || (!who && ob.length < 2)) return "";
    if (who) {
      var N = WHO[who].es;
      return "Size and scale: " + N + " is about 30 cm tall; " + ob.map(function (k) {
        var z = SIZES[zOf(ep, s, k)];
        return shortEn(ep.objs[k]) + " is " + z[2] + ", " + z[3].replace(/\{N\}/g, N);
      }).join("; ") + ". Keep these exact sizes for the whole shot. ";
    }
    return "Size and scale: " + joinEn(ob.map(function (k) { return shortEn(ep.objs[k]) + " is " + SIZES[zOf(ep, s, k)][2]; })) +
      ". Keep these relative sizes for the whole shot. ";
  }

  /* ---------- Prompts ---------- */
  function refs(ep, tags) { return tags.split("").map(function (k) { return WHO[k] || ep.objs[k]; }); }
  function joinEn(a) { return a.length < 2 ? a.join("") : a.slice(0, -1).join(", ") + " and " + a[a.length - 1]; }
  function hdr(ep, tags) {
    var r = refs(ep, tags);
    return r.length ? "Using the provided reference images of " + joinEn(r.map(function (x) { return x.en; })) + ": " : "";
  }
  function puppet(s) { return /[PL]/.test(s.tags) && !s.open ? MOUTH + " " : ""; }
  function attach(ep, tags) {
    var r = refs(ep, tags);
    return r.length ? r.map(function (x) { return x.tag; }).join(" + ") : "ninguno (solo el prompt)";
  }
  function pClip(ep, s) {
    return CAM[s.cam].v + ". " + hdr(ep, s.tags) + s.scene + " " + scale(ep, s) + "One continuous action for the whole 8-second shot: " + s.act +
      " Everything else in the frame stays still. " + STYLE_V + " " + puppet(s) + AUDIO;
  }
  function pMotion(ep, s) {
    return CAM[s.cam].v + ". Starting from the provided first frame, one continuous action for the whole 8-second shot: " + s.act +
      " Everything else stays still, and the colors, clay texture, sizes and character design stay exactly as in the first frame. Handmade claymation stop-motion motion, animated on twos at 12 fps. " +
      puppet(s) + AUDIO;
  }
  function pKey(ep, s) {
    return "16:9 still frame. " + CAM[s.cam].k + ". " + hdr(ep, s.tags) + s.scene + " " + scale(ep, s) + STYLE_I + " The frame holds only these clay figures on the plain white set.";
  }
  function pStill(ep, s) {
    return "16:9 still image. " + hdr(ep, s.tags) + s.scene + " " + scale(ep, s) + STYLE_I + " The image holds only these clay figures on the plain white set.";
  }
  function pScale(ep) {
    var N = WHO[ep.star].es, ks = Object.keys(ep.objs);
    return "16:9 still image, a size comparison line-up. Using the provided reference images of " + joinEn([WHO[ep.star].en].concat(ks.map(function (k) { return ep.objs[k].en; }))) + ": " +
      N + " stands on the left, facing the camera, about 30 cm tall. To his right, standing in one straight row on the same floor and evenly spaced, are " +
      joinEn(ks.map(function (k) { var z = SIZES[ep.objs[k].z]; return shortEn(ep.objs[k]) + " (" + z[2] + ", " + z[3].replace(/\{N\}/g, N) + ")"; })) +
      ". Every object keeps exactly this real size next to " + N + ". " + STYLE_I + " The image holds only these clay figures on the plain white set.";
  }
  function pObj(o) { return o.p + " 16:9 frame at eye level, the object centered. " + STYLE_I; }

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
      "Pipo tiene una idea loca, Plop hace la pregunta correcta y juntos descubren la respuesta en plastilina.\n\n" +
      "CAPÍTULOS\n" + ch + "\n\n" +
      "RETO EN CASA\n" + ep.reto + "\n\n" +
      "PARA FAMILIAS Y DOCENTES\nIdea central: " + ep.secret + "\nPalabras nuevas: " + ep.vocab + "\nFuentes: (pega aquí tus dos fuentes)\n\n" +
      "También se busca como: " + ep.syn + "\n\n" +
      "Animación creada con herramientas de inteligencia artificial. Guion, revisión científica y montaje hechos por personas.\n\n" +
      "#CienciaParaNiños #PipoYPlop " + ep.tags;
  }

  /* ---------- Pasos de la guía ---------- */
  var STEPS = [
    {t: "1 · Ciencia y guion", i: [
      ["Verifica la ficha científica con dos fuentes", "Pestaña Guion. Un libro de texto, un museo de ciencia o una universidad. Anota las fuentes: van en la descripción del video."],
      ["Lee el guion en voz alta con cronómetro", "Cada frase corresponde a un clip de 8 s. Si una frase pasa de 7 s al leerla, recórtala antes de generar la voz."]]},
    {t: "2 · Voz en ElevenLabs", i: [
      ["Usa siempre la misma voz del canal", "Una voz cálida y curiosa en español neutro. Guárdala en tus voces y no la cambies entre episodios."],
      ["Genera el guion bloque por bloque, con velocidad 0,9", "Pestaña Guion. Modelo Eleven v3, estabilidad Natural y velocidad 0,9 en los ajustes de la voz. Haz dos o tres tomas por bloque y quédate con la mejor."],
      ["Exporta y nombra cada bloque", "__E___VO_B1 a __E___VO_B7. La voz de todo el episodio dura unos 4 minutos: es lo correcto. Los 5:00 los dan los clips, y cada frase se coloca sobre el suyo en el montaje."]]},
    {t: "3 · Elenco y láminas en Nano Banana Pro", i: [
      ["Ten listo el banco del canal", "Pestaña Elenco. Los 20 clips de reacción y las 2 láminas del canal se generan una sola vez y sirven para todos los episodios."],
      ["Genera los objetos del episodio", "Pestaña Elenco. Un objeto por imagen, sobre fondo blanco. Guárdalos como ingredientes en Flow."],
      ["Comprueba los tamaños con la hoja de escala", "Pestaña Elenco. Una imagen del protagonista junto a todos los objetos en su tamaño real. Es la regla con la que revisas cada fotograma clave."],
      ["Genera las 3 láminas del episodio", "Pestaña Tomas, tarjetas amarillas. Sin texto: los rótulos se añaden en DaVinci."]]},
    {t: "4 · Clips en Google Flow", i: [
      ["Configura el proyecto", "Veo 3.1 Lite, 16:9, 8 segundos, un resultado por prompt. En este episodio el único personaje que se adjunta es __STAR__. __CO__ sale siempre del banco."],
      ["Genera los clips en orden", "__GEN__ Copia cada prompt tal cual. Si un clip falla dos veces, pasa al Plan B de su tarjeta."],
      ["Revisa cada clip antes de seguir", "Personaje correcto, boca cerrada, sin texto, fondo blanco y una sola acción. Descárgalo y nómbralo con su ID."],
      ["Controla los créditos", "__PTS__"]]},
    {t: "5 · Montaje en DaVinci Resolve", i: [
      ["Línea de tiempo 1920×1080 a 24 fps", "Coloca primero los clips y las láminas, en orden y sin huecos: son ellos los que dan los 5:00. No montes al ritmo de la voz, o el episodio se queda en unos 3:30."],
      ["Importa los subtítulos de tiempos", "Pestaña Guion, archivo .srt. En DaVinci: File → Import → Subtitle, y arrástralo a la línea de tiempo. Cada subtítulo marca dónde empieza una frase."],
      ["Una frase sobre cada clip", "Corta la voz de cada bloque en sus pausas y coloca cada frase al comienzo de su subtítulo. Si una frase pasa de su clip, recórtala o acelérala hasta un 110 %, nunca más. Deja 2 s de silencio después de «Piénsalo…»."],
      ["Clips del banco", "Colócalos donde indica la pestaña Tomas. Para que no se vean idénticos de un episodio a otro, voltéalos en espejo o cambia el encuadre."],
      ["Láminas con rótulos", "Zoom lento de 100 % a 106 % y los rótulos que indica cada lámina, en letra grande."],
      ["Sonido", "Silencia el audio de Flow o déjalo a −18 dB si solo tiene roces de arcilla. Añade los efectos de la pestaña Guion y música suave a −20 dB bajo la voz. Mezcla final a −14 LUFS."],
      ["Textura de stop-motion", "Si un clip se ve demasiado fluido, conviértelo a 12 fps. Mantén tu ajuste de Midtone Detail +30 y grano sutil."]]},
    {t: "6 · Publicación en YouTube", i: [
      ["Título, descripción y capítulos", "Cópialos de aquí abajo y añade tus dos fuentes.", "yt"],
      ["Miniatura", "__THUMB__"],
      ["Audiencia: «Sí, es contenido para niños»", "Es obligatorio en un canal dirigido a niños. Desactiva comentarios, tarjetas y pantallas finales: por eso el cierre hablado anuncia el siguiente episodio."],
      ["Subtítulos y lista de reproducción", "Sube el guion como subtítulos en español y añade el video a la lista de su temporada."],
      ["Revisión en televisor", "Míralo completo en una TV: nitidez, volumen de la voz y rótulos legibles a tres metros."]]},
    {t: "7 · Después de publicar", i: [
      ["Corta dos Shorts", "El primero: los cuatro clips centrales del bloque 4 (C19 a C22) con su voz, 32 s. El segundo: el dato extra (C31 y C32) con el título en pantalla."],
      ["Lee la retención a las 48 horas y a los 7 días", "Anota en qué segundo cae la curva y a qué bloque pertenece. Corrige ese bloque en el siguiente episodio."]]}
  ];
  var TOTAL = STEPS.reduce(function (s, p) { return s + p.i.length; }, 0);
  function chk(ep) { return store.get("chk" + ep.n, []); }
  function credits(n) { return Math.ceil(n * calc.tk * calc.cr); }
  function status(ep) {
    var n = chk(ep).length;
    return n === 0 ? "Sin empezar" : n >= TOTAL ? "Publicado" : "En producción · " + n + "/" + TOTAL;
  }

  /* ---------- Vista: Guía ---------- */
  function vGuia(ep) {
    var c = count(ep), done = chk(ep), pct = Math.round(done.length / TOTAL * 100), E = "E" + pad(ep.n);
    var h = "<section class='panel'><h2>Ep. " + ep.n + " · " + esc(ep.title) + "</h2>" +
      "<p class='mut'>Protagonista: " + WHO[ep.star].es + " · " + WHO[coOf(ep)].es + " aparece solo con clips del banco · " + CATS[ep.cat] + " · " + CERT[ep.cert][0] + "</p>" +
      "<p class='secret'>" + esc(ep.secret) + "</p>" +
      "<ul class='stats'><li>" + tc(c.dur) + " de video</li><li>" + c.clips + " clips de 8 s</li><li>" + c.gen + " por generar</li><li>" + c.bank + " del banco</li><li>3 láminas nuevas y 2 del canal</li></ul>" +
      "<div class='barp' role='progressbar' aria-valuemin='0' aria-valuemax='100' aria-valuenow='" + pct + "' aria-label='Avance del episodio'><i style='width:" + pct + "%'></i></div>" +
      "<p class='mut'>" + done.length + " de " + TOTAL + " pasos completados" + (done.length === TOTAL ? ". Episodio publicado." : "") + "</p></section>";
    STEPS.forEach(function (p, pi) {
      h += "<h3>" + esc(p.t) + "</h3><div class='steps'>";
      p.i.forEach(function (it, ii) {
        var id = "p" + pi + "i" + ii, on = done.indexOf(id) > -1;
        var det = it[1].replace(/__E__/g, E)
          .replace("__STAR__", WHO[ep.star].tag).replace("__CO__", WHO[coOf(ep)].es)
          .replace("__GEN__", c.gen + " clips nuevos; los otros " + c.bank + " ya están en el banco.")
          .replace("__PTS__", "Este episodio: unos " + credits(c.gen) + " créditos (" + c.gen + " clips × " + calc.tk + " intentos × " + calc.cr + " créditos). Ajusta los números en Reglas de Flow. Prueba primero con los créditos diarios.")
          .replace("__THUMB__", ep.thumbIdea + " Texto: «" + ep.thumb + "».");
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
    var h = "<section class='panel'><h2>Guion para ElevenLabs · Ep. " + ep.n + "</h2>" +
      "<p class='mut'>" + c.words + " palabras para " + tc(c.dur) + " de video. Cada línea es la voz de una toma: explica, pregunta y responde a las ideas de Pipo y Plop. La acción la muestra la imagen.</p>" +
      "<p class='note'><b>La voz dura unos " + tc(vt) + ", no 5:00, y está bien así.</b> Cada frase ocupa unos 6 de los 8 segundos de su clip; el resto es respiro para la imagen, la música y los efectos. " +
      "Los 5:00 los dan los clips. Si generas la voz de corrido y montas a su ritmo, el episodio se queda en unos 3:30. " +
      "En el montaje, cada frase se coloca al comienzo de su clip: el archivo de subtítulos de abajo marca dónde.</p>" +
      ul(["<b>Modelo:</b> Eleven v3, que entiende las etiquetas entre corchetes. Admite unos 5.000 caracteres por generación; cada bloque cabe de sobra.",
          "<b>Velocidad:</b> 0,9 en los ajustes de la voz. Un ritmo algo más pausado, mejor para niños, que llena más cada clip sin pasarse de los 8 segundos. Medido: a velocidad 1,0, el guion del Ep. 2 duró 3:30.",
          "<b>Pausas:</b> Eleven v3 no admite etiquetas de pausa con tiempo (<i>break</i>). No intentes estirar el audio con pausas: el tiempo se ajusta en el montaje.",
          "<b>Voz:</b> una sola para todo el canal. Cálida, curiosa, español neutro.",
          "<b>Estabilidad:</b> Natural. Si las etiquetas no se notan, baja a Creative y regenera. Si la voz cambia demasiado, sube a Robust.",
          "<b>Etiquetas:</b> ya vienen puestas, una por frase como máximo. Los efectos de sonido van aparte, no en el texto.",
          "<b>Números y siglas:</b> están escritos como se pronuncian."]) + "</section>";
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
      "<p><a class='btn' download='E" + pad(ep.n) + "_tiempos_voz.srt' href='data:application/x-subrip;charset=utf-8," + encodeURIComponent(srt(ep)) + "'>Descargar E" + pad(ep.n) + "_tiempos_voz.srt</a></p>" +
      "<details class='fold'><summary>Ver o copiar el .srt (si la descarga no funciona, pégalo en un archivo de texto con extensión .srt)</summary><div>" + cb(srt(ep), "Copiar .srt", {txt: 1}) + "</div></details></section>" +
      "<details class='fold'><summary>Guion con tiempos e ID de cada toma, para el montaje</summary><div>" +
      "<p class='mut'>No lo pegues en ElevenLabs. Sirve para colocar cada frase bajo su clip.</p>" + cb(marks.join("\n"), "Copiar guion con tiempos", {txt: 1}) + "</div></details>";
    h += "<section class='panel'><h3>Efectos de sonido de este episodio</h3>" +
      "<p class='mut'>Genera cada uno en Sound Effects de ElevenLabs y colócalo en el montaje. Así la voz queda limpia y controlas el volumen.</p>" +
      ep.sfx.map(function (x) { return cb(x[1], "Copiar", {lab: x[0], ghost: 1}); }).join("") + "</section>" +
      "<details class='fold'><summary>Kit sonoro del canal (se genera una sola vez)</summary><div>" +
      KIT.map(function (x) { return cb(x[1], "Copiar", {lab: x[0], ghost: 1}); }).join("") + "</div></details>";
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
        "<p class='meta'><b>Ingredientes:</b> " + esc(attach(ep, s.tags)) + " · <b>Rótulos en DaVinci:</b> " + esc(s.lab) + "</p>" + sizeLine(ep, s) +
        cb(pStill(ep, s), "Copiar prompt de la lámina") + "</div></article>";
    }
    if (s.k === "K") {
      return "<article class='shot still'>" + rail(s, "Lámina del canal · 4 s") + "<div class='body'>" +
        "<p class='vo'>" + esc(s.vo) + "</p><p class='es'><b>En pantalla:</b> " + esc(s.es) + "</p>" +
        "<p class='meta'><b>Rótulos en DaVinci:</b> " + esc(s.lab) + "</p>" +
        "<p class='note'><b>Ya la tienes:</b> es la misma imagen en todos los episodios. Su prompt está en Elenco, en el banco del canal.</p></div></article>";
    }
    if (s.k === "R") {
      return "<article class='shot bank'>" + rail(s, "Banco · 8 s") + "<div class='body'>" +
        "<p class='vo'>" + esc(s.vo) + "</p><p class='es'><b>En pantalla:</b> " + esc(s.es) + "</p>" +
        "<p class='note'><b>Usa el clip " + s.bid + " («" + esc(s.name) + "») del banco.</b> No se genera ni gasta créditos. Si acaba de salir en otro episodio, voltéalo en espejo.</p></div></article>";
    }
    h = "<article class='shot'>" + rail(s, "Clip · 8 s") + "<div class='body'>" +
      "<p class='vo'>" + esc(s.vo) + "</p><p class='es'><b>En pantalla:</b> " + esc(s.es) + "</p>" +
      "<p class='meta'><b>Ingredientes:</b> " + esc(attach(ep, s.tags)) + " · <b>Cámara:</b> " + CAM[s.cam].es + "</p>" +
      sizeLine(ep, s) +
      (s.sc ? "" : s.key ? "<p><span class='flag k'>Mejor con fotograma clave</span></p>" : "");
    if (s.sc && !s.from) {
      h += "<p class='note'><span class='flag k'>Escala crítica · usa fotograma clave</span> " + esc(WHO[ep.star].es) + " aparece junto a algo mucho más pequeño que él. " +
        "Con ingredientes sueltos, Flow no sabe el tamaño de cada cosa y suele hacer los objetos tan grandes como el personaje. Compón primero la imagen, comprueba los tamaños y después anímala.</p>" +
        cb(pKey(ep, s), "Copiar prompt del fotograma", {lab: "1 · Imagen en Nano Banana Pro, con los mismos ingredientes. Revisa que los tamaños sean los indicados antes de seguir"}) +
        cb(pMotion(ep, s), "Copiar prompt del clip", {lab: "2 · Clip en Flow con esa imagen como fotograma inicial (Frames to Video)"}) +
        "<details class='alt'><summary>Ruta rápida con ingredientes (más riesgo de tamaño equivocado)</summary><div>" +
        cb(pClip(ep, s), "Copiar prompt del clip") + "</div></details>";
    } else if (s.from) {
      h += "<p class='note'><b>Fotograma inicial:</b> el último fotograma de " + s.from + ". Así continúa exactamente donde quedó.</p>" +
        cb(pMotion(ep, s), "Copiar prompt del clip") +
        "<details class='alt'><summary>Si la continuación pierde calidad: fotograma clave nuevo</summary><div>" +
        cb(pKey(ep, s), "Copiar prompt del fotograma", {lab: "1 · Imagen en Nano Banana Pro"}) + "<p class='mut'>Después usa esa imagen como fotograma inicial con el prompt de arriba.</p></div></details>";
    } else {
      h += cb(pClip(ep, s), "Copiar prompt del clip") +
        "<details class='alt'><summary>Plan B · fotograma clave</summary><div>" +
        cb(pKey(ep, s), "Copiar prompt del fotograma", {lab: "1 · Imagen en Nano Banana Pro, con los mismos ingredientes"}) +
        cb(pMotion(ep, s), "Copiar prompt del clip", {lab: "2 · Clip en Flow con esa imagen como fotograma inicial"}) + "</div></details>";
    }
    return h + "</div></article>";
  }
  function sizeLine(ep, s) {
    var ob = s.tags.split("").filter(function (k) { return ep.objs[k]; });
    if (!ob.length) return "";
    return "<p class='meta'><b>Tamaños:</b> " + ob.map(function (k) {
      var z = SIZES[zOf(ep, s, k)]; return esc(ep.objs[k].tag) + " " + z[0].toLowerCase() + " (" + z[1].split(",")[0] + ")";
    }).join(" · ") + "</p>";
  }
  function vTomas(ep) {
    var S = build(ep), c = count(ep);
    var h = "<section class='panel'><h2>Tomas · Ep. " + ep.n + " · " + esc(ep.topic) + "</h2>" +
      "<p class='mut'>" + c.gen + " clips por generar, " + c.bank + " del banco y 5 láminas suman " + tc(c.dur) + ". Cada toma entra con la frase de voz que la acompaña. Cada prompt pide una sola acción continua para los 8 segundos. El único personaje que se genera aquí es " + WHO[ep.star].es + ".</p>" +
      "<div class='tl' aria-hidden='true'>" + BLOCKS.map(function (b, bi) {
        var L = S.filter(function (s) { return s.b === bi; }), sp = blockSpan(ep, bi);
        return "<div class='tb' style='flex:" + (sp[1] - sp[0]) + "'><div class='seg'>" +
          L.map(function (s) { return "<i class='" + (s.k === "C" ? "" : s.k === "R" ? "r" : "s") + "' style='flex:" + s.d + "'></i>"; }).join("") +
          "</div><small>" + tc(sp[0]) + "</small></div>";
      }).join("") + "</div>" +
      "<p class='legend'><span><i></i>Clip por generar</span><span><i class='r'></i>Clip del banco</span><span><i class='s'></i>Lámina fija</span></p>" +
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

  /* ---------- Vista: Elenco ---------- */
  var BANK_TOTAL = Object.keys(BANK).length + 2;
  function bankItem(code) {
    var B = BANK[code], s = {cam: B[2], tags: code.charAt(0), scene: B[3], act: B[4]}, id = bankId(code), on = bankDone.indexOf(id) > -1;
    return "<div class='bitem'><label class='step" + (on ? " on" : "") + "'><input type='checkbox' id='bk-" + id + "' data-bank='" + id + "'" + (on ? " checked" : "") + "><div><b>" + id + " · " + esc(B[0]) + "</b><span>" + esc(B[1]) + " " + CAM[B[2]].es + ". Adjunta solo " + WHO[code.charAt(0)].tag + ".</span></div></label>" +
      cb(pClip({objs: {}}, s), "Copiar prompt del clip") +
      "<details class='alt'><summary>Plan B · fotograma clave</summary><div>" +
      cb(pKey({objs: {}}, s), "Copiar prompt del fotograma", {lab: "1 · Imagen en Nano Banana Pro"}) +
      cb(pMotion({objs: {}}, s), "Copiar prompt del clip", {lab: "2 · Clip en Flow con esa imagen como fotograma inicial"}) + "</div></details></div>";
  }
  function cardItem(k) {
    var K = CARDS[k], id = k === "T" ? "CANAL_INICIO" : "CANAL_FINAL", on = bankDone.indexOf(id) > -1;
    return "<div class='bitem'><label class='step" + (on ? " on" : "") + "'><input type='checkbox' id='bk-" + id + "' data-bank='" + id + "'" + (on ? " checked" : "") + "><div><b>" + id + " · " + esc(K[0]) + "</b><span>" + esc(K[1]) + " Adjunta @PIPO y @PLOP. Es la única imagen donde aparecen juntos.</span></div></label>" +
      cb(pStill({objs: {}}, {tags: "PL", scene: K[2]}), "Copiar prompt de la lámina") + "</div>";
  }
  function vElenco(ep) {
    var w = WHO[ep.star], co = WHO[coOf(ep)], P = [], L = [];
    Object.keys(BANK).forEach(function (k) { (k.charAt(0) === "P" ? P : L).push(k); });
    var h = "<section class='panel'><h2>Elenco · Ep. " + ep.n + " · " + esc(ep.topic) + "</h2>" +
      "<p class='secret'>Un solo personaje por episodio en Flow.</p>" +
      "<p class='prose'>En este episodio solo se genera a " + w.es + ". " + co.es + " aparece con clips del banco, que se generan una sola vez y se aprueban antes de empezar. Así ningún episodio mezcla dos personajes en Flow, y no hay forma de que se contagien colores o rasgos.</p></section>";
    h += "<section class='panel'><h3>" + w.tag + " · " + w.es + ", protagonista</h3><p>" + esc(w.bio) + "</p>" +
      "<p class='note'><b>Si ya lo tienes, no lo regeneres.</b> Este es tu prompt maestro original, sin cambios.</p>" +
      cb(w.p, "Copiar prompt maestro", {txt: 1}) + "</section>";
    Object.keys(ep.objs).forEach(function (k) {
      var o = ep.objs[k], z = SIZES[o.z];
      h += "<section class='panel'><h3>" + o.tag + " · " + esc(o.es) + "</h3>" +
        "<p class='meta'><b>Tamaño en las escenas:</b> " + z[0] + ", " + esc(z[1]) + " de " + w.es + ".</p>" +
        cb(pObj(o), "Copiar prompt del objeto") + "</section>";
    });
    h += "<section class='panel'><h3>Hoja de escala del episodio</h3>" +
      "<p class='prose'>Cada imagen de referencia muestra un objeto solo, a pantalla completa: no dice nada de su tamaño. Por eso Flow puede hacer una gota tan grande como " + w.es + ". " +
      "Antes de generar los clips, haz esta imagen en Nano Banana Pro con " + w.tag + " y todos los objetos adjuntos. Si los tamaños salen bien, tenla a mano: es la regla con la que compruebas cada fotograma clave.</p>" +
      cb(pScale(ep), "Copiar prompt de la hoja de escala") + "</section>";
    h += "<section class='panel'><h2>Banco del canal</h2>" +
      "<p class='prose'>Veinte clips de reacción y dos láminas. Se generan una sola vez, con calma, y sirven para los 52 episodios. Genera el banco de Pipo en una sesión y el de Plop en otra, cada una con un solo ingrediente adjunto. Marca cada pieza cuando la apruebes.</p>" +
      "<ul class='stats'><li id='bank-count'>" + bankDone.length + " de " + BANK_TOTAL + " piezas listas</li><li>Costo único: unos " + credits(Object.keys(BANK).length) + " créditos</li></ul></section>" +
      "<details class='fold'><summary>Banco de Pipo · " + P.length + " clips</summary><div>" + P.map(bankItem).join("") + "</div></details>" +
      "<details class='fold'><summary>Banco de Plop · " + L.length + " clips</summary><div>" + L.map(bankItem).join("") + "</div></details>" +
      "<details class='fold'><summary>Láminas del canal · cortinilla y tarjeta final</summary><div>" + cardItem("T") + cardItem("F") + "</div></details>" +
      "<details class='fold'><summary>Prompt maestro de " + co.es + " (para generar su banco)</summary><div>" + cb(co.p, "Copiar prompt maestro", {txt: 1}) + "</div></details>";
    return h;
  }

  /* ---------- Vista: Reglas de Flow ---------- */
  function rule(a) { return "<div class='rule'><b>" + esc(a[0]) + (a[2] ? "<span class='src'>" + a[2] + "</span>" : "") + "</b><span>" + esc(a[1]) + "</span></div>"; }
  var DO = [
    ["Un solo personaje por episodio", "En Flow solo se adjunta al protagonista. El otro personaje sale del banco de reacciones, ya generado y aprobado."],
    ["Una sola acción continua por clip", "Un verbo principal que dure los 8 s. «Slowly» y «again and again» estiran la acción y te dejan cortar en cualquier punto.", "Comunidad"],
    ["Sigue la fórmula de Google", "Cámara, sujeto, acción, contexto, estilo y ambiente. Siempre en ese orden.", "Google"],
    ["Nombra las referencias", "Empieza con «Using the provided reference images of…» y llama a cada cosa siempre igual.", "Google"],
    ["Escribe el tamaño de cada cosa", "Una imagen de referencia no trae tamaño: el objeto ocupa todo el cuadro. Cada prompt con dos o más elementos dice cuánto mide cada uno respecto al títere (unos 30 cm). Cuando el protagonista sale con algo pequeño, compón antes el fotograma en Nano Banana Pro y comprueba los tamaños."],
    ["Describe el estado inicial tal como se ve", "Si la imagen muestra a Pipo sentado, el prompt no puede pedirle que se siente. La imagen es el punto de partida; el texto dice qué cambia.", "Google"],
    ["Repite el bloque de estilo palabra por palabra", "El mismo texto de arcilla, luz y fondo en todos los clips. Cambiar un adjetivo cambia el aspecto.", "Comunidad"],
    ["Define el audio aunque lo silencies", "Un clip sin indicación de sonido tiende a inventar voces, música y subtítulos.", "Google"],
    ["Pide lo que quieres, en positivo", "«Plain pure-white background» funciona mejor que «no background».", "Google"],
    ["Cámara fija por defecto", "El stop-motion real se rueda con cámara fija. Si la cámara se mueve, el sujeto se queda quieto.", "Comunidad"],
    ["Corrige en imagen antes que en video", "Si la composición es difícil, apruébala primero como fotograma clave. Repetir una imagen cuesta mucho menos que repetir un clip.", "Comunidad"],
    ["Escribe los prompts en inglés", "Es el idioma de los ejemplos oficiales y donde el modelo obedece con más precisión. La línea «En pantalla» te dice en español qué debe verse.", "Práctica"]
  ];
  var DONT = [
    ["Pipo y Plop en el mismo proyecto de Flow", "Dos personajes parecidos se contagian colores y rasgos, y es fácil adjuntar el equivocado. Su diálogo se arma en el montaje con los clips del banco."],
    ["Partir el clip en tramos de tiempo", "Nada de «0–4 s… 4–8 s» ni cadenas de «then… then…». Si hacen falta dos acciones, son dos clips."],
    ["Diálogo y comillas", "El habla en el prompt dispara subtítulos incrustados y bocas que se mueven. Aquí solo habla el narrador, y se añade en el montaje.", "Google Labs"],
    ["Texto, letras o números en la imagen", "Salen deformados. Los rótulos se ponen en DaVinci."],
    ["Cantidades exactas y figuras geométricas por texto", "Más de tres o cuatro objetos iguales, anillos o filas se fijan con un fotograma clave."],
    ["Listas de prohibiciones", "«No humans, no text, no…» es poco fiable y a veces provoca justo eso.", "Google"],
    ["Dedos, líquidos, vidrio, humo y fuego reales", "Todo es arcilla sólida. Gotas, vapor y calor son piezas de plastilina."],
    ["Mover a la vez la cámara y el sujeto", "Es la causa más común de deformaciones.", "Comunidad"],
    ["Encadenar más de dos clips por el último fotograma", "Cada eslabón pierde nitidez y color. Al tercero, empieza de nuevo con un fotograma clave.", "Comunidad"],
    ["Más de tres referencias por clip", "Un personaje y hasta dos objetos. Con más, el modelo los mezcla."]
  ];
  var FIX = [
    ["Aparecen subtítulos o letras", "Revisa que el prompt no tenga comillas ni palabras habladas. Si insiste, añade al final «(no subtitles, no on-screen text)» o recorta el borde inferior en DaVinci."],
    ["El personaje habla o abre la boca", "Usa un plano más abierto y repite «mouth stays closed». Silencia el audio del clip."],
    ["Cambia el color o la forma del personaje", "No lo arregles con más texto. Pasa al Plan B y fija el aspecto con un fotograma clave hecho con el ingrediente original."],
    ["Aparece el otro personaje, o una mezcla de los dos", "Comprueba que solo hay un personaje adjunto. Si trabajas en el banco, usa un proyecto distinto para cada uno."],
    ["Aparece un escenario o un fondo", "Plan B. El fotograma clave ya trae el ciclorama blanco y el clip lo respeta."],
    ["La acción termina a los 3 s y el resto queda quieto", "Añade «slowly» o «again and again». O usa solo los segundos buenos y ralentiza al 85 %."],
    ["El clip va y viene entre dos estados", "La imagen de partida ya muestra el final de la acción. Corrige el estado inicial o cambia el fotograma."],
    ["Salen objetos duplicados o de más", "Di la cantidad («one kernel») y usa fotograma clave."],
    ["Un objeto sale tan grande como el personaje", "Pasa a la ruta del fotograma clave: genera la imagen en Nano Banana Pro, compárala con la hoja de escala del episodio (Elenco) y regenera la imagen hasta que los tamaños sean correctos. Solo entonces anímala. Corregir la imagen cuesta mucho menos que repetir el video."],
    ["El movimiento se ve demasiado fluido", "En DaVinci, convierte el clip a 12 fps. El prompt ya pide «animated on twos»."],
    ["La cámara se mueve sola", "Empieza el prompt con «Locked-off camera, tripod shot»."],
    ["Dos intentos fallidos seguidos", "Para. Cambia de ruta o simplifica la acción antes de gastar más créditos."]
  ];
  function calcText(ep) {
    var c = count(ep), cr = credits(c.gen), per = cr > 0 ? Math.floor(calc.mo / cr) : 0;
    return "Ep. " + ep.n + ": " + c.gen + " clips nuevos ≈ " + cr + " créditos. Con " + calc.mo + " créditos al mes alcanza para " + per + (per === 1 ? " episodio." : " episodios.") +
      " El banco, una sola vez: " + credits(Object.keys(BANK).length) + " créditos.";
  }
  function vFlow(ep) {
    var s = build(ep).filter(function (x) { return x.k === "C" && /[PL]/.test(x.tags); })[0] || build(ep)[0];
    var h = "<section class='panel'><h2>Reglas de Flow para evitar alucinaciones</h2>" +
      "<p class='prose'>Todos los prompts de la pestaña Tomas ya siguen estas reglas. Sirven para entender por qué están escritos así y para escribir los de episodios nuevos.</p>" +
      "<h3>Configuración del proyecto</h3>" +
      ul(["<b>Modelo:</b> Veo 3.1 Lite. Hace clips de 8 s en 720p con ingredientes o con fotograma inicial, por unos 10 créditos.",
          "<b>Cambio del 5 de diciembre de 2026:</b> Flow retira Veo 3.1 Fast y Quality. Google recomienda Veo 3.1 Lite u Omni Flash 1.2. Omni cuesta unos 24 créditos por 8 s: resérvalo para la toma que Lite no logre.",
          "<b>Formato:</b> 16:9, 8 segundos, un resultado por prompt.",
          "<b>Ingredientes:</b> una imagen por personaje u objeto, sobre fondo blanco. Tres como máximo por clip, y un solo personaje por episodio."]) + "</section>";
    h += "<section class='panel'><h3>Por qué un solo personaje por episodio</h3>" +
      ul(["Pipo y Plop se parecen: mismo tipo de cuerpo, mismos ojos, misma arcilla. Si los dos están como ingredientes en el mismo proyecto, es fácil adjuntar el equivocado, y el modelo tiende a mezclar sus colores y accesorios.",
          "Con el banco de reacciones, el personaje que acompaña nunca se vuelve a generar. Sus 10 clips se hacen una vez, se revisan con calma y se reutilizan.",
          "El protagonista sí se genera en cada episodio, siempre solo y siempre con la misma imagen de referencia.",
          "Las únicas imágenes donde aparecen juntos son la cortinilla y la tarjeta final. Son láminas fijas, se generan una vez y son las mismas en todos los episodios.",
          "Efecto secundario bueno: cada episodio necesita unos 25 clips nuevos en lugar de 34."]) + "</section>";
    h += "<section class='panel'><h3>Así está armado cada prompt</h3>" +
      "<p class='mut'>Ejemplo: " + s.id + ". Una frase por pieza, siempre en el mismo orden.</p>" +
      ul(["<b>Cámara:</b> " + esc(CAM[s.cam].v) + ".", "<b>Referencias:</b> " + esc(hdr(ep, s.tags)), "<b>Escena inicial:</b> " + esc(s.scene),
          "<b>Acción única:</b> " + esc(s.act), "<b>Estilo, siempre igual:</b> " + esc(STYLE_V), "<b>Boca y audio:</b> " + esc(MOUTH + " " + AUDIO)]) + "</section>";
    h += "<div class='two'><section class='panel do'><h3>Haz</h3>" + DO.map(rule).join("") + "</section>" +
      "<section class='panel dont'><h3>Evita</h3>" + DONT.map(rule).join("") + "</section></div>";
    h += "<section class='panel'><h3>Dos rutas para generar un clip</h3>" +
      ul(["<b>Ruta A, ingredientes.</b> Adjuntas las imágenes de referencia y pegas el prompt. Es la más rápida y la que usa cada tarjeta por defecto.",
          "<b>Plan B, fotograma clave.</b> Primero generas una imagen fija de la escena en Nano Banana Pro y luego la animas como fotograma inicial con un prompt que solo describe el movimiento. Fija el personaje, el encuadre y el fondo.",
          "<b>Cuándo cambiar:</b> al segundo intento fallido, y desde el principio en las tomas marcadas «Mejor con fotograma clave».",
          "<b>Continuaciones:</b> algunas tomas parten del último fotograma de un clip anterior. No encadenes más de dos seguidas."]) + "</section>";
    h += "<section class='panel'><h3>Si algo sale mal</h3><dl class='fix'>" +
      FIX.map(function (f) { return "<div><dt>" + esc(f[0]) + "</dt><dd>" + esc(f[1]) + "</dd></div>"; }).join("") + "</dl></section>";
    h += "<section class='panel'><h3>Presupuesto de créditos</h3>" +
      "<p class='mut'>Cambia los números por los de tu plan. Los clips del banco no cuentan en cada episodio.</p>" +
      "<div class='calc'>" +
      "<label for='c-cr'>Créditos por clip<input id='c-cr' type='number' inputmode='decimal' min='0' step='1' value='" + calc.cr + "'></label>" +
      "<label for='c-tk'>Intentos por clip<input id='c-tk' type='number' inputmode='decimal' min='1' step='0.1' value='" + calc.tk + "'></label>" +
      "<label for='c-mo'>Créditos al mes<input id='c-mo' type='number' inputmode='decimal' min='0' step='50' value='" + calc.mo + "'></label></div>" +
      "<p class='result' id='c-out'>" + esc(calcText(ep)) + "</p>" +
      "<p class='mut'>Referencia de noviembre de 2026, según guías de terceros: Veo 3.1 Lite cuesta 10 créditos por clip (5 en Ultra) y el plan AI Pro incluye 1.000 créditos al mes. Confírmalo en Flow.</p></section>";
    h += "<section class='panel'><h3>De dónde salen estas reglas</h3>" +
      ul([link("https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1", "Google Cloud: guía de prompts para Veo 3.1") + ". Fórmula, audio, referencias y fotogramas.",
          link("https://support.google.com/flow/answer/16352836", "Ayuda de Google Flow: modelos y funciones") + ". Qué hace cada modelo y cuáles se retiran.",
          link("https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/best-practice", "Google Cloud: buenas prácticas de Veo") + ". En imagen a video, el prompt describe el movimiento.",
          link("https://www.technologyreview.com/2025/07/15/1120156/googles-generative-video-model-veo-3-has-a-subtitles-problem/", "MIT Technology Review: el problema de los subtítulos de Veo 3") + ".",
          "Las reglas marcadas «Comunidad» vienen de guías y reseñas de creadores de 2025 y 2026. No son documentación oficial: compruébalas con tus propios clips."]) + "</section>";
    return h;
  }

  /* ---------- Vista: Canal ---------- */
  function vCanal() {
    var ep = EP[0];
    var h = "<section class='panel'><h2>El canal</h2>" +
      "<p class='secret'>Una pregunta que un niño de verdad haría, una respuesta verdadera y cinco minutos de plastilina.</p>" +
      ul(["<b>Para quién:</b> niños de 6 a 10 años que ven con un adulto cerca, casi siempre en el televisor.",
          "<b>Qué se llevan:</b> una idea que pueden contar en la cena y un reto para probarla.",
          "<b>Qué lo distingue:</b> dos personajes con papeles fijos y una voz que piensa con ellos."]) + "</section>";
    h += "<section class='panel'><h3>Cómo habla la voz</h3>" +
      ul(["La imagen muestra la acción. La voz explica qué significa.",
          "No narra lo que ya se ve. En vez de «Pipo se sienta sobre el grano», dice «ni con todo su peso se abre».",
          "Las ideas de Pipo son hipótesis: se ponen a prueba y se descartan con una razón, nunca con burla.",
          "Las preguntas de Plop son las del espectador. La voz las celebra y las responde.",
          "Habla de tú: mira, fíjate, piénsalo, ¿tú qué crees?",
          "Una idea por frase y 18 palabras como máximo. Cada frase es un clip.",
          "Toda palabra nueva llega con una comparación conocida: casco, renacuajo, puerta, panal."]) + "</section>";
    h += "<section class='panel'><h3>Rituales que se repiten en todos los episodios</h3>" +
      ul(["«La idea loca de Pipo», con su silbido y siempre el mismo clip del banco.", "«Plop se pregunta…», también con su clip.", "«¡Hagamos zoom!», siempre con el mismo sonido.",
          "«¿Tú qué crees? Piénsalo…» y dos segundos de tic-tac.", "«Repasemos»: tres ideas, tres imágenes.",
          "«La ciencia está en todas partes. ¡Hasta el próximo misterio!»"]) +
      "<p class='mut'>Los niños vuelven por lo que reconocen. Los clips del banco son parte de ese ritual: ver a Pipo levantar el brazo ya anuncia una idea loca.</p></section>";
    h += "<section class='panel'><h3>Los cinco minutos, bloque por bloque</h3><div class='scroll'><table><thead><tr><th>Bloque</th><th>Tiempo</th><th>Para qué sirve</th><th>Qué sostiene la atención</th></tr></thead><tbody>" +
      BLOCKS.map(function (b, i) { var sp = blockSpan(ep, i); return "<tr><td>" + (i + 1) + " · " + esc(b[0]) + "</td><td>" + tc(sp[0]) + "–" + tc(sp[1]) + "</td><td>" + esc(b[1]) + "</td><td>" + esc(b[2]) + "</td></tr>"; }).join("") +
      "</tbody></table></div></section>";
    h += "<section class='panel'><h3>Título y miniatura</h3>" +
      ul(["<b>Título:</b> la pregunta tal como la diría un niño, con la palabra clave al principio y menos de 60 caracteres.",
          "<b>Miniatura:</b> un personaje con una emoción clara, un objeto gigante y una o dos palabras.",
          "<b>Fondo de color pleno,</b> distinto en cada episodio. El blanco del estudio se pierde entre las demás miniaturas.",
          "Debe leerse en un móvil pequeño y a tres metros del televisor.",
          "Los primeros 8 s del video cumplen lo que promete la miniatura.",
          "Si a los 7 días una miniatura no funciona, cámbiala y compara los clics por impresión de la semana siguiente."]) + "</section>";
    h += "<section class='panel'><h3>Publicación</h3>" +
      ul(["<b>Audiencia:</b> «Sí, es contenido para niños». Un canal dirigido a niños debe marcarlo.",
          "Eso desactiva los comentarios, las tarjetas, las pantallas finales, la campana, los anuncios personalizados y guardar en listas.",
          "Por eso el guion nunca pide comentar ni suscribirse. El cierre anuncia la siguiente pregunta y la lista de la temporada reproduce el siguiente episodio.",
          "La descripción lleva capítulos, reto, palabras nuevas y fuentes. Es lo que leen padres y docentes.",
          "Sube el guion como subtítulos en español.",
          "Di en la descripción que la animación se hizo con IA y que el guion y la revisión son humanos. Responde con cuidado la pregunta sobre contenido alterado al subir el video."]) +
      "<p class='mut'>Ayuda de YouTube: " + link("https://support.google.com/youtube/answer/9527654", "audiencia del canal o del video") + " y " + link("https://support.google.com/youtube/answer/10774223", "buenas prácticas para contenido infantil y familiar") + ".</p></section>";
    h += "<div class='two'><section class='panel do'><h3>Lo que YouTube premia en contenido infantil</h3>" +
      ul(["Aprender y despertar la curiosidad.", "Creatividad, juego e imaginación.", "Ser buena persona.", "Conexión con el mundo real.", "Diversidad e inclusión."]) + "</section>" +
      "<section class='panel dont'><h3>Lo que castiga</h3>" +
      ul(["Contenido muy comercial.", "Conductas o actitudes negativas.", "Contenido educativo engañoso.", "Lo que dificulta la comprensión.", "Lo sensacionalista.", "Uso extraño de personajes infantiles."]) + "</section></div>" +
      "<p class='note'><b>Contexto de 2026:</b> más de 200 organizaciones pidieron a YouTube frenar el contenido infantil hecho con IA de baja calidad. Un canal con ciencia verificada, ritmo tranquilo y fuentes a la vista queda del lado correcto de esa discusión. No publiques en serie: un episodio bien hecho por semana.</p>";
    h += "<section class='panel'><h3>Ritmo de trabajo</h3>" +
      ul(["Antes de estrenar: el banco completo y tres episodios terminados.", "Después: uno por semana, el mismo día y a la misma hora.",
          "Dos Shorts por episodio entre estreno y estreno: el mecanismo y el dato extra. El fondo blanco permite recortar a vertical sin perder al personaje.",
          "Cuatro temporadas de 13 episodios al año, cada una en su lista de reproducción.",
          "Al empezar cada temporada, genera una variante nueva de los cuatro clips del banco que más se repiten."]) + "</section>";
    h += "<section class='panel'><h3>Qué mirar en YouTube Studio</h3>" +
      ul(["<b>Clics por impresión por debajo del 4 %:</b> cambia la miniatura y el título.",
          "<b>Retención a los 30 s por debajo del 70 %:</b> el misterio no se entiende en los primeros 8 s.",
          "<b>Duración media por debajo de 2:30:</b> busca el segundo exacto donde cae la curva y mira a qué bloque pertenece.",
          "<b>Porcentaje visto en televisor:</b> si sube, las familias lo están viendo juntas."]) +
      "<p class='mut'>Son referencias orientativas para un canal nuevo, no reglas de YouTube.</p></section>";
    return h;
  }

  /* ---------- Vista: Plan anual ---------- */
  function planRow(ep) {
    var tags = "<span class='tag'>" + CATS[ep.cat] + "</span>" +
      ep.mot.split("").map(function (k) { return "<span class='tag m'>" + MOTORS[k][0] + "</span>"; }).join("") +
      (ep.anc ? "<span class='tag a'>Ancla</span>" : "") + (ep.cert > 1 ? "<span class='tag c" + ep.cert + "'>" + CERT[ep.cert][0] + "</span>" : "") +
      "<span class='tag st'>" + status(ep) + "</span>";
    var rows = [["Por qué engancha", ep.why], ["Respuesta", ep.secret], ["Reto en casa", ep.reto], ["Conecta con", ep.link], ["Nota de producción", ep.nota],
                ["Certeza", CERT[ep.cert][0] + ". " + CERT[ep.cert][1]]];
    var i = EP.indexOf(ep);
    return "<details class='ep'><summary><span class='num'>" + pad(ep.n) + "</span><span class='q'>" + esc(ep.title) + "</span>" + tags + "</summary><div>" +
      "<p class='mut'>Protagonista: " + WHO[ep.star].es + " · Texto de miniatura: «" + esc(ep.thumb) + "» · " + count(ep).gen + " clips por generar</p><dl class='ficha'>" +
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
          "<b>¿Despierta una emoción fuerte y segura?</b> Risa, asco, asombro o un poco de miedo.",
          "<b>¿La respuesta está escondida dentro de algo?</b> Eso permite el zoom y sostiene la intriga hasta la mitad del video.",
          "<b>¿Deja un dato para contar?</b> Lo que el niño repite en la cena es lo que trae al siguiente espectador.",
          "<b>¿Tiene un reto que se puede hacer hoy,</b> sin riesgo?",
          "<b>¿Se puede mostrar con cuatro objetos de arcilla o menos?</b>"]) +
      "<p>Y un adulto tiene que poder decir que sí: los padres deciden qué se queda en la pantalla.</p>" +
      "<h3>En qué se apoya</h3>" +
      ul(["Los estudios sobre las preguntas que los niños envían por su cuenta a científicos encuentran que la biología, es decir, el cuerpo y los animales, está entre lo que más preguntan. Por eso casi la mitad de los temas son de cuerpo o de animales. " + link("https://informalscience.org/research/using-questions-sent-ask-scientist-site-identify-childrens-interests-science/", "Baram-Tsabari y otros, 2006") + ".",
          "En una encuesta a 2.000 padres, entre las preguntas que más temían estaban por qué el cielo es azul y cómo se sostienen los aviones en el aire. Las dos están en el plan como anclas. " + link("https://www.publico.es/actualidad/cielo-azul-preguntas-padres-temen.html", "Público, 2012") + ".",
          "Un estudio de 2026 sobre 32.000 videos infantiles de YouTube halló que el movimiento en pantalla aumenta las vistas, pero que el movimiento de fondo se lleva la atención sin mejorar el aprendizaje. En este formato el fondo es blanco y quieto: lo único que se mueve es lo que se explica. " + link("https://digitallearning.eletsonline.com/2026/11/isb-study-visual-motion-children-educational-videos-youtube-attention/", "Estudio de ISB") + ".",
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
          "Pipo protagoniza los episodios impares y Plop los pares. El otro aparece siempre, con sus clips del banco.",
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
  function hashOf() { return tab === "canal" || tab === "plan" ? tab : "e" + pad(EP[cur].n) + "-" + tab; }
  function readHash() {
    var h = (location.hash || "").slice(1), m = /^e(\d+)-([a-z]+)$/.exec(h);
    if (m) {
      var i = EP.map(function (e) { return e.n; }).indexOf(+m[1]);
      if (i > -1 && TABS.indexOf(m[2]) > -1) { cur = i; tab = m[2]; return true; }
    } else if (h === "canal" || h === "plan") { tab = h; return true; }
    return false;
  }
  function render(keepScroll) {
    var ep = EP[cur];
    CP = [];
    [].forEach.call(document.querySelectorAll("#tabs .tab"), function (b) { b.setAttribute("aria-selected", b.dataset.v === tab); });
    $("picker").hidden = tab === "canal" || tab === "plan";
    picker();
    $("view").innerHTML = tab === "guion" ? vGuion(ep) : tab === "tomas" ? vTomas(ep) : tab === "elenco" ? vElenco(ep) : tab === "flow" ? vFlow(ep) : tab === "canal" ? vCanal() : tab === "plan" ? vPlan() : vGuia(ep);
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
    var m = {"c-cr": "cr", "c-tk": "tk", "c-mo": "mo"}[e.target.id]; if (!m) return;
    var n = parseFloat(e.target.value);
    if (!(n >= 0)) return;
    calc[m] = n; store.set("calc", calc);
    $("c-out").textContent = calcText(EP[cur]);
  });
  window.addEventListener("hashchange", function () { if (readHash()) render(); });

  readHash();
  render(true);
})();
