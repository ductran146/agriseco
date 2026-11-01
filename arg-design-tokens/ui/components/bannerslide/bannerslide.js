/* ARG UI bannerslide: [data-arg-bslide] > .arg-bslide__track (các .arg-bslide__item) + .arg-bslide__dots (nút .arg-bslide__dot).
   Chấm theo vị trí cuộn, bấm chấm thì cuộn tới ảnh đó. Tự chuyển ảnh sau 5 giây, dừng khi rê chuột, chạm, hoặc bật giảm chuyển động. Bắn "arg:bslide" ({ index }). */
(function () {
  'use strict';
  ARG.register('bannerslide', function (root) {
    ARG.$$('[data-arg-bslide]', root).forEach(function (el) {
      if (!ARG.once(el, 'bslide')) return;
      var track = ARG.$('.arg-bslide__track', el), items = ARG.$$('.arg-bslide__item', el), dots = ARG.$$('.arg-bslide__dot', el), idx = 0, paused = false;
      function go(i) { idx = (i + items.length) % items.length; track.scrollTo({ left: items[idx].offsetLeft - track.offsetLeft, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }); }
      function mark(i) { idx = i; dots.forEach(function (d, k) { if (k === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); }); el.dispatchEvent(new CustomEvent('arg:bslide', { bubbles: true, detail: { index: i } })); }
      track.addEventListener('scroll', function () { var i = Math.round(track.scrollLeft / Math.max(1, track.clientWidth)); if (i !== idx && i >= 0 && i < items.length) mark(i); });
      dots.forEach(function (d, k) { d.addEventListener('click', function () { go(k); }); });
      ['mouseenter', 'pointerdown', 'focusin'].forEach(function (n) { el.addEventListener(n, function () { paused = true; }); });
      ['mouseleave', 'focusout'].forEach(function (n) { el.addEventListener(n, function () { paused = false; }); });
      if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && items.length > 1) setInterval(function () { if (!paused && !document.hidden && el.offsetParent) go(idx + 1); }, 5000);
    });
  });
})();
