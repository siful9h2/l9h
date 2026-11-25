#!/usr/bin/env python3
"""Build the travel pages: worldwide.html (hub) and one page per target country.

Focus (owner, 2026-11-20): Shih Shui (marrow washing, Xi Sui Gong) and Taoist lovemaking, taught in person
only, anywhere in the world; arrangements made individually by email. The pages reuse system-shih-shui.html's
template (head styles, nav, footer) unchanged. Edit the text here, then run:

    python3 tools/build_country_pages.py && python3 tools/build_lang_pages.py

Countries live in tools/countries.json and their sentences, per language, in tools/country_templates.json.
`--check` validates the data. A run writes the pages, the country sentences into lang/*.json and any missing
sitemap entries. Each country page is translated only into its own language (PAGE_LANGS, read by
build_lang_pages.py; English-only countries get no language versions); the hub is translated into every language.
"""
import json, os, re, sys

BASE = 'https://l9hkungfu.com'
TEMPLATE = 'system-shih-shui.html'

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LANGS = ['zh', 'es', 'fr', 'de', 'pt', 'ru', 'ja', 'th', 'ar', 'hi', 'it', 'el']
DATA = json.load(open(os.path.join(HERE, 'countries.json'), encoding='utf-8'))['countries']
TPL = json.load(open(os.path.join(HERE, 'country_templates.json'), encoding='utf-8'))
# slug, English name, language of the country's own page ('en' = English only)
COUNTRIES = [(c['slug'], c['name'], c['lang']) for c in DATA]
# English wording inside sentences ('the United Kingdom'); defaults to the name
def en_in(c): return c.get('en_in', c['name'])
def page_name(slug): return f'marrow-washing-{slug}.html'
PAGE_LANGS = {page_name(s): ([] if L == 'en' else [L]) for s, _, L in COUNTRIES}

# ---- shared text (same keys on every page, so each is translated once per language) ----
INTRO_2 = ("The two practices belong together. Shih Shui is nei-kung: specific breathing methods, strengthening of "
           "the deep structures and directed energy circulation, with work on sexual energy at its centre. Taoist "
           "lovemaking is the classical art of conserving, transforming and circulating that same energy, the "
           "<em>jing</em>, instead of spending it carelessly.")
DIRECT = ("Shih Shui has been widely and badly copied, and much of what circulates under its name is taught wrong by "
          "people who never received correction. Here it is passed on the way it always has been: in person, from "
          "teacher to student, stage by stage, with every detail corrected, as the masters before taught it. "
          "It is not learned from a book.")
LINEAGE_1 = ('Sifu Ajay Kumra has practiced for 20 years and taught for 10, in the United States, Thailand and China. '
             'He trained under <a href="teacher-mcneil.html">Master James McNeil (麥克傑模)</a>, Gate Keeper of the '
             'Little Nine Heaven Wu Tao system.')
LINEAGE_2 = ('Master McNeil trained with <a href="teacher-chiao.html">Grandmaster Chiao Chang-Hung (喬長虹)</a> in '
             'Taipei from 1984 until Chiao\'s death in 2001, and before that with <a href="teacher-hsu.html">Master '
             'Hsu Hong-Chi (許鴻基)</a>, "The Man With the Magic Hands". It was Grandmaster Chiao who chose to '
             'release Shih Shui beyond a handful of martial disciples.')
LINEAGE_3 = ("Master McNeil learned the bedchamber arts from Master Hsu Hong-Chi, from Master Huang, and from four "
             "women in the mountains who were experts in them.")
HOW = [
    "Private and in person only: there are no video or online lessons.",
    "One-on-one, as a couple, or in a small group.",
    "Open to adult men and women. No martial arts experience is needed.",
    "The length of the visit, the schedule and travel are arranged individually.",
]
CONTACT = ('Write through the <a href="index.html#contact">contact form</a> or to '
           '<a href="mailto:info@l9hkungfu.com">info@l9hkungfu.com</a>, say where you are and what you would like '
           'to learn, and the details are worked out with you personally.')
FAQ_SHARED = [
    ("Are lessons available online?",
     "No. Shih Shui and Taoist lovemaking are taught in person only, so every detail can be corrected."),
    ("Do I need a partner?",
     "No. Men and women study these practices, as a couple or single."),
    ("How is a visit arranged?",
     "By email, individually. Write through the contact form or to info@l9hkungfu.com with where you are and what you would like to learn."),
]

def country_text(C, label=None):
    label = label or C
    return {
        'title': f'Marrow Washing & Taoist Lovemaking in {C}',
        'desc': (f'Private, in-person Shih Shui (marrow washing, Xi Sui Gong) and Taoist lovemaking with Sifu Ajay '
                 f'Kumra, who travels to students in {C}.'),
        'eyebrow': f'Private Instruction · {C}',
        'h1': f'Marrow Washing & Taoist Lovemaking in {C}',
        'where': f'{C}, at your location',
        'intro': (f'Sifu Ajay Kumra travels to {C} to teach <a href="system-shih-shui.html">Shih Shui</a> (bone '
                  f'marrow washing, Xi Sui Gong 洗髓功) and <a href="system-taoist-lovemaking.html">Taoist '
                  f'lovemaking</a> (fang chung shu) privately and in person. He comes to you: lessons take place '
                  f'where you are, one-on-one or in a small group.'),
        'elsewhere_h': f'Not in {C}?',
        'faq': [
            (f'Can I learn marrow washing (Xi Sui Gong) in {C}?',
             f'Yes. Sifu Ajay Kumra travels to {C} to teach Shih Shui privately and in person. Visits are arranged individually by email.'),
            (f'Is Taoist lovemaking taught in {C}?',
             f'Yes, privately, to adults who approach it as cultivation. It is usually taught together with Shih Shui, because the two overlap directly.'),
        ] + FAQ_SHARED,
        'cta_h': f'Learn in {C}',
        'crumb': label,
        'area': {"@type": "Country", "name": label},
    }

HUB_SENTENCE = 'Sifu Ajay travels to students in any country. He also teaches in Santee, California (San Diego County).'
ELSEWHERE = ('Sifu Ajay travels to students <a href="worldwide.html">anywhere in the world</a>. He also teaches in '
             'Santee, California (San Diego County).')

HUB = {
    'title': 'Marrow Washing & Taoist Lovemaking Worldwide',
    'desc': ('Private, in-person Shih Shui (marrow washing, Xi Sui Gong) and Taoist lovemaking with Sifu Ajay Kumra, '
             'who travels to students anywhere in the world.'),
    'eyebrow': 'Private Instruction · Worldwide',
    'h1': 'Marrow Washing & Taoist Lovemaking, Anywhere in the World',
    'where': 'Anywhere in the world, at your location',
    'intro': ('Sifu Ajay Kumra travels to students anywhere in the world to teach <a href="system-shih-shui.html">'
              'Shih Shui</a> (bone marrow washing, Xi Sui Gong 洗髓功) and <a href="system-taoist-lovemaking.html">'
              'Taoist lovemaking</a> (fang chung shu) privately and in person. He comes to you: lessons take place '
              'where you are, one-on-one or in a small group.'),
    'faq': [
        ('Where do you teach marrow washing (Xi Sui Gong)?',
         'Anywhere in the world. Sifu Ajay Kumra travels to students at their location, and also teaches in Santee, California (San Diego County).'),
        ('Is Taoist lovemaking taught outside the United States?',
         'Yes, privately, to adults who approach it as cultivation, wherever they are. It is usually taught together with Shih Shui, because the two overlap directly.'),
    ] + FAQ_SHARED,
    'cta_h': 'Learn Wherever You Are',
    'crumb': 'Worldwide',
    'area': 'Worldwide',
}

def esc(s): return s.replace('&', '&amp;').replace('"', '&quot;')
def strip_tags(s): return re.sub(r'<[^>]+>', '', s)

def jsonld(obj): return '  <script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n  </script>\n'

def body(t, others):
    facts = [('Teaches', 'Shih Shui (Xi Sui Gong) and Taoist lovemaking'), ('Where', t['where']),
             ('Format', 'Private and in person only'), ('Arrangements', 'Made individually by email')]
    fg = ''.join(f'<div class="fact"><div class="dot"></div><strong>{a}</strong><span>{b}</span></div>' for a, b in facts)
    faq = '\n'.join(f'        <p><strong>{q}</strong></p>\n        <p>{a}</p>' for q, a in t['faq'])
    how = '\n'.join(f'          <li>{x}</li>' for x in HOW)
    return f'''  <div class="page-hero">
    <div class="page-hero-bg"></div>
    <img class="page-hero-photo" data-pending-src="images/system-shih-shui.jpg" alt="Shih Shui internal training" onerror="this.style.display='none'"/>
    <div class="page-hero-content">
      <p class="eyebrow">{t['eyebrow']}</p>
      <h1>{t['h1'].replace('&', '&amp;')}</h1>
      <p class="subtitle">Shih Shui · Fang Chung Shu · In Person</p>
      <div class="hero-divider"></div>
    </div>
  </div>

  <section class="bio-section">
    <div class="bio-grid">
      <div class="reveal">
        <div class="portrait-frame">
          <img data-pending-src="images/system-shih-shui.jpg" alt="Shih Shui internal training" onerror="this.style.display='none'"/>
          <div class="portrait-placeholder">☯</div>
          <p class="portrait-placeholder-text">Photo</p>
        </div>
        <div class="portrait-caption">
          <strong>Sifu Ajay Kumra</strong>
          <span>Travels to students anywhere</span>
        </div>
      </div>
      <div class="bio-content reveal">
        <p class="section-label">{t['eyebrow']}</p>
        <h2>Shih Shui and Taoist Lovemaking, Taught in Person</h2>
        <div class="gold-line"></div>
        <div class="facts-grid">{fg}</div>
        <p>{t['intro']}</p>

        <p>{INTRO_2}</p>

        <h3>Direct Transmission, Not a Book</h3>
        <p>{DIRECT}</p>

        <h3>The Lineage</h3>
        <p>{LINEAGE_1}</p>
        <p>{LINEAGE_2}</p>
        <p>{LINEAGE_3}</p>

        <h3>How It Works</h3>
        <ul>
{how}
        </ul>
        <p>{CONTACT}</p>

        <h3>{t.get('elsewhere_h', 'Where Sifu Ajay Teaches')}</h3>
        {others}

        <h3>Questions</h3>
{faq}
      </div>
    </div>
  </section>

  <div class="cta-bar">
    <h2>{t['cta_h']}</h2>
    <p>Private, in-person instruction in Shih Shui and Taoist lovemaking, arranged individually by email.</p>
    <a href="index.html#contact" class="btn btn-light">Get in Touch</a>
  </div>

'''

def build(fname, t, others, area):
    src = open(TEMPLATE, encoding='utf-8').read()
    head, rest = src.split('  <div class="page-hero">', 1)
    footer = rest[rest.index('  <footer>'):]
    url = f'{BASE}/{fname[:-5]}'
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(t["title"])}</title>', head)
    head = re.sub(r'<meta name="description" content="[^"]*"/>', f'<meta name="description" content="{esc(t["desc"])}"/>', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*"/>', f'<link rel="canonical" href="{url}"/>', head)
    head = re.sub(r'<!-- hreflang:start -->.*?<!-- hreflang:end -->', '<!-- hreflang:start -->\n  <!-- hreflang:end -->', head, flags=re.S)
    head = re.sub(r'<meta property="og:title" content="[^"]*"/>', f'<meta property="og:title" content="{esc(t["title"])}"/>', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*"/>', f'<meta property="og:description" content="{esc(t["desc"])}"/>', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*"/>', f'<meta property="og:url" content="{url}"/>', head)
    head = head.replace('<meta property="og:type" content="article"/>', '<meta property="og:type" content="website"/>')
    head = re.sub(r'\s*<script type="application/ld\+json">.*?</script>\n?', '\n', head, flags=re.S)
    ld = jsonld({"@context": "https://schema.org", "@type": "Service",
                 "name": t['title'], "description": t['desc'], "url": url,
                 "serviceType": "Shih Shui (bone marrow washing) and Taoist lovemaking instruction",
                 "provider": {"@type": "MartialArtsSchool", "@id": f"{BASE}/#school", "name": "Little Nine Heaven SoCal",
                              "url": BASE, "email": "info@l9hkungfu.com"},
                 "areaServed": area, "inLanguage": "en"})
    ld += jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": "Shih Shui", "item": f"{BASE}/system-shih-shui"},
        {"@type": "ListItem", "position": 3, "name": t['crumb'], "item": url}]})
    ld += jsonld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in t['faq']]})
    head = head.replace('</head>', ld + '</head>', 1) if '</head>' in head else head
    html = head + body(t, others) + footer
    if '</head>' not in head:  # head closes inside the template's nav part; insert JSON-LD before </head> there
        html = html.replace('</head>', ld + '</head>', 1)
    html = re.sub(r'\n{3,}', '\n\n', html)
    open(fname, 'w', encoding='utf-8').write(html)
    print('wrote', fname)

# English keys whose translations come from country_templates.json, in the order of its 'country' lists
def country_keys(C, label=None):
    t = country_text(C, label)
    return [('strings', t['eyebrow']), ('strings', t['h1']), ('strings', t['where']), ('strings', t['elsewhere_h']),
            ('strings', t['faq'][0][0]), ('strings', t['faq'][0][1]), ('strings', t['faq'][1][0]),
            ('strings', t['cta_h']), ('strings', t['desc']), ('html', t['intro'])]

def norm(x): return re.sub(r'\s+', ' ', x).strip()
def tags(x): return re.findall(r'</?([a-z]+)', x)

def forms(c, L):
    """{name}, {in}, {In}, {to} for country c in language L (its own language)."""
    loc = c.get('local', {})
    name = loc.get('name') or c['names'][L]
    rule = TPL['rules'][L]
    if 'in' in loc: inn = loc['in']
    elif rule['in'] == 'required': raise ValueError(f"{c['slug']}: countries.json needs local.in for language {L}")
    else: inn = rule['in'].format(name=name)
    to = loc.get('to') or rule['to'].format(name=name, **{'in': inn})
    return {'name': name, 'in': inn, 'In': inn[:1].upper() + inn[1:], 'to': to}

def problems():
    out = []
    slugs = [c['slug'] for c in DATA]
    if len(set(slugs)) != len(slugs): out.append('duplicate slugs in countries.json')
    for c in DATA:
        for k in ('slug', 'name', 'lang', 'names'):
            if k not in c: out.append(f"{c.get('slug')}: missing '{k}'")
        if not re.fullmatch(r'[a-z0-9-]+', c.get('slug', '')): out.append(f"{c.get('slug')}: slug must be lowercase a-z, 0-9, -")
        L = c.get('lang')
        if L != 'en' and L not in LANGS: out.append(f"{c['slug']}: lang '{L}' is not a site language (use one of {LANGS} or en)")
        miss = [x for x in LANGS if x not in c.get('names', {})]
        if miss: out.append(f"{c['slug']}: names missing for {miss}")
        if L in LANGS:
            if L not in TPL['country']: out.append(f"{c['slug']}: no sentence templates for {L} in country_templates.json")
            else:
                try: forms(c, L)
                except ValueError as e: out.append(str(e))
    return out

def write_translations():
    """Fill lang/<L>.json with the generated country-page sentences, the hub sentence and the country names."""
    packs = {L: json.load(open(os.path.join(ROOT, 'lang', f'{L}.json'), encoding='utf-8')) for L in LANGS}
    n = 0
    for L in LANGS:
        P = packs[L]
        P['strings'][norm(HUB_SENTENCE)] = TPL['shared']['hub'][L]
        if L in TPL['shared']['elsewhere']: P['html'].setdefault(norm(ELSEWHERE), TPL['shared']['elsewhere'][L])
        for c in DATA:
            P['strings'][c['name']] = c['names'][L]
    for c in DATA:
        L = c['lang']
        if L == 'en': continue
        f = forms(c, L)
        for (sec, key), tpl in zip(country_keys(en_in(c), c['name']), TPL['country'][L]):
            val = tpl.replace('{In}', f['In']).replace('{in}', f['in']).replace('{to}', f['to']).replace('{name}', f['name'])
            if sec == 'html' and tags(val) != tags(key): raise ValueError(f'{c["slug"]}/{L}: tag mismatch in template')
            if '{' in val: raise ValueError(f'{c["slug"]}/{L}: unfilled placeholder in {val!r}')
            packs[L][sec][norm(key)] = val; n += 1
    for L, P in packs.items():
        open(os.path.join(ROOT, 'lang', f'{L}.json'), 'w', encoding='utf-8').write(
            json.dumps(P, ensure_ascii=False, separators=(',', ':')))
    print(f'translations: {n} country sentences written')

def update_sitemap():
    p = os.path.join(ROOT, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
    add = ''
    for fname in ['worldwide.html'] + [page_name(c['slug']) for c in DATA]:
        loc = f'{BASE}/{fname[:-5]}'
        if f'<loc>{loc}</loc>' not in s:
            add += f'  <url><loc>{loc}</loc><lastmod>{__import__("datetime").date.today()}</lastmod></url>\n'
    if add:
        s = s.replace('  <!-- lang-pages:start -->', add + '  <!-- lang-pages:start -->', 1)
        open(p, 'w', encoding='utf-8').write(s); print('sitemap: added', add.count('<url>'))

def main():
    errs = problems()
    if errs or '--check' in sys.argv:
        print('\n'.join(errs) if errs else 'countries.json OK: ' + ', '.join(c['name'] for c in DATA))
        sys.exit(1 if errs else 0)
    os.chdir(ROOT)
    links = '\n'.join(f'          <li><a href="{page_name(s)}">{C}</a></li>' for s, C, _ in sorted(COUNTRIES, key=lambda x: x[1]))
    build('worldwide.html', HUB,
          f'<p>{HUB_SENTENCE}</p>\n        <ul class="country-list">\n{links}\n        </ul>',
          HUB['area'])
    for c in DATA:
        t = country_text(en_in(c), c['name'])
        build(page_name(c['slug']), t, f'<p>{ELSEWHERE}</p>', t['area'])
    write_translations()
    update_sitemap()
    print('next: python3 tools/build_lang_pages.py')

if __name__ == '__main__':
    main()
