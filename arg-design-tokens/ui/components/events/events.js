/* ARG UI events: [data-arg-events] lọc các thẻ [data-date="YYYY-MM-DD"] theo hai ô ngày [data-arg-events-from], [data-arg-events-to].
   Hai ô ngày là Datepicker (input[data-arg-datepicker], giá trị chuẩn ở data-iso); ô Đến ngày không chọn trước Từ ngày và ngược lại.
   Cập nhật [data-arg-events-count="all"|"dividend"|"week"] (sự kiện trong khoảng; loại cổ tức data-type="dividend"; trong tuần data-week-start..data-week-end)
   và hiện [data-arg-events-empty] khi không còn thẻ nào. Bắn "arg:filter" ({ shown }). */
(function () {
  'use strict';
  ARG.register('events', function (root) {
    ARG.$$('[data-arg-events]', root).forEach(function (box) {
      if (!ARG.once(box, 'events')) return;
      var from = ARG.$('[data-arg-events-from]', box), to = ARG.$('[data-arg-events-to]', box), empty = ARG.$('[data-arg-events-empty]', box);
      function val(el) { return el ? el.dataset.iso || '' : ''; }
      function run() {
        var f = val(from), t = val(to), ws = box.dataset.weekStart || '', we = box.dataset.weekEnd || '', c = { all: 0, dividend: 0, week: 0 };
        if (to) to.dataset.min = f;
        if (from) from.dataset.max = t;
        ARG.$$('[data-date]', box).forEach(function (it) {
          var d = it.dataset.date, ok = (!f || d >= f) && (!t || d <= t);
          it.hidden = !ok;
          if (!ok) return;
          c.all++;
          if (it.dataset.type === 'dividend') c.dividend++;
          if (ws && d >= ws && d <= we) c.week++;
        });
        ARG.$$('[data-arg-events-count]', box).forEach(function (el) { el.textContent = c[el.getAttribute('data-arg-events-count')]; });
        if (empty) empty.hidden = c.all > 0;
        box.dispatchEvent(new CustomEvent('arg:filter', { bubbles: true, detail: { shown: c.all } }));
      }
      box.addEventListener('change', run);
      run();
    });
  });
})();
