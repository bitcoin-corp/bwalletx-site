#!/usr/bin/env node
// Sites hub: data/sites.json is the single source of truth for every bWalletX satellite site.
//   node scripts/sync-sites.mjs            fetch each site, refresh title/description/og:image/status, rebuild pages
//   node scripts/sync-sites.mjs --offline  rebuild pages from data/sites.json only (no network)
// Curated fields (name, pitch, badge, listed, home, related, links, manual_status) are never overwritten.
// Fetched fields: title, description, og_image, status (from <ul class="status"> with <span class="tag live|soon">).
// A failed fetch keeps the previous data. "updated" changes only when the data changes, so a daily run with
// no news makes no commit. Writes: data/sites.json, sites/index.html, sites/<slug>.html, and the sites
// tiles + footer links in index.html (between <!-- sites:... --> markers).
// After a change, run: python3 scripts/seo-head.py && python3 scripts/gen-llms.py
import { readFileSync, writeFileSync, mkdirSync, readdirSync, unlinkSync } from 'node:fs';
import { join, resolve } from 'node:path';

const ROOT = resolve(new URL('..', import.meta.url).pathname);
const DATA = join(ROOT, 'data/sites.json');
const BASE = 'https://bwalletx.com';
const OFFLINE = process.argv.includes('--offline');

// ---------- parsing ----------
const ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', rsquo: '’', lsquo: '‘', ldquo: '“', rdquo: '”',
  mdash: '—', ndash: '–', hellip: '…', middot: '·', rsaquo: '›', lsaquo: '‹', rarr: '→', larr: '←', cent: '¢', pound: '£', check: '✓' };
const unent = (s) => s
  .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
  .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(+d))
  .replace(/&([a-z]+);/gi, (m, n) => ENT[n.toLowerCase()] ?? m);
const strip = (h) => unent(h.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/gi, '').replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').replace(/\s+([.,;:!?)])/g, '$1').trim();
const attr = (tag, name) => { const m = new RegExp(`\\b${name}\\s*=\\s*("([^"]*)"|'([^']*)')`, 'i').exec(tag); return m ? unent(m[2] ?? m[3]) : ''; };
function metaContent(html, key) {
  for (const m of html.matchAll(/<meta\b[^>]*>/gi)) {
    const t = m[0];
    if (attr(t, 'property') === key || attr(t, 'name') === key) return attr(t, 'content').trim();
  }
  return '';
}
export function parseSite(html, pageUrl) {
  const title = strip((/<title[^>]*>([\s\S]*?)<\/title>/i.exec(html) || [, ''])[1]);
  const description = metaContent(html, 'description') || metaContent(html, 'og:description');
  let og = metaContent(html, 'og:image') || metaContent(html, 'twitter:image');
  if (og) og = new URL(og, pageUrl).href;
  // The status checklist: the first <ul> whose class list includes "status".
  const ul = /<ul\b[^>]*class\s*=\s*["'][^"']*\bstatus\b[^"']*["'][^>]*>([\s\S]*?)<\/ul>/i.exec(html);
  let status = null;
  if (ul) {
    status = [];
    for (const li of ul[1].matchAll(/<li\b[^>]*>([\s\S]*?)<\/li>/gi)) {
      const body = li[1];
      const tag = /<(span|em|i|b)\b[^>]*class\s*=\s*["'][^"']*\btag\b([^"']*)["'][^>]*>([\s\S]*?)<\/\1>/i.exec(body);
      const cls = tag ? tag[2] : '';
      const word = tag ? strip(tag[3]).toLowerCase() : '';
      const state = /\blive\b/.test(cls) || word === 'live' ? 'live' : /\b(soon|coming)\b/.test(cls) || /coming|soon/.test(word) ? 'coming' : null;
      if (!state) continue;
      const rest = tag ? body.replace(tag[0], '') : body;
      const small = /<small\b[^>]*>([\s\S]*?)<\/small>/i.exec(rest);
      const head = /<b\b[^>]*>([\s\S]*?)<\/b>/i.exec(rest);
      let text, detail = '';
      if (small && head) { text = strip(head[1]); detail = strip(small[1]); }
      else text = strip(rest);
      if (text) status.push(detail ? { state, text, detail } : { state, text });
    }
    if (!status.length) status = null;
  }
  return { title, description, og_image: og, status };
}

async function fetchText(url) {
  const r = await fetch(url, { headers: { 'user-agent': 'bwalletx-sites-sync/1 (+https://bwalletx.com/sites)' }, redirect: 'follow', signal: AbortSignal.timeout(20000) });
  if (!r.ok) throw new Error(`${url}: HTTP ${r.status}`);
  return r.text();
}

// ---------- html helpers ----------
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const fmtDate = (iso) => { const [y, m, d] = iso.split('-').map(Number); return `${d} ${'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(' ')[m - 1]} ${y}`; };
const statusOf = (s) => s.status || s.manual_status || [];
const counts = (s) => { const st = statusOf(s); return { live: st.filter((x) => x.state === 'live').length, coming: st.filter((x) => x.state === 'coming').length }; };
const countLine = (s) => { const c = counts(s); return `<span class="cnt live">${c.live} Live</span><span class="cnt soon">${c.coming} Coming</span>`; };

const TOPBAR = `    <div class="beta-banner">bWalletX is in <strong>beta</strong>: test with small amounts.</div>
    <header class="topbar">
      <div class="wrap topbar-in">
        <a class="brand" href="/"><img src="/logo.svg" alt="" width="34" height="30" /><span>bWallet<span class="gold">X</span></span></a>
        <nav aria-label="Pages">
          <a href="/features">Features</a><a href="/exchange">Exchange</a><a href="/social">Social</a><a href="/agent">Agents</a><a href="/extension">Extension</a><a href="/developers">Developers</a>
        </nav>
        <span class="nav-cta"><a class="dl-btn" href="/get">Download</a><a class="web-btn" href="https://web.bwalletx.com" target="_blank" rel="noopener">Web &rarr;</a></span>
      </div>
    </header>
    <script src="/nav.js"></script>`;

const STYLE = `    <style>
      .ext { max-width: 1080px; margin: 0 auto; padding: 120px 20px 80px; }
      .ext.narrow { max-width: 760px; }
      .ext h1 { font-size: clamp(2rem, 6vw, 3rem); margin: 10px 0 10px; line-height: 1.15; }
      .ext h2 { margin: 44px 0 10px; font-size: 1.4rem; }
      .ext p, .ext li { line-height: 1.7; }
      .ext a { overflow-wrap: anywhere; }
      .meta { color: #8a8a86; font-size: 0.9rem; margin: 0; }
      .meta a { color: #8a8a86; }
      .lede { color: #d7dbe2; font-size: 1.15rem; max-width: 720px; }
      .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin: 32px 0; }
      .scard { display: flex; flex-direction: column; background: #101114; border: 1px solid #ffffff14; border-radius: 18px; overflow: hidden; color: #fff; text-decoration: none; transition: border-color .15s, transform .15s; }
      .scard:hover { border-color: #F5B80088; transform: translateY(-2px); }
      .scard > img { display: block; width: 100%; height: auto; max-height: none; aspect-ratio: 1200 / 630; object-fit: cover; background: #17191e; }
      .scard .in { padding: 16px 18px 18px; display: flex; flex-direction: column; gap: 8px; flex: 1; }
      .scard .nm { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 1.2rem; }
      .scard .nm img { width: 26px; height: 26px; aspect-ratio: 1; border-radius: 6px; background: none; }
      .scard p { margin: 0; color: #a7adb8; line-height: 1.5; font-size: .95rem; }
      .scard .ft { margin-top: auto; display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap; padding-top: 6px; }
      .scard .dom { color: #F5B800; font-size: .9rem; font-weight: 600; }
      .cnts { display: flex; gap: 6px; }
      .cnt { font-size: .75rem; font-weight: 700; letter-spacing: .02em; border-radius: 999px; padding: 3px 9px; }
      .cnt.live { color: #0b1a0f; background: #4ade80; }
      .cnt.soon { color: #F5B800; border: 1px solid #F5B80077; }
      .hero-img { display: block; border-radius: 18px; overflow: hidden; border: 1px solid #ffffff14; margin: 26px 0; }
      .hero-img img { display: block; width: 100%; height: auto; aspect-ratio: 1200 / 630; object-fit: cover; }
      .btns { display: flex; flex-wrap: wrap; gap: 12px; margin: 18px 0; }
      .btn { display: inline-block; background: #F5B800; color: #1a1300; font-weight: 700; border-radius: 999px; padding: 11px 20px; text-decoration: none; }
      .btn.ghost { background: none; color: #F5B800; border: 1.5px solid #F5B80077; }
      .box { background: #101114; border: 1px solid #ffffff12; border-radius: 16px; padding: 18px 22px; margin: 28px 0; }
      .box h2 { margin: 0 0 8px; font-size: 1.1rem; }
      .box ul.chk { list-style: none; padding-left: 0; margin: 0; }
      .box ul.chk li { margin: 8px 0; display: flex; gap: 10px; }
      .box ul.chk li .ic { flex: 0 0 1.2em; color: #4ade80; font-weight: 700; }
      .box ul.chk li.coming .ic { color: #8a8a86; }
      .box ul.chk small { display: block; color: #8a8a86; line-height: 1.5; }
      .small { color: #8a8a86; font-size: 0.85rem; }
      .related { color: #a7adb8; }
      .pn { display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; margin-top: 40px; border-top: 1px solid #ffffff14; padding-top: 20px; }
      .pn a { color: #F5B800; text-decoration: none; max-width: 100%; }
      @media (max-width: 520px) { .grid { grid-template-columns: 1fr; } }
    </style>`;

function head({ title, desc, path, og, ogAlt }) {
  const url = BASE + path;
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${esc(title)}</title>
    <meta name="description" content="${esc(desc)}" />
    <link rel="canonical" href="${url}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="${url}" />
    <meta property="og:site_name" content="bWalletX" />
    <meta property="og:title" content="${esc(title)}" />
    <meta property="og:description" content="${esc(desc)}" />
    <meta property="og:image" content="${BASE}${og}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="${esc(ogAlt)}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@bWalletX" />
    <meta name="twitter:title" content="${esc(title)}" />
    <meta name="twitter:description" content="${esc(desc)}" />
    <meta name="twitter:image" content="${BASE}${og}" />
    <link rel="icon" href="/favicon.ico" />
    <link rel="stylesheet" href="/styles.css" />
${STYLE}
  </head>`;
}

const cardImg = (s) => s.og_image || `${BASE}/og/og-site-${s.slug}-v1.png`;

function hubPage(data) {
  const listed = data.sites.filter((s) => s.listed);
  const cards = listed.map((s) => `        <a class="scard" href="/sites/${s.slug}">
          <img src="${esc(cardImg(s))}" alt="${esc(s.name)} share image" width="1200" height="630" />
          <span class="in">
            <span class="nm"><img src="https://${esc(s.domain)}/favicon.svg" alt="" width="26" height="26" loading="lazy" onerror="this.remove()" />${esc(s.name)}</span>
            <p>${esc(s.pitch)}</p>
            <span class="ft"><span class="dom">${esc(s.domain.replace(/^www\./, ''))}</span><span class="cnts">${countLine(s)}</span></span>
          </span>
        </a>`).join('\n');
  return `${head({ title: 'Sites · bWalletX', desc: `Every site that runs on bWalletX: ${listed.map((s) => s.name).join(', ')}. One wallet signs you in to all of them. Each shows what is live today and what is coming.`, path: '/sites', og: '/og/og-sites-v1.png', ogAlt: 'bWalletX sites: one wallet, every site' })}
  <body>
${TOPBAR}
    <main class="ext">
      <p class="meta"><a href="/">bWalletX</a> · Sites · updated ${fmtDate(data.updated)}</p>
      <h1>One wallet. Every site.</h1>
      <p class="lede">Each of these sites runs on bWalletX. Sign in once with your wallet and they all work together. Every site keeps its own list of what is live today and what is coming; the counts below come from those lists.</p>
      <div class="grid">
${cards}
      </div>
      <p class="small">Counts are read from each site&rsquo;s own status list once a day. Last change: ${fmtDate(data.updated)}.</p>
      <p class="related">Related: <a href="/bapps">bApps</a> · <a href="/features">Features</a> · <a href="/connect">Connect</a> · <a href="/blog">Blog</a></p>
    </main>
  </body>
</html>
`;
}

function sitePage(data, s, i, list) {
  const st = statusOf(s);
  const c = counts(s);
  const from = s.status ? `as listed on ${esc(s.domain.replace(/^www\./, ''))}` : 'kept by hand';
  const items = st.map((x) => `          <li class="${x.state}"><span class="ic">${x.state === 'live' ? '&check;' : '&#9723;'}</span><span>${esc(x.text)}${x.detail ? `<small>${esc(x.detail)}</small>` : ''}</span></li>`).join('\n');
  const links = (s.links || []).map((l) => `<a class="btn ghost" href="${esc(l.url)}">${esc(l.label)} &rarr;</a>`).join('');
  const related = (s.related || []).map(([h, t]) => `<a href="${esc(h)}">${esc(t)}</a>`).join(' · ');
  const prev = list[(i - 1 + list.length) % list.length], next = list[(i + 1) % list.length];
  const about = s.description_override || s.description;
  const what = about && about !== s.pitch ? `      <h2>What it is</h2>\n      <p>${esc(about)}</p>\n` : '';
  const desc = `${s.name} (${s.domain.replace(/^www\./, '')}): ${s.pitch} ${c.live} live, ${c.coming} coming.`;
  return `${head({ title: `${s.name} · bWalletX sites`, desc, path: `/sites/${s.slug}`, og: `/og/og-site-${s.slug}-v1.png`, ogAlt: `${s.name}: ${s.pitch}` })}
  <body>
${TOPBAR}
    <main class="ext narrow">
      <p class="meta"><a href="/sites">Sites</a> · ${esc(s.domain.replace(/^www\./, ''))}</p>
      <h1>${esc(s.name)}</h1>
      <p class="lede">${esc(s.pitch)}</p>
      <a class="hero-img" href="${esc(s.url)}"><img src="${esc(cardImg(s))}" alt="${esc(s.name)} share image" width="1200" height="630" /></a>
      <div class="btns"><a class="btn" href="${esc(s.url)}">Open ${esc(s.domain.replace(/^www\./, ''))} &rarr;</a>${links}</div>
${what}      <div class="box" id="status">
        <h2>Status: ${c.live} live, ${c.coming} coming</h2>
        <ul class="chk">
${items}
        </ul>
        <p class="small">${from}, updated ${fmtDate(data.updated)}.</p>
      </div>
      <p>${esc(s.name)} runs on bWalletX: one wallet signs you in and pays, here and on every other site. <a href="/get">Get bWalletX</a>.</p>
${related ? `      <p class="related">In bWalletX: ${related}</p>\n` : ''}      <div class="pn"><a href="/sites/${prev.slug}">&larr; ${esc(prev.name)}</a><a href="/sites">All sites</a><a href="/sites/${next.slug}">${esc(next.name)} &rarr;</a></div>
    </main>
  </body>
</html>
`;
}

function homeTiles(data) {
  return data.sites.filter((s) => s.home).map((s) => {
    const live = s.badge === 'live';
    return `            <a class="tile" href="${esc(s.url)}"><span class="tile-tag ${live ? 'live' : 'soon'}">${live ? 'Live' : 'Coming'}</span><span class="tile-name">${esc(s.name)}</span><span class="tile-verb">${esc(s.pitch)}</span></a>`;
  }).join('\n');
}
function homeFooter(data) {
  const l = data.sites.filter((s) => s.listed).map((s) => `<a href="/sites/${s.slug}">${esc(s.name)}</a>`).join(' · ');
  return `<p class="foot-sites"><a href="/sites">Sites</a>: ${l}</p>`;
}
const between = (src, name, body) => {
  const re = new RegExp(`(<!-- sites:${name} -->)[\\s\\S]*?(\\s*<!-- /sites:${name} -->)`);
  if (!re.test(src)) throw new Error(`index.html: missing <!-- sites:${name} --> markers`);
  return src.replace(re, (_, a, b) => `${a}\n${body}${b}`);
};

// ---------- main ----------
const data = JSON.parse(readFileSync(DATA, 'utf8'));
const before = JSON.stringify(data.sites);
if (!OFFLINE) {
  for (const s of data.sites) {
    try {
      const html = await fetchText(s.url);
      const p = parseSite(html, s.url);
      if (p.title) s.title = p.title;
      if (p.description) s.description = p.description;
      if (p.og_image) s.og_image = p.og_image;
      if (p.status) s.status = p.status;
      for (const l of s.links || []) {
        try { const q = parseSite(await fetchText(l.url), l.url); if (q.og_image) l.og_image = q.og_image; } catch (e) { console.warn('  link', e.message); }
      }
      console.log(`${s.slug.padEnd(15)} ${p.status ? `${p.status.filter((x) => x.state === 'live').length} live / ${p.status.filter((x) => x.state === 'coming').length} coming` : 'no status list'}`);
    } catch (e) {
      console.warn(`${s.slug.padEnd(15)} kept previous data (${e.message})`);
    }
  }
}
const changed = JSON.stringify(data.sites) !== before;
if (changed) data.updated = new Date().toISOString().slice(0, 10);
writeFileSync(DATA, JSON.stringify(data, null, 2) + '\n');

const listed = data.sites.filter((s) => s.listed);
mkdirSync(join(ROOT, 'sites'), { recursive: true });
writeFileSync(join(ROOT, 'sites/index.html'), hubPage(data));
const keep = new Set(['index.html']);
listed.forEach((s, i) => { writeFileSync(join(ROOT, `sites/${s.slug}.html`), sitePage(data, s, i, listed)); keep.add(`${s.slug}.html`); });
for (const f of readdirSync(join(ROOT, 'sites'))) if (f.endsWith('.html') && !keep.has(f)) unlinkSync(join(ROOT, 'sites', f));

const idxPath = join(ROOT, 'index.html');
let idx = readFileSync(idxPath, 'utf8');
idx = between(idx, 'tiles', homeTiles(data));
idx = between(idx, 'footer', `        ${homeFooter(data)}`);
writeFileSync(idxPath, idx);
console.log(changed ? `data changed (updated ${data.updated})` : 'no data change', `· ${listed.length} site pages`);
