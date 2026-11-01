/* ARG UI appbar: header.arg-appbar--condense[data-arg-condense="selector"] chuyển tiêu đề sang dòng thông tin thị trường (tên + giá)
   theo đúng tốc độ cuộn. Biến --p (0..1) trên thanh = mức khối selector (tìm trong cùng màn hình) đã trượt khuất dưới thanh,
   tính trên đoạn 48px cuối (đổi bằng data-arg-condense-range). CSS dùng --p để mờ, trượt, phóng nên chuyển động bám theo ngón tay.
   .is-condensed bật khi p >= 0.5. Bắn "arg:condense" ({ progress }). Khi bật giảm chuyển động, p chỉ nhận 0 hoặc 1. */
(function () {
  'use strict';
  var calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)');
  function update(bar) {
    if (!bar.offsetParent) return;
    var scope = bar.closest('[data-arg-screen]') || document;
    var target = scope.querySelector(bar.getAttribute('data-arg-condense'));
    if (!target) return;
    var range = +bar.getAttribute('data-arg-condense-range') || 48;
    var d = target.getBoundingClientRect().bottom - bar.getBoundingClientRect().bottom;
    var p = Math.max(0, Math.min(1, 1 - d / range));
    if (calm && calm.matches) p = p >= 0.5 ? 1 : 0;
    if (bar._p === p) return;
    bar._p = p;
    bar.style.setProperty('--p', p.toFixed(3));
    var on = p >= 0.5;
    if (on !== bar.classList.contains('is-condensed')) bar.classList.toggle('is-condensed', on);
    bar.dispatchEvent(new CustomEvent('arg:condense', { bubbles: true, detail: { progress: p } }));
  }
  /* [data-arg-fav-toggle]: nút ngôi sao yêu thích, bấm đổi aria-pressed (sao đặc màu vàng khi đã yêu thích) và nhãn theo data-label-on / data-label-off. Bắn "arg:fav" ({ on }). */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-arg-fav-toggle]');
    if (!b) return;
    var on = b.getAttribute('aria-pressed') !== 'true';
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
    var l = b.getAttribute(on ? 'data-label-on' : 'data-label-off');
    if (l) b.setAttribute('aria-label', l);
    b.dispatchEvent(new CustomEvent('arg:fav', { bubbles: true, detail: { on: on } }));
  });
  function all() { ARG.$$('[data-arg-condense]').forEach(update); }
  document.addEventListener('scroll', all, true);
  document.addEventListener('arg:screen', all);
  ARG.register('appbar', all);
})();
