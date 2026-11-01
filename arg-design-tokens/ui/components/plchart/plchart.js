/* ARG UI plchart: vùng [data-arg-plchart] mang data-points (mảng lãi/lỗ luỹ kế, đồng), data-dates (nhãn ngày cùng độ dài), data-min và data-max (đồng, khớp trục dọc của SVG).
   Đường gióng, chấm và tooltip chỉ hiện khi rê chuột, hoặc chạm giữ khoảng 250ms rồi kéo; vuốt nhanh vẫn cuộn trang. Bắn "arg:plchart" ({ index }). */
(function () {
  'use strict';
  function vnd(v) { var s = Math.abs(Math.round(v)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.'); return (v > 0 ? '+' : v < 0 ? '-' : '') + s; }
  ARG.register('plchart', function (scope) {
    ARG.$$('[data-arg-plchart]', scope).forEach(function (plot) {
      if (!ARG.once(plot, 'plchart')) return;
      var pts = JSON.parse(plot.getAttribute('data-points')), dates = JSON.parse(plot.getAttribute('data-dates'));
      var lo = parseFloat(plot.getAttribute('data-min')), hi = parseFloat(plot.getAttribute('data-max'));
      var dot = ARG.$('.arg-plchart__dot', plot), tip = ARG.$('.arg-plchart__tip', plot), timer = null, held = false;
      function show(clientX) {
        var r = plot.getBoundingClientRect(), t = Math.min(1, Math.max(0, (clientX - r.left) / r.width)), i = Math.round(t * (pts.length - 1)), v = pts[i];
        var x = i / (pts.length - 1) * 100, y = (hi - v) / (hi - lo) * 100, up = v >= 0;
        plot.style.setProperty('--x', x); plot.style.setProperty('--y', y);
        plot.style.setProperty('--tx', x < 25 ? '0%' : x > 75 ? '-100%' : '-50%');
        dot.style.setProperty('--c', up ? 'var(--arg-trading-up-light-increase)' : 'var(--arg-trading-down-light-increase)');
        tip.innerHTML = '<span>' + dates[i] + '</span><span>Lãi/lỗ luỹ kế: <b class="' + (up ? 'arg-up' : 'arg-down') + '">' + vnd(v) + '</b></span>';
        plot.classList.add('is-active');
        plot.dispatchEvent(new CustomEvent('arg:plchart', { bubbles: true, detail: { index: i } }));
      }
      function hide() { plot.classList.remove('is-active'); held = false; clearTimeout(timer); }
      plot.addEventListener('pointermove', function (e) { if (e.pointerType === 'mouse' || held) show(e.clientX); });
      plot.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') hide(); });
      plot.addEventListener('pointerdown', function (e) {
        if (e.pointerType === 'mouse') return;
        var x = e.clientX; timer = setTimeout(function () { held = true; plot.style.touchAction = 'none'; show(x); }, 250);
      });
      ['pointerup', 'pointercancel'].forEach(function (n) { plot.addEventListener(n, function (e) { if (e.pointerType !== 'mouse') { plot.style.touchAction = ''; hide(); } }); });
    });
  });
})();
