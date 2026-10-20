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
    full: [
      { label: 'Wallet', href: '/features', pages: ['/names', '/name-bindings', '/seedless-login', '/features', '/subscriptions', '/pots', '/lock', '/lock/verify', '/token-locking', '/restore', '/recover-relayx', '/history', '/identity', '/handles', '/bavatars', '/themes', '/themes/custom', '/business-agents', '/sms', '/nfts', '/swap', '/mint', '/get', '/download', '/android', '/iphone', '/extension', '/push-notifications', '/testers', '/privacy'],
        sub: [
          { label: 'Features', href: '/features' },
          { label: 'Subscriptions', href: '/subscriptions' },
          { label: 'Pots', href: '/pots' },
          { label: 'Lock', href: '/lock' },
          { label: 'Token locking', href: '/token-locking' },
          { label: 'Seedless login', href: '/seedless-login' },
          { label: 'Restore', href: '/restore' },
          { label: 'RelayX NFTs', href: '/recover-relayx' },
          { label: 'History', href: '/history' },
          { label: 'Identity', href: '/identity' },
          { label: 'Handles', href: '/handles' },
          { label: 'Names', href: '/names' },
          { label: 'Signed names', href: '/name-bindings' },
          { label: 'bAvatars', href: '/bavatars' },
          { label: 'Themes', href: '/themes' },
          { label: 'Custom editions', href: '/themes/custom' },
          { label: 'Business agents (coming)', href: '/business-agents' },
          { label: 'SMS (coming)', href: '/sms' },
          { label: 'NFTs', href: '/nfts' },
          { label: 'Swap into BSV', href: '/swap' },
          { label: 'Mint', href: '/mint' },
          { label: 'Notifications', href: '/push-notifications' },
          { label: 'Extension', href: '/extension' },
          { label: 'iPhone', href: '/iphone' },
          { label: 'Android', href: '/android' },
          { label: 'Testers', href: '/testers' }
        ] },
      { label: 'Exchange', href: '/exchange', pages: ['/exchange', '/exchange/strategies', '/token-curves', '/pnees', '/pnee', '/buy', '/launchpad', '/store'],
        sub: [
          { label: 'Exchange', href: '/exchange' },
          { label: 'Strategies', href: '/exchange/strategies' },
          { label: 'Token curves', href: '/token-curves' },
          { label: 'PNEEs', href: '/pnees', also: ['/pnee'] },
          { label: 'Launchpad', href: '/launchpad' },
          { label: 'Store', href: '/store' },
          { label: 'Buy BSV', href: '/buy' }
        ] },
      { label: 'Social', href: '/social', pages: ['/social', '/chat', '/friends', '/lounge', '/games', '/video', '/live', '/tips', '/streaming-payments', '/credits', '/bspaces', '/bphone', '/bmail', '/bpositive', '/airdrops', '/sign', '/x', '/sign-in-with-handcash', '/gmail'],
        sub: [
          { label: 'Social', href: '/social' },
          { label: 'Chat', href: '/chat' },
          { label: 'Friends', href: '/friends' },
          { label: 'Lounge', href: '/lounge' },
          { label: 'Games', href: '/games' },
          { label: 'Video', href: '/video' },
          { label: 'Live', href: '/live' },
          { label: 'Tips', href: '/tips' },
          { label: 'Streaming payments', href: '/streaming-payments' },
          { label: 'Credits (in testing)', href: '/credits' },
          { label: 'bSpaces', href: '/bspaces' },
          { label: 'bPhone', href: '/bphone' },
          { label: 'bMail', href: '/bmail' },
          { label: 'bPositive (coming)', href: '/bpositive' },
          { label: 'Airdrops', href: '/airdrops' },
          { label: 'Your signature', href: '/sign' },
          { label: 'Sign in with X', href: '/x' },
          { label: 'Sign in with HandCash', href: '/sign-in-with-handcash' },
          { label: 'Sign in with Gmail', href: '/gmail' }
        ] },
      { label: 'Artists', href: '/artists', pages: ['/artists', '/artists/vexvoid', '/vexvoid', '/aivj', '/b-creative'],
        sub: [
          { label: 'Artists', href: '/artists' },
          { label: 'VexVoid', href: '/artists/vexvoid', also: ['/vexvoid'] },
          { label: 'bTV: AIVJ', href: '/aivj' },
          { label: 'b creative', href: '/b-creative' }
        ] },
      { label: 'bApps', href: '/bapps', pages: ['/bapps', '/bapps/bmovies', '/bshares', '/partnership-shares', '/bweb'],
        sub: [
          { label: 'All bApps', href: '/bapps' },
          { label: 'bMovies', href: '/bapps/bmovies' },
          { label: 'bChatX', href: 'https://www.bchatx.com' },
          { label: 'bMailX', href: 'https://bmailx.com' },
          { label: 'bRadioX', href: 'https://bradiox.com' },
          { label: 'bCalX', href: 'https://bcalx.com' },
          { label: 'bJobsX', href: 'https://bjobsx.com' },
          { label: 'bNewsX', href: 'https://bnewsx.com' },
          { label: 'bMusicX', href: 'https://bmusicx.com' },
          { label: 'bStoreX', href: 'https://bstorex.com' },
          { label: 'bMintX: FLICK OFF', href: 'https://bmintx.com/flick-off' },
          { label: 'bVideoX', href: 'https://bvideox.com' },
          { label: 'bFriendsX', href: 'https://bfriendsx.com' },
          { label: 'bDojoX', href: 'https://bdojox.com' },
          { label: 'bDriveX', href: 'https://bdrivex.com' },
          { label: 'bShares: registers for any company', href: '/bshares' },
          { label: 'Partnership shares (coming)', href: '/partnership-shares' },
          { label: 'bWeb (coming)', href: '/bweb' }
        ] },
      { label: 'Agents', href: '/agents', pages: ['/agents', '/agent', '/ideas', '/bugs', '/hold-to-talk', '/strategies', '/strategies/spec', '/cli', '/mcp'],
        sub: [
          { label: 'Agent accounts', href: '/agents' },
          { label: 'b agent', href: '/agent' },
          { label: 'Ideas', href: '/ideas' },
          { label: 'Bugs', href: '/bugs' },
          { label: 'Hold to talk', href: '/hold-to-talk' },
          { label: 'Strategies', href: '/strategies' },
          { label: 'Strategy spec', href: '/strategies/spec' },
          { label: 'CLI', href: '/cli' },
          { label: 'MCP', href: '/mcp' }
        ] },
      // Developers holds the Blog too (owner, 18 Oct 2026). When you publish a post, add it to the top of
      // Latest and drop the oldest (keep 5).
      { label: 'Developers', href: '/developers', pages: ['/developers', '/connect', '/apps/add', '/open-source', '/blog', '/releases', '/hodl-my-b'],
        // The pill row under the bar shows these only (not the post list in the menu).
        pills: ['/developers', '/connect', '/apps/add', '/cli', '/mcp', '/open-source', '/blog', '/releases', '/hodl-my-b'],
        sub: [
          { label: 'Developers', href: '/developers' },
          { label: 'Sign in with bWalletX', href: '/connect' },
          { label: 'Add your app', href: '/apps/add' },
          { label: 'CLI', href: '/cli' },
          { label: 'MCP', href: '/mcp' },
          { label: 'Open source', href: '/open-source' },
          { label: 'Blog', href: '/blog' },
          { label: 'Releases', href: '/releases' },
          { label: 'Hodl my b · weekly', href: '/hodl-my-b' },
          { head: 'Latest' }
        ].concat([
          { label: '053 Friends, bPics, video', href: '/blog/053-friends-bpics-and-video' },
          { label: '052 Tip buttons', href: '/blog/052-tip-buttons' },
          { label: '051 Spaces on a schedule', href: '/blog/051-spaces-schedule-and-ask-b' },
          { label: '050 bTV: AIVJ — VexVoid, live', href: '/blog/050-aivj-tv-vexvoid-live' },
          { label: '049 The Exchange, sorted', href: '/blog/049-the-exchange-sorted' }
        ]) }
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
  var items = NAV[store ? 'store' : 'full'];

  function norm(p) {
    p = p.replace(/\.html$/, '').replace(/\/index$/, '').replace(/\/+$/, '');
    return p || '/';
  }
  var path = norm(location.pathname);
  var fullPath = path;
  if (/^\/blog\//.test(path)) path = '/blog'; // every post sits under Blog
  function link(it, active) {
    if (it.head) return '<span class="nd-head">' + it.head + '</span>';
    return '<a href="' + it.href + '"' + (active ? ' aria-current="page"' : '') + '>' + it.label + '</a>';
  }

  var section = null;
  items.forEach(function (it) {
    if ((it.pages || [it.href]).indexOf(path) !== -1) section = it;
  });

  var main = document.querySelector('.topbar nav[aria-label="Pages"]');
  if (!main) return;
  function subLinks(it) {
    return it.sub.map(function (s) { return link(s, (s.href && /^\/blog(\/|$)/.test(s.href) ? fullPath : path) === s.href || (s.also || []).indexOf(path) !== -1); }).join('');
  }
  // Desktop: each section is a link with a dropdown of its pages.
  main.innerHTML = items.map(function (it) {
    if (!it.sub) return link(it, it === section);
    return '<span class="nd">' + link(it, it === section) + '<span class="nd-menu">' + subLinks(it) + '</span></span>';
  }).join('');
  // Phones: a Menu button opening one accordion per section (the current one open).
  var ctaBox = main.closest('.topbar') && main.closest('.topbar').querySelector('.nav-cta');
  if (ctaBox && !ctaBox.querySelector('.menu-btn')) {
    var mb = document.createElement('button');
    mb.type = 'button';
    mb.className = 'menu-btn';
    mb.setAttribute('aria-expanded', 'false');
    mb.setAttribute('aria-controls', 'm-menu');
    mb.textContent = 'Menu';
    var panel = document.createElement('nav');
    panel.id = 'm-menu';
    panel.className = 'm-menu';
    panel.setAttribute('aria-label', 'Menu');
    panel.hidden = true;
    panel.innerHTML = items.map(function (it) {
      if (!it.sub) return '<a class="m-top" href="' + it.href + '">' + it.label + '</a>';
      return '<details' + (it === section ? ' open' : '') + '><summary>' + it.label + '</summary>' + subLinks(it) + '</details>';
    }).join('') + '<a class="m-top" href="https://web.bwalletx.com">Web wallet &rarr;</a><p class="m-follow"><a href="https://x.com/bWalletX">X</a><a href="https://bwalletx.com/twetch">Twetch</a><a href="https://github.com/bitcoin-corp/bwallet">GitHub</a><a href="https://www.youtube.com/@bWalletX">YouTube</a><a href="https://www.bchatx.com/room/LOUNGE">bChatX Lounge</a></p>';
    mb.addEventListener('click', function () {
      var open = panel.hidden;
      panel.hidden = !open;
      mb.setAttribute('aria-expanded', String(open));
    });
    ctaBox.appendChild(mb);
    main.closest('.topbar').appendChild(panel);
  }

  if (section && section.sub && section.pills !== false) {
    var sub = document.createElement('nav');
    sub.className = 'section-nav sub-nav';
    sub.setAttribute('aria-label', section.label.replace(/&[a-z]+;/g, '') + ' pages');
    var pillItems = Array.isArray(section.pills)
      ? section.sub.filter(function (it) { return section.pills.indexOf(it.href) !== -1; })
      : section.sub;
    sub.innerHTML = '<div class="wrap">' + pillItems.map(function (it) {
      return link(it, path === it.href || (it.also || []).indexOf(path) !== -1);
    }).join('') + '</div>';
    var bar = main.closest('.topbar');
    var on = bar.querySelector('.section-nav');
    if (on) bar.insertBefore(sub, on); else bar.appendChild(sub);
    document.documentElement.classList.add('has-subnav');
    // The pill row wraps (no sideways scrolling), so its height varies: push the page down to match.
    var fitNav = function () { document.documentElement.style.setProperty('--nav-h', (bar.offsetTop + bar.offsetHeight) + 'px'); };
    if (window.ResizeObserver) new ResizeObserver(fitNav).observe(bar); else { fitNav(); window.addEventListener('resize', fitNav); }
  }

  // Follow on X (bWalletX only): an icon before the Download / Web buttons, on every page.
  var cta = main.closest('.topbar') && main.closest('.topbar').querySelector('.nav-cta');
  // Both editions (owner, 6 Oct 2026: bwallet.space needs X and GitHub too).
  if (cta && !cta.querySelector('.x-link')) {
    var x = document.createElement('a');
    x.className = 'x-link';
    x.href = 'https://x.com/bWalletX';
    x.target = '_blank';
    x.rel = 'noopener';
    x.setAttribute('aria-label', 'bWalletX on X');
    x.title = '@bWalletX on X';
    x.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>';
    cta.insertBefore(x, cta.firstChild);
    // Source on GitHub (the wallet is open source), next to X (owner, 6 Oct 2026).
    var gh = document.createElement('a');
    gh.className = 'x-link';
    gh.href = 'https://github.com/bitcoin-corp/bwallet';
    gh.target = '_blank';
    gh.rel = 'noopener';
    gh.setAttribute('aria-label', 'bWalletX source code on GitHub');
    gh.title = 'Source code on GitHub';
    gh.innerHTML = '<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>';
    cta.insertBefore(gh, x.nextSibling);
    // YouTube channel (owner, 7 Oct 2026), after GitHub.
    var yt = document.createElement('a');
    yt.className = 'x-link';
    yt.href = 'https://www.youtube.com/@bWalletX';
    yt.target = '_blank';
    yt.rel = 'noopener';
    yt.setAttribute('aria-label', 'bWalletX on YouTube');
    yt.title = 'bWalletX on YouTube';
    yt.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg>';
    cta.insertBefore(yt, gh.nextSibling);
    // bChat instead of Telegram/Discord (owner, 6 Oct 2026): a white b, next to X and GitHub.
    var bc = document.createElement('a');
    bc.className = 'x-link bchat-link';
    bc.href = 'https://www.bchatx.com/room/LOUNGE';
    bc.target = '_blank';
    bc.rel = 'noopener';
    bc.setAttribute('aria-label', 'Join the bWallet Lounge on bChat');
    bc.title = 'Join the bWallet Lounge on bChat';
    // bChat's own b (bit-sign public/bchat-icon.svg: flag-top stem + bowl), in white.
    bc.innerHTML = '<svg viewBox="12 10 96 96" width="20" height="20" aria-hidden="true"><mask id="bc-hole"><rect x="0" y="0" width="120" height="120" fill="#fff"/><circle cx="60" cy="72" r="15" fill="#000"/></mask><g fill="currentColor" mask="url(#bc-hole)"><polygon points="45,12 45,76 27,76 27,30"/><circle cx="60" cy="72" r="33"/></g></svg>';
    cta.insertBefore(bc, gh.nextSibling);
  }

  var css = document.createElement('style');
  css.textContent =
    '.topbar .sub-nav a[aria-current="page"]{color:#000!important;background:#F5B800;border-color:#F5B800}' +
    '.sub-nav{padding-top:0}' +
    '.nav-cta .x-link{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;border:1px solid #ffffff33;color:#fff;margin-right:8px;vertical-align:middle}' +
    '.nav-cta .x-link:hover{border-color:#F5B800;color:#F5B800}' +
    'html.has-subnav main.ext{padding-top:max(190px,calc(var(--nav-h,0px) + 66px))!important}' +
    '.nd{position:relative;display:inline-flex;align-items:center}' +
    '.nd-menu{display:none;position:absolute;top:100%;left:-14px;min-width:200px;padding:8px;margin-top:0;background:#0d0e11;border:1px solid #ffffff1f;border-radius:12px;box-shadow:0 12px 30px #0009;flex-direction:column;gap:2px;z-index:60}' +
    '.nd:hover .nd-menu,.nd:focus-within .nd-menu{display:flex}' +
    '.nd-menu a{padding:7px 10px;border-radius:8px;white-space:nowrap;font-size:.9rem!important}' +
    '.nd-menu a:hover{background:#ffffff10}' +
    '.nd-head{display:block;padding:8px 10px 2px;font-size:.7rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#8a8a85}' +
    '.m-menu .nd-head{padding:8px 12px 2px}' +
    '.menu-btn{display:none;font:600 .9rem inherit;color:#fff;background:transparent;border:1px solid #ffffff40;border-radius:999px;padding:5px 12px;cursor:pointer}' +
    '.m-menu{background:#0d0e11;border-top:1px solid #ffffff14;padding:6px 16px 14px;max-height:calc(100vh - 120px);overflow-y:auto}' +
    '.m-menu details{border-bottom:1px solid #ffffff12}' +
    '.m-menu summary{padding:12px 0;font-weight:700;color:#fff;cursor:pointer}' +
    '.m-menu a{display:block;padding:8px 12px;color:#c9c9c4;text-decoration:none}' +
    '.m-menu a.m-top{padding:12px 0;font-weight:700;color:#fff}' +
    '.m-menu a[aria-current="page"]{color:#F5B800}' +
    '.m-follow{display:flex;flex-wrap:wrap;gap:4px;margin:10px 0 0}.m-follow a{padding:6px 10px!important;font-size:.85rem}' +
    '@media (max-width:859px){.topbar nav[aria-label="Pages"]{display:none!important}.menu-btn{display:inline-block}' +
    '.topbar-in:has(nav[aria-label="Pages"]){flex-wrap:nowrap!important;height:64px!important;padding-top:0!important}' +
    '.nav-cta .x-link,.nav-cta .web-btn{display:none}.topbar nav.m-menu:not([hidden]){display:block}.brand{flex:none}main.ext{padding-top:120px!important}html.has-subnav main.ext{padding-top:max(160px,calc(var(--nav-h,0px) + 36px))!important}html.has-subnav .topbar{position:absolute}}' +
    '@media (min-width:860px){.m-menu{display:none!important}}' +
    // Paper pages (body.paper: /themes, /b-creative, ...): the Menu button and phone menu in ink, not white.
    'body.paper .menu-btn{color:var(--ink,#111);border-color:var(--ink,#111)}body.paper .m-menu{background:var(--sheet,#fff);border-top-color:var(--hair,#d9d6ce)}body.paper .m-menu details{border-bottom-color:var(--hair,#d9d6ce)}body.paper .m-menu summary,body.paper .m-menu a.m-top{color:var(--ink,#111)}body.paper .m-menu a{color:var(--muted,#5d5b56)}' +
    (store ? '.nd-menu,.m-menu{background:#F5B800!important}.nd-menu a,.m-menu a,.m-menu summary{color:#010101!important}.menu-btn{color:#010101;border-color:#0006}' +
      '.topbar .sub-nav a[aria-current="page"]{color:#F5B800!important;background:#010101!important;border-color:#010101!important}' +
      '.nav-cta .x-link{color:#010101!important;border-color:rgba(0,0,0,.35)!important}.nav-cta .x-link:hover{background:#010101;color:#F5B800!important}' : '');
  document.head.appendChild(css);
})();
