#!/usr/bin/env python3
"""Blog release + QA tool for l9hkungfu.com.

  python3 tools/blog.py due [YYYY-MM-DD]        list scheduled posts due on/before the date (default today, PT)
  python3 tools/blog.py release SLUG YYYY-MM-DD  publish a draft from origin/drafts/blog and rebuild indexes
  python3 tools/blog.py check                    pre-release QA over the whole site (exit 1 on problems)
  python3 tools/blog.py indexnow URL [URL...]     print IndexNow ping links (fetch each one; 200/202 = accepted)
"""
import json, re, subprocess, sys, os, datetime, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CAL = 'blog-calendar.json'
DRAFTS = 'origin/drafts/blog'
SITE = 'https://l9hkungfu.com'

def load(): return json.load(open(CAL, encoding='utf-8'))
def save(c): open(CAL, 'w', encoding='utf-8').write(json.dumps(c, indent=2, ensure_ascii=False) + '\n')
def read(f): return open(f, encoding='utf-8').read()
def write(f, s): open(f, 'w', encoding='utf-8').write(s)
def draft(name): return subprocess.run(['git', 'show', f'{DRAFTS}:{name}'], capture_output=True, text=True, check=True).stdout

def published(c): return sorted([p for p in c['posts'] if p['status'] == 'published'], key=lambda p: p['release'])

def draft_cards():
    s = draft('blog.html')
    return {m.group(1): m.group(0) for m in re.finditer(r'\s*<a class="post-card" href="([^"]+)\.html">.*?</a>', s, re.S)}

def draft_shorts():
    s = draft('blog-hsing-i-part-1-origins-and-eight-fundamentals.html')
    grid = s[s.index('teachers-nav-grid'):]
    return {m.group(1): html.unescape(m.group(2)) for m in re.finditer(r'<a href="(blog-[^"]+)\.html"[^>]*>([^<]+)</a>', grid)}

def rebuild(c):
    pubs = published(c)
    cards = draft_cards(); shorts = draft_shorts()
    # blog index: newest first
    s = read('blog.html')
    i = s.index('<div class="post-list">') + len('<div class="post-list">')
    j = s.index('\n        </div>', i)
    s = s[:i] + ''.join(cards[p['slug']] for p in reversed(pubs)) + s[j:]
    write('blog.html', s)
    # "From the Blog" box in every published post
    for p in pubs:
        f = p['slug'] + '.html'; s = read(f)
        i = s.index('<div class="teachers-nav-grid">') + len('<div class="teachers-nav-grid">')
        j = s.index('\n      </div>', i)
        links = '\n        <a href="blog.html">All posts</a>' + ''.join(
            '\n        <a href="%s.html"%s>%s</a>' % (q['slug'], ' class="current"' if q['slug'] == p['slug'] else '', html.escape(shorts.get(q['slug'], q['slug'])))
            for q in pubs)
        write(f, s[:i] + links + s[j:])
    # sitemap
    sm = read('sitemap.xml')
    def upsert(path, date):
        nonlocal sm
        loc = f'<loc>{SITE}/{path}</loc>'
        if loc in sm:
            sm = re.sub(re.escape(loc) + r'<lastmod>[^<]*</lastmod>', f'{loc}<lastmod>{date}</lastmod>', sm)
        else:
            sm = sm.replace('</urlset>', f'  <url>{loc}<lastmod>{date}</lastmod></url>\n</urlset>')
    latest = pubs[-1]['release'] if pubs else datetime.date.today().isoformat()
    upsert('blog', latest)
    for p in pubs: upsert(p['slug'], p['release'])
    write('sitemap.xml', sm)

def release(slug, date):
    c = load()
    post = next((p for p in c['posts'] if p['slug'] == slug), None)
    if not post: sys.exit(f'{slug} is not in {CAL}')
    s = draft(slug + '.html').replace('RELEASE_DATE', date)
    if os.path.exists('mobile.css') and 'mobile.css' not in s:
        s = s.replace('</head>', '  <link rel="stylesheet" href="mobile.css" />\n  <script src="mobile-menu.js" defer></script>\n</head>', 1)
    write(slug + '.html', s)
    post['status'] = 'published'; post['release'] = date
    save(c); rebuild(c)
    print(f'released {slug} on {date}')
    print('After pushing and confirming it is live, ping IndexNow with:')
    indexnow([slug, 'blog'])
    return check()

def due(date):
    for p in load()['posts']:
        if p['status'] == 'scheduled' and p['release'] <= date: print(p['slug'], p['release'])

def check():
    problems = []
    files = sorted(f for f in os.listdir('.') if f.endswith('.html'))
    sm = read('sitemap.xml')
    pubs = {p['slug'] for p in published(load())}
    for f in files:
        s = read(f); slug = f[:-5]
        for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try: json.loads(m)
            except Exception as e: problems.append(f'{f}: invalid JSON-LD ({e})')
        if 'RELEASE_DATE' in s: problems.append(f'{f}: RELEASE_DATE placeholder left in page')
        for h in re.findall(r'href="([^"#:?]+\.html)', s):
            if not os.path.exists(h): problems.append(f'{f}: broken link to {h}')
        if os.path.exists('mobile.css') and 'href="mobile.css"' not in s: problems.append(f'{f}: missing mobile.css link')
        if f.startswith('blog'):
            t = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1))
            d = re.search(r'name="description" content="([^"]*)"', s).group(1)
            canon = re.search(r'rel="canonical" href="([^"]+)"', s).group(1)
            want = f'{SITE}/blog' if f == 'blog.html' else f'{SITE}/{slug}'
            if len(t) > 60: problems.append(f'{f}: title is {len(t)} chars (keep under 60)')
            if not 70 <= len(d) <= 160: problems.append(f'{f}: meta description is {len(d)} chars (aim for 70-160)')
            if canon != want: problems.append(f'{f}: canonical {canon} should be {want}')
            if f'<loc>{want}</loc>' not in sm: problems.append(f'{f}: not in sitemap.xml')
            if f != 'blog.html' and slug not in pubs: problems.append(f'{f}: page is public but not marked published in {CAL}')
    for p in pubs:
        if f'href="{p}.html"' not in read('blog.html'): problems.append(f'blog.html: no card for {p}')
    if problems:
        print('QA FAILED:'); [print(' -', x) for x in problems]; return 1
    print(f'QA passed: {len(files)} pages, {len(pubs)} blog posts published.')
    return 0

INDEXNOW_KEY = '212a9b89e41f158056d6f3102f117957'
def indexnow(urls):
    from urllib.parse import quote
    for u in urls:
        if not u.startswith('http'): u = f'{SITE}/{u.lstrip("/")}'
        print(f'https://api.indexnow.org/indexnow?url={quote(u, safe=":/")}&key={INDEXNOW_KEY}')

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == 'due': due(a[1] if len(a) > 1 else datetime.date.today().isoformat())
    elif a[0] == 'release': sys.exit(release(a[1], a[2]))
    elif a[0] == 'check': sys.exit(check())
    elif a[0] == 'indexnow': indexnow(a[1:])
    else: sys.exit(__doc__)
