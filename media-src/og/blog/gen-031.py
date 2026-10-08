#!/usr/bin/env python3
"""OG images for blog 031-034. Writes og-blog-0NN.html here; shot-031.cjs renders them to /og/og-blog-0NN.png."""
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
.tabs i.on{background:#22c55e;color:#000}
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
 '031': ('5.1.88: Calls, mics,<br>a new menu',
         'A Calls tab with a keypad, microphones that work, and up to four accounts in one menu.',
         '<div class="card"><h3>CALLS</h3><div class="tabs"><i>Recents</i><i>Contacts</i><i>Services</i><i class="on">Keypad</i></div>'
         '<div class="row">In a Space<div class="bars"><b style="height:12px"></b><b style="height:26px"></b><b style="height:18px"></b><b style="height:32px"></b><b style="height:14px"></b></div></div>'
         '<div class="row">Accounts<span>4 inline</span></div><div class="row">Recent sign-ins<span>alerts on</span></div>'
         '<div class="yb">bPhone · charge to receive calls</div></div>'),
 '032': ('Meet<br>bChatX.com',
         'Chat&rsquo;s new home. Sign in with bWalletX. Your wallet is bWalletX, not a second one.',
         '<div class="card"><span class="ex">EXAMPLE</span><h3>WWW.BCHATX.COM</h3><div class="row">bChatX<span class="g">$you &#9679;</span></div>'
         '<div class="row">Show Twetch posts<span>on</span></div><div class="row">Images from other apps<span>blurred</span></div>'
         '<div class="row">Feed loads<span>~0.5 s</span></div><div class="gb">Sign in with bWalletX</div>'
         '<div class="bar"><span class="on">Feed</span><span>Rooms</span><span class="on">b</span><span>Spaces</span><span>DMs</span></div></div>'),
 '033': ('Spaces you can<br>just listen to',
         'Public Spaces on bChatX need no sign-in to listen. Sign in when you want to speak.',
         '<div class="card"><span class="ex">EXAMPLE</span><h3>SPACES</h3><div class="row"><span class="live">LIVE</span><span>8 speakers · 41 listening</span></div>'
         '<div class="row">Building on BSV<span>host $alice</span></div><div class="gb">Listen</div>'
         '<div class="db">Raise hand · sign in</div><div class="row" style="margin-top:8px">Stage<span>up to 12 speakers</span></div></div>'),
 '034': ('Open apps,<br>open protocol',
         'MIT-licensed apps, a public protocol, and a server that can&rsquo;t spend your money.',
         '<div class="card"><h3>WHAT IS OPEN</h3><div class="row">bWalletX<span class="g">MIT &#10003;</span></div>'
         '<div class="row">bChat desktop<span>to follow</span></div><div class="row">bChatX web app<span>to follow</span></div>'
         '<div class="row">bChat Protocol<span class="g">GitHub &#10003;</span></div><div class="row">Server<span>closed for now</span></div>'
         '<div class="row" style="margin-top:4px"><span class="mono">your keys stay in your wallet</span></div></div>'),
}
for n, (h, sub, card) in posts.items():
    with open(os.path.join(D, f'og-blog-{n}.html'), 'w') as f:
        f.write(HEAD + f'<div class="k">DEVELOPMENT BLOG · {n}</div>\n<h1>{h}</h1>\n<div class="sub">{sub}</div>\n{card}\n</body></html>')
