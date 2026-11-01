/* ARG UI dropdown: [data-arg-dropdown] > button[aria-haspopup] + .arg-menu.
   Enter/Space/click opens, ArrowUp/Down moves, Esc or outside click closes.
   Items with aria-checked act as a select: [data-arg-label] shows the choice, fires "arg:select". */
(function () {
  'use strict';
  var all = [];

  function parts(dd) { return { trigger: ARG.$('button[aria-haspopup]', dd), menu: ARG.$('.arg-menu', dd) }; }
  function close(dd) {
    var p = parts(dd);
    p.menu.hidden = true;
    p.trigger.setAttribute('aria-expanded', 'false');
  }
  function open(dd) {
    all.forEach(function (o) { if (o !== dd) close(o); });
    var p = parts(dd);
    p.menu.hidden = false;
    p.trigger.setAttribute('aria-expanded', 'true');
  }

  ARG.register('dropdown', function (root) {
    ARG.$$('[data-arg-dropdown]', root).forEach(function (dd) {
      if (!ARG.once(dd, 'dropdown')) return;
      all.push(dd);
      var p = parts(dd);
      var items = function () { return ARG.$$('.arg-menu__item', p.menu); };

      p.trigger.addEventListener('click', function () { p.menu.hidden ? open(dd) : close(dd); });
      p.trigger.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown') { e.preventDefault(); open(dd); var f = items()[0]; if (f) f.focus(); }
      });
      p.menu.addEventListener('keydown', function (e) {
        var list = items(), i = list.indexOf(document.activeElement);
        if (e.key === 'ArrowDown') { e.preventDefault(); list[(i + 1) % list.length].focus(); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); list[(i - 1 + list.length) % list.length].focus(); }
        else if (e.key === 'Escape') { close(dd); p.trigger.focus(); }
        else if (e.key === 'Tab') close(dd);
      });
      p.menu.addEventListener('click', function (e) {
        var it = e.target.closest('.arg-menu__item');
        if (!it) return;
        if (it.hasAttribute('aria-checked')) {
          items().forEach(function (x) {
            var on = x === it;
            x.setAttribute('aria-checked', String(on));
            var tick = ARG.$('.end', x);
            if (tick) tick.style.visibility = on ? 'visible' : 'hidden';
          });
          var label = ARG.$('[data-arg-label]', dd);
          if (label) label.textContent = it.firstChild.textContent.trim();
          dd.dispatchEvent(new CustomEvent('arg:select', { bubbles: true, detail: { item: it } }));
        }
        close(dd);
        p.trigger.focus();
      });
    });
  });

  document.addEventListener('click', function (e) {
    all.forEach(function (dd) { if (!dd.contains(e.target)) close(dd); });
  });
})();
