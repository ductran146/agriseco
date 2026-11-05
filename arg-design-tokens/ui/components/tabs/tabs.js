/* ARG UI tabs: [data-arg-tabs] > [role=tablist] + [role=tabpanel] (same order).
   Arrow keys, Home, End move focus; aria-orientation="vertical" switches to Up/Down. Fires "arg:tab".
   Dải tab cuộn ngang: tab được chọn (bấm hoặc phím) cuộn ra giữa dải. */
(function () {
  'use strict';
  ARG.register('tabs', function (root) {
    ARG.$$('[data-arg-tabs]', root).forEach(function (t) {
      if (!ARG.once(t, 'tabs')) return;
      var own = function (el) { return el.closest('[data-arg-tabs]') === t; }; /* bỏ qua tab lồng bên trong một tabpanel */
      var list = ARG.$$('[role="tablist"]', t).filter(own)[0];
      var tabs = ARG.$$('[role="tab"]', t).filter(own);
      var panels = ARG.$$('[role="tabpanel"]', t).filter(own);
      var vertical = list.getAttribute('aria-orientation') === 'vertical';

      /* dải tab cuộn ngang: đưa tab vừa chọn ra giữa dải để luôn thấy một phần các tab hai bên (chỉ cuộn ngang trong dải, không cuộn trang); tab đầu, cuối dải thì dừng ở mép */
      function center(x) {
        if (vertical || list.scrollWidth <= list.clientWidth) return;
        var l = x.getBoundingClientRect().left - list.getBoundingClientRect().left + list.scrollLeft;
        list.scrollTo({ left: Math.max(0, l + x.offsetWidth / 2 - list.clientWidth / 2), behavior: ARG.reducedMotion && ARG.reducedMotion() ? 'auto' : 'smooth' });
      }
      function select(i, focus) {
        tabs.forEach(function (x, j) { x.setAttribute('aria-selected', String(i === j)); x.tabIndex = i === j ? 0 : -1; });
        panels.forEach(function (p, j) { p.hidden = i !== j; });
        if (focus) tabs[i].focus();
        t.dispatchEvent(new CustomEvent('arg:tab', { bubbles: true, detail: { index: i } }));
        /* data-arg-tabs-sync="nhóm": các bộ tab cùng nhóm chọn cùng vị trí (ví dụ chọn sàn ở nhiều chế độ xem) */
        var g = t.getAttribute('data-arg-tabs-sync');
        if (g && !select.syncing) ARG.$$('[data-arg-tabs-sync="' + g + '"]').forEach(function (o) { if (o !== t && o._argSelect) { o._argSelect.syncing = true; o._argSelect(i); o._argSelect.syncing = false; } });
      }
      tabs.forEach(function (x, i) {
        x.addEventListener('click', function () {
          if (x.disabled) return;
          select(i);
          center(x);
        });
        x.addEventListener('keydown', function (e) {
          var next = vertical ? 'ArrowDown' : 'ArrowRight', prev = vertical ? 'ArrowUp' : 'ArrowLeft';
          var enabled = tabs.map(function (_, k) { return k; }).filter(function (k) { return !tabs[k].disabled; });
          var pos = enabled.indexOf(i), to = null;
          if (e.key === next) to = enabled[(pos + 1) % enabled.length];
          else if (e.key === prev) to = enabled[(pos - 1 + enabled.length) % enabled.length];
          else if (e.key === 'Home') to = enabled[0];
          else if (e.key === 'End') to = enabled[enabled.length - 1];
          if (to !== null) { e.preventDefault(); select(to, true); center(tabs[to]); }
        });
      });
      t._argSelect = select;
      var start = tabs.findIndex(function (x) { return x.getAttribute('aria-selected') === 'true'; });
      select(start < 0 ? 0 : start);
    });
  });
})();
