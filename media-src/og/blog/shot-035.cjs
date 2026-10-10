// Render og-blog-035..038.html to ../../../og/og-blog-0NN.png with headless Chrome (playwright).
// node media-src/og/blog/shot-031.cjs   (playwright from any checkout: set PW=/path/to/node_modules/playwright)
const path = require('path');
const { chromium } = require(process.env.PW || '/Volumes/2026/Projects/bmovies-app-bwallet/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ channel: 'chrome' });
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  for (const n of ['035', '036', '037', '038']) {
    await p.goto('file://' + path.join(__dirname, 'og-blog-' + n + '.html'));
    await p.waitForTimeout(800);
    await p.screenshot({ path: path.join(__dirname, '../../../og/og-blog-' + n + '.png') });
  }
  await b.close();
})();
