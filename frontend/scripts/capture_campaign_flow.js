const { chromium } = require('playwright');
const path = require('path');

async function capture() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1280, height: 900 });

  const artifactDir = "C:\\Users\\User\\.gemini\\antigravity\\brain\\449d913b-aff4-429b-87b7-df20ea995eaa";

  console.log('Navigating to http://localhost:3000/campaigns...');
  await page.goto('http://localhost:3000/campaigns', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);

  // 1. Capture Hub View
  await page.screenshot({ path: path.join(artifactDir, 'campaign_hub_preview.png') });
  console.log('Captured campaign_hub_preview.png');

  // 2. Select a Campaign to open Builder & Simulator
  const manageBtn = page.locator('button:has-text("Manage Campaign & Simulation")').first();
  if (await manageBtn.isVisible()) {
    await manageBtn.click();
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(artifactDir, 'campaign_builder_preview.png') });
    console.log('Captured campaign_builder_preview.png');

    // 3. Trigger Simulation
    const simBtn = page.locator('button:has-text("Run Predictive Simulation")');
    if (await simBtn.isVisible()) {
      await simBtn.click();
      await page.waitForTimeout(1500);
      await page.screenshot({ path: path.join(artifactDir, 'campaign_simulation_preview.png') });
      console.log('Captured campaign_simulation_preview.png');
    }

    // 4. Trigger Deliberate Policy Rejection (Budget = 65000)
    const budgetInput = page.locator('input[type="number"]').first();
    if (await budgetInput.isVisible()) {
      await budgetInput.fill('65000');
      const evalBtn = page.locator('button:has-text("Evaluate Policy Rules")');
      await evalBtn.click();
      await page.waitForTimeout(1000);
      await page.screenshot({ path: path.join(artifactDir, 'supervisor_rejection_preview.png') });
      console.log('Captured supervisor_rejection_preview.png');
    }
  }

  await browser.close();
  console.log('Flow capture complete!');
}

capture().catch(err => {
  console.error(err);
  process.exit(1);
});
