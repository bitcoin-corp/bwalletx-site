/* "Start your store" on /store (18 Oct 2026).
 * Sign in with bWalletX (extension / in-app browser, else phone pairing by QR) using @bwalletx/connect 0.2.0,
 * then every call to the shop server is signed by the wallet's identity key: BRC-43 protocol [2,'bwalletx shop'],
 * keyID '1', counterparty 'anyone', over 'bwalletx-shop|v1|<action>|k=v|…' (server: bwalletX site/lib/webShops.js).
 * Nothing secret leaves the wallet. The preview works without signing in; the text fields are kept on this device. */
(function () {
  'use strict';
  var API = '/api/shops/';
  var PROTOCOL = [2, 'bwalletx shop'];
  var KEY = 'bwx.store.draft.v1';
  var HANDLE_RE = /^[a-z0-9](?:[a-z0-9-]{1,28}[a-z0-9])$/;
  var LIMITS = { logo: { w: 512, h: 512, type: 'image/png', max: 1024 * 1024 }, banner: { w: 1500, h: 500, type: 'image/jpeg', max: 2 * 1024 * 1024 } };
  var $ = function (id) { return document.getElementById(id); };

  var state = { wallet: null, identityKey: null, files: { logo: null, banner: null }, refs: { logo: null, banner: null }, pairAbort: null, serverOpen: true };

  // ---------- small helpers ----------
  function toHex(arr) { var s = ''; for (var i = 0; i < arr.length; i++) s += (arr[i] & 255).toString(16).padStart(2, '0'); return s; }
  function utf8(str) { return Array.from(new TextEncoder().encode(str)); }
  function b64(buf) { var b = new Uint8Array(buf), s = ''; for (var i = 0; i < b.length; i += 0x8000) s += String.fromCharCode.apply(null, b.subarray(i, i + 0x8000)); return btoa(s); }
  function sha256Hex(buf) { return crypto.subtle.digest('SHA-256', buf).then(function (d) { return toHex(new Uint8Array(d)); }); }
  function msg(el, text, kind) { el.textContent = text || ''; el.className = 'hint' + (kind ? ' ' + kind : ''); }
  function handleOf(v) { return String(v || '').trim().toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/-{2,}/g, '-').replace(/^-+/, '').slice(0, 30); }
  function short(k) { return k.slice(0, 8) + '…' + k.slice(-6); }

  // ---------- preview ----------
  var f = { name: $('f-name'), handle: $('f-handle'), blurb: $('f-blurb'), accent: $('f-accent'), bg: $('f-bg'), logo: $('f-logo'), banner: $('f-banner') };
  var handleTouched = false;

  function luminance(hex) {
    var n = parseInt(hex.slice(1), 16), r = (n >> 16) / 255, g = ((n >> 8) & 255) / 255, b = (n & 255) / 255;
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  }
  function render() {
    var pv = $('pv'), acc = f.accent.value, bg = f.bg.value, light = luminance(bg) > 0.6;
    pv.style.setProperty('--acc', acc);
    pv.style.setProperty('--bg', bg);
    pv.style.setProperty('--tx', light ? '#111' : '#fff');
    pv.style.setProperty('--mu', light ? '#5d5b56' : '#a7adb8');
    pv.style.setProperty('--sf', light ? '#ffffff' : 'color-mix(in srgb, ' + bg + ' 82%, #fff 8%)');
    pv.style.setProperty('--ln', light ? '#d9d6cc' : 'color-mix(in srgb, ' + acc + ' 28%, #222)');
    $('pv-name').textContent = f.name.value.trim() || 'Your shop';
    $('pv-blurb').textContent = f.blurb.value.trim() || 'A line about what you make.';
    var h = handleOf(f.handle.value);
    $('pv-url').textContent = 'bwalletx.com/shop/' + (h || '…');
    var ban = state.files.banner ? state.files.banner.url : state.refs.banner && state.refs.banner.url;
    $('pv-ban').style.backgroundImage = ban ? 'url("' + ban + '")' : '';
    var logo = state.files.logo ? state.files.logo.url : state.refs.logo && state.refs.logo.url;
    $('pv-logo').src = logo || 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
    $('pv-logo').style.background = logo ? '#000' : acc;
  }
  function remember() {
    try { localStorage.setItem(KEY, JSON.stringify({ name: f.name.value, handle: f.handle.value, blurb: f.blurb.value, accent: f.accent.value, bg: f.bg.value })); } catch (e) { /* private mode */ }
  }
  function restore() {
    try {
      var d = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (!d) return;
      f.name.value = d.name || ''; f.handle.value = d.handle || ''; f.blurb.value = d.blurb || '';
      if (/^#[0-9a-f]{6}$/i.test(d.accent)) f.accent.value = d.accent;
      if (/^#[0-9a-f]{6}$/i.test(d.bg)) f.bg.value = d.bg;
      handleTouched = !!d.handle;
    } catch (e) { /* ignore */ }
  }

  f.name.addEventListener('input', function () {
    if (!handleTouched) f.handle.value = handleOf(f.name.value);
    render(); remember(); checkHandleSoon();
  });
  f.handle.addEventListener('input', function () { handleTouched = true; render(); remember(); checkHandleSoon(); });
  f.handle.addEventListener('blur', function () { f.handle.value = handleOf(f.handle.value).replace(/-+$/, ''); render(); });
  [f.blurb, f.accent, f.bg].forEach(function (el) { el.addEventListener('input', function () { render(); remember(); }); });
  document.querySelectorAll('.sx .sw').forEach(function (sw) {
    sw.addEventListener('click', function (e) {
      var c = e.target && e.target.style && e.target.style.getPropertyValue('--c');
      if (!c) return;
      $(sw.getAttribute('data-for')).value = c.trim();
      render(); remember();
    });
  });

  // Pictures: cropped to the shop's sizes in the browser, so uploads stay small.
  function crop(file, kind) {
    var L = LIMITS[kind];
    return new Promise(function (resolve, reject) {
      if (!/^image\/(png|jpeg|webp)$/.test(file.type)) return reject(new Error('Use a PNG, JPG or WebP picture.'));
      var img = new Image(), url = URL.createObjectURL(file);
      img.onload = function () {
        var c = document.createElement('canvas'); c.width = L.w; c.height = L.h;
        var s = Math.max(L.w / img.naturalWidth, L.h / img.naturalHeight), w = img.naturalWidth * s, h = img.naturalHeight * s;
        var x = c.getContext('2d');
        if (L.type === 'image/jpeg') { x.fillStyle = '#000'; x.fillRect(0, 0, L.w, L.h); }
        x.drawImage(img, (L.w - w) / 2, (L.h - h) / 2, w, h);
        URL.revokeObjectURL(url);
        c.toBlob(function (blob) {
          if (!blob) return reject(new Error("Couldn't read that picture."));
          if (blob.size > L.max) return reject(new Error('That picture is too big after resizing. Try a simpler one.'));
          resolve({ blob: blob, type: L.type, url: URL.createObjectURL(blob) });
        }, L.type, 0.88);
      };
      img.onerror = function () { URL.revokeObjectURL(url); reject(new Error("Couldn't read that picture.")); };
      img.src = url;
    });
  }
  ['logo', 'banner'].forEach(function (kind) {
    f[kind].addEventListener('change', function () {
      var file = f[kind].files && f[kind].files[0];
      if (!file) return;
      crop(file, kind).then(function (r) {
        if (state.files[kind]) URL.revokeObjectURL(state.files[kind].url);
        state.files[kind] = r; render();
      }, function (e) { msg($('save-msg'), e.message, 'bad'); f[kind].value = ''; });
    });
  });

  // ---------- server ----------
  function post(op, body) {
    return fetch(API + op, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok) { var e = new Error(j.error || 'http_' + r.status); e.status = r.status; e.code = j.error || ''; throw e; }
        return j;
      });
    });
  }
  var notOpen = function (e) { return !e.status || e.status === 404 || e.status === 503 || e.status >= 500; };
  var NOT_OPEN = 'Saving drafts opens soon. Your preview and your text are kept on this device for now.';

  function sign(action, fields) {
    var ts = String(Date.now());
    var all = Object.assign({}, fields, { identityKey: state.identityKey, timestamp: ts });
    var line = ['bwalletx-shop', 'v1', action].concat(Object.keys(all).sort().map(function (k) { return k + '=' + (all[k] == null ? '' : all[k]); })).join('|');
    return state.wallet.createSignature({ data: utf8(line), protocolID: PROTOCOL, keyID: '1', counterparty: 'anyone' }).then(function (r) {
      return { identityKey: state.identityKey, timestamp: Number(ts), fields: fields, signature: toHex(r.signature) };
    });
  }

  var checkTimer = null;
  function checkHandleSoon() { clearTimeout(checkTimer); checkTimer = setTimeout(checkHandle, 450); }
  function checkHandle() {
    var h = handleOf(f.handle.value), el = $('handle-msg');
    if (!h) return msg(el, '3–30 letters, numbers and dashes.');
    if (!HANDLE_RE.test(h)) return msg(el, '3–30 letters, numbers and dashes (not at the ends).', 'bad');
    if (!state.serverOpen) return msg(el, 'bwalletx.com/shop/' + h);
    post('check', { handle: h, identityKey: state.identityKey || '' }).then(function (r) {
      if (handleOf(f.handle.value) !== h) return;
      if (r.available) msg(el, 'bwalletx.com/shop/' + h + ' is free.', 'good');
      else msg(el, r.reason === 'reserved' ? 'That name is kept for us or a brand. Try another.' : r.reason === 'taken' ? 'That name is taken. Try another.' : '3–30 letters, numbers and dashes.', 'bad');
    }, function (e) { if (notOpen(e)) { state.serverOpen = false; msg(el, 'bwalletx.com/shop/' + h); } });
  }

  // ---------- sign in ----------
  function signedIn() {
    $('signin-box').hidden = true; $('pair-box').hidden = true; $('who').hidden = false;
    $('who-key').textContent = short(state.identityKey);
    msg($('signin-msg'), 'Loading your shop…');
    sign('shop-mine', {}).then(function (b) { return post('mine', b); }).then(function (r) {
      state.serverOpen = true;
      if (r.shop) {
        var s = r.shop;
        f.name.value = s.name || ''; f.handle.value = s.handle || ''; f.blurb.value = s.blurb || '';
        if (s.colours) { f.accent.value = s.colours.accent || f.accent.value; f.bg.value = s.colours.background || f.bg.value; }
        state.refs.logo = s.logo; state.refs.banner = s.banner; handleTouched = true;
        render(); remember();
        msg($('signin-msg'), 'Your draft is loaded. Status: ' + s.status + '.', 'good');
      } else msg($('signin-msg'), 'No shop yet on this wallet. Fill in the form and save.', 'good');
    }, function (e) {
      if (notOpen(e)) { state.serverOpen = false; msg($('signin-msg'), NOT_OPEN); }
      else msg($('signin-msg'), e.code === 'Bad signature' ? "The wallet's signature didn't check out. Try again." : 'Couldn’t load your shop (' + e.message + ').', 'bad');
    });
  }
  function useWallet(w) {
    state.wallet = w;
    var ready = typeof w.waitForAuthentication === 'function' ? w.waitForAuthentication({}) : Promise.resolve();
    return ready.then(function () { return w.getPublicKey({ identityKey: true }); }).then(function (r) {
      state.identityKey = String(r.publicKey).toLowerCase(); signedIn();
    });
  }
  function startPairing(C) {
    var box = $('pair-box'); box.hidden = false; $('signin-box').hidden = true;
    $('pair-qr').innerHTML = ''; $('pair-link').textContent = ''; $('pair-code').textContent = '';
    state.pairAbort = typeof AbortController === 'function' ? new AbortController() : null;
    var asking = false;
    return C.pairBwalletX({
      signal: state.pairAbort ? state.pairAbort.signal : undefined,
      onLink: function (link) {
        $('pair-link').textContent = link;
        if (window.qrcode) { var q = window.qrcode(0, 'M'); q.addData(link); q.make(); $('pair-qr').innerHTML = q.createSvgTag({ cellSize: 4, margin: 0 }); }
      },
      // Shown by every connect version; 0.5.5+ also asks (confirmCode below) and waits for the yes.
      // 0.5.5 asks before it shows, so don't overwrite the question's buttons.
      onCode: function (code) { if (asking) return; $('pair-code').innerHTML = 'Check bWalletX shows <b>' + String(code).replace(/[^0-9]/g, '') + '</b>, then tap Connect.'; },
      // Asked, not just shown: pairing finishes only on a yes here and Connect in bWalletX.
      confirmCode: function (code) {
        asking = true;
        var el = $('pair-code');
        el.innerHTML = 'Does bWalletX show <b>' + String(code).replace(/[^0-9]/g, '') + '</b>? ';
        return new Promise(function (resolve) {
          var no = document.createElement('button'); no.type = 'button'; no.textContent = 'No';
          var yes = document.createElement('button'); yes.type = 'button'; yes.textContent = 'Yes, it matches';
          no.onclick = function () { el.textContent = "The codes didn't match, so nothing was connected."; resolve(false); };
          yes.onclick = function () { el.textContent = 'Now tap Connect in bWalletX.'; resolve(true); };
          el.append(no, ' ', yes);
        });
      },
    });
  }
  function connect() {
    var C = window.bWalletXConnect;
    if (!C) return msg($('signin-msg'), 'Still loading. Try again in a second.', 'bad');
    msg($('signin-msg'), 'Looking for bWalletX…');
    C.discoverBwalletX(1200).then(function (found) {
      if (found) return useWallet(found.wallet);
      msg($('signin-msg'), '');
      return startPairing(C).then(useWallet);
    }).catch(function (e) {
      $('pair-box').hidden = true; $('signin-box').hidden = false;
      if (e && e.name === 'AbortError') return msg($('signin-msg'), '');
      msg($('signin-msg'), 'Sign-in stopped: ' + ((e && e.message) || 'no answer from the wallet') + '. No bWalletX yet? Get it at bwalletx.com/get.', 'bad');
    });
  }
  document.addEventListener('bwalletx-signin', function (e) {
    if (!e.target || e.target.id !== 'signin') return;
    e.preventDefault(); connect();
  });
  $('pair-cancel').addEventListener('click', function () { if (state.pairAbort) state.pairAbort.abort(); $('pair-box').hidden = true; $('signin-box').hidden = false; });
  $('signout').addEventListener('click', function () {
    if (state.wallet && typeof state.wallet.close === 'function') state.wallet.close();
    state.wallet = null; state.identityKey = null; state.refs = { logo: null, banner: null };
    $('who').hidden = true; $('signin-box').hidden = false; msg($('signin-msg'), 'Signed out.'); render();
  });

  // ---------- save ----------
  function upload(kind) {
    var file = state.files[kind];
    if (!file) return Promise.resolve(state.refs[kind]);
    return file.blob.arrayBuffer().then(function (buf) {
      return sha256Hex(buf).then(function (sha) {
        return sign('shop-upload', { kind: kind, type: file.type, sha256: sha }).then(function (b) { b.data = b64(buf); return post('upload', b); });
      });
    }).then(function (ref) { state.refs[kind] = ref; return ref; });
  }
  var ERRORS = {
    handle_taken: 'That web address is taken. Try another.',
    handle_reserved: 'That web address is kept for us or a brand. Try another.',
    handle_locked: 'Your shop is being reviewed, so its web address is fixed. Ask b to change it.',
    'rate-limited': 'Slow down a moment, then try again.',
  };
  $('shop-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var out = $('save-msg'), name = f.name.value.trim(), handle = handleOf(f.handle.value).replace(/-+$/, '');
    if (name.length < 2) return msg(out, 'Give your shop a name (2–40 characters).', 'bad');
    if (!HANDLE_RE.test(handle)) return msg(out, 'Pick a web address: 3–30 letters, numbers and dashes.', 'bad');
    if (!state.wallet) { msg(out, 'Sign in first (step 1), so the shop belongs to your wallet.', 'bad'); $('signin-box').scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
    if (!state.serverOpen) return msg(out, NOT_OPEN);
    var btn = $('save'); btn.disabled = true; msg(out, 'Approve in your wallet to save…');
    upload('logo').then(function () { return upload('banner'); }).then(function () {
      var fields = {
        handle: handle, name: name, blurb: f.blurb.value.trim(),
        colours: JSON.stringify({ accent: f.accent.value, background: f.bg.value }),
        logo: state.refs.logo ? JSON.stringify({ path: state.refs.logo.path, type: state.refs.logo.type, size: state.refs.logo.size }) : '',
        banner: state.refs.banner ? JSON.stringify({ path: state.refs.banner.path, type: state.refs.banner.type, size: state.refs.banner.size }) : '',
      };
      return sign('shop-save', fields).then(function (b) { return post('save', b); });
    }).then(function (r) {
      state.files = { logo: null, banner: null };
      state.refs.logo = r.shop.logo; state.refs.banner = r.shop.banner;
      render(); remember();
      msg(out, 'Draft saved. bwalletx.com/shop/' + r.shop.handle + ' is yours. Only you can see it until shops open.', 'good');
    }).catch(function (err) {
      if (notOpen(err)) { state.serverOpen = false; return msg(out, NOT_OPEN); }
      msg(out, ERRORS[err.code] || (err.code && err.code.indexOf(':') > 0 ? err.code.replace(/^[a-z]+: /, '') : 'Not saved: ' + err.message), 'bad');
    }).then(function () { btn.disabled = false; });
  });

  restore();
  render();
  if (f.handle.value) checkHandleSoon();
})();
