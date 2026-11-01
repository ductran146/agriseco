/* ARG UI book: [data-arg-book-center] là vùng cuộn nội bộ của chế độ danh sách; data-asks = số mức bán ở trên.
   Khi vùng hiện ra (khởi tạo, đổi tab), cuộn để ranh giới giữa mức bán và mức mua nằm giữa vùng nhìn. */
(function () {
  'use strict';
  function center(box) {
    if (!box.offsetParent) return;
    var row = ARG.$('.arg-book__li', box), n = +box.getAttribute('data-asks') || 0;
    if (!row) return;
    box.scrollTop = Math.max(0, n * row.offsetHeight - box.clientHeight / 2);
  }
  function all() { ARG.$$('[data-arg-book-center]').forEach(center); }
  document.addEventListener('arg:tab', function () { setTimeout(all); });
  document.addEventListener('arg:screen', function () { setTimeout(all); });
  ARG.register('book', all);
})();
