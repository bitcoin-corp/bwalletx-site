#!/usr/bin/env python3
"""Kintsugi work log: build /kintsugi/work (a public log of the last month's work) from git history and the site itself.

    python3 scripts/kintsugi-log.py            # gather data -> data/kintsugi-log.json, render kintsugi/work.html
    python3 scripts/kintsugi-log.py --render   # re-render kintsugi/work.html from the committed data/kintsugi-log.json

Then run seo-head.py and gen-llms.py as usual.

Sources (approximate by design, the method is printed on the page):
  * pages and posts: the HTML in this repo (only URLs listed in sitemap.xml, minus a deny list)
  * commits: this repo plus sibling app repos (see REPOS); commit messages are never read or published
  * PRs: `gh pr list --state merged` per repo (counts and open->merge times only, no titles)
  * on X: data/kintsugi-log-x-posted.json (URLs already posted to X)

Default deny: anything about shares, investors, registers, treasury, cap tables or the board is dropped,
both as pages and as commits (a commit touching any such path is ignored entirely).
"""
import datetime, glob, html, json, os, re, statistics, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.dirname(ROOT)
DATA = os.path.join(ROOT, 'data', 'kintsugi-log.json')
XPOSTED = os.path.join(ROOT, 'data', 'kintsugi-log-x-posted.json')
START = '2026-10-03'   # the project began 3 Oct 2026; the log covers START to today
DEV = 'b0ase'          # all current work is credited to this developer (with Claude)
GAP_H = 2.0          # a gap longer than this starts a new session
PAD_H = 0.5          # each session gets this added (work before the first commit)
DAY_H = 7.5
CAP_H_DAY = 18  # owner 30 Oct: the founder's own log counts at most 18 hours a day since the start
USD_H = 20   # Kintsugi rate: $20 per hour, paid in BSV at the BSV/USD rate on payment day
PRICE = {}   # filled once per build: {'usd': float, 'date': 'D Mon YYYY'}

# (label shown publicly, local directory under PROJ, ref). The site repo is ROOT itself.
REPOS = [
    ('bwalletx.com site', None, 'origin/main'),
    ('bWalletX app', 'bwalletX', 'origin/bwallet'),
    ('bChatX', 'bit-sign', 'origin/main'),
    ('bMailX site', 'bmailx-site', 'origin/main'),
    ('bMarketX site', 'bMarketX', 'origin/main'),
    ('bGitX site', 'bgitx-site', 'origin/main'),
]
DENY = re.compile(r'bshares|partnership-shares|share-?register|register-of|investor|treasury|cap-?table|placement|'
                  r'board-|/board|shareholder|dividend|bcorp-bsv|bcorp-placement|kyc|\.env', re.I)
EXCL = {'404.html', 'bugs.html', 'feedback.html', 'ideas.html', 'kintsugi/work.html'}
EXCL_PFX = ('kintsugi/', 'blog/', 'og/', 'media-src/', 'testers/', 'themes/custom/', 'hodl-my-b/0/pdf', 'docs/')

TOP = [  # (topic, keywords in slug/title) - first match wins
    ('Start here, brand and campaigns', ['index.html', 'b-family', 'just-b', 'b-cool', 'b-is', 'be-on-b', 'happy-b', 'b-in-black', 'brand', 'flick-off', 'newsletter', 'b-socials', 'b-creative', 'b-on-twetch']),
    ('Safety and control', ['b-aware', 'privacy', 'terms', 'seedless', 'sign.html', 'verify', 'bounties', 'name-bindings', 'security']),
    ('Calls (bPhone)', ['bphone', 'sms', 'push-notif', 'hold-to-talk']),
    ('Your wallet and money', ['restore', 'hodl', 'sweep', 'relayx', 'pots', 'lock', 'pnee', 'swap', 'subscriptions', 'buy', 'digital-ice', 'btrust', 'direct', 'recover']),
    ('Exchange, tokens and launches', ['exchange', 'launchpad', 'token', 'airdrop', 'tokenblaster', 'strateg', 'b-market', 'bpositive']),
    ('Store, creators and media', ['store', 'artist', 'nft', 'gig', 'tips', 'aivj', 'video', 'themes', 'mint', 'creative', 'streaming', 'auteurs', 'shopkeepers', 'b/acc', 'credits', 'wallet-frames', 'culture', 'bad']),
    ('Agents and b', ['agent', 'ask-b', 'b-bots', 'mcp', 'cli', 'business-agents', 'services', 'jobs']),
    ('Rooms, chat and Spaces (bChatX)', ['bchatx', 'chat', 'spaces', 'lounge', 'friends', 'bradio', 'live', 'social', 'race-card', 'talk-to-b']),
    ('Your identity and names', ['handle', 'names', 'identity', 'person', 'sign-in', 'invite', 'x.html', 'gmail', 'migrate', 'history', 'name', 'bavatar', 'your-character', 'connect']),
    ('Mail, meetings and signing', ['bmail', 'contracts', 'sign']),
    ('bApps, games and the open platform', ['bapps', 'apps', 'games', 'open-source', 'developers', 'extension', 'desktop', 'web', 'download', 'android', 'iphone', 'get', 'partners', 'clients', 'on-b', 'bweb', 'bgitx', 'roadmap', 'releases', 'features']),
]
PLATFORM = 'Platform and shared code'
# Extra path keywords for app-repo commits, by page URL. Default: the slug's own words.
KW = {
    '/bphone': ['phone', 'calls', 'call'], '/sms': ['sms'], '/push-notifications': ['push'], '/hold-to-talk': ['ptt', 'talk'],
    '/bmail': ['bmail', 'mail'], '/pots': ['pots', 'pot'], '/lock': ['lock', 'locks'], '/swap': ['swap'],
    '/exchange': ['exchange', 'market'], '/names': ['names', 'opns'], '/handles': ['handle', 'handles', 'paymail'],
    '/bchatx': ['bchatx', 'chat', 'room'], '/bspaces': ['spaces', 'space', 'livekit'], '/lounge': ['lounge'],
    '/agent': ['agent'], '/agents': ['agents'], '/ask-b': ['askb', 'ask-b'], '/b-bots': ['bbots', 'bots'],
    '/themes': ['theme', 'themes'], '/airdrops': ['airdrop', 'airdrops'], '/mint': ['mint'], '/bradio': ['radio'],
    '/subscriptions': ['subscription', 'subscriptions'], '/pnees': ['pnee'], '/restore': ['restore', 'sweep', 'import'],
    '/bavatars': ['bavatar', 'avatar'], '/store': ['store'], '/tips': ['tip', 'tips'], '/video': ['video', 'player'],
    '/social': ['feed', 'social'], '/friends': ['friends', 'contacts'], '/invite': ['invite', 'invites'],
    '/seedless-login': ['passkey'], '/extension': ['extension', 'chrome'], '/desktop': ['desktop', 'wide'],
    '/games': ['games', 'game'], '/bapps': ['bapps', 'apps'], '/launchpad': ['launchpad'], '/tokenblaster': ['tokenblaster'],
    '/token-curves': ['curve'], '/btrust': ['btrust', 'trust'], '/history': ['history'], '/identity': ['identity'],
    '/sign': ['sign', 'signing'], '/contracts': ['contract', 'contracts'], '/mcp': ['mcp'], '/cli': ['cli'],
    '/connect': ['connect', 'brc100'], '/buy': ['ramp', 'onramp'], '/nfts': ['nft', 'nfts'], '/artists': ['artist', 'artists'],
    '/aivj': ['aivj'], '/live': ['live'], '/streaming-payments': ['stream', 'streaming'], '/credits': ['credits'],
    '/jobs': ['jobs'], '/bounties': ['bounty', 'bounties'], '/b-aware': ['aware'], '/verify-note': ['verify'],
    '/bweb': ['bweb'], '/wallet-frames': ['frames', 'frame'], '/services': [], '/features': [], '/get': [], '/download': [], '/web': [], '/bgitx': ['bgitx'], '/b-market': ['bmarket'],
}
REPO_ITEM = {'bMailX site': '/bmail', 'bMarketX site': '/b-market', 'bGitX site': '/bgitx'}
GENERIC = set('the and your with for you bwalletx from how new what all page pages coming home more wallet bwallet services src app mobile'.split())


def rd(p): return open(p, encoding='utf-8', errors='ignore').read()
def title(t):
    m = re.search(r'<title>(.*?)</title>', t, re.S | re.I)
    s = html.unescape(re.sub(r'\s+', ' ', m.group(1))).strip() if m else ''
    return re.sub(r'\s*[|·—–-]\s*bWalletX\s*$', '', s)
def isredir(t): return bool(re.search(r'http-equiv=["\']?refresh', t, re.I)) and len(re.sub(r'<[^>]+>', '', t).strip()) < 600
def topic(key, t):
    s = (key + ' ' + t).lower()
    for tp, kws in TOP:
        if any(k in s for k in kws): return tp
    return 'Other pages'
def nu(u):
    u = u.strip().lower(); u = re.sub(r'^https?://(www\.)?', '', u); u = u.split('?')[0].split('#')[0].rstrip('/')
    if u.endswith('.html'): u = u[:-5]
    if u.endswith('/index'): u = u[:-6]
    return u
def sh(cmd, cwd=None):
    try: return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600).stdout
    except Exception: return ''


def site_inventory():
    sitemap = {nu(u) for u in re.findall(r'<loc>([^<]+)</loc>', rd(os.path.join(ROOT, 'sitemap.xml')))}
    pages, posts = {}, {}
    for p in sorted(glob.glob(ROOT + '/**/*.html', recursive=True)):
        rel = os.path.relpath(p, ROOT)
        if rel in EXCL or rel.startswith(EXCL_PFX): continue
        t = rd(p)
        if isredir(t): continue
        url = '/' + ('' if rel == 'index.html' else rel[:-5].removesuffix('/index'))
        if nu('bwalletx.com' + url) not in sitemap or DENY.search(url + ' ' + title(t)): continue  # default deny
        pages[url] = dict(rel=rel, title=title(t), text=t, topic=topic(rel, title(t)))
    for p in sorted(glob.glob(ROOT + '/blog/[0-9][0-9][0-9]-*.html')):
        rel = os.path.relpath(p, ROOT); t = rd(p); url = '/' + rel[:-5]
        if isredir(t) or nu('bwalletx.com' + url) not in sitemap or DENY.search(url + ' ' + title(t)): continue
        posts[os.path.basename(p)[:3]] = dict(rel=rel, url=url, title=title(t), text=t)
    return pages, posts


def links(t):
    out = set()
    for h in re.findall(r'href=["\']([^"\'#?]+)', t):
        h = re.sub(r'^https?://(www\.)?bwalletx\.com', '', h)
        if h.startswith(('http', 'mailto')): continue
        h = h.lstrip('.').rstrip('/')
        if h.endswith('.html'): h = h[:-5]
        out.add(h if h.startswith('/') else '/' + h)
    return out


def match_posts(pages, posts):
    match = {u: set() for u in pages}
    for n, po in posts.items():
        pl = links(po['text'])
        for u, pg in pages.items():
            if u == '/': continue
            slug = u.strip('/').split('/')[-1]
            if (u in pl or po['url'] in links(pg['text']) or
                    (len(slug) >= 4 and re.search(r'\b' + re.escape(slug.replace('-', ' ')) + r'\b', (po['title'] + ' ' + po['rel'].replace('-', ' ')).lower()))):
                match[u].add(n)
    for u in pages:  # hub pages linked from every post via nav: keep only keyword/back-links
        if len(match[u]) > 20:
            slug = u.strip('/').split('/')[-1]
            match[u] = {n for n in match[u] if slug in posts[n]['rel'] or posts[n]['url'] in links(pages[u]['text'])}
    return match


def commits(path, ref, since):
    out, cur = [], None
    log = sh(['git', 'log', ref, '--no-merges', '--since=' + since, '--format=%x01%H%x09%aI', '--name-only'], cwd=path)
    for line in log.splitlines():
        if line.startswith('\x01'):
            h, ts = line[1:].split('\t'); cur = dict(h=h, ts=ts, files=[]); out.append(cur)
        elif line.strip() and cur: cur['files'].append(line.strip())
    return out


def pr_list(path, since):
    url = sh(['git', 'remote', 'get-url', 'origin'], cwd=path).strip()
    m = re.search(r'github\.com[:/]([^/]+/[^/.]+)', url)
    if not m: return []
    raw = sh(['gh', 'pr', 'list', '-R', m.group(1), '--state', 'merged', '--search', 'merged:>=' + since,
              '--limit', '1000', '--json', 'number,createdAt,mergedAt,files'])
    try: return json.loads(raw or '[]')
    except ValueError: return []


def kw_re(u):
    words = KW[u] if u in KW else [w for w in u.strip('/').split('/')[-1].split('-') if len(w) >= 4 and w not in GENERIC]
    return re.compile(r'(^|[/_.\-])(' + '|'.join(map(re.escape, words)) + r')([/_.\-]|s?\.|$)', re.I) if words else None


def gather():
    since = START
    pages, posts = site_inventory()
    match = match_posts(pages, posts)
    xp = {nu(k) for k in json.load(open(XPOSTED))} if os.path.exists(XPOSTED) else set()
    rels = {pg['rel']: u for u, pg in pages.items()}
    slug_of = {u: (u.strip('/').replace('/', '-') or 'home') for u in pages}
    post_pages = {}
    for u, ns in match.items():
        for n in ns: post_pages.setdefault(posts[n]['rel'], []).append(u)
    kws = {u: kw_re(u) for u in pages if u != '/'}
    items = {u: dict(ts=[], prs=[]) for u in pages}
    plat = {}

    def targets(label, files):
        hit = set()
        for f in files:
            if label == 'bwalletx.com site':
                if f in rels: hit.add(rels[f])
                elif f in post_pages: hit.update(post_pages[f])
                else:
                    m = re.match(r'(?:media-src/og/)?og-(.+?)(?:-v\d+)?\.(?:png|jpg|html)$', os.path.basename(f))
                    if m:
                        hit.update(u for u, s in slug_of.items() if s == m.group(1))
            else:
                if label in REPO_ITEM and REPO_ITEM[label] in items: hit.add(REPO_ITEM[label]); continue
                hit.update(u for u, r in kws.items() if r and r.search(f))
        return hit

    repo_stats = []
    for label, d, ref in REPOS:
        path = ROOT if d is None else os.path.join(PROJ, d)
        if not os.path.isdir(path): continue
        cs = [c for c in commits(path, ref, since) if not any(DENY.search(f) for f in c['files'])]
        n_att = 0
        for c in cs:
            hit = targets(label, c['files'])
            if hit:
                n_att += 1
                for u in hit: items[u]['ts'].append((c['ts'], 1 / len(hit)))
            elif label != 'bwalletx.com site':
                plat.setdefault(label, dict(ts=[], prs=[]))['ts'].append((c['ts'], 1.0))
        for pr in pr_list(path, since):
            files = [f['path'] for f in pr.get('files') or []]
            if any(DENY.search(f) for f in files): continue
            hit = targets(label, files) if files else set()
            dur = (datetime.datetime.fromisoformat(pr['mergedAt'].replace('Z', '+00:00')) -
                   datetime.datetime.fromisoformat(pr['createdAt'].replace('Z', '+00:00'))).total_seconds() / 3600
            for u in hit: items[u]['prs'].append(dur)
            if not hit and label != 'bwalletx.com site': plat.setdefault(label, dict(ts=[], prs=[]))['prs'].append(dur)
        repo_stats.append(dict(repo=label, commits=len(cs), attributed=n_att))

    def summarise(ts, prs):
        if not ts: return None
        pts = sorted((datetime.datetime.fromisoformat(t), w) for t, w in ts)
        sess, hours = [[pts[0]]], 0.0
        for p in pts[1:]:
            (sess[-1].append(p) if (p[0] - sess[-1][-1][0]).total_seconds() / 3600 <= GAP_H else sess.append([p]))
        for s in sess:
            hours += ((s[-1][0] - s[0][0]).total_seconds() / 3600 + PAD_H) * (sum(w for _, w in s) / len(s))
        return dict(hours=round(hours, 2), sessions=len(sess), commits=round(sum(w for _, w in pts), 1),
                    first=pts[0][0].date().isoformat(), last=pts[-1][0].date().isoformat(),
                    elapsed_days=(pts[-1][0] - pts[0][0]).days + 1,
                    prs=len(prs), pr_median_h=round(statistics.median(prs), 1) if prs else None)

    out_items, open_work = [], []
    for u, pg in pages.items():
        s = summarise(items[u]['ts'], items[u]['prs'])
        ps = sorted(match[u])
        it = dict(url=u, title=pg['title'] or u, topic=pg['topic'], live=True,
                  posts=[dict(n=n, url=posts[n]['url'], title=posts[n]['title']) for n in ps],
                  on_x=nu('bwalletx.com' + u) in xp or any(nu('bwalletx.com' + posts[n]['url']) in xp for n in ps), time=s)
        if s: out_items.append(it)
        if not ps and u != '/': open_work.append(dict(kind='page', url=u, title=it['title'], what='Page with no blog post yet'))
    for label, v in plat.items():
        s = summarise(v['ts'], v['prs'])
        if s: out_items.append(dict(url=None, title=label + ': shared code', topic=PLATFORM, live=True, posts=[], on_x=False, time=s))
    held = os.path.join(ROOT, 'data', 'kintsugi-log-held.json')
    for h in (json.load(open(held)) if os.path.exists(held) else []):
        open_work.append(dict(kind='post', url=None, title=h['title'], what='Blog post written, held back until the feature it describes is in a release build'))
    return dict(generated=datetime.datetime.now().strftime('%-d %b %Y'), since=since, days=(datetime.date.today() - datetime.date.fromisoformat(since)).days + 1, gap_h=GAP_H, pad_h=PAD_H,
                usd_h=USD_H, price=fetch_price(), repos=repo_stats, items=out_items, open=open_work)


E = html.escape


def money(h): return '${:,.0f}'.format(h * USD_H)
def bsv(h):
    v = h * USD_H / PRICE['usd']
    return '~{:,.2f} BSV'.format(v) if v < 10 else '~{:,.1f} BSV'.format(v) if v < 100 else '~{:,.0f} BSV'.format(v)


def fetch_price():
    raw = sh(['curl', '-s', '--max-time', '20', 'https://api.whatsonchain.com/v1/bsv/main/exchangerate'])
    return dict(usd=round(float(json.loads(raw)['rate']), 2), date=datetime.date.today().strftime('%-d %b %Y'))
def hrs(h): return ('{:.1f}'.format(h) if h < 10 else '{:,.0f}'.format(h)) + ' h'


CLIENT = 'The Bitcoin Corporation Ltd'
CLIENT_NO = '16735102'
PAYMAIL = 'b0asex@bwalletx.com'
GENERIC = 'Shared code behind several pages: components, fixes and plumbing used across {repo}.'
DESC_BAD = re.compile(r'coming soon|soon|invest', re.I)


def describe(it):
    """One plain sentence for an item, from its page's meta description (or og:description)."""
    if not it['url']:
        return GENERIC.format(repo=it['title'].split(':')[0])
    u = it['url'].strip('/') or 'index'
    for f in (u + '.html', u + '/index.html'):
        fp = os.path.join(ROOT, f)
        if os.path.exists(fp):
            t = rd(fp)
            m = (re.search(r'<meta\s+name="description"\s+content="([^"]*)"', t, re.I)
                 or re.search(r'<meta\s+property="og:description"\s+content="([^"]*)"', t, re.I))
            if m:
                txt = html.unescape(m.group(1)).strip()
                sents = [x for x in re.split(r'(?<=[.!?])\s+', txt) if x and not DENY.search(x) and not DESC_BAD.search(x)]
                out = ''
                for x in sents:
                    if len(out) >= 60 or len(out) + len(x) > 240: break
                    out = (out + ' ' + x).strip()
                if out: return out
            break
    return f'The {it["title"]} page on bwalletx.com.'


def fdate(s): return datetime.date.fromisoformat(s).strftime('%-d %b %Y')


FOUNDER = "This log is the founder's own work, counted at up to 18 hours a day. It comes from before the 8-hour daily cap that applies to Kintsugi developers."
OPEN_H = {'page': 2, 'post': 1}   # fixed estimates for open offers


def terms_html(founder=False, done='the change is live on the stated page'):
    t = f'''          <h3>Terms</h3>
          <ol class="ct-terms">
            <li>Payment is peer to peer: the client pays the developer directly, wallet to wallet. Kintsugi never holds the money.</li>
            <li>Up to 8 billable hours per day.</li>
            <li>Done means: the pull request is merged into the agreed repo, {done}, and the security tool results are attached.</li>
            <li>Security tools: Shannon for any change that touches sign-in, payments, keys or signing; Semgrep, gitleaks, pnpm audit and OSV-Scanner, CodeQL, OWASP ZAP (baseline scan) and Claude Code /security-review. Tool and AI usage costs are the developer's and are not billable hours.</li>
            <li>Kintsugi checks the spec and reviews the work. When the work is accepted, the client pays the developer's $handle in bWalletX, with Kintsugi's fee as a separate payment in the same transaction.</li>
            <li>Disputes: if the client and developer disagree about whether the work is done, Kintsugi reviews it and decides.</li>
            <li>Delivered work belongs to the client once it is paid for.</li>
            <li>Code under the Open BSV licence; specs and docs CC BY 4.0.</li>
            <li>All three parties sign the same contract in bChatX before work starts.</li>
'''
    if founder: t += f'            <li>{FOUNDER}</li>\n'
    return t + '          </ol>'


def offer(o, n):
    h = OPEN_H[o['kind']]
    if o['kind'] == 'page':
        task = f'Write and publish a blog post for <a href="{E(o["url"])}">{E(o["title"])}</a> <span class="u">bwalletx.com{E(o["url"])}</span>'
        dep = 'None'; done = 'the post is live on bwalletx.com/blog and linked from the page'
    else:
        task = f'Publish post “{E(o["title"])}” once its feature ships in a release build'
        dep = 'The feature the post describes must be in a release build first. The post is already written.'
        done = 'the post is live on bwalletx.com/blog after the feature is in a release build'
    sig = ''.join(f'<div class="sig"><span>{r}</span><i>Example — not signed</i></div>' for r in ('Client', 'Developer', 'Kintsugi'))
    return f'''<div class="ct" role="region" aria-label="Open offer {n}">
          <p class="ct-note"><strong>Open offer</strong>: example of how this job will be offered. Not open for acceptance yet. <a href="/kintsugi/program#apply">Register interest</a> to be told when tasks open.</p>
          <dl class="ct-dl">
            <dt>Offer</dt><dd class="tn">{n}</dd>
            <dt>Client</dt><dd>{CLIENT}, company no. {CLIENT_NO}, registered in England &amp; Wales</dd>
            <dt>Developer</dt><dd>Open: first accepted developer</dd>
            <dt>Review</dt><dd>Kintsugi, run by {CLIENT}</dd>
            <dt>Task</dt><dd>{task}</dd>
            <dt>Depends on</dt><dd>{dep}</dd>
            <dt>Estimate</dt><dd class="tn">{h} h (fixed)</dd>
            <dt>Price</dt><dd class="tn"><span class="gold">{money(h)}</span> ({h} h × $20), paid in BSV at the BSV/USD rate on the day of payment · {bsv(h)} at ${PRICE["usd"]:,.2f}/BSV</dd>
            <dt>Status</dt><dd>Not open yet</dd>
          </dl>
          {terms_html(done=done)}
          <div class="sigs">{sig}</div>
        </div>'''


def contract(it, n):
    t = it['time']; h = t['hours']
    task = (f'<a href="{E(it["url"])}">{E(it["title"])}</a> <span class="u">bwalletx.com{E(it["url"])}</span>' if it['url'] else E(it['title']))
    sig = ''.join(f'<div class="sig"><span>{r}</span><i>Example — not signed</i></div>' for r in ('Client', 'Developer', 'Kintsugi'))
    return f'''<div class="ct" role="region" aria-label="Example contract {n}">
          <p class="ct-note"><strong>Example contract</strong> — shows what a Kintsugi contract for this job looks like. Not signed, not an invoice.</p>
          <dl class="ct-dl">
            <dt>Contract</dt><dd class="tn">{n}</dd>
            <dt>Client</dt><dd>{CLIENT}, company no. {CLIENT_NO}, registered in England &amp; Wales. Commissioned the work.</dd>
            <dt>Developer</dt><dd>{E(DEV)} · paymail <span class="pm">{PAYMAIL}</span> ($b0asex)</dd>
            <dt>Review</dt><dd>Kintsugi, run by {CLIENT}</dd>
            <dt>Task</dt><dd>{task}<span class="sub">{E(it["desc"])}</span></dd>
            <dt>Estimate</dt><dd class="tn">{hrs(h)} (wall-clock)</dd>
            <dt>Price</dt><dd class="tn"><span class="gold">{money(h)}</span> ({hrs(h)} × $20), paid in BSV at the BSV/USD rate on the day of payment · {bsv(h)} at ${PRICE["usd"]:,.2f}/BSV</dd>
            <dt>Estimated value of work</dt><dd class="tn"><span class="val">{money(t["value_hours"])}</span></dd>
            <dt>Started</dt><dd class="tn">{fdate(t["first"])}</dd>
            <dt>Delivered</dt><dd class="tn">{fdate(t["last"])}</dd>
          </dl>
          {terms_html(founder=True)}
          <div class="sigs">{sig}</div>
        </div>'''


def render(d):
    order = [t for t, _ in TOP] + ['Other pages', PLATFORM]
    groups = {}
    for it in d['items']: groups.setdefault(it['topic'], []).append(it)
    tot_h = sum(it['time']['hours'] for it in d['items'])
    tot_v = sum(it['time']['value_hours'] for it in d['items'])
    sections, toc = '', []
    num = {id(it): f'KS-2026-{k:04d}' for k, it in enumerate(sorted(d['items'], key=lambda x: (x['url'] or '~', x['title'])), 1)}
    for tp in [t for t in order if t in groups]:
        rows = ''
        g = sorted(groups[tp], key=lambda x: -x['time']['hours'])
        gh = sum(it['time']['hours'] for it in g)
        gv = sum(it['time']['value_hours'] for it in g)
        for it in g:
            t = it['time']
            it['desc'] = describe(it)
            name = (f'<span class="nm">{E(it["title"])}</span><span class="u">{E(it["url"])}</span>' if it['url']
                    else f'<span class="nm">{E(it["title"])}</span><span class="u">Commits not tied to one page</span>')
            chips = '<span class="chip live">Live</span>'
            if it['posts']: chips += f'<span class="chip post">{len(it["posts"])} post{"s" if len(it["posts"]) != 1 else ""}</span>'
            if it['on_x']: chips += '<span class="chip x">On X</span>'
            pl = ''.join(f'<a href="{E(p["url"])}" title="{E(p["title"])}">{E(p["n"])}</a>' for p in it['posts'][:8])
            pr = f'{t["prs"]} PR{"s" if t["prs"] != 1 else ""}, median {t["pr_median_h"]:g} h open to merge' if t['prs'] else 'No PRs matched'
            rows += (f'<details class="job"><summary><span class="it">{name}<span class="ds">{E(it["desc"])}</span><span class="chips">{chips}</span></span>'
                     f'<span class="n">{hrs(t["hours"])}<span class="sub">{t["sessions"]} session{"s" if t["sessions"] != 1 else ""} · '
                     f'{t["elapsed_days"]} day{"s" if t["elapsed_days"] != 1 else ""} elapsed</span><span class="sub">{pr}</span></span>'
                     f'<span class="n c">{money(t["hours"])}<span class="sub">{bsv(t["hours"])} pay</span><span class="sub val">{money(t["value_hours"])} estimated value of work</span></span>'
                     f'<span class="cv" aria-hidden="true"></span></summary>'
                     f'{f"<p class=pl>Posts: {pl}</p>" if pl else ""}{contract(it, num[id(it)])}</details>')
        sid = re.sub(r'[^a-z]+', '-', tp.lower()).strip('-')
        toc.append(f'<a href="#{sid}">{E(tp)}</a>')
        sections += (f'<section id="{sid}"><div class="sh"><h2>{E(tp)}</h2><p class="st"><span>{len(g)} item{"s" if len(g) != 1 else ""}</span>'
                     f'<span>{hrs(gh)}</span><span class="c">{money(gh)}</span><span>{bsv(gh)}</span> <span class="est val">{money(gv)} estimated value of work</span></p></div>'
                     f'<div class="jobs"><div class="jh" aria-hidden="true"><span>Item · tap to see an example contract</span><span class="n">Time taken</span><span class="n">At the Kintsugi rate</span><span></span></div>'
                     f'{rows}</div></section>')
    ow = ''
    for k, o in enumerate(d['open'], 1):
        h = OPEN_H[o['kind']]
        nm = f'Blog post for {E(o["title"])}' if o['kind'] == 'page' else f'Publish “{E(o["title"])}”'
        ow += (f'<details class="job"><summary><span class="it"><span class="nm">{nm}</span><span class="u">{E(o["url"] or "Held until its feature is in a release build")}</span>'
               f'<span class="ds">{E(o["what"])}.</span><span class="chips"><span class="chip x">Not open yet</span></span></span>'
               f'<span class="n">{h} h<span class="sub">fixed estimate</span></span><span class="n c">{money(h)}<span class="sub">{bsv(h)}</span></span>'
               f'<span class="cv" aria-hidden="true"></span></summary>{offer(o, f"KS-OFFER-{k:04d}")}</details>')
    oh = sum(OPEN_H[o['kind']] for o in d['open'])
    repos = ', '.join(f'{E(r["repo"])} ({r["commits"]:,} commits)' for r in d['repos'])
    body = f'''<main class="bb">
      <h1><b>Kintsugi</b> work log: a month of work, in the open</h1>
      <p class="lede">Every page and feature shipped since the project began, between {E(datetime.date.fromisoformat(d["since"]).strftime("%-d %b"))} and {E(d["generated"])}, with the time it took and what it would cost at the Kintsugi rate. Built from git history.</p>
      <div class="totals">
        <div class="tot"><b class="tn">{len(d["items"])}</b><span>items shipped</span></div>
        <div class="tot"><b class="tn">{tot_h:,.0f} h</b><span>wall-clock hours (estimate, at most {CAP_H_DAY} a day)</span></div>
        <div class="tot big"><b class="tn">{money(tot_h)}</b><span>pay at the Kintsugi rate ($20 per hour, paid in BSV), about {bsv(tot_h)[1:]} at ${PRICE["usd"]:,.2f}/BSV on {E(PRICE["date"])}</span></div>
        <div class="tot big val"><b class="tn">{money(tot_v)}</b><span>estimated value of work: {tot_v:,.0f} hours of work at $20, across parallel sessions. What a developer creates over and above the pay.</span></div>
      </div>
      <p class="how"><strong>How Kintsugi works.</strong> Work is written up as tasks that an AI-assisted coder can pick up with Cursor, GitHub and a Claude account. The rate is $20 per hour, paid in BSV at the BSV/USD rate on the day of payment.</p>
      <p class="how">Tap any job to see an example contract for it: the offer, the terms, who commissioned it ({CLIENT}) and the paymail of the developer who did it.</p>
      <p class="how">{FOUNDER}</p>
      <p class="warn">Every figure here is an estimate, derived from git timestamps. It is not an invoice, a valuation or a claim.</p>
      <nav class="toc" aria-label="Topics">{"".join(toc)}<a href="#open-work">Open work</a><a href="#method">Method</a></nav>
      {sections}
      <section id="open-work"><h2>Open work</h2><p>Pages that have no blog post yet, and posts held back until the feature they describe is in a release build. Each is shown as an open offer.</p><p class="st"><span>{len(d["open"])} open offers, about <b class="c">{money(oh)}</b> ({oh} h at $20, paid in BSV). Not open yet: <a href="/kintsugi/program#apply">register interest</a> to be told when tasks open.</span></p><div class="jobs" style="margin-top:12px"><div class="jh" aria-hidden="true"><span>Offer · tap to see how it will be offered</span><span class="n">Estimate</span><span class="n">Price</span><span></span></div>{ow}</div></section>
      <section id="method"><h2>How the numbers are made</h2>
        <ol class="method">
          <li><strong>Items.</strong> Every public page on bwalletx.com that is in the sitemap. Internal company matters are left out on purpose.</li>
          <li><strong>Commits.</strong> Every commit since the project began on {E(datetime.date.fromisoformat(d["since"]).strftime("%-d %b %Y"))}, from: {repos}. A site commit counts towards the pages and share images it touched. An app commit counts towards a page when a file path names that feature (for example a <code>pots</code> folder counts towards Pots). A commit that touches several items is split evenly between them. App commits that match no page go into "shared code". Commit messages are never published.</li>
          <li><strong>Time taken.</strong> Commits are grouped into sessions: a gap of more than {d["gap_h"]:g} hours starts a new one. Each session counts as last commit minus first commit, plus {d["pad_h"] * 60:.0f} minutes for the work before the first commit. Elapsed days and PR open-to-merge times are shown for context only.</li>
          <li><strong>Cost.</strong> Hours × the Kintsugi rate of $20 an hour, paid in BSV at the BSV/USD rate on the day of payment. BSV figures are approximate, converted at ${PRICE["usd"]:,.2f} per BSV, the price fetched once from WhatsOnChain on {E(PRICE["date"])}. This is what the same output would cost an AI-assisted coder on Kintsugi, not what it cost us.</li>
          <li><strong>Limits.</strong> Commit gaps miss design and thinking time, and quick AI-assisted bursts look short. Treat each figure as a rough range.</li>
        </ol>
        <p class="gen">Generated {E(d["generated"])} by <code>scripts/kintsugi-log.py</code>.</p>
      </section>
    </main>'''
    return body


CSS = '''<style>
      :root { --kw-green: #3ddc84; }
      .bb .val, .bb .tot.big.val b, .bb .sub.val, .bb .est.val { color: var(--kw-green); }
      .bb .jobs { border: 1px solid #ffffff14; border-radius: 14px; overflow: hidden; }
      .bb .jh, .bb .job > summary { display: grid; grid-template-columns: minmax(0, 1fr) 230px 240px 18px; gap: 16px; padding: 12px 16px; }
      .bb .jh { background: #0e0f12; color: #9aa1ad; font-weight: 600; font-size: 0.82rem; }
      .bb .job { border-top: 1px solid #ffffff12; }
      .bb .job > summary { list-style: none; cursor: pointer; font-size: 0.94rem; }
      .bb .job > summary::-webkit-details-marker { display: none; }
      .bb .job > summary:hover { background: #ffffff08; }
      .bb .job > summary:focus-visible { outline: 2px solid #F5B800; outline-offset: -2px; border-radius: 4px; }
      .bb .job .n.c { color: #F5B800; font-weight: 700; }
      .bb .job .sub.val { color: var(--kw-green); font-weight: 600; }
      .bb .ds { display: block; color: #c9ced8; font-size: 0.86rem; line-height: 1.5; margin: 4px 0 6px; }
      .bb .cv { width: 8px; height: 8px; margin-top: 6px; border-right: 2px solid #9aa1ad; border-bottom: 2px solid #9aa1ad; transform: rotate(45deg); }
      .bb .job[open] .cv { transform: rotate(225deg); margin-top: 10px; }
      .bb .job > .pl { padding: 0 16px; margin: 0 0 8px; }
      .bb .ct { margin: 0 16px 16px; padding: 18px 20px; background: #0e0f12; border: 1px solid #ffffff14; border-radius: 12px; }
      .bb .ct-note { margin: 0 0 14px; color: #c9ced8; font-size: 0.88rem; }
      .bb .ct-dl { display: grid; grid-template-columns: 180px minmax(0, 1fr); gap: 8px 18px; margin: 0; font-size: 0.9rem; }
      .bb .ct-dl dt { color: #9aa1ad; }
      .bb .ct-dl dd { margin: 0; color: #e8e6e1; overflow-wrap: anywhere; }
      .bb .ct-dl dd .val { font-weight: 700; }
      .bb .ct-dl dd .gold { color: #F5B800; font-weight: 700; }
      .bb .ct .pm { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.86rem; }
      .bb .ct h3 { font-size: 0.95rem; margin: 18px 0 6px; }
      .bb .ct-terms { margin: 0; padding-left: 20px; color: #d4d6dc; font-size: 0.88rem; line-height: 1.6; }
      .bb .sigs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; margin-top: 18px; }
      .bb .sig { border-top: 1px solid #ffffff33; padding-top: 6px; font-size: 0.82rem; }
      .bb .sig span { display: block; color: #9aa1ad; }
      .bb .sig i { color: #8a8a86; }
      @media (prefers-reduced-motion: no-preference) { .bb .cv { transition: transform .15s ease; } }
      @media (max-width: 720px) {
        .bb .jh { display: none; }
        .bb .job > summary { grid-template-columns: minmax(0, 1fr) 18px; gap: 6px 12px; }
        .bb .job > summary .it { grid-column: 1; }
        .bb .job > summary .n { grid-column: 1; text-align: left; white-space: normal; }
        .bb .job > summary .cv { grid-column: 2; grid-row: 1; }
        .bb .ct { margin: 0 8px 12px; padding: 14px; }
        .bb .ct-dl { grid-template-columns: minmax(0, 1fr); gap: 2px; }
        .bb .ct-dl dd { margin-bottom: 8px; }
        .bb .sigs { grid-template-columns: minmax(0, 1fr); }
      }
      .bb { max-width: 1040px; margin: 0 auto; padding: 120px 16px 80px; }
      .bb h1 { font-size: clamp(2rem, 6vw, 3.2rem); line-height: 1.08; margin: 0 0 12px; letter-spacing: -0.02em; }
      .bb h1 b, .bb .gold { color: #F5B800; }
      .bb .lede { color: #c9ced8; font-size: 1.1rem; line-height: 1.6; max-width: 720px; margin: 0 0 28px; }
      .bb .tn, .bb .n, .bb .st, .bb .rate { font-variant-numeric: tabular-nums; }
      .bb .totals { display: flex; flex-wrap: wrap; gap: 28px 48px; align-items: flex-end; padding: 22px 0; border-top: 1px solid #ffffff1a; border-bottom: 1px solid #ffffff1a; }
      .bb .tot b { display: block; font-size: clamp(1.8rem, 5vw, 2.4rem); color: #fff; line-height: 1.1; }
      .bb .tot.big b { color: #F5B800; font-size: clamp(2.2rem, 7vw, 3.4rem); }
      .bb .tot span { color: #9aa1ad; font-size: 0.9rem; }
      .bb .rate { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin: 18px 0 6px; color: #9aa1ad; font-size: 0.9rem; }
      .bb .rate button { font: inherit; font-weight: 600; color: #e8e6e1; background: #15161a; border: 1px solid #ffffff22; border-radius: 999px; padding: 6px 14px; cursor: pointer; }
      .bb .rate button[aria-pressed="true"] { background: #F5B800; color: #1a1300; border-color: #F5B800; }
      .bb .how { color: #c9ced8; line-height: 1.6; margin: 18px 0 0; max-width: 760px; }
      .bb .warn { color: #fcd9a0; font-size: 0.92rem; margin: 10px 0 24px; }
      .bb .toc { display: flex; flex-wrap: wrap; gap: 6px 16px; margin: 0 0 12px; font-size: 0.92rem; }
      .bb a { color: #F5B800; }
      .bb section { margin-top: 44px; }
      .bb .sh { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap: 4px 20px; margin-bottom: 10px; }
      .bb h2 { font-size: 1.35rem; margin: 0; }
      .bb .st { margin: 0; color: #9aa1ad; display: flex; gap: 14px; flex-wrap: wrap; align-items: baseline; }
      .bb .st .c { color: #F5B800; font-weight: 700; }
      .bb .est, .bb .sub { color: #8a8a86; font-size: 0.78rem; }
      .bb .tw { overflow-x: auto; -webkit-overflow-scrolling: touch; border: 1px solid #ffffff14; border-radius: 14px; }
      .bb table { border-collapse: collapse; width: 100%; min-width: 640px; font-size: 0.94rem; }
      .bb th, .bb td { text-align: left; vertical-align: top; padding: 11px 14px; border-top: 1px solid #ffffff12; }
      .bb thead th { border-top: 0; color: #9aa1ad; font-weight: 600; font-size: 0.82rem; background: #0e0f12; }
      .bb .n { text-align: right; white-space: nowrap; }
      .bb td.c { color: #F5B800; font-weight: 700; }
      .bb .sub { display: block; font-weight: 400; }
      .bb .it a { font-weight: 600; color: #fff; text-decoration: none; }
      .bb .it a:hover { color: #F5B800; }
      .bb .nm { font-weight: 600; }
      .bb .u { display: block; color: #8a8a86; font-size: 0.8rem; }
      .bb .pl { display: block; font-size: 0.8rem; color: #8a8a86; margin-top: 4px; }
      .bb .pl a { color: #F5B800 !important; font-weight: 500 !important; margin-left: 6px; }
      .bb .chip { display: inline-block; font-size: 0.74rem; font-weight: 600; padding: 2px 9px; border-radius: 999px; margin: 0 4px 4px 0; white-space: nowrap; }
      .bb .chip.live { background: #22c55e22; color: #5fe08f; }
      .bb .chip.post { background: #F5B80022; color: #F5B800; }
      .bb .chip.x { background: #ffffff14; color: #e8e6e1; }
      .bb .open { list-style: none; padding: 0; margin: 12px 0 0; columns: 2 300px; column-gap: 32px; }
      .bb .open li { break-inside: avoid; padding: 8px 0; border-top: 1px solid #ffffff12; }
      .bb .open li span { display: block; color: #8a8a86; font-size: 0.82rem; }
      .bb .method li { margin: 0 0 12px; line-height: 1.65; color: #d4d6dc; }
      .bb code { background: #17191e; padding: 1px 6px; border-radius: 6px; }
      .bb .gen { color: #8a8a86; font-size: 0.85rem; }
    </style>'''

JS = '''<script>
    (function () {
      var DAY = %s;
      function fmt(n) { return '£' + Math.round(n).toLocaleString('en-GB'); }
      var btns = document.querySelectorAll('.rate button');
      function set(rate) {
        btns.forEach(function (b) { b.setAttribute('aria-pressed', String(+b.dataset.rate === rate)); });
        document.querySelectorAll('.bb .c[data-h]').forEach(function (el) {
          var sub = el.querySelector('.sub'); el.firstChild.nodeValue = fmt(el.dataset.h / DAY * rate);
          if (sub && el.firstChild === sub) el.insertBefore(document.createTextNode(fmt(el.dataset.h / DAY * rate)), sub);
        });
        try { localStorage.setItem('bb-rate', rate); } catch (e) {}
      }
      btns.forEach(function (b) { b.addEventListener('click', function () { set(+b.dataset.rate); }); });
      try { var r = +localStorage.getItem('bb-rate'); if (r && document.querySelector('.rate button[data-rate="' + r + '"]')) set(r); } catch (e) {}
    })();
    </script>'''

DESC = 'A public log of the last month of work on bWalletX: every page and feature, with time taken from git history and an estimated cost at the Kintsugi rate.'


def page(d):
    tpl = rd(os.path.join(ROOT, 'bounties.html'))
    head_end = tpl.index('<style>')
    head = tpl[:head_end]
    head = re.sub(r'<title>.*?</title>', '<title>Kintsugi work log: a month of work, in the open · bWalletX</title>', head)
    head = head.replace('https://bwalletx.com/bounties', 'https://bwalletx.com/kintsugi/work')
    head = head.replace('og-bounties-v1.png', 'og-kintsugi-work-v1.png')
    head = re.sub(r'(name="description" content=")[^"]*', r'\g<1>' + DESC, head)
    head = re.sub(r'(property="og:description" content=")[^"]*', r'\g<1>' + DESC, head)
    head = re.sub(r'(name="twitter:description" content=")[^"]*', r'\g<1>' + DESC, head)
    head = re.sub(r'(property="og:title" content=")[^"]*', r'\g<1>Kintsugi: a month of bWalletX work, in the open', head)
    head = re.sub(r'(name="twitter:title" content=")[^"]*', r'\g<1>Kintsugi: a month of bWalletX work, in the open', head)
    head = re.sub(r'(property="og:image:alt" content=")[^"]*', r'\g<1>Kintsugi work log: items shipped, hours and estimated cost', head)
    body_start = tpl.index('<body>'); main_start = tpl.index('<main')
    chrome = tpl[body_start:main_start]
    return head + CSS + '\n  </head>\n  ' + chrome + render(d) + '\n  </body>\n</html>\n'


def summary_html(d):
    """Overview block for /kintsugi, injected between <!-- kintsugi-work:start --> and <!-- kintsugi-work:end -->."""
    th = sum(i['time']['hours'] for i in d['items'])
    tv = sum(i['time']['value_hours'] for i in d['items'])
    start = datetime.date.fromisoformat(d['since']).strftime('%-d %b %Y')
    return f'''<!-- kintsugi-work:start -->
      <section class="kw" aria-labelledby="kw-h">
        <h2 id="kw-h">Work done so far</h2>
        <p>Since the project began on {start}: {len(d["items"])} pages and features, about {th:,.0f} wall-clock hours, worth $20 an hour in pay. Running work in parallel with Claude produced about {tv:,.0f} hours of work, the estimated value of work.</p>
        <div class="kw-tw"><table class="kw-t">
          <thead><tr><th>Developer</th><th class="n">Jobs</th><th class="n">Hours</th><th class="n">Pay at $20/h</th><th class="n">Estimated value of work</th></tr></thead>
          <tbody><tr><td><strong>{E(DEV)}</strong> · with Claude</td><td class="n">{len(d["items"])}</td><td class="n">{th:,.0f}</td><td class="n"><strong>≈ {money(th)}</strong> · ≈ {bsv(th)[1:]}</td><td class="n kw-g">≈ {money(tv)}</td></tr></tbody>
          <tfoot><tr><td>Running total</td><td class="n">{len(d["items"])}</td><td class="n">{th:,.0f}</td><td class="n">≈ {money(th)} · ≈ {bsv(th)[1:]}</td><td class="n kw-g">≈ {money(tv)}</td></tr></tfoot>
        </table></div>
        <p class="kw-note">Estimate from git history, capped at {CAP_H_DAY} hours a day for {d["cap"]["days"]} days; not an invoice or payment. BSV at ${PRICE["usd"]:,.2f} per BSV on {E(PRICE["date"])}. Updated {E(d["generated"])}.</p>
        <p><a href="/kintsugi/work">See every job &rarr;</a></p>
        <style>
          .kw-tw {{ overflow-x: auto; border: 1px solid #ffffff14; border-radius: 14px; margin: 12px 0 8px; }}
          .kw-t {{ border-collapse: collapse; width: 100%; min-width: 560px; font-variant-numeric: tabular-nums; }}
          .kw-t th, .kw-t td {{ text-align: left; padding: 10px 14px; border-top: 1px solid #ffffff12; vertical-align: top; }}
          .kw-t thead th {{ border-top: 0; color: #9aa1ad; font-size: 0.82rem; font-weight: 600; }}
          .kw-t .n {{ text-align: right; white-space: nowrap; }}
          .kw-t tfoot td {{ color: #F5B800; font-weight: 700; }}
          .kw-t .kw-g, .kw-t tfoot td.kw-g {{ color: #3ddc84; font-weight: 700; }}
          .kw-note {{ color: #8a8a86; font-size: 0.88rem; }}
        </style>
      </section>
      <!-- kintsugi-work:end -->'''


def cap_hours(d):
    """Parallel sessions overlap, so summed estimates can exceed the clock. Scale all items down to CAP_H_DAY a day."""
    days = max(1, (datetime.datetime.strptime(d['generated'], '%d %b %Y').date() - datetime.date.fromisoformat(d['since'])).days)
    tot, cap = sum(i['time']['hours'] for i in d['items']), CAP_H_DAY * days
    d['cap'] = dict(days=days, hours=cap, applied=tot > cap)
    for i in d['items']: i['time']['value_hours'] = i['time']['hours']
    if tot > cap:
        for i in d['items']: i['time']['hours'] *= cap / tot


def inject(d):
    p = os.path.join(ROOT, 'kintsugi.html')
    if not os.path.exists(p): return
    s = rd(p); block = summary_html(d)
    if '<!-- kintsugi-work:start -->' in s:
        s = re.sub(r'<!-- kintsugi-work:start -->.*?<!-- kintsugi-work:end -->', lambda m: block, s, flags=re.S)
    else:
        anchor = '<h2>Open source</h2>' if '<h2>Open source</h2>' in s else '</main>'
        s = s.replace(anchor, block + '\n\n      ' + anchor, 1)
    open(p, 'w').write(s)


if __name__ == '__main__':
    if '--render' in sys.argv:
        d = json.load(open(DATA))
        if 'price' not in d:
            d['price'] = fetch_price(); json.dump(d, open(DATA, 'w'), indent=1)
    else:
        d = gather()
        os.makedirs(os.path.dirname(DATA), exist_ok=True)
        json.dump(d, open(DATA, 'w'), indent=1)
    os.makedirs(os.path.join(ROOT, 'kintsugi'), exist_ok=True)
    PRICE.update(d['price'])
    cap_hours(d)
    open(os.path.join(ROOT, 'kintsugi', 'work.html'), 'w').write(page(d))
    inject(d)
    th = sum(i['time']['hours'] for i in d['items'])
    print(f"items={len(d['items'])} hours={th:.0f} cost={money(th)} / {bsv(th)} open={len(d['open'])}")
