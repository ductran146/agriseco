/* ARG UI progress: setProgress(el, value) and a stepper trigger.
   Trigger: <button data-arg-progress-step="#barId" data-arg-progress-label="#textId" data-step="15"> (wraps to 0 after 100). */
(function () {
  'use strict';
  ARG.setProgress = function (progress, value) {
    var v = Math.max(0, Math.min(100, Math.round(value)));
    var bar = ARG.$('.arg-progress__bar', progress);
    bar.style.setProperty('--v', v + '%');
    progress.setAttribute('aria-valuenow', String(v));
    return v;
  };
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-arg-progress-step]');
    if (!b) return;
    var pb = ARG.$(b.getAttribute('data-arg-progress-step'));
    var now = Number(pb.getAttribute('aria-valuenow')) || 0;
    var step = Number(b.getAttribute('data-step')) || 10;
    var v = ARG.setProgress(pb, now >= 100 ? 0 : now + step);
    var label = b.getAttribute('data-arg-progress-label');
    if (label) ARG.$(label).textContent = v + '%';
  });
})();
