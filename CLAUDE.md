# Little Nine Heaven SoCal website: agent rules

Static HTML site for l9hkungfu.com (Sifu Ajay Kumra, internal kung-fu in Southern California).
Pushing to `main` publishes the live site automatically. There is no build step.

## Site conventions
- Live URLs use the bare domain with no `.html`: `https://l9hkungfu.com/system-hsing-i`.
  Canonical tags, og:url, schema URLs and sitemap.xml must use this form. Never use `www.`.
- Internal links in the HTML stay as relative `page.html` links (the host rewrites them).
- index.html has an in-page translation system: dictionaries keyed by the exact English text.
  If you change English text that has a translation key, update the key in every language block
  (and the translation itself) so the switcher keeps working.
- Teacher name spellings: Chiao Chang-Hung, Pan Wing-Chow, Hsu Hong-Chi, Haumea Lefiti,
  Chin Cheng-Yen, James McNeil, Ajay Kumra.
- When you add or remove a page, update sitemap.xml (thank-you.html stays out: it is noindex).
- If mobile.css exists in the repo, every page must link it just before </head>:
  `<link rel="stylesheet" href="mobile.css" />` (add it to any page that is missing it).
- Writings by Sifu James W. McNeil (the owner's teacher) may be adapted into articles with credit to him.
  Articles drawn from his writings count as history/lineage content: always send them as a proposal PR.

## Blog (once blog.html exists on main)
- Posts are flat files named `blog-<short-slug>.html`, built from an existing post as the template.
- Each post needs: BlogPosting JSON-LD (author, datePublished), a card at the top of the list in blog.html,
  a link in the "From the Blog" box on every post, an entry in sitemap.xml, and the mobile.css /
  mobile-menu.js lines in <head>.
- Posts from Sifu McNeil's newsletters credit him as author and name the issue they first appeared in.
  They are history/lineage content: always send new ones as a proposal PR.

## School facts (confirmed by the owner)
- Location: Santee, California (San Diego County). No street address is published; do not add one.
- Classes are private and by appointment only. There is no public class schedule.
- The first class is a free introductory class.

## What the agent may change on its own (commit straight to main)
Text and SEO only (except history and lineage, see below): copy edits, new or expanded written content, new blog/article pages
that reuse an existing page's template unchanged, titles, meta descriptions, headings, alt text,
structured data (JSON-LD), canonical tags, sitemap.xml, robots.txt, fixing broken links and typos.

## What needs the owner's approval first (open a pull request, never push to main)
Anything visual: layout, CSS/styles, colors, fonts, images or video, adding/removing/reordering
menu items or homepage sections/cards, new page templates or design elements.
Also any content about history or lineage, even text-only: the lineage page, the teacher-*.html pages,
the instructor page's training background, the homepage "Living Tradition" and "Lineage" sections,
origin dates and history passages on the system pages, and any new article about history or lineage.
Pure SEO tags on those pages (title, meta description, canonical, JSON-LD) and obvious typo fixes
may still go straight to main, as long as they don't change any historical or lineage claim.
Put these on a branch named `proposal/<short-name>`, open a PR describing the change in plain
language, and wait. The owner approves by merging.

## Never
- Invent facts: class times, locations, prices, credentials, lineage claims or testimonials.
  If content needs a fact you don't have, list it as a question for the owner.
- Delete pages or remove the contact form.
- Touch littlenineheaven.com links' destinations.

## Log
Append each run's changes to CHANGELOG.md (date, what changed, why).
