const { chromium } = require('/Volumes/2026/Projects/bmovies-app-bwallet/node_modules/playwright');
(async()=>{const b=await chromium.launch({channel:'chrome'});const p=await b.newPage({viewport:{width:1200,height:630}});
await p.goto('file://'+__dirname+'/og-bavatars-v5.html');await p.waitForLoadState('networkidle');await p.waitForTimeout(500);
await p.screenshot({path:'/Volumes/2026/Projects/bwalletx-site/og-bavatars-v5.png'});await b.close();})();
