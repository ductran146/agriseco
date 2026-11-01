/* ARG UI ordermodify: màn [data-arg-modify] (Sửa lệnh). Giá, khối lượng ở hai chế độ Lite, Pro luôn đồng bộ; nút [data-om-submit] chỉ bật khi giá hoặc khối lượng khác lệnh gốc
   (data-om-price, data-om-qty trên form). Bấm nút: điền [data-ord="title|symbol|type|price|qty|value"] vào hộp [data-om-modal] rồi mở; [data-om-ok] đóng hộp, mở hộp [data-om-done].
   Bắn "arg:ordermodify" ({ symbol, price, qty }). */
(function () {
  'use strict';
  function val(form, name) { var i = ARG.$('[data-arg-field="' + name + '"] input', form); return i ? i.value : ''; }
  function put(root, key, text) { ARG.$$('[data-ord="' + key + '"]', root).forEach(function (el) { el.textContent = text; }); }
  function forms(root) { return ARG.$$('[data-arg-order]', root); }
  function active(root) { return forms(root).filter(function (f) { return f.offsetParent !== null; })[0] || forms(root)[0]; }
  function sync(root) {
    var f = forms(root)[0], dirty = val(f, 'price') !== f.getAttribute('data-om-price') || val(f, 'qty') !== f.getAttribute('data-om-qty');
    ARG.$$('[data-om-submit]', root).forEach(function (b) { b.disabled = !dirty; });
  }
  document.addEventListener('input', function (e) {
    var root = e.target.closest('[data-arg-modify]'), box = e.target.closest('[data-arg-field]');
    if (!root || !box) return;
    var name = box.getAttribute('data-arg-field');
    forms(root).forEach(function (f) {
      var i = ARG.$('[data-arg-field="' + name + '"] input', f);
      if (i && i !== e.target && i.value !== e.target.value) { i.value = e.target.value; i.dispatchEvent(new Event('input', { bubbles: true })); }
    });
    sync(root);
  });
  document.addEventListener('click', function (e) {
    var root = e.target.closest('[data-arg-modify]');
    if (!root) return;
    var go = e.target.closest('[data-om-submit]'), ok = e.target.closest('[data-om-ok]');
    if (go && !go.disabled) {
      var f = active(root), m = ARG.$('[data-om-modal]', root), t = ARG.$('[data-arg-order-total]', f);
      put(m, 'title', f.getAttribute('data-side') === 'sell' ? 'Sửa lệnh bán ' + f.getAttribute('data-symbol') : 'Sửa lệnh mua ' + f.getAttribute('data-symbol'));
      put(m, 'symbol', f.getAttribute('data-symbol')); put(m, 'type', 'LO'); put(m, 'price', val(f, 'price')); put(m, 'qty', val(f, 'qty')); put(m, 'value', t ? t.textContent : '');
      ARG.openLayer(m, go);
    } else if (ok) {
      var g = active(root), d = ARG.$('[data-om-done]', root), side = g.getAttribute('data-side') === 'sell' ? 'bán' : 'mua';
      ARG.closeLayer(ARG.$('[data-om-modal]', root));
      put(d, 'done', 'Lệnh ' + side + ' ' + g.getAttribute('data-symbol') + ' đã được sửa thành ' + val(g, 'qty') + ' cổ phiếu, giá ' + val(g, 'price') + '. Bạn có thể xem trạng thái lệnh tại Sổ lệnh.');
      ARG.openLayer(d, ok);
      root.dispatchEvent(new CustomEvent('arg:ordermodify', { bubbles: true, detail: { symbol: g.getAttribute('data-symbol'), price: val(g, 'price'), qty: val(g, 'qty') } }));
    }
  });
  ARG.register('ordermodify', function (root) { ARG.$$('[data-arg-modify]', root).forEach(sync); });
})();
