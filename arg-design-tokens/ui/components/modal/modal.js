/* ARG UI modal + offcanvas (shared layer handling).
   Open:  [data-arg-open="layerId"]   Layer: .arg-overlay[data-arg-modal] or .arg-offcanvas-wrap[data-arg-offcanvas]
   Close: [data-arg-close], Esc, or a click on the backdrop. Focus is trapped inside and returned to the opener.
   API: ARG.openLayer(el), ARG.closeLayer(el). Khi mở, focus vào phần tử [data-arg-autofocus] (nếu có), không thì phần tử nhập đầu tiên. Fires "arg:open" / "arg:close". */
(function () {
  'use strict';
  var lastOpener = null;
  var SEL = '[data-arg-modal], [data-arg-offcanvas]';

  ARG.openLayer = function (el, opener) {
    lastOpener = opener || document.activeElement;
    el.hidden = false;
    document.documentElement.style.overflow = 'hidden';
    requestAnimationFrame(function () { el.classList.add('is-open'); });
    var first = ARG.$('[data-arg-autofocus]', el) || ARG.$('input, select, textarea, button:not([data-arg-close]), [data-arg-close]', el);
    (first || el).focus();
    el.dispatchEvent(new CustomEvent('arg:open', { bubbles: true }));
  };
  ARG.closeLayer = function (el) {
    el.classList.remove('is-open');
    var done = function () {
      el.hidden = true;
      document.documentElement.style.overflow = '';
      if (lastOpener && lastOpener.focus) lastOpener.focus();
      el.dispatchEvent(new CustomEvent('arg:close', { bubbles: true }));
    };
    if (el.hasAttribute('data-arg-offcanvas') && !ARG.reducedMotion()) setTimeout(done, 240);
    else done();
  };

  /* Nhấn xuống trong hộp rồi nhả ra ngoài (ví dụ bàn phím mô phỏng đẩy hộp lên giữa lúc bấm) không được tính là bấm nền để đóng hộp. */
  var downIn = false;
  document.addEventListener('pointerdown', function (e) { downIn = !!e.target.closest('.arg-modal, .arg-offcanvas'); }, true);
  document.addEventListener('click', function (e) {
    var op = e.target.closest('[data-arg-open]');
    if (op) { ARG.openLayer(document.getElementById(op.getAttribute('data-arg-open')), op); return; }
    var layer = e.target.closest(SEL);
    if (!layer) return;
    var inside = e.target.closest('.arg-modal, .arg-offcanvas');
    if (e.target.closest('[data-arg-close]') || (!inside && !downIn)) ARG.closeLayer(layer);
  });
  document.addEventListener('keydown', function (e) {
    var layer = ARG.$$(SEL).filter(function (l) { return !l.hidden; })[0];
    if (!layer) return;
    if (e.key === 'Escape') { ARG.closeLayer(layer); return; }
    if (e.key !== 'Tab') return;
    var f = ARG.$$('button, input, select, textarea, [href]', layer).filter(function (x) { return !x.disabled && x.offsetParent !== null; });
    if (!f.length) return;
    var a = f[0], z = f[f.length - 1];
    if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
    else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
  });
})();
