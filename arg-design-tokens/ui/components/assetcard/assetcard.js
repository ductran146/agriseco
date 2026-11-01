/* ARG UI assetcard: nút [data-arg-asset-eye] trong .arg-assetcard ẩn hoặc hiện mọi số [data-arg-secret] trong vùng [data-arg-secret-scope] gần nhất (không có thì chỉ trong thẻ).
   Icon luôn là trạng thái sẽ chuyển tới (đang hiện số thì eye-slash). Vùng nhận lớp .is-hidden khi đang ẩn. Bắn "arg:secret" ({ hidden }). */
(function () {
  'use strict';
  var MASK = '••••••';
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-arg-asset-eye]');
    if (!btn) return;
    var card = btn.closest('.arg-assetcard'), scope = btn.closest('[data-arg-secret-scope]') || card;
    if (!card) return;
    var hide = !scope.classList.contains('is-hidden');
    ARG.$$('[data-arg-secret]', scope).forEach(function (el) {
      if (hide) { if (!el.hasAttribute('data-arg-value')) { el.setAttribute('data-arg-value', el.textContent); el.textContent = MASK; } }
      else if (el.hasAttribute('data-arg-value')) { el.textContent = el.getAttribute('data-arg-value'); el.removeAttribute('data-arg-value'); }
    });
    scope.classList.toggle('is-hidden', hide);
    btn.setAttribute('aria-label', hide ? 'Hiện số dư' : 'Ẩn số dư');
    btn.innerHTML = ARG.icon(hide ? 'eye' : 'eye-slash', 'i--20');
    scope.dispatchEvent(new CustomEvent('arg:secret', { bubbles: true, detail: { hidden: hide } }));
  });
})();
