/* Viewer shell only: sidebar, scrollspy, light/dark switch, automatic checks.
   No component behaviour lives here; components run from dist/arg-ui.js. */
(function () {
  'use strict';
  var $ = ARG.$, $$ = ARG.$$;
  var app = document.getElementById('app');

  /* sidebar */
  var scrim = $('#scrim');
  function setNav(open) { app.classList.toggle('nav-open', open); scrim.hidden = !open; }
  $('#menu-btn').addEventListener('click', function () { setNav(!app.classList.contains('nav-open')); });
  scrim.addEventListener('click', function () { setNav(false); });
  var grp = $('#grp-btn'), nav = $('#nav');
  grp.addEventListener('click', function () {
    var open = grp.getAttribute('aria-expanded') !== 'true';
    grp.setAttribute('aria-expanded', String(open));
    nav.hidden = !open;
  });
  var links = $$('#nav a');
  links.forEach(function (a) { a.addEventListener('click', function () { setNav(false); }); });
  var title = $('#top-title');
  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      links.forEach(function (a) { a.setAttribute('aria-current', String(a.getAttribute('href') === '#' + e.target.id)); });
      title.textContent = 'Base UI · ' + $('h2', e.target).textContent;
    });
  }, { rootMargin: '-72px 0px -70% 0px' });
  links.forEach(function (a) { var s = $(a.getAttribute('href')); if (s) spy.observe(s); });

  /* light / dark */
  var prefersDark = matchMedia('(prefers-color-scheme: dark)');
  var chosen = null;
  try { chosen = localStorage.getItem('arg-ui-mode'); } catch (e) {}
  function hostMode() {
    var t = document.documentElement.getAttribute('data-theme');
    return t === 'dark' || t === 'light' ? t : (prefersDark.matches ? 'dark' : 'light');
  }
  function setMode(m) {
    app.dataset.mode = m;
    $$('.top .seg button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.mode === m)); });
    requestAnimationFrame(runChecks);
  }
  $$('.top .seg button').forEach(function (b) {
    b.addEventListener('click', function () {
      chosen = b.dataset.mode;
      try { localStorage.setItem('arg-ui-mode', chosen); } catch (e) {}
      setMode(chosen);
    });
  });
  prefersDark.addEventListener('change', function () { if (!chosen) setMode(hostMode()); });
  new MutationObserver(function () { if (!chosen) setMode(hostMode()); })
    .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  /* checks */
  var report = JSON.parse($('#build-report').textContent);
  function row(ok, name, detail) {
    return '<tr><td>' + name + '</td><td>' + (ok ? '✓ Đạt' : '✗ Lỗi') + '</td><td>' + detail + '</td></tr>';
  }
  function runChecks() {
    var rows = report.checks.map(function (c) { return row(c.ok, c.name, c.detail); });

    var hs = $$('[data-h]'), bad = [];
    hs.forEach(function (el) {
      var h = Math.round(el.getBoundingClientRect().height);
      if (h !== Number(el.dataset.h)) bad.push(el.className.split(' ')[0] + ' ' + el.dataset.h + ' → ' + h);
    });
    rows.push(row(!bad.length, 'Chiều cao nút, input, select (32 / 40 / 44 / 48)', hs.length + ' phần tử đo' + (bad.length ? '; sai: ' + bad.join(', ') : '')));

    var inits = [['tabs', 'tabs'], ['dropdown', 'dropdown'], ['accordion', 'accordion'], ['carousel', 'carousel']];
    inits.forEach(function (p) {
      var els = $$('[data-arg-' + p[0] + ']'), miss = els.filter(function (e) { return !e['__arg_' + p[1]]; });
      rows.push(row(els.length > 0 && !miss.length, 'Khởi tạo ' + p[0], els.length + ' phần tử, ' + miss.length + ' chưa chạy'));
    });
    var pending = $$('i[data-arg-icon]').length;
    var unresolved = $$('svg use').filter(function (u) { return !document.getElementById(u.getAttribute('href').slice(1)); }).length;
    rows.push(row(!pending && !unresolved, 'Icon Solar', $$('svg.i').length + ' icon hiển thị, ' + pending + ' chưa thay, ' + unresolved + ' không tìm thấy'));
    rows.push(row(typeof ARG.toast === 'function' && typeof ARG.openLayer === 'function' && typeof ARG.setProgress === 'function', 'API JS', 'ARG.toast, ARG.openLayer, ARG.closeLayer, ARG.setProgress, ARG.icon'));
    $('#checks-table tbody').innerHTML = rows.join('');
  }

  function start() { setMode(chosen || hostMode()); if (document.fonts) document.fonts.ready.then(runChecks); addEventListener('resize', runChecks); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
