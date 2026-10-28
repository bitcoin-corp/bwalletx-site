#!/usr/bin/env python3
"""Give every post on /blog its share-card thumbnail, taken from that post's own og:image, so the index
can't drift from the posts. Run: python3 scripts/blog-index-thumbs.py         (rewrites blog/index.html)
                                 python3 scripts/blog-index-thumbs.py --check (exit 1 if a post has no share image)"""
import html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'blog', 'index.html')
BASE = 'https://bwalletx.com'

def og_image(slug):
    p = os.path.join(ROOT, 'blog', slug + '.html')
    if not os.path.exists(p): return None
    m = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', open(p, encoding='utf-8').read())
    if not m: return None
    src = m.group(1)
    src = src[len(BASE):] if src.startswith(BASE) else src
    return src if src.startswith('/') and os.path.exists(os.path.join(ROOT, src.lstrip('/'))) else None

def fix(li):
    m = re.search(r'href="/blog/(\d{3}-[^"]+)"', li)
    if not m: return li, None
    slug = m.group(1); img = og_image(slug)
    if not img: return li, slug
    li = re.sub(r'<a class="thumb"[^>]*>.*?</a>', '', li, count=1, flags=re.S)
    title = re.search(r'<a href="/blog/%s">(.*?)</a>' % re.escape(slug), li, re.S)
    alt = 'Cover image for post %s: %s' % (slug[:3], html.unescape(re.sub('<[^>]+>', '', title.group(1))) if title else slug)
    thumb = '<a class="thumb" href="/blog/%s"><img src="%s" alt="%s" width="1200" height="630" loading="lazy" decoding="async" /></a>' % (slug, img, html.escape(alt, quote=True))
    return li.replace('<li>', '<li>' + thumb, 1), None

s = open(INDEX, encoding='utf-8').read()
missing = []
def sub(m):
    li, miss = fix(m.group(0))
    if miss: missing.append(miss)
    return li
out = re.sub(r'<li>.*?</li>', sub, s, flags=re.S)
if missing:
    print('posts with no share image:', ', '.join(missing)); sys.exit(1)
if '--check' in sys.argv:
    if out != s: print('blog/index.html thumbnails are out of date: run python3 scripts/blog-index-thumbs.py'); sys.exit(1)
    print('blog index thumbnails OK'); sys.exit(0)
open(INDEX, 'w', encoding='utf-8').write(out)
print('blog index thumbnails synced')
