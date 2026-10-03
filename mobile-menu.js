/* Tap-to-open menu for phones. Uses each page's existing menu; no markup changes needed. */
(function () {
  var nav = document.querySelector('nav');
  var list = nav && nav.querySelector('.nav-links');
  if (!list) return;
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'menu-toggle';
  btn.setAttribute('aria-label', 'Open menu');
  btn.setAttribute('aria-expanded', 'false');
  btn.innerHTML = '<span></span><span></span><span></span>';
  nav.appendChild(btn);
  function setOpen(open) {
    nav.classList.toggle('menu-open', open);
    document.body.classList.toggle('menu-lock', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (open) list.style.top = nav.getBoundingClientRect().bottom + 'px';
  }
  btn.addEventListener('click', function () { setOpen(!nav.classList.contains('menu-open')); });
  list.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () { setOpen(false); });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  window.addEventListener('resize', function () { if (window.innerWidth > 760) setOpen(false); });
})();
