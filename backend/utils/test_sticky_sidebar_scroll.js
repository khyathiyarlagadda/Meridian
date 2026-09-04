const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

  // 1. Load /products and scroll main content area down by 700px
  console.log('Navigating to http://localhost:3000/products...');
  await page.goto('http://localhost:3000/products', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);

  console.log('Scrolling main content on /products...');
  await page.evaluate(() => {
    const mainEl = document.querySelector('main');
    if (mainEl) mainEl.scrollTop = 650;
  });
  await page.waitForTimeout(1000);

  await page.screenshot({
    path: 'C:\\Users\\User\\.gemini\\antigravity\\brain\\449d913b-aff4-429b-87b7-df20ea995eaa\\products_sidebar_pinned_scroll.png',
    fullPage: false
  });
  console.log('Saved products_sidebar_pinned_scroll.png');

  // 2. Load /ai-activity and scroll main content area down by 500px
  console.log('Navigating to http://localhost:3000/ai-activity...');
  await page.goto('http://localhost:3000/ai-activity', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);

  console.log('Scrolling main content on /ai-activity...');
  await page.evaluate(() => {
    const mainEl = document.querySelector('main');
    if (mainEl) mainEl.scrollTop = 500;
  });
  await page.waitForTimeout(1000);

  await page.screenshot({
    path: 'C:\\Users\\User\\.gemini\\antigravity\\brain\\449d913b-aff4-429b-87b7-df20ea995eaa\\ai_activity_sidebar_pinned_scroll.png',
    fullPage: false
  });
  console.log('Saved ai_activity_sidebar_pinned_scroll.png');

  await browser.close();
})();
