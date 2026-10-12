// Artists pages: live original prices, listener board and sponsor pot from bMusic.
// Every element keeps its baked text if a fetch fails.
(function () {
  var API = 'https://bitcoin-music.vercel.app/api/bmusic';
  function get(p) { return fetch(API + p).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function bsv(sats) {
    var b = sats / 1e8;
    return (b >= 1 ? (Math.round(b * 100) / 100).toString() : b.toFixed(4).replace(/0+$/, '')) + ' BSV';
  }
  function num(n) { return Math.round(n).toLocaleString('en-GB'); }

  // Prices: <span data-rel="first-12-01">1 BSV</span>
  document.querySelectorAll('[data-rel]').forEach(function (el) {
    get('/release/' + encodeURIComponent(el.getAttribute('data-rel'))).then(function (d) {
      if (!d) return;
      if (d.minted) { el.textContent = 'Original owned'; el.classList.add('owned'); return; }
      if (d.forSale && d.mintPriceSats) el.textContent = bsv(d.mintPriceSats) + (el.hasAttribute('data-usd') ? ' (about $' + el.getAttribute('data-usd') + ')' : '');
    });
  });

  // Per-track original status on the artist page
  var tl = document.querySelector('#ar-tracks[data-orig]');
  if (tl) tl.querySelectorAll('a').forEach(function (a, k) {
    var id = 'first-12-' + String(k + 1).padStart(2, '0');
    get('/release/' + id).then(function (d) {
      if (!d) return;
      var o = document.createElement('span'); o.className = 'o';
      if (d.minted) { o.textContent = 'Original owned'; o.classList.add('owned'); }
      else if (d.forSale && d.mintPriceSats) o.textContent = 'Original ' + bsv(d.mintPriceSats);
      else return;
      a.appendChild(o);
    });
  });

  // Top listeners
  var board = document.getElementById('ar-board');
  if (board) get('/leaderboard?albumId=first-12').then(function (d) {
    if (!d || !Array.isArray(d.listeners)) return;
    if (!d.listeners.length) { board.innerHTML = '<li class="empty">No named listeners yet. Opt in from the player to appear here.</li>'; return; }
    board.innerHTML = d.listeners.slice(0, 10).map(function (x, k) {
      var name = (x.handle && String(x.handle).trim()) || (x.identityKey ? String(x.identityKey).slice(0, 8) + '…' : 'Listener');
      var secs = x.secondsTotal || 0;
      return '<li><span class="n">' + (k + 1) + '</span><span class="t">' + esc(name) + '</span><span class="d">' + num(secs / 60) + ' min</span></li>';
    }).join('');
  });

  // Sponsor pot gauge
  var pot = document.getElementById('ar-pot');
  if (pot) get('/stream/sponsored?albumId=first-12').then(function (d) {
    if (!d || !d.sponsored || !d.capSats) return;
    var left = Math.max(0, d.capSats - (d.spentSats || 0));
    var pct = Math.max(0, Math.min(100, (left / d.capSats) * 100));
    pot.querySelector('.bar i').style.width = pct.toFixed(1) + '%';
    pot.querySelector('.txt').textContent = num(left) + ' of ' + num(d.capSats) + ' sats left in VexVoid’s pot for tracks 1–6';
    pot.hidden = false;
  });
})();
