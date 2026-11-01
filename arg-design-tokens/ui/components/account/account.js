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
