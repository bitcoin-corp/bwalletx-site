#!/usr/bin/env python3
"""OG images for blog 035-038. Writes og-blog-0NN.html here; shot-035.cjs renders them to /og/og-blog-0NN.png."""
import os
D = os.path.dirname(os.path.abspath(__file__))
HEAD = '''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;background:#000;color:#fff;font-family:'Space Grotesk',-apple-system,Arial,sans-serif;position:relative;overflow:hidden}
.glow{position:absolute;right:-160px;top:-80px;width:820px;height:820px;background:radial-gradient(circle,#F5B80026,transparent 62%)}
.top{position:absolute;left:72px;top:58px;display:flex;align-items:center;gap:14px;font-weight:700;font-size:30px}.top img{width:44px}.g{color:#F5B800}
.k{position:absolute;left:72px;top:146px;color:#F5B800;font-weight:700;letter-spacing:.12em;font-size:21px}
h1{position:absolute;left:72px;top:184px;width:600px;font-size:66px;line-height:1.06;letter-spacing:-.02em;color:#F5B800}
.sub{position:absolute;left:72px;top:372px;width:590px;color:#e4e6ea;font-size:27px;line-height:1.35;font-weight:500}
.card{position:absolute;left:720px;top:90px;width:410px;background:#0d0e11;border:1px solid #F5B80055;border-radius:22px;padding:22px 24px;box-shadow:0 0 60px #F5B80026;transform:rotate(-1.5deg)}
.card h3{font-size:16px;color:#8a8f99;letter-spacing:.1em;margin-bottom:12px;font-weight:600}
.row{display:flex;justify-content:space-between;align-items:center;font-size:20px;font-weight:600;padding:10px 0;border-top:1px solid #ffffff12}.row:first-of-type{border-top:0}
.row span{color:#8a8f99;font-weight:500}
.tabs{display:flex;gap:8px;margin-bottom:14px}.tabs i{font-style:normal;flex:1;text-align:center;font-size:15px;padding:8px 0;border-radius:10px;background:#1b1d22;color:#c9ccd2;font-weight:600}
.tabs i.on{background:#F5B800;color:#000}
.yb{background:#F5B800;color:#000;border-radius:14px;padding:14px 16px;font-weight:700;font-size:20px;margin-top:12px}
.gb{background:#F5B800;color:#000;border-radius:12px;padding:12px;text-align:center;font-weight:700;font-size:19px;margin-top:14px}
.db{background:#1b1d22;color:#d5d9e0;border-radius:12px;padding:12px;text-align:center;font-weight:600;font-size:19px;margin-top:10px}
.bars{display:flex;gap:5px;align-items:flex-end;height:34px}.bars b{width:7px;background:#22c55e;border-radius:3px}
.bar{display:flex;justify-content:space-between;margin-top:14px;padding-top:12px;border-top:1px solid #ffffff12;font-size:15px;color:#8a8f99;font-weight:600}
.bar .on{color:#F5B800}
.live{display:inline-block;background:#ef4444;color:#fff;font-size:13px;font-weight:700;padding:3px 9px;border-radius:8px;letter-spacing:.06em}
.ex{position:absolute;right:22px;top:18px;font-size:13px;font-weight:700;letter-spacing:.12em;color:#8a8f99;border:1px solid #ffffff2a;border-radius:7px;padding:3px 8px}
.mono{font-family:Menlo,monospace;font-size:17px;color:#d5d9e0}
</style></head><body><div class="glow"></div>
<div class="top"><img src="logo.svg"><span>bWallet<span class="g">X</span></span></div>
'''
posts = {
 '035': ('Pots &amp;<br>Locks',
         'Locks grouped into pots. Back PNEEs with locked BSV. Nobody can break a lock early.',
         '<div class="card"><span class="ex">EXAMPLE</span><h3>POTS &amp; LOCKS</h3><div class="row">In pots<span class="g">1.20 BSV</span></div>'
         '<div class="row">PNEEs<span>0.50 BSV · locked</span></div><div class="row">Pension<span>0.40 BSV</span></div>'
         '<div class="row">Savings goal<span>0.30 BSV</span></div><div class="gb">Lock BSV</div><div class="db">+ Pot</div></div>'),
 '036': ('Subscriptions,<br>in dollars',
         'Priced in dollars, paid in BSV at the day&rsquo;s rate, from a pot you choose. Pause any time.',
         '<div class="card"><span class="ex">EXAMPLE</span><h3>SUBSCRIPTIONS</h3><div class="row">Bitcoin Writer Pro<span>$1.00 / month</span></div>'
         '<div class="row">bChatX Plus<span>$0.01 / day</span></div><div class="row">Pays from<span class="g">Subscriptions pot</span></div>'
         '<div class="row">About a month<span>$1.30</span></div><div class="db">Pause all</div></div>'),
 '037': ('Portfolio<br>vs market',
         'Your wallet against just holding BSV, holding BTC or keeping dollars.',
         '<div class="card"><span class="ex">EXAMPLE</span><h3>VS MARKET · 1M</h3><div class="tabs"><i>1D</i><i>1W</i><i class="on">1M</i><i>1Y</i><i>All</i></div>'
         '<div class="row">You<span class="g">+6.2%</span></div><div class="row">Hold BSV<span>+4.8%</span></div>'
         '<div class="row">Hold BTC<span>+3.1%</span></div><div class="row">Keep dollars<span>0.0%</span></div></div>'),
 '038': ('Swap into<br>BSV',
         'BTC, ETH and 1,000+ coins into BSV, sent straight to your own wallet.',
         '<div class="card"><h3>SWAP INTO BSV</h3><div class="row">You send<span>0.01 BTC</span></div>'
         '<div class="row">You get about<span class="g">BSV</span></div><div class="row">Paid to<span>this wallet</span></div>'
         '<div class="row">Run by<span>ChangeNOW</span></div><div class="gb">Get deposit address</div></div>'),
}
for n, (h, sub, card) in posts.items():
    with open(os.path.join(D, f'og-blog-{n}.html'), 'w') as f:
        f.write(HEAD + f'<div class="k">DEVELOPMENT BLOG · {n}</div>\n<h1>{h}</h1>\n<div class="sub">{sub}</div>\n{card}\n</body></html>')
