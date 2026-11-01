/* ARG UI icon: Solar (Linear, Bold Duotone, Bold) sprite + <i data-arg-icon="name"> replacement.
   The sprite string is injected by build.py (placeholder below). */
(function () {
  'use strict';
  var SPRITE = '__ARG_ICON_SPRITE__';
  var NS = 'http://www.w3.org/2000/svg';

  function mountSprite() {
    if (document.getElementById('arg-icon-sprite')) return;
    var host = document.createElement('div');
    host.id = 'arg-icon-sprite';
    host.setAttribute('aria-hidden', 'true');
    host.style.cssText = 'position:absolute;width:0;height:0;overflow:hidden';
    host.innerHTML = SPRITE;
    document.body.insertBefore(host, document.body.firstChild);
  }

  /* ARG.icon('check', 'i--16') -> svg markup string */
  ARG.icon = function (name, cls) {
    return '<svg class="i ' + (cls || '') + '" aria-hidden="true"><use href="#i-' + name + '"/></svg>';
  };
  ARG.iconNames = function () {
    return ARG.$$('#arg-icon-sprite symbol').map(function (s) { return s.id.slice(2); });
  };

  ARG.register('icon', function (root) {
    mountSprite();
    ARG.$$('i[data-arg-icon]', root).forEach(function (el) {
      var svg = document.createElementNS(NS, 'svg');
      svg.setAttribute('class', ('i ' + el.className).trim());
      svg.setAttribute('aria-hidden', 'true');
      if (el.getAttribute('style')) svg.setAttribute('style', el.getAttribute('style'));
      var use = document.createElementNS(NS, 'use');
      use.setAttribute('href', '#i-' + el.getAttribute('data-arg-icon'));
      svg.appendChild(use);
      el.replaceWith(svg);
    });
  });
})();
