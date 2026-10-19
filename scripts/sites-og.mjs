#!/usr/bin/env node
// Share images for /sites and /sites/<slug>, from data/sites.json.
//   node scripts/sites-og.mjs [slug ...]     (no args: the hub and every listed site)
// Writes og/og-sites-v1.png and og/og-site-<slug>-v1.png with headless Chrome (local only; the daily sync
// does not need it, because these images carry no counts that could go stale). Look at every PNG before
// publishing. Templates go to media-src/og/sites/ (gitignored).
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { join, resolve } from 'node:path';

const ROOT = resolve(new URL('..', import.meta.url).pathname);
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const SRC = join(ROOT, 'media-src/og/sites');
mkdirSync(SRC, { recursive: true });
const data = JSON.parse(readFileSync(join(ROOT, 'data/sites.json'), 'utf8'));
const listed = data.sites.filter((s) => s.listed);
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const logo = 'file://' + join(ROOT, 'logo.svg');
const poster = 'file://' + join(ROOT, 'media/hero-poster.jpg');

const CSS = `
html,body{margin:0;width:1200px;height:630px;overflow:hidden;background:#000}
.og{position:relative;width:1200px;height:630px;overflow:hidden;font-family:'IBM Plex Sans',sans-serif;color:#fff}
.bg{position:absolute;inset:0;background:url(${poster}) center/cover;filter:brightness(.4) saturate(1.2);transform:scale(1.2) translateX(260px)}
.shade{position:absolute;inset:0;background:radial-gradient(circle at 80% 45%,rgba(245,184,0,.22),transparent 45%),linear-gradient(90deg,#000 0%,rgba(0,0,0,.92) 42%,rgba(0,0,0,.4) 80%,rgba(0,0,0,.6) 100%)}
.left{position:absolute;left:72px;top:58px;width:530px}
.mark{display:flex;align-items:center;gap:14px}
.mark img{width:50px;filter:drop-shadow(0 0 22px rgba(245,184,0,.65))}
.mark span{font-family:'Space Grotesk';font-weight:700;font-size:34px;letter-spacing:-1px}
.gold{color:#F5B800}
h1{font-family:'Space Grotesk';font-weight:700;font-size:96px;line-height:1;letter-spacing:-4px;margin:44px 0 22px;background:linear-gradient(180deg,#FFD84D,#E8A100);-webkit-background-clip:text;color:transparent}
.sub{font-size:28px;line-height:1.35;color:#e6e9ee;margin:0}
.url{position:absolute;left:72px;bottom:44px;font-family:'Space Grotesk';font-size:26px;color:#c9ced8}
.url b{color:#fff}
.shot{position:absolute;right:56px;top:150px;width:500px;border-radius:20px;overflow:hidden;border:1px solid #F5B80077;box-shadow:0 0 80px rgba(245,184,0,.3);transform:rotate(3deg);background:#111}
.shot img{display:block;width:100%;aspect-ratio:1200/630;object-fit:cover}
.chips{position:absolute;right:56px;top:96px;width:520px;display:flex;flex-wrap:wrap;gap:12px;justify-content:flex-end}
.chips span{border:1.5px solid #F5B80088;color:#F5B800;border-radius:999px;padding:10px 18px;font-family:'Space Grotesk';font-weight:700;font-size:26px;background:#000a}
`;
const page = (body) => `<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>${CSS}</style></head><body><div class="og"><div class="bg"></div><div class="shade"></div>${body}</div></body></html>`;

const jobs = [];
const only = process.argv.slice(2);
if (!only.length || only.includes('hub')) {
  jobs.push(['og-sites-v1', page(`<div class="left"><div class="mark"><img src="${logo}"><span>bWallet<span class="gold">X</span></span></div>
<h1 style="font-size:84px">One wallet. Every site.</h1><p class="sub">Sign in once with your wallet. Each site shows what is live today.</p></div>
<div class="chips">${listed.map((s) => `<span>${esc(s.name)}</span>`).join('')}</div>
<div class="url"><b>bwalletx.com/sites</b> · ${listed.length} sites</div>`)]);
}
for (const s of listed) {
  if (only.length && !only.includes(s.slug)) continue;
  const img = s.og_image ? `<div class="shot"><img src="${esc(s.og_image)}"></div>` : '';
  jobs.push([`og-site-${s.slug}-v1`, page(`<div class="left"><div class="mark"><img src="${logo}"><span>bWallet<span class="gold">X</span> sites</span></div>
<h1>${esc(s.name)}</h1><p class="sub">${esc(s.pitch)}</p></div>${img}
<div class="url"><b>bwalletx.com/sites/${esc(s.slug)}</b> · ${esc(s.domain.replace(/^www\./, ''))}</div>`)]);
}
const run = promisify(execFile);
for (const [name, html] of jobs) {
  const f = join(SRC, name + '.html');
  writeFileSync(f, html);
  await run(CHROME, ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--virtual-time-budget=8000',
    '--window-size=1200,630', `--screenshot=${join(ROOT, 'og', name + '.png')}`, 'file://' + f]);
  console.log('og/' + name + '.png');
}
