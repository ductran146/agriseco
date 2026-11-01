/* ARG UI carousel: [data-arg-carousel] > .arg-carousel__track > slides, with .arg-carousel__nav--prev/next and .arg-carousel__dots.
   Dots are built from the slides. Left/Right arrows work when the carousel has focus. Fires "arg:slide". */
(function () {
  'use strict';
  ARG.register('carousel', function (root) {
    ARG.$$('[data-arg-carousel]', root).forEach(function (c) {
      if (!ARG.once(c, 'carousel')) return;
      var track = ARG.$('.arg-carousel__track', c);
      var slides = Array.prototype.slice.call(track.children);
      var dots = ARG.$('.arg-carousel__dots', c);
      var n = slides.length, i = 0;

      slides.forEach(function (_, k) {
        var d = document.createElement('button');
        d.type = 'button';
        d.setAttribute('aria-label', 'Tới slide ' + (k + 1));
        d.addEventListener('click', function () { go(k); });
        dots.appendChild(d);
      });
      function go(k) {
        i = (k + n) % n;
        track.style.transform = 'translateX(' + (-i * 100) + '%)';
        ARG.$$('button', dots).forEach(function (d, j) { d.setAttribute('aria-current', String(j === i)); });
        slides.forEach(function (s, j) {
          s.setAttribute('role', 'group');
          s.setAttribute('aria-label', (j + 1) + ' / ' + n);
          s.setAttribute('aria-hidden', String(j !== i));
        });
        c.dispatchEvent(new CustomEvent('arg:slide', { bubbles: true, detail: { index: i } }));
      }
      ARG.$('.arg-carousel__nav--prev', c).addEventListener('click', function () { go(i - 1); });
      ARG.$('.arg-carousel__nav--next', c).addEventListener('click', function () { go(i + 1); });
      c.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') go(i - 1);
        if (e.key === 'ArrowRight') go(i + 1);
      });
      go(0);
    });
  });
})();
