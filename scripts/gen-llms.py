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

pages = []
for p in sorted(glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)):
    rel = os.path.relpath(p, ROOT)
    if os.path.basename(p) in SKIP or rel.startswith(('download', 'node_modules', 'scripts', '.')): continue
    s = open(p, encoding='utf-8').read()
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    pages.append(dict(url=url_of(p), rel=rel, title=html.unescape(t.group(1)).strip() if t else rel,
                      desc=meta(s, 'description') or meta(s, 'og:description'), md=to_md(s)))

def group(r):
    if r.startswith('blog/'): return 'Development blog'
    if r in ('privacy.html',): return 'Legal'
    if r.split('/')[0].replace('.html', '') in ('developers', 'connect', 'cli', 'mcp', 'apps', 'strategies', 'agent', 'agents'): return 'Developers and agents'
    return 'Product'

order = ['Product', 'Developers and agents', 'Development blog', 'Legal']
lines = ['# bWalletX', '',
         '> bWalletX is a non-custodial BSV wallet from The Bitcoin Corporation Ltd, forked from the open-source Yours Wallet (MIT). '
         'It runs as an Android app, an iPhone web app, a Chrome/Brave extension and a web app, with an Exchange, token-gated chat rooms, '
         'AI agent accounts with strategies, and PNEEs (Penny Stablecoins, a BSV-backed dollar token in a capped mainnet pilot). '
         'The store edition is called bWallet (bwallet.space). Beta software: test with small amounts.', '',
         'Full text of every page: %s/llms-full.txt' % BASE, '']
for g in order:
    items = [p for p in pages if group(p['rel']) == g]
    if not items: continue
    lines += ['## ' + g, '']
    for p in items:
        lines.append('- [%s](%s)%s' % (p['title'], p['url'], (': ' + p['desc']) if p['desc'] else ''))
    lines.append('')
lines.insert(lines.index('## Developers and agents') + 2, '- [Sign in with bWalletX (Markdown)](%s/connect.md): The sign-in guide as plain Markdown, for AI coding agents.' % BASE)
open(os.path.join(ROOT, 'llms.txt'), 'w').write('\n'.join(lines))

full = ['# bWalletX: full site text', '', 'Generated %s from %s. Source pages are linked above each section.' % (datetime.date.today().isoformat(), BASE), '']
for g in order:
    for p in [p for p in pages if group(p['rel']) == g]:
        full += ['---', '', 'Source: ' + p['url'], '', p['md'], '']
open(os.path.join(ROOT, 'llms-full.txt'), 'w').write('\n'.join(full))

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += ['  <url><loc>%s</loc></url>' % p['url'] for p in pages if p['rel'] != 'privacy.html'] + ['  <url><loc>%s/privacy</loc></url>' % BASE, '  <url><loc>%s/connect.md</loc></url>' % BASE]
sm += ['</urlset>']
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
print(len(pages), 'pages ->', 'llms.txt', 'llms-full.txt', 'sitemap.xml')
