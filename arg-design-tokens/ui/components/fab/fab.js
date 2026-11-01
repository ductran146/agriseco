/* ARG UI fab: button.arg-fab[data-arg-fab][data-arg-target="selector"][data-arg-class="tên-class"].
   Bấm thì bật tắt class trên các phần tử khớp selector trong vùng [data-arg-listbar-scope] gần nhất (hoặc cả trang), cập nhật aria-pressed. */
(function () {
  'use strict';
  ARG.register('fab', function (root) {
    ARG.$$('[data-arg-fab]', root).forEach(function (b) {
      if (!ARG.once(b, 'fab')) return;
      b.addEventListener('click', function () {
        var scope = b.closest('[data-arg-listbar-scope]') || document, on = b.getAttribute('aria-pressed') !== 'true';
        ARG.$$(b.getAttribute('data-arg-target'), scope).forEach(function (el) { el.classList.toggle(b.getAttribute('data-arg-class'), on); });
        b.setAttribute('aria-pressed', String(on));
      });
    });
  });
})();
