"""Hodl my b, Edition 0: the whole story of bWalletX and the suite. Imported by hodl-my-b.py.
Every Live pill must be true today (checked 18 Oct 2026 against /releases 5.2.24-5.2.32, docs/ROADMAP.md,
bmailx.com status list, /desktop, /open-source, /privacy, /get). Anything else goes on the Coming page."""


def pages(h, back):
    page, bg, BLOB, RING, emo, card, getqr, barcode = h['page'], h['bg'], h['BLOB'], h['RING'], h['emo'], h['card'], h['getqr'], h['barcode']
    L, C = h['L'], h['C']

    def SHOT(src, alt, cls=''):
        return f'<figure class="shot {cls} r3"><img src="/media/hodl/e0/{src}" alt="{alt}" /></figure>'

    P = []
    P.append(page('<div class="hero e0h">' + BLOB('radial-gradient(circle at 30% 30%,#fff3b0,#f5b800 55%,#8a5d00)', 78, 74, 70)
        + RING('rgba(255,210,77,.45)', 78, 74, 92) + RING('rgba(255,210,77,.22)', 78, 74, 118) + '<div class="bigb">b</div></div>'
        + '<p class="mh e0mh r1">Hodl my <em>b</em></p><p class="dl r2"><span>Edition 0</span><span>The whole story</span><span>October 2026</span></p>'
        + '<p class="hl e0hl r3">One wallet. <span class="gd">Your whole Bitcoin life.</span></p>'
        + '<ul class="cl r4"><li><b>Every device</b>Phone, web, Chrome, Desktop</li><li><b>One name</b>Two addresses</li><li><b>bChatX</b>Rooms, Spaces, b</li><li><b>bMail</b>Mail that pays</li></ul>'
        + '<div class="bc r4"><div class="pr"><b>Edition 0</b><span>Free &middot; pass it on</span></div>' + barcode() + '</div>', 's-cover', hard=True))
    P.append(page('<p class="k r1">Inside</p><h2 class="r2">The whole story.</h2><ol class="toc r3">'
        '<li><span>One wallet, every device</span><b>3</b></li>'
        '<li><span>One name, two addresses</span><b>5</b></li><li><span>bChatX: rooms and Spaces</span><b>6</b></li>'
        '<li><span>Ask b, open all hours</span><b>7</b></li><li><span>bMail: mail that pays</span><b>8</b></li>'
        '<li><span>Exchange, coins, the Store</span><b>9</b></li><li><span>NFTs: old wallets welcome</span><b>10</b></li>'
        '<li><span>Agents with pocket money</span><b>11</b></li><li><span>Yours, really</span><b>12</b></li>'
        '<li><span>Privacy, plainly</span><b>13</b></li><li><span>Coming, and how to get it</span><b>14</b></li></ol>'
        f'<p class="q r4">Everything in here is {L} today, unless it says {C}.</p>', 's-cream', 2, issue=0,
        deco=bg('dots', BLOB('#ffd24d', 70, -10, 70), emo(['book', 'spark', 'beer'], 21))))
    P.append(page('<p class="k r1">The wallet</p><h2 class="r2">One wallet. <span class="gd">Every device.</span></h2>'
        f'<ul class="st r3"><li>{L}Web: web.bwalletx.com</li><li>{L}Android: direct download</li><li>{L}Chrome extension</li><li>{L}Desktop, in your browser</li><li>{L}iPhone: web app, or the TestFlight beta</li></ul>'
        '<p class="r3">Your keys are made and kept on your device. We can&rsquo;t move your money.</p>'
        + SHOT('web-top.jpg', 'The bWalletX web wallet start screen', 'wide'), 's-black', 3, issue=0,
        deco=bg('grid', RING('rgba(255,210,77,.35)', 70, 60, 80), emo(['phone', 'lock', 'spark'], 22))))
    P.append(page('<p class="k r1">The wallet &middot; Desktop</p><h2 class="r2">The big screen.</h2>'
        '<p class="r3">Money, bMail, chat rooms, Spaces, bApps and Ask b side by side. Free in your browser, or install it as an app. Press &#8984;K and tell b what to do.</p>'
        f'<p class="r3">{L} <a href="/desktop">desktop.bwalletx.com</a></p>'
        + SHOT('desktop.jpg', 'bWalletX Desktop opening screen', 'wide'), 's-paper', 4, issue=0,
        deco=bg('grid', BLOB('#ffd24d', 80, 85, 60), emo(['sun', 'spark'], 23))))
    P.append(page('<p class="k r1">Names</p><h2 class="r2">One name. Two addresses.</h2>'
        '<div class="names r3"><b>$you</b><span>you@bwalletx.com</span><span>you@bmailx.com</span></div>'
        f'<ul class="st r3"><li>{L}Claim a $name: it works at both addresses, same wallet</li><li>{L}Signed by your own wallet, so nobody (us included) can quietly re-point it</li><li>{L}Every change goes into a public log</li><li>{L}Hand a name on: it moves only when the other wallet accepts</li></ul>'
        '<p class="q r4">Pay $you. It lands with you. That&rsquo;s it.</p>', 's-yellow', 5, issue=0,
        deco=bg('stripes', BLOB('#fff', 70, 30, 70), emo(['label', 'link', 'ok'], 24))))
    P.append(page('<p class="k r1">bChatX</p><h2 class="r2">Rooms and Spaces, <span class="gd">owned by you.</span></h2>'
        f'<ul class="st r3"><li>{L}Rooms with their own token: hold it to get in</li><li>{L}DMs, voice and video calls, tips</li><li>{L}Spaces: live talks with a stage; pay at the door or by the minute</li><li>{L}Guests can listen without signing in</li></ul>'
        + SHOT('bchatx-top.jpg', 'bchatx.com sign-in screen', 'wide'), 's-black', 6, issue=0,
        deco=bg('grid', RING('rgba(255,210,77,.35)', 60, 55, 80), emo(['chat', 'head', 'note'], 25))))
    P.append(page('<p class="k r1">Ask b</p><h2 class="r2">Help that never closes.</h2>'
        '<p class="r3">b is the assistant inside the wallet. Ask in plain words in the app, at bchatx.com/ask-b, or hold to talk. b also sits in the Help Desk Space, open 24/7.</p>'
        f'<p class="r3">{L} Send b a bug report in one tap, then see what happened to it under Your reports.</p>'
        + SHOT('helpdesk.jpg', 'The bWallet Help Desk Space on bChatX, open 24/7'), 's-lime', 7, issue=0,
        deco=bg('dots', BLOB('#7ee0a1', 70, 70, 80), emo(['robot', 'chat', 'heart'], 26))))
    P.append(page('<p class="k r1">bMail &middot; bMailX</p><h2 class="r2">Mail that pays you.</h2>'
        f'<ul class="st r3"><li>{L}Sealed letters: only the person you write to can open them</li><li>{L}Each stamp is a real payment to the reader. Penny post: 1&cent;</li><li>{L}Set your price to reach you. Friends free, always on top</li><li>{L}Reply paid, so they can answer for free</li></ul>'
        + SHOT('bmailx-top.jpg', 'bmailx.com: Email that pays', 'wide') + '<p class="q r4">Spam pays you now.</p>', 's-pink', 8, issue=0,
        deco=bg('dots', BLOB('#ff6b9e', 65, 55, 90), emo(['env', 'mail', 'coin'], 27))))
    P.append(page('<p class="k r1">Exchange</p><h2 class="r2">Buy, sell, launch.</h2>'
        f'<ul class="st r3"><li>{L}Buy and sell tokens and NFTs wallet to wallet; we never hold them</li><li>{L}Launch your own coin, your share time-locked with a public receipt</li><li>{L}Airdrop to every holder with one approval</li><li>{L}The Store: themes for $1, yours to keep</li></ul>'
        '<div class="g r3">' + card('/exchange', 'og-exchange-v6.png', 'Exchange', 'Live') + card('/themes', 'og-themes-v2.png', 'Themes', 'Live') + '</div>', 's-orange', 9, issue=0,
        deco=bg('dots', BLOB('#ffd24d', 65, 60, 80), emo(['cart', 'rocket', 'gem'], 28))))
    P.append(page('<p class="k r1">NFTs</p><h2 class="r2">Old wallets welcome.</h2>'
        f'<ul class="st r3"><li>{L}One library: pictures, video, music, documents</li><li>{L}Restore a RelayX wallet and its NFTs appear</li><li>{L}NFTs still listed on RelayX are found; one tap cancels the listing</li><li>{L}Restore from Yours, Panda, Twetch, SimplyCash, Money Button and more</li></ul>'
        '<div class="g r3">' + card('/recover-relayx', 'og-recover-relayx-v2.png', 'Recover RelayX', 'Live') + card('/nfts', 'og-nfts-v1.png', 'NFTs', 'Live') + '</div>', 's-peach', 10, issue=0,
        deco=bg('dots', BLOB('#ffb347', 70, 70, 70), emo(['art', 'gift', 'star'], 29))))
    P.append(page('<p class="k r1">Agents</p><h2 class="r2">An AI with <span class="gd">pocket money.</span></h2>'
        f'<ul class="st r3"><li>{L}Agent accounts: own keys, own budget, a daily cap, and Stop</li><li>{L}The <code>bwalletx</code> CLI and MCP server for your own agents</li><li>{L}Any site or agent can ask bWalletX to pay or sign (BRC-100)</li></ul>'
        '<div class="flt"><div class="big stopb">STOP</div></div><p class="q r4">It can only spend what you gave it.</p>', 's-black', 11, issue=0,
        deco=bg('grid', RING('rgba(255,210,77,.35)', 60, 55, 80), emo(['robot', 'moneybag', 'stop'], 30))))
    P.append(page('<p class="k r1">Open source</p><h2 class="r2">Yours, really.</h2>'
        f'<ul class="st r3"><li>{L}The wallet is open source (MIT): read it, build it, fork it</li><li>{L}Your coins sit at your own addresses; your 12 words restore them</li><li>{L}Locks are enforced by the network: nobody can move them early, us included</li></ul>'
        '<p class="r3"><a href="/open-source">What&rsquo;s open, and under which licence</a></p>', 's-cream', 12, issue=0,
        deco=bg('grid', BLOB('#7ee0a1', 75, 70, 60), emo(['lock', 'book', 'ok'], 31))))
    P.append(page('<p class="k r1">Privacy</p><h2 class="r2">Plainly.</h2>'
        f'<ul class="st r3"><li>{L}Your keys and recovery phrase never leave your device</li><li>{L}No ads, no tracking, no selling your data</li><li>{L}No analytics or crash reports</li></ul>'
        f'<ul class="st r3"><li>{C}Space transcripts only when the host turns them on and each speaker agrees, with a visible badge; audio deleted after</li><li>{C}End-to-end encrypted DMs</li></ul>'
        '<p class="r3"><a href="/privacy">Privacy policy</a></p>', 's-gold', 13, issue=0,
        deco=bg('dots', RING('#111', 60, 40, 80), emo(['lock', 'shades'], 32))))
    P.append(page('<p class="k r1">Coming</p><h2 class="r2">Not live yet.</h2>'
        f'<ul class="st r3"><li>{C}bWallet on the App Store and Google Play (beta testing today)</li><li>{C}A real email inbox at name@bmailx.com</li><li>{C}Agreements in bMail: send, both sign, sealed</li><li>{C}bCredits top-up</li><li>{C}Share one fact, such as over 18</li><li>{C}Space transcription, with consent</li></ul>'
        '<p class="q r4">When it ships, it moves to Live. Not before.</p>', 's-black', 14, issue=0,
        deco=bg('grid', RING('rgba(255,210,77,.35)', 60, 55, 80), emo(['soon', 'cal'], 33))))
    P.append(page('<p class="k r1">Get it</p><h2 class="r2">Start in a minute.</h2>'
        '<ul class="st r3"><li><a href="https://web.bwalletx.com">Web &middot; web.bwalletx.com</a></li><li><a href="/android">Android &middot; download</a></li><li><a href="/extension">Chrome extension</a></li><li><a href="https://desktop.bwalletx.com">Desktop &middot; desktop.bwalletx.com</a></li><li><a href="/iphone">iPhone web app</a> &middot; <a href="https://testflight.apple.com/join/1TTnQNKm">TestFlight beta</a></li></ul>'
        + getqr() + '<p class="r4">Beta: test with small amounts. <a href="/hodl-my-b/hodl-my-b-edition-0.pdf" download>PDF of this edition</a></p>', 's-paper', 15, issue=0,
        deco=bg('grid', BLOB('#ffd24d', 72, -12, 60), emo(['gift', 'rocket'], 34))))
    P.append(page('<p class="k r1">Back cover</p><h2 class="r2">Just <span class="gd">b.</span></h2><p class="q r3">Less noise. More life.</p><p class="k r3">Every edition</p><div class="g r3">' + back
        + '</div><p class="foot2">By The Bitcoin Corporation Ltd &middot; Emoji: Twemoji, CC-BY 4.0 &middot; Screens from the live apps, 18 Oct 2026</p>', 's-back', hard=True,
        deco=bg('grid', BLOB('radial-gradient(circle,#f5b800,transparent 70%)', 40, 50, 100), emo(['beer', 'clink', 'cool'], 35))))
    return P
