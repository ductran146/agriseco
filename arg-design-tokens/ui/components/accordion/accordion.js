/* ARG UI accordion + collapse.
   [data-arg-accordion]: one panel open at a time (buttons are .arg-accordion__btn, panels are .arg-collapse via aria-controls).
   [data-arg-collapse]: standalone toggle; aria-controls points at a .arg-collapse. */
(function () {
  'use strict';
  function panel(btn) { return document.getElementById(btn.getAttribute('aria-controls')); }

  ARG.register('accordion', function (root) {
    ARG.$$('[data-arg-accordion]', root).forEach(function (acc) {
      if (!ARG.once(acc, 'accordion')) return;
      acc.addEventListener('click', function (e) {
        var b = e.target.closest('.arg-accordion__btn');
        if (!b || !acc.contains(b)) return;
        var open = b.getAttribute('aria-expanded') !== 'true';
        ARG.$$('.arg-accordion__btn', acc).forEach(function (x) {
          var on = x === b && open;
          x.setAttribute('aria-expanded', String(on));
          panel(x).classList.toggle('is-open', on);
        });
      });
    });
    ARG.$$('[data-arg-collapse]', root).forEach(function (btn) {
      if (!ARG.once(btn, 'collapse')) return;
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') !== 'true';
        btn.setAttribute('aria-expanded', String(open));
        panel(btn).classList.toggle('is-open', open);
      });
    });
  });
})();
