#!/usr/bin/env python3
"""Idempotent <head> pass for every public page: canonical link, meta description and og:image backstops,
and JSON-LD structured data between <!-- ld:start --> / <!-- ld:end --> markers.
Run before gen-llms.py:  python3 scripts/seo-head.py && python3 scripts/gen-llms.py"""
import glob, html, json, os, re, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://bwalletx.com'
MONTHS = {m: i + 1 for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}

ORG = {
    '@type': 'Organization', '@id': BASE + '/#org', 'name': 'The Bitcoin Corporation Ltd',
    'url': BASE + '/', 'logo': BASE + '/icon-512.png', 'email': 'support@bwalletx.com',
    'sameAs': ['https://x.com/bWalletX', 'https://www.youtube.com/@bWalletX', 'https://github.com/b0ase/yours-mobile'],
}
APP = {
    '@type': 'SoftwareApplication', '@id': BASE + '/#app', 'name': 'bWalletX',
    'description': 'Non-custodial Bitcoin SV wallet for tokens, media and apps: an Exchange for tokens and NFTs, token-gated chat, '
                   'a bApps store, an on-chain media player and b, a built-in AI assistant. bWalletX is the full edition; '
                   'bWallet is the App Store / Google Play edition with fewer features.',
    'operatingSystem': 'Android, iOS, ChromeOS, Web', 'applicationCategory': 'FinanceApplication',
    'url': BASE + '/', 'downloadUrl': BASE + '/get', 'installUrl': BASE + '/get', 'image': BASE + '/og-home-v3.png',
    'softwareVersion': None, 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'},
    'publisher': {'@id': BASE + '/#org'},
}
SITE = {'@type': 'WebSite', '@id': BASE + '/#site', 'name': 'bWalletX', 'url': BASE + '/', 'publisher': {'@id': BASE + '/#org'}}


def url_of(rel):
    if rel == 'index.html': return BASE + '/'
    if rel.endswith('/index.html'): return BASE + '/' + rel[:-10]
    return BASE + '/' + rel[:-5]


def meta(s, name):
    m = re.search(r'<meta\s+(?:name|property)="%s"\s+content="([^"]*)"' % re.escape(name), s)
    return html.unescape(m.group(1)) if m else ''


def text(x):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip()


def blog_date(s):
    m = re.search(r'class="meta">(.*?)</p>', s, re.S)
    m = m and re.search(r'·\s*\d{3}\s*·\s*([^·]*)', text(m.group(1)))
    if not m: return None
    t = m.group(1)
    # "29–30 Sep 2026", "30 Sep – 4 Oct 2026", "7 Oct 2026": published = first date, modified = last.
    year = int(re.search(r'\d{4}', t).group(0)); t = t.replace(str(year), '')
    days = [int(x) for x in re.findall(r'\b\d{1,2}\b', t)]
    months = re.findall(r'[A-Z][a-z]{2}', t)
    first = datetime.date(year, MONTHS[months[0]], days[0]).isoformat()
    last = datetime.date(year, MONTHS[months[-1]], days[-1]).isoformat()
    return first, last


def ld_for(rel, s):
    url = url_of(rel)
    graph = []
    if rel == 'index.html':
        graph += [ORG, SITE, APP]
    elif rel.startswith('blog/') and rel != 'blog/index.html':
        h = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
        post = {'@type': 'BlogPosting', 'headline': text(h.group(1)) if h else meta(s, 'og:title'),
                'description': meta(s, 'description'), 'url': url, 'mainEntityOfPage': url,
                'image': meta(s, 'og:image'), 'inLanguage': 'en',
                'author': {'@type': 'Organization', 'name': 'The Bitcoin Corporation Ltd', 'url': BASE + '/'},
                'publisher': {'@type': 'Organization', 'name': 'The Bitcoin Corporation Ltd',
                              'logo': {'@type': 'ImageObject', 'url': BASE + '/icon-512.png'}}}
        d = blog_date(s)
        if d:
            post['datePublished'] = d[0]
            if d[1] != d[0]: post['dateModified'] = d[1]
        graph.append(post)
    if rel == 'mint.html':  # the only page with a real Q&A section
        sec = s.split('<h2>Questions</h2>', 1)[1].split('<div class="row">', 1)[0]
        qa = re.findall(r'<h3>(.*?)</h3><p>(.*?)</p>', sec, re.S)
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': text(q), 'acceptedAnswer': {'@type': 'Answer', 'text': text(a)}} for q, a in qa]})
    if not graph: return None
    for g in graph:
        for k in [k for k, v in g.items() if v is None]: del g[k]
    return {'@context': 'https://schema.org', '@graph': graph}


tracked = subprocess.check_output(['git', 'ls-files', '*.html'], cwd=ROOT).decode().split()
changed = 0
for rel in tracked:
    if rel.split('/')[0] in ('media-src', 'download', 'scripts', 'og') or rel == '404.html': continue
    p = os.path.join(ROOT, rel)
    s0 = s = open(p, encoding='utf-8').read()
    if '</head>' not in s: continue
    canon = {'download.html': BASE + '/get', 'pnee.html': BASE + '/pnees'}.get(rel, url_of(rel))
    if 'rel="canonical"' not in s:
        s = re.sub(r'(<title>.*?</title>)', lambda m: m.group(1) + '\n    <link rel="canonical" href="%s" />' % canon, s, count=1, flags=re.S)
    if 'name="description"' not in s:
        d = {'privacy.html': 'Privacy policy for bWalletX (beta): what bWalletX and The Bitcoin Corporation Ltd collect, why, and how to contact us.'}.get(rel, meta(s, 'og:description'))
        s = s.replace('<link rel="canonical"', '<meta name="description" content="%s" />\n    <link rel="canonical"' % html.escape(d), 1)
    if 'property="og:image"' not in s:
        s = s.replace('<link rel="canonical"', '<meta property="og:image" content="%s/og-home-v3.png" />\n    <link rel="canonical"' % BASE, 1)
    s = re.sub(r'\n?\s*<!-- ld:start -->.*?<!-- ld:end -->', '', s, flags=re.S)
    ld = ld_for(rel, s)
    if ld:
        block = '    <!-- ld:start -->\n    <script type="application/ld+json">\n%s\n    </script>\n    <!-- ld:end -->\n' % \
                json.dumps(ld, ensure_ascii=False, indent=1).replace('</', '<\\/')
        s = s.replace('</head>', block + '  </head>', 1)
    if s != s0:
        open(p, 'w', encoding='utf-8').write(s); changed += 1
print(changed, 'pages updated')
