const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium', args:['--no-sandbox'] });
  const p = await b.newPage({ viewport:{width:1280,height:1000} });
  await p.goto('http://localhost:8120/aroma-index.html');
  await p.waitForTimeout(1500);
  await p.screenshot({ path:'preview.png' });
  await b.close();
})();
