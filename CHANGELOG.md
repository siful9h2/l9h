# Website changelog

## 2026-10-03
- Canonical, og:url and schema URLs now use the live address (https://l9hkungfu.com/page) instead of www + .html, so Google gets one consistent address per page.
- Fixed Sifu Chin Cheng-Yen's name on the homepage lineage section and the instructor page (was "Chin Chen-Yen" / "Ching Chen-Yen").
- Added sitemap.xml listing all 22 public pages and robots.txt pointing to it.
- Added CLAUDE.md with the rules the weekly website agent follows.

## 2026-10-03 (later)
- Homepage now says where and how classes happen: private instruction in Santee, CA (San Diego County), by appointment, with a free first class. Added in all 11 languages.
- Homepage title, description, social preview text and search markup updated to name Santee and the free intro class.
- Agent rules: history and lineage content now needs the owner's approval; added confirmed school facts.

## 2026-10-03 (blog launch)
- Launched the blog (/blog) with post #1: "The Devastating Style of Hsing-I, Part 1: Origins and the Eight Fundamentals" by Sifu James W. McNeil (from his September 2015 newsletter).
- Corrected the Yue Fei dates in that post to Yue Fei (1103-1142), Sung dynasty (960-1279), as the owner asked.
- "Blog" added to the menu on every page (translated on the homepage); the Hsing-I page links to the series.
- Added blog-calendar.json (release schedule) and tools/blog.py (release + QA checks). Remaining posts are scheduled weekly on Thursdays.

## 2026-10-03 (mobile)
- Owner approved the mobile proposal: phones now get a tap-to-open menu and a light parchment reading theme (desktop unchanged). Files: mobile.css, mobile-menu.js, linked from every page.

## 2026-10-03 (SEO run)
- No blog post due (next: Hsing-I Part 3 on Thu Oct 8).
- All 11 system pages and the instructor page now name Santee, CA (San Diego County) in their titles, search descriptions and social previews, using the spellings people search for (Tai Chi, Xing Yi Quan, Baguazhang, Qigong). Why: these pages only said "Southern California", and local searches use the town/county.
- Added search markup (Course for each system page, Person for the instructor page) linking them to the Santee school.
- Each system page's closing "Begin Your Path" box now says classes are in Santee, by appointment, with a free first class; instructor page labels say Santee instead of Southern California.
- Question for owner: Hsing-I, Ba Kua and instructor pages mention "small classes/small groups"; confirmed facts say classes are private. Left as is pending an answer.
- Owner answers: classes are one-on-one or small groups (so the "small classes/groups" wording stays; recorded in CLAUDE.md). Hsing-I Part 2 is on hold until the owner finds it (noted in CLAUDE.md).
- Added Google Search Console verification tag to the homepage.

## 2026-10-04
- Owner asked to hold the Hsing-I series until Part 2 is found: Parts 3 and 4 (were Oct 8 and Oct 15) are now on hold in blog-calendar.json. Taiwan & Thailand trip post stays on Oct 22.
- Owner moved the Taiwan & Thailand trip post from Oct 22 to Thu Oct 8 to fill the gap.
- Set up IndexNow (key file in site root) so new and changed pages can be submitted to Bing and other engines; added the ping step to the release procedure.
- Owner request: "Sifu Chin Cheng-Yen" is now "Master Chin Cheng-Yen" everywhere (his page, the Tzu Men Chuan page, all menus and teacher lists, and all 10 homepage translations), matching the other masters.
- Proposed a new blog post for the owner to read: "Why the Internal Arts Must Be Taught in Person" (PR #4 against drafts/blog). It is not scheduled until he approves it and picks a date.
- Fixed: "Send Inquiry" and red "Begin Your Path" buttons had dark text on phones; now white.
- Owner approved post #4, "Why the Internal Arts Must Be Taught in Person"; merged into drafts and scheduled for Thu Oct 15.
- Owner approved: light parchment reading theme now applies on desktop too (same as phones).
- Speed: added preconnect hints for Google Fonts on every page (PageSpeed mobile score was 88; first paint 3.1s).
- PageSpeed fixes: missing photos no longer requested (no more 404 console errors), higher contrast on the homepage quote credit, security headers added (_headers), new tools/blog.py photos command.
- Netlify production deploys appear paused (Free plan credit limit, about 20 deploys a month; ~23 pushed since Oct 3). The preconnect and PageSpeed fixes are on GitHub but not live yet. Added netlify.toml so pushes that only touch notes or tools are not deployed, plus a one-push-per-run rule.
- Owner chose to wait for the Netlify reset (Oct 25) and publish once a week from now on. New staging branch holds all changes; weekly publish on Thursdays starting Oct 29. Blog posts moved: Taiwan & Thailand trip to Oct 29, "Why the Internal Arts Must Be Taught in Person" to Nov 5.
- Owner request: removed the Taiwan & Thailand trip post from the calendar (draft kept unpublished on drafts/blog); "Why the Internal Arts Must Be Taught in Person" moved up to Thu Oct 29.
- Started the owner's running update log (tools/update-log.csv, plus an Excel export script) with every update since Oct 3.
- Owner approved homepage banner (Lo Shu grid, option C): images/hero.jpg added, shown at 60% opacity in full colour; alt text updated. Goes live with the Oct 29 publish.
- Owner-provided candid photo of Ajay training with Master McNeil: cropped, black-and-white with warm tone, added with caption under "Study Under Master McNeil" on the instructor page. Goes live Oct 29.

## 2026-10-05 (Monday SEO run, on staging)
- Homepage: shorter Google title and description (were 73 and 207 characters, so Google cut them off); now name kung-fu and tai chi classes in Santee within the visible length. Title/description only; page text and translations unchanged.
- Six teacher pages: each had the same generic Google description; now each has its own title and description built only from facts already on that page (systems taught, years, who they taught), plus social-sharing preview tags. Lineage page title now says "Little Nine Heaven Kung-Fu Lineage". No historical claims changed.
- No blog post due (next: "Why the Internal Arts Must Be Taught in Person", Thu Oct 29). Site not yet showing in web search results for site:l9hkungfu.com.
- Questions for owner: shop page shows placeholder products; Hsu page dates (trained 1977-1984 vs. died 1983).

## 2026-10-07 (whole-site translation)
- Every page can now be read in all 10 languages, not just the homepage: Chinese, Spanish, French, German, Portuguese, Russian, Japanese, Thai, Arabic (right-to-left) and Hindi. The owner asked for this.
- The language picker is on every page's menu. The chosen language is remembered and carried on every link (?lang=xx), so a visitor who picks a language stays in it as they browse.
- Moved the homepage translations out of index.html into shared files (i18n.js + lang/*.json). index.html is about 130KB lighter, which helps load speed.
- Language picker and per-language font styles moved from the homepage into mobile.css so every page shares them.
- tools/blog.py now adds the translation script to released posts and checks every page has it; new tools/i18n_missing.py lists text that still needs translating.

## 2026-10-08 (Thursday SEO run, on staging; no publish until Oct 29)
- Added breadcrumb search markup (Home > page, Home > Lineage > teacher, Home > Blog > post) to 22 pages, so Google can show a clean page trail in results and understand how pages fit together. Markup only; nothing visible changes.
- Homepage contact section label now says "Santee, California" instead of "Southern California" (local search signal); added the translation in all 10 languages. The lineage and McNeil pages keep "Southern California" (history content).
- Proposal PR #6 (against staging): homepage FAQ section with FAQ search markup, built only from confirmed facts, in all 11 languages.
- Search check: site:l9hkungfu.com still returns no results in web search. Local searches for "tai chi Santee" are dominated by the City of Santee's senior tai chi listings.
- No blog post due (next: "Why the Internal Arts Must Be Taught in Person", Thu Oct 29). The live-site check couldn't be done this run (page fetch permission timed out); no main push was needed.

## 2026-10-12 (Monday SEO run, on staging; no publish until Oct 29)
- Every public page now has a social-share preview image (og:image + twitter:image), so shared links show a picture. Uses images already on the site: the homepage banner by default; Hsing-I, Chen Tai-Chi, blog and instructor pages use their own photos. tools/blog.py now adds these tags to released posts and QA flags pages without one.
- Homepage school markup: added an @id, image and founder (Sifu Ajay Kumra), linked each course to its page, and added the three systems that were missing (Chi-Kung, Shih Shui, Tzu Men Chuan). System pages and the instructor page now point to the same school/person @ids so Google ties them together. Markup only.
- Shop page set to noindex and removed from sitemap.xml while it still shows placeholder products ("Product Name", "$00"); thin placeholder pages can drag down how Google rates a small site. Page and menu link unchanged. Switch back once real products are listed.
- Index check: site:l9hkungfu.com searches still return nothing, including Hsing-I Part 1 (released Oct 3, 9 days ago). Page has index,follow, a correct canonical and is in the sitemap; owner asked to check Search Console's Pages report and request indexing.
- No blog post due (next: "Why the Internal Arts Must Be Taught in Person", Thu Oct 29). Live-site fetch not possible this run (fetch permission timed out); no main push needed.

## 2026-10-15 (Thursday SEO run, on staging; no publish until Oct 29)
- Five system pages now link the teacher they name to that teacher's page, inside the existing sentence (Chen Tai-Chi → Master Pan Wing-Chow, Hsing-I → Master Hsu Hong-Chi, Little Nine Heaven and Shih Shui → Grandmaster Chiao Chang-Hung, Tzu Men Chuan → Master Chin Cheng-Yen). Wording unchanged; links help Google connect each art to its lineage and help visitors explore. Linked versions of the five paragraphs added to all 10 language files.
- sitemap.xml "last modified" dates updated to when each page actually last changed (were all Oct 3), so Google knows which pages to re-crawl after the Oct 29 publish.
- Search check: site:l9hkungfu.com still returns nothing in web search. Live-site fetch not possible this run (network permission); no main push needed.
- No blog post due (next: "Why the Internal Arts Must Be Taught in Person", Thu Oct 29).

## 2026-10-16 (owner request, on staging)
- Master Hsu Hong-Chi's page: year of death changed from 1983 to 1984, as the owner confirmed (matches McNeil studying with him 1977-1984). Updated in all 10 language files.
- Noted for owner: the same sentence says Grandmaster Chiao accepted McNeil "after" Master Hsu's death, while other pages say McNeil trained with Chiao from 1983. Left unchanged pending his answer.
- Owner then decided to keep 1983 for Master Hsu's death (and 1983 for McNeil starting with Grandmaster Chiao, "after which" wording kept). Hsu page and translations restored to 1983; nothing about this goes out on Oct 29.
- Owner request: Master Hsu's page now says McNeil studied with him 1977-1983 (was 1977-1984), matching Master Hsu's death in 1983. Fact box and paragraph, all 10 language files.
- Owner approved PR #6: homepage FAQ section (6 questions, FAQ search markup, all 11 languages) merged into staging. Goes live with the Oct 29 publish.
- Owner request: added a 7th FAQ question, "Can I learn Shih Shui Gong (Bone Marrow Washing)?", noting it is taught only privately (plus FAQ search markup and all 10 translations). Other details come from the Shih Shui page.

## 2026-10-16 (owner request: earlier publish)
- Owner approved publishing on Sunday Oct 25, the day Netlify deploys resume, instead of waiting until Thursday Oct 29. The live site still has the Oct 4 version, whose sitemap is missing /blog and the Hsing-I Part 1 post. A one-time scheduled run will do this publish. The regular Thursday Oct 29 publish still goes ahead with that day's blog post.

## 2026-10-19 (Monday SEO run, on staging; next publish Sun Oct 25)
- Found that the Chi-Kung (Qigong) page is orphaned: no page links to it (it is missing from the Systems menu, the systems list at the bottom of each system page and the homepage cards), so Google and visitors can barely reach it, even though "qigong" is one of the main local searches.
- Text/SEO fix on staging: the Shih Shui page's existing word "chi-kung" now links to the Chi-Kung page, and the Chi-Kung page's mention of Hsing-I links to the Hsing-I page. Wording unchanged; linked versions added to all 10 language files. Added the missing "Chi-Kung" label translation (ja, zh, ru, ar, hi, th). Sitemap dates for both pages updated.
- Proposal PR #7 (against staging): add Chi-Kung to the Systems menu on every page, to the systems list on system pages, as an 11th homepage card, and link it from the homepage FAQ answer.
- update-log.csv: rows waiting for publish now say they go live Sun Oct 25 (the approved early publish), not Thu Oct 29.
- Index check (Monday): site:l9hkungfu.com still returns nothing in web search, including Hsing-I Part 1 (released Oct 3, 16 days ago). Checked the post: index,follow, correct canonical, in the sitemap on main. Most likely cause: the live site is still the Oct 4 version and its sitemap/links reach Google only after the Oct 25 publish. Owner told.
- No blog post due (next: "Why the Internal Arts Must Be Taught in Person", Thu Oct 29). Live-site fetch not possible this run (fetch permission timed out); no main push.

## 2026-10-22 (Thursday SEO run, on staging; next publish Sun Oct 25)
- All 11 system pages: the main section heading (an H2 that repeated the page's H1 word for word) now names the art plus "in Santee", e.g. "Ba Kua Chang in Santee", "Chen Tai-Chi in Santee"; the Chi-Kung page's says "Chi-Kung (Qigong) in Santee", the spelling most people search. Why: duplicate headings carried no extra signal, and local searches pair the art with the town. Translations added for all 10 languages; sitemap dates for the 11 pages updated.
- Dry-ran next Thursday's release ("Why the Internal Arts Must Be Taught in Person", Oct 29) in a scratch copy: it releases cleanly and QA passes. Nothing committed for it.
- To do at the Oct 29 release: the blog page's description, social preview and "Writings · Sifu James W. McNeil" eyebrow say all posts are by Sifu McNeil, but the Oct 29 post is by Sifu Ajay Kumra. Update that wording (and its translations) in the same publish, without changing what it says about Sifu McNeil.
- Search check: site:l9hkungfu.com still returns nothing; the Oct 25 publish (sitemap with /blog and the Hsing-I post) is the next step for indexing. Live-site fetch blocked from this run's network; no main push (not a publish day).

## 2026-10-25 (one-time owner-approved Sunday publish)
- QA passed on staging; merged staging into main (fast-forward to f032a33) and pushed main once at 17:08 UTC. This publishes everything saved up since Oct 4: full site in 10 languages, homepage FAQ (7 questions), sitemap with /blog and the Hsing-I Part 1 post, social preview images, better Google titles/descriptions, breadcrumb and school markup, Chi-Kung links, "in Santee" headings, Master Hsu date fix, banner and instructor photos, speed and security fixes.
- No blog post released (next: "Why the Internal Arts Must Be Taught in Person", Thu Oct 29).
- Live-site check NOT possible: this run's page fetches (sitemap.xml, homepage) were blocked by an unanswered fetch permission, so the deploy could not be confirmed and IndexNow pings could not be sent. update-log.csv rows left as "Waiting for weekly publish" until a run confirms the live site; owner asked to check. Main was not pushed again.

## 2026-10-26 (Monday SEO run, on staging; next publish Thu Oct 29)
- Blog page prepared for Thursday's post by Sifu Ajay Kumra (the first post not by Sifu McNeil): eyebrow now "Writings · Sifu James W. McNeil & Sifu Ajay Kumra", subtitle "Hsing-I, Tai-Chi, Ba Kua and the Internal Arts" (was "From the Little Nine Heaven Newsletter"), intro says many posts are adapted from Sifu McNeil's newsletters and others are by Sifu Ajay Kumra (the sentence about Sifu McNeil unchanged). Meta/og description, Blog JSON-LD description and title ("Internal Kung-Fu & Tai Chi Blog | Little Nine Heaven SoCal") updated. All 10 translations added. Dry-ran Thursday's release in a scratch copy: QA passes. If the Oct 29 post has to be skipped, revert this wording before publishing.
- Homepage meta description: adds the searched spellings "Xing Yi" and "Qigong" (152 chars). Sitemap dates for / and /blog updated.
- Live-site check of the Oct 25 publish still not possible (page fetches blocked from this run's network). Must be confirmed before Thursday's main push.
- Index check (Monday): site:l9hkungfu.com still returns no results in web search, including Hsing-I Part 1 (released Oct 3, 23 days ago; reached the live sitemap only with the Oct 25 publish). Owner asked to check Search Console.
- No blog post due today (next: "Why the Internal Arts Must Be Taught in Person", Thu Oct 29). PR #7 (Chi-Kung in menu/homepage) still open.

## 2026-10-29 (Thursday weekly publish)
- Released the scheduled blog post "Why the Internal Arts Must Be Taught in Person" (Sifu Ajay Kumra) on staging with tools/blog.py (blog list, "From the Blog" boxes, sitemap rebuilt; QA passed). Post body was already translated; added the blog-card label and summary in all 10 languages.
- Live-site check of the Oct 25 publish still not possible from this run (page fetches blocked: curl gets a proxy 403, WebFetch permission timed out).
