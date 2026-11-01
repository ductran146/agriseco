/* ARG UI button: toggle state in .arg-btn-group (aria-pressed) and block disabled links. */
(function () {
  'use strict';
  document.addEventListener('click', function (e) {
    var disabled = e.target.closest('.arg-btn[aria-disabled="true"]');
    if (disabled) { e.preventDefault(); return; }
    var group = e.target.closest('.arg-btn-group');
    var btn = e.target.closest('.arg-btn-group .arg-btn');
    if (!group || !btn || !btn.hasAttribute('aria-pressed')) return;
    ARG.$$('.arg-btn', group).forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
    group.dispatchEvent(new CustomEvent('arg:change', { bubbles: true, detail: { button: btn } }));
  });
})();
