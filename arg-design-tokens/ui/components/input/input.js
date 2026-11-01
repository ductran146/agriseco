/* ARG UI input: [data-arg-password] button toggles the password field in the same .arg-control. */
(function () {
  'use strict';
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-arg-password]');
    if (!btn) return;
    var input = ARG.$('input', btn.closest('.arg-control'));
    if (!input) return;
    var show = input.type === 'password';
    input.type = show ? 'text' : 'password';
    btn.setAttribute('aria-label', show ? 'Ẩn mật khẩu' : 'Hiện mật khẩu');
    btn.innerHTML = ARG.icon(show ? 'eye-slash' : 'eye', 'i--16');
  });
})();
