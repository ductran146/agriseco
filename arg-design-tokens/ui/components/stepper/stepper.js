/* ARG UI stepper: .arg-stepper[data-step][data-dec] với nút [data-arg-step="-1|1"]. Số theo định dạng Việt Nam. Bắn "arg:step". */
(function () {
  'use strict';
  function parse(s) { var n = parseFloat(String(s).replace(/\./g, '').replace(',', '.')); return isNaN(n) ? 0 : n; }
  function fmt(n, d) { var s = n.toFixed(d).split('.'); s[0] = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.'); return s.join(','); }
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-arg-step]');
    if (!btn) return;
    var box = btn.closest('.arg-stepper'), input = box && ARG.$('input', box);
    if (!input) return;
    var step = parseFloat(box.getAttribute('data-step')) || 1, dec = +box.getAttribute('data-dec') || 0;
    var v = Math.max(0, parse(input.value) + step * (+btn.getAttribute('data-arg-step')));
    input.value = fmt(v, dec);
    input.dispatchEvent(new Event('input', { bubbles: true }));
    box.dispatchEvent(new CustomEvent('arg:step', { bubbles: true, detail: { value: v } }));
  });
  /* Chip chọn nhanh trong form [data-arg-order]: [data-arg-set="91,80"] đặt giá; [data-arg-qty-pct="50"] đặt khối lượng bằng % của data-max-qty, làm tròn xuống lô 100. */
  function setField(form, name, text) {
    var input = ARG.$('[data-arg-field="' + name + '"] input', form);
    if (!input) return;
    input.value = text;
    input.dispatchEvent(new Event('input', { bubbles: true }));
  }
  document.addEventListener('click', function (e) {
    var chip = e.target.closest('[data-arg-set], [data-arg-qty-pct]');
    if (!chip) return;
    var form = chip.closest('[data-arg-order]');
    if (!form) return;
    if (chip.hasAttribute('data-arg-set')) setField(form, 'price', chip.getAttribute('data-arg-set'));
    else {
      var max = +form.getAttribute('data-max-qty') || 0, q = Math.floor(max * (+chip.getAttribute('data-arg-qty-pct')) / 100 / 100) * 100;
      setField(form, 'qty', fmt(q, 0));
    }
  });
})();
