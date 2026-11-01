/* ARG UI dragscroll: trên máy tính, bấm giữ chuột rồi kéo ngang để cuộn mọi dải cuộn ngang (thanh tab, chip, thẻ chỉ số, khuyến nghị...).
   Không cần gắn thuộc tính: tự tìm phần tử cha gần nhất đang cuộn ngang được (overflow-x auto hoặc scroll và nội dung dài hơn khung).
   Chỉ nghe chuột; cảm ứng đã vuốt được sẵn. Kéo quá 4px mới tính là kéo: bấm bình thường vẫn mở liên kết, chọn tab. Sau khi kéo, lần bấm kế tiếp bị nuốt
   để thả chuột không kích hoạt nút bên dưới. Tạm tắt scroll-snap trong lúc kéo; thả ra thì trả lại. Bỏ qua ô nhập, [data-arg-nodrag]. */
(function () {
  'use strict';
  var THRESHOLD = 4;
  var scroller = function (el) {
    for (; el && el !== document.documentElement; el = el.parentElement) {
      if (el.hasAttribute && el.hasAttribute('data-arg-nodrag')) return null;
      var ox = getComputedStyle(el).overflowX;
      if ((ox === 'auto' || ox === 'scroll') && el.scrollWidth > el.clientWidth + 1) return el;
    }
    return null;
  };
  var st = null; /* { el, x, left, snap, moved } */
  document.addEventListener('mouseover', function (e) {
    var s = scroller(e.target);
    if (s && !s.hasAttribute('data-arg-dragscroll')) s.setAttribute('data-arg-dragscroll', '');
  });
  document.addEventListener('mousedown', function (e) {
    if (e.button !== 0 || /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
    var s = scroller(e.target);
    if (!s) return;
    st = { el: s, x: e.clientX, left: s.scrollLeft, snap: s.style.scrollSnapType, moved: false };
  });
  document.addEventListener('mousemove', function (e) {
    if (!st) return;
    var dx = e.clientX - st.x;
    if (!st.moved) {
      if (Math.abs(dx) < THRESHOLD) return;
      st.moved = true;
      st.el.style.scrollSnapType = 'none';
      st.el.classList.add('is-dragging');
      var sel = window.getSelection && window.getSelection(); if (sel) sel.removeAllRanges();
    }
    st.el.scrollLeft = st.left - dx;
    e.preventDefault();
  });
  var end = function () {
    if (!st) return;
    var s = st; st = null;
    if (!s.moved) return;
    s.el.classList.remove('is-dragging');
    s.el.style.scrollSnapType = s.snap;
    var eat = function (ev) { ev.stopPropagation(); ev.preventDefault(); };
    document.addEventListener('click', eat, true);
    setTimeout(function () { document.removeEventListener('click', eat, true); }, 0);
    s.el.dispatchEvent(new CustomEvent('arg:dragscroll', { bubbles: true, detail: { left: s.el.scrollLeft } }));
  };
  document.addEventListener('mouseup', end);
  document.addEventListener('dragstart', function (e) { if (st) e.preventDefault(); });
})();
