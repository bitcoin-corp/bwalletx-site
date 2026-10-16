#!/usr/bin/env python3
"""Builds the Hodl my b flipbook. Latest issue is /hodl-my-b (hodl-my-b.html); each issue also at /hodl-my-b/<n>.
Edit ISSUES / pages_issue_N below, then: python3 scripts/hodl-my-b.py && python3 scripts/seo-head.py && python3 scripts/gen-llms.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = '<i class="p l">Live</i>'; N = '<i class="p">Next release</i>'; C = '<i class="p">Coming</i>'
BEER = '<img class="beer" src="/images/twemoji-beer.svg" alt="" width="72" height="72" />'
ISSUES = [  # newest last
    dict(n=1, week='12 Oct 2026', story='Don&rsquo;t be bland. Get bBranded.', og='og-hodl-my-b-1.png',
         blurb='Business agents, plus the week&rsquo;s round-up.'),
]

def card(href, img, t, s, ext=False):
    tg = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a class="cd" href="{href}"{tg}><img class="og" src="/{img}" alt="" width="1200" height="630" /><b>{t}</b><span>{s}</span></a>'

def page(body, cls='', n=None, issue=1):
    folio = f'<p class="folio">Hodl my b &middot; Issue {issue} &middot; {n}</p>' if n else ''
    return f'<div class="page {cls}"><div class="pin">{body}{folio}</div></div>'

def pages_issue_1(back):
    P = []
    P.append(page('''<p class="mh">Hodl my <em>b</em> ''' + BEER + '''</p>
<p class="dl"><span>Weekly</span><span>Issue 1</span><span>Week of 12 Oct 2026</span></p>
<p class="hl">Don&rsquo;t be bland. Get bBranded.</p>
<div class="chat" aria-hidden="true"><div class="u">Got the sticker pack?</div><div class="a">Yes! 1,500 sats. Tap to pay.</div><div class="u">Paid &#x2714;</div><div class="rc">Receipt on chain</div></div>
<ul class="cl"><li>Theme Store</li><li>Credits card</li><li>bChatX rooms</li><li>All 19 bApps</li></ul>
<span class="blob b1"></span><span class="blob b2"></span>''', 'cover hard'))
    P.append(page('''<p class="k">Inside</p><h2>This week</h2><ol class="toc">
<li><span>Paste a link, get a shopkeeper</span><b>3</b></li><li><span>The till is the chat</span><b>4</b></li>
<li><span>An agent with pocket money</span><b>5</b></li><li><span>Bitcoin by text</span><b>6</b></li>
<li><span>Receipts anyone can check</span><b>7</b></li><li><span>New in 5.2.26</span><b>8</b></li>
<li><span>Also this week</span><b>9</b></li><li><span>Where things stand</span><b>11</b></li></ol>
<p class="q">Every feature says plainly: Live, Next release, or Coming. Swipe, drag a corner, or use the arrow keys.</p>''', n=2))
    P.append(page(f'<p class="k">Cover story &middot; bBrand</p><h2>Paste a link. Get a shopkeeper.</h2><p>Give b your website. b reads it and drafts an agent that knows your menu, prices and hours, then answers customers in chat.</p><p>{N} Agent from a link. <a href="/business-agents">Business agents</a></p><img class="og" src="/og-business-agents-bbrand.png" alt="bBrand business agents" width="1200" height="630" /><p class="q">It never calls in sick. It does ask for a logo.</p>', n=3))
    P.append(page(f'<p class="k">Cover story &middot; checkout</p><h2>The till is the chat.</h2><p>Customer asks, agent quotes, customer taps Pay. Sats move, the chat says Paid, and both sides keep the same receipt.</p><p>{N} Chat checkout for business agents.</p><p class="q">No card machine. No &ldquo;it&rsquo;s gone through twice&rdquo;.</p><div class="chat" aria-hidden="true"><div class="u">Two flat whites?</div><div class="a">900 sats. Tap to pay.</div><div class="u">Paid &#x2714;</div></div>', n=4))
    P.append(page(f'<p class="k">Cover story &middot; pocket money</p><h2>An agent with a daily allowance.</h2><p>Agents get their own capped account: a daily limit, and a big Stop button for when it gets ideas above its station.</p><p>{C} Capped agent account inside the app.</p><p>{L} Today on your computer: the <code>bwalletx</code> CLI agent wallet, with a daily cap and Stop. <a href="/cli">CLI</a></p>', n=5))
    P.append(page(f'<p class="k">Cover story &middot; SMS</p><h2>Bitcoin by text.</h2><p>Customers text a business&rsquo;s agent like they text a friend. The agent replies, quotes and takes payment.</p><p>{C} SMS for agents. <a href="/sms">Bitcoin by text</a></p><p class="q">Finally, a good reason to reply to a text.</p>', n=6))
    P.append(page(f'<p class="k">Cover story &middot; receipts</p><h2>Receipts anyone can check.</h2><p>Every bWalletX payment settles on chain. You, your customer and anyone else see the same record. Arguments about who paid what get very short.</p><p>{L} On-chain receipts.</p>', n=7))
    P.append(page(f'<p class="k">This week &middot; 5.2.26</p><h2>New in the wallet.</h2><ul class="st"><li>{L}A White paper theme with minimalist bApp icons</li><li>{L}Your bAvatar is the menu</li><li>{L}Like &middot; 1&cent; on token cards buys a little of that token</li><li>{L}Album Spaces, synced video, pay to speak</li><li>{L}All 19 bApps sign in and pay with bWalletX</li><li>{N}Ask b sends error reports for you</li></ul><p><a href="/releases">All releases</a></p>', n=8))
    P.append(page('<p class="k">Also this week</p><div class="g">' + card('/themes/custom','og-themes-custom.png','Editions','Live &middot; your branded wallet') + card('/themes','og-themes-v2.png','Theme Store','Live &middot; new looks') + card('/credits','og-credits-v1.png','Credits card','Coming &middot; prepay') + card('/bshares','og-bshares-v3.jpg','bShares','Share registers') + '</div>', n=9))
    P.append(page('<p class="k">Also this week</p><div class="g">' + card('https://www.bchatx.com/room/new/invite/b-creative','og-b-creative.png','bChatX rooms','Live &middot; a token per room',True) + card('/b-creative','og-b-creative.png','b creative','The spot') + card('/digital-ice-cream','og-digital-ice-cream-v1.png','Digital Ice-Cream','Three friends, one token') + card('/bapps','og-bapps-v1.png','bApps','Live &middot; all 19') + '</div>', n=10))
    P.append(page(f'<p class="k">Where things stand</p><h2>Live today.</h2><ul class="st"><li>{L}On-chain receipts for every payment</li><li>{L}BRC-100: any site or agent can ask bWalletX to pay or sign. <a href="/developers">Developers</a></li><li>{L}CLI + MCP agent wallet with cap, Stop, rate limit. <a href="/cli">CLI</a></li><li>{L}Ask b, the assistant inside the wallet</li><li>{L}Your own theme for $99 a year. <a href="/themes/custom">Editions</a></li><li>{L}A bChatX room with its own token</li></ul>', n=11))
    P.append(page(f'<p class="k">Where things stand</p><h2>On the way.</h2><ul class="st"><li>{N}Agent from a link</li><li>{N}Error reports from Ask b</li><li>{C}Capped agent account in the app</li><li>{C}SMS for agents. <a href="/sms">Bitcoin by text</a></li><li>{C}bCredits: prepay for b. <a href="/credits">Credits</a></li><li>{C}Share one fact, such as over 18. <a href="/identity">Identity</a></li></ul>', n=12))
    P.append(page('<p class="k">Next week</p><h2>Same time, same beer.</h2><p>A new issue every week: everything we shipped, nicely presented.</p><a class="btn" href="/get">Get bWalletX &rarr;</a><p class="q">Less noise. More life. Just b.</p>', n=13))
    P.append(page('<p class="k">Back cover</p><h2>Past issues</h2>' + back + '<p class="foot2">By The Bitcoin Corporation Ltd &middot; Beer emoji: Twemoji, CC-BY 4.0</p>', 'back hard'))
    return P

CSS = r'''
:root{--paper:#f7f6f2;--sheet:#fff;--ink:#111;--muted:#5d5b56;--hair:#d9d6ce;--hf:'Space Grotesk',sans-serif;--bf:'IBM Plex Sans',sans-serif;--mono:'IBM Plex Mono',ui-monospace,monospace;color-scheme:light}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--paper);color:var(--ink);font-family:var(--bf);background-image:linear-gradient(rgba(17,17,17,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(17,17,17,.055) 1px,transparent 1px);background-size:40px 40px;min-height:100vh}
.tb{height:48px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;border-bottom:1px solid var(--ink);background:var(--paper);position:relative;z-index:5}
.tb a.brand{display:flex;gap:8px;align-items:center;color:var(--ink);text-decoration:none;font:700 1.05rem var(--hf)}
.tb details{position:relative;font:500 .74rem var(--mono);letter-spacing:.12em;text-transform:uppercase}
.tb summary{cursor:pointer;list-style:none;border:1px solid var(--ink);padding:7px 10px;background:var(--sheet)}
.tb details ul{position:absolute;right:0;top:110%;margin:0;padding:0;list-style:none;background:var(--sheet);border:1px solid var(--ink);min-width:220px}
.tb details a{display:block;padding:10px 12px;color:var(--ink);text-decoration:none}
.stage{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:16px;min-height:calc(100vh - 48px)}
.book{width:100%;max-width:1040px}
.nav{display:none;gap:10px;align-items:center;margin-top:14px;font:500 .72rem var(--mono);letter-spacing:.12em;text-transform:uppercase}
.on .nav{display:flex}
.nav button{font:inherit;letter-spacing:inherit;text-transform:inherit;border:1px solid var(--ink);background:var(--sheet);color:var(--ink);padding:9px 14px;cursor:pointer}
/* pages */
.page{background:var(--sheet);border:1px solid var(--ink);container-type:inline-size;overflow:hidden}
.book:not(.on) .page{max-width:520px;aspect-ratio:5/7;margin:0 auto 20px}
.pin{position:relative;height:100%;padding:7cqw 7cqw 9cqw;display:flex;flex-direction:column;gap:2.6cqw;font-size:3.6cqw;line-height:1.45}
.pin p{margin:0}.pin a{color:var(--ink);text-underline-offset:2px}
.k{font:500 2.6cqw var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--muted);display:flex;gap:3cqw;align-items:center}
.k::after{content:"";flex:1;border-top:.5px solid var(--ink)}
.pin h2{font:700 9cqw/.98 var(--hf);letter-spacing:-.04em;margin:0}
.q{font:italic 500 3.8cqw var(--hf);border-left:2px solid var(--ink);padding-left:3cqw}
.p{font:500 2.3cqw var(--mono);font-style:normal;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--ink);padding:.5cqw 1.6cqw;margin-right:2cqw;white-space:nowrap;vertical-align:1px}
.p.l{background:var(--ink);color:var(--paper)}
img.og{width:100%;height:auto;aspect-ratio:1200/630;object-fit:cover;border:1px solid var(--ink);display:block}
.folio{position:absolute;left:7cqw;right:7cqw;bottom:3.5cqw;font:400 2.2cqw var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);border-top:.5px solid var(--ink);padding-top:1.6cqw}
.st{list-style:none;padding:0;margin:0;border-top:.5px solid var(--ink)}
.st li{padding:2.2cqw 0;border-bottom:.5px solid var(--ink);font-size:3.4cqw}
.toc{list-style:none;padding:0;margin:0;counter-reset:t}
.toc li{display:flex;justify-content:space-between;gap:3cqw;padding:2.2cqw 0;border-bottom:.5px solid var(--ink);font:600 4.2cqw var(--hf)}
.toc b{font:500 3cqw var(--mono)}
.g{display:grid;grid-template-columns:1fr 1fr;gap:4cqw}
.cd{text-decoration:none;color:var(--ink)}
.cd b{display:block;margin-top:1.6cqw;font:600 3.6cqw var(--hf)}.cd span{display:block;font:400 2.4cqw var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.btn{display:block;text-align:center;background:var(--ink);color:var(--paper)!important;text-decoration:none;font:600 4.4cqw var(--hf);padding:4cqw}
.chat{display:flex;flex-direction:column;gap:1.6cqw;border:1.5px solid var(--ink);border-radius:5cqw;padding:3cqw;background:#fff;font:500 3.2cqw var(--bf);position:relative;z-index:1}
.chat div{padding:1.6cqw 2.6cqw;border-radius:3cqw;max-width:85%}
.chat .u{align-self:flex-end;background:var(--ink);color:var(--paper)}
.chat .a{background:#ffd23f;border:1px solid var(--ink)}
.chat .rc{align-self:center;font:600 2.3cqw var(--mono);letter-spacing:.12em;text-transform:uppercase;border:1px solid var(--ink);border-radius:0;background:#7ee0a1}
.cover .pin{gap:2.4cqw}
.mh{font:700 15cqw/.84 var(--hf);letter-spacing:-.06em;text-transform:uppercase;white-space:nowrap}
.mh em{font-style:normal;text-transform:none}.mh .beer{height:.8em;width:auto;vertical-align:-.04em}
.dl{display:flex;justify-content:space-between;font:500 2.5cqw var(--mono);letter-spacing:.12em;text-transform:uppercase;border-block:1.5px solid var(--ink);padding:1.6cqw 0}
.hl{font:700 10.5cqw/.94 var(--hf);letter-spacing:-.045em;position:relative;z-index:1}
.cover .chat{width:62%;align-self:flex-end}
.cl{list-style:none;padding:0;margin:auto 0 0;font:600 4.2cqw var(--hf);position:relative;z-index:1;width:60%}
.cl li{border-top:1px solid var(--ink);padding:1.4cqw 0}
.blob{position:absolute;border-radius:50%;z-index:0}.b1{width:55%;aspect-ratio:1;background:#ffd23f;right:-14%;bottom:-12%}.b2{width:24%;aspect-ratio:1;background:#ff6b57;right:-8%;top:40%}
.back .pin{background:var(--ink);color:var(--paper)}.back .pin a,.back .k,.back h2{color:var(--paper)}.back .k::after{border-color:var(--paper)}
.back .cd{color:var(--paper);display:grid;grid-template-columns:42% 1fr;gap:3cqw;align-items:center}.back .cd span{color:#bbb}
.foot2{margin-top:auto!important;font:400 2.2cqw var(--mono);letter-spacing:.1em;text-transform:uppercase;color:#bbb}
'''

JS = r'''<script src="https://cdn.jsdelivr.net/npm/page-flip@2.0.7/dist/js/page-flip.browser.js"></script>
<script>
(function(){var el=document.getElementById('book');
if(!window.St||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
var stage=document.querySelector('.stage');stage.classList.add('on');el.classList.add('on');
var pages=el.querySelectorAll('.page'),cnt=document.querySelector('.cnt');
var vh=innerHeight-48-90,vw=innerWidth-32,two=vw>=760;
var h=Math.max(360,Math.min(vh,760)),w=Math.round(h*5/7);
if(!two&&w>vw){w=vw;h=Math.round(w*7/5)}if(two&&w*2>vw){w=Math.floor(vw/2);h=Math.round(w*7/5)}
var pf=new St.PageFlip(el,{width:w,height:h,size:'fixed',showCover:true,usePortrait:!two,mobileScrollSupport:false,flippingTime:650,drawShadow:true,maxShadowOpacity:.4});
pf.loadFromHTML(pages);
var m=/^#p(\d+)$/.exec(location.hash);if(m)pf.turnToPage(Math.min(pages.length-1,m[1]-1));
function ui(){cnt.textContent='Page '+(pf.getCurrentPageIndex()+1)+' / '+pages.length}
pf.on('flip',function(){ui();history.replaceState(null,'','#p'+(pf.getCurrentPageIndex()+1))});ui();
document.querySelector('.prev').onclick=function(){pf.flipPrev()};document.querySelector('.next').onclick=function(){pf.flipNext()};
addEventListener('keydown',function(e){if(e.key==='ArrowRight')pf.flipNext();if(e.key==='ArrowLeft')pf.flipPrev()});
var t;addEventListener('resize',function(){clearTimeout(t);t=setTimeout(function(){if(Math.abs(innerWidth-vw-32)>80)location.reload()},400)});
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

def build():
    back = ''.join(card(f'/hodl-my-b/{i["n"]}', i['og'], f'Issue {i["n"]} &middot; week of {i["week"]}', i['blurb']) for i in reversed(ISSUES))
    menu = ''.join(f'<li><a href="/hodl-my-b/{i["n"]}">Issue {i["n"]} &middot; {i["week"]}</a></li>' for i in reversed(ISSUES))
    for i in ISSUES:
        pages = globals()[f'pages_issue_{i["n"]}'](back)
        body = f'''  <body>
    <header class="tb"><a class="brand" href="/"><img src="/logo.svg" alt="" width="27" height="24" />bWalletX</a>
      <details><summary>Issue {i["n"]} &#9662;</summary><ul>{menu}<li><a href="/hodl-my-b">Latest</a></li></ul></details></header>
    <main class="stage"><div class="book" id="book">{''.join(pages)}</div>
      <div class="nav"><button class="prev" type="button">&larr; Prev</button><span class="cnt" aria-live="polite"></span><button class="next" type="button">Next &rarr;</button></div></main>
    {JS}
  </body>
</html>
'''
        title = f'Hodl my b, Issue {i["n"]}: {i["story"]}'
        desc = f'Hodl my b, the weekly bWalletX magazine. Issue {i["n"]}, week of {i["week"]}: {i["blurb"]}'
        alt = f'Magazine cover: Hodl my b, Weekly, Issue {i["n"]}. {i["story"]}'
        open(os.path.join(ROOT, f'hodl-my-b/{i["n"]}.html'), 'w').write(head(f'/hodl-my-b/{i["n"]}', title, desc, i['og'] + '?v=1', alt) + body)
        if i is ISSUES[-1]:
            open(os.path.join(ROOT, 'hodl-my-b.html'), 'w').write(head('/hodl-my-b', 'Hodl my b', 'Hodl my b: the weekly bWalletX magazine. Everything shipped each week, with what is live and what is coming.', 'og-hodl-my-b.png?v=1', 'A mug of beer beside the words Hodl my b.') + body)

build()
