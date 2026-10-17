#!/usr/bin/env node
// Make the /releases share image for the newest release and point releases.html at it.
//   node scripts/release-og.mjs            (newest <article class="rel"> in releases.html)
// Feature lines: each <li data-og="Short line"> if present, else the bullet up to its first ":" or ",".
// Renders media-src/og/og-releases-<v>.html (copied from the latest earlier one) to og-releases-<v>.png
// with headless Chrome, then updates og:image / twitter:image / titles / alt in releases.html.
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { createServer } from 'node:http';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { join, extname, resolve } from 'node:path';

const ROOT = resolve(new URL('..', import.meta.url).pathname);
const OG = join(ROOT, 'media-src/og');
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 8767; // the og templates load the logo and poster from http://localhost:8767

const page = readFileSync(join(ROOT, 'releases.html'), 'utf8');
const art = /<article class="rel" id="v([\d.]+)">([\s\S]*?)<\/article>/.exec(page);
if (!art) throw new Error('no <article class="rel"> in releases.html');
const [, ver, body] = art;

const text = (h) =>
  h.replace(/<[^>]+>/g, '').replace(/&ldquo;|&rdquo;/g, '"').replace(/&rsquo;/g, '’').replace(/&amp;/g, '&').trim();
const short = (li) => {
  const og = /data-og="([^"]+)"/.exec(li[0]);
  if (og) return og[1];
  const t = text(li[1]).split(/[:,;]/)[0].trim();
  return t.length > 44 ? `${t.slice(0, 43).replace(/\s+\S*$/, '')}…` : t;
};
const items = [...body.matchAll(/<li[^>]*>([\s\S]*?)<\/li>/g)];
const tagged = items.filter((li) => /data-og="/.test(li[0]));
const feats = (tagged.length ? tagged : items).map(short).slice(0, 5);
if (!feats.length) throw new Error(`release ${ver} has no bullets`);

// Template: the newest earlier og-releases-*.html.
const vnum = (v) => v.split('.').map(Number).reduce((a, n) => a * 1000 + n, 0);
const prev = readdirSync(OG)
  .map((f) => /^og-releases-([\d.]+)\.html$/.exec(f)?.[1])
  .filter((v) => v && v !== ver)
  .sort((a, b) => vnum(b) - vnum(a))[0];
if (!prev) throw new Error('no earlier media-src/og/og-releases-*.html to copy');
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const html = readFileSync(join(OG, `og-releases-${prev}.html`), 'utf8')
  .replace(new RegExp(`>${prev.replace(/\./g, '\\.')}<`), `>${ver}<`)
  // A function, not a string: a feature like "$1 each" must not be read as a back-reference.
  .replace(/(<h3>NEW IN THIS RELEASE<\/h3>\s*)[\s\S]*?(<\/div>\s*<div class="url">)/, (_m, a, b) => `${a}\n${feats.map((f) => `<div>${esc(f)}</div>`).join('')}${b}`);
if (!html.includes(`>${ver}<`)) throw new Error('template version slot not found');
if (!feats.every((f) => html.includes(`<div>${esc(f)}</div>`))) throw new Error('template feature list not found');
const src = join(OG, `og-releases-${ver}.html`);
writeFileSync(src, html);

// Serve the site root so the template's localhost:8767 assets load, then screenshot.
const types = { '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.html': 'text/html' };
const server = createServer((req, res) => {
  const p = join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(ROOT) || !existsSync(p)) return res.writeHead(404).end();
  res.writeHead(200, { 'content-type': types[extname(p)] || 'application/octet-stream' }).end(readFileSync(p));
});
await new Promise((r) => server.listen(PORT, r));
const png = join(ROOT, `og-releases-${ver}.png`);
try {
  // Async: Chrome loads from this process's server, so blocking here would deadlock.
  await promisify(execFile)(CHROME, [
    '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=1200,630',
    '--virtual-time-budget=5000', `--screenshot=${png}`, `http://localhost:${PORT}/media-src/og/og-releases-${ver}.html`,
  ], { timeout: 60_000 });
} finally {
  server.close();
}

// Point the page at it.
const title = `bWalletX ${ver} — what's new`;
const out = page
  .replace(/og-releases-[\d.]+\.png/g, `og-releases-${ver}.png`)
  .replace(/(<meta property="og:title" content=")[^"]*/, `$1${title}`)
  .replace(/(<meta name="twitter:title" content=")[^"]*/, `$1${title}`)
  .replace(/Latest: [\d.]+\./g, `Latest: ${ver}.`);
writeFileSync(join(ROOT, 'releases.html'), out);
console.log(`✓ og-releases-${ver}.png (${feats.length} features from ${prev} template); releases.html updated`);
