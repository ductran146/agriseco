/* ARG UI alert: [data-arg-dismiss="selector"] removes the closest match (default .arg-alert) and fires "arg:dismiss". */
(function () {
  'use strict';
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-arg-dismiss]');
    if (!btn) return;
    var target = btn.closest(btn.getAttribute('data-arg-dismiss') || '.arg-alert');
    if (!target) return;
    target.dispatchEvent(new CustomEvent('arg:dismiss', { bubbles: true }));
    /* thu chiều cao, mờ dần và triệt khoảng cách (gap) để các khối bên dưới trượt lên; không animation nếu người dùng giảm chuyển động */
    var parent = target.parentNode, gap = parseFloat(getComputedStyle(parent).rowGap) || 0;
    if (matchMedia('(prefers-reduced-motion: reduce)').matches || !target.offsetHeight) { target.remove(); return; }
    var st = target.style;
    st.boxSizing = 'border-box'; st.height = target.offsetHeight + 'px'; st.overflow = 'hidden'; st.pointerEvents = 'none';
    target.offsetHeight;
    st.transition = 'height .32s cubic-bezier(.4,0,.2,1), margin-bottom .32s cubic-bezier(.4,0,.2,1), padding .32s cubic-bezier(.4,0,.2,1), opacity .2s linear, transform .32s cubic-bezier(.4,0,.2,1)';
    st.height = '0px'; st.paddingTop = '0px'; st.paddingBottom = '0px'; st.marginBottom = -gap + 'px'; st.opacity = '0'; st.transform = 'translateY(-8px)';
    var done = false;
    function end() { if (done) return; done = true; target.remove(); }
    target.addEventListener('transitionend', function (e) { if (e.propertyName === 'height') end(); });
    setTimeout(end, 450);
  });
})();
