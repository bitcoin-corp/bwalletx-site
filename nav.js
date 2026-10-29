/* Shared navbar for bwalletx.com (bWalletX) and bwallet.space (bWallet, the store edition).
   One config renders the main page links into <nav aria-label="Pages"> and, for the current section,
   a contextual sub-nav under the top bar. Pages keep plain fallback links inside the nav for no-JS
   and crawlers; this script replaces them.
   Usage: <script src="/nav.js"></script> right after </header>
          <script src="/nav.js" data-edition="store"></script> on bwallet.space (also auto on that host). */
// Vercel Web Analytics (owner, 6 Oct 2026): cookieless page views, on every page that loads nav.js.
(function () {
  if (document.querySelector('script[src="/_vercel/insights/script.js"]')) return;
  window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
  var s = document.createElement('script');
  s.defer = true;
  s.src = '/_vercel/insights/script.js';
  document.head.appendChild(s);
})();

(function () {
  var X = 'https://bwalletx.com';
  var NAV = {
    // Five sections by what people come for (owner, 7 Oct 2026: the bar was cluttered). Desktop: hover/focus
    // dropdowns. Phones: a Menu button with one accordion per section. The current section's pages also show
    // as a pill row under the bar.
    // Nav (owner, 28 Oct 2026): tabs by what a visitor wants, then Blog, socials and the one
    // wallet button on the right, everything else in the footer. Owner decisions: Identity, Creators,
    // bApps as a tab (A-Z, ignoring the leading b), bAcc as its own tab (a movement, not a bApp).
    full: [
      { key: 'wallet', label: 'Wallet', href: '/features', pages: ['/features', '/buy', '/swap', '/pots', '/lock', '/lock/verify', '/subscriptions', '/history', '/push-notifications', '/restore', '/recover-relayx', '/migrate', '/sweep-simplycash', '/seedless-login', '/seedless-signin', '/btrust', '/wallet-frames'],
        sub: [
          { label: 'Features overview', href: '/features', ov: 1 },
          { label: 'Buy BSV', href: '/buy' },
          { label: 'Swap into BSV', href: '/swap' },
          { label: 'Pots', href: '/pots' },
          { label: 'Lock', href: '/lock' },
          { label: 'Subscriptions', href: '/subscriptions' },
          { label: 'History', href: '/history' },
          { label: 'Notifications', href: '/push-notifications' },
          { label: 'Restore', href: '/restore', also: ['/migrate', '/sweep-simplycash', '/recover-relayx'] },
          { label: 'NFTs', href: '/nfts' },
          { label: 'Seedless login', href: '/seedless-login', also: ['/seedless-signin'] }
        ] },
      { key: 'you', label: 'Identity', href: '/identity', pages: ['/identity', '/identity-map', '/handles', '/names', '/name-bindings', '/sign', '/bavatars', '/your-character', '/themes', '/themes/custom', '/themes-custom', '/x', '/sign-in-with-handcash', '/gmail'],
        sub: [
          { label: 'Identity overview', href: '/identity', ov: 1 },
          { label: 'Handles', href: '/handles' },
          { label: 'Names', href: '/names' },
          { label: 'Signed names', href: '/name-bindings' },
          { label: 'Your signature', href: '/sign' },
          { label: 'bAvatars', href: '/bavatars' },
          { label: 'Your character', href: '/your-character' },
          { label: 'Themes', href: '/themes' },
          { label: 'Custom editions', href: '/themes/custom', also: ['/themes-custom'] },
          { label: 'Sign in with X', href: '/x' }
        ] },
      { key: 'exchange', label: 'Exchange', href: '/exchange', pages: ['/exchange', '/exchange/strategies', '/launchpad', '/token-curves', '/token-locking', '/nfts', '/pnees', '/pnee', '/store', '/airdrops'],
        sub: [
          { label: 'Exchange', href: '/exchange', ov: 1 },
          { label: 'Strategies', href: '/exchange/strategies' },
          { label: 'Launchpad', href: '/launchpad' },
          { label: 'Token curves', href: '/token-curves' },
          { label: 'Token locking', href: '/token-locking' },
          { label: 'NFTs', href: '/nfts' },
          { label: 'PNEEs', href: '/pnees', also: ['/pnee'] },
          { label: 'Store', href: '/store' },
          { label: 'Airdrops', href: '/airdrops' }
        ] },
      { key: 'social', label: 'Social', href: '/social', pages: ['/social', '/chat', '/bchatx', '/friends', '/bspaces', '/bradio', '/lounge', '/live', '/video', '/games', '/tips', '/bphone', '/bmail', '/verify-note', '/contracts'],
        sub: [
          { label: 'Social overview', href: '/social', ov: 1 },
          { label: 'Chat', href: '/chat', also: ['/bchatx'] },
          { label: 'Friends', href: '/friends' },
          { label: 'bSpaces', href: '/bspaces' },
          { label: 'Lounge', href: '/lounge' },
          { label: 'Live', href: '/live' },
          { label: 'Video', href: '/video' },
          { label: 'Games', href: '/games' },
          { label: 'Tips', href: '/tips' },
          { label: 'bPhone', href: '/bphone' },
          { label: 'bMail', href: '/bmail', also: ['/verify-note'] }
        ] },
      { key: 'create', label: 'Creators', href: '/culture', pages: ['/culture', '/artists', '/artists/vexvoid', '/vexvoid', '/aivj', '/digital-ice-cream', '/mint', '/streaming-payments', '/credits', '/bads', '/bad', '/creative', '/b-creative', '/happy-b', '/partners', '/bshares', '/clients'],
        sub: [
          { label: 'Overview', href: '/culture', ov: 1 },
          { label: 'Artists', href: '/artists', also: ['/artists/vexvoid', '/vexvoid', '/aivj', '/digital-ice-cream'] },
          { label: 'Mint', href: '/mint' },
          { label: 'Streaming payments', href: '/streaming-payments' },
          { label: 'Credits', href: '/credits' },
          { label: 'bAds', href: '/bads', also: ['/bad'] },
          { label: 'b Creative', href: '/creative', also: ['/b-creative', '/happy-b'] },
          { label: 'Partners', href: '/partners' },
          { label: 'bShares', href: '/bshares' },
          { label: 'Branded wallets', href: '/clients' }
        ] },
      { key: 'build', label: 'Build', href: '/developers', pages: ['/developers', '/agent', '/ask-b', '/talk-to-b', '/agents', '/strategies', '/strategies/spec', '/cli', '/mcp', '/connect', '/direct', '/sign-in-button', '/apps/add', '/open-source', '/releases', '/roadmap', '/on-b', '/your-apps-on-b', '/hold-to-talk'],
        sub: [
          { label: 'Developers', href: '/developers', ov: 1 },
          { label: 'b agent', href: '/agent', also: ['/ask-b', '/talk-to-b', '/hold-to-talk'] },
          { label: 'Agent accounts', href: '/agents' },
          { label: 'Strategies', href: '/strategies', also: ['/strategies/spec'] },
          { label: 'CLI', href: '/cli' },
          { label: 'MCP', href: '/mcp' },
          { label: 'Sign in with bWalletX', href: '/connect', also: ['/direct', '/sign-in-button'] },
          { label: 'Add your app', href: '/apps/add', also: ['/on-b', '/your-apps-on-b'] },
          { label: 'Open source', href: '/open-source' },
          { label: 'Releases', href: '/releases' },
          { label: 'Roadmap', href: '/roadmap' }
        ] },
      { key: 'bapps', label: 'bApps', href: '/bapps', icon: 1, pages: ['/bapps', '/bapps/bmovies', '/b-bots', '/services', '/b-market', '/bgitx', '/flick-off', '/tokenblaster'],
        sub: [
          { label: 'All bApps', href: '/bapps', ov: 1 },
          { label: 'bBots', href: '/b-bots' },
          { label: 'bCalX', href: 'https://bcalx.com' },
          { label: 'bChatX', href: 'https://chat.bwalletx.com' },
          { label: 'bDojoX', href: 'https://bdojox.com' },
          { label: 'bDriveX', href: 'https://bdrivex.com' },
          { label: 'bFriendsX', href: 'https://bfriendsx.com' },
          { label: 'bGamesX', href: 'https://bgamesx.com' },
          { label: 'bGitX', href: '/bgitx' },
          { label: 'bJobsX', href: 'https://bjobsx.com' },
          { label: 'bMailX', href: 'https://bmailx.com' },
          { label: 'bMarketX', href: '/b-market' },
          { label: 'bMintX', href: 'https://bmintx.com', also: ['/flick-off'] },
          { label: 'bMovies', href: '/bapps/bmovies' },
          { label: 'bMoviesX', href: 'https://bmoviesx.com' },
          { label: 'bMusicX', href: 'https://bmusicx.com' },
          { label: 'bNewsX', href: 'https://bnewsx.com' },
          { label: 'bRadioX', href: 'https://bradiox.com' },
          { label: 'bSharesX', href: 'https://bsharesx.com' },
          { label: 'bStoreX', href: 'https://bstorex.com' },
          { label: 'tokenblaster', href: '/tokenblaster' },
          { label: 'bVaultX', href: 'https://bvaultx.com' },
          { label: 'bVideoX', href: 'https://bvideox.com' },
          { label: 'bWalletX', href: '/get' },
          { label: 'bWriterX', href: 'https://bwriterx.com' },
          { label: 'b*X services', href: '/services' }
        ] },
      { key: 'bacc', label: 'bAcc', href: '/b/acc', pages: ['/b/acc', '/b/acc/store', '/race-card'],
        sub: [
          { label: 'bAcc: the movement', href: '/b/acc', ov: 1 },
          { label: 'bAcc theme', href: '/b/acc/store' },
          { label: 'bAcc RACE', href: '/race-card' }
        ] },
      { key: 'blog', label: 'Blog', href: '/blog', pages: ['/blog', '/hodl-my-b', '/hodl-my-b/0', '/hodl-my-b/1'] }
    ],
    // Footer columns (built by this script on every page).
    foot: [
      ['Get bWalletX', [['Get bWalletX', '/get'], ['Web wallet', '/web'], ['iPhone', '/iphone'], ['Android', '/android'], ['Chrome extension', '/extension'], ['Desktop', '/desktop'], ['Testers', '/testers']]],
      ['Help &amp; trust', [['Feedback', '/feedback'], ['Ideas', '/ideas'], ['Bugs', '/bugs'], ['b-Aware', '/b-Aware'], ['Bounties', '/bounties'], ['bTrust', '/btrust'], ['Hold to talk', '/hold-to-talk']]],
      ['Company', [['The b family', '/b-family'], ['Blog', '/blog'], ['Hodl my b', '/hodl-my-b'], ['Newsletter', '/newsletter'], ['Brand', '/brand'], ['Jobs', '/jobs'], ['Gigs', '/gigs']]],
      ['More', [['Sign in with HandCash', '/sign-in-with-handcash'], ['Sign in with Gmail', '/gmail'], ['Wallet Frames', '/wallet-frames'], ['Your apps on b', '/on-b'], ['Contracts in chat', '/contracts'], ['bRadio', '/bradio']]],
      ['Coming', [['Business agents', '/business-agents'], ['SMS', '/sms'], ['bPositive', '/bpositive'], ['Partnership shares', '/partnership-shares'], ['bWeb', '/bweb']]],
      ['Follow', [['bChatX', 'https://www.bchatx.com'], ['X', 'https://x.com/bWalletX'], ['Twetch', '/twetch'], ['GitHub', 'https://github.com/bitcoin-corp/bwallet'], ['YouTube', 'https://www.youtube.com/@bWalletX'], ['bChatX Lounge', 'https://chat.bwalletx.com/room/LOUNGE'], ['Privacy', '/privacy'], ['Terms', '/terms']]]
    ],
    // Store edition (bWallet): browse-only Market, no trading, everything else lives on bWalletX.
    store: [
      { label: 'Market', href: '/market', pages: ['/market', '/market/strategies'],
        sub: [
          { label: 'Market', href: '/market' },
          { label: 'Strategies', href: '/market/strategies' }
        ] },
      { label: 'bWalletX features', href: X + '/features' },
      { label: 'Rooms &amp; tokens', href: X + '/friends' },
      { label: 'Get bWalletX &rarr;', href: X }
    ]
  };

  var me = document.currentScript;
  var store = (me && me.getAttribute('data-edition') === 'store') || /(^|\.)bwallet\.space$/.test(location.hostname);

  function norm(p) {
    p = p.replace(/\.html$/, '').replace(/\/index$/, '').replace(/\/+$/, '');
    return p || '/';
  }
  var path = norm(location.pathname);
  var fullPath = path;
  if (/^\/blog\//.test(path)) path = '/blog';

  var all = NAV[store ? 'store' : 'full'];
  var items = all;
  var tabs = items.filter(function (it) { return !it.right; });
  var bappsIt = items.filter(function (it) { return it.icon; })[0];
  var blogIt = items.filter(function (it) { return it.right; })[0];

  var SOC = [
    ['bchat', 'https://www.bchatx.com', 'bChatX: chat, rooms and Spaces', '<svg viewBox="12 10 96 96" width="18" height="18" aria-hidden="true"><mask id="bc-hole"><rect x="0" y="0" width="120" height="120" fill="#fff"/><circle cx="60" cy="72" r="15" fill="#000"/></mask><g fill="currentColor" mask="url(#bc-hole)"><polygon points="45,12 45,72 27,72 27,30"/><circle cx="60" cy="72" r="33"/></g></svg>'],
    ['x', 'https://x.com/bWalletX', 'bWalletX on X', '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>'],
    ['gh', 'https://github.com/bitcoin-corp/bwallet', 'Source code on GitHub', '<svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'],
    ['yt', 'https://www.youtube.com/@bWalletX', 'bWalletX on YouTube', '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg>']
  ];
  function socHtml(cls) { return '<span class="' + cls + '">' + SOC.map(function (x) { return '<a class="nx-soc nx-' + x[0] + '" href="' + x[1] + '" target="_blank" rel="noopener" aria-label="' + x[2] + '" title="' + x[2] + '">' + x[3]  + '</a>'; }).join('') + '</span>'; }
  function link(it, active) {
    if (it.head) return '<span class="nd-head">' + it.head + '</span>';
    return '<a href="' + it.href + '"' + (it.ov ? ' class="nd-ov"' : '') + (active ? ' aria-current="page"' : '') + '>' + it.label + (it.ov ? ' &rarr;' : '') + '</a>';
  }
  var section = null;
  items.forEach(function (it) { if ((it.pages || [it.href]).indexOf(path) !== -1) section = it; });

  var main = document.querySelector('.topbar nav[aria-label="Pages"]');
  if (!main) return;
  function isOn(s) { return path === s.href || (s.also || []).indexOf(path) !== -1; }
  function subLinks(it) { return it.sub.map(function (s) { return link(s, isOn(s)); }).join(''); }

  main.innerHTML = tabs.map(function (it) {
    if (!it.sub) return link(it, it === section);
    return '<span class="nd">' + link({ label: it.label, href: it.href }, it === section) + '<span class="nd-menu' + (it.sub.length > 12 ? ' nd-3' : '') + '">' + subLinks(it) + '</span></span>';
  }).join('');

  var bar = main.closest('.topbar');
  var ctaBox = bar && bar.querySelector('.nav-cta');
  if (ctaBox && !store) {
    // Right side: Blog, bApps grid icon (option), the ONE wallet button (placeholder until the official one lands).
    ctaBox.innerHTML = '';
    ctaBox.insertAdjacentHTML('beforeend', socHtml('nx-socs'));
    ctaBox.insertAdjacentHTML('beforeend', '<a class="dl-btn nx-wallet" href="/get" title="Placeholder for the official wallet button (GET bWALLETX / CONNECT / your chip)">Get bWalletX</a>');
  }
  // Site search (owner, 29 Oct 2026): a magnifier in the bar opens a search box over this site's pages.
  // Index = /search-index.json, built by scripts/gen-llms.py from the same pages as llms.txt and the sitemap.
  if (ctaBox && !store && !ctaBox.querySelector('.nx-sbtn')) {
    var sb = document.createElement('button');
    sb.type = 'button'; sb.className = 'nx-sbtn'; sb.setAttribute('aria-label', 'Search this site'); sb.title = 'Search (/)';
    sb.setAttribute('aria-expanded', 'false'); sb.setAttribute('aria-controls', 'nx-search');
    sb.innerHTML = '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>';
    ctaBox.insertBefore(sb, ctaBox.firstChild);
    var sp = document.createElement('div');
    sp.id = 'nx-search'; sp.className = 'nx-search'; sp.hidden = true;
    sp.innerHTML = '<form role="search" class="nx-sform"><input type="search" placeholder="Search bWalletX pages" aria-label="Search bWalletX pages" autocomplete="off" spellcheck="false" /></form><div class="nx-sres" role="list"></div>';
    bar.appendChild(sp);
    var si = sp.querySelector('input'), sr = sp.querySelector('.nx-sres'), sidx = null;
    var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    var load = function () {
      if (sidx) return;
      sidx = [];
      fetch('/search-index.json').then(function (r) { return r.json(); }).then(function (d) { sidx = d; run(); }).catch(function () {});
    };
    var run = function () {
      var q = si.value.trim().toLowerCase();
      if (!q) { sr.innerHTML = ''; return; }
      var words = q.split(/\s+/);
      var hits = (sidx || []).map(function (p) {
        var t = p.t.toLowerCase(), d = (p.d || '').toLowerCase(), u = p.u.toLowerCase(), sc = 0;
        for (var i = 0; i < words.length; i++) {
          var w = words[i], s1 = 0;
          if (t.indexOf(w) === 0) s1 = 12; else if (t.indexOf(w) !== -1) s1 = 8;
          if (u.indexOf(w) !== -1) s1 = Math.max(s1, 6);
          if (d.indexOf(w) !== -1) s1 = Math.max(s1, 3);
          if (!s1) return null;
          sc += s1;
        }
        if (/^\/blog\//.test(p.u)) sc -= 1;
        return { p: p, s: sc };
      }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 8);
      sr.innerHTML = hits.length ? hits.map(function (h) {
        return '<a role="listitem" href="' + esc(h.p.u) + '"><b>' + esc(h.p.t) + '</b>' + (h.p.d ? '<span>' + esc(h.p.d) + '</span>' : '') + '</a>';
      }).join('') : (sidx && sidx.length ? '<p class="nx-snone">No pages match &ldquo;' + esc(si.value.trim()) + '&rdquo;.</p>' : '');
    };
    var openS = function (o) {
      sp.hidden = !o; sb.setAttribute('aria-expanded', String(o));
      if (o) { load(); si.focus(); var m = document.getElementById('m-menu'); if (m && !m.hidden) { m.hidden = true; var b2 = ctaBox.querySelector('.menu-btn'); if (b2) b2.setAttribute('aria-expanded', 'false'); } }
    };
    sb.addEventListener('click', function () { openS(sp.hidden); });
    si.addEventListener('input', run);
    sp.querySelector('form').addEventListener('submit', function (e) { e.preventDefault(); var a = sr.querySelector('a'); if (a) location.href = a.getAttribute('href'); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !sp.hidden) { openS(false); sb.focus(); }
      else if (e.key === '/' && sp.hidden && !/^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement || {}).tagName || '') && !(document.activeElement || {}).isContentEditable) { e.preventDefault(); openS(true); }
    });
    document.addEventListener('click', function (e) { if (!sp.hidden && !sp.contains(e.target) && !sb.contains(e.target)) openS(false); });
  }
  if (ctaBox && !ctaBox.querySelector('.menu-btn')) {
    var mb = document.createElement('button');
    mb.type = 'button'; mb.className = 'menu-btn';
    mb.setAttribute('aria-expanded', 'false'); mb.setAttribute('aria-controls', 'm-menu');
    mb.textContent = 'Menu';
    var panel = document.createElement('nav');
    panel.id = 'm-menu'; panel.className = 'm-menu'; panel.setAttribute('aria-label', 'Menu'); panel.hidden = true;
    var mItems = tabs;
    panel.innerHTML = mItems.map(function (it) {
      if (!it.sub) return '<a class="m-top" href="' + it.href + '">' + it.label + '</a>';
      return '<details' + (it === section ? ' open' : '') + '><summary>' + it.label + '</summary><div class="m-grid">' + subLinks(it) + '</div></details>';
    }).join('') + socHtml('m-soc');
    mb.addEventListener('click', function () { var o = panel.hidden; panel.hidden = !o; mb.setAttribute('aria-expanded', String(o)); var ss = document.getElementById('nx-search'); if (o && ss) { ss.hidden = true; var bb = ctaBox.querySelector('.nx-sbtn'); if (bb) bb.setAttribute('aria-expanded', 'false'); } });
    // One accordion open at a time keeps the panel short.
    panel.addEventListener('toggle', function (e) { if (e.target.open) panel.querySelectorAll('details').forEach(function (d) { if (d !== e.target) d.open = false; }); }, true);
    ctaBox.appendChild(mb);
    bar.appendChild(panel);
  }

  if (section && section.sub) {
    var sub = document.createElement('nav');
    sub.className = 'section-nav sub-nav';
    sub.setAttribute('aria-label', section.label.replace(/&[a-z]+;/g, '') + ' pages');
    sub.innerHTML = '<div class="wrap">' + section.sub.map(function (it) { return link({ label: it.label.replace(/ overview$/, ''), href: it.href }, isOn(it)); }).join('') + '</div>';
    var on = bar.querySelector('.section-nav');
    if (on) bar.insertBefore(sub, on); else bar.appendChild(sub);
    document.documentElement.classList.add('has-subnav');
    var fitNav = function () { document.documentElement.style.setProperty('--nav-h', (bar.offsetTop + bar.offsetHeight) + 'px'); };
    if (window.ResizeObserver) new ResizeObserver(fitNav).observe(bar); else { fitNav(); window.addEventListener('resize', fitNav); }
  }

  // Footer: the proposal's columns, on every page (added on top of a page's own footer, or as a new one).
  if (!store && NAV.foot) {
    var f = document.createElement('div');
    f.className = 'nx-foot';
    f.innerHTML = '<div class="nx-cols">' + NAV.foot.map(function (c) {
      return '<div><h4>' + c[0] + '</h4>' + c[1].map(function (l) { return '<a href="' + l[1] + '"' + (/^https?:/.test(l[1]) ? ' target="_blank" rel="noopener"' : '') + '>' + l[0] + '</a>'; }).join('') + '</div>';
    }).join('') + '</div>';
    var done = function () {
      var ft = document.querySelector('footer.foot, body > footer');
      if (ft) ft.insertBefore(f, ft.firstChild); else { var w = document.createElement('footer'); w.className = 'nx-foot-wrap'; w.appendChild(f); document.body.appendChild(w); }
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', done); else done();
  }

  var css = document.createElement('style');
  css.textContent =
    '.topbar .sub-nav a[aria-current="page"]{color:#000!important;background:#F5B800;border-color:#F5B800}' +
    '.sub-nav{padding-top:0}' +
    'html.has-subnav main.ext{padding-top:max(190px,calc(var(--nav-h,0px) + 66px))!important}' +
    '.nd{position:relative;display:inline-flex;align-items:center}' +
    '.nd-menu{display:none;position:absolute;top:100%;left:-14px;width:440px;padding:10px;background:#0d0e11;border:1px solid #ffffff1f;border-radius:12px;box-shadow:0 12px 30px #0009;grid-template-columns:1fr 1fr;gap:2px 8px;z-index:60}' +
    '.nd-menu.nd-3{width:560px;grid-template-columns:1fr 1fr 1fr}' +
    '.topbar nav[aria-label="Pages"] .nd:nth-last-child(-n+2) .nd-menu{left:auto;right:-14px}' +
    '.nd:hover .nd-menu,.nd:focus-within .nd-menu{display:grid}' +
    '.nd-menu a{padding:7px 10px;border-radius:8px;white-space:nowrap;font-size:.9rem!important;color:#ddd}' +
    '.nd-menu a:hover{background:#ffffff10}' +
    '.nd-menu a.nd-ov,.m-menu a.nd-ov{grid-column:1/-1;color:#F5B800!important;font-weight:700;border-bottom:1px solid #ffffff14;border-radius:0;margin-bottom:4px}' +
    '.nd-menu a[aria-current="page"]{color:#F5B800}' +
    '.nav-cta{display:inline-flex;align-items:center;gap:12px}' +
    '.nx-blog{color:#ddd;text-decoration:none;font-weight:500}.nx-blog:hover,.nx-blog[aria-current]{color:#F5B800}' +
    '.nx-wallet{white-space:nowrap}' +
    '.nx-socs{display:inline-flex;align-items:center;gap:6px}.nx-soc{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;border:1px solid #ffffff33;color:#fff}.nx-soc:hover{border-color:#F5B800;color:#F5B800}' +
    '.m-soc{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 4px}.m-menu .m-soc a.nx-soc{display:inline-flex;align-items:center;justify-content:center;padding:0 10px;color:#fff}.m-soc .nx-soc{width:auto;min-width:40px;height:40px;padding:0 10px}' +
    '@media (max-width:1180px) and (min-width:860px){.nx-socs .nx-soc{width:28px;height:28px}.nx-socs{gap:4px}.nav-cta{gap:8px}}' +
    '.nx-sbtn{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;flex:none;border-radius:50%;border:1px solid #ffffff33;background:transparent;color:#fff;cursor:pointer;padding:0}.nx-sbtn:hover,.nx-sbtn[aria-expanded="true"]{border-color:#F5B800;color:#F5B800}' +
    '.nx-search{position:absolute;top:100%;right:max(16px,calc((100vw - 1180px)/2));width:min(460px,calc(100vw - 32px));box-sizing:border-box;padding:12px;background:#0d0e11;border:1px solid #ffffff1f;border-radius:14px;box-shadow:0 14px 34px #000a;z-index:70}' +
    '.nx-search[hidden]{display:none}' +
    '.nx-search input{width:100%;box-sizing:border-box;font:500 1rem inherit;color:#fff;background:#16171b;border:1px solid #ffffff2a;border-radius:10px;padding:11px 14px;outline:none}.nx-search input:focus{border-color:#F5B800}' +
    '.nx-sres{max-height:min(60vh,460px);overflow-y:auto;margin-top:6px}.nx-sres:empty{display:none}' +
    '.nx-sres a{display:block;padding:9px 10px;border-radius:9px;text-decoration:none;color:#ddd}.nx-sres a:hover,.nx-sres a:focus{background:#ffffff10;outline:none}.nx-sres a:first-child{background:#ffffff0a}' +
    '.nx-sres b{display:block;color:#fff;font-weight:600;font-size:.95rem}.nx-sres span{display:block;margin-top:2px;color:#9a988f;font-size:.82rem;line-height:1.4;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}' +
    '.nx-snone{margin:8px 10px;color:#9a988f;font-size:.9rem}' +
    '@media (max-width:859px){.nx-search{left:16px;right:16px;width:auto}}' +
    '@media (max-width:430px){.nav-cta{gap:6px!important}.nx-sbtn{width:30px;height:30px}.nx-wallet{padding-left:10px!important;padding-right:10px!important;font-size:.8rem!important}.menu-btn{padding:5px 9px}.topbar .brand span{font-size:1rem}.topbar .brand img{width:28px;height:auto}}' +
    'body.paper .nx-sbtn{color:var(--ink,#111);border-color:var(--ink,#111)}' +
    '.menu-btn{display:none;font:600 .9rem inherit;color:#fff;background:transparent;border:1px solid #ffffff40;border-radius:999px;padding:5px 12px;cursor:pointer}' +
    '.m-menu{background:#0d0e11;border-top:1px solid #ffffff14;padding:6px 16px 14px;max-height:calc(100vh - 120px);overflow-y:auto}' +
    '.m-menu details{border-bottom:1px solid #ffffff12}' +
    '.m-menu summary{padding:12px 0;font-weight:700;color:#fff;cursor:pointer}' +
    '.m-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 8px;padding-bottom:8px}' +
    '.m-menu a{display:block;padding:8px 4px;color:#c9c9c4;text-decoration:none;font-size:.92rem}' +
    '.m-menu a.m-top{padding:12px 0;font-weight:700;color:#fff}' +
    '.m-menu a[aria-current="page"]{color:#F5B800}' +
    '.nx-foot{max-width:1180px;margin:0 auto;padding:32px 16px 8px}.nx-cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:20px}' +
    '.nx-foot h4{margin:0 0 8px;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:#8a8a85}.nx-foot a{display:block;padding:3px 0;color:#c9c9c4;text-decoration:none;font-size:.9rem}.nx-foot a:hover{color:#F5B800}' +
    '.nx-foot-wrap{border-top:1px solid #ffffff14;margin-top:48px;padding-bottom:40px}' +
    '.topbar nav[aria-label="Pages"] a{white-space:nowrap}' +
    '@media (max-width:1180px) and (min-width:860px){.topbar nav[aria-label="Pages"]{gap:0!important;margin:0 6px!important}.topbar nav[aria-label="Pages"]>.nd>a,.topbar nav[aria-label="Pages"]>a{padding-left:5px!important;padding-right:5px!important;font-size:.84rem!important}.nx-blog{font-size:.84rem}.brand span{font-size:1.05rem}.nx-wallet{padding-left:12px!important;padding-right:12px!important;font-size:.84rem!important}}' +
    '' +
    '@media (max-width:859px){.topbar nav[aria-label="Pages"]{display:none!important}.menu-btn{display:inline-block}.nx-blog,.nx-socs{display:none!important}' +
    '.topbar-in:has(nav[aria-label="Pages"]){flex-wrap:nowrap!important;height:64px!important;padding-top:0!important}' +
    '.topbar nav.m-menu:not([hidden]){display:block}.brand{flex:none}main.ext{padding-top:120px!important}html.has-subnav main.ext{padding-top:120px!important}.topbar .sub-nav{display:none!important}}' +
    '@media (min-width:860px){.m-menu{display:none!important}}' +
    'body.paper .menu-btn{color:var(--ink,#111);border-color:var(--ink,#111)}body.paper .m-menu{background:var(--sheet,#fff);border-top-color:var(--hair,#d9d6ce)}body.paper .m-menu details{border-bottom-color:var(--hair,#d9d6ce)}body.paper .m-menu summary,body.paper .m-menu a.m-top{color:var(--ink,#111)}body.paper .m-menu a{color:var(--muted,#5d5b56)}body.paper .nx-foot a{color:var(--muted,#5d5b56)}body.paper .nx-blog{color:var(--ink,#111);border-color:var(--ink,#111)}' +
    (store ? '.nd-menu,.m-menu{background:#F5B800!important}.nd-menu a,.m-menu a,.m-menu summary{color:#010101!important}.menu-btn{color:#010101;border-color:#0006}.topbar .sub-nav a[aria-current="page"]{color:#F5B800!important;background:#010101!important;border-color:#010101!important}' : '');
  document.head.appendChild(css);
})();
