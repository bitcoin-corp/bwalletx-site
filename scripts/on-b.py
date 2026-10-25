#!/usr/bin/env python3
"""Build the "<app> on b" pages (/twetch-on-b, /relayx-on-b, ...), the /on-b index and their share images.

    python3 scripts/on-b.py          # writes <slug>.html, on-b.html and og-<slug>-<OG_VER>.png (headless Chrome)
    python3 scripts/on-b.py --no-og  # pages only

Every "live" line must name the bWalletX source file that proves it (the `src` field, kept in an HTML
comment so reviewers can check it). Other apps' logos are shown only to identify them (nominative use),
at a modest size, exactly as each app publishes them: never redrawn, recoloured or distorted. No wording
that suggests a partnership. Each logo's source URL is in LOGOS below.
"""
import html
import os
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CHROME = os.environ.get('CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
OG_VER = 'v2'

# Official logos, saved unmodified under /img/apps/. Source of each file:
LOGOS = {
    # https://twetch.com/favicon.svg (twetch.com <link rel="icon" type="image/svg+xml">)
    'Twetch': ('/img/apps/twetch.svg', '#4a4c66'),
    # https://relayx.com/logo192.png (apple-touch-icon), via https://web.archive.org/web/2024id_/https://relayx.com/logo192.png
    'RelayX': ('/img/apps/relayx.png', '#2a6bf2'),
    # https://coingeek.com/wp-content/uploads/2024/09/cropped-android-chrome-512x512-1.png (site icon, 512px)
    'CoinGeek': ('/img/apps/coingeek.png', '#e0263a'),
    # https://peck.to/apple-touch-icon.png (peck.to apple-touch-icon)
    'Peck': ('/img/apps/peck.png', '#e8e3d6'),
    # https://treechat.com/assets/favicon.svg (treechat.com <link rel="icon">)
    'Treechat': ('/img/apps/treechat.svg', '#8d7fe3'),
    # https://yours.org/favicon.ico (144x144, converted ico -> png without other changes)
    'Yours Wallet': ('/img/apps/yours.png', '#3ecf6e'),
    # Hodlocker: hodlocker.com is down; the archived site (web.archive.org, 2024) has only a 48px generic
    # padlock favicon and no logo, so its name is shown in plain text. Colour taken from that favicon.
    'Hodlocker': (None, '#f5a623'),
}

PAGES = [
    {
        'slug': 'twetch-on-b',
        'app': 'Twetch',
        'title': 'Twetch on b',
        'desc': 'Read Twetch in the bWalletX Feed, tip authors in BSV, lock behind posts, restore a Twetch wallet from its 12 words and pay name@twetch.me.',
        'og_sub': 'Read Twetch, tip authors and lock behind posts, all from bWalletX.',
        'lede': 'Keep using Twetch, and use bWalletX next to it. The Twetch you know is in the bWalletX Feed, your old Twetch wallet can come with you, and b is on Twetch too.',
        'sections': [
            ('Read Twetch in the Feed', 'Open Feed and pick the Twetch chip. You see recent public Twetch posts, read from Twetch&rsquo;s own public API. Tap a name to see that person&rsquo;s posts and profile.'),
            ('Tip, like, lock and reply', 'Tip the author in BSV: it goes to the address of the key their Twetch posts are signed with. Lock BSV behind a post you rate; it stays yours and unlocks on the date shown. Likes and replies you make here are written on chain as bChat posts.'),
            ('Bookmarks and paid posts stay on Twetch', 'Twetch bookmarks and paid unlocks live on Twetch&rsquo;s servers, so those buttons open the post on Twetch. Twetch is also on the Apps tab&rsquo;s home screen.'),
            ('Bring your Twetch wallet', 'Add account &rsaquo; Restore &rsaquo; Twetch, then enter your Twetch 12 words. bWalletX uses the address path Twetch wallets used, so your coins show up. Your words stay on your device.'),
            ('Pay someone on Twetch', 'In Send, choose Other wallet &rsaquo; twetch.me to pay name@twetch.me. It is shown in full and marked outside bWalletX, and only offered while Twetch&rsquo;s paymail answers.'),
        ],
        'status': [
            (True, 'Twetch posts in the Feed, with author pages', 'src/mobile/feed/feedApi.ts (fetchTwetch), src/mobile/feed/authorFeed.ts'),
            (True, 'Tip a Twetch author in BSV', 'src/mobile/feed/feedApi.ts (twetchAddress), src/mobile/feed/FeedPage.tsx'),
            (True, 'Lock BSV behind a Twetch post', 'src/mobile/feed/sources.ts (twetch actions), src/mobile/feed/locks.ts'),
            (True, 'Like, reply and branch from bWalletX (written as bChat)', 'src/mobile/feed/sources.ts (FEED_APP)'),
            (True, 'Restore a Twetch wallet from its 12 words', 'src/pages/onboarding/RestoreAccount.tsx, src/services/Keys.service.ts, src/utils/constants.ts (DEFAULT_TWETCH_WALLET_PATH)'),
            (True, 'Pay a name@twetch.me paymail', 'src/mobile/names/paymailDomains.ts'),
            (True, 'Twetch on the Apps tab home screen', 'src/mobile/BrowserPage.tsx'),
            (True, 'b answers on Twetch as @bWalletX', 'bwalletx.com/b-on-twetch'),
            (False, 'Import who you follow on Twetch (Twetch&rsquo;s API for this is offline)', 'src/mobile/chat/contactSources.ts'),
            (False, 'Locks made on Twetch counted in the Most locked board', 'src/mobile/feed/FeedPage.tsx'),
            (False, 'Your bWalletX likes and replies showing inside the Twetch app', ''),
        ],
        'extra': '<p>Want to ask b something on Twetch? Read <a href="/b-on-twetch">b is on Twetch</a>.</p>',
    },
    {
        'slug': 'relayx-on-b',
        'app': 'RelayX',
        'title': 'RelayX on b',
        'desc': 'RelayX has closed, but your RelayX NFTs and BSV are still on chain. bWalletX finds them from your 12 words, keeps them in your wallet and cancels old listings.',
        'og_sub': 'Your RelayX NFTs and BSV are still on chain. bWalletX finds them.',
        'lede': 'RelayX has closed, but what you held there is still on chain, under the keys in your RelayX 12 words. bWalletX reads the chain for those keys and gives it back to you.',
        'sections': [
            ('Find your NFTs', 'Wallet &rsaquo; Bring in old assets &rsaquo; Recover RelayX collections. Enter your 12 words and tap Find my NFTs. Your NFTs appear as a gallery, grouped by collection. Finding is read-only: nothing moves.'),
            ('Keep them in bWalletX', 'Add account &rsaquo; Restore &rsaquo; RelayX. A Your RelayX collection card appears at the top of that account; one tap finds your NFTs again, and they sit in the NFTs tab under Run.'),
            ('Move leftover BSV', 'If your old RelayX addresses still hold BSV, one tap moves it into your account. RelayX NFTs are recognised first and never spent as coins.'),
            ('Cancel old listings', 'NFTs still listed for sale on RelayX when it closed are found too. The cancel is built and signed on your phone and shown before you allow it; one tap brings the NFT back to your own address.'),
        ],
        'status': [
            (True, 'Find RelayX NFTs from your 12 words, read-only', 'src/mobile/sweep/RelayxRecoverScreen.tsx, src/sweep/relayxRecover.ts'),
            (True, 'Restore a RelayX wallet and keep its NFTs in the NFTs tab (Run)', 'src/pages/onboarding/RestoreAccount.tsx, src/mobile/sweep/relayxSaved.ts'),
            (True, 'Move BSV left on old RelayX addresses in one tap', 'src/mobile/sweep/RelayxRecoverScreen.tsx (Move it into this account), src/mobile/sweep/HdSweepScreen.tsx'),
            (True, 'Cancel a listing still open on RelayX, back to your address', 'src/mobile/sweep/RelayxListedCancel.tsx, src/sweep/relayxListing.ts'),
            (True, 'Optional for Ninja Punk Girls holders: melt into element cards', 'src/mobile/sweep/NpgMelt.tsx, src/sweep/npgMelt.ts'),
            (False, 'Other Run collections shown with their pictures, not only names', ''),
            (False, 'Trading Run NFTs as Run NFTs in bWalletX', ''),
        ],
        'extra': '<p>The full walk-through, with screenshots: <a href="/recover-relayx">Recover RelayX collections</a>.</p>',
    },
    {
        'slug': 'coingeek-on-b',
        'app': 'CoinGeek',
        'title': 'CoinGeek on b',
        'desc': 'Read CoinGeek headlines in bNews inside bWalletX, open each story on CoinGeek, and talk about it in an on-chain thread where you can tip, like and lock.',
        'og_sub': 'CoinGeek headlines in bNews, with on-chain talk under each story.',
        'lede': 'CoinGeek writes about Bitcoin SV news. In bWalletX, its headlines sit in bNews next to other tech news, and every story gets its own thread where readers talk on chain.',
        'sections': [
            ('Headlines in bNews', 'Open Feed and switch to bNews. CoinGeek is one of its sources. We show the headline, picture, time and link only, never the article itself: tap through to read it on coingeek.com.'),
            ('A thread for every story', 'Each story opens as a thread. Posts there are ordinary on-chain bChat posts that link the story, so the discussion is on chain and nobody&rsquo;s server owns it.'),
            ('Tip the people in the thread', 'Tip, like or lock behind the posts other readers write about a story, the same as anywhere in the Feed.'),
        ],
        'status': [
            (True, 'CoinGeek headlines in bNews (headline, image, link only)', 'src/mobile/feed/bnews.ts (NEWS_SOURCES)'),
            (True, 'Each story opens as an on-chain thread', 'src/mobile/feed/NewsThread.tsx, src/mobile/feed/bnews.ts'),
            (True, 'Tip, like and lock behind posts in a story&rsquo;s thread', 'src/mobile/feed/FeedPage.tsx, src/mobile/feed/locks.ts'),
            (False, 'Paying CoinGeek, or a CoinGeek writer, per article', ''),
            (False, 'Pay-to-read articles in bNews', ''),
            (False, 'CoinGeek Conversations in bRadio (its feed lists no episodes)', 'src/mobile/bradio/podcastFeeds.ts'),
        ],
        'extra': '',
    },
    {
        'slug': 'peck-on-b',
        'app': 'Peck',
        'title': 'Peck on b',
        'desc': 'Read Peck posts in the bWalletX Feed from its public overlay, see each author&rsquo;s posts, tip signed authors in BSV and lock behind posts.',
        'og_sub': 'Read Peck in the bWalletX Feed. Tip signed authors in BSV.',
        'lede': 'Peck posts are plain Bitcoin Schema on chain, so bWalletX can read them. Use Peck as you do, and follow it from the same place you keep your coins.',
        'sections': [
            ('Read Peck in the Feed', 'Open Feed and pick the Peck chip. Posts come from Peck&rsquo;s public overlay, current to the latest block. Tap a name to see that author&rsquo;s posts; tap Open to see a post on peck.to.'),
            ('Tip signed authors', 'When a post&rsquo;s signature checks out, the tip goes to the address that signed it. If it can&rsquo;t be tied to the author, the tip button says so instead of guessing.'),
            ('Like, reply and lock', 'Lock BSV behind a post you rate; it stays yours. Likes and replies you make here are written on chain as bChat posts.'),
        ],
        'status': [
            (True, 'Peck posts in the Feed, from its public overlay', 'src/mobile/feed/feedApi.ts (fetchPeck), src/mobile/feed/peck.ts'),
            (True, 'A Peck author&rsquo;s posts on one page', 'src/mobile/feed/authorFeed.ts'),
            (True, 'Tip authors whose signature checks out', 'src/mobile/feed/peck.ts (aip_verified)'),
            (True, 'Lock, like and reply from bWalletX (written as bChat)', 'src/mobile/feed/sources.ts, src/mobile/feed/locks.ts'),
            (False, 'Your bWalletX posts showing in the Peck app', ''),
            (False, 'Import who you follow on Peck', ''),
        ],
        'extra': '',
    },
    {
        'slug': 'hodlocker-on-b',
        'app': 'Hodlocker',
        'title': 'Hodlocker on b',
        'desc': 'Lock BSV behind posts in bWalletX the way Hodlocker did: same lock format, your coins stay yours, they unlock on the date shown, and a Most locked board.',
        'og_sub': 'Lock behind posts, Hodlocker-style. Your BSV stays yours.',
        'lede': 'Hodlocker made locking popular: you back a post by time-locking your own BSV against it. The site has gone, but the idea lives on in bWalletX, written in the same on-chain format.',
        'sections': [
            ('Lock behind any post', 'In the Feed, tap Lock on a post. Pick an amount and a time: a day, a week, a month, or your own (up to about ten years). One approval and it&rsquo;s done.'),
            ('Your BSV stays yours', 'The coins never leave your wallet. They sit in a lock only your key can open, show on the Wallet&rsquo;s Locks row, and unlock on the date shown.'),
            ('Same format Hodlocker used', 'Each lock is the same lockup contract plus a like for the post, the shape Hodlocker wrote and read. Locks on a post are counted from the chain.'),
            ('Most locked', 'A board of the most locked people and posts over a day, a week, a month or all time. It counts the posts bWalletX has loaded, and says so.'),
        ],
        'status': [
            (True, 'Lock BSV behind a post, 1 day to about 10 years', 'src/mobile/feed/locks.ts (LOCK_DURATIONS)'),
            (True, 'Same lockup contract and like format as Hodlocker', 'src/mobile/feed/locks.ts, src/mobile/feed/locks.test.ts'),
            (True, 'Locks show on the Wallet&rsquo;s Locks row and unlock on the date', 'src/mobile/feed/feedApi.ts (lockToPost), src/mobile/locks/lockApi.ts'),
            (True, 'Lock totals for a post, read from the chain', 'src/mobile/feed/feedApi.ts (fetchPostLocks)'),
            (True, 'Most locked board: people and posts, 1D / 7D / 1M / All', 'src/mobile/feed/leaderboard.ts'),
            (False, 'Lock totals across the whole network (no live lock indexer since Hodlocker closed)', 'src/mobile/feed/leaderboard.ts'),
            (False, 'Locks made on Twetch counted on the board', 'src/mobile/feed/FeedPage.tsx'),
            (False, 'Checked: finding locks you made on Hodlocker with another wallet', ''),
        ],
        'extra': '',
    },
    {
        'slug': 'treechat-on-b',
        'app': 'Treechat',
        'title': 'Treechat on b',
        'desc': 'Read Treechat posts and whole threads in the bWalletX Feed, open them on Treechat, lock behind posts, and keep Treechat on your Apps home screen.',
        'og_sub': 'Read Treechat posts and whole threads in the bWalletX Feed.',
        'lede': 'Treechat posts are on chain, so bWalletX can show them next to everything else you follow. Keep Treechat for Treechat, and see it from your wallet too.',
        'sections': [
            ('Read Treechat in the Feed', 'Open Feed and pick the Treechat chip. Tap a post to read its whole thread, oldest first, or Open to see it on Treechat. Treechat authors get a gold bAvatar, since Treechat doesn&rsquo;t put pictures on chain.'),
            ('Lock, like and reply', 'Lock BSV behind a post you rate; it stays yours. Likes and replies you make here are written on chain as bChat posts.'),
            ('One tap to Treechat', 'Treechat is on the Apps tab&rsquo;s home screen, next to our own apps.'),
        ],
        'status': [
            (True, 'Treechat posts in the Feed', 'src/mobile/feed/feedApi.ts (fetchTreechat)'),
            (True, 'Whole Treechat threads, and Open on Treechat', 'src/mobile/feed/FeedPage.tsx, src/mobile/feed/sources.ts (postUrl)'),
            (True, 'Lock, like and reply from bWalletX (written as bChat)', 'src/mobile/feed/sources.ts, src/mobile/feed/locks.ts'),
            (True, 'Treechat on the Apps tab home screen', 'src/mobile/BrowserPage.tsx'),
            (False, 'Tips to Treechat authors (Treechat posts are signed by one shared key, so there is no author address to pay)', 'src/mobile/feed/FeedPage.tsx'),
            (False, 'Import who you follow on Treechat (no public API)', 'src/mobile/chat/contactSources.ts'),
        ],
        'extra': '',
    },
    {
        'slug': 'yours-on-b',
        'app': 'Yours Wallet',
        'title': 'Yours on b',
        'desc': 'Move a Yours Wallet into bWalletX with your 12 words or a Yours backup file. The Yours extension is not needed.',
        'og_sub': 'Bring your Yours Wallet in with your 12 words. No extension needed.',
        'lede': 'bWalletX grew from the open-source Yours Wallet code, so a Yours wallet fits straight in: same keys, same addresses, coins, tokens and ordinals.',
        'sections': [
            ('Restore with your 12 words', 'Add account &rsaquo; Restore &rsaquo; Yours, then enter your 12 words. They are all you need; the Yours extension is not required.'),
            ('Or use a Yours backup file', 'If you saved a Yours backup (a .json file), upload it instead. Its address paths come with it, so a custom setup restores as it was.'),
        ],
        'status': [
            (True, 'Restore a Yours wallet from its 12 words', 'src/pages/onboarding/RestoreAccount.tsx'),
            (True, 'Restore from a Yours JSON backup, with its address paths', 'src/pages/onboarding/RestoreAccount.tsx (handleYoursJsonUpload)'),
            (False, 'Bringing over the sites you had connected in Yours', ''),
        ],
        'extra': '',
    },
]

FOOT_NOTE = '{app} is a separate service; bWalletX is not affiliated with it. Logos belong to their owners.'


def logo_tag(app, cls=''):
    src = LOGOS[app][0]
    if not src:
        return '<span class="nm">{}</span>'.format(html.escape(app))
    return '<img src="{}" alt="{} logo" width="56" height="56" />'.format(src, html.escape(app))


def pair_html(app):
    return ('<div class="pair">{}<span class="plus">+</span>'
            '<img class="bmark" src="/logo.svg" alt="bWalletX b" width="56" height="50" /></div>').format(logo_tag(app))

HEAD = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} · bWalletX</title>
    <link rel="canonical" href="https://bwalletx.com/{slug}" />
    <meta name="description" content="{desc}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://bwalletx.com/{slug}" />
    <meta property="og:site_name" content="bWalletX" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:image" content="https://bwalletx.com/og-{slug}-{ver}.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="{title}: {og_sub}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bWalletX" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="https://bwalletx.com/og-{slug}-{ver}.png" />
    <link rel="icon" href="/favicon.ico" />
    <link rel="stylesheet" href="/styles.css" />
    <style>
      .ext .meta {{ color: #8a8a86; font-size: 0.9rem; margin: 0; }}
      .ext h1 {{ font-size: clamp(2.2rem, 6vw, 3.4rem); margin: 18px 0 10px; overflow-wrap: anywhere; }}
      .ext h1 .gold {{ color: #F5B800; }}
      .ext h2 {{ margin: 48px 0 10px; font-size: 1.5rem; }}
      .ext p, .ext li {{ line-height: 1.65; }}
      .box {{ background: #101114; border: 1px solid #ffffff12; border-radius: 16px; padding: 18px 20px; margin: 16px 0; }}
      .box h3 {{ margin: 0 0 6px; font-size: 1rem; }}
      .box p {{ margin: 0; color: #a7adb8; }}
      .ext .small {{ color: #8a8a86; font-size: 0.85rem; }}
      .ext .row {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 26px 0; }}
      .feat {{ list-style: none; padding: 0; margin: 18px 0; }}
      .feat li {{ display: flex; gap: 12px; align-items: baseline; padding: 12px 0; border-bottom: 1px solid #ffffff10; }}
      .feat li span:last-child {{ min-width: 0; overflow-wrap: anywhere; }}
      .tag {{ flex: none; font-size: 0.75rem; font-weight: 700; padding: 2px 9px; border-radius: 999px; white-space: nowrap; }}
      .tag.live {{ background: #F5B800; color: #000; }}
      .tag:not(.live) {{ background: #ffffff14; color: #cfcabd; }}
      .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 14px; margin: 22px 0; }}
      .grid a.box {{ display: block; margin: 0; text-decoration: none; color: inherit; }}
      .grid a.box:hover {{ border-color: #F5B80066; }}
      .grid a.box h3 .gold {{ color: #F5B800; }}
      .pair {{ display: flex; align-items: center; gap: 14px; margin: 22px 0 0; flex-wrap: wrap; }}
      .pair img, .tile .logo img {{ width: 56px; height: 56px; object-fit: contain; border-radius: 12px; display: block; }}
      .pair .plus {{ color: #8a8a86; font-size: 1.6rem; font-weight: 700; }}
      .pair .bmark {{ width: 56px; height: 50px; }}
      .pair .nm, .tile .nm {{ font-weight: 800; font-size: 1.15rem; padding: 14px 16px; border: 1px solid #ffffff22; border-radius: 12px; }}
      .tile .logo {{ display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }}
      .tile .logo .plus {{ color: #8a8a86; font-weight: 700; }}
      .tile .logo .bmark {{ width: 34px; height: 30px; }}
    </style>
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
    <main class="ext">
'''

TAIL = '''    </main>
  </body>
</html>
'''


def gold_b(title):
    # "Twetch on b" -> "Twetch on <span class=gold>b</span>"
    assert title.endswith(' on b')
    return html.escape(title[:-1], quote=False) + '<span class="gold">b</span>'


def page_html(p):
    out = [HEAD.format(ver=OG_VER, **p)]
    out.append('      <p class="meta"><a href="/on-b">On b</a> · Using {} with bWalletX</p>\n'.format(p['app']))
    out.append('      ' + pair_html(p['app']) + '\n')
    out.append('      <h1>{}</h1>\n'.format(gold_b(p['title'])))
    out.append('      <p class="lede">{}</p>\n\n'.format(p['lede']))
    out.append('      <h2>What you can do</h2>\n')
    for h, t in p['sections']:
        out.append('      <div class="box"><h3>{}</h3><p>{}</p></div>\n'.format(h, t))
    if p['extra']:
        out.append('      ' + p['extra'] + '\n')
    out.append('\n      <h2>Status</h2>\n      <p class="small">What works in bWalletX today, and what doesn&rsquo;t yet.</p>\n      <ul class="feat">\n')
    for live, text, src in p['status']:
        cmt = ' <!-- {} -->'.format(src) if src else ''
        tag = '<span class="tag live">&check; Live</span>' if live else '<span class="tag">&#9675; Not yet</span>'
        out.append('        <li>{}<span>{}</span>{}</li>\n'.format(tag, text, cmt))
    out.append('      </ul>\n\n')
    out.append('      <div class="row"><a class="btn btn-store" href="/get?from={}">Get bWalletX</a></div>\n'.format(p['slug']))
    out.append('      <p class="small">Your keys stay with you: bWalletX is self-custody. ' + FOOT_NOTE.format(app=p['app']) + ' <a href="/on-b">More apps on b</a>.</p>\n')
    out.append(TAIL)
    return ''.join(out)


INDEX = {
    'slug': 'on-b',
    'title': 'Your apps, on b',
    'desc': 'Use the Bitcoin SV apps you already know with bWalletX: Twetch, RelayX, CoinGeek, Peck, Hodlocker, Treechat and Yours. What works today, app by app.',
    'og_sub': 'Twetch, RelayX, CoinGeek, Peck, Hodlocker, Treechat, Yours.',
}


def index_html():
    out = [HEAD.format(ver=OG_VER, **INDEX)]
    out.append('      <p class="meta">On b</p>\n      <h1>Your apps, on <span class="gold">b</span></h1>\n')
    out.append('      <p class="lede">You already use Bitcoin SV apps. Here is what each one looks like from bWalletX: what you can bring over, what you can use side by side, and what doesn&rsquo;t work yet.</p>\n')
    out.append('      <div class="grid">\n')
    for p in PAGES:
        n = sum(1 for s in p['status'] if s[0])
        out.append('        <a class="box tile" href="/{}"><div class="logo">{}<span class="plus">+</span>'
                   '<img class="bmark" src="/logo.svg" alt="" width="34" height="30" /></div>'
                   '<h3>{}</h3><p>{}</p><p class="small">{} live</p></a>\n'.format(
            p['slug'], logo_tag(p['app']), gold_b(p['title']), p['og_sub'], n))
    out.append('      </div>\n')
    out.append('      <div class="row"><a class="btn btn-store" href="/get?from=on-b">Get bWalletX</a></div>\n')
    out.append('      <p class="small">Each app named here is a separate service; bWalletX is not affiliated with any of them. Logos belong to their owners. Our own sites: <a href="/services">b*X services</a>.</p>\n')
    out.append(TAIL)
    return ''.join(out)


OG_CSS = """html,body{margin:0;width:1200px;height:630px;overflow:hidden}
body{color:#fff;font-family:-apple-system,"Helvetica Neue",Arial,sans-serif;position:relative;
background:radial-gradient(700px 520px at 8% 10%,BRAND 0,transparent 70%),
radial-gradient(760px 560px at 96% 96%,#ff7a1a 0,transparent 68%),
radial-gradient(700px 600px at 70% 0%,#F5B800 0,transparent 70%),
linear-gradient(135deg,BRAND 0,#c2410c 55%,#F5B800 100%)}
body:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,#0000 0,#0006 100%)}
.z{position:absolute;z-index:1}
.k{left:80px;top:60px;font-weight:800;letter-spacing:.14em;font-size:24px;color:#fff;opacity:.9}
.u{left:80px;bottom:56px;font-size:28px;color:#fff;opacity:.85;font-weight:600}
.tile{background:#fff;border-radius:44px;box-shadow:0 24px 60px #0007;display:flex;align-items:center;justify-content:center}
.tile img{width:100%;height:100%;object-fit:contain;border-radius:44px}
.btile{background:#000;border-radius:44px;box-shadow:0 24px 60px #0007,0 0 0 4px #F5B800;display:flex;align-items:center;justify-content:center}
.nm{font-weight:900;color:#111;text-align:center;line-height:1}
"""

OG_APP = """<!doctype html><html><head><meta charset="utf-8"><style>{css}
.pair{{left:80px;top:122px;display:flex;align-items:center;gap:34px}}
.pair .tile,.pair .btile{{width:220px;height:220px}}
.plus{{font-size:110px;font-weight:900;color:#fff;text-shadow:0 6px 24px #0006}}
h1{{left:76px;top:378px;margin:0;font-size:{size}px;font-weight:900;letter-spacing:-.02em;line-height:1;text-shadow:0 6px 30px #0007}}
h1 b{{color:#000;background:#F5B800;border-radius:22px;padding:0 22px}}
</style></head><body><div class="z k">BWALLETX · ON b</div>
<div class="z pair"><div class="tile">{logo}</div><div class="plus">+</div><div class="btile"><img src="file://{b}" style="width:150px"></div></div>
<h1 class="z">{h1}</h1><div class="z u">bwalletx.com/{slug}</div></body></html>"""

OG_INDEX = """<!doctype html><html><head><meta charset="utf-8"><style>{css}
.t{{width:150px;height:150px;border-radius:34px}} .t img{{border-radius:34px}}
.big{{left:480px;top:150px;width:240px;height:240px}}
h1{{left:0;width:1200px;text-align:center;top:450px;margin:0;font-size:76px;font-weight:900;text-shadow:0 6px 30px #0007}}
h1 b{{color:#000;background:#F5B800;border-radius:18px;padding:0 16px}}
.u{{left:0;width:1200px;text-align:center;bottom:26px;font-size:24px}}
.nm{{font-size:28px}}
</style></head><body>{tiles}
<div class="z btile big"><img src="file://{b}" style="width:170px"></div>
<h1 class="z">Your apps, on <b>b</b></h1><div class="z u">bwalletx.com/on-b</div></body></html>"""


def og_logo(app, fs=40):
    src = LOGOS[app][0]
    if not src:
        return '<div class="nm" style="font-size:{}px">{}</div>'.format(fs, html.escape(app))
    return '<img src="file://{}">'.format(os.path.join(ROOT, src.lstrip('/')))


def shoot(page, slug):
    tmp = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False)
    tmp.write(page)
    tmp.close()
    out = os.path.join(ROOT, 'og-{}-{}.png'.format(slug, OG_VER))
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=1', '--window-size=1200,630', '--screenshot=' + out, 'file://' + tmp.name],
                   check=True, capture_output=True)
    os.unlink(tmp.name)
    print('wrote', out)


def render_og(p):
    app, title = p['app'], p['title']
    name = title[:-len(' on b')]
    size = 130 if len(title) <= 12 else 112
    css = OG_CSS.replace('BRAND', LOGOS[app][1])
    shoot(OG_APP.format(css=css, logo=og_logo(app), b=os.path.join(ROOT, 'logo.svg'), slug=p['slug'], size=size,
                        h1=html.escape(name) + ' on <b>b</b>'), p['slug'])


def render_og_index():
    # logos ring around the big gold b: 4 across the top, 3 lower on the sides
    spots = [(120, 120), (330, 60), (720, 60), (930, 120), (80, 330), (970, 330), (300, 300)]
    tiles = []
    for (x, y), p in zip(spots, PAGES):
        tiles.append('<div class="z tile t" style="left:{}px;top:{}px">{}</div>'.format(x, y, og_logo(p['app'], 28)))
    css = OG_CSS.replace('BRAND', '#7c3aed')
    shoot(OG_INDEX.format(css=css, tiles=''.join(tiles), b=os.path.join(ROOT, 'logo.svg')), 'on-b')


def main():
    for p in PAGES:
        with open(os.path.join(ROOT, p['slug'] + '.html'), 'w') as f:
            f.write(page_html(p))
    with open(os.path.join(ROOT, 'on-b.html'), 'w') as f:
        f.write(index_html())
    if '--no-og' not in sys.argv:
        for p in PAGES:
            render_og(p)
        render_og_index()


if __name__ == '__main__':
    main()
