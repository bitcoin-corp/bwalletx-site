#!/usr/bin/env python3
"""Build data/kintsugi-offers.json: every Kintsugi contract and open offer in one machine-readable feed.

    python3 scripts/kintsugi-feed.py

Read by bChatX (/api/offers?market=kintsugi) for its two tabs:
  kind "fund"   = past work anyone can pay for (stamped contracts KS-2026-xxxx)
  kind "tender" = open offers a developer can take on (KS-OFFER-xxxx)
Reads only committed data (kintsugi-log.json, kintsugi-contracts/index.json, kintsugi-stamps.json,
kintsugi-payments.json if present). Never writes the stamped contract texts.
"""
import datetime, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, 'data', *p)
SITE = 'https://bwalletx.com'
CLIENT_H, DEV_H = 25, 20               # same rates as scripts/kintsugi-log.py
OPEN_H = {'page': 2, 'post': 1}        # same fixed estimates as scripts/kintsugi-log.py
CLIENT = 'The Bitcoin Corporation Ltd'
DEV_HANDLE = '$b0asex'
CLIENT_HANDLE = '$bCorp'   # owner 31 Oct: The Bitcoin Corporation Ltd = bCorp@bwalletx.com
CLIENT_PAYMAIL = 'bCorp@bwalletx.com'


def load(p, default):
    return json.load(open(p)) if os.path.exists(p) else default


def main():
    log = json.load(open(D('kintsugi-log.json')))
    index = json.load(open(D('kintsugi-contracts', 'index.json')))['contracts']
    stamps = {s['contract_id']: s['txid'] for s in load(D('kintsugi-stamps.json'), [])}
    paid = load(D('kintsugi-payments.json'), {})   # id -> [txid, ...]
    hours = {(it['url'], it['title']): it['time']['hours'] for it in log['items']}

    def row(id, kind, title, task, h, status, contract_url, text_url=None, page_url=None, developer=None, usd=None):
        price, dev, fee = usd or (h * CLIENT_H, h * DEV_H, h * (CLIENT_H - DEV_H))
        return dict(source='kintsugi', id=id, kind=kind, title=title, task=task, client=CLIENT, developer=developer,
                    estimate_h=round(h, 2), price_usd=round(price, 2), dev_usd=round(dev, 2),
                    fee_usd=round(fee, 2), status=status, contract_url=contract_url,
                    text_url=text_url, page_url=page_url, stamp_txid=stamps.get(id), paid_txids=paid.get(id, []))

    rows = []
    for c in index:
        # Hours and amounts come from the stamped text itself (the log has been re-gathered since stamping).
        m = re.search(r'Client pays \$([\d,]+) \(([\d.]+) h × \$\d+\): \$([\d,]+) to the developer .*? and \$([\d,]+) to Kintsugi',
                      open(os.path.join(ROOT, c['file']), encoding='utf-8').read())
        num = lambda s: float(s.replace(',', ''))
        h = num(m.group(2)) if m else hours.get((c['url'], c['title']), 0)
        usd = (num(m.group(1)), num(m.group(3)), num(m.group(4))) if m else None
        rows.append(row(c['id'], 'fund', c['title'], f'Delivered work: {c["title"]}', h,
                        'paid' if paid.get(c['id']) else 'delivered', f'{SITE}/kintsugi/work',
                        text_url=f'{SITE}/{c["file"]}', page_url=SITE + c['url'] if c['url'] else None,
                        developer=DEV_HANDLE, usd=usd))
    # Offers: first issue (withdrawn 31 Oct, except KS-OFFER-0001 = done) and the -v2 reissue at content-job prices.
    OPEN_USD = {'page': 1.00, 'post': 0.50}; OPEN_MIN = {'page': 15, 'post': 5}
    for e in json.load(open(D('kintsugi-offers', 'index.json')))['offers']:
        if e['kind'] == 'page':
            task = f'Write and publish a blog post for {e["title"]} (bwalletx.com{e["url"]})'
        else:
            task = f'Publish post "{e["title"]}" once its feature ships in a release build'
        v1 = not e['id'].endswith('-v2')
        h = OPEN_H[e['kind']] if v1 else OPEN_MIN[e['kind']] / 60
        x = h * CLIENT_H if v1 else OPEN_USD[e['kind']]
        r = row(e['id'], 'tender', e['title'], task, h, e.get('status', 'open'), f'{SITE}/kintsugi/work',
                text_url=f'{SITE}/{e["file"]}', page_url=SITE + e['url'] if e.get('url') else None,
                usd=(x, x * 0.8, x * 0.2) if v1 else (x, x, 0))   # reissue: developer paid in full, no Kintsugi fee
        r.update(client_handle=CLIENT_HANDLE, client_paymail=CLIENT_PAYMAIL, signers=['client', 'developer'],
                 replaces=e.get('replaces'), replaced_by=e.get('replaced_by'))
        rows.append(r)

    out = dict(source='kintsugi', updated_at=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
               rates=dict(client_usd_h=CLIENT_H, dev_usd_h=DEV_H, paid_in='BSV at the BSV/USD rate on payment day'),
               statuses=dict(delivered='work done, not paid', paid='a payment is recorded against the stamp',
                             open='open for tender', withdrawn='replaced by a reissued offer (see replaced_by)', done='delivered'),
               offers=rows)
    json.dump(out, open(D('kintsugi-offers.json'), 'w'), indent=1, ensure_ascii=False)
    f = sum(r['kind'] == 'fund' for r in rows)
    print(f'{len(rows)} rows: {f} fund, {len(rows) - f} tender, {sum(bool(r["stamp_txid"]) for r in rows)} stamped')


if __name__ == '__main__':
    main()
