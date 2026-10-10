#!/usr/bin/env python3
"""Snapshot of the coins you can swap FROM into BSV, for /swap. The bitcoinchat.online swaps API sends no CORS
headers for bwalletx.com, so the page reads this static file instead. Popular list + notice come from
bitcoinchat.online/api/bitsign/swaps/currencies; the full list from ChangeNOW's public currencies API.
Run:  python3 scripts/gen-swap-coins.py"""
import json, os, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'bwalletx-site'}), timeout=30))

ours = get('https://www.bitcoinchat.online/api/bitsign/swaps/currencies')
full = get('https://api.changenow.io/v2/exchange/currencies?active=true&flow=standard')
pop = [(p['ticker'], p['network']) for p in ours['popular']]
labels = {(p['ticker'], p['network']): p['label'] for p in ours['popular']}
coins, seen = [], set()
for c in full:
    if c.get('isFiat') or not c.get('sell', True) or c['ticker'] == 'bsv':
        continue
    k = (c.get('legacyTicker') and c['ticker'], c.get('network') or c['ticker'])
    key = (c['ticker'], k[1])
    if key in seen: continue
    seen.add(key)
    coins.append({'t': c['ticker'].upper(), 'n': c['name'], 'net': key[1].upper(), 'img': c.get('image') or '',
                  'p': pop.index(key) if key in pop else (900 if c.get('featured') else 999)})
coins.sort(key=lambda c: (c['p'], c['t']))
for c in coins:
    c['p'] = c['p'] < 900
out = {'source': 'ChangeNOW', 'count': len(coins), 'notice': ours['notice'], 'coins': coins}
json.dump(out, open(os.path.join(ROOT, 'swap-coins.json'), 'w'), separators=(',', ':'))
print(len(coins), 'coins,', sum(c['p'] for c in coins), 'popular')
