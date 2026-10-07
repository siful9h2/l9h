/* Site-wide translation for l9hkungfu.com.
   - English is the source; translations live in lang/<code>.json:
       { "strings": { "<English text>": "<translation>" },
         "html":    { "<English inner HTML>": "<translated inner HTML>" } }
   - "html" entries cover sentences that contain links or bold/italic words, so they can be
     translated as a whole; "strings" covers everything else, plus titles, placeholders and alt text.
   - Missing entries simply stay in English.
   - The chosen language is remembered (localStorage) and carried on every internal link (?lang=xx),
     so a visitor who picks Spanish stays in Spanish as they move around the site. */
(function () {
  var LANGS = [
    ["en", "English"], ["zh", "中文"], ["es", "Español"], ["fr", "Français"], ["de", "Deutsch"],
    ["pt", "Português"], ["ru", "Русский"], ["ja", "日本語"], ["th", "ไทย"], ["ar", "العربية"], ["hi", "हिन्दी"]
  ];
  var CODES = LANGS.map(function (l) { return l[0]; });
  var RTL = ["ar"];
  var KEY = "l9h-lang";
  var INLINE = { A: 1, EM: 1, STRONG: 1, B: 1, I: 1, BR: 1, SPAN: 1, SMALL: 1, CITE: 1, SUP: 1, SUB: 1 };
  var SKIP = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, SELECT: 1, OPTION: 1, TEXTAREA: 1 };

  function norm(s) { return String(s).replace(/\s+/g, " ").trim(); }
  function store(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }

  function pickLang() {
    var p = new URLSearchParams(location.search).get("lang");
    if (p && CODES.indexOf(p) > -1) { store(p); return p; }
    var s = stored();
    if (s && CODES.indexOf(s) > -1) return s;
    var nav = (navigator.language || "").toLowerCase().split("-")[0];
    return CODES.indexOf(nav) > -1 ? nav : "en";
  }

  /* A "mixed block": an element with at least one child element, where every descendant
     element is inline (links, bold, italics). Its whole inner HTML is one translation unit. */
  function isMixedBlock(el) {
    if (!el.children.length || SKIP[el.nodeName] || INLINE[el.nodeName]) return false;
    if (!norm(el.textContent)) return false;
    var all = el.getElementsByTagName("*");
    for (var i = 0; i < all.length; i++) if (!INLINE[all[i].nodeName]) return false;
    var t = 0; // needs real text outside the child elements too, otherwise text-node handling is fine
    for (var n = el.firstChild; n; n = n.nextSibling) if (n.nodeType === 3 && norm(n.nodeValue)) t++;
    return t > 0;
  }

  function collect(root) {
    root = root || document.body;
    var blocks = [], texts = [], inBlock = new Set();
    var els = root.querySelectorAll("*");
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.closest("#langSelect, .lang-item, script, style")) continue;
      var anc = el.parentElement, nested = false;
      while (anc && anc !== root) { if (inBlock.has(anc)) { nested = true; break; } anc = anc.parentElement; }
      if (nested) continue;
      if (isMixedBlock(el)) { blocks.push(el); inBlock.add(el); }
    }
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: function (n) {
      var p = n.parentNode;
      if (!p || SKIP[p.nodeName] || !norm(n.nodeValue)) return NodeFilter.FILTER_REJECT;
      if (p.closest && p.closest("#langSelect, .lang-item")) return NodeFilter.FILTER_REJECT;
      for (var a = p; a && a !== root; a = a.parentNode) if (inBlock.has(a)) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    }});
    var n; while ((n = w.nextNode())) texts.push(n);
    return { blocks: blocks, texts: texts };
  }

  function apply(pack, lang) {
    var S = pack.strings || {}, H = pack.html || {};
    var c = collect();
    c.blocks.forEach(function (el) { var t = H[norm(el.innerHTML)]; if (t) el.innerHTML = t; });
    c.texts.forEach(function (n) {
      var k = norm(n.nodeValue), t = S[k];
      if (t) n.nodeValue = n.nodeValue.replace(n.nodeValue.trim(), t);
    });
    document.querySelectorAll("[placeholder]").forEach(function (el) {
      var t = S[norm(el.getAttribute("placeholder"))]; if (t) el.setAttribute("placeholder", t);
    });
    document.querySelectorAll("img[alt]").forEach(function (el) {
      var t = S[norm(el.getAttribute("alt"))]; if (t) el.setAttribute("alt", t);
    });
    var tt = S[norm(document.title)]; if (tt) document.title = tt;
    document.documentElement.lang = lang;
    if (RTL.indexOf(lang) > -1) { document.documentElement.dir = "rtl"; document.body.classList.add("rtl"); }
    document.body.classList.add("lang-" + lang);
  }

  function withLang(href, lang) {
    try {
      var u = new URL(href, location.href);
      if (u.origin !== location.origin) return null;
      if (lang === "en") u.searchParams.delete("lang"); else u.searchParams.set("lang", lang);
      return u.pathname + u.search + u.hash;
    } catch (e) { return null; }
  }

  function carryLang(lang) {
    document.querySelectorAll("a[href]").forEach(function (a) {
      var h = a.getAttribute("href");
      if (!h || h.charAt(0) === "#" || /^(mailto|tel|sms|javascript):/i.test(h)) return;
      var v = withLang(h, lang); if (v) a.setAttribute("href", v);
    });
    document.querySelectorAll("form[action]").forEach(function (f) {
      var v = withLang(f.getAttribute("action"), lang); if (v) f.setAttribute("action", v);
    });
  }

  function picker(lang) {
    var sel = document.getElementById("langSelect");
    if (!sel) {
      var ul = document.querySelector("nav .nav-links");
      if (!ul) return;
      var li = document.createElement("li"); li.className = "lang-item";
      sel = document.createElement("select"); sel.className = "lang-select"; sel.id = "langSelect";
      sel.setAttribute("aria-label", "Language");
      LANGS.forEach(function (l) { var o = document.createElement("option"); o.value = l[0]; o.textContent = l[1]; sel.appendChild(o); });
      li.appendChild(sel); ul.appendChild(li);
    } else {
      sel = sel.cloneNode(true); document.getElementById("langSelect").replaceWith(sel); // drop old listeners
    }
    sel.value = lang;
    sel.addEventListener("change", function () {
      store(sel.value);
      var v = withLang(location.href, sel.value);
      location.href = v || location.href;
    });
  }

  window.L9H_I18N = { collect: collect, norm: norm, langs: LANGS };

  var lang = pickLang();
  var ready = new Promise(function (r) {
    if (document.readyState !== "loading") r(); else document.addEventListener("DOMContentLoaded", r);
  });

  if (lang === "en") { ready.then(function () { picker("en"); }); return; }

  // Hide the page briefly so visitors don't see English flash before the translation lands.
  var hide = document.createElement("style");
  hide.textContent = "html.i18n-pending body{opacity:0}";
  document.head.appendChild(hide);
  document.documentElement.classList.add("i18n-pending");
  var reveal = function () { document.documentElement.classList.remove("i18n-pending"); };
  setTimeout(reveal, 2500);

  var base = (document.currentScript && document.currentScript.src) || location.href;
  var data = fetch(new URL("lang/" + lang + ".json", base).href).then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; });

  Promise.all([data, ready]).then(function (res) {
    try { apply(res[0] || {}, lang); } catch (e) {}
    picker(lang); carryLang(lang); reveal();
  });
})();
