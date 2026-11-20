#!/usr/bin/env python3
"""Build the travel pages: worldwide.html (hub) and one page per target country.

Focus (owner, 2026-11-20): Shih Shui (marrow washing, Xi Sui Gong) and Taoist lovemaking, taught in person
only, anywhere in the world; arrangements made individually by email. The pages reuse system-shih-shui.html's
template (head styles, nav, footer) unchanged. Edit the text here, then run:

    python3 tools/build_country_pages.py && python3 tools/build_lang_pages.py

Each country page is translated only into its own language (PAGE_LANGS in build_lang_pages.py reads COUNTRIES
below); the hub is translated into every language.
"""
import json, os, re, sys

BASE = 'https://l9hkungfu.com'
TEMPLATE = 'system-shih-shui.html'

# slug, English name, language of the country's own page
COUNTRIES = [
    ('thailand', 'Thailand', 'th'),
    ('china', 'China', 'zh'),
    ('greece', 'Greece', 'el'),
    ('italy', 'Italy', 'it'),
    ('spain', 'Spain', 'es'),
    ('mexico', 'Mexico', 'es'),
]
def page_name(slug): return f'marrow-washing-{slug}.html'
PAGE_LANGS = {page_name(s): [L] for s, _, L in COUNTRIES}

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

def country_text(C):
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
        'crumb': C,
        'area': {"@type": "Country", "name": C},
    }

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
        <p>{others}</p>

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

def main():
    links = ' · '.join(f'<a href="{page_name(s)}">{C}</a>' for s, C, _ in COUNTRIES)
    build('worldwide.html', HUB,
          f'Sifu Ajay travels to students in any country, including {links}. He also teaches in Santee, California (San Diego County).',
          HUB['area'])
    for s, C, _ in COUNTRIES:
        t = country_text(C)
        build(page_name(s), t,
              'Sifu Ajay travels to students <a href="worldwide.html">anywhere in the world</a>. He also teaches in Santee, California (San Diego County).',
              t['area'])

if __name__ == '__main__':
    main()
