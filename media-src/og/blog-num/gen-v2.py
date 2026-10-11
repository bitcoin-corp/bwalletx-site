# House-style blog cards (the 027 template) for posts that were rendered in the wrong style.
# Run: python3 gen-v2.py && node shot-v2.cjs   (serve the site root on :8768 first)
import re
T=open('og-027.html').read().replace('http://localhost:8767','http://localhost:8768')
TOTAL=38
posts={
 '030':('bPhone: charge to receive calls','A price per second, minute, hour or call, paid wallet to wallet while you talk.','8 Oct 2026'),
 '032':('Meet bChatX.com','Chat has a new home. Sign in with bWalletX; your wallet stays bWalletX.','8 Oct 2026'),
 '033':('Spaces you can just listen to','See who is live and listen to public Spaces without signing in.','8 Oct 2026'),
 '034':('Open apps, open protocol','MIT-licensed apps, a public chat protocol, and a server that can’t spend your money.','8 Oct 2026'),
 '035':('Pots &amp; Locks, and backing PNEEs','Locks grouped into pots like Pension or Savings goal, plus a PNEEs pot.','10 Oct 2026'),
 '036':('Subscriptions, priced in dollars','Paid in BSV at the day’s rate, from a pot you choose. Pause any time.','10 Oct 2026'),
 '037':('Portfolio vs market','Your wallet against just holding BSV, holding BTC or keeping dollars.','10 Oct 2026'),
 '038':('Swap into BSV','BTC, ETH and 1,000+ coins into BSV, sent straight to your wallet.','10 Oct 2026'),
}
import sys
extra=sys.argv[1:]  # optional: n|title|sub|date|total for drafts
for a in extra:
    n,t,s,d,tot=a.split('|'); posts[n]=(t,s,d); TOTAL_D=int(tot)
for n,(t,s,d) in posts.items():
    tot=TOTAL if int(n)<=TOTAL else int(n)
    h=T
    h=re.sub(r'(<span class="n">)\d+(</span>)',r'\g<1>'+n+r'\2',h)
    h=re.sub(r'<h1>.*?</h1>','<h1>'+t+'</h1>',h,flags=re.S)
    h=re.sub(r'<p class="sub">.*?</p>','<p class="sub">'+s+'</p>',h,flags=re.S)
    h=re.sub(r'<div class="num"><b>\d+</b><small>.*?</small></div>','<div class="num"><b>'+n+'</b><small>'+d+'</small></div>',h)
    h=re.sub(r'post \d+ of \d+','post '+str(int(n))+' of '+str(tot),h)
    open('og-'+n+'-v2.html','w').write(h)
print('ok',len(posts))
