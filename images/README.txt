Drop photos here using these exact filenames — the site picks them up automatically.

  hero.jpg        Wide banner behind the title. ~2000px wide, landscape.
                  It sits at low opacity behind text, so avoid busy images.

  sifu-ajay.jpg   Portrait of Sifu Ajay. Portrait orientation, ~1000x1250px.
  training-1.jpg  Form practice. Portrait orientation, ~1000x1250px.
  training-2.jpg  Partner or weapons work. Portrait orientation, ~1000x1250px.

Notes:
- Keep each file under ~500KB so the page loads fast. Any image resizer will do this.
- .jpg only, lowercase filenames. "Hero.JPG" will not load.
- Missing files degrade gracefully: the hero falls back to its gradient and
  gallery frames show a labelled placeholder. Nothing breaks.
- To add more gallery photos, copy a <figure> block in index.html's gallery section.

── SYSTEM & LINEAGE PAGE PHOTOS (all optional) ──
Each inner page looks for one image. Missing files just fall back to the
gradient, so add them whenever you have them:

  system-little-nine-heaven.jpg    system-ba-kua.jpg
  system-hsing-i.jpg               system-taoist-lovemaking.jpg
  system-chen-tai-chi.jpg          system-taoist-meditation.jpg
  system-splashing-hands.jpg       system-shih-shui.jpg
  system-iron-hand.jpg             system-tzu-men-chuan.jpg
  lineage.jpg

sifu-ajay.jpg is reused on instructor.html, so you only need it once.
Each image appears twice on its page: as a faint hero background and in the
portrait frame. Landscape or square works; the frame crops to 3:4.

  teacher-mcneil.jpg   (optional) Portrait for Master James McNeil's page.

── SHOP PAGE ──
  shop.jpg             (optional) faint banner behind the Shop title
  shop-product-1.jpg   product photos, 4:3 landscape, ~1200x900px
  shop-product-2.jpg
  shop-product-3.jpg
Add more as shop-product-4.jpg etc. when you add product blocks.

── OPTIONAL HERO VIDEOS ──
Any hero can play a silent looping video instead of a still. Use the same
filename as the image, with .mp4:

  hero.mp4                     homepage
  system-chen-tai-chi.mp4      Chen Tai-Chi page
  system-hsing-i.mp4           ...and so on for every system page
  teacher-mcneil.mp4, lineage.mp4, shop.mp4

Rules:
- Keep each file under ~3MB. These autoplay, so weight matters.
- No audio track. Mobile browsers block autoplay on anything with sound.
- 1080p is plenty; the hero sits at low opacity behind the title text.
- The matching .jpg still acts as the fallback, so keep it in place.
- Visitors who set "reduce motion" in their OS see the still instead.
