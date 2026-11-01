/* ARG UI chart: [data-arg-chart] > .arg-chart__plot[data-candles][data-base][data-date].
   Đường gióng ngang dọc, nhãn giá và tooltip chỉ hiện khi rê chuột, hoặc khi chạm giữ (~250ms) rồi kéo trên cảm ứng.
   Đường dọc bám theo nến gần nhất, đường ngang theo đúng điểm chạm. Thả tay hoặc rời chuột thì ẩn. */
(function () {
  'use strict';
  function fmt(x, d) {
    var s = Math.abs(x).toFixed(d).split('.');
    s[0] = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return (x < 0 ? '-' : '') + s.join(',');
  }
  ARG.register('chart', function (root) {
    ARG.$$('[data-arg-chart]', root).forEach(function (chart) {
      if (!ARG.once(chart, 'chart')) return;
      var plot = ARG.$('.arg-chart__plot', chart), price = ARG.$('.arg-chart__price', chart);
      var tip = ARG.$('.arg-chart__tip', chart), tag = ARG.$('.arg-chart__tag', chart), dot = ARG.$('.arg-chart__dot', chart);
      var lx = ARG.$$('.cur--x', chart), ly = ARG.$('.cur--y', chart);
      var candles = JSON.parse(plot.dataset.candles), base = +plot.dataset.base, date = plot.dataset.date, n = candles.length;
      var vb = price.viewBox.baseVal, timer = null, pressed = false, sx0 = 0, sy0 = 0, last = null;
      /* Tuỳ chọn trên __plot (mặc định theo chỉ số): data-span biên độ giá so với base (0,03), data-vol hệ số khối lượng (274),
         data-vol-unit đơn vị khối lượng (tr), data-start / data-end phút đầu và cuối trong ngày của nến (540 = 09:00, 885 = 14:45) */
      var d = plot.dataset, span = +(d.span || 0.03), vs = +(d.vol || 274), vu = d.volUnit || 'tr', t0 = +(d.start || 540), t1 = +(d.end || 885);
      var pv = function (t) { return base * (1 - span / 2 + t * span); };

      function show(cx, cy) {
        last = [cx, cy];
        var r = price.getBoundingClientRect(), p = plot.getBoundingClientRect();
        var x = Math.max(0, Math.min(r.width, cx - r.left)), y = Math.max(0, Math.min(r.height, cy - r.top));
        var i = Math.min(n - 1, Math.floor(x / r.width * n)), c = candles[i];
        var vx = (i + 0.5) / n * vb.width, vy = y / r.height * vb.height;
        lx.forEach(function (l) { l.setAttribute('x1', vx); l.setAttribute('x2', vx); });
        ly.setAttribute('y1', vy); ly.setAttribute('y2', vy);
        tag.textContent = fmt(pv(1 - y / r.height), 2);
        tag.style.top = (r.top - p.top + y) + 'px';
        var m = t0 + Math.round(i * (t1 - t0) / (n - 1)), o = pv(c[0]), cl = pv(c[3]), ch = (cl - o) / o * 100;
        var cls = ch >= 0 ? 'arg-up' : 'arg-down', line = chart.classList.contains('arg-chart--line'), hm = ('0' + Math.floor(m / 60)).slice(-2) + ':' + ('0' + m % 60).slice(-2);
        if (line) {
          tip.innerHTML = '<div class="arg-chart__tip--line"><span>' + date + ' · ' + hm + '</span><b>' + fmt(cl, 2) + '</b></div>';
          var dy = (1 - c[3]) * r.height;
          dot.style.left = (r.left - p.left + vx / vb.width * r.width) + 'px'; dot.style.top = (r.top - p.top + dy) + 'px'; dot.hidden = false;
        } else {
          dot.hidden = true;
          tip.innerHTML = '<b>' + date + ' · ' + ('0' + Math.floor(m / 60)).slice(-2) + ':' + ('0' + m % 60).slice(-2) + '</b><dl>' +
          '<dt>Mở cửa</dt><dd>' + fmt(o, 2) + '</dd><dt>Cao nhất</dt><dd class="arg-up">' + fmt(pv(c[1]), 2) + '</dd>' +
          '<dt>Đóng cửa</dt><dd>' + fmt(cl, 2) + '</dd><dt>Thấp nhất</dt><dd class="arg-down">' + fmt(pv(c[2]), 2) + '</dd>' +
          '<dt>KLGD</dt><dd>' + fmt(c[4] * vs, 1) + ' ' + vu + '</dd><dt>Thay đổi</dt><dd class="' + cls + '">' + (ch >= 0 ? '▲ +' : '▼ ') + fmt(ch, 2) + '%</dd></dl>';
        }
        chart.classList.add('is-active'); tip.hidden = false; tag.hidden = false;
        var px = r.left - p.left + vx / vb.width * r.width, w = tip.offsetWidth;
        tip.style.left = Math.max(0, Math.min(p.width - w, line ? px - w / 2 : (px + 12 + w > p.width ? px - w - 12 : px + 12))) + 'px';
      }
      function hide() { chart.classList.remove('is-active'); tip.hidden = true; tag.hidden = true; dot.hidden = true; }

      var mode = ARG.$('[data-arg-chart-mode]', chart);
      if (mode) mode.addEventListener('click', function () {
        var line = chart.classList.toggle('arg-chart--line');
        mode.innerHTML = ARG.icon(line ? 'candlestick' : 'wave-sine', 'i--24');
        mode.setAttribute('aria-label', line ? 'Chuyển sang biểu đồ nến' : 'Chuyển sang biểu đồ đường');
        mode.setAttribute('aria-pressed', String(line));
        hide();
      });

      plot.addEventListener('pointermove', function (e) {
        if (e.pointerType === 'mouse') { show(e.clientX, e.clientY); return; }
        if (pressed) show(e.clientX, e.clientY);
        else if (timer && Math.hypot(e.clientX - sx0, e.clientY - sy0) > 8) { clearTimeout(timer); timer = null; }
      });
      plot.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') hide(); });
      plot.addEventListener('pointerdown', function (e) {
        if (e.pointerType === 'mouse') return;
        sx0 = e.clientX; sy0 = e.clientY;
        timer = setTimeout(function () { timer = null; pressed = true; show(sx0, sy0); }, 250);
      });
      function end() { clearTimeout(timer); timer = null; if (pressed) { pressed = false; hide(); } }
      plot.addEventListener('pointerup', end); plot.addEventListener('pointercancel', end);
      plot.addEventListener('touchmove', function (e) { if (pressed) e.preventDefault(); }, { passive: false });
      plot.addEventListener('contextmenu', function (e) { e.preventDefault(); });
    });
  });
})();
