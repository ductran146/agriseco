/* ARG UI search: màn hình [data-arg-search].
   - Ô [data-arg-search-input]: rỗng thì hiện [data-arg-search-recent] (tìm gần đây), có chữ thì hiện [data-arg-search-results] đã lọc theo mã hoặc tên (không phân biệt hoa thường, bỏ dấu), mã bắt đầu bằng chữ gõ xếp trước. [data-arg-search-none] hiện khi không có kết quả.
   - [data-arg-search-clear] xoá chữ trong ô và đặt con trỏ lại ô (chỉ hiện khi ô có chữ).
   - Dòng tìm gần đây [data-arg-search-pick="MÃ"]: bấm điền mã vào ô. [data-arg-search-remove] xoá một dòng, [data-arg-search-clear-all] xoá cả danh sách (hiện [data-arg-search-empty] và ẩn nút xoá).
   - Mở màn thì tự đặt con trỏ vào ô (bàn phím mô phỏng trượt lên). Sao yêu thích do Appbar xử lý (data-arg-fav-toggle). Bắn "arg:search" ({ q, count }) khi lọc. */
(function () {
  'use strict';
  function fold(t) { return t.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd').toLowerCase(); }
  function rank(li, q) {
    var code = li.getAttribute('data-code').toLowerCase(), name = li.getAttribute('data-q');
    if (code.indexOf(q) === 0) return 0;
    if (code.indexOf(q) > 0) return 1;
    return name.indexOf(q) >= 0 ? 2 : 3;
  }
  function apply(root) {
    var input = ARG.$('[data-arg-search-input]', root), q = fold(input.value.trim()), list = ARG.$('[data-arg-search-results]', root), n = 0;
    ARG.$$('[data-arg-search-clear]', root).forEach(function (b) { b.hidden = !input.value; });
    ARG.$('[data-arg-search-recent]', root).hidden = !!q;
    list.hidden = !q;
    if (q) {
      var rows = ARG.$$('li', list).map(function (li) { return { li: li, r: rank(li, q) }; });
      rows.sort(function (a, b) { return a.r - b.r || a.li.getAttribute('data-code').localeCompare(b.li.getAttribute('data-code')); });
      rows.forEach(function (x) { x.li.hidden = x.r > 2; if (!x.li.hidden) n++; list.appendChild(x.li); });
    }
    ARG.$('[data-arg-search-none]', root).hidden = !q || n > 0;
    root.dispatchEvent(new CustomEvent('arg:search', { bubbles: true, detail: { q: input.value.trim(), count: n } }));
  }
  function recentSync(root) {
    var left = ARG.$$('[data-arg-search-recent] .arg-search__row', root).length;
    ARG.$('[data-arg-search-empty]', root).hidden = left > 0;
    ARG.$$('[data-arg-search-clear-all]', root).forEach(function (b) { b.hidden = left === 0; });
  }
  ARG.register('search', function (scope) {
    ARG.$$('[data-arg-search]', scope).forEach(function (root) {
      if (!ARG.once(root, 'search')) return;
      var input = ARG.$('[data-arg-search-input]', root);
      apply(root); recentSync(root);
      if (root.classList.contains('arg-screen') && !root.hidden) setTimeout(function () { input.focus(); }, 0);
    });
  });
  document.addEventListener('arg:screen', function (e) {
    var root = document.querySelector('[data-arg-search]:not([hidden])');
    if (root && e.detail && e.detail.id === root.getAttribute('data-arg-screen')) ARG.$('[data-arg-search-input]', root).focus();
  });
  document.addEventListener('input', function (e) {
    var root = e.target.closest('[data-arg-search]');
    if (root && e.target.matches('[data-arg-search-input]')) apply(root);
  });
  document.addEventListener('click', function (e) {
    var root = e.target.closest('[data-arg-search]'); if (!root) return;
    var input = ARG.$('[data-arg-search-input]', root), t;
    if ((t = e.target.closest('[data-arg-search-clear]'))) { input.value = ''; apply(root); input.focus(); }
    else if ((t = e.target.closest('[data-arg-search-pick]'))) { input.value = t.getAttribute('data-arg-search-pick'); apply(root); input.focus(); }
    else if ((t = e.target.closest('[data-arg-search-remove]'))) { t.closest('.arg-search__row').remove(); recentSync(root); }
    else if (e.target.closest('[data-arg-search-clear-all]')) { ARG.$$('[data-arg-search-recent] .arg-search__row', root).forEach(function (li) { li.remove(); }); recentSync(root); }
  });
})();
