/* Explainer lightbox: loads the video only when opened. Wide on desktop, tall on phones. */
(function () {
  var btn = document.querySelector('[data-explainer]');
  var dlg = document.getElementById('explainer');
  if (!btn || !dlg || typeof dlg.showModal !== 'function') return;
  var video = dlg.querySelector('video');
  var closeBtn = dlg.querySelector('.vbox-close');
  var tall = window.matchMedia('(max-width: 720px), (orientation: portrait) and (max-width: 900px)');
  var opener = null;

  function pick() {
    var t = tall.matches;
    var src = t ? video.dataset.tall : video.dataset.wide;
    video.poster = t ? video.dataset.posterTall : video.dataset.posterWide;
    if (video.getAttribute('src') !== src) video.src = src;
  }
  function open(e) {
    if (e) e.preventDefault();
    opener = document.activeElement;
    pick();
    dlg.showModal();
    closeBtn.focus();
    var p = video.play();
    if (p && p.catch) p.catch(function () {});
  }
  function close() {
    if (dlg.open) dlg.close();
  }
  btn.addEventListener('click', open);
  closeBtn.addEventListener('click', close);
  dlg.addEventListener('close', function () {
    video.pause();
    if (opener && opener.focus) opener.focus();
  });
  dlg.addEventListener('click', function (e) {
    if (e.target === dlg || e.target.classList.contains('vbox-in')) close();
  });
  // Focus trap: only the close button and the video are focusable.
  dlg.addEventListener('keydown', function (e) {
    if (e.key !== 'Tab') return;
    var f = [closeBtn, video];
    var i = f.indexOf(document.activeElement);
    e.preventDefault();
    f[(i + (e.shiftKey ? f.length - 1 : 1)) % f.length].focus();
  });
})();
