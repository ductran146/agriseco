/* ARG UI orderdetail: màn [data-arg-orderdetail]. Bấm [data-od-cancel] mở hộp xác nhận [data-od-modal]; bấm [data-od-ok] đóng hộp, đổi nhãn [data-od-badge] thành Đã huỷ, ẩn nút huỷ.
   Bắn "arg:ordercancel" ({ count: 1 }). */
(function () {
  'use strict';
  document.addEventListener('click', function (e) {
    var root = e.target.closest('[data-arg-orderdetail]');
    if (!root) return;
    if (e.target.closest('[data-od-cancel]')) { ARG.openLayer(ARG.$('[data-od-modal]', root), e.target.closest('[data-od-cancel]')); return; }
    if (e.target.closest('[data-od-ok]')) {
      ARG.closeLayer(ARG.$('[data-od-modal]', root));
      var b = ARG.$('[data-od-badge]', root); b.className = 'arg-badge'; b.textContent = 'Đã huỷ';
      ARG.$$('[data-od-cancel]', root).forEach(function (x) { x.hidden = true; });
      root.dispatchEvent(new CustomEvent('arg:ordercancel', { bubbles: true, detail: { count: 1 } }));
    }
  });
})();
