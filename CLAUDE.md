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

## Blog and release calendar
- The blog is live at /blog. Unreleased drafts live on the `drafts/blog` branch, never on main
  (anything on main is public). The schedule is in blog-calendar.json.
- Posts in blog-calendar.json were approved by the owner, along with their release dates. On their date,
  release them straight to main. No PR is needed for these, only for new posts or changes to their content.
- Release procedure, every time:
  1. `git fetch origin drafts/blog:refs/remotes/origin/drafts/blog`
  2. `python3 tools/blog.py due` lists posts due today (Pacific time) or earlier.
  3. For each: `python3 tools/blog.py release <slug> <today's date>`. It copies the draft, sets the
     publish date, rebuilds the blog list, the "From the Blog" boxes and the sitemap, then runs QA.
  4. If QA fails, fix the problem (or skip the post and tell the owner). Never push a failing build.
  5. Commit, push, wait ~2 minutes, then fetch the live post and /blog and confirm they show the post
     with the right title. Log it in CHANGELOG.md.
  6. Ping IndexNow (Bing, Yandex and other engines; Google doesn't support it) for the new post and /blog:
     `python3 tools/blog.py indexnow <slug> blog` prints the links. Open each with WebFetch. An empty
     reply (200/202) means it was accepted. Do the same for any existing page you change substantially.
     The key file 212a9b89e41f158056d6f3102f117957.txt must stay in the site root.
     Google can't be pinged. In the owner summary, list each new URL so the owner can paste it
     into Search Console's URL Inspection and click "Request indexing" (Search Console is verified).
  7. About 7 days after a release, web-search `site:l9hkungfu.com <post slug or title>` to see whether
     Google has indexed it, and include that in the owner summary. If a post isn't indexed after
     14 days, check it for problems and tell the owner.
- Run `python3 tools/blog.py check` before any push that touches HTML; it catches broken links,
  bad JSON-LD, missing sitemap entries, and title/description lengths on blog pages.
- New posts: build from an existing post in drafts/blog (same template), keep the title under 60
  characters and the description between 70 and 160, use RELEASE_DATE as the datePublished placeholder,
  add a card to drafts/blog's blog.html, and add a link to the "From the Blog" box. Propose new posts
  and their dates to the owner as a PR against drafts/blog, and add them to the calendar once approved.
  Posts from Sifu McNeil's writings credit him as author and name the newsletter issue they first appeared in.
- Google Search Console is set up (verified via the meta tag in index.html, which must stay). The
  sitemap was submitted on 2026-10-03.
- Hsing-I Part 2 is not in the calendar on purpose: the owner is looking for it. Don't add or ask about it until he provides it.
  Parts 3 and 4 are on hold (status "on-hold" in blog-calendar.json) until Part 2 is ready; then ask the owner for new dates.
- Cadence: one post a week, on Thursdays. Don't bunch releases together; a steady cadence matters more than volume.

## School facts (confirmed by the owner)
- Location: Santee, California (San Diego County). No street address is published; do not add one.
- Classes are private and by appointment only, taught one-on-one or in small groups. There is no public class schedule.
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
