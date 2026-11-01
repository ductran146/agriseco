/* ARG UI selectsheet: ô .arg-selectsheet chứa <select> thật (giữ giá trị, ẩn khỏi bấm chuột) và nút phủ .arg-selectsheet__hit[data-arg-open="id"] mở bảng [data-arg-selectsheet].
   Bảng có các nút [role="radio"][data-value]. Mở bảng: đánh dấu mục theo giá trị của select. Chọn mục: gán select.value, bắn "change" trên select, cập nhật aria-label của nút phủ, đóng bảng. */
(function () {
  'use strict';
  var current = null;
  document.addEventListener('click', function (e) {
    var hit = e.target.closest('.arg-selectsheet__hit');
    if (hit) {
      var box = hit.closest('.arg-selectsheet'), sel = ARG.$('select', box), sheet = document.getElementById(hit.getAttribute('data-arg-open'));
      current = { sel: sel, hit: hit, sheet: sheet };
      if (sheet) ARG.$$('[role="radio"]', sheet).forEach(function (r) { r.setAttribute('aria-checked', String(r.getAttribute('data-value') === sel.value)); });
      return;
    }
    var opt = e.target.closest('[data-arg-selectsheet] [role="radio"]');
    if (!opt || !current) return;
    var v = opt.getAttribute('data-value');
    current.sel.value = v;
    current.sel.dispatchEvent(new Event('change', { bubbles: true }));
    current.hit.setAttribute('aria-label', (current.hit.getAttribute('data-label') || '') + ', đang chọn ' + v);
    ARG.$$('[role="radio"]', current.sheet).forEach(function (r) { r.setAttribute('aria-checked', String(r === opt)); });
    ARG.closeLayer(current.sheet);
  });
})();
