#!/usr/bin/env python3
"""Build /migrate/invite/<service>: one template, one page and one share card per service.

    python3 scripts/migrate-invite.py          # writes migrate/invite/<slug>.html and og/migrate-invite-<slug>-<OG_VER>.png
    python3 scripts/migrate-invite.py --no-og  # pages only
    python3 scripts/migrate-invite.py --check  # verify the generated pages match SERVICES (no writes)

Also rewrites the services grid in migrate.html between the MIGRATE-INVITE markers.
Only X has a live import on bChatX. Every other service says "import coming soon";
never mark one live until bChatX actually ships its import.
"""
import html
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OG_VER = 'v1'
CHROME = os.environ.get('CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
BCHATX_HUB = 'https://www.bchatx.com/migrate'

# (slug, display name, bChatX import live?)
SERVICES = [
    ('x', 'X', True),
    ('instagram', 'Instagram', False),
    ('tiktok', 'TikTok', False),
    ('youtube', 'YouTube', False),
    ('reddit', 'Reddit', False),
    ('linkedin', 'LinkedIn', False),
    ('facebook', 'Facebook', False),
    ('threads', 'Threads', False),
    ('bluesky', 'Bluesky', False),
    ('pinterest', 'Pinterest', False),
    ('twetch', 'Twetch', False),
    ('treechat', 'Treechat', False),
]


def bchatx_import(slug):
    # bChatX puts the service before "invite".
    return f'https://www.bchatx.com/migrate/{slug}/invite'


def og_name(slug):
    return f'og/migrate-invite-{slug}-{OG_VER}.png'


def tagline(name):
    return f'Move from {name} to bWalletX: your posts, your name and your followers, owned by you.'


def page(slug, name, live):
    e = html.escape
    title = f'Move from {name} to bWalletX'
    desc = tagline(name)
    url = f'https://bwalletx.com/migrate/invite/{slug}'
    img = f'https://bwalletx.com/{og_name(slug)}'
    if live:
        step2 = (f'<li><b>Bring your {e(name)} posts</b>Open bChatX&rsquo;s {e(name)} import, choose your archive and approve in bWalletX. '
                 f'Your posts are signed with your own key.</li>')
        cta2 = f'<a class="mi-btn mi-line" data-ref href="{bchatx_import(slug)}" rel="noopener">Import from {e(name)} on bChatX</a>'
        status = '<span class="tag live">Import live</span>'
    else:
        step2 = (f'<li><b>{e(name)} import: coming soon</b>bChatX doesn&rsquo;t import from {e(name)} yet. '
                 f'Get bWalletX now and claim your name; we&rsquo;ll show the import here when it ships.</li>')
        cta2 = f'<a class="mi-btn mi-line" href="{BCHATX_HUB}" rel="noopener">See what bChatX imports today</a>'
        status = '<span class="tag soon">Import coming soon</span>'
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{e(title)}</title>
    <link rel="canonical" href="{url}" />
    <meta name="description" content="{e(desc)}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{url}" />
    <meta property="og:site_name" content="bWalletX" />
    <meta property="og:title" content="{e(title)}" />
    <meta property="og:description" content="Your posts, your name and your followers, owned by you." />
    <meta property="og:image" content="{img}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="{e(title)}: your posts, your name and your followers, owned by you." />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bWalletX" />
    <meta name="twitter:title" content="{e(title)}" />
    <meta name="twitter:description" content="Your posts, your name and your followers, owned by you." />
    <meta name="twitter:image" content="{img}" />
    <link rel="icon" href="/favicon.ico" />
    <link rel="stylesheet" href="/styles.css" />
    <link rel="stylesheet" href="/migrate-invite.css" />
  </head>
  <body>
    <div class="beta-banner">bWalletX is in <strong>beta</strong>: test with small amounts.</div>
    <header class="topbar">
      <div class="wrap topbar-in">
        <a class="brand" href="/"><img src="/logo.svg" alt="" width="34" height="30" /><span>bWallet<span class="gold">X</span></span></a>
        <nav aria-label="Pages">
          <a href="/features">Features</a><a href="/exchange">Exchange</a><a href="/social">Social</a><a href="/agent">Agents</a><a href="/extension">Extension</a><a href="/developers">Developers</a>
        </nav>
        <span class="nav-cta"><a class="dl-btn" href="/get">Download</a><a class="web-btn" href="https://web.bwalletx.com" target="_blank" rel="noopener">Web &rarr;</a></span>
      </div>
    </header>
    <script src="/nav.js"></script>
    <main class="mg mi" data-service="{slug}">
      <p class="kicker"><a href="/migrate">Move to bWalletX</a> &rsaquo; {e(name)}</p>
      <p class="invited" id="invited" hidden></p>
      <h1>Move from {e(name)} <span class="gold">to bWalletX.</span></h1>
      <p class="lede">Your posts, your name and your followers, owned by you.</p>
      <p>{status}</p>
      <ol class="mi-steps">
        <li><b>Get bWalletX</b>Your wallet is your account: one key that signs your posts and holds your name. No password, nothing to lose to a platform.</li>
        {step2}
        <li><b>Bring your people</b>Share this page with the people you follow on {e(name)} so they can move too.</li>
      </ol>
      <div class="mi-row"><a class="mi-btn mi-gold" data-ref href="/get">Get bWalletX</a>{cta2}</div>
      <section class="share" aria-labelledby="share-h">
        <h2 id="share-h">Invite your {e(name)} friends</h2>
        <div class="share-row"><input id="share-url" readonly aria-label="Invite link" value="{url}" /><button type="button" id="copy">Copy link</button></div>
        <a class="mi-btn mi-line" id="post-x" href="#" target="_blank" rel="noopener" data-text="{e(title)}: your posts, your name and your followers, owned by you.">Post to X</a>
        <p class="small" id="copied" role="status"></p>
      </section>
      <p class="small">Other services are named only to say where you can move from; bWalletX isn&rsquo;t affiliated with them. <a href="/migrate">All services</a> · <a href="/invite">Invite someone to bWalletX</a></p>
    </main>
    <script src="/invite.js"></script>
  </body>
</html>
'''


def grid():
    cards = []
    for slug, name, live in SERVICES:
        tag = '<span class="tag live">Import live</span>' if live else '<span class="tag soon">Coming soon</span>'
        cards.append(f'          <a class="svc{"" if live else " soon"}" href="/migrate/invite/{slug}"><b>{html.escape(name)}</b>{tag}</a>')
    return '\n'.join(cards)


def og_html(name, live):
    e = html.escape
    status = 'Import live on bChatX' if live else 'Import coming soon'
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
body{{background:#f7f5ef;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;color:#111;position:relative}}
.k{{position:absolute;left:80px;top:72px;font-size:26px;font-weight:800;letter-spacing:.08em;color:#9a6c00}}
h1{{position:absolute;left:80px;top:120px;width:1040px;margin:0;font-size:92px;line-height:1.02;letter-spacing:-.035em}}
h1 span{{color:#9a6c00}}
p{{position:absolute;left:80px;top:372px;width:960px;margin:0;font-size:38px;line-height:1.3;color:#333}}
.tag{{position:absolute;left:80px;bottom:72px;font-size:26px;font-weight:800;padding:12px 24px;border-radius:999px;background:{"#F5B800" if live else "#ece7da"};color:{"#000" if live else "#6b5a2e"}}}
.u{{position:absolute;right:80px;bottom:82px;font-size:30px;font-weight:700}}
.u span{{color:#9a6c00}}
</style></head><body>
<div class="k">Move to bWalletX</div>
<h1>Move from {e(name)}<br><span>to bWalletX.</span></h1>
<p>Your posts, your name and your followers, owned by you.</p>
<div class="tag">{status}</div>
<div class="u">bWallet<span>X</span>.com</div>
</body></html>'''


def render_og(slug, name, live):
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
        f.write(og_html(name, live))
        src = f.name
    try:
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=1200,630',
                        f'--screenshot={os.path.join(ROOT, og_name(slug))}', f'file://{src}'],
                       check=True, capture_output=True, timeout=60)
    finally:
        os.unlink(src)


MARK = re.compile(r'(<!-- MIGRATE-INVITE:START -->)[\s\S]*?(<!-- MIGRATE-INVITE:END -->)')


def main():
    check = '--check' in sys.argv
    out_dir = os.path.join(ROOT, 'migrate', 'invite')
    mig_path = os.path.join(ROOT, 'migrate.html')
    mig = open(mig_path, encoding='utf8').read()
    if not MARK.search(mig):
        sys.exit('migrate.html has no MIGRATE-INVITE markers')
    new_mig = MARK.sub(lambda m: m.group(1) + '\n' + grid() + '\n' + m.group(2), mig)
    bad = []
    for slug, name, live in SERVICES:
        p = os.path.join(out_dir, f'{slug}.html')
        want = page(slug, name, live)
        if check:
            if not os.path.exists(p) or open(p, encoding='utf8').read() != want:
                bad.append(p)
            if not os.path.exists(os.path.join(ROOT, og_name(slug))):
                bad.append(og_name(slug))
            continue
        os.makedirs(out_dir, exist_ok=True)
        open(p, 'w', encoding='utf8').write(want)
        if '--no-og' not in sys.argv:
            render_og(slug, name, live)
    if check:
        if new_mig != mig:
            bad.append('migrate.html grid')
        if bad:
            sys.exit('out of date (run scripts/migrate-invite.py): ' + ', '.join(bad))
        print(f'ok: {len(SERVICES)} migrate invite pages up to date')
        return
    open(mig_path, 'w', encoding='utf8').write(new_mig)
    print(f'wrote {len(SERVICES)} pages to migrate/invite/ and the grid in migrate.html')


if __name__ == '__main__':
    main()
