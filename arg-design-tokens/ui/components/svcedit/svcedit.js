/* ARG UI svcedit: màn [data-arg-svcedit] (Tuỳ chỉnh dịch vụ nhanh). data-arg-catalog là JSON { id: { id, label, icon } }, data-max là số dịch vụ tối đa.
   - Lựa chọn ban đầu lấy từ sessionStorage "arg-services" (mảng id theo thứ tự), không có thì theo thẻ đang vẽ sẵn.
   - [data-svc-remove] bỏ một dịch vụ; [data-svc-add] thêm vào cuối (tắt khi đủ tối đa); kéo thẻ đổi vị trí (Reorder dạng lưới, sự kiện arg:reorder).
   - [data-svc-save] lưu thứ tự vào sessionStorage, đặt cờ "arg-services-saved" để Trang chủ báo toast, rồi quay lại. Lưu: ghi đè hoàn toàn danh sách. */
(function () {
  'use strict';
  var KEY = 'arg-services', FLAG = 'arg-services-saved';
  function read() { try { var v = JSON.parse(sessionStorage.getItem(KEY)); return Array.isArray(v) ? v : null; } catch (e) { return null; } }
  ARG.register('svcedit', function (root) {
    ARG.$$('[data-arg-svcedit]', root).forEach(function (scr) {
      if (!ARG.once(scr, 'svcedit')) return;
      var cat = {}, max = +scr.getAttribute('data-max') || 6, grid = ARG.$('.arg-svcedit__grid', scr), cnt = ARG.$('[data-svc-count]', scr), empty = ARG.$('[data-svc-empty]', scr);
      try { cat = JSON.parse(scr.getAttribute('data-arg-catalog')); } catch (e) {}
      var fav = read() || ARG.$$('.arg-svcedit__tile', grid).map(function (t) { return t.getAttribute('data-id'); });
      fav = fav.filter(function (id) { return cat[id]; });
      function tile(d) {
        return '<li class="arg-svcedit__tile" data-id="' + d.id + '"><button class="arg-svcedit__remove" type="button" data-svc-remove aria-label="Bỏ ' + d.label + ' khỏi dịch vụ nhanh">' + ARG.icon('minus') + '</button>' +
          '<span class="arg-service__icon">' + ARG.icon(d.icon) + '</span><span class="arg-service__label">' + d.label + '</span></li>';
      }
      function render() {
        grid.innerHTML = fav.map(function (id) { return tile(cat[id]); }).join('');
        ARG.init(grid);
        if (cnt) cnt.textContent = fav.length;
        if (empty) empty.hidden = fav.length > 0;
        ARG.$$('.arg-svcedit__row', scr).forEach(function (row) {
          var id = row.getAttribute('data-id'), on = fav.indexOf(id) >= 0, b = ARG.$('.arg-svcedit__add', row);
          if (on && b) b.remove();
          if (!on) {
            if (!b) { row.insertAdjacentHTML('beforeend', '<button class="arg-svcedit__add" type="button" data-svc-add aria-label="Thêm ' + cat[id].label + ' vào dịch vụ nhanh">' + ARG.icon('plus-circle') + '</button>'); ARG.init(row); b = ARG.$('.arg-svcedit__add', row); }
            b.disabled = fav.length >= max;
          }
        });
      }
      scr.addEventListener('click', function (e) {
        var rm = e.target.closest('[data-svc-remove]'), ad = e.target.closest('[data-svc-add]'), sv = e.target.closest('[data-svc-save]');
        if (rm) { var id = rm.closest('li').getAttribute('data-id'); fav = fav.filter(function (x) { return x !== id; }); render(); }
        else if (ad && !ad.disabled && fav.length < max) { fav.push(ad.closest('li').getAttribute('data-id')); render(); }
        else if (sv) {
          try { sessionStorage.setItem(KEY, JSON.stringify(fav)); sessionStorage.setItem(FLAG, '1'); } catch (x) {}
          scr.dispatchEvent(new CustomEvent('arg:services', { bubbles: true, detail: { ids: fav.slice() } }));
          var back = ARG.$('[data-arg-back]', scr); if (back) back.click();
        }
      });
      grid.addEventListener('arg:reorder', function () { fav = ARG.$$('.arg-svcedit__tile', grid).map(function (t) { return t.getAttribute('data-id'); }); });
      render();
    });
  });
})();
