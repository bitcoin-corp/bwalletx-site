const { chromium } = require('/Volumes/2026/Projects/bmovies-app-bwallet/node_modules/playwright');
const ns=process.argv.slice(2);const out=process.env.OUT||'/Volumes/2026/Projects/bwalletx-site/og';
(async()=>{const b=await chromium.launch({channel:'chrome'});const p=await b.newPage({viewport:{width:1200,height:630}});
for(const n of ns){await p.goto('file://'+__dirname+'/og-'+n+'-v2.html');await p.waitForLoadState('networkidle');await p.waitForTimeout(400);await p.screenshot({path:out+'/og-blog-'+n+'-v2.png'});}
await b.close();})();
