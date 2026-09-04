const { chromium } = require('playwright');
const path = require('path');

async function captureProductsSync() {
  console.log('Capturing Products page with store sync indicator...');
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1280, height: 900 });

  const artifactDir = "C:\\Users\\User\\.gemini\\antigravity\\brain\\449d913b-aff4-429b-87b7-df20ea995eaa";

  await page.goto('http://localhost:3000/products', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);

  const screenshotPath = path.join(artifactDir, 'products_page_store_sync_indicator.png');
  await page.screenshot({ path: screenshotPath });
  console.log('Saved screenshot to:', screenshotPath);

  await browser.close();
}

captureProductsSync().catch(err => {
  console.error('Capture error:', err);
  process.exit(1);
});
