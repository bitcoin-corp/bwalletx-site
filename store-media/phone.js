// Fills every <div class="ph THEME" data-art="/store-media/icon-x-512.png"> with a demo wallet home screen.
(function () {
  var base = (document.currentScript && document.currentScript.src.replace(/phone\.js.*$/, '')) || '/store-media/';
  document.querySelectorAll('.ph').forEach(function (p) {
    var art = p.getAttribute('data-art');
    p.innerHTML = '<div class="scr" aria-hidden="true">' +
      '<div class="ic"><i></i><i></i><i></i><i></i><i></i></div>' +
      '<div class="cd">' + (art ? '<img class="art" alt="" src="' + base + art + '">' : '') +
      '<small>demo@bwalletx.com</small><b>$128.40</b><span>687,744 sats</span><div class="ad">1DemoX…7Qk9</div></div>' +
      '<div class="bt"><span>Send</span><span>Receive</span><span>Mint</span></div>' +
      '<div class="tk">Tokens</div>' +
      '<div class="row"><i></i>BSV<em>$128.40</em></div>' +
      '<div class="dock"><span class="on">Wallet</span><span>Exchange</span><span class="b">b</span><span>Feed</span><span>Chat</span></div>' +
      '</div>';
  });
})();
