/* ARG UI acctsel (hai kiểu chọn tiểu khoản: menu Dropdown trên thanh đầu, và Select gốc cạnh tiêu đề khối). Kiểu Select: chọn tiểu khoản bằng Select gốc: select.arg-select-native[data-arg-acct], mỗi option có data-sub (chữ dòng phụ của tiêu đề).
   Đổi lựa chọn: hiện các khối [data-arg-acct-pane="giá trị option"] cùng tabpanel (hoặc cùng trang), ẩn khối của tiểu khoản khác,
   và đổi chữ mọi phần tử [data-arg-acct-sub] trong vùng đó. Bắn "arg:acct" ({ id }). */
(function () {
  'use strict';
  /* [data-arg-acct-menu] (Dropdown): chọn mục thì ghi số (dòng trên) và loại (dòng dưới) tiểu khoản lên nút .arg-acctsel (data-no, data-type của mục). Bắn "arg:acct" ({ no, type }). */
  document.addEventListener('arg:select', function (e) {
    var dd = e.target.closest && e.target.closest('[data-arg-acct-menu]');
    if (!dd) return;
    var it = e.detail.item, btn = ARG.$('.arg-acctsel', dd), no = it.getAttribute('data-no'), ty = it.getAttribute('data-type');
    var tyEl = ARG.$('.arg-acctsel__type', btn);
    if (tyEl) { ARG.$('.arg-acctsel__no', btn).textContent = no; tyEl.textContent = ty; } else ARG.$('.arg-acctsel__no', btn).textContent = no + ' - ' + ty;
    btn.setAttribute('aria-label', 'Đổi tiểu khoản, đang chọn ' + no + ' - ' + ty);
    dd.dispatchEvent(new CustomEvent('arg:acct', { bubbles: true, detail: { no: it.getAttribute('data-no'), type: it.getAttribute('data-type') } }));
  });
  /* Bấm nền mờ (phần tử ::after của [data-arg-acct-menu], nên đích bấm chính là dropdown) thì đóng danh sách. */
  document.addEventListener('click', function (e) {
    if (e.target.matches && e.target.matches('[data-arg-acct-menu]')) ARG.$('.arg-acctsel', e.target).click();
  });
  ARG.register('acctsel', function (root) {
    ARG.$$('select[data-arg-acct]', root).forEach(function (sel) {
      if (!ARG.once(sel, 'acctsel')) return;
      var scope = sel.closest('[role="tabpanel"]') || document;
      sel.addEventListener('change', function () {
        var id = sel.value, opt = sel.options[sel.selectedIndex];
        ARG.$$('[data-arg-acct-pane]', scope).forEach(function (p) { p.hidden = p.getAttribute('data-arg-acct-pane') !== id; });
        ARG.$$('[data-arg-acct-sub]', scope).forEach(function (el) { el.textContent = opt.getAttribute('data-sub') || opt.textContent; });
        sel.dispatchEvent(new CustomEvent('arg:acct', { bubbles: true, detail: { id: id } }));
      });
    });
  });
})();
