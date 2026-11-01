/* ARG UI account: nút [data-arg-account-eye] trong .arg-account ẩn hoặc hiện mọi số [data-arg-secret] trong thẻ.
   Icon luôn là trạng thái sẽ chuyển tới: đang hiện số thì eye-slash (bấm để ẩn), đang ẩn thì eye (bấm để hiện).
   Thẻ nhận lớp .is-hidden khi đang ẩn. Bắn "arg:secret" ({ hidden }). */
(function () {
  'use strict';
  var MASK = '••••••';
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-arg-account-eye]');
    if (!btn) return;
    var card = btn.closest('.arg-account');
    if (!card) return;
    var hide = !card.classList.contains('is-hidden');
    ARG.$$('[data-arg-secret]', card).forEach(function (el) { if (el.__argCountEnd) el.__argCountEnd(); });
    ARG.$$('[data-arg-secret]', card).forEach(function (el) {
      if (hide) { el.setAttribute('data-arg-value', el.textContent); el.textContent = MASK; }
      else if (el.hasAttribute('data-arg-value')) { el.textContent = el.getAttribute('data-arg-value'); el.removeAttribute('data-arg-value'); }
    });
    card.classList.toggle('is-hidden', hide);
    btn.setAttribute('aria-label', hide ? 'Hiện số dư' : 'Ẩn số dư');
    btn.innerHTML = ARG.icon(hide ? 'eye' : 'eye-slash');
    card.dispatchEvent(new CustomEvent('arg:secret', { bubbles: true, detail: { hidden: hide } }));
  });
})();

/* Số tổng tài sản đếm từ 0 lên giá trị thật (~600ms, giảm tốc) khi thẻ hiện ra lần đầu. Dùng setInterval, không dùng requestAnimationFrame
   (headless không chạy). Tôn trọng prefers-reduced-motion: không đếm, hiện số thật ngay. */
(function () {
  'use strict';
  var fmt = function (n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); };
  function count(el) {
    var finalText = el.textContent, target = parseInt(finalText.replace(/\D/g, ''), 10);
    if (!target || ARG.reducedMotion()) return;
    var steps = 24, i = 0, timer;
    el.__argCountEnd = function () { clearInterval(timer); el.textContent = finalText; el.__argCountEnd = null; };
    el.textContent = fmt(0);
    timer = setInterval(function () {
      i += 1;
      var t = i / steps; t = 1 - Math.pow(1 - t, 3);
      if (i >= steps) el.__argCountEnd(); else el.textContent = fmt(target * t);
    }, 25);
  }
  ARG.register('account-count', function (root) {
    ARG.$$('.arg-account__amount[data-arg-secret]', root).forEach(function (el) {
      if (!ARG.once(el, 'count')) return;
      if (!('IntersectionObserver' in window)) { count(el); return; }
      var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { io.disconnect(); count(el); } });
      io.observe(el);
    });
  });
})();
