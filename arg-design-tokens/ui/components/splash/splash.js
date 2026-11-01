/* ARG UI splash: phần tử [data-arg-splash] hiện ~1,1 giây rồi mờ dần và gỡ khỏi trang. Chỉ hiện một lần mỗi phiên trình duyệt
   (sessionStorage; không dùng được thì vẫn hiện). Bật giảm chuyển động: gỡ ngay, không hiện. Bắn "arg:splash" khi đã gỡ. */
(function () {
  'use strict';
  var KEY = 'arg-splash-seen';
  var seen = function () { try { return sessionStorage.getItem(KEY) === '1'; } catch (e) { return false; } };
  var mark = function () { try { sessionStorage.setItem(KEY, '1'); } catch (e) { /* bỏ qua */ } };
  ARG.register('splash', function (root) {
    ARG.$$('[data-arg-splash]', root).forEach(function (el) {
      if (!ARG.once(el, 'splash')) return;
      var done = function () { el.remove(); document.dispatchEvent(new CustomEvent('arg:splash')); };
      if (seen() || ARG.reducedMotion()) { done(); return; }
      mark();
      setTimeout(function () { el.classList.add('is-leaving'); setTimeout(done, 450); }, 1100);
    });
  });
})();
