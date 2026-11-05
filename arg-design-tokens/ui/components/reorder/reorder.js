/* ARG UI reorder: danh sách [data-arg-reorder] (ul) có dòng li chứa nút kéo [data-arg-handle]. Nhấn giữ nút rồi kéo lên xuống (chuột hoặc cảm ứng) để đổi thứ tự; dòng đang kéo nổi lên
   và bám theo con trỏ, các dòng khác nhường chỗ. Nút kéo cũng dùng được bằng bàn phím: mũi tên lên, xuống đổi một bậc. Sau khi thả, ghi lại thứ tự vào li.dataset.i
   (để kiểu sắp xếp "Mặc định" của Listbar nhận thứ tự mới). Dạng lưới: xem khối "Dạng lưới" bên dưới. Bắn "arg:reorder" ({ code, index }) trên ul. */
(function () {
  'use strict';
  function items(ul) { return Array.prototype.slice.call(ul.children).filter(function (x) { return x.tagName === 'LI' && !x.hasAttribute('data-fixed'); }); }
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
  /* Dạng lưới [data-arg-reorder="grid"]: cả thẻ li là nút kéo (không có nút kéo riêng). Chuột: kéo thẻ khi đã di chuyển quá 4px; cảm ứng: giữ khoảng 250ms rồi kéo (vuốt nhanh vẫn cuộn trang).
     Bản sao nổi (có bóng) bám theo con trỏ; thẻ thật ở lại làm ô giữ chỗ viền nét đứt, con trỏ vào thẻ nào thì ô giữ chỗ đổi chỗ tới vị trí đó. Nút bên trong thẻ (button) không bắt đầu kéo; ô có data-fixed (ví dụ ô trống) không kéo được và không nhận thẻ. */
  var gr = null, gTimer = 0, HOLD = 250;
  function gTarget(t) { var li = t.closest && t.closest('[data-arg-reorder="grid"] > li:not([data-fixed])'); return li && !t.closest('button, a') ? li : null; }
  function gBegin(li, x, y) {
    var r = li.getBoundingClientRect();
    gr = { li: li, ul: li.parentNode, gx: x - r.left, gy: y - r.top, x0: x, y0: y, on: false };
  }
  /* Thẻ thật ở lại trong lưới làm ô giữ chỗ (viền nét đứt, nội dung ẩn) cho thấy vị trí sẽ thả; một bản sao nổi (ghost, có bóng) bám theo con trỏ. */
  function gStart() {
    var li = gr.li, r = li.getBoundingClientRect(), g = li.cloneNode(true);
    gr.on = true; li.classList.add('is-placeholder'); gr.ul.classList.add('is-sorting');
    g.removeAttribute('id'); g.setAttribute('aria-hidden', 'true'); g.classList.add('arg-reorder__ghost');
    g.style.cssText = 'position:fixed;margin:0;left:' + r.left + 'px;top:' + r.top + 'px;width:' + r.width + 'px;height:' + r.height + 'px';
    document.body.appendChild(g); gr.ghost = g;
  }
  function gMove(x, y) {
    var li = gr.li, all = items(gr.ul), hit = null;
    all.forEach(function (o) { if (o !== li && !hit) { var b = o.getBoundingClientRect(); if (x >= b.left && x <= b.right && y >= b.top && y <= b.bottom) hit = o; } });
    if (hit) gr.ul.insertBefore(li, all.indexOf(hit) < all.indexOf(li) ? hit : hit.nextSibling);
    gr.ghost.style.left = x - gr.gx + 'px'; gr.ghost.style.top = y - gr.gy + 'px';
  }
  function gEnd() {
    clearTimeout(gTimer);
    if (!gr) return;
    var d = gr; gr = null;
    if (!d.on) return;
    d.ghost.remove(); d.li.classList.remove('is-placeholder'); d.ul.classList.remove('is-sorting');
    commit(d.ul, d.li);
  }
  document.addEventListener('mousedown', function (e) { var li = e.button === 0 && gTarget(e.target); if (li) gBegin(li, e.clientX, e.clientY); });
  document.addEventListener('mousemove', function (e) {
    if (!gr) return;
    if (!gr.on) { if (Math.abs(e.clientX - gr.x0) + Math.abs(e.clientY - gr.y0) > 4) gStart(); else return; }
    gMove(e.clientX, e.clientY);
  });
  document.addEventListener('mouseup', gEnd);
  document.addEventListener('touchstart', function (e) {
    var li = gTarget(e.target); if (!li) return;
    var t = e.touches[0]; gBegin(li, t.clientX, t.clientY);
    clearTimeout(gTimer); gTimer = setTimeout(function () { if (gr) { gStart(); gMove(gr.x0, gr.y0); } }, HOLD);
  }, { passive: true });
  document.addEventListener('touchmove', function (e) {
    if (!gr) return;
    var t = e.touches[0];
    if (gr.on) { e.preventDefault(); gMove(t.clientX, t.clientY); }
    else if (Math.abs(t.clientX - gr.x0) + Math.abs(t.clientY - gr.y0) > 8) { clearTimeout(gTimer); gr = null; }
  }, { passive: false });
  document.addEventListener('touchend', gEnd); document.addEventListener('touchcancel', gEnd);
  document.addEventListener('contextmenu', function (e) { if (gr && gr.on) e.preventDefault(); });

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
