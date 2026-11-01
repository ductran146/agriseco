/* ARG UI suggest: vùng [data-arg-watch] (cũng là [data-arg-listbar-scope]) gồm
   - các khung [data-arg-pane] chứa ul danh sách; danh sách đang chọn theo select[data-arg-pane-select];
   - [data-arg-suggest]: khối gợi ý, tự hiện khi danh sách đang chọn trống; thẻ .arg-suggest__card có input checkbox value=mã;
   - nút [data-arg-suggest-add]: thêm các thẻ đã chọn vào danh sách, hiện số mã đã chọn trong [data-arg-count], tắt khi chưa chọn;
   - <template data-arg-row="MÃ">: dòng mẫu (li) để nhân bản khi thêm;
   - bảng thêm mã: ô tìm [data-arg-suggest-search] lọc các li[data-q]; nút [data-arg-add="MÃ"] thêm mã, tự tắt khi mã đã có trong danh sách;
   - tạo danh sách mới: xem khối [data-arg-newlist-*] bên dưới;
   - nút ngôi sao .arg-fav trong dòng: bấm thì bỏ mã khỏi danh sách; [data-arg-watch-clear]: xoá hết mã của danh sách đang chọn.
   Bắn "arg:rows" sau khi thêm dòng để Listbar giữ kiểu sắp xếp. */
(function () {
  'use strict';
  function plain(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd'); }
  ARG.register('suggest', function (root) {
    ARG.$$('[data-arg-watch]', root).forEach(function (w) {
      if (!ARG.once(w, 'suggest')) return;
      var sel = ARG.$('select[data-arg-pane-select]', w), box = ARG.$('[data-arg-suggest]', w), add = ARG.$('[data-arg-suggest-add]', w);
      var cards = ARG.$$('.arg-suggest__card input', w), found = ARG.$('[data-arg-suggest-none]', w);
      function list() { return ARG.$('[data-arg-pane="' + sel.value + '"] ul', w); }
      function has(code) { return !!ARG.$('li[data-code="' + code + '"]', list()); }
      function picked() { return cards.filter(function (c) { return c.checked; }); }
      function sheet() {
        ARG.$$('[data-arg-add]', w).forEach(function (b) { b.disabled = has(b.getAttribute('data-arg-add')); });
      }
      function sync() {
        box.hidden = list().children.length > 0;
        var n = picked().length, c = ARG.$('[data-arg-count]', add);
        add.disabled = n === 0;
        if (c) c.textContent = n ? ' (' + n + ')' : '';
        sheet();
      }
      function put(code) {
        var ul = list(), t = ARG.$('template[data-arg-row="' + code + '"]', w);
        if (!t || has(code)) return;
        var li = t.content.firstElementChild.cloneNode(true);
        li.dataset.added = '1';
        ul.appendChild(li);
        ARG.init(li);
        w.dispatchEvent(new CustomEvent('arg:rows', { bubbles: true }));
      }
      sel.addEventListener('change', sync);
      cards.forEach(function (c) { c.addEventListener('change', sync); });
      add.addEventListener('click', function () {
        picked().forEach(function (c) { put(c.value); c.checked = false; });
        sync();
      });
      w.addEventListener('click', function (e) {
        var fav = e.target.closest('.arg-fav'), a = e.target.closest('[data-arg-add]'), clr = e.target.closest('[data-arg-watch-clear]');
        if (fav && fav.closest('li')) { fav.closest('li').remove(); sync(); }
        else if (a) { put(a.getAttribute('data-arg-add')); sync(); }
        else if (clr) { list().innerHTML = ''; sync(); ARG.closeLayer(clr.closest('[data-arg-modal]')); }
      });
      var q = ARG.$('[data-arg-suggest-search]', w);
      if (q) q.addEventListener('input', function () {
        var v = plain(q.value.trim()), n = 0;
        ARG.$$('li[data-q]', w).forEach(function (li) { var ok = !v || li.getAttribute('data-q').indexOf(v) > -1; li.hidden = !ok; if (ok) n++; });
        if (found) found.hidden = n > 0;
      });
      /* Tạo danh sách mới: sheet [data-arg-newlist-input] + [data-arg-newlist-ok] (bật khi đã nhập tên); thêm option vào select, khung [data-arg-pane] từ <template data-arg-pane-tpl>, chọn danh sách mới, báo toast. */
      var nin = ARG.$('[data-arg-newlist-input]', w), nok = ARG.$('[data-arg-newlist-ok]', w), ptpl = ARG.$('template[data-arg-pane-tpl]', w), seq = sel.options.length;
      if (nin && nok && ptpl) {
        nin.addEventListener('input', function () { nok.disabled = !nin.value.trim(); });
        nin.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !nok.disabled) nok.click(); });
        nok.addEventListener('click', function () {
          var name = nin.value.trim();
          if (!name) return;
          var v = 'w' + (seq++), o = document.createElement('option'), p = document.createElement('div');
          o.value = v; o.textContent = name; sel.appendChild(o);
          p.setAttribute('data-arg-pane', v); p.hidden = true; p.appendChild(ptpl.content.cloneNode(true));
          list().closest('[data-arg-pane]').parentNode.insertBefore(p, box);
          sel.value = v; sel.dispatchEvent(new Event('change', { bubbles: true }));
          ARG.closeLayer(nok.closest('[data-arg-offcanvas]'));
          if (ARG.toast) ARG.toast({ type: 'success', title: 'Đã tạo danh sách yêu thích', text: '' });
        });
        w.addEventListener('arg:open', function (e) { if (e.target.id === 'watch-new') { nin.value = ''; nok.disabled = true; } });
      }
      w.addEventListener('arg:open', sheet);
      sync();
    });
  });
})();
