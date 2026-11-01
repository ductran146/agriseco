/* ARG UI screen: [data-arg-screen="id"] là một màn hình; [data-arg-go="id"] mở màn đó; [data-arg-back] quay lại màn trước; thêm data-arg-root cho mục điều hướng gốc (thanh tab): xoá ngăn xếp, chuyển bằng hiệu ứng mờ.
   Bắn "arg:screen" ({ id, direction }). Màn đầu tiên không có thuộc tính hidden là màn khởi đầu. */
(function () {
  'use strict';
  var stack = [];
  function show(id, dir) {
    var next = ARG.$('[data-arg-screen="' + id + '"]');
    if (!next) return;
    ARG.$$('[data-arg-screen]').forEach(function (s) { s.hidden = s !== next; s.classList.remove('arg-screen--in-fwd', 'arg-screen--in-back', 'arg-screen--in-fade'); });
    window.scrollTo(0, 0);
    void next.offsetWidth;
    next.classList.add(dir === 'back' ? 'arg-screen--in-back' : dir === 'root' ? 'arg-screen--in-fade' : 'arg-screen--in-fwd');
    next.dispatchEvent(new CustomEvent('arg:screen', { bubbles: true, detail: { id: id, direction: dir } }));
  }
  document.addEventListener('click', function (e) {
    var go = e.target.closest('[data-arg-go]');
    if (go) {
      e.preventDefault();
      if (go.hasAttribute('data-arg-root')) { stack.length = 0; show(go.getAttribute('data-arg-go'), 'root'); return; }
      var cur = go.closest('[data-arg-screen]');
      if (cur) stack.push(cur.getAttribute('data-arg-screen'));
      show(go.getAttribute('data-arg-go'), 'fwd');
      return;
    }
    if (e.target.closest('[data-arg-back]')) { e.preventDefault(); var prev = stack.pop(); if (prev) show(prev, 'back'); }
  });
})();
