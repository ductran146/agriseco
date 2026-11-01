/* ARG UI side: .arg-side__btn trong [data-arg-order] đổi chiều lệnh Mua/Bán; đổi nút [data-arg-order-cta]. Bắn "arg:side".
   Cũng tính [data-arg-order-total] = giá × khối lượng × 1000 khi ô [data-arg-field="price"|"qty"] đổi. */
(function () {
  'use strict';
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.arg-side__btn');
    if (!btn) return;
    var side = btn.classList.contains('arg-side__btn--sell') ? 'sell' : 'buy';
    ARG.$$('.arg-side__btn', btn.parentNode).forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
    var form = btn.closest('[data-arg-order]');
    if (!form) return;
    form.setAttribute('data-side', side);
    var cta = ARG.$('[data-arg-order-cta]', form);
    if (cta) {
      cta.classList.toggle('arg-btn--buy', side === 'buy');
      cta.classList.toggle('arg-btn--sell', side === 'sell');
      cta.textContent = (side === 'buy' ? 'Mua' : 'Bán') + ' - ' + (form.getAttribute('data-symbol') || '');
    }
    form.dispatchEvent(new CustomEvent('arg:side', { bubbles: true, detail: { side: side } }));
  });
  /* Nút [data-arg-go][data-arg-side="buy"|"sell"]: screen.js mở màn trước (nạp trước file này), sau đó chọn sẵn chiều lệnh trong màn đó. */
  document.addEventListener('click', function (e) {
    var go = e.target.closest('[data-arg-go][data-arg-side]');
    if (!go) return;
    var scr = ARG.$('[data-arg-screen="' + go.getAttribute('data-arg-go') + '"]');
    if (scr) ARG.$$('.arg-side__btn--' + go.getAttribute('data-arg-side'), scr).forEach(function (b) { b.click(); });
  });
  /* Công tắc chế độ: [data-arg-modes] (Tabs) với tab[data-mode] đặt data-mode trên màn hình chứa nó; CSS ẩn hiện theo data-mode. */
  document.addEventListener('arg:tab', function (e) {
    var box = e.target.closest && e.target.closest('[data-arg-modes]');
    if (!box) return;
    var tab = ARG.$$('[role="tab"]', box)[e.detail.index], screen = box.closest('[data-arg-screen]');
    if (tab && screen) screen.setAttribute('data-mode', tab.getAttribute('data-mode'));
  });
  function num(box) { var i = box && ARG.$('input', box); var n = parseFloat(String(i ? i.value : '').replace(/\./g, '').replace(',', '.')); return isNaN(n) ? 0 : n; }
  function total(form) {
    var out = ARG.$('[data-arg-order-total]', form);
    if (!out) return;
    var v = Math.round(num(ARG.$('[data-arg-field="price"]', form)) * num(ARG.$('[data-arg-field="qty"]', form)) * 1000);
    out.textContent = String(v).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  }
  document.addEventListener('input', function (e) { var f = e.target.closest && e.target.closest('[data-arg-order]'); if (f) total(f); });
  ARG.register('side', function (root) { ARG.$$('[data-arg-order]', root).forEach(total); });
})();
