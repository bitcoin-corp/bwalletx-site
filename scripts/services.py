#!/usr/bin/env python3
"""Build /services (every b*X.com site we run) and its share image, in the /on-b layout.

    python3 scripts/services.py          # writes services.html and og-services-<OG_VER>.png (headless Chrome)
    python3 scripts/services.py --no-og  # page only

Live = the site is a working product today. Coming = a domain we own with only a holding page, or nothing yet.
Live descriptions come from each site's own <title>/description; Coming ones promise nothing.
Icons are each site's own favicon, saved unmodified under /img/services/ from https://<domain>/favicon.svg
(bChatX: /bchatx-icon.svg, bMusicX: /apple-icon). Checked 25 Oct 2026.
"""
import html
import importlib.util
import os
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_spec = importlib.util.spec_from_file_location('onb', os.path.join(ROOT, 'scripts', 'on-b.py'))
onb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(onb)
OG_VER = 'v1'

# (name, domain, live, one-liner, icon, colour)
SERVICES = [
    ('bChatX', 'bchatx.com', True, 'Chat, rooms and Spaces on Bitcoin. Sign in with bWalletX.', 'bchatx.svg', '#2a6bf2'),
    ('bMailX', 'bmailx.com', True, 'Email that pays: sealed letters with paid stamps, and your own price to reach you.', 'bmailx.svg', '#e0263a'),
    ('bCalX', 'bcalx.com', True, 'What&rsquo;s on, live: the calendar of live audio Spaces on bChatX.', 'bcalx.svg', '#0ea5e9'),
    ('bRadioX', 'bradiox.com', True, 'Radio you can join: listen in the bRadio Lounge and raise your hand to speak.', 'bradiox.svg', '#f97316'),
    ('bNewsX', 'bnewsx.com', True, 'The news market: headlines you discuss on chain in the bWalletX Feed.', 'bnewsx.svg', '#64748b'),
    ('bMusicX', 'bmusicx.com', True, 'The Bitcoin Music Exchange: stream by the second, and every second pays the artist.', 'bmusicx.png', '#db2777'),
    ('bWriterX', 'bwriterx.com', True, 'Write it down. Keep it forever. Bitcoin Writer saves each version to Bitcoin.', 'bwriterx.svg', '#16a34a'),
    ('bMintX', 'bmintx.com', True, 'You made it. Prove it&rsquo;s yours. Timestamp what you make on Bitcoin, in your own name.', 'bmintx.svg', '#7c3aed'),
    ('bStoreX', 'bstorex.com', True, 'Sell digital things, paid in Bitcoin. Themes sell today, each with a signed receipt.', 'bstorex.svg', '#ca8a04'),
    ('bVideoX', 'bvideox.com', True, 'Your channel, owned by you: bring your YouTube channel to Bitcoin.', 'bvideox.svg', '#dc2626'),
    ('bJobsX', 'bjobsx.com', True, 'Your work history, in your own wallet: import your LinkedIn export and choose what shows.', 'bjobsx.svg', '#0a66c2'),
    ('bFriendsX', 'bfriendsx.com', True, 'Bring your people with you: find who you know on Bitcoin and invite the rest.', 'bfriendsx.svg', '#06b6d4'),
    ('bAdvertisingX', 'badvertisingx.com', True, 'Tell b about your business and get the ad, for one fixed price in Bitcoin.', 'badvertisingx.svg', '#e11d48'),
    ('bMessageX', 'bmessagex.com', True, 'Channels and direct messages for your team and your community, Slack-style, on your bChatX rooms. Sign in with bWalletX.', 'bmessagex.svg', '#4f46e5'),
    ('bMoviesX', 'bmoviesx.com', False, '', 'bmoviesx.svg', '#9333ea'),
    ('bDriveX', 'bdrivex.com', False, '', 'bdrivex.svg', '#2563eb'),
    ('bVaultX', 'bvaultx.com', False, '', 'bvaultx.svg', '#475569'),
    ('bSharesX', 'bsharesx.com', False, '', 'bsharesx.svg', '#15803d'),
    ('bDojoX', 'bdojox.com', False, '', 'bdojox.svg', '#e0262f'),
    ('bMoneyX', 'bmoneyx.com', False, '', 'bmoneyx.svg', '#059669'),
    ('bSearchX', 'bsearchx.com', False, '', 'bsearchx.svg', '#0891b2'),
    ('bSocialX', 'bsocialx.com', False, '', 'bsocialx.svg', '#c026d3'),
]

PAGE = {
    'slug': 'services',
    'title': 'Our b*X services',
    'desc': 'Every b*X.com site from bWalletX in one place: bChatX, bMailX, bCalX, bRadioX, bNewsX, bMusicX, bWriterX and more. What is live today, and what is coming.',
    'og_sub': 'Every b*X.com site, one wallet.',
}

CSS = '''    <style>
      .svc .ic {{ width: 48px; height: 48px; border-radius: 12px; display: grid; place-items: center; margin-bottom: 12px; }}
      .svc .ic img {{ width: 48px; height: 48px; border-radius: 12px; display: block; }}
      .svc .ic .bmark {{ width: 30px; height: 27px; border-radius: 0; }}
      .svc h3 {{ display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }}
      .svc .dom {{ color: #8a8a86; font-size: 0.85rem; margin-top: 8px; overflow-wrap: anywhere; }}
    </style>
  </head>'''




def own_icon(src):
    # Sites using the shared gold-b favicon have no file here; they get the gold b on the service's own colour.
    return src and os.path.exists(os.path.join(ROOT, 'img/services', src))


def icon(name, src, colour):
    if own_icon(src):
        return '<span class="ic" style="background:{}"><img src="/img/services/{}" alt="{} icon" width="48" height="48" /></span>'.format(colour, src, name)
    return '<span class="ic" style="background:{}"><img class="bmark" src="/logo.svg" alt="" width="30" height="27" /></span>'.format(colour)


def page_html():
    head = onb.HEAD.format(ver=OG_VER, **PAGE).replace('  </head>', CSS, 1)
    out = [head]
    out.append('      <p class="meta">Services</p>\n      <h1>Our <span class="gold">b</span>*X services</h1>\n')
    out.append('      <p class="lede">Each of these sites runs on bWalletX. Sign in once with your wallet and they work together. '
               'Some are live today; the rest are domains we own, marked Coming until they work.</p>\n')
    out.append('      <div class="grid">\n')
    for name, dom, live, desc, src, col in SERVICES:
        tag = '<span class="tag live">&check; Live</span>' if live else '<span class="tag">&#9675; Coming</span>'
        out.append('        <a class="box svc" href="https://{d}">{ic}<h3>{n} {t}</h3><p>{desc}</p><p class="dom">{d}</p></a>\n'.format(
            d=dom, ic=icon(name, src, col), n=name, t=tag, desc=desc if live else 'Coming.'))
    out.append('      </div>\n')
    out.append('\n      <h2>Status</h2>\n      <p class="small">Which sites work today, and which don&rsquo;t yet. Items move to Live when you can use them.</p>\n      <ul class="feat">\n')
    for name, dom, live, desc, src, col in sorted(SERVICES, key=lambda s: not s[2]):
        tag = '<span class="tag live">&check; Live</span>' if live else '<span class="tag">&#9675; Coming</span>'
        out.append('        <li>{}<span><a href="https://{}">{}</a></span></li>\n'.format(tag, dom, name))
    out.append('      </ul>\n\n')
    out.append('      <div class="row"><a class="btn btn-store" href="/get?from=services">Get bWalletX</a></div>\n')
    out.append('      <p class="small">Your keys stay with you: bWalletX is self-custody. Using other Bitcoin SV apps? See <a href="/on-b">Your apps, on b</a>.</p>\n')
    out.append(onb.TAIL)
    return ''.join(out)


OG = """<!doctype html><html><head><meta charset="utf-8"><style>{css}
.t{{width:104px;height:104px;border-radius:26px;box-shadow:0 18px 40px #0007;display:flex;align-items:center;justify-content:center}}
.t{{flex-direction:column;gap:6px}} .t img{{width:104px;height:104px;border-radius:26px}} .t img.bm{{width:50px;height:45px;border-radius:0}}
.t span{{font-weight:800;font-size:17px;color:#fff;text-shadow:0 1px 4px #0006}}
.big{{left:480px;top:120px;width:240px;height:240px}}
h1{{left:0;width:1200px;text-align:center;top:452px;margin:0;font-size:76px;font-weight:900;text-shadow:0 6px 30px #0007}}
h1 b{{color:#000;background:#F5B800;border-radius:18px;padding:0 16px}}
.u{{left:0;width:1200px;text-align:center;bottom:26px;font-size:24px}}
</style></head><body>{tiles}
<div class="z btile big"><img src="file://{b}" style="width:170px"></div>
<h1 class="z">Our <b>b</b>*X services</h1><div class="z u">bwalletx.com/services</div></body></html>"""


def render_og():
    # 18 tiles: a 3x3 block each side of the big b
    spots = [(40, 40), (164, 40), (288, 40), (40, 164), (164, 164), (288, 164), (40, 288), (164, 288), (288, 288),
             (808, 40), (932, 40), (1056, 40), (932, 164), (1056, 164), (808, 164), (1056, 288), (932, 288), (808, 288)]
    tiles = []
    for (x, y), s in zip(spots, SERVICES):
        name, _, _, _, src, col = s
        img = ('<img src="file://{}">'.format(os.path.join(ROOT, 'img/services', src)) if own_icon(src)
               else '<img class="bm" src="file://{}"><span>{}</span>'.format(os.path.join(ROOT, 'logo.svg'), name[1:-1]))
        tiles.append('<div class="z t" style="left:{}px;top:{}px;background:{}">{}</div>'.format(x, y, col, img))
    css = onb.OG_CSS.replace('BRAND', '#db2777')
    page = OG.format(css=css, tiles=''.join(tiles), b=os.path.join(ROOT, 'logo.svg'))
    tmp = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False)
    tmp.write(page)
    tmp.close()
    out = os.path.join(ROOT, 'og-services-{}.png'.format(OG_VER))
    subprocess.run([onb.CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=1', '--window-size=1200,630', '--screenshot=' + out, 'file://' + tmp.name],
                   check=True, capture_output=True)
    os.unlink(tmp.name)
    print('wrote', out)


def main():
    with open(os.path.join(ROOT, 'services.html'), 'w') as f:
        f.write(page_html())
    if '--no-og' not in sys.argv:
        render_og()


if __name__ == '__main__':
    main()
