/* ARG UI notification.
   Toast: ARG.toast({ type: 'success|error|warning|info', title, text, duration }) or a trigger [data-arg-toast="type"].
   List:  [data-arg-mark-read="#listId"] clears .is-unread and the .arg-count in the card header. */
(function () {
  'use strict';
  var KINDS = {
    success: ['check', 'var(--arg-action-noti-toast-success)', 'Thành công', 'Đã đặt lệnh mua 1.000 AGR giá 19,75.'],
    error: ['x', 'var(--arg-action-noti-toast-error)', 'Có lỗi xảy ra', 'Sức mua không đủ để đặt lệnh này.'],
    warning: ['warning', 'var(--arg-ui-label-strong-warning)', 'Cảnh báo', 'Phiên ATC sắp kết thúc trong 5 phút.'],
    info: ['info', 'var(--arg-ui-label-strong-blue)', 'Thông tin', 'Thị trường nghỉ giao dịch ngày 02/09.']
  };
  function box() {
    var b = ARG.$('.arg-toasts', ARG.root());
    if (!b) {
      b = document.createElement('div');
      b.className = 'arg-toasts';
      b.setAttribute('aria-live', 'polite');
      ARG.root().appendChild(b);
    }
    return b;
  }
  ARG.toast = function (opt) {
    opt = opt || {};
    var k = KINDS[opt.type] || KINDS.info;
    var t = document.createElement('div');
    t.className = 'arg-toast';
    t.setAttribute('role', opt.type === 'error' ? 'alert' : 'status');
    t.innerHTML = '<span class="arg-toast__icon" style="--c:' + k[1] + '">' + ARG.icon(k[0]) + '</span>' +
      '<div class="arg-toast__body"><span class="arg-toast__title"></span><span class="arg-toast__text"></span></div>' +
      '<button class="arg-icon-btn" type="button" aria-label="Đóng">' + ARG.icon('x', 'i--16') + '</button>';
    ARG.$('.arg-toast__title', t).textContent = opt.title || k[2];
    ARG.$('.arg-toast__text', t).textContent = opt.text || k[3];
    ARG.$('button', t).addEventListener('click', function () { t.remove(); });
    var b = box();
    b.appendChild(t);
    while (b.children.length > 4) b.firstChild.remove();
    setTimeout(function () { t.remove(); }, opt.duration || 4000);
    return t;
  };
  document.addEventListener('click', function (e) {
    var trg = e.target.closest('[data-arg-toast]');
    if (trg) ARG.toast({ type: trg.getAttribute('data-arg-toast') });
    var mr = e.target.closest('[data-arg-mark-read]');
    if (mr) {
      var list = ARG.$(mr.getAttribute('data-arg-mark-read'));
      ARG.$$('.is-unread', list).forEach(function (n) { n.classList.remove('is-unread'); });
      var card = list.closest('.arg-card');
      var c = card && ARG.$('.arg-card__header .arg-count', card);
      if (c) c.remove();
    }
  });
})();
