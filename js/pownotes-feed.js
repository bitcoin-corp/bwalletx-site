// Live feed of genuine PoWNotes from the Mint's registry (/.well-known/bmint-notes.json).
// Only notes listed there are shown; pictures always load through <img>, so no SVG code ever runs.
(function () {
  var box = document.getElementById('pn-feed');
  if (!box) return;
  var only = box.getAttribute('data-type'); // e.g. "bacon-note"; empty = all
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var okOrigin = function (o) { return /^[0-9a-f]{64}_\d+$/.test(o); };
  var render = function (notes) {
    notes = notes.filter(function (n) { return n && okOrigin(n.origin) && (!only || n.type === only); });
    if (!notes.length) { box.innerHTML = '<p class="small">No notes minted yet. They appear here the moment the Mint issues them.</p>'; return; }
    box.innerHTML = notes.slice(0, 60).map(function (n) {
      return '<a class="pn-card" href="https://ordfs.network/' + esc(n.origin) + '" target="_blank" rel="noopener">' +
        '<img src="https://ordfs.network/' + esc(n.origin) + '" alt="PoWNote ' + esc(n.serial) + '" loading="lazy" />' +
        '<span>No. ' + esc(n.serial) + (n.face ? ' · ' + esc(n.face) : '') + '</span></a>';
    }).join('');
  };
  var load = function () {
    fetch('/.well-known/bmint-notes.json', { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : { notes: [] }; })
      .then(function (j) { render((j.notes || []).slice().reverse()); })
      .catch(function () { render([]); });
  };
  load();
  setInterval(load, 60000);
})();
