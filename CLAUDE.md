# Little Nine Heaven SoCal website: agent rules

Static HTML site for l9hkungfu.com (Sifu Ajay Kumra, internal kung-fu in Southern California).
Pushing to `main` publishes the live site automatically. There is no build step.

## Site conventions
- Live URLs use the bare domain with no `.html`: `https://l9hkungfu.com/system-hsing-i`.
  Canonical tags, og:url, schema URLs and sitemap.xml must use this form. Never use `www.`.
- Internal links in the HTML stay as relative `page.html` links (the host rewrites them).
- The whole site is translated into 10 languages (zh, es, fr, de, pt, ru, ja, th, ar, hi) by i18n.js,
  which every page loads before </head> (`<script src="i18n.js"></script>`; tools/blog.py check enforces it).
  Translations live in lang/<code>.json: "strings" (plain text, titles, placeholders, alt text) and "html"
  (text blocks containing links/em/strong, keyed by their innerHTML; a translation must keep the same tags in
  the same order). Keys are the exact English text with whitespace collapsed, so changing English text breaks
  its translation until the new text is translated.
  After changing or adding English text (including a newly released blog post), run
  `python3 tools/i18n_missing.py --out /tmp/missing.json`, translate everything listed into all 10 languages,
  and add it to every lang/*.json. Names and words that read the same (Little Nine Heaven, Blog) can stay.
  Untranslated text just shows in English, so it's never a blocker, but don't leave real sentences untranslated.
  The chosen language is remembered (localStorage) and carried on links as ?lang=xx. Arabic is right-to-left.
- Teacher name spellings: Chiao Chang-Hung, Pan Wing-Chow, Hsu Hong-Chi, Haumea Lefiti,
  Chin Cheng-Yen, James McNeil, Ajay Kumra.
- When you add or remove a page, update sitemap.xml (thank-you.html stays out: it is noindex).
- If mobile.css exists in the repo, every page must link it just before </head>:
  `<link rel="stylesheet" href="mobile.css" />` (add it to any page that is missing it).
- Photos: pages reference files in images/ (see images/README.txt). Tags for files that don't exist yet
  use `data-pending-src` instead of `src`, so missing photos don't cause 404s. After adding photos,
  run `python3 tools/blog.py photos` to switch the matching tags back to `src`. Adding photos is a
  visual change, so send it as a proposal PR (resize to under ~300KB first and write descriptive alt text).
- _headers holds the security headers (Netlify). Don't remove it.
- Writings by Sifu James W. McNeil (the owner's teacher) may be adapted into articles with credit to him.
  Articles drawn from his writings count as history/lineage content: always send them as a proposal PR.
  On 2026-10-17 the owner confirmed he has his teacher's explicit permission to use ALL of Master McNeil's
  material, including in paid offerings (courses, a Skool community, books). Keep crediting McNeil.

## Weekly publishing (important: read first)
- The site is on Netlify's Free plan: 300 credits a month, 15 per production deploy, plus credits for
  bandwidth. If credits run out completely, Netlify takes the whole site offline until the billing
  cycle resets. In October 2026 deploys were paused after about 23 deploys; the billing cycle runs from
  the 25th to the 24th, and deploys resume on Oct 25.
- The owner chose to save up changes and publish ONCE A WEEK. Every push to `main` is a production deploy,
  so treat `main` as "what's live" and do all work on the `staging` branch:
  - Every run: `git checkout staging` (create it from origin/staging), make changes there, run QA,
    commit and push `staging`. Pushing `staging` does not deploy.
  - Proposal PRs (visual or history/lineage changes) target `staging`, not main. When the owner merges
    one, it goes live with the next weekly publish.
  - Weekly publish: on Thursday runs only, starting Thursday 2026-10-29. First release any blog posts due
    that day on staging (blog procedure below). Then check the live site reflects the last publish. Then
    merge staging into main (`git checkout main && git merge --no-edit staging`), run QA, and push main
    once. Confirm the live site updated, then do the IndexNow pings. That is the only push to main all week.
  - One-time exception approved by the owner on 2026-10-16: a publish on Sunday 2026-10-25 (the day deploys
    resume), done by a separate one-time scheduled run, so the fixed sitemap and SEO work reach Google sooner.
    The Thursday 2026-10-29 publish still happens as normal (it releases that day's blog post); that week has
    two deploys (30 of 300 credits). From then on, back to once a week on Thursdays.
  - Never push to main on any other day, and never more than once a week, unless the owner explicitly asks.
  - If a weekly publish doesn't go live within about 10 minutes, deploys are paused: tell the owner and
    don't push again.
- netlify.toml has NO ignore rule: every push to main is a real production deploy (15 credits). An ignore
  rule made Netlify cancel the Oct 25 and Oct 29 publishes; don't add one back. Keep main pushes to the weekly publish.
  After each publish, confirm the live site changed; if the agent can't fetch the site, ask the owner to check
  Netlify's Deploys tab (a "Canceled" or "Skipped" deploy means it did not go live).
- In the owner summary, say what's waiting on staging and when it will go live.
- Credits report (owner request, 2026-10-30): after anything that uses Netlify credits (every push to main), tell the
  owner how many credits are left until the billing cycle resets on the 25th. Keep the running count in
  tools/netlify-credits.md: 300 per cycle, minus 15 per production deploy that actually ran (Canceled or Skipped
  deploys don't count), minus a small amount for bandwidth that only Netlify's Usage page shows, so label it an
  estimate and ask the owner for the real figure from Netlify (Team > Usage & billing) when it matters.

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
  5. Commit on staging. The post goes live with the weekly publish that same Thursday; after that
     publish, fetch the live post and /blog and confirm they show it with the right title. Log it in CHANGELOG.md.
  6. Ping IndexNow (Bing, Yandex and other engines; Google doesn't support it) for the new post and /blog:
     `python3 tools/blog.py indexnow <slug> blog` prints the links. Open each with WebFetch. An empty
     reply (200/202) means it was accepted. Do the same for any existing page you change substantially.
     The key file 212a9b89e41f158056d6f3102f117957.txt must stay in the site root.
     Google can't be pinged. In the owner summary, list each new URL so the owner can paste it
     into Search Console's URL Inspection and click "Request indexing" (Search Console is verified).
     Also add each new or substantially changed URL to tools/indexing-queue.md: a daily scheduled task reminds the
     owner and submits the queue through his signed-in browser (about 10 a day).
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
- Owner rule (2026-10-30): before ANY post goes on the calendar, show the owner the exact final text of that post
  (title, description and full body as it will read) and get his approval for that post individually. Never
  schedule a post he hasn't read and approved. Send drafts in small batches for review; record each approval
  (date, and any edits he asked for) in the post's calendar entry.
- Google Search Console is set up (verified via the meta tag in index.html, which must stay). The
  sitemap was submitted on 2026-10-03.
- Hsing-I Part 2 is not in the calendar on purpose: the owner is looking for it. Don't add or ask about it until he provides it.
  Parts 3 and 4 are on hold (status "on-hold" in blog-calendar.json) until Part 2 is ready; then ask the owner for new dates.
- Cadence: one post a week, on Thursdays (the weekly publish day). Don't bunch releases together; a steady cadence matters more than volume.

## School facts (confirmed by the owner)
- Location: Santee, California (San Diego County). No street address is published; do not add one.
- Classes are private and by appointment only, taught one-on-one or in small groups. There is no public class schedule.
- The first class is a free introductory class.
- PRIVATE, DO NOT PUBLISH: the owner holds a lineage title (confirmed 2026-10-17) but does NOT want it publicly
  advertised. Never add it, or any generation-number reference to him, to the website, blog, structured data,
  social posts, Skool or any other public content, and don't suggest adding it. Only the owner can lift this.

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
- Append each run's changes to CHANGELOG.md (date, what changed, why).
- ALSO keep the owner's update log, tools/update-log.csv, current. It's his running spreadsheet
  (GitHub shows it as a table: https://github.com/siful9h2/l9h/blob/staging/tools/update-log.csv).
  Columns: ID, Update, Category, Pages affected, Approved by, Date developed, Date live, Status, Notes.
  - Add one row per meaningful update when it's developed, written in plain language for the owner
    (not commit messages). Dates are YYYY-MM-DD, Pacific time.
  - Status values: Live, Waiting for weekly publish, Scheduled (blog posts with a date), Proposal
    (waiting for owner approval, with the PR link in Notes), On hold, Removed.
  - At each weekly publish, once the live site shows the changes, fill in "Date live" and set
    Status to Live for every row that went out. When a proposal is approved or declined, update its row.
  - `python3 tools/update_log_xlsx.py out.xlsx` builds a formatted Excel copy if the owner wants one.
