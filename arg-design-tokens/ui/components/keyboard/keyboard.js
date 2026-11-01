/* ARG UI keyboard: bàn phím mô phỏng điện thoại, hiện khi bấm vào ô nhập trong .arg-page.
   - Kiểu bàn phím theo ô nhập: inputmode="numeric" hoặc type="number" → phím số; inputmode="decimal" → phím số có dấu phẩy; type="tel" hoặc inputmode="tel" → phím số điện thoại;
     còn lại → bàn phím chữ (có trang số và ký hiệu). Ô type="date", checkbox... không hiện bàn phím.
   - enterkeyhint (search, go, next) đổi nhãn phím xuống dòng; mặc định "Xong". Nút Xong trên thanh công cụ đóng bàn phím.
   - Bấm nút (button) khi bàn phím đang mở thì ô nhập giữ focus, bàn phím không hạ xuống trước lúc nút nhận lần bấm.
   - Phím gõ vào ô bằng setRangeText và bắn "input", nên các JS lắng nghe ô nhập vẫn chạy. Phím xoá giữ để lặp.
   - Đặt inputmode="none" lên ô để bàn phím hệ điều hành không hiện cùng lúc. Bàn phím gõ thật vẫn dùng được.
   - [data-arg-kb-static="num|decimal|tel|alpha"] vẽ bản tĩnh để minh hoạ. Bắn "arg:keyboard" ({ open, mode }) trên document. */
(function () {
  'use strict';
  var SUB = { 2: 'ABC', 3: 'DEF', 4: 'GHI', 5: 'JKL', 6: 'MNO', 7: 'PQRS', 8: 'TUV', 9: 'WXYZ' };
  var ROWS = { abc: ['qwertyuiop', 'asdfghjkl', 'zxcvbnm'], sym: ['1234567890', '-/:;()₫&@"', '.,?!\''] };
  var NOKB = /^(checkbox|radio|date|time|datetime-local|month|week|range|color|file|button|submit|reset|image|hidden)$/;
  var kb, body, cur = null, st = { mode: 'alpha', page: 'abc', shift: 0 }, tShift = 0, hideT = 0, rep = 0, repI = 0;

  function btn(cls, label, attrs) { return '<button class="arg-kb__key ' + cls + '" type="button" tabindex="-1" ' + (attrs || '') + '>' + label + '</button>'; }
  function numpad(mode) {
    var h = '';
    for (var d = 1; d <= 9; d++) h += btn('', '<span>' + d + '</span>' + (SUB[d] ? '<span class="arg-kb__sub">' + SUB[d] + '</span>' : ''), 'data-ch="' + d + '" aria-label="' + d + '"');
    h += mode === 'tel' ? btn('arg-kb__key--bare', '<span class="arg-kb__glyph">+*#</span>', 'data-ch="+" aria-label="Dấu cộng"')
      : mode === 'decimal' ? btn('arg-kb__key--c', ',', 'data-ch="," aria-label="Dấu phẩy"') : '<span></span>';
    h += btn('arg-kb__key--c', '0', 'data-ch="0" aria-label="0"') + btn('arg-kb__key--bare', ARG.icon('backspace'), 'data-act="back" aria-label="Xoá"');
    return '<div class="arg-kb__num">' + h + '</div>';
  }
  function alpha() {
    var up = st.shift > 0, sym = st.page === 'sym', rows = ROWS[sym ? 'sym' : 'abc'], c = function (k) { return up && !sym ? k.toUpperCase() : k; };
    var key = function (k, extra) { return btn(extra || '', c(k), 'data-ch="' + c(k) + '"' + (sym ? '' : ' data-k="' + c(k) + '"') + ' aria-label="' + c(k) + '"'); };
    var h = rows[0].split('').map(function (k) { return key(k); }).join('');
    h += rows[1].split('').map(function (k, i) { return key(k, i === 0 && !sym ? 'arg-kb__key--off' : ''); }).join('');
    if (sym) h += '<span class="arg-kb__key--w7"></span>' + rows[2].split('').map(function (k) { return key(k); }).join('');
    else h += btn('arg-kb__key--fn arg-kb__key--w3' + (st.shift ? ' is-on' : ''), ARG.icon('arrow-fat-up'), 'data-act="shift" aria-label="Chữ hoa"') + rows[2].split('').map(function (k) { return key(k); }).join('');
    h += btn('arg-kb__key--fn arg-kb__key--w3', ARG.icon('backspace'), 'data-act="back" aria-label="Xoá"');
    h += btn('arg-kb__key--fn arg-kb__key--w5', sym ? 'ABC' : '123', 'data-act="page" aria-label="Đổi trang"') + btn('arg-kb__key--w10', 'dấu cách', 'data-ch=" " aria-label="Dấu cách"') + btn('arg-kb__key--fn arg-kb__key--w5', retLabel(), 'data-act="ret" aria-label="' + retLabel() + '"');
    return '<div class="arg-kb__alpha">' + h + '</div>';
  }
  function retLabel() { var h = cur && cur.getAttribute('enterkeyhint'); return { search: 'Tìm', go: 'Đi', next: 'Tiếp', send: 'Gửi', done: 'Xong' }[h] || 'Xong'; }
  function pad(mode) { return mode === 'alpha' ? alpha() : numpad(mode); }
  function frame(inner, bar) {
    return (bar ? '<div class="arg-kb__bar"><button class="arg-kb__done" type="button" tabindex="-1" data-act="done">' + ARG.icon('keyboard') + '<span>Xong</span></button></div>' : '') +
      '<div class="arg-kb__body">' + inner + '</div><div class="arg-kb__home"></div>';
  }
  function render() { body.innerHTML = pad(st.mode); }

  function modeOf(el) {
    var im = el.dataset.kbIm || el.getAttribute('inputmode') || '';
    if (el.type === 'tel' || im === 'tel') return 'tel';
    if (im === 'decimal') return 'decimal';
    if (im === 'numeric' || el.type === 'number') return 'numeric';
    return 'alpha';
  }
  function eligible(el) { return el && el.matches && el.matches('input, textarea') && !el.readOnly && !el.disabled && !NOKB.test(el.type || 'text') && !!el.closest('.arg-page'); }
  function mute(el) { if (eligible(el) && el.dataset.kbIm === undefined) { el.dataset.kbIm = el.getAttribute('inputmode') || ''; el.setAttribute('inputmode', 'none'); } }

  function sel(el) { try { return [el.selectionStart, el.selectionEnd]; } catch (e) { return [null, null]; } }
  function put(ch) {
    var el = cur; if (!el || (el.maxLength > 0 && el.value.length >= el.maxLength)) return;
    var s = sel(el);
    if (s[0] === null) el.value += ch; else el.setRangeText(ch, s[0], s[1], 'end');
    el.dispatchEvent(new Event('input', { bubbles: true }));
    if (st.shift === 1 && st.mode === 'alpha') { st.shift = 0; render(); }
  }
  function back() {
    var el = cur; if (!el) return;
    var s = sel(el);
    if (s[0] === null) el.value = el.value.slice(0, -1);
    else if (s[0] !== s[1]) el.setRangeText('', s[0], s[1], 'end');
    else if (s[0] > 0) el.setRangeText('', s[0] - 1, s[0], 'end');
    el.dispatchEvent(new Event('input', { bubbles: true }));
  }
  function act(a) {
    if (a === 'back') back();
    else if (a === 'done') { if (cur) cur.blur(); }
    else if (a === 'ret') { if (cur) { cur.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true })); cur.blur(); } }
    else if (a === 'page') { st.page = st.page === 'abc' ? 'sym' : 'abc'; render(); }
    else if (a === 'shift') { var n = Date.now(); st.shift = st.shift === 1 && n - tShift < 400 ? 2 : st.shift ? 0 : 1; tShift = n; render(); }
  }

  function open(el) {
    clearTimeout(hideT); cur = el; st.mode = modeOf(el); st.page = 'abc'; st.shift = 0; render();
    kb.hidden = false; document.documentElement.classList.add('arg-kb-open');
    requestAnimationFrame(function () { requestAnimationFrame(function () { kb.classList.add('is-open'); }); });
    setTimeout(function () {
      if (cur !== el) return;
      var r = el.getBoundingClientRect(), vis = window.innerHeight - kb.offsetHeight - 16;
      if (r.bottom > vis) window.scrollBy({ top: r.bottom - vis, behavior: 'smooth' });
    }, 280);
    document.dispatchEvent(new CustomEvent('arg:keyboard', { detail: { open: true, mode: st.mode } }));
  }
  function close() {
    cur = null; kb.classList.remove('is-open'); document.documentElement.classList.remove('arg-kb-open');
    hideT = setTimeout(function () { if (!cur) kb.hidden = true; }, 260);
    document.dispatchEvent(new CustomEvent('arg:keyboard', { detail: { open: false } }));
  }
  function stopRep() { clearTimeout(rep); clearInterval(repI); }

  ARG.register('keyboard', function (root) {
    ARG.$$('[data-arg-kb-static]', root).forEach(function (el) {
      if (!ARG.once(el, 'kbs')) return;
      var m = el.getAttribute('data-arg-kb-static'); st = { mode: m, page: 'abc', shift: 0 }; cur = null;
      el.classList.add('arg-kb', 'arg-kb--static'); el.setAttribute('aria-hidden', 'true'); el.innerHTML = frame(pad(m), true);
      ARG.init(el);
    });
    if (kb || !document.querySelector('.arg-page')) return;
    kb = document.createElement('div'); kb.className = 'arg-kb'; kb.hidden = true; kb.setAttribute('aria-hidden', 'true');
    kb.innerHTML = frame('', true); body = ARG.$('.arg-kb__body', kb); document.body.appendChild(kb); ARG.init(kb);
    ARG.$$('input, textarea', document).forEach(mute);
    document.addEventListener('pointerdown', function (e) { mute(e.target); }, true);
    document.addEventListener('focusin', function (e) { if (eligible(e.target)) { mute(e.target); open(e.target); } });
    document.addEventListener('focusout', function () {
      setTimeout(function () { if (!eligible(document.activeElement)) close(); else if (document.activeElement !== cur) open(document.activeElement); }, 0);
    });
    kb.addEventListener('mousedown', function (e) { e.preventDefault(); });
    /* Bấm một nút khi bàn phím đang mở không làm ô nhập mất focus (như iOS): nếu mất focus, bàn phím hạ xuống, hộp chứa nút tụt theo và lần bấm đầu bị nuốt. */
    document.addEventListener('mousedown', function (e) { if (cur && e.target.closest && e.target.closest('button, [role="button"]') && !e.target.closest('input, textarea')) e.preventDefault(); });
    kb.addEventListener('pointerdown', function (e) {
      var k = e.target.closest('.arg-kb__key, .arg-kb__done'); if (!k) return;
      e.preventDefault();
      var a = k.getAttribute('data-act'), ch = k.getAttribute('data-ch');
      if (ch !== null) put(ch); else if (a) act(a);
      if (a === 'back') { stopRep(); rep = setTimeout(function () { repI = setInterval(back, 70); }, 420); }
    });
    ['pointerup', 'pointercancel', 'pointerleave'].forEach(function (t) { kb.addEventListener(t, stopRep); });
  });
})();
