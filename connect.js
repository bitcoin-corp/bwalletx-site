/*!
 * bWalletX Connect — drop-in "Connect with bWalletX" for any website.
 * https://bwalletx.com/developers
 *
 *   <script src="https://bwalletx.com/connect.js"></script>
 *   const { wallet, info } = await bWalletX.connect();   // BRC-100 WalletInterface
 *   const r = await bWalletX.signIn({ challenge, pairing }); // sign-in, see bwalletx.com/login.md
 *
 * Finds bWalletX by BRC-100 discovery (brc100:requestWallet → brc100:announceWallet, rdns
 * com.bwalletx.extension), so it is chosen by name even when another wallet (e.g. Yours) also
 * sits on window.CWI. No keys or data pass through bwalletx.com.
 */
(function () {
  'use strict';
  var RDNS = 'com.bwalletx.extension';
  var INSTALL = 'https://bwalletx.com/extension';
  var found = {}; // rdns -> { info, wallet }

  window.addEventListener('brc100:announceWallet', function (e) {
    var d = e.detail;
    if (d && d.info && d.info.rdns && d.wallet) found[d.info.rdns] = d;
  });

  /** Every BRC-100 wallet that answered, after waiting `ms` for replies. */
  function discover(ms) {
    window.dispatchEvent(new Event('brc100:requestWallet'));
    return new Promise(function (r) {
      setTimeout(function () {
        r(Object.keys(found).map(function (k) { return found[k]; }));
      }, ms == null ? 400 : ms);
    });
  }

  /**
   * bWalletX's wallet, authenticated. Rejects with code 'NOT_INSTALLED' if bWalletX isn't there.
   * opts.timeout: ms to wait for the wallet to announce (default 1500).
   */
  function connect(opts) {
    opts = opts || {};
    var deadline = Date.now() + (opts.timeout || 1500);
    return (function poll() {
      return discover(250).then(function () {
        var d = found[RDNS];
        if (d) {
          return d.wallet.waitForAuthentication({}).then(function () {
            return d.wallet.getPublicKey({ identityKey: true }).then(function (r) {
              return { wallet: d.wallet, info: d.info, identityKey: r.publicKey };
            });
          });
        }
        if (Date.now() < deadline) return poll();
        var err = new Error('bWalletX is not installed');
        err.code = 'NOT_INSTALLED';
        err.installUrl = INSTALL;
        throw err;
      });
    })();
  }

  /** Turn any element into a Connect button. onConnect gets { wallet, info, identityKey }. */
  function button(el, onConnect, onError) {
    if (typeof el === 'string') el = document.querySelector(el);
    el.addEventListener('click', function () {
      connect().then(onConnect, function (e) {
        if (e.code === 'NOT_INSTALLED') window.open(INSTALL, '_blank', 'noopener');
        if (onError) onError(e);
      });
    });
    return el;
  }

  // Sign-in and phone pairing live in @bwalletx/connect (about 125 KB with @bsv/sdk). It is
  // loaded from next to this file only when one of these is first called.
  var self = document.currentScript && document.currentScript.src;
  var FULL = new URL('connect/bwalletx-connect.global.js', self || 'https://bwalletx.com/').href;
  var loading = null;
  function load() {
    if (window.bWalletXConnect) return Promise.resolve(window.bWalletXConnect);
    if (!loading) {
      loading = new Promise(function (resolve, reject) {
        var s = document.createElement('script');
        s.src = FULL;
        s.async = true;
        s.onload = function () { resolve(window.bWalletXConnect); };
        s.onerror = function () { loading = null; reject(new Error('Could not load ' + FULL)); };
        document.head.appendChild(s);
      });
    }
    return loading;
  }

  /** signInWithBwalletX from @bwalletx/connect: extension, in-app browser or QR pairing. */
  function signIn(opts) { return load().then(function (m) { return m.signInWithBwalletX(opts); }); }
  /** pairBwalletX from @bwalletx/connect: a wallet paired by QR or pasted link. */
  function pair(opts) { return load().then(function (m) { return m.pairBwalletX(opts); }); }
  /** renderButton from @bwalletx/connect: the gold "Sign in with bWalletX" button. */
  function renderButton(el, opts) { return load().then(function (m) { return m.renderButton(el, opts); }); }

  window.bWalletX = {
    connect: connect, discover: discover, button: button, RDNS: RDNS, INSTALL_URL: INSTALL,
    load: load, signIn: signIn, pair: pair, renderButton: renderButton,
  };
})();
