// bwalletx.com/testers: Google sign-in (pay.bwallet.space social.js, return_to "testers"), apply, status.
// Server: push.bwalletx.com /v1/testers/* (bwalletx-push src/testers).
(() => {
  const API = 'https://push.bwalletx.com/v1/testers';
  const SOCIAL = 'https://pay.bwallet.space/api/social';
  const PLAY_OPT_IN = 'https://play.google.com/apps/testing/com.bitcoincorp.bwallet';
  const box = document.getElementById('app');
  const ls = {
    get: (k) => { try { return localStorage.getItem(k); } catch { return null; } },
    set: (k, v) => { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, v); } catch {} },
  };
  const ss = {
    get: (k) => { try { return sessionStorage.getItem(k); } catch { return null; } },
    set: (k, v) => { try { v == null ? sessionStorage.removeItem(k) : sessionStorage.setItem(k, v); } catch {} },
  };
  const el = (t, a = {}, ...kids) => {
    const e = document.createElement(t);
    for (const [k, v] of Object.entries(a)) k === 'class' ? (e.className = v) : k.startsWith('on') ? e.addEventListener(k.slice(2), v) : e.setAttribute(k, v);
    for (const c of kids) if (c != null) e.append(c);
    return e;
  };
  const show = (...kids) => box.replaceChildren(...kids.filter((k) => k != null));
  const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');

  async function places() {
    try {
      const p = await fetch(API + '/places').then((r) => r.json());
      document.getElementById('places').textContent = p.remaining > 0 ? `${p.remaining} of ${p.total} places left` : `All ${p.total} places are taken`;
      return p;
    } catch { return null; }
  }

  async function signIn() {
    const secret = hex(crypto.getRandomValues(new Uint8Array(32)));
    ss.set('testerSecret', secret);
    const vh = hex(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(secret)));
    try {
      const r = await fetch(SOCIAL + '/start', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ provider: 'google', verifier_hash: vh, return_to: 'testers' }) });
      const j = await r.json();
      if (!j.authorizeUrl) throw new Error(j.error || 'Google sign-in is not available right now.');
      location.href = j.authorizeUrl;
    } catch (e) { signedOut(e.message); }
  }

  function signedOut(error) {
    show(
      el('p', {}, 'Apply with the Google account you use on your Android phone. Google tells us your email, name and photo; nothing else.'),
      error ? el('p', { class: 'err' }, error) : null,
      el('button', { class: 'btn btn-store', onclick: signIn }, 'Sign in with Google to apply'),
    );
  }

  const authed = (path, body) => fetch(API + path, {
    method: body ? 'POST' : 'GET',
    headers: { authorization: 'Bearer ' + ls.get('testerToken'), 'content-type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  }).then(async (r) => ({ ok: r.ok, status: r.status, j: await r.json().catch(() => ({})) }));

  const who = (me) => el('div', { class: 'me' }, me.photo ? el('img', { src: me.photo, alt: '', referrerpolicy: 'no-referrer' }) : null,
    el('div', {}, el('b', {}, me.name || me.email), el('br'), el('span', { class: 'muted' }, me.email), ' · ',
      el('a', { href: '#', onclick: (e) => { e.preventDefault(); ls.set('testerToken', null); signedOut(); } }, 'sign out')));

  function form(me) {
    if (me.places.remaining <= 0) return show(who(me), el('p', {}, 'All 20 places are taken. Sorry: follow @bWalletX in case one opens up.'));
    const device = el('input', { type: 'text', placeholder: 'e.g. Pixel 8, Galaxy S23', maxlength: '80' });
    const x = el('input', { type: 'text', placeholder: '@yourname (optional)', maxlength: '40' });
    const gh = el('input', { type: 'text', placeholder: 'yourname (optional)', maxlength: '60' });
    const addr = el('input', { type: 'text', placeholder: '1…', maxlength: '40', autocomplete: 'off', spellcheck: 'false' });
    const ok = el('input', { type: 'checkbox' });
    const err = el('p', { class: 'err' });
    const send = async () => {
      err.textContent = '';
      const r = await authed('/apply', { device: device.value, x: x.value || null, github: gh.value || null, address: addr.value.trim(), consent: ok.checked });
      if (r.status === 401) return signedOut('Your sign-in expired. Please sign in again.');
      if (!r.ok) { err.textContent = r.j.error || 'Something went wrong. Try again.'; return; }
      load();
    };
    show(who(me),
      el('label', {}, 'Your Android phone model'), device,
      el('label', {}, 'Your bWallet receive address'), addr,
      el('p', { class: 'muted small' }, 'Where I pay you. In bWallet tap Receive and copy the address (starts with 1). Don\'t have bWallet yet? Get the APK from /android to make a wallet now, then switch to the Play version when you\'re approved; your 12 words restore it.'),
      el('label', {}, 'X (optional)'), x,
      el('label', {}, 'GitHub (optional)'), gh,
      el('label', { class: 'chk' }, ok, el('span', {}, 'I\'ll test bWallet on Android for 14 days. I understand payment is not tied to ratings or reviews, one place per person, and the owner approves testers.')),
      err,
      el('button', { class: 'btn btn-store', onclick: send }, 'Apply'));
  }

  function status(me) {
    const a = me.application;
    const kids = [who(me)];
    if (a.status === 'applied') kids.push(el('p', {}, el('b', {}, 'Application received.'), ' I approve testers by hand, usually within a day. Check back here.'));
    if (a.status === 'declined' || a.status === 'removed') kids.push(el('p', {}, 'Sorry, this application wasn\'t approved.'));
    if (a.status === 'approved') {
      const p = me.progress;
      kids.push(
        el('p', {}, el('b', { class: 'gold' }, 'You\'re in.'), ' Your tester code: ', el('code', {}, a.code)),
        el('ol', {},
          el('li', {}, 'Join the test: ', el('a', { href: PLAY_OPT_IN, target: '_blank', rel: 'noopener' }, 'open the Google Play test page'), ' signed in as ', el('b', {}, me.email), '. If it says you\'re not a tester yet, I haven\'t added you to the list; try again later.'),
          el('li', {}, 'Install bWallet from Google Play.'),
          el('li', {}, 'In bWallet: Settings › Testing › enter ', el('code', {}, a.code), '.')),
        p.started
          ? el('div', {}, el('p', {}, el('b', {}, `Day ${p.dayOfWindow} of 14`), ` · ${p.counted} days checked in · ${p.missed} missed`),
            el('div', { class: 'bar' }, el('i', { style: `width:${Math.round((Math.min(p.counted, 12) / 12) * 100)}%` })),
            p.playVerified ? null : el('p', { class: 'err' }, 'Your check-ins aren\'t from the Google Play install yet. Install bWallet from Play to get paid.'),
            !p.canStillComplete && !p.complete ? el('p', { class: 'err' }, 'Too many missed days to reach 12 of 14 now.') : null)
          : el('p', { class: 'muted' }, 'No check-ins yet. Day 1 starts the first time you open the Play version after entering your code.'),
      );
    }
    for (const x of me.payouts || []) kids.push(el('p', {}, `${x.kind === 'first_open' ? 'First open' : '14 days'}: ${x.bsv} BSV · `, x.status === 'paid' ? el('a', { href: `https://whatsonchain.com/tx/${x.txid}`, target: '_blank', rel: 'noopener' }, 'paid') : 'due, I\'ll send it soon'));
    kids.push(el('p', { class: 'muted small' }, 'Paying to ', el('code', {}, a.address)));
    show(...kids);
  }

  async function load() {
    if (!ls.get('testerToken')) return signedOut();
    const r = await authed('/me').catch(() => null);
    if (!r) return show(el('p', { class: 'err' }, 'Can\'t reach the testers server. Try again in a minute.'));
    if (r.status === 401) { ls.set('testerToken', null); return signedOut(); }
    r.j.application ? status(r.j) : form(r.j);
  }

  async function start() {
    places();
    const q = new URLSearchParams(location.hash.slice(1));
    if (q.get('t') || q.get('error')) history.replaceState(null, '', location.pathname);
    if (q.get('error')) return signedOut(q.get('error') === 'cancelled' ? 'Sign-in cancelled.' : q.get('error'));
    if (q.get('t')) {
      if (q.get('p') && q.get('p') !== 'google') return signedOut('Please sign in with Google.');
      const r = await fetch(API + '/session', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ ticket: q.get('t'), secret: ss.get('testerSecret') || '' }) })
        .then(async (x) => ({ ok: x.ok, j: await x.json().catch(() => ({})) })).catch(() => ({ ok: false, j: {} }));
      ss.set('testerSecret', null);
      if (!r.ok) return signedOut(r.j.error || 'Sign-in failed. Please try again.');
      ls.set('testerToken', r.j.token);
    }
    load();
  }
  start();
})();
