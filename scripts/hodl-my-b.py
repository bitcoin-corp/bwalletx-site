#!/usr/bin/env python3
"""Builds the Hodl my b flipbook. Latest issue is /hodl-my-b (hodl-my-b.html); each issue also at /hodl-my-b/<n>.
Edit ISSUES / pages_issue_N below, then: python3 scripts/hodl-my-b.py && python3 scripts/seo-head.py && python3 scripts/gen-llms.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = '<i class="p l">Live</i>'; N = '<i class="p">Next release</i>'; C = '<i class="p">Coming</i>'
BEER = '<img class="beer" src="/images/twemoji-beer.svg" alt="" width="72" height="72" />'
ISSUES = [  # newest last
    dict(n=1, week='12 Oct 2026', story='Don&rsquo;t be bland. Get bRanded.', og='og-hodl-my-b-1-v2.png',
         blurb='Business agents, plus the week&rsquo;s round-up.'),
]

MEDIA = {  # slot name -> '/media/hodl/<file>.jpg' or '.mp4' (muted loop). Empty = built-in art. See docs/HODL-MY-B.md.
    "cover": "/media/hodl/",
    "brand": "/media/hodl/",
    "checkout": "/media/hodl/",
    "allowance": "/media/hodl/",
    "receipts": "/media/hodl/",
    "release": "/media/hodl/",
    "next": "/media/hodl/",
    "lifestyle": "/media/hodl/",
}
TW = 'https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.1.0/assets/svg/'
E = dict(beer='1f37a', spark='2728', heart='1f49b', bag='1f6cd', coffee='2615', ice='1f366', art='1f3a8', head='1f3a7', palm='1f334',
         cool='1f60e', chat='1f4ac', phone='1f4f1', receipt='1f9fe', ok='2705', stop='1f6d1', money='1f4b8', party='1f389', cocktail='1f379',
         rainbow='1f308', ball='1faa9', fire='1f525', donut='1f369', note='1f3b5', star='1f31f', berry='1f353', cake='1f9c1', balloon='1f388',
         rocket='1f680', card='1f4b3', cart='1f6d2', burger='1f354', moneybag='1f4b0', coin='1fa99', robot='1f916', cal='1f4c5', env='2709', signal='1f4f6', link='1f517', search='1f50d', store='1f3ea', label='1f3f7', gift='1f381', soon='1f51c', sunrise='1f305', clink='1f942', notes='1f3b6', book='1f4d6', lock='1f512', mail='1f4e9', shades='1f576', sun='1f31e', flower='1f33c', gem='1f48e', crown='1f451', wave='1f30a', pizza='1f355')

def emo(names, seed, area='edge', n=None):
    """Scatter Twemoji around the page edges (behind the text)."""
    out = []; import random; r = random.Random(seed); names = names * 3
    for k, nm in enumerate(names[:n or len(names)]):
        side = k % 4
        if area == 'edge':
            x, y = [(r.uniform(82, 96), r.uniform(2, 20)), (r.uniform(84, 97), r.uniform(30, 92)), (r.uniform(30, 80), r.uniform(88, 97)), (r.uniform(-3, 5), r.uniform(55, 95))][side]
        else:
            x, y = r.uniform(-2, 96), r.uniform(-2, 96)
        sz = r.uniform(5, 11) if area == 'edge' else r.uniform(6, 14); rot = r.uniform(-30, 30); d = r.uniform(0, 3)
        out.append(f'<img class="em" src="{TW}{E[nm]}.svg" alt="" style="left:{x:.1f}%;top:{y:.1f}%;width:{sz:.1f}cqmin;--r:{rot:.0f}deg;animation-delay:-{d:.1f}s" />')
    return ''.join(out)

def wave(c1, c2):
    return (f'<svg class="wv" viewBox="0 0 400 120" preserveAspectRatio="none"><path d="M0 60 C80 10 160 110 240 60 S360 20 400 50 V120 H0Z" fill="{c1}"/>'
            f'<path d="M0 85 C90 50 170 120 260 80 S370 60 400 80 V120 H0Z" fill="{c2}"/></svg>')

def bg(pattern='dots', shapes='', emojis='', img='', wv=None):
    im = f'<img class="bgimg" src="/{img}" alt="" />' if img else ''
    return f'<div class="bg pat-{pattern}" aria-hidden="true">{im}{shapes}{wave(*wv) if wv else ""}{emojis}</div>'

def media(slot, art=''):
    src = MEDIA.get(slot, '')
    if src.endswith('.mp4'):
        return f'<div class="media photo" data-media="{slot}"><video src="{src}" autoplay muted loop playsinline></video></div>'
    elif src.endswith('/'):  # folder: <slot>-4x5.jpg on phones, <slot>-16x9.jpg on wide screens
        return f'<div class="media photo" data-media="{slot}"><img src="{src}{slot}-4x5.jpg" alt="" /></div>'
    elif src:
        return f'<div class="media photo" data-media="{slot}"><img src="{src}" alt="" /></div>'
    else:
        inner = art
    return f'<div class="media" data-media="{slot}">{inner}</div>'

def card(href, img, t, s, ext=False):
    tg = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a class="cd" href="{href}"{tg}><img class="og" src="/{img}" alt="" width="1200" height="630" loading="lazy" /><b>{t}</b><span>{s}</span></a>'

def page(body, scene, n=None, issue=1, hard=False, deco=''):
    folio = f'<p class="folio">Hodl my b &middot; Issue {issue} &middot; {n}</p>' if n else ''
    dens = ' data-density="hard"' if hard else ''
    import re as _re
    m = _re.search(r'<div class="media photo".*?</div>', body)
    if m:  # the photo becomes the full-bleed background, washed in the scene colour under the text
        body = body.replace(m.group(0), '' if scene == 's-cover' else '<div class="spacer"></div>')
        deco = m.group(0) + '<div class="wash" aria-hidden="true"></div>' + deco
    return f'<div class="page {scene}"{dens}>{deco}<div class="pin">{body}{folio}</div><i class="sheen"></i></div>'

def og(img, alt=''):
    return f'<img class="og" src="/{img}" alt="{alt}" width="1200" height="630" />'

CHAT = lambda a, b, c: f'<div class="chat" aria-hidden="true"><div class="u">{a}</div><div class="a">{b}</div><div class="u">{c}</div><div class="rc">Receipt on chain</div></div>'
BLOB = lambda c, x, y, w: f'<span class="blob" style="background:{c};left:{x}%;top:{y}%;width:{w}cqmin"></span>'
RING = lambda c, x, y, w: f'<span class="ring" style="border-color:{c};left:{x}%;top:{y}%;width:{w}cqmin"></span>'

def barcode():
    import random; r = random.Random(7); x = 0; bars = []
    while x < 96:
        w = r.choice([1, 1, 2, 3]); bars.append(f'<rect x="{x}" y="0" width="{w}" height="40"/>'); x += w + r.choice([1, 2, 2, 3])
    return f'<svg viewBox="0 0 100 40" preserveAspectRatio="none">{"".join(bars)}</svg>'

def cover_art():
    return ('<div class="hero">' + BLOB('radial-gradient(circle at 30% 30%,#fff3b0,#f5b800 55%,#8a5d00)', 52, 30, 95)
            + RING('rgba(255,210,77,.5)', 8, 50, 70) + RING('rgba(255,210,77,.3)', 60, 8, 50)
            + '<div class="bigb">b</div>' + emo(['beer', 'spark', 'beer', 'spark', 'beer', 'spark'], 11, 'all')
            + '<div class="cchat">' + CHAT('Got the sticker pack?', 'Yes! 1,500 sats. Tap to pay.', 'Paid &#x2714;') + '</div></div>')

def pages_issue_1(back):
    P = []
    P.append(page(media('cover', cover_art())
        + '<p class="mh r1">Hodl my <em>b</em></p><p class="dl r2"><span>Weekly</span><span>Issue 1</span><span>Week of 12 Oct 2026</span></p>'
        + '<p class="hl r3">Don&rsquo;t be bland. <span class="gd">Get bRanded.</span></p>'
        + '<ul class="cl r4"><li><b>Theme Store</b>New looks, live</li><li><b>Credits card</b>Prepay, coming</li><li><b>bChatX rooms</b>A token per room</li><li><b>All 19 bApps</b>Sign in and pay</li></ul>'
        + '<div class="bc r4"><div class="pr"><b>Issue 1</b><span>Free &middot; weekly</span></div>' + barcode() + '</div>', 's-cover', hard=True))
    P.append(page('<p class="k r1">Inside</p><h2 class="r2">This week.</h2><ol class="toc r3">'
        '<li><span>Paste a link, get a shopkeeper</span><b>3</b></li><li><span>The till is the chat</span><b>4</b></li>'
        '<li><span>An agent with pocket money</span><b>5</b></li><li><span>Bitcoin by text</span><b>6</b></li>'
        '<li><span>Receipts anyone can check</span><b>7</b></li><li><span>New in 5.2.26</span><b>8</b></li>'
        '<li><span>Also this week</span><b>9</b></li><li><span>Where things stand</span><b>11</b></li></ol>'
        '<p class="q r4">Just b. Every feature says plainly: Live, Next release, or Coming.</p>', 's-cream', 2,
        deco=bg('dots', BLOB('#ffd24d', 70, -10, 70) + RING('#111', 75, 60, 40), emo(['book', 'spark', 'beer'], 2), wv=('rgba(255,179,71,.35)', 'rgba(255,210,77,.5)'))))
    P.append(page(f'<p class="k r1">Cover story &middot; bRand</p><h2 class="r2">Paste a link. <span class="gd">Get a shopkeeper.</span></h2><p class="r3">Give b your website. b drafts an agent that knows your menu, prices and hours, and answers customers in chat.</p><p class="r3">{N} Agent from a link. <a href="/business-agents">bRand business agents</a></p>' + media('brand', og('og-business-agents-brand.png', 'bRand business agents')) + '<p class="q r4">It never calls in sick. It does ask for a logo.</p>', 's-black', 3,
        deco=bg('grid', BLOB('radial-gradient(circle,#f5b800,transparent 70%)', 55, 45, 110), emo(['bag', 'store', 'label', 'spark'], 3), img='og-themes-custom.png')))
    P.append(page(f'<p class="k r1">Cover story &middot; checkout</p><h2 class="r2">The till is the chat.</h2><p class="r3">Customer asks, agent quotes, customer taps Pay. Both sides keep the same receipt.</p><p class="r3">{N} Chat checkout for business agents.</p>' + media('checkout', CHAT('Two flat whites?', '900 sats. Tap to pay.', 'Paid &#x2714;')) + '<p class="q r4">No card machine. No &ldquo;it&rsquo;s gone through twice&rdquo;.</p>', 's-yellow', 4,
        deco=bg('stripes', BLOB('#fff', 60, 30, 80) + RING('#111', -10, 70, 50), emo(['card', 'receipt', 'cart', 'burger', 'coffee', 'ok'], 4), wv=('rgba(255,122,61,.35)', 'rgba(255,255,255,.5)'))))
    P.append(page(f'<p class="k r1">Cover story &middot; pocket money</p><h2 class="r2">An agent with a daily allowance.</h2><p class="r3">Its own capped account: a daily limit, and a big Stop button for when it gets ideas above its station.</p><p class="r3">{N} Capped agent account inside the app.</p><p class="r3">{L} Today on your computer: the <code>bwalletx</code> CLI agent wallet, with a daily cap and Stop. <a href="/cli">CLI</a></p>' + media('allowance', '<div class="big stopb">STOP</div>'), 's-pink', 5,
        deco=bg('dots', BLOB('#ff6b9e', 65, 55, 90) + RING('#fff', 5, 5, 40), emo(['moneybag', 'coin', 'stop', 'robot', 'cal'], 5))))
    P.append(page(f'<p class="k r1">Cover story &middot; SMS</p><h2 class="r2">Bitcoin by text.</h2><p class="r3">Customers text a business&rsquo;s agent like they text a friend. It replies, quotes and takes payment.</p><p class="r3">{C} SMS for agents. <a href="/sms">Bitcoin by text</a></p>' + media('sms', CHAT('Table for 2 at 8?', 'Booked. 500 sats deposit?', 'Y')) + '<p class="q r4">Finally, a good reason to reply to a text.</p>', 's-lime', 6,
        deco=bg('stripes', BLOB('#7ee0a1', 60, 50, 90), emo(['phone', 'chat', 'env', 'signal'], 6), wv=('rgba(17,17,17,.12)', 'rgba(126,224,161,.6)'))))
    P.append(page(f'<p class="k r1">Cover story &middot; receipts</p><h2 class="r2">Receipts <span class="gd">anyone can check.</span></h2><p class="r3">Every bWalletX payment settles on chain. You, your customer and anyone else see the same record.</p><p class="r3">{L} On-chain receipts.</p>' + media('receipts', '<div class="big gd">&#x2714;</div>') + '<p class="q r4">Arguments about who paid what get very short.</p>', 's-black', 7,
        deco=bg('grid', RING('rgba(255,210,77,.4)', 50, 40, 90) + RING('rgba(255,210,77,.2)', 40, 30, 120), emo(['receipt', 'link', 'search', 'ok'], 7))))
    P.append(page(f'<p class="k r1">This week &middot; 5.2.26</p><h2 class="r2">New in the wallet.</h2>' + media('release', '<div class="big gd">5.2.26</div>') + f'<ul class="st r3"><li>{L}White paper theme, minimalist bApp icons</li><li>{L}Your bAvatar is the menu</li><li>{L}Like &middot; 1&cent; buys a little of that token</li><li>{L}Album Spaces, synced video, pay to speak</li><li>{L}All 19 bApps sign in and pay</li><li>{N}Ask b sends error reports for you</li></ul><p class="r4"><a href="/releases">All releases</a></p>', 's-paper', 8,
        deco=bg('grid', BLOB('#ffd24d', 72, -12, 60), emo(['gift', 'rocket', 'party'], 8))))
    P.append(page('<p class="k r1">Also this week</p><h2 class="r2">Make it yours.</h2><div class="g r3">' + card('/themes/custom','og-themes-custom.png','Editions','Live &middot; your branded wallet') + card('/themes','og-themes-v2.png','Theme Store','Live &middot; new looks') + card('/credits','og-credits-v1.png','Credits card','Coming &middot; prepay') + card('/bshares','og-bshares-v3.jpg','bShares','Share registers') + '</div>', 's-orange', 9,
        deco=bg('dots', BLOB('#ffd24d', 65, 60, 80) + RING('#111', -8, -6, 50), emo(['art', 'gem', 'card', 'spark'], 9), wv=('rgba(255,210,77,.4)', 'rgba(255,255,255,.3)'))))
    P.append(page('<p class="k r1">Also this week</p><h2 class="r2">Rooms, spots, ice-cream.</h2><div class="g r3">' + card('https://www.bchatx.com/room/new/invite/b-creative','og-chat-v2.png','bChatX rooms','Live &middot; a token per room',True) + card('/b-creative','og-b-creative.png','b creative','The spot') + card('/digital-ice-cream','og-digital-ice-cream-v1.png','Digital Ice-Cream','Three friends, one token') + card('/bapps','og-bapps-v1.png','bApps','Live &middot; all 19') + '</div>', 's-peach', 10,
        deco=bg('dots', BLOB('#ffb347', 70, 70, 70) + BLOB('#ff9ec4', -10, 20, 50), emo(['ice', 'cake', 'berry', 'donut', 'party', 'balloon', 'note', 'head', 'art', 'rainbow', 'heart', 'spark', 'sun', 'flower', 'cool', 'ball'], 10, 'all'))))
    P.append(page(f'<p class="k r1">Where things stand</p><h2 class="r2">Live today.</h2><ul class="st r3"><li>{L}On-chain receipts for every payment</li><li>{L}BRC-100: any site or agent can ask bWalletX to pay or sign. <a href="/developers">Developers</a></li><li>{L}CLI + MCP agent wallet with cap, Stop, rate limit. <a href="/cli">CLI</a></li><li>{L}Ask b, the assistant inside the wallet</li><li>{L}Your own theme for $99 a year. <a href="/themes/custom">Editions</a></li><li>{L}A bChatX room with its own token</li></ul>', 's-cream', 11,
        deco=bg('grid', BLOB('#7ee0a1', 75, 70, 60), emo(['ok', 'link', 'rocket'], 11))))
    P.append(page(f'<p class="k r1">Where things stand</p><h2 class="r2">On the way.</h2><ul class="st r3"><li>{N}Agent from a link</li><li>{N}Error reports from Ask b</li><li>{N}Capped agent account in the app</li><li>{C}SMS for agents. <a href="/sms">Bitcoin by text</a></li><li>{C}bCredits: prepay for b. <a href="/credits">Credits</a></li><li>{C}Share one fact, such as over 18. <a href="/identity">Identity</a></li></ul>', 's-black', 12,
        deco=bg('grid', RING('rgba(255,210,77,.35)', 60, 55, 80), emo(['soon', 'rocket', 'cal'], 12))))
    P.append(page('<p class="k r1">Next week</p><h2 class="r2">Same time, same beer.</h2><p class="r3">A new issue every week: everything we shipped, nicely presented.</p>' + media('next', '<img class="beer2" src="/images/twemoji-beer.svg" alt="" />') + '<a class="btn r4" href="/get">Get bWalletX &rarr;</a><p class="q r4">Less noise. More life. Just b.</p>', 's-gold', 13,
        deco=bg('dots', RING('#111', 60, 40, 80), emo(['soon', 'sunrise', 'gift'], 13), wv=('rgba(255,255,255,.35)', 'rgba(17,17,17,.12)'))))
    P.append(page('<p class="k r1">Back cover</p><h2 class="r2">Just b.</h2>' + media('lifestyle', '<div class="big gd">b</div>') + '<p class="k r3">Past issues</p><div class="r3">' + back + '</div><p class="foot2">By The Bitcoin Corporation Ltd &middot; Emoji: Twemoji, CC-BY 4.0 &middot; Music: original, made in your browser</p>', 's-back', hard=True,
        deco=bg('grid', BLOB('radial-gradient(circle,#f5b800,transparent 70%)', 40, 50, 100), emo(['beer', 'clink', 'notes', 'cool'], 14))))
    return P

CSS = r'''
:root{--ink:#111;--gold:#f5b800;--gold2:#ffd24d;--hf:'Space Grotesk',sans-serif;--bf:'IBM Plex Sans',sans-serif;--mono:'IBM Plex Mono',ui-monospace,monospace;color-scheme:light}
*{box-sizing:border-box}html,body{margin:0;background:#0b0a08;color:var(--ink);font-family:var(--bf);overflow-x:hidden;max-width:100vw}
body{overflow:hidden;height:100dvh}body.stack{overflow:auto;height:auto}
.tb{position:fixed;inset:0 0 auto;height:44px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;z-index:50;pointer-events:none}
.tb>*{pointer-events:auto}
.tb a.brand{display:flex;gap:8px;align-items:center;color:#fff;text-decoration:none;font:700 1rem var(--hf);mix-blend-mode:difference}
.tb details{position:relative;font:500 .7rem var(--mono);letter-spacing:.12em;text-transform:uppercase}
.tb summary{cursor:pointer;list-style:none;padding:7px 12px;border-radius:99px;background:rgba(0,0,0,.55);color:#fff;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.tb details ul{position:absolute;right:0;top:120%;margin:0;padding:6px;list-style:none;background:rgba(0,0,0,.85);border-radius:12px;min-width:220px}
.tb details a{display:block;padding:10px 12px;color:#fff;text-decoration:none}
.ctl{position:fixed;z-index:40;display:none}.on .ctl{display:flex}
.arw{top:50%;transform:translateY(-50%);width:46px;height:46px;border-radius:50%;border:0;background:rgba(0,0,0,.45);color:#fff;font-size:1.3rem;cursor:pointer;align-items:center;justify-content:center;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.arw.prev{left:12px}.arw.next{right:12px}.arw:disabled{opacity:.15}
.dots{left:50%;bottom:14px;transform:translateX(-50%);gap:6px;padding:7px 10px;border-radius:99px;background:rgba(0,0,0,.45);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.dots button{width:7px;height:7px;border-radius:50%;border:0;padding:0;background:rgba(255,255,255,.45);cursor:pointer}
.dots button.cur{background:var(--gold2);width:20px;border-radius:4px}
.mute{right:14px;bottom:12px;width:40px;height:40px;border-radius:50%;border:0;background:rgba(0,0,0,.55);color:#ffd24d;font-size:1rem;cursor:pointer;align-items:center;justify-content:center}
.gate{position:fixed;inset:0;z-index:60;display:none;flex-direction:column;align-items:center;justify-content:center;gap:14px;background:radial-gradient(circle at 50% 55%,rgba(0,0,0,.35),rgba(0,0,0,.82));color:#fff;text-align:center;padding:16px}
.on .gate{display:flex}.gate.gone{opacity:0;pointer-events:none;transition:opacity .5s}
.gate button{font:700 clamp(1.4rem,5vw,2rem) var(--hf);letter-spacing:-.02em;padding:22px 46px;border-radius:99px;border:0;cursor:pointer;color:#111;background:linear-gradient(180deg,#fff3b0,#ffd24d 45%,#f5b800);box-shadow:0 0 0 8px rgba(255,210,77,.18),0 20px 50px -10px rgba(245,184,0,.7);animation:pulse 2.2s ease-in-out infinite}
.gate small{font:500 .72rem var(--mono);letter-spacing:.16em;text-transform:uppercase;opacity:.8}
@keyframes pulse{50%{box-shadow:0 0 0 16px rgba(255,210,77,.08),0 20px 60px -10px rgba(245,184,0,.9)}}
.page{overflow:hidden;container-type:size;position:relative}
body.stack .page{width:100vw;height:100dvh;min-height:640px}
.pin{position:relative;z-index:2;height:100%;padding:max(64px,8cqh) max(16px,8cqw) 10cqh;display:flex;flex-direction:column;gap:2.2cqh;font-size:clamp(15px,min(2.4cqh,4.2cqw),22px);line-height:1.45;overflow:hidden}
.pin p{margin:0;max-width:34em}.pin a{color:inherit;text-underline-offset:3px}
.sheen{position:absolute;inset:0;z-index:3;pointer-events:none;background:linear-gradient(120deg,rgba(255,255,255,0) 30%,rgba(255,255,255,.22) 45%,rgba(255,255,255,0) 60%);background-size:250% 100%;background-position:100% 0}
.in .sheen{animation:sheen 1.6s ease-out .2s}
@keyframes sheen{from{background-position:100% 0}to{background-position:-60% 0}}
/* background art */
.bg{position:absolute;inset:0;z-index:1;overflow:hidden;pointer-events:none}
.bg.pat-dots::before,.bg.pat-grid::before,.bg.pat-stripes::before{content:"";position:absolute;inset:0;opacity:.5}
.bg.pat-dots::before{background:radial-gradient(currentColor 1.2px,transparent 1.6px) 0 0/18px 18px;opacity:.12}
.bg.pat-grid::before{background:linear-gradient(rgba(255,210,77,.08) 1px,transparent 1px) 0 0/40px 40px,linear-gradient(90deg,rgba(255,210,77,.08) 1px,transparent 1px) 0 0/40px 40px;opacity:1}
.s-paper .bg.pat-grid::before,.s-cream .bg.pat-grid::before{background:linear-gradient(rgba(17,17,17,.06) 1px,transparent 1px) 0 0/40px 40px,linear-gradient(90deg,rgba(17,17,17,.06) 1px,transparent 1px) 0 0/40px 40px}
.bg.pat-stripes::before{background:repeating-linear-gradient(-45deg,rgba(255,255,255,.18) 0 14px,transparent 14px 34px);opacity:1}
.bgimg{position:absolute;right:-10%;top:0;width:85%;height:100%;object-fit:cover;opacity:.35;-webkit-mask-image:linear-gradient(90deg,transparent,#000 60%),linear-gradient(transparent,#000 30%,#000 70%,transparent);mask-image:linear-gradient(90deg,transparent,#000 70%);filter:saturate(1.2)}
.blob{position:absolute;aspect-ratio:1;border-radius:50%;opacity:.55;filter:blur(2px);transform:translate(-50%,-50%)}
.ring{position:absolute;aspect-ratio:1;border-radius:50%;border:2px solid;opacity:.35;transform:translate(-50%,-50%)}
.wv{position:absolute;left:0;right:0;bottom:0;width:100%;height:24%}
.em{position:absolute;height:auto;transform:rotate(var(--r));filter:drop-shadow(0 8px 12px rgba(0,0,0,.25));animation:bob 6s ease-in-out infinite;opacity:.95}
@keyframes bob{50%{transform:rotate(var(--r)) translateY(-8px)}}
.k{font:500 clamp(11px,1.5cqh,14px) var(--mono);letter-spacing:.18em;text-transform:uppercase;opacity:.75;display:flex;gap:12px;align-items:center}
.k::after{content:"";flex:1;border-top:1px solid currentColor;opacity:.5}
.pin h2{font:700 min(9cqh,13cqw)/.92 var(--hf);letter-spacing:-.045em;margin:0}
.gd{background:linear-gradient(180deg,#fff3b0,#ffd24d 45%,#f5b800 60%,#b98500);-webkit-background-clip:text;background-clip:text;color:transparent}
.q{font:italic 500 1.05em var(--hf);border-left:3px solid currentColor;padding-left:12px}
.p{font:600 .62em var(--mono);font-style:normal;letter-spacing:.1em;text-transform:uppercase;border:1.5px solid currentColor;padding:2px 8px;margin-right:8px;white-space:nowrap;border-radius:99px;vertical-align:2px}
.s-black .p.l,.s-back .p.l,.s-cover .p.l{background:var(--gold2);color:#111;border-color:var(--gold2)}
.s-cream .p.l,.s-yellow .p.l,.s-pink .p.l,.s-lime .p.l,.s-paper .p.l,.s-orange .p.l,.s-peach .p.l,.s-gold .p.l{background:#111;color:#fff;border-color:#111}
img.og{width:100%;height:auto;aspect-ratio:1200/630;object-fit:cover;display:block;border-radius:14px;box-shadow:0 30px 60px -25px rgba(0,0,0,.6)}
.media{flex:1 1 auto;min-height:0;display:flex;align-items:center;justify-content:center;position:relative}
.media>img:not(.og):not(.beer2),.media>video,.media>picture,.media>picture>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:14px}
.media .og{max-height:100%;width:auto;max-width:100%}
.folio{position:absolute;left:max(16px,8cqw);bottom:max(3cqh,54px);font:400 11px var(--mono);letter-spacing:.14em;text-transform:uppercase;opacity:.55;margin:0}
.st{list-style:none;padding:0;margin:0}
.st li{padding:1.4cqh 0;border-bottom:1px solid rgba(127,127,127,.4)}
.toc{list-style:none;padding:0;margin:0}
.toc li{display:flex;justify-content:space-between;gap:12px;padding:1.3cqh 0;border-bottom:1px solid rgba(0,0,0,.25);font:600 1.15em var(--hf)}
.toc b{font:500 .8em var(--mono)}
.g{display:grid;grid-template-columns:1fr 1fr;gap:3cqh 4cqw;min-height:0}
.cd{text-decoration:none;color:inherit}.cd b{display:block;margin-top:8px;font:700 1.05em var(--hf)}.cd span{display:block;font:400 .7em var(--mono);letter-spacing:.08em;text-transform:uppercase;opacity:.7}
.btn{display:block;text-align:center;background:#111;color:#ffd24d!important;text-decoration:none;font:700 1.3em var(--hf);padding:18px;border-radius:99px;max-width:420px}
.chat{display:flex;flex-direction:column;gap:12px;width:min(100%,420px);padding:20px;border-radius:30px;background:rgba(255,255,255,.96);border:2px solid #111;font:600 1.05em var(--bf);box-shadow:0 40px 70px -30px rgba(0,0,0,.7);color:#111}
.chat div{padding:10px 14px;border-radius:18px;max-width:85%}
.chat .u{align-self:flex-end;background:#111;color:#fff}.chat .a{background:#ffd24d;border:1.5px solid #111}
.chat .rc{align-self:center;font:600 .65em var(--mono);letter-spacing:.14em;text-transform:uppercase;border-radius:99px;background:#7ee0a1;border:1.5px solid #111}
.big{font:700 min(26cqh,40cqw)/1 var(--hf);letter-spacing:-.06em}
.stopb{color:#fff;background:#e0303a;border-radius:50%;aspect-ratio:1;display:grid;place-items:center;font-size:min(9cqh,14cqw);width:min(30cqh,50cqw);box-shadow:inset 0 -10px 0 rgba(0,0,0,.2),0 20px 40px -10px rgba(224,48,58,.6)}
.beer2{width:min(36cqh,60cqw);height:auto}
/* scenes */
.s-cover,.s-black,.s-back{background:radial-gradient(120% 80% at 80% 0%,#3a2e00 0%,#0b0a08 55%);color:#f1ead9}
.s-cream{background:linear-gradient(160deg,#fffdf0,#fff0a8);color:#111}
.s-yellow{background:linear-gradient(160deg,#ffe14d,#ffb347);color:#111}
.s-pink{background:linear-gradient(160deg,#ffd0e4,#ff9ec4);color:#111}
.s-lime{background:linear-gradient(160deg,#e8ff7a,#a8f07a);color:#111}
.s-paper{background:#f7f6f2;color:#111}
.s-orange{background:linear-gradient(160deg,#ffb347,#ff7a3d);color:#111}
.s-peach{background:linear-gradient(160deg,#ffd9a3,#ffd0e4);color:#111}
.s-gold{background:linear-gradient(160deg,#ffe680,#f5b800 60%,#c48a00);color:#111}
/* cover */
.s-cover .pin{padding-top:max(52px,6cqh)}
.s-cover .media[data-media="cover"]{position:absolute;inset:0;z-index:0}
.s-cover .media[data-media="cover"]>img,.s-cover .media[data-media="cover"]>video{border-radius:0}
.s-cover .media[data-media="cover"]::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,10,8,.85) 0%,rgba(11,10,8,0) 30%,rgba(11,10,8,0) 55%,rgba(11,10,8,.9) 100%);pointer-events:none}
.hero{position:absolute;inset:0;overflow:hidden;background:radial-gradient(90% 60% at 70% 55%,#4a3700,#0b0a08 70%)}
.hero .blob{opacity:.9;filter:none}
.bigb{position:absolute;right:-4%;top:22%;font:700 min(70cqh,110cqw)/.8 var(--hf);letter-spacing:-.08em;color:transparent;background:linear-gradient(160deg,#fff7c9,#ffd24d 40%,#c48a00 70%,#fff3b0);-webkit-background-clip:text;background-clip:text;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6));opacity:.95}
.cchat{position:absolute;left:6%;top:43%;width:min(62%,380px);transform:rotate(-4deg);font-size:.82em;z-index:1}
.mh{position:relative;z-index:2;font:700 min(14cqh,19cqw)/.82 var(--hf);letter-spacing:-.065em;text-transform:uppercase;white-space:nowrap;color:#ffd24d;margin:0;text-shadow:0 6px 30px rgba(0,0,0,.6)}
.mh em{font-style:normal;text-transform:none}
.dl{position:relative;z-index:2;display:flex;justify-content:space-between;font:500 clamp(10px,1.4cqh,13px) var(--mono);letter-spacing:.14em;text-transform:uppercase;border-block:1.5px solid rgba(255,210,77,.7);padding:8px 0}
.hl{position:relative;z-index:2;font:700 min(7cqh,11cqw)/.92 var(--hf);letter-spacing:-.045em;max-width:9em;text-shadow:0 4px 24px rgba(0,0,0,.6)}
.cl{position:absolute;z-index:2;right:max(16px,6cqw);top:34cqh;width:min(36%,240px);list-style:none;padding:0;margin:0;text-align:right;font:400 clamp(10px,1.3cqh,13px) var(--mono);letter-spacing:.08em;text-transform:uppercase;color:#f1ead9}
.cl li{padding:1.2cqh 0;border-bottom:1px solid rgba(255,210,77,.5);text-shadow:0 2px 10px #000}
.cl b{display:block;font:700 clamp(15px,2.4cqh,24px) var(--hf);letter-spacing:-.02em;text-transform:none;color:#ffd24d}
.bc{position:absolute;z-index:2;left:max(16px,6cqw);bottom:max(60px,6cqh);display:flex;gap:10px;align-items:stretch;background:#fff;color:#111;padding:8px;border-radius:4px;width:min(46%,230px)}
.bc .pr{display:flex;flex-direction:column;justify-content:center;font:500 10px var(--mono);letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}.bc .pr b{font:700 15px var(--hf);letter-spacing:0;text-transform:none}
.bc svg{flex:1;height:auto;min-height:38px;fill:#111}
.s-cover .sheen{background:linear-gradient(115deg,rgba(255,255,255,0) 35%,rgba(255,255,255,.28) 46%,rgba(255,255,255,0) 52%),linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,0) 40%);background-size:250% 100%,100% 100%}
.s-cover .hl .gd{background:none;color:#ffd24d;-webkit-text-fill-color:#ffd24d;text-shadow:0 3px 0 #000,0 8px 30px rgba(0,0,0,.9)}
.hero .em{opacity:.55}.bigb{opacity:.6;top:34%}
.cl{background:rgba(11,10,8,.62);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);padding:4px 12px!important;border-radius:6px}
@container (max-width:600px){.s-cover .cl{top:auto;bottom:max(60px,6cqh);width:48%}.s-cover .cl li{padding:.7cqh 0}.s-cover .cl b{font-size:15px}.cchat{top:36%;width:64%}.bc{width:44%}}
.page>.media.photo{position:absolute;inset:0;z-index:0;margin:0}
.page>.media.photo img,.page>.media.photo video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:0}
.wash{position:absolute;inset:0;z-index:0;background:linear-gradient(180deg,var(--w) 0%,color-mix(in srgb,var(--w) 88%,transparent) 38%,color-mix(in srgb,var(--w) 0%,transparent) 66%,color-mix(in srgb,var(--w) 55%,transparent) 100%)}
.page{--w:#0b0a08}.s-cream{--w:#fffdf0}.s-yellow{--w:#ffe14d}.s-pink{--w:#ffd0e4}.s-lime{--w:#e8ff7a}.s-paper{--w:#f7f6f2}.s-orange{--w:#ffb347}.s-peach{--w:#ffd9a3}.s-gold{--w:#ffd24d}
.page:has(>.media.photo) .bg .blob,.page:has(>.media.photo) .bg .ring,.page:has(>.media.photo) .bgimg,.page:has(>.media.photo) .wv{display:none}.page:has(>.media.photo) .bg::before{opacity:.35!important}
.spacer{flex:1}
.s-cover>.wash{background:linear-gradient(180deg,rgba(11,10,8,.85) 0%,rgba(11,10,8,.2) 32%,rgba(11,10,8,0) 55%,rgba(11,10,8,.85) 100%)}
.book{transition:transform .7s cubic-bezier(.2,.8,.2,1)}
.foot2{margin-top:auto!important;font:400 11px var(--mono);letter-spacing:.1em;text-transform:uppercase;opacity:.6}
.s-back .cd{display:grid;grid-template-columns:44% 1fr;gap:16px;align-items:center}
/* turn-in motion */
.on .page .r1,.on .page .r2,.on .page .r3,.on .page .r4,.on .page .pin>.media{opacity:0;transform:translateY(24px)}
.on .page.in .r1,.on .page.in .r2,.on .page.in .r3,.on .page.in .r4,.on .page.in .pin>.media{opacity:1;transform:none;transition:opacity .6s ease,transform .7s cubic-bezier(.2,.8,.2,1)}
.on .page.in .r2{transition-delay:.08s}.on .page.in .r3{transition-delay:.16s}.on .page.in .pin>.media{transition-delay:.22s}.on .page.in .r4{transition-delay:.3s}
.on .s-cover .r4{transform:none!important}
@media (prefers-reduced-motion:reduce){.sheen{display:none}.em{animation:none}}
'''

JS = r'''<script src="https://cdn.jsdelivr.net/npm/page-flip@2.0.7/dist/js/page-flip.browser.js"></script>
<script>
// Lounge loop: original, synthesised with Web Audio (adapted from the b-creative engine, lighter). Starts only after Open.
var Lounge=(function(){var ctx,master,verb,keys,nb,on=false,step=0,next=0,timer,BPM=92,S=60/BPM/4;
function mtof(m){return 440*Math.pow(2,(m-69)/12)}
function env(g,t,a,p,d){g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(p,t+a);g.gain.exponentialRampToValueAtTime(.0001,t+d)}
function init(){ctx=new(window.AudioContext||window.webkitAudioContext)();var c,d,i;
var comp=ctx.createDynamicsCompressor();comp.threshold.value=-16;comp.ratio.value=3;master=ctx.createGain();master.gain.value=.0001;master.connect(comp);comp.connect(ctx.destination);
verb=ctx.createConvolver();var len=ctx.sampleRate*2.6|0,ir=ctx.createBuffer(2,len,ctx.sampleRate);for(c=0;c<2;c++){d=ir.getChannelData(c);for(i=0;i<len;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/len,3)}
verb.buffer=ir;var vg=ctx.createGain();vg.gain.value=.3;verb.connect(vg);vg.connect(master);
keys=ctx.createGain();keys.gain.value=.9;keys.connect(master);var ks=ctx.createGain();ks.gain.value=.5;keys.connect(ks);ks.connect(verb);
nb=ctx.createBuffer(1,ctx.sampleRate,ctx.sampleRate);d=nb.getChannelData(0);for(i=0;i<d.length;i++)d[i]=Math.random()*2-1}
function noise(t,type,f,v,dec,q){var s=ctx.createBufferSource(),fl=ctx.createBiquadFilter(),g=ctx.createGain();s.buffer=nb;fl.type=type;fl.frequency.value=f;if(q)fl.Q.value=q;env(g,t,.001,v,dec);s.connect(fl);fl.connect(g);g.connect(master);s.start(t,Math.random()*.5);s.stop(t+dec+.02)}
function kick(t){var o=ctx.createOscillator(),g=ctx.createGain();o.frequency.setValueAtTime(120,t);o.frequency.exponentialRampToValueAtTime(45,t+.12);env(g,t,.003,.5,.35);o.connect(g);g.connect(master);o.start(t);o.stop(t+.4)}
function ep(t,notes,len,v){notes.forEach(function(m){var f=mtof(m),c=ctx.createOscillator(),md=ctx.createOscillator(),mg=ctx.createGain(),g=ctx.createGain();c.frequency.value=f;md.frequency.value=f;mg.gain.setValueAtTime(f*1.1,t);mg.gain.exponentialRampToValueAtTime(f*.05,t+.4);md.connect(mg);mg.connect(c.frequency);
g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(v,t+.01);g.gain.exponentialRampToValueAtTime(v*.3,t+len);g.gain.exponentialRampToValueAtTime(.0001,t+len+.3);c.connect(g);g.connect(keys);c.start(t);md.start(t);c.stop(t+len+.35);md.stop(t+len+.35)})}
function bass(t,m,len){var o=ctx.createOscillator(),g=ctx.createGain(),f=ctx.createBiquadFilter();o.type='triangle';o.frequency.value=mtof(m);f.type='lowpass';f.frequency.value=600;env(g,t,.01,.32,len);o.connect(f);f.connect(g);g.connect(master);o.start(t);o.stop(t+len+.05)}
var CH=[[62,66,69,73,76],[59,62,66,69,73],[55,59,62,66,69],[57,61,64,67,71]],BS=[38,35,31,33],MEL=[78,null,76,null,73,null,null,71,73,null,null,null,69,null,71,null];
function tick(t,s){var bar=Math.floor(s/16)%4,b=s%16;
if(b===0||b===10)kick(t);if(b===4||b===12)noise(t,'bandpass',1800,.12,.08,2);
if(b%2===0)noise(t+(b%4===2?S*.18:0),'highpass',8000,b%4===2?.05:.03,.04);
if(b===0)ep(t,CH[bar],S*7,.05);if(b===7)ep(t,CH[bar].slice(1,4),S*3,.035);
if(b===0)bass(t,BS[bar],S*3);if(b===6)bass(t,BS[bar]+7,S*1.5);if(b===10)bass(t,BS[bar],S*2);
var m=MEL[b];if(m&&(Math.floor(s/64)%2===1))ep(t,[m+(bar===3?-2:0)],S*2,.045)}
function loop(){while(next<ctx.currentTime+.2){tick(next,step);step++;next+=S}}
return{start:function(){if(!ctx)init();ctx.resume();if(on)return;on=true;next=ctx.currentTime+.08;master.gain.setTargetAtTime(.7,ctx.currentTime,.6);timer=setInterval(loop,50)},
toggle:function(){if(!ctx)return false;if(on){master.gain.setTargetAtTime(.0001,ctx.currentTime,.15);on=false;setTimeout(function(){if(!on)clearInterval(timer)},400)}else{this.start()}return on}}})();
(function(){var el=document.getElementById('book');
if(!window.St||matchMedia('(prefers-reduced-motion: reduce)').matches){document.body.classList.add('stack');return}
document.body.classList.add('on');
var pages=[].slice.call(el.querySelectorAll('.page')),W=document.documentElement.clientWidth,H=document.documentElement.clientHeight,two=W>=900;
var pf=new St.PageFlip(el,{width:two?Math.floor(W/2):W,height:H,size:'fixed',showCover:two,usePortrait:!two,mobileScrollSupport:false,flippingTime:800,drawShadow:true,maxShadowOpacity:.5,autoSize:false});
pf.loadFromHTML(pages);
function spreadOf(c){return two?(c===0?0:Math.floor((c+1)/2)):c}function pageOf(k){return two?(k===0?0:2*k-1):k}
var dots=document.querySelector('.dots'),nS=spreadOf(pages.length-1)+1;
for(var i=0;i<nS;i++){(function(k){var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Spread '+(k+1));b.onclick=function(){pf.flip(pageOf(k))};dots.appendChild(b)})(i)}
var m=/^#p(\d+)$/.exec(location.hash),deep=m&&+m[1]>1;if(deep)pf.turnToPage(Math.min(pages.length-1,m[1]-1));
function ui(){var c=pf.getCurrentPageIndex();if(two){var sh=c===0?-W/4:(c>=pages.length-1&&pages.length%2===0?W/4:0);el.style.transform='translateX('+sh+'px)'}pages.forEach(function(p,k){p.classList.toggle('in',k===c||(two&&c>0&&k===c+1))});
[].forEach.call(dots.children,function(d,k){d.classList.toggle('cur',k===spreadOf(c))});
document.querySelector('.arw.prev').disabled=c===0;document.querySelector('.arw.next').disabled=spreadOf(c)>=nS-1}
pf.on('changeState',function(e){if(two&&e.data==='flipping'&&pf.getCurrentPageIndex()===0)el.style.transform='translateX(0)'});pf.on('flip',function(){ui();history.replaceState(null,'','#p'+(pf.getCurrentPageIndex()+1))});setTimeout(ui,60);
document.querySelector('.arw.prev').onclick=function(){pf.flipPrev()};document.querySelector('.arw.next').onclick=function(){pf.flipNext()};
addEventListener('keydown',function(e){if(e.key==='ArrowRight')pf.flipNext();if(e.key==='ArrowLeft')pf.flipPrev()});
var gate=document.querySelector('.gate'),mute=document.querySelector('.mute');mute.style.display='none';
if(deep)gate.classList.add('gone');
function open(){gate.classList.add('gone');try{Lounge.start();mute.style.display='';mute.textContent='♫';mute.setAttribute('aria-pressed','false')}catch(e){}if(pf.getCurrentPageIndex()===0)setTimeout(function(){pf.flipNext()},250)}
gate.querySelector('button').onclick=open;
mute.onclick=function(){var on=Lounge.toggle();mute.textContent=on?'♫':'×';mute.setAttribute('aria-label',on?'Mute music':'Play music')};
var t;addEventListener('resize',function(){clearTimeout(t);t=setTimeout(function(){if(Math.abs(document.documentElement.clientWidth-W)>60||Math.abs(document.documentElement.clientHeight-H)>120)location.reload()},400)});
})();</script>'''

def head(url, title, desc, img, alt):
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <link rel="canonical" href="https://bwalletx.com{url}" />
    <meta name="description" content="{desc}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://bwalletx.com{url}" />
    <meta property="og:site_name" content="bWalletX" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:image" content="https://bwalletx.com/{img}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="{alt}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bWalletX" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="https://bwalletx.com/{img}" />
    <link rel="icon" href="/favicon.ico" />
    <meta name="theme-color" content="#f7f6f2" />
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />
    <style>{CSS}</style>
  </head>
'''

OG_COVER = 'og-hodl-my-b-cover.png?v=2'  # share image for the landing and the latest issue

def build():
    back = ''.join(card(f'/hodl-my-b/{i["n"]}', i['og'], f'Issue {i["n"]} &middot; week of {i["week"]}', i['blurb']) for i in reversed(ISSUES))
    menu = ''.join(f'<li><a href="/hodl-my-b/{i["n"]}">Issue {i["n"]} &middot; {i["week"]}</a></li>' for i in reversed(ISSUES))
    for i in ISSUES:
        pages = globals()[f'pages_issue_{i["n"]}'](back)
        body = f'''  <body>
    <header class="tb"><a class="brand" href="/"><img src="/logo.svg" alt="" width="27" height="24" />bWalletX</a>
      <details><summary>Issue {i["n"]} &#9662;</summary><ul>{menu}<li><a href="/hodl-my-b">Latest</a></li></ul></details></header>
    <main><div class="book" id="book">{''.join(pages)}</div>
      <button class="ctl arw prev" type="button" aria-label="Previous page">&larr;</button><button class="ctl arw next" type="button" aria-label="Next page">&rarr;</button><nav class="ctl dots" aria-label="Pages"></nav><button class="ctl mute" type="button" aria-label="Mute music">&#9835;</button></main>
    <div class="gate" role="dialog" aria-label="Open the magazine"><button type="button">Open &rarr;</button><small>Hodl my b &middot; Issue {i["n"]} &middot; sound on</small></div>
    {JS}
  </body>
</html>
'''
        title = f'Hodl my b, Issue {i["n"]}: {i["story"]}'
        desc = f'Hodl my b, the weekly bWalletX magazine. Issue {i["n"]}, week of {i["week"]}: {i["blurb"]}'
        alt = f'Magazine cover: Hodl my b, Weekly, Issue {i["n"]}. {i["story"]}'
        open(os.path.join(ROOT, f'hodl-my-b/{i["n"]}.html'), 'w').write(head(f'/hodl-my-b/{i["n"]}', title, desc, OG_COVER, alt) + body)
        if i is ISSUES[-1]:
            open(os.path.join(ROOT, 'hodl-my-b.html'), 'w').write(head('/hodl-my-b', 'Hodl my b', 'Hodl my b: the weekly bWalletX magazine. Everything shipped each week, with what is live and what is coming.', OG_COVER, 'Magazine cover: Hodl my b, Weekly, Issue 1. Don&#39;t be bland. Get bRanded.') + body)

build()
