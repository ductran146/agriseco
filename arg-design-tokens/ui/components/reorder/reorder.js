/* ARG UI reorder: danh sách [data-arg-reorder] (ul) có dòng li chứa nút kéo [data-arg-handle]. Nhấn giữ nút rồi kéo lên xuống (chuột hoặc cảm ứng) để đổi thứ tự; dòng đang kéo nổi lên
   và bám theo con trỏ, các dòng khác nhường chỗ. Nút kéo cũng dùng được bằng bàn phím: mũi tên lên, xuống đổi một bậc. Sau khi thả, ghi lại thứ tự vào li.dataset.i
   (để kiểu sắp xếp "Mặc định" của Listbar nhận thứ tự mới). Bắn "arg:reorder" ({ code, index }) trên ul. */
(function () {
  'use strict';
  function items(ul) { return Array.prototype.slice.call(ul.children).filter(function (x) { return x.tagName === 'LI'; }); }
  function commit(ul, li) {
    var all = items(ul);
    all.forEach(function (x, i) { x.dataset.i = i; delete x.dataset.added; });
    ul.dispatchEvent(new CustomEvent('arg:reorder', { bubbles: true, detail: { code: li.getAttribute('data-code'), index: all.indexOf(li) } }));
  }
  var drag = null;
  document.addEventListener('pointerdown', function (e) {
    var h = e.target.closest('[data-arg-handle]');
    if (!h || (e.pointerType === 'mouse' && e.button !== 0)) return;
    var li = h.closest('li'), ul = li && li.closest('[data-arg-reorder]');
    if (!ul) return;
    e.preventDefault();
    var r = li.getBoundingClientRect();
    drag = { li: li, ul: ul, h: h, grab: e.clientY - r.top, id: e.pointerId };
    li.classList.add('is-dragging'); ul.classList.add('is-sorting');
    try { h.setPointerCapture(e.pointerId); } catch (x) {}
  });
  document.addEventListener('pointermove', function (e) {
    if (!drag || e.pointerId !== drag.id) return;
    var li = drag.li, y = e.clientY, prev, next, b;
    li.style.transform = '';
    for (;;) {
      prev = li.previousElementSibling; next = li.nextElementSibling;
      if (prev && prev.tagName === 'LI' && (b = prev.getBoundingClientRect()) && y < b.top + b.height / 2) { drag.ul.insertBefore(li, prev); continue; }
      if (next && next.tagName === 'LI' && (b = next.getBoundingClientRect()) && y > b.top + b.height / 2) { drag.ul.insertBefore(li, next.nextElementSibling); continue; }
      break;
    }
    li.style.transform = 'translateY(' + (y - drag.grab - li.getBoundingClientRect().top) + 'px)';
  });
  function end(e) {
    if (!drag || (e && e.pointerId !== drag.id)) return;
    var d = drag; drag = null;
    d.li.style.transform = ''; d.li.classList.remove('is-dragging'); d.ul.classList.remove('is-sorting');
    commit(d.ul, d.li);
  }
  document.addEventListener('pointerup', end); document.addEventListener('pointercancel', end);
  document.addEventListener('keydown', function (e) {
    var h = e.target.closest && e.target.closest('[data-arg-handle]');
    if (!h || (e.key !== 'ArrowUp' && e.key !== 'ArrowDown')) return;
    var li = h.closest('li'), ul = li.closest('[data-arg-reorder]');
    if (!ul) return;
    e.preventDefault();
    var sib = e.key === 'ArrowUp' ? li.previousElementSibling : li.nextElementSibling;
    if (!sib) return;
    ul.insertBefore(li, e.key === 'ArrowUp' ? sib : sib.nextElementSibling);
    h.focus(); commit(ul, li);
  });
})();
