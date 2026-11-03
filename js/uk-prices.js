/* UK visitors also see prices in pounds.
 * USD is always shown. GBP prices sit in <span class="gbp" hidden>…</span> and are revealed when the
 * browser's time zone is a UK one. No network calls, no cookies; without JS everyone sees USD.
 * ?cur=gbp / ?cur=usd forces either view (for checking and screenshots). */
(function () {
  var UK = ['Europe/London', 'Europe/Belfast', 'Europe/Guernsey', 'Europe/Isle_of_Man', 'Europe/Jersey', 'GB', 'GB-Eire'];
  var force = null, tz = '';
  try { force = (new URLSearchParams(location.search).get('cur') || '').toLowerCase(); } catch (e) { /* old browser */ }
  try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) { /* no Intl */ }
  var show = force === 'gbp' || (force !== 'usd' && UK.indexOf(tz) !== -1);
  if (!show) return;
  document.documentElement.classList.add('uk-prices');
  var reveal = function () { [].forEach.call(document.querySelectorAll('.gbp'), function (el) { el.hidden = false; }); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', reveal); else reveal();
})();
