#!/usr/bin/env python3
"""Build blog-post drafts from Sifu McNeil's newsletters, in the existing post template.

  python3 tools/make_post.py SPEC.json [SPEC.json ...] --out DIR

Run it from a checkout of the drafts/blog branch (or point --template at a post file). Each SPEC is a JSON
object (or a list of them):

  {
    "slug": "blog-shih-shui-kung-explained",          # file name without .html; must start with blog-
    "title": "Shih Shui Kung: Bone Marrow Washing",    # <title> and h2; keep under 60 characters
    "h1": "Shih Shui Kung",                             # big hero heading (short)
    "subtitle": "Bone marrow washing, explained",      # line under the h1
    "description": "70-160 characters for Google",
    "month": "September 2014",                          # newsletter month, shown as "Blog · September 2014"
    "issue": "L9H Internal Kung-Fu newsletter, September 2014 (Volume 7, Issue 9)",
    "series": "Optional series name · Part 2",          # optional
    "image": "images/system-shih-shui.jpg",             # optional hero photo (default system-hsing-i.jpg)
    "image_alt": "Shih Shui practice",
    "caption": "Shih Shui Kung",                        # caption under the side photo
    "card_meta": "September 2014 · Shih Shui",          # line above the title on the blog index card
    "card_summary": "One or two sentences for the blog index card.",
    "short": "Shih Shui Kung: Bone Marrow Washing",     # label in the "From the Blog" box
    "body": "<h3>...</h3><p>...</p>"                    # article HTML: h3, p, ul/ol/li, blockquote, em, strong, a
  }

Writes DIR/<slug>.html, plus DIR/cards.html (blog index cards) and DIR/shorts.json (box labels) to merge into
drafts/blog's blog.html and the Part 1 post's "From the Blog" grid (tools/blog.py reads labels from there).
datePublished stays RELEASE_DATE; tools/blog.py release fills it in and adds the current menu, i18n and social tags.
"""
import json, re, sys, os, html, argparse

AUTHOR_NOTE = ('<p><em>Adapted for the web from Sifu James W. McNeil\'s newsletter, lightly edited. Sifu McNeil is the '
               'Gate Keeper of the Little Nine Heaven Wu Tao System and the teacher of Sifu Ajay Kumra, who teaches '
               'privately in Santee, California.</em></p>')

def esc(s): return html.escape(s, quote=True)

def build(t, p):
    need = ['slug', 'title', 'h1', 'description', 'month', 'issue', 'body', 'card_summary']
    miss = [k for k in need if not p.get(k)]
    if miss: raise SystemExit(f"{p.get('slug','?')}: missing {miss}")
    if not p['slug'].startswith('blog-'): raise SystemExit(f"{p['slug']}: slug must start with blog-")
    if len(p['title']) > 60: print(f"warning: {p['slug']}: title is {len(p['title'])} chars (>60)", file=sys.stderr)
    if not 70 <= len(p['description']) <= 160: print(f"warning: {p['slug']}: description is {len(p['description'])} chars", file=sys.stderr)
    url = f"https://l9hkungfu.com/{p['slug']}"
    img = p.get('image', 'images/system-hsing-i.jpg'); alt = p.get('image_alt', 'Little Nine Heaven practice')
    s = t
    s = re.sub(r'<title>.*?</title>', f"<title>{esc(p['title'])} | L9H SoCal</title>", s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(p['description']), s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(p['title']) + ' | Little Nine Heaven SoCal', s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + esc(p['description']), s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    # drop any social image tags copied from the template; blog.py release adds the right ones
    s = re.sub(r'\n\s*<meta (property="og:image[^"]*"|name="twitter:(card|image)")[^>]*>', '', s)
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p['title'],
          "description": p['description'], "datePublished": "RELEASE_DATE", "dateModified": "RELEASE_DATE",
          "author": {"@type": "Person", "name": "James W. McNeil", "jobTitle": "Gate Keeper, Little Nine Heaven Wu Tao System",
                     "url": "https://l9hkungfu.com/teacher-mcneil"},
          "publisher": {"@type": "MartialArtsSchool", "name": "Little Nine Heaven SoCal", "url": "https://l9hkungfu.com"},
          "mainEntityOfPage": url,
          "isPartOf": {"@type": "Blog", "name": "Little Nine Heaven SoCal Blog", "url": "https://l9hkungfu.com/blog"},
          "isBasedOn": p['issue']}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>',
               '<script type="application/ld+json">\n' + json.dumps(ld, indent=2, ensure_ascii=False) + '\n  </script>', s, count=1, flags=re.S)
    # hero
    s = re.sub(r'(<img class="page-hero-photo" src=")[^"]*(" alt=")[^"]*', lambda m: m.group(1) + img + m.group(2) + esc(alt), s, count=1)
    s = re.sub(r'(<source src=")images/[^"]*\.mp4', lambda m: m.group(1) + img.rsplit('.', 1)[0] + '.mp4', s, count=1)
    s = re.sub(r'(<div class="page-hero-content">\s*<p class="eyebrow">)[^<]*', lambda m: m.group(1) + 'Blog · ' + esc(p['month']), s, count=1)
    s = re.sub(r'(<div class="page-hero-content">.*?<h1>)[^<]*(</h1>)', lambda m: m.group(1) + esc(p['h1']) + m.group(2), s, count=1, flags=re.S)
    if p.get('subtitle'):
        s = re.sub(r'(<div class="page-hero-content">.*?<p class="subtitle">)[^<]*', lambda m: m.group(1) + esc(p['subtitle']), s, count=1, flags=re.S)
    else:
        s = re.sub(r'\n\s*<p class="subtitle">[^<]*</p>', '', s, count=1)
    # side photo + caption
    s = re.sub(r'(<div class="portrait-frame">\s*<img src=")[^"]*(" alt=")[^"]*', lambda m: m.group(1) + img + m.group(2) + esc(alt), s, count=1)
    cap = p.get('caption', p['h1'])
    s = re.sub(r'(<div class="portrait-caption">\s*<strong>)[^<]*', lambda m: m.group(1) + esc(cap), s, count=1)
    # article: label, h2, facts, author note, body
    a = s.index('<div class="bio-content reveal">'); b = s.index('</div>\n    </div>\n  </section>', a)
    facts = [('Author', 'Sifu James W. McNeil'), ('First published', p['issue'])]
    if p.get('series'): facts.append(('Series', p['series']))
    facts_html = ''.join(f'<div class="fact"><div class="dot"></div><strong>{k}</strong><span>{esc(v)}</span></div>' for k, v in facts)
    article = ('<div class="bio-content reveal">\n'
               f'        <p class="section-label">Blog · {esc(p["month"])}</p>\n'
               f'        <h2>{esc(p["title"])}</h2>\n'
               '        <div class="gold-line"></div>\n'
               f'        <div class="facts-grid">{facts_html}</div>\n'
               f'        {AUTHOR_NOTE}\n\n'
               + '\n'.join('        ' + line for line in p['body'].strip().split('\n')) + '\n      ')
    s = s[:a] + article + s[b:]
    s = re.sub(r'<body data-slug="[^"]*"', f'<body data-slug="{p["slug"]}"', s, count=1)
    card = (f'\n          <a class="post-card" href="{p["slug"]}.html">\n'
            f'            <p class="post-meta">{esc(p.get("card_meta", p["month"]))}</p>\n'
            f'            <h3>{esc(p["title"])}</h3>\n'
            f'            <p>{esc(p["card_summary"])}</p>\n'
            '            <span class="post-more">Read the post →</span>\n'
            '          </a>')
    return s, card

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('specs', nargs='+'); ap.add_argument('--out', required=True)
    ap.add_argument('--template', default='blog-hsing-i-part-3-body-power-and-touch-go-kiss.html')
    a = ap.parse_args()
    t = open(a.template, encoding='utf-8').read()
    os.makedirs(a.out, exist_ok=True)
    cards, shorts = [], {}
    for f in a.specs:
        data = json.load(open(f, encoding='utf-8'))
        for p in (data if isinstance(data, list) else [data]):
            s, card = build(t, p)
            open(os.path.join(a.out, p['slug'] + '.html'), 'w', encoding='utf-8').write(s)
            cards.append(card); shorts[p['slug']] = p.get('short', p['title'])
            print('built', p['slug'])
    open(os.path.join(a.out, 'cards.html'), 'w', encoding='utf-8').write(''.join(cards))
    json.dump(shorts, open(os.path.join(a.out, 'shorts.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

if __name__ == '__main__': main()
