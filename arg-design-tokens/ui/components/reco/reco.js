/* ARG UI reco: button.arg-reco__sort sắp xếp các dòng .arg-reco__item theo [data-pl] trong cùng thẻ. Bắn "arg:sort". */
(function () {
  'use strict';
  ARG.register('reco', function (root) {
    ARG.$$('.arg-reco__sort', root).forEach(function (btn) {
      if (!ARG.once(btn, 'reco-sort')) return;
      btn.addEventListener('click', function () {
        var card = btn.closest('.arg-reco');
        var body = ARG.$('.arg-reco__body', card);
        var dir = btn.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending';
        var rows = ARG.$$('.arg-reco__item', body);
        rows.sort(function (a, b) { return (parseFloat(a.dataset.pl) - parseFloat(b.dataset.pl)) * (dir === 'ascending' ? 1 : -1); });
        rows.forEach(function (r) { body.appendChild(r); });
        btn.setAttribute('aria-sort', dir);
        card.dispatchEvent(new CustomEvent('arg:sort', { bubbles: true, detail: { direction: dir } }));
      });
    });
  });
})();
