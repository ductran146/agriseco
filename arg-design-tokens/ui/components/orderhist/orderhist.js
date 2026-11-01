/* ARG UI orderhist: tab Lịch sử lệnh [data-arg-orderhist] (lệnh của các phiên trước; xem orderbook.js cho lệnh trong ngày).
   - data-today (yyyy-mm-dd): ngày "hôm nay" của dữ liệu mẫu; data-period: khoảng thời gian đang chọn (7, 30, 90, custom).
   - Lọc: select[data-oh-period-select] (chọn khoảng thời gian: 7, 30, 90, custom; custom hiện [data-oh-range] với hai ô ngày datepicker), [data-oh-status], [data-oh-side] (all, buy, sell) là radio trong bảng Bộ lọc; [data-oh-reset] đặt lại hai bộ lọc này.
   - Mỗi lệnh .arg-orderrow có data-date, data-side, data-status, data-matched (khối lượng khớp), data-value (giá trị khớp, đồng).
   - Cập nhật: tổng kết ([data-oh-buy] [data-oh-sell]), số lệnh từng ngày ([data-oh-day-n]), ẩn ngày không còn lệnh, [data-oh-empty], số bộ lọc đang bật ([data-oh-fcount], trạng thái hoặc chiều lệnh khác Tất cả; nút Bộ lọc thêm .is-active), nhãn nút áp dụng [data-oh-apply] ("Xem n lệnh").
   Bắn "arg:orderhist" ({ count }) sau mỗi lần lọc. */
(function () {
  'use strict';
  var state = new WeakMap();
  function st(root) { if (!state.has(root)) state.set(root, { status: 'all', side: 'all', period: root.getAttribute('data-period') || '30', from: '', to: '' }); return state.get(root); }
  function iso(d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function range(root) {
    var s = st(root), t = root.getAttribute('data-today') || iso(new Date());
    if (s.period === 'custom') return [s.from || '0000-00-00', s.to || '9999-99-99'];
    var d = new Date(t + 'T00:00:00'); d.setDate(d.getDate() - parseInt(s.period, 10));
    return [iso(d), t];
  }
  function money(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }
  function apply(root) {
    var s = st(root), r = range(root), rows = ARG.$$('.arg-orderrow', root), shown = 0, buy = 0, sell = 0;
    var inRange = function (li) { return li.dataset.date >= r[0] && li.dataset.date <= r[1]; };
    rows.forEach(function (li) {
      var on = inRange(li) && (s.status === 'all' || li.dataset.status === s.status) && (s.side === 'all' || li.dataset.side === s.side);
      li.hidden = !on;
      if (!on) return;
      shown++;
      var v = +li.dataset.value || 0;
      if (+li.dataset.matched > 0) { if (li.dataset.side === 'buy') buy += v; else sell += v; }
    });
    ARG.$$('[data-oh-day]', root).forEach(function (d) {
      var n = ARG.$$('.arg-orderrow', d).filter(function (li) { return !li.hidden; }).length;
      d.hidden = n === 0;
      var c = ARG.$('[data-oh-day-n]', d); if (c) c.textContent = n + ' lệnh';
    });
    var set = function (sel, v) { ARG.$$(sel, root).forEach(function (el) { el.textContent = v; }); };
    set('[data-oh-buy]', money(buy)); set('[data-oh-sell]', money(sell)); set('[data-oh-apply]', 'Xem ' + shown + ' lệnh');
    var fc = (s.status !== 'all' ? 1 : 0) + (s.side !== 'all' ? 1 : 0);
    ARG.$$('[data-oh-fcount]', root).forEach(function (el) { el.textContent = fc; el.hidden = fc === 0; });
    ARG.$$('.arg-orderhist__filter', root).forEach(function (b) { b.classList.toggle('is-active', fc > 0); });
    ARG.$$('[data-oh-empty]', root).forEach(function (el) { el.hidden = shown > 0; });
    root.dispatchEvent(new CustomEvent('arg:orderhist', { bubbles: true, detail: { count: shown } }));
  }
  /* Bộ lọc là radio (chọn một trong nhiều): chọn xong lọc ngay; Đặt lại chọn lại "Tất cả" của cả hai nhóm */
  document.addEventListener('change', function (e) {
    var root = e.target.closest && e.target.closest('[data-arg-orderhist]');
    if (!root || !e.target.matches('input[type="radio"]')) return;
    var s = st(root);
    if (e.target.matches('[data-oh-status]')) s.status = e.target.value;
    else if (e.target.matches('[data-oh-side]')) s.side = e.target.value;
    else return;
    apply(root);
  });
  document.addEventListener('click', function (e) {
    var root = e.target.closest('[data-arg-orderhist]');
    if (!root || !e.target.closest('[data-oh-reset]')) return;
    var s = st(root);
    s.status = 'all'; s.side = 'all';
    ARG.$$('input[data-oh-status][value="all"], input[data-oh-side][value="all"]', root).forEach(function (r) { r.checked = true; });
    apply(root);
  });
  document.addEventListener('change', function (e) {
    var root = e.target.closest && e.target.closest('[data-arg-orderhist]');
    if (!root || !e.target.matches('[data-oh-period-select]')) return;
    var s = st(root);
    s.period = e.target.value; root.setAttribute('data-period', s.period);
    ARG.$$('[data-oh-range]', root).forEach(function (el) { el.hidden = s.period !== 'custom'; });
    if (s.period === 'custom') readRange(root);
    apply(root);
  });
  function readRange(root) {
    var s = st(root), ins = ARG.$$('[data-oh-range] input[data-iso]', root);
    if (ins[0]) s.from = ins[0].getAttribute('data-iso'); if (ins[1]) s.to = ins[1].getAttribute('data-iso');
  }
  document.addEventListener('arg:date', function (e) {
    var root = e.target.closest && e.target.closest('[data-arg-orderhist]');
    if (!root) return;
    readRange(root); if (st(root).period === 'custom') apply(root);
  });
  ARG.register('orderhist', function (root) {
    ARG.$$('[data-arg-orderhist]', root).forEach(function (el) { if (ARG.once(el, 'orderhist')) apply(el); });
  });
})();
