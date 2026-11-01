/* ARG UI listbar: .arg-listbar[data-arg-listbar] trong vùng [data-arg-listbar-scope].
   - select[data-arg-pane-select]: giá trị chọn hiện khung [data-arg-pane="giá trị"] cùng vùng, ẩn các khung khác.
   - menu sắp xếp [data-arg-sort] (dropdown, mỗi mục có data-sort): sắp xếp mọi ul[data-arg-sortable] trong vùng theo data-code, data-pct, data-price, data-vol của li.
     Mục "def" trả về thứ tự ban đầu. Dòng thêm sau đó giữ đúng kiểu sắp xếp đang chọn (bắn "arg:rows" trên vùng).
   - nút chip [data-arg-pane-tab="giá trị"] (kiểu danh mục): bấm chọn chip, hiện khung [data-arg-pane] tương ứng; dải chip cuộn ngang, chip chọn được cuộn vào giữa, đặt data-more trên __main khi còn chip bị khuất bên phải (CSS làm mờ mép).
   Bắn "arg:pane" ({ value }) trên vùng khi đổi khung. */
(function () {
  'use strict';
  var CMP = {
    code: function (a, b) { return a.dataset.code.localeCompare(b.dataset.code); },
    up: function (a, b) { return b.dataset.pct - a.dataset.pct; },
    down: function (a, b) { return a.dataset.pct - b.dataset.pct; },
    price: function (a, b) { return b.dataset.price - a.dataset.price; },
    vol: function (a, b) { return b.dataset.vol - a.dataset.vol; },
    pl: function (a, b) { return b.dataset.pl - a.dataset.pl; },
    loss: function (a, b) { return a.dataset.pl - b.dataset.pl; },
    val: function (a, b) { return b.dataset.val - a.dataset.val; },
    def: function (a, b) { return a.dataset.i - b.dataset.i; }
  };
  ARG.register('listbar', function (root) {
    ARG.$$('[data-arg-listbar]', root).forEach(function (bar) {
      if (!ARG.once(bar, 'listbar')) return;
      var scope = bar.closest('[data-arg-listbar-scope]') || bar.parentNode, key = 'def';
      var sel = ARG.$('select[data-arg-pane-select]', bar);
      function panes() { return ARG.$$('[data-arg-pane]', scope); }
      function sort() {
        ARG.$$('ul[data-arg-sortable]', scope).forEach(function (ul) {
          var items = Array.prototype.slice.call(ul.children);
          items.forEach(function (li, i) { if (li.dataset.i === undefined) li.dataset.i = i; });
          if (key === 'def') items.forEach(function (li, i) { if (li.dataset.added) li.dataset.i = 1e6 + i; });
          items.sort(CMP[key]).forEach(function (li) { ul.appendChild(li); });
        });
      }
      if (sel) sel.addEventListener('change', function () {
        panes().forEach(function (p) { p.hidden = p.getAttribute('data-arg-pane') !== sel.value; });
        scope.dispatchEvent(new CustomEvent('arg:pane', { bubbles: true, detail: { value: sel.value } }));
      });
      var chips = ARG.$$('[data-arg-pane-tab]', bar), strip = ARG.$('.arg-chip-tabs__list', bar), main = ARG.$('.arg-listbar__main', bar);
      function more() { if (strip && main) main.toggleAttribute('data-more', strip.scrollLeft + strip.clientWidth < strip.scrollWidth - 2); }
      chips.forEach(function (c) {
        c.addEventListener('click', function () {
          var v = c.getAttribute('data-arg-pane-tab');
          chips.forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
          panes().forEach(function (p) { p.hidden = p.getAttribute('data-arg-pane') !== v; });
          var calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
          strip.scrollTo({ left: c.offsetLeft - (strip.clientWidth - c.offsetWidth) / 2, behavior: calm ? 'auto' : 'smooth' }); if (calm) more();
          scope.dispatchEvent(new CustomEvent('arg:pane', { bubbles: true, detail: { value: v } }));
        });
      });
      if (strip) { strip.addEventListener('scroll', more); window.addEventListener('resize', more); document.addEventListener('arg:screen', function () { setTimeout(more); }); document.addEventListener('arg:tab', function () { setTimeout(more); }); more(); }
      var dd = ARG.$('[data-arg-sort]', bar);
      if (dd) dd.addEventListener('arg:select', function (e) { key = e.detail.item.getAttribute('data-sort') || 'def'; sort(); });
      scope.addEventListener('arg:rows', function () { if (key !== 'def') sort(); });
    });
  });
})();
