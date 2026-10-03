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

## What the agent may change on its own (commit straight to main)
Text and SEO only: copy edits, new or expanded written content, new blog/article pages
that reuse an existing page's template unchanged, titles, meta descriptions, headings, alt text,
structured data (JSON-LD), canonical tags, sitemap.xml, robots.txt, fixing broken links and typos.

## What needs the owner's approval first (open a pull request, never push to main)
Anything visual: layout, CSS/styles, colors, fonts, images or video, adding/removing/reordering
menu items or homepage sections/cards, new page templates or design elements.
Put these on a branch named `proposal/<short-name>`, open a PR describing the change in plain
language, and wait. The owner approves by merging.

## Never
- Invent facts: class times, locations, prices, credentials, lineage claims or testimonials.
  If content needs a fact you don't have, list it as a question for the owner.
- Delete pages or remove the contact form.
- Touch littlenineheaven.com links' destinations.

## Log
Append each run's changes to CHANGELOG.md (date, what changed, why).
