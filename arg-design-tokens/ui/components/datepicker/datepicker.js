/* ARG UI datepicker: input[data-arg-datepicker] (readonly) trong .arg-control. Bấm ô, icon, hoặc phím Enter, Space thì bảng lịch trượt từ dưới lên.
   - Ô hiện ngày dd/mm/yyyy (không phụ thuộc ngôn ngữ máy); giá trị chuẩn yyyy-mm-dd nằm ở input.dataset.iso.
   - data-min, data-max (yyyy-mm-dd) trên ô: ngày ngoài khoảng bị tắt. Có thể đổi lúc chạy, bảng đọc lại mỗi lần mở.
   - "Hôm nay" lấy từ [data-arg-today="yyyy-mm-dd"] (đặt trên .arg-page để khớp dữ liệu mẫu), không có thì dùng ngày của máy.
   - Chọn ngày rồi bấm Chọn: ghi vào ô, bắn "change" (bubbles) trên ô và "arg:date" ({ iso }). Bấm Huỷ, Esc hoặc nền thì không đổi.
   - Bàn phím: mũi tên đổi ngày (trái phải ±1, lên xuống ±7), PageUp, PageDown đổi tháng, Enter, Space chọn. Bấm tiêu đề để chọn tháng và năm. */
(function () {
  'use strict';
  var MN = ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6', 'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'];
  var WD = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN'];
  var wrap, st = { v: 'day', y: 0, m: 0, sel: '', focus: '', input: null, min: '', max: '' };

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function iso(y, m, d) { var t = new Date(y, m, d); return t.getFullYear() + '-' + pad(t.getMonth() + 1) + '-' + pad(t.getDate()); }
  function parse(s) { var p = (s || '').split('-'); return p.length === 3 ? { y: +p[0], m: p[1] - 1, d: +p[2] } : null; }
  function fmt(s) { var p = parse(s); return pad(p.d) + '/' + pad(p.m + 1) + '/' + p.y; }
  function today() {
    var t = document.querySelector('[data-arg-today]'), s = t && t.getAttribute('data-arg-today');
    if (s) return s;
    var n = new Date(); return iso(n.getFullYear(), n.getMonth(), n.getDate());
  }
  function ok(s) { return (!st.min || s >= st.min) && (!st.max || s <= st.max); }
  function clamp(s) { return st.min && s < st.min ? st.min : st.max && s > st.max ? st.max : s; }
  function $(sel) { return ARG.$(sel, wrap); }

  function render() {
    var t = today(), h = '', title = $('.arg-datepicker__title span');
    if (st.v === 'day') {
      title.textContent = MN[st.m] + ', ' + st.y;
      var lead = (new Date(st.y, st.m, 1).getDay() + 6) % 7, n = new Date(st.y, st.m + 1, 0).getDate();
      for (var i = 0; i < lead; i++) h += '<span></span>';
      for (var d = 1; d <= n; d++) {
        var s = iso(st.y, st.m, d);
        h += '<button class="arg-datepicker__day" type="button" data-dp-day="' + s + '" tabindex="' + (s === st.focus ? 0 : -1) + '" aria-label="' + d + ' ' + MN[st.m].toLowerCase() + ', ' + st.y + '"' +
          (s === st.sel ? ' aria-pressed="true"' : ' aria-pressed="false"') + (s === t ? ' aria-current="date"' : '') + (ok(s) ? '' : ' disabled') + '>' + d + '</button>';
      }
      $('.arg-datepicker__wd').hidden = false;
      $('.arg-datepicker__grid').className = 'arg-datepicker__grid';
    } else {
      title.textContent = String(st.y);
      var tp = parse(t), sp = parse(st.sel);
      for (var k = 0; k < 12; k++) {
        var on = sp && sp.y === st.y && sp.m === k, enabled = ok(iso(st.y, k, 1)) || ok(iso(st.y, k, new Date(st.y, k + 1, 0).getDate()));
        h += '<button class="arg-datepicker__month" type="button" data-dp-month="' + k + '" aria-pressed="' + !!on + '"' + (tp.y === st.y && tp.m === k ? ' aria-current="date"' : '') + (enabled ? '' : ' disabled') + '>Th' + (k + 1) + '</button>';
      }
      $('.arg-datepicker__wd').hidden = true;
      $('.arg-datepicker__grid').className = 'arg-datepicker__grid arg-datepicker__grid--month';
    }
    $('.arg-datepicker__grid').innerHTML = h;
    $('[data-dp-ok]').disabled = !st.sel || !ok(st.sel);
    $('[data-dp-today]').disabled = !ok(t);
    $('[data-dp-prev]').disabled = st.v === 'day' ? !!st.min && iso(st.y, st.m, 1) <= st.min : !!st.min && st.y <= +st.min.slice(0, 4);
    $('[data-dp-next]').disabled = st.v === 'day' ? !!st.max && iso(st.y, st.m + 1, 1) > st.max : !!st.max && st.y >= +st.max.slice(0, 4);
  }
  function focusDay() { var b = $('[data-dp-day][tabindex="0"]') || $('[data-dp-month]:not(:disabled)'); if (b) b.focus(); }
  function go(delta) {   // đổi tháng (ngày) hoặc năm (tháng), giữ ngày đang chọn tiêu điểm nếu còn
    if (st.v === 'day') {
      var f = parse(st.focus), n = new Date(st.y, st.m + delta, 1);
      st.y = n.getFullYear(); st.m = n.getMonth();
      st.focus = clamp(iso(st.y, st.m, Math.min(f.d, new Date(st.y, st.m + 1, 0).getDate())));
      var q = parse(st.focus); st.y = q.y; st.m = q.m;
    } else st.y += delta;
    render();
  }
  function build() {
    wrap = document.createElement('div'); wrap.className = 'arg-offcanvas-wrap'; wrap.id = 'arg-dp'; wrap.hidden = true; wrap.setAttribute('data-arg-offcanvas', '');
    wrap.innerHTML = '<aside class="arg-offcanvas arg-offcanvas--bottom arg-datepicker" role="dialog" aria-modal="true" aria-labelledby="arg-dp-t">' +
      '<div class="arg-modal__header"><h4 class="arg-modal__title" id="arg-dp-t">Chọn ngày</h4><button class="arg-icon-btn" type="button" data-arg-close aria-label="Đóng">' + ARG.icon('x', 'i--20') + '</button></div>' +
      '<div class="arg-datepicker__body"><div class="arg-datepicker__nav"><button type="button" data-dp-prev aria-label="Tháng trước">' + ARG.icon('caret-left') + '</button>' +
      '<button class="arg-datepicker__title" type="button" aria-live="polite"><span></span>' + ARG.icon('caret-down') + '</button><button type="button" data-dp-next aria-label="Tháng sau">' + ARG.icon('caret-right') + '</button></div>' +
      '<div class="arg-datepicker__wd" aria-hidden="true">' + WD.map(function (w) { return '<span>' + w + '</span>'; }).join('') + '</div><div class="arg-datepicker__grid" role="group"></div></div>' +
      '<div class="arg-modal__footer arg-datepicker__foot"><button class="arg-btn arg-btn--text arg-datepicker__today" type="button" data-dp-today>Hôm nay</button>' +
      '<button class="arg-btn arg-btn--tertiary" type="button" data-arg-close>Huỷ</button><button class="arg-btn arg-btn--primary" type="button" data-dp-ok>Chọn</button></div></aside>';
    (document.querySelector('.arg-page') || document.body).appendChild(wrap);
    wrap.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b || b.disabled) return;
      if (b.hasAttribute('data-dp-prev')) go(-1);
      else if (b.hasAttribute('data-dp-next')) go(1);
      else if (b.classList.contains('arg-datepicker__title')) { st.v = st.v === 'day' ? 'month' : 'day'; render(); focusDay(); }
      else if (b.hasAttribute('data-dp-day')) { st.sel = st.focus = b.getAttribute('data-dp-day'); render(); focusDay(); }
      else if (b.hasAttribute('data-dp-month')) {
        st.m = +b.getAttribute('data-dp-month'); st.v = 'day';
        var f = parse(st.focus); st.focus = clamp(iso(st.y, st.m, Math.min(f.d, new Date(st.y, st.m + 1, 0).getDate()))); var q = parse(st.focus); st.y = q.y; st.m = q.m; render(); focusDay();
      } else if (b.hasAttribute('data-dp-today')) { var t = today(), p = parse(t); st.sel = st.focus = t; st.y = p.y; st.m = p.m; st.v = 'day'; render(); focusDay(); }
      else if (b.hasAttribute('data-dp-ok')) {
        var inp = st.input; inp.value = fmt(st.sel); inp.dataset.iso = st.sel;
        inp.dispatchEvent(new Event('change', { bubbles: true }));
        inp.dispatchEvent(new CustomEvent('arg:date', { bubbles: true, detail: { iso: st.sel } }));
        ARG.closeLayer(wrap);
      }
    });
    wrap.addEventListener('keydown', function (e) {
      var d = e.target.closest && e.target.closest('[data-dp-day]'); if (!d) return;
      var f = parse(st.focus), step = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 }[e.key], nx;
      if (step) nx = iso(f.y, f.m, f.d + step);
      else if (e.key === 'PageUp' || e.key === 'PageDown') nx = iso(f.y, f.m + (e.key === 'PageUp' ? -1 : 1), f.d);
      else return;
      e.preventDefault();
      if (!ok(nx)) return;
      var p = parse(nx); st.focus = nx; st.y = p.y; st.m = p.m; render(); focusDay();
    });
  }
  function open(input) {
    if (!wrap) build();
    st.input = input; st.v = 'day'; st.min = input.dataset.min || ''; st.max = input.dataset.max || ''; st.sel = input.dataset.iso || '';
    st.focus = clamp(st.sel || today()); var p = parse(st.focus); st.y = p.y; st.m = p.m;
    render(); ARG.openLayer(wrap, input);
    setTimeout(focusDay, 60);
  }

  ARG.register('datepicker', function (root) {
    ARG.$$('input[data-arg-datepicker]', root).forEach(function (inp) {
      if (!ARG.once(inp, 'datepicker')) return;
      inp.readOnly = true; inp.setAttribute('aria-haspopup', 'dialog');
      var box = inp.closest('.arg-control') || inp;
      box.addEventListener('click', function () { if (!inp.disabled) open(inp); });
      inp.addEventListener('keydown', function (e) { if ((e.key === 'Enter' || e.key === ' ') && !inp.disabled) { e.preventDefault(); open(inp); } });
    });
  });
})();
