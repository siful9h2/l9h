#!/usr/bin/env python3
"""Build static, search-engine-visible copies of every page in each translated language.

  python3 tools/build_lang_pages.py            rebuild all languages (zh es fr de pt ru ja th ar hi)
  python3 tools/build_lang_pages.py zh th      rebuild only these languages
  python3 tools/build_lang_pages.py --check    QA the generated pages only (exit 1 on problems)

Why: i18n.js translates in the visitor's browser on the same URL, so Google only ever indexes English.
This renders each English page with i18n.js (headless Chromium), and saves the translated result as
<lang>/<page>.html, served at https://l9hkungfu.com/<lang>/<page>. Every version (English included)
gets hreflang tags pointing at all the others, and the language pages go into sitemap.xml.

English stays the source. Run this after any English or lang/*.json change, and at every weekly publish
(after releasing that day's blog posts). Output folders are generated: never edit them by hand.
A page/language pair is only built when enough of the page is actually translated (MIN_TRANSLATED).
"""
import os, re, sys, json, html, threading, functools, http.server
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = 'https://l9hkungfu.com'
LANGS = ['zh', 'es', 'fr', 'de', 'pt', 'ru', 'ja', 'th', 'ar', 'hi']
HREFLANG = {'zh': 'zh-Hans'}  # simplified Chinese; others are plain language codes (all countries)
LOCALE = {'en': 'en_US', 'zh': 'zh_CN', 'es': 'es_ES', 'fr': 'fr_FR', 'de': 'de_DE', 'pt': 'pt_BR',
          'ru': 'ru_RU', 'ja': 'ja_JP', 'th': 'th_TH', 'ar': 'ar_AR', 'hi': 'hi_IN'}
MIN_TRANSLATED = 0.6
MARK_A, MARK_B = '<!-- hreflang:start -->', '<!-- hreflang:end -->'
SM_A, SM_B = '  <!-- lang-pages:start -->', '  <!-- lang-pages:end -->'
SKIP_FILES = set()  # pages never translated

def read(f): return open(f, encoding='utf-8').read()
def write(f, s): open(f, 'w', encoding='utf-8').write(s)
def norm(s): return re.sub(r'\s+', ' ', s or '').strip()
def pages(): return sorted(f for f in os.listdir('.') if f.endswith('.html') and f not in SKIP_FILES)
def slug_url(f, lang='en'):
    slug = '' if f == 'index.html' else f[:-5]
    return f'{SITE}/{slug}' if lang == 'en' else f'{SITE}/{lang}/{slug}'
def indexable(src):
    m = re.search(r'name="robots" content="([^"]*)"', src)
    return not (m and 'noindex' in m.group(1))

def text_nodes(soup):
    for t in soup(['script', 'style', 'noscript', 'select']): t.decompose()
    body = soup.body or soup
    return [norm(s) for s in body.find_all(string=True) if len(re.sub(r'[^\w]', '', norm(s))) >= 3]

def coverage(en_html, tr_html):
    en = text_nodes(BeautifulSoup(en_html, 'html.parser'))
    tr = text_nodes(BeautifulSoup(tr_html, 'html.parser'))
    if not en: return 0.0
    same = sum(1 for a, b in zip(en, tr) if a == b) if len(en) == len(tr) else len(set(en) & set(tr))
    return 1 - same / len(en)

NEUTRALIZE = [(re.compile(r'\n?\s*' + re.escape(MARK_A) + r'.*?' + re.escape(MARK_B), re.S), ''),  # else i18n.js would jump to the live /<lang>/ page
              (re.compile(r'<script>'), '<script type="text/x-l9h-off">'),
              (re.compile(r'<script src="mobile-menu\.js" defer>'), '<script type="text/x-l9h-off" src="mobile-menu.js" defer>')]

CLEAN_JS = r"""(L) => {
  document.querySelectorAll('style').forEach(s => { if (s.textContent.indexOf('i18n-pending') > -1) s.remove(); });
  const de = document.documentElement;
  de.classList.remove('i18n-pending'); if (!de.className) de.removeAttribute('class');
  document.querySelectorAll('.lang-item').forEach(e => e.remove());
  document.querySelectorAll('a[href], form[action]').forEach(e => {
    const at = e.tagName === 'FORM' ? 'action' : 'href';
    let h = e.getAttribute(at); if (!h) return;
    h = h.replace(/([?&])lang=[a-z]{2}(?=&|#|$)/, '$1').replace(/\?&/, '?').replace(/[?&](?=#|$)/, '');
    if (h === '/') h = 'index.html';
    else if (h.charAt(0) === '/' && h.charAt(1) !== '/') h = h.slice(1);
    e.setAttribute(at, h);
  });
  document.querySelectorAll('script[type="text/x-l9h-off"]').forEach(s => s.removeAttribute('type'));
  return '<!DOCTYPE html>\n' + de.outerHTML;
}"""

def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Quiet, directory=ROOT)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

def render(langs):
    from playwright.sync_api import sync_playwright
    srv = serve(); base = f'http://127.0.0.1:{srv.server_address[1]}'
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch(); ctx = br.new_context()
        def route(r):
            f = r.request.url.split('?')[0].split('#')[0][len(base) + 1:] or 'index.html'
            if f.endswith('.html') and os.path.exists(f):
                s = read(f)
                for rx, rep in NEUTRALIZE: s = rx.sub(rep, s)
                r.fulfill(status=200, content_type='text/html; charset=utf-8', body=s)
            else: r.continue_()
        ctx.route(re.compile(r'.*\.html(\?.*)?$'), route)
        pg = ctx.new_page()
        for f in pages():
            for L in langs:
                pg.goto(f'{base}/{f}?lang={L}')
                try:
                    pg.wait_for_function("l => document.documentElement.lang === l && !document.documentElement.classList.contains('i18n-pending')", arg=L, timeout=10000)
                except Exception:
                    print(f'  ! {L}/{f}: translation did not load'); continue
                out[(f, L)] = pg.evaluate(CLEAN_JS, L)
        br.close()
    srv.shutdown()
    return out

def rel(u):
    return bool(u) and not re.match(r'^(#|[a-z][a-z0-9+.-]*:|//|/|\.\./)', u, re.I)

def fix_assets(soup):
    for tag in soup.find_all(True):
        for at in ('src', 'href', 'poster', 'data-pending-src', 'action'):
            v = tag.get(at)
            if not v or not rel(v): continue
            if at in ('href', 'action') and tag.name in ('a', 'form') and re.match(r'^[\w-]+\.html([?#].*)?$', v): continue
            tag[at] = '../' + v
        if tag.get('srcset'):
            tag['srcset'] = ', '.join(('../' + x.strip() if rel(x.strip()) else x.strip()) for x in tag['srcset'].split(','))
        if tag.get('style') and 'url(' in tag['style']:
            tag['style'] = re.sub(r'url\((["\']?)(?!["\']|[a-z]+:|/|\.\./|#)', r'url(\1../', tag['style'])
    for st in soup.find_all('style'):
        if st.string and 'url(' in st.string:
            st.string = re.sub(r'url\((["\']?)(?!["\']|[a-z]+:|/|\.\./|#)', r'url(\1../', st.string)

def hreflang_block(f, avail):
    lines = [MARK_A, f'<link rel="alternate" hreflang="en" href="{slug_url(f)}"/>']
    for L in LANGS:
        if L in avail: lines.append(f'<link rel="alternate" hreflang="{HREFLANG.get(L, L)}" href="{slug_url(f, L)}"/>')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{slug_url(f)}"/>')
    lines.append(MARK_B)
    return '\n  '.join(lines)

def set_meta(soup, attr, key, val):
    m = soup.find('meta', attrs={attr: key})
    if m: m['content'] = val
    else:
        m = soup.new_tag('meta'); m[attr] = key; m['content'] = val; soup.head.append(m)

def finish_lang_page(f, L, tr, pack, block):
    soup = BeautifulSoup(tr, 'html.parser')
    S = pack.get('strings', {})
    de = soup.html; de['lang'] = L; de['data-static-lang'] = L
    for c in soup.head.find_all('link', rel='canonical'): c['href'] = slug_url(f, L)
    for m in soup.head.find_all('meta', attrs={'property': 'og:url'}): m['content'] = slug_url(f, L)
    set_meta(soup, 'property', 'og:locale', LOCALE[L])
    for attr, key in (('name', 'description'), ('property', 'og:description'), ('property', 'og:title'),
                      ('name', 'twitter:title'), ('name', 'twitter:description'), ('property', 'og:image:alt')):
        m = soup.head.find('meta', attrs={attr: key})
        if m and S.get(norm(m.get('content'))): m['content'] = S[norm(m['content'])]
    for sc in soup.find_all('script', type='application/ld+json'):
        sc.string = sc.string.replace('"inLanguage": "en"', f'"inLanguage": "{L}"') if sc.string else sc.string
    fix_assets(soup)
    s = str(soup)
    s = re.sub(re.escape(MARK_A) + r'.*?' + re.escape(MARK_B), '', s, flags=re.S)
    s = re.sub(r'(<link[^>]*rel="canonical"[^>]*/?>)', lambda m: m.group(1) + '\n  ' + block, s, count=1)
    if not s.lstrip().lower().startswith('<!doctype'): s = '<!DOCTYPE html>\n' + s
    return s

def add_hreflang_to_english(f, block):
    s = read(f)
    s2 = re.sub(r'\n?\s*' + re.escape(MARK_A) + r'.*?' + re.escape(MARK_B), '', s, flags=re.S)
    s2 = re.sub(r'(<link[^>]*rel="canonical"[^>]*/?>)', lambda m: m.group(1) + '\n  ' + block, s2, count=1)
    if 'property="og:locale"' not in s2:
        s2 = re.sub(r'(<meta property="og:url"[^>]*>)', lambda m: m.group(1) + '\n  <meta property="og:locale" content="en_US"/>', s2, count=1)
    if s2 != s: write(f, s2)

def update_sitemap(built):
    sm = read('sitemap.xml')
    sm = re.sub(r'\n' + re.escape(SM_A) + r'.*?' + re.escape(SM_B), '', sm, flags=re.S)
    lines = [SM_A]
    for L in LANGS:
        for f in pages():
            if (f, L) in built and f'<loc>{slug_url(f)}</loc>' in sm:
                lines.append(f'  <url><loc>{slug_url(f, L)}</loc></url>')
    lines.append(SM_B)
    sm = sm.replace('</urlset>', '\n'.join(lines) + '\n</urlset>')
    write('sitemap.xml', sm)

def check():
    problems, n = [], 0
    for L in LANGS:
        if not os.path.isdir(L): continue
        for f in sorted(os.listdir(L)):
            if not f.endswith('.html'): continue
            n += 1; s = read(os.path.join(L, f))
            if f'data-static-lang="{L}"' not in s: problems.append(f'{L}/{f}: missing data-static-lang')
            if 'rel="canonical"' in read(f) and 'noindex' not in s and not re.search(r'<link[^>]*href="' + re.escape(slug_url(f, L)) + r'"[^>]*rel="canonical"|<link[^>]*rel="canonical"[^>]*href="' + re.escape(slug_url(f, L)) + '"', s): problems.append(f'{L}/{f}: wrong canonical')
            for h in re.findall(r'href="([\w-]+\.html)', s):
                if not os.path.exists(os.path.join(L, h)): problems.append(f'{L}/{f}: broken link {h}')
            for h in re.findall(r'(?<![-\w])(?:src|href)="\.\./([^"#?]+)"', s):
                if not os.path.exists(h): problems.append(f'{L}/{f}: missing asset {h}')
            if re.search(r'(?:src|href)="(?!\.\./|https?:|#|mailto:|tel:|data:|//)(?![\w-]+\.html)[^"]+"', s):
                problems.append(f'{L}/{f}: asset path not rewritten: ' + re.search(r'(?:src|href)="(?!\.\./|https?:|#|mailto:|tel:|data:|//)(?![\w-]+\.html)([^"]+)"', s).group(1))
            for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
                try: json.loads(m)
                except Exception as e: problems.append(f'{L}/{f}: invalid JSON-LD ({e})')
            if 'lang=' in ''.join(re.findall(r'href="[^"]*"', s)) and re.search(r'href="[^"]*[?&]lang=', s): problems.append(f'{L}/{f}: ?lang= left in links')
    if problems:
        print('LANG QA FAILED:'); [print(' -', x) for x in problems[:60]]; return 1
    print(f'Lang QA passed: {n} language pages.'); return 0

def main(args):
    if '--check' in args: return check()
    langs = [a for a in args if a in LANGS] or LANGS
    print(f'Rendering {len(pages())} pages x {len(langs)} languages...')
    out = render(langs)
    packs = {L: json.load(open(f'lang/{L}.json', encoding='utf-8')) for L in LANGS}
    built = set()
    # keep pages already built for languages not being rebuilt this run
    for L in LANGS:
        if L in langs or not os.path.isdir(L): continue
        for f in os.listdir(L):
            if f.endswith('.html'): built.add((f, L))
    cov = {}
    for (f, L), tr in out.items():
        c = coverage(read(f), tr); cov[(f, L)] = c
        if c >= MIN_TRANSLATED: built.add((f, L))
        else: built.discard((f, L)); print(f'  - skip {L}/{f}: only {c:.0%} translated')
    for L in langs:
        os.makedirs(L, exist_ok=True)
        for f in os.listdir(L):
            if f.endswith('.html') and (f, L) not in out: os.remove(os.path.join(L, f))
    for f in pages():
        avail = {L for L in LANGS if (f, L) in built}
        idx = indexable(read(f))
        block = hreflang_block(f, avail) if idx else ''
        if idx: add_hreflang_to_english(f, block)
        for L in langs:
            if (f, L) in out:  # under-translated pages are still written (links must work) but kept out of search
                page = finish_lang_page(f, L, out[(f, L)], packs[L], block if (f, L) in built else '')
                if (f, L) not in built:
                    page = re.sub(r'<meta content="[^"]*" name="robots"/>', '', page)
                    page = page.replace('</head>', '<meta content="noindex,follow" name="robots"/>\n</head>', 1)
                write(os.path.join(L, f), page)
    update_sitemap(built)
    print(f'Built {sum(1 for k in built if k[1] in langs)} language pages; ' +
          ', '.join(f'{L}: {sum(1 for k in built if k[1] == L)}' for L in langs))
    return check()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
