/* ARG UI core: module registry and auto init. Load first.
   Modules call ARG.register(name, init); init(root) must be safe to run twice (use ARG.once).
   Call ARG.init(el) after you insert new markup. */
(function (g) {
  'use strict';
  var ARG = (g.ARG = g.ARG || {});
  var modules = [];

  ARG.$ = function (sel, root) { return (root || document).querySelector(sel); };
  ARG.$$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  ARG.once = function (el, key) {
    var k = '__arg_' + key;
    if (el[k]) return false;
    el[k] = true;
    return true;
  };
  ARG.register = function (name, init) { modules.push({ name: name, init: init }); };
  ARG.init = function (root) {
    root = root || document;
    modules.forEach(function (m) { m.init(root); });
  };
  ARG.modules = function () { return modules.map(function (m) { return m.name; }); };
  ARG.reducedMotion = function () { return g.matchMedia('(prefers-reduced-motion: reduce)').matches; };
  /* Themed root: overlays and toasts mount here so they inherit the active theme tokens. */
  ARG.root = function () { return ARG.$('.arg-ui') || document.body; };

  var start = function () { ARG.init(document); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else Promise.resolve().then(start);
})(window);
