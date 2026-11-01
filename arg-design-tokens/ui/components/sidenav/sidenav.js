/* ARG UI sidenav: [data-arg-sidenav] > nav có nút [data-sn-btn="i"] và vùng nội dung có nhóm [data-sn-group="i"]. Bấm nút thì nhóm tương ứng có [data-sn-active] (CSS chỉ ẩn nhóm khác ở tablet; mobile hiện mọi nhóm). Bắn "arg:sidenav" ({ index }). */
(function () {
  'use strict';
  ARG.register('sidenav', function (root) {
    ARG.$$('[data-arg-sidenav]', root).forEach(function (nav) {
      if (!ARG.once(nav, 'sidenav')) return;
      nav.addEventListener('click', function (e) {
        var b = e.target.closest('[data-sn-btn]');
        if (!b || !nav.contains(b)) return;
        var i = b.getAttribute('data-sn-btn');
        ARG.$$('[data-sn-btn]', nav).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        ARG.$$('[data-sn-group]', nav).forEach(function (g) { g.toggleAttribute('data-sn-active', g.getAttribute('data-sn-group') === i); });
        nav.dispatchEvent(new CustomEvent('arg:sidenav', { bubbles: true, detail: { index: +i } }));
      });
    });
  });
})();
