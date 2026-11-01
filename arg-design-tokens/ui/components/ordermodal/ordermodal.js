/* ARG UI ordermodal: bấm [data-arg-order-cta] trong form [data-arg-order] mở hộp xác nhận [data-arg-confirm] của màn hình (cùng [data-arg-screen]).
   Điền [data-ord="title|symbol|type|price|qty|value"] từ form, đổi nút [data-ord="ok"] thành Mua hoặc Bán theo data-side của form.
   Bấm [data-arg-confirm-ok]: đóng hộp xác nhận, mở hộp báo thành công [data-arg-done], điền [data-ord="done"]. Bắn "arg:order" ({ side, symbol, price, qty }). */
(function () {
  'use strict';
  var last = null;
  function num(box) { var i = box && ARG.$('input', box); var n = parseFloat(String(i ? i.value : '').replace(/\./g, '').replace(',', '.')); return isNaN(n) ? 0 : n; }
  function put(root, key, text) { ARG.$$('[data-ord="' + key + '"]', root).forEach(function (el) { el.textContent = text; }); }
  document.addEventListener('click', function (e) {
    var cta = e.target.closest('[data-arg-order-cta]');
    if (cta) {
      var form = cta.closest('[data-arg-order]'), scope = cta.closest('[data-arg-screen]') || document, m = ARG.$('[data-arg-confirm]', scope);
      if (!form || !m) return;
      var priceBox = ARG.$('[data-arg-field="price"]', form), qtyBox = ARG.$('[data-arg-field="qty"]', form);
      if (num(priceBox) <= 0 || num(qtyBox) <= 0) return;
      var buy = form.getAttribute('data-side') !== 'sell', sel = ARG.$('select', form), amount = ARG.$('[data-arg-order-total]', form);
      last = { side: buy ? 'buy' : 'sell', symbol: form.getAttribute('data-symbol') || '', price: ARG.$('input', priceBox).value, qty: ARG.$('input', qtyBox).value, type: sel ? sel.value : 'LO', value: amount ? amount.textContent : '', form: form };
      put(m, 'title', buy ? 'Xác nhận lệnh mua' : 'Xác nhận lệnh bán');
      put(m, 'symbol', last.symbol); put(m, 'type', last.type); put(m, 'price', last.price); put(m, 'qty', last.qty); put(m, 'value', last.value);
      var ok = ARG.$('[data-ord="ok"]', m);
      ok.textContent = buy ? 'Mua' : 'Bán';
      ok.classList.toggle('arg-btn--buy', buy); ok.classList.toggle('arg-btn--sell', !buy);
      ARG.openLayer(m, cta);
      return;
    }
    var yes = e.target.closest('[data-arg-confirm-ok]');
    if (yes && last) {
      var box = yes.closest('[data-arg-confirm]'), scope2 = yes.closest('[data-arg-screen]') || document, done = ARG.$('[data-arg-done]', scope2);
      ARG.closeLayer(box);
      if (navigator.vibrate && !ARG.reducedMotion()) navigator.vibrate(15); /* rung nhẹ xác nhận lệnh (trình duyệt hỗ trợ, chủ yếu Android) */
      if (done) {
        put(done, 'done', 'Lệnh ' + (last.side === 'buy' ? 'mua' : 'bán') + ' ' + last.qty + ' ' + last.symbol + ' giá ' + last.price + ' đã được gửi. Bạn có thể xem trạng thái lệnh tại Sổ lệnh.');
        ARG.openLayer(done, last.form);
      }
      document.dispatchEvent(new CustomEvent('arg:order', { detail: { side: last.side, symbol: last.symbol, price: last.price, qty: last.qty } }));
    }
  });
})();
