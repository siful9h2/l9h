"""List English text on the site that has no translation in lang/<code>.json.

Usage (from the repo root):
    python3 tools/i18n_missing.py [page.html ...] [--out missing.json]

Starts a local server, opens each page in English with Playwright, collects the
translatable units exactly as i18n.js does (window.L9H_I18N.collect), and reports
which ones are missing from each language file. With --out it writes
{"strings": [...], "html": [...]} of everything missing in ANY language, so the
translations can be written and merged into every lang/*.json.

Keys: "strings" = normalized plain text (also titles, placeholders, alt text);
"html" = normalized innerHTML of text blocks that contain inline tags (links, em,
strong). A translated "html" value must keep the same tags in the same order.
Names and words that read the same in every language (e.g. "Little Nine Heaven",
"Blog") may stay missing: the page just shows the English.
"""
import json, os, re, sys, glob, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright

args = sys.argv[1:]
out = None
if '--out' in args:
    i = args.index('--out'); out = args[i + 1]; del args[i:i + 2]
pages = args or sorted(glob.glob('*.html'))
langs = {os.path.basename(p)[:-5]: json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob('lang/*.json'))}

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=os.getcwd()))
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

JS = r'''() => { const I = window.L9H_I18N; if (!I) return null; const c = I.collect();
  const t = c.texts.map(n => I.norm(n.nodeValue));
  t.push(I.norm(document.title));
  document.querySelectorAll('[placeholder]').forEach(e => t.push(I.norm(e.getAttribute('placeholder'))));
  document.querySelectorAll('img[alt]').forEach(e => t.push(I.norm(e.getAttribute('alt'))));
  return { t: t, h: c.blocks.map(b => I.norm(b.innerHTML)) }; }'''

has_letters = lambda s: re.search(r'[A-Za-z]', re.sub(r'<[^>]+>', '', s))
miss = {'strings': {}, 'html': {}}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_context(locale='en-US').new_page()
    pg.add_init_script("try{localStorage.setItem('l9h-lang','en')}catch(e){}")
    for f in pages:
        pg.goto(f'http://127.0.0.1:{port}/{f}?lang=en'); pg.wait_for_timeout(300)
        r = pg.evaluate(JS)
        if r is None: print(f'{f}: i18n.js not loaded'); continue
        for kind, items in (('strings', r['t']), ('html', r['h'])):
            for s in items:
                if not s or not has_letters(s): continue
                lacking = [l for l, d in langs.items() if s not in d.get(kind, {})]
                if lacking: miss[kind].setdefault(s, {'page': f, 'langs': lacking})
    b.close()
srv.shutdown()

for kind in ('strings', 'html'):
    for s, v in miss[kind].items():
        print(f"[{kind}] {v['page']}: {s[:90]}  (missing: {','.join(v['langs'])})")
print(f"{len(miss['strings'])} strings and {len(miss['html'])} html blocks missing a translation in at least one language")
if out:
    json.dump({k: list(v) for k, v in miss.items()}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
