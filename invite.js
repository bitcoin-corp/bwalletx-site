// /invite and /migrate/invite/<service>: "@handle invited you", ref passed to /get, copy link, post to X.
(function () {
  var clean = function (h) {
    h = String(h || '').trim().replace(/^@+/, '');
    return /^[A-Za-z0-9_]{1,30}$/.test(h) ? h : '';
  };
  var q = new URLSearchParams(location.search);
  var from = clean(q.get('from') || q.get('ref'));
  var withParam = function (href, key, val, full) {
    var u = new URL(href, location.origin);
    if (val) u.searchParams.set(key, val); else u.searchParams.delete(key);
    return full || u.origin !== location.origin ? u.toString() : u.pathname + u.search + u.hash;
  };

  var invited = document.getElementById('invited');
  if (from && invited) {
    invited.textContent = '@' + from + ' invited you';
    invited.hidden = false;
  }
  if (from) {
    document.querySelectorAll('a[data-ref]').forEach(function (a) {
      a.setAttribute('href', withParam(a.getAttribute('href'), 'ref', from));
    });
  }

  var input = document.getElementById('share-url');
  var mine = document.getElementById('my-handle');
  var post = document.getElementById('post-x');
  var base = 'https://bwalletx.com' + location.pathname.replace(/\.html$/, '').replace(/^\/index$/, '/');
  var update = function () {
    var url = withParam(base, 'from', mine ? clean(mine.value) : '', true);
    if (input) input.value = url;
    if (post) {
      post.href = 'https://x.com/intent/post?text=' + encodeURIComponent(post.getAttribute('data-text') || '') +
        '&url=' + encodeURIComponent(url);
    }
  };
  if (mine) mine.addEventListener('input', update);
  update();

  var copy = document.getElementById('copy');
  var said = document.getElementById('copied');
  if (copy && input) {
    copy.addEventListener('click', function () {
      var done = function () { if (said) said.textContent = 'Link copied.'; };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(input.value).then(done, function () { input.select(); document.execCommand('copy'); done(); });
      } else { input.select(); document.execCommand('copy'); done(); }
    });
  }
})();
