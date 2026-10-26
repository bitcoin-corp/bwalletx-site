#!/usr/bin/env python3
"""Build /llms.txt (llmstxt.org-style guide), /llms-full.txt (all page text as Markdown) and /sitemap.xml
from the site's HTML pages. Run before deploying: python3 scripts/gen-llms.py"""
import glob, html, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://bwalletx.com'
SKIP = {'404.html'}

def url_of(path):
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    if rel == 'index.html': return BASE + '/'
    if rel.endswith('/index.html'): return BASE + '/' + rel[:-10]
    return BASE + '/' + rel[:-5]

def meta(s, name):
    m = re.search(r'<meta\s+(?:name|property)="%s"\s+content="([^"]*)"' % re.escape(name), s)
    return html.unescape(m.group(1)) if m else ''

def to_md(s):
    m = re.search(r'<main[^>]*>(.*?)</main>', s, re.S)
    body = m.group(1) if m else s
    body = re.sub(r'<(script|style|svg|noscript|video)[^>]*>.*?</\1>', '', body, flags=re.S)
    body = re.sub(r'<h1[^>]*>(.*?)</h1>', lambda m: '\n# ' + m.group(1) + '\n', body, flags=re.S)
    body = re.sub(r'<h2[^>]*>(.*?)</h2>', lambda m: '\n## ' + m.group(1) + '\n', body, flags=re.S)
    body = re.sub(r'<h3[^>]*>(.*?)</h3>', lambda m: '\n### ' + m.group(1) + '\n', body, flags=re.S)
    body = re.sub(r'<li[^>]*>', '\n- ', body)
    body = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', lambda m: '[%s](%s)' % (re.sub('<[^>]+>', '', m.group(2)).strip(), m.group(1) if m.group(1).startswith('http') else BASE + m.group(1) if m.group(1).startswith('/') else m.group(1)), body, flags=re.S)
    body = re.sub(r'<(pre|code)[^>]*>', '`', body); body = re.sub(r'</(pre|code)>', '`', body)
    body = re.sub(r'</?(p|div|section|ul|ol|br|tr|table)[^>]*>', '\n', body)
    body = re.sub(r'<[^>]+>', '', body)
    body = html.unescape(body)
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in body.split('\n')]
    out, blank = [], False
    for l in lines:
        if not l:
            if not blank and out: out.append('')
            blank = True
        else:
            out.append(l); blank = False
    return '\n'.join(out).strip()

# Allowlist: only git-tracked public pages. Top-level *.html, blog/*.html, a few known sub-pages, and docs .md.
# Never media-src/, walkthrough-*/, tmp/, cut/, og/, node_modules/, *-template files (they are gitignored and
# .vercelignored, and git ls-files keeps untracked scratch out too).
import subprocess, fnmatch
SUBPAGES = {'b/acc.html', 'b/acc/store.html', 'apps/add.html', 'exchange/strategies.html', 'strategies/spec.html', 'lock/verify.html', 'bapps/bmovies.html', 'artists/vexvoid.html', 'testers/bwallet/iphone.html', 'testers/bwallet/android.html', 'testers/bwalletx/chrome-extension.html', 'testers/bwalletx/web.html', 'testers/bwalletx/desktop.html', 'hodl-my-b/0.html', 'hodl-my-b/1.html'}
DUPES = {'download.html', 'pnee.html'}  # canonical points to /get and /pnees
BAD_DIRS = {'media-src', 'tmp', 'node_modules', 'cut', 'og', 'scripts', 'download'}
tracked = subprocess.check_output(['git', 'ls-files'], cwd=ROOT).decode().split('\n')
def allowed(rel):
    parts = rel.split('/')
    if set(parts[:-1]) & BAD_DIRS or any(x.startswith('walkthrough-') for x in parts) or '-template' in rel or rel in DUPES or os.path.basename(rel) in SKIP: return False
    if rel.endswith('.html'):
        return '/' not in rel or fnmatch.fnmatch(rel, 'blog/*.html') or rel in SUBPAGES
    return False
pages = []
for rel in sorted(r for r in tracked if allowed(r)):
    p = os.path.join(ROOT, rel)
    s = open(p, encoding='utf-8').read()
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    pages.append(dict(url=url_of(p), rel=rel, title=html.unescape(t.group(1)).strip() if t else rel,
                      desc=meta(s, 'description') or meta(s, 'og:description'), md=to_md(s)))
DOCS = [r for r in tracked if r.endswith('.md') and '/' not in r and r not in ('README.md', 'CLAUDE.md', 'AGENTS.md')]

SECTIONS = {
    'Product': ['index', 'get', 'android', 'iphone', 'extension', 'features', 'video', 'testers', 'buy', 'restore', 'restore-simplycash', 'history', 'push-notifications', 'web'],
    'Wallet features': ['exchange', 'exchange/strategies', 'mint', 'pnees', 'pots', 'subscriptions', 'lock', 'lock/verify', 'token-locking', 'launchpad', 'identity', 'identity-map', 'handles', 'bavatars', 'themes', 'swap', 'sign', 'games'],
    'Social': ['social', 'chat', 'bmail', 'friends', 'lounge', 'live', 'airdrops', 'gmail', 'x'],
    'Agents & developers': ['agent', 'hold-to-talk', 'agents', 'strategies', 'strategies/spec', 'developers', 'connect', 'sign-in-button', 'cli', 'mcp', 'apps/add', 'open-source'],
    'Support': ['privacy'],
}
def group(r):
    if r.startswith('blog/'): return 'Blog'
    k = r[:-5]
    for g, ks in SECTIONS.items():
        if k in ks: return g
    return 'Product'

order = ['Product', 'Wallet features', 'Social', 'Agents & developers', 'Blog', 'Support']
def one_line(d):
    d = re.sub(r'\s+', ' ', d).strip()
    return d
lines = ['# bWalletX', '',
         '> bWalletX is the full edition of the wallet (web app, Chrome extension, Android sideload APK and a private iPhone build, with the iPhone web app from Safari for everyone else); '
         'bWallet is the App Store / Google Play edition with fewer features. Both are non-custodial Bitcoin SV (BSV) wallets from '
         'The Bitcoin Corporation Ltd, forked from the open-source Yours Wallet (MIT). bwallet.space is the older bWallet store-edition site '
         '(it still hosts the testing waitlist); bwalletx.com is the main site. Beta software: test with small amounts.', '',
         'bWalletX includes an Exchange for tokens and NFTs, token-gated chat rooms, a bApps store, an on-chain media player, '
         'b (a built-in AI assistant), agent accounts with strategies, and PNEEs (Penny Stablecoins, a BSV-backed dollar token in a capped mainnet pilot).', '',
         'Full text of every page below: %s/llms-full.txt' % BASE, '']
for g in order:
    items = [p for p in pages if group(p['rel']) == g]
    ks = SECTIONS.get(g, [])
    items.sort(key=lambda p: (ks.index(p['rel'][:-5]) if p['rel'][:-5] in ks else 999, p['rel']))
    if not items: continue
    lines += ['## ' + g, '']
    for p in items:
        lines.append('- [%s](%s)%s' % (p['title'], p['url'], (': ' + one_line(p['desc'])) if p['desc'] else ''))
    if g == 'Agents & developers':
        for d in DOCS:
            lines.append('- [%s (Markdown)](%s/%s): Plain Markdown for AI coding agents.' % ('Sign in with bWalletX' if d == 'connect.md' else d, BASE, d))
    if g == 'Support':
        lines.append('- [Email support](mailto:support@bwalletx.com): support@bwalletx.com')
    lines.append('')
open(os.path.join(ROOT, 'llms.txt'), 'w').write('\n'.join(lines))

full = ['# bWalletX: full site text', '', 'Generated %s from %s. Source pages are linked above each section.' % (datetime.date.today().isoformat(), BASE), '']
for g in order:
    for p in [p for p in pages if group(p['rel']) == g]:
        full += ['---', '', 'Source: ' + p['url'], '', p['md'], '']
for d in DOCS:
    full += ['---', '', 'Source: %s/%s' % (BASE, d), '', open(os.path.join(ROOT, d), encoding='utf-8').read().strip(), '']
open(os.path.join(ROOT, 'llms-full.txt'), 'w').write('\n'.join(full))

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += ['  <url><loc>%s</loc></url>' % p['url'] for p in pages] + ['  <url><loc>%s/%s</loc></url>' % (BASE, d) for d in DOCS]
sm += ['</urlset>']
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
print(len(pages), 'pages ->', 'llms.txt', 'llms-full.txt', 'sitemap.xml')
