// Shows the "Live" links when the site is served by the live Worker (it answers /api/health).
// On GitHub Pages there is no backend, so they stay hidden.
(function () {
  if (!/^https?:$/.test(location.protocol)) return;
  fetch('/api/health', { cache: 'no-store' })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (h) {
      if (!h || !h.ok) return;
      document.querySelectorAll('[data-live]').forEach(function (el) { el.hidden = false; });
    })
    .catch(function () {});
})();
