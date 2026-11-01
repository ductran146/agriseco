/* ARG UI donut: rê chuột (máy tính) hoặc nhấn giữ khoảng 250ms rồi kéo (điện thoại) lên một cung [path.seg] thì cung đó phóng to, các cung khác mờ đi,
   giữa vòng hiện thông số của cung (data-main trên dòng đậm, data-name trên dòng nhỏ). Rời chuột hoặc thả tay thì trả về như cũ. Vuốt nhanh vẫn cuộn trang.
   Bắn "arg:donut" ({ name, main }) trên .arg-donut khi đổi cung. */
(function () {
  'use strict';
  var HOLD = 250, MOVE = 8;
  function setup(box) {
    var chart = ARG.$('.arg-donut__chart', box), b = ARG.$('.arg-donut__center b', box), sp = ARG.$('.arg-donut__center span', box);
    if (!chart || !b || !sp) return;
    var orig = { b: b.textContent, s: sp.textContent }, segs = ARG.$$('path.seg', chart), cur = null, timer = 0, on = false, x0 = 0, y0 = 0;
    function show(seg) {
      if (seg === cur) return;
      cur = seg;
      chart.classList.toggle('is-active', !!seg);
      segs.forEach(function (s) { s.classList.toggle('is-on', s === seg); });
      b.textContent = seg ? seg.getAttribute('data-main') : orig.b;
      sp.textContent = seg ? seg.getAttribute('data-name') : orig.s;
      if (seg) box.dispatchEvent(new CustomEvent('arg:donut', { bubbles: true, detail: { name: seg.getAttribute('data-name'), main: seg.getAttribute('data-main') } }));
    }
    function at(x, y) { var el = document.elementFromPoint(x, y); return el && el.closest && el.closest('path.seg') && segs.indexOf(el.closest('path.seg')) >= 0 ? el.closest('path.seg') : null; }
    segs.forEach(function (s) {
      s.addEventListener('mouseenter', function () { show(s); });
      s.addEventListener('mouseleave', function () { show(null); });
    });
    chart.addEventListener('touchstart', function (e) {
      var t = e.touches[0]; x0 = t.clientX; y0 = t.clientY; on = false; clearTimeout(timer);
      timer = setTimeout(function () { on = true; show(at(x0, y0)); }, HOLD);
    }, { passive: true });
    chart.addEventListener('touchmove', function (e) {
      var t = e.touches[0];
      if (on) { e.preventDefault(); show(at(t.clientX, t.clientY)); return; }
      if (Math.abs(t.clientX - x0) > MOVE || Math.abs(t.clientY - y0) > MOVE) clearTimeout(timer);
    }, { passive: false });
    function end() { clearTimeout(timer); on = false; show(null); }
    chart.addEventListener('touchend', end); chart.addEventListener('touchcancel', end);
    chart.addEventListener('contextmenu', function (e) { if (on) e.preventDefault(); });
  }
  ARG.register('donut', function (root) { ARG.$$('.arg-donut', root).forEach(function (el) { if (ARG.once(el, 'donut')) setup(el); }); });
})();
