// Connects a page to the live room. Without a backend (opened from disk or from GitHub Pages) it reports
// 'offline' once and the page carries on as plain slides.
window.Live = function (opts) {
  var role = opts.role, onState = opts.onState || function () {}, onYou = opts.onYou || function () {},
    onCmd = opts.onCmd || function () {}, onStatus = opts.onStatus || function () {};
  var ws = null, wait = 1000, alive = null, retry = null, closed = false, everOpen = false;

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  var id = store('sn-id');
  if (!id) { id = Math.random().toString(36).slice(2) + Date.now().toString(36); store('sn-id', id); }

  // A host key arrives once in the URL (?key=...), is kept on this device, and is taken out of the address bar
  var params = new URLSearchParams(location.search);
  var key = params.get('key');
  if (key) { store('sn-key', key); params.delete('key'); history.replaceState(null, '', location.pathname + (params.toString() ? '?' + params : '') + location.hash); }
  else if (opts.wantsKey) key = store('sn-key');

  var hosted = /^https?:$/.test(location.protocol) && !/github\.io$/.test(location.hostname);

  function open() {
    if (!hosted) { onStatus('offline'); return; }
    var q = new URLSearchParams({ role: role, id: id });
    if (key) q.set('key', key);
    onStatus('connecting');
    ws = new WebSocket((location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws?' + q);
    ws.onopen = function () {
      everOpen = true; wait = 1000; onStatus('live');
      clearInterval(alive);
      alive = setInterval(function () { send({ type: 'ping' }); }, 25000);
    };
    ws.onmessage = function (e) {
      var m; try { m = JSON.parse(e.data); } catch (err) { return; }
      if (m.type === 'state') onState(m.state, m.host);
      else if (m.type === 'you') onYou(m);
      else if (m.type === 'cmd') onCmd(m.cmd);
    };
    ws.onclose = function (e) {
      clearInterval(alive);
      if (closed) return;
      // A refused upgrade before any success usually means no backend or a wrong key
      onStatus(everOpen ? 'reconnecting' : (key && role !== 'phone' ? 'badkey-or-offline' : 'offline'));
      retry = setTimeout(open, wait);
      wait = Math.min(wait * 2, 15000);
    };
  }

  function send(m) {
    if (ws && ws.readyState === 1) { ws.send(JSON.stringify(m)); return true; }
    return false;
  }

  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible' && hosted && (!ws || ws.readyState > 1)) { clearTimeout(retry); wait = 1000; open(); }
  });

  open();
  return { send: send, id: id, hasKey: Boolean(key), hosted: hosted };
};
