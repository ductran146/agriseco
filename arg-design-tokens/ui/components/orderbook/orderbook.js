/* ARG UI orderbook: màn hình [data-arg-orderbook] (thường là chính .arg-screen).
   - Lọc: chip [data-ob-status] (all, pending, partial, matched, cancelled), nút [data-ob-side] (all, buy, sell), ô tìm [data-ob-search] theo mã; [data-ob-count] ghi số lệnh đang hiện; [data-ob-empty] hiện khi không có lệnh.
   - Bấm .arg-orderrow__main (liên kết data-arg-go) mở màn chi tiết lệnh; ở chế độ chọn nhiều thì bấm là chọn lệnh còn huỷ được, không chuyển màn.
   - Chọn nhiều: [data-ob-select] bật hoặc tắt data-select (hiện ô chọn của lệnh còn huỷ được, thanh [data-ob-bar] thay thanh tab); [data-ob-all] chọn tất cả lệnh đang hiện còn huỷ được; [data-ob-cancel] huỷ các lệnh đã chọn,
     nhấn giữ (450ms) một lệnh còn huỷ được cũng bật chế độ chọn và chọn sẵn lệnh đó. Huỷ mở hộp xác nhận [data-ob-modal]; bấm [data-ob-ok] đổi các lệnh sang Đã huỷ. Bắn "arg:ordercancel" ({ count }). */
(function () {
  'use strict';
  var LABEL = { pending: 'Chờ khớp', partial: 'Khớp một phần', matched: 'Đã khớp', cancelled: 'Đã huỷ' };
  var BADGE = { pending: 'arg-badge--yellow', partial: 'arg-badge--blue', matched: 'arg-badge--success', cancelled: '' };
  var state = new WeakMap();
  function st(root) { if (!state.has(root)) state.set(root, { status: 'all', side: 'all', q: '', pending: [] }); return state.get(root); }
  function rows(root) { return ARG.$$('.arg-orderrow', root); }
  function pick(li) { return ARG.$('.arg-orderrow__pick input', li); }
  function apply(root) {
    var s = st(root), n = 0;
    rows(root).forEach(function (li) {
      var on = (s.status === 'all' || li.dataset.status === s.status) && (s.side === 'all' || li.dataset.side === s.side) && (!s.q || li.dataset.code.indexOf(s.q) >= 0);
      li.hidden = !on; if (on) n++;
    });
    ARG.$$('[data-ob-count]', root).forEach(function (el) { el.textContent = n + ' lệnh'; });
    ARG.$$('[data-ob-empty]', root).forEach(function (el) { el.hidden = n > 0; });
    ARG.$$('[data-ob-status]', root).forEach(function (c) {
      var k = c.getAttribute('data-ob-status'), cnt = rows(root).filter(function (li) { return k === 'all' || li.dataset.status === k; }).length;
      var t = ARG.$('[data-ob-n]', c); if (t) t.textContent = cnt;
    });
    sync(root);
  }
  function sync(root) {
    var vis = rows(root).filter(function (li) { return !li.hidden && li.hasAttribute('data-cancelable'); });
    var sel = vis.filter(function (li) { return pick(li).checked; }).length;
    var btn = ARG.$('[data-ob-cancel]', root), all = ARG.$('[data-ob-all]', root);
    if (btn) { btn.disabled = sel === 0; btn.textContent = sel ? 'Huỷ lệnh (' + sel + ')' : 'Huỷ lệnh'; }
    if (all) { all.checked = vis.length > 0 && sel === vis.length; all.indeterminate = sel > 0 && sel < vis.length; }
  }
  function ask(root, list) {
    var s = st(root), m = ARG.$('[data-ob-modal]', root);
    if (!list.length || !m) return;
    s.pending = list;
    ARG.$$('[data-ob-title]', m).forEach(function (el) { el.textContent = list.length > 1 ? 'Huỷ ' + list.length + ' lệnh?' : 'Huỷ lệnh này?'; });
    ARG.$$('[data-ob-text]', m).forEach(function (el) { el.textContent = list.length > 1 ? 'Các lệnh đã chọn sẽ bị huỷ và không thể khôi phục.' : 'Lệnh ' + (list[0].dataset.side === 'buy' ? 'mua ' : 'bán ') + list[0].dataset.code + ' sẽ bị huỷ và không thể khôi phục.'; });
    ARG.openLayer(m);
  }
  function setStatus(li, status) {
    li.dataset.status = status;
    li.removeAttribute('data-cancelable');
    var b = ARG.$('.arg-badge', li); b.className = 'arg-badge' + (BADGE[status] ? ' ' + BADGE[status] : ''); b.textContent = LABEL[status];
    var p = ARG.$('.arg-orderrow__pick', li); if (p) p.remove();
  }
  /* Nhấn giữ: vào chế độ chọn nhiều và chọn sẵn lệnh; cờ held chặn lần bấm (click) ngay sau khi nhả tay. */
  var timer = null, held = false;
  document.addEventListener('pointerdown', function (e) {
    var m = e.target.closest('.arg-orderrow__main'), root = m && m.closest('[data-arg-orderbook]'), li = m && m.closest('.arg-orderrow');
    if (!root || !li.hasAttribute('data-cancelable') || root.hasAttribute('data-select')) return;
    clearTimeout(timer);
    timer = setTimeout(function () {
      held = true;
      root.setAttribute('data-select', '');
      ARG.$$('[data-ob-select]', root).forEach(function (b) { b.textContent = 'Xong'; });
      pick(li).checked = true; sync(root);
    }, 450);
  });
  ['pointerup', 'pointercancel', 'pointermove', 'scroll'].forEach(function (n) { document.addEventListener(n, function () { clearTimeout(timer); }, true); });
  /* Pha bắt (capture) chạy trước việc chuyển màn của screen.js: sau nhấn giữ thì bỏ lần bấm vừa nhả; ở chế độ chọn nhiều, bấm lệnh còn huỷ được là chọn lệnh, không chuyển màn. */
  document.addEventListener('click', function (e) {
    if (held) { held = false; e.stopImmediatePropagation(); e.preventDefault(); return; }
    var m = e.target.closest('.arg-orderrow__main'), root = m && m.closest('[data-arg-orderbook]');
    if (!m || !root || !root.hasAttribute('data-select')) return;
    e.preventDefault(); e.stopImmediatePropagation();
    var li = m.closest('.arg-orderrow');
    if (li.hasAttribute('data-cancelable')) { var p = pick(li); p.checked = !p.checked; sync(root); }
  }, true);
  document.addEventListener('click', function (e) {
    var root = e.target.closest('[data-arg-orderbook]');
    if (!root) return;
    var t;
    if ((t = e.target.closest('[data-ob-status]'))) {
      st(root).status = t.getAttribute('data-ob-status');
      ARG.$$('[data-ob-status]', root).forEach(function (c) { c.setAttribute('aria-pressed', String(c === t)); });
      apply(root); return;
    }
    if ((t = e.target.closest('[data-ob-side]'))) {
      st(root).side = t.getAttribute('data-ob-side');
      ARG.$$('[data-ob-side]', root).forEach(function (c) { c.setAttribute('aria-selected', String(c === t)); });
      apply(root); return;
    }
    if ((t = e.target.closest('[data-ob-select]'))) {
      var on = !root.hasAttribute('data-select');
      root.toggleAttribute('data-select', on);
      t.textContent = on ? 'Xong' : 'Chọn';
      if (!on) rows(root).forEach(function (li) { var p = pick(li); if (p) p.checked = false; });
      sync(root); return;
    }
    if ((t = e.target.closest('[data-ob-cancel]'))) { ask(root, rows(root).filter(function (li) { return !li.hidden && pick(li) && pick(li).checked; })); return; }
    if ((t = e.target.closest('[data-ob-ok]'))) {
      var list = st(root).pending;
      list.forEach(function (li) { setStatus(li, 'cancelled'); });
      st(root).pending = [];
      ARG.closeLayer(ARG.$('[data-ob-modal]', root));
      if (root.hasAttribute('data-select')) { root.removeAttribute('data-select'); ARG.$$('[data-ob-select]', root).forEach(function (b) { b.textContent = 'Chọn'; }); }
      apply(root);
      root.dispatchEvent(new CustomEvent('arg:ordercancel', { bubbles: true, detail: { count: list.length } }));
      return;
    }
  });
  document.addEventListener('change', function (e) {
    var root = e.target.closest('[data-arg-orderbook]');
    if (!root) return;
    if (e.target.matches('[data-ob-all]')) {
      var on = e.target.checked;
      rows(root).forEach(function (li) { if (!li.hidden && pick(li)) pick(li).checked = on; });
    }
    sync(root);
  });
  document.addEventListener('input', function (e) {
    var root = e.target.closest('[data-arg-orderbook]');
    if (!root || !e.target.matches('[data-ob-search]')) return;
    st(root).q = e.target.value.trim().toUpperCase();
    apply(root);
  });
})();
