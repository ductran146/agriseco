/* ARG UI service: lưới [data-arg-catalog] (Dịch vụ nhanh ở Trang chủ) được dựng lại theo lựa chọn đã lưu ở màn Tuỳ chỉnh dịch vụ nhanh
   (sessionStorage "arg-services": mảng id theo thứ tự; data-arg-catalog là JSON { id: { id, label, icon } }). Có cờ "arg-services-saved" thì báo toast một dòng rồi xoá cờ. */
(function () {
  'use strict';
  ARG.register('service', function (root) {
    ARG.$$('[data-arg-catalog]', root).forEach(function (grid) {
      if (grid.hasAttribute('data-arg-svcedit') || !ARG.once(grid, 'service')) return;
      var cat = {}, ids = null, saved = false;
      try { cat = JSON.parse(grid.getAttribute('data-arg-catalog')); ids = JSON.parse(sessionStorage.getItem('arg-services')); saved = sessionStorage.getItem('arg-services-saved') === '1'; } catch (e) {}
      if (Array.isArray(ids)) {
        var html = ids.filter(function (id) { return cat[id]; }).map(function (id) {
          var d = cat[id];
          return '<a class="arg-service" href="#" data-id="' + d.id + '"><span class="arg-service__icon">' + ARG.icon(d.icon) + '</span><span class="arg-service__label">' + d.label + '</span></a>';
        }).join('');
        grid.innerHTML = html || '<p class="arg-note" style="grid-column:1/-1;text-align:center">Chưa có dịch vụ nhanh. Bấm Tuỳ chỉnh để thêm.</p>';
        ARG.init(grid);
      }
      if (saved) {
        try { sessionStorage.removeItem('arg-services-saved'); } catch (e) {}
        setTimeout(function () { if (ARG.toast) ARG.toast({ type: 'success', title: 'Đã lưu dịch vụ nhanh', text: '' }); }, 350);
      }
    });
  });
})();
