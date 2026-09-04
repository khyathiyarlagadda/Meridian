const { chromium } = require('playwright');
const path = require('path');

async function captureRazorpayVerification() {
  console.log('Starting Playwright automated browser verification...');
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1280, height: 900 });

  const artifactDir = "C:\\Users\\User\\.gemini\\antigravity\\brain\\449d913b-aff4-429b-87b7-df20ea995eaa";

  // 1. Open Opportunity Detail Page & Approve Campaign
  console.log('1. Navigating to http://localhost:3000/opportunities/OPP_CASE_SCREEN_BUNDLE...');
  await page.goto('http://localhost:3000/opportunities/OPP_CASE_SCREEN_BUNDLE', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1000);

  const approveBtn = page.locator('button:has-text("Approve & Launch Campaign")');
  if (await approveBtn.isVisible()) {
    console.log('Clicking Approve & Launch Campaign...');
    await approveBtn.click();
    await page.waitForTimeout(2000);
  }

  // 2. Open Checkout Page
  console.log('2. Opening Checkout page...');
  await page.goto('http://localhost:3000/checkout?campaign_id=CAMP_OPP_CASE_SCREEN_BUNDLE', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);

  // Take Checkout Page Screenshot showing TEST MODE badge
  await page.screenshot({ path: path.join(artifactDir, 'checkout_page_test_mode_badge.png') });
  console.log('Captured checkout_page_test_mode_badge.png');

  // 3. Perform Order Creation & Verify Payment directly on page context
  console.log('3. Triggering Razorpay Order & HMAC Verification...');
  await page.evaluate(async () => {
    // 1. Create order
    const createRes = await fetch('http://127.0.0.1:8000/api/campaigns/CAMP_OPP_CASE_SCREEN_BUNDLE/checkout/create-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customer_id: 'CUST_1001', product_id: 'PROD_CASE_01' })
    });
    const orderData = await createRes.json();

    // 2. Compute signature
    const testPaymentId = 'pay_rzp_test_' + Math.random().toString(36).substring(2, 14);
    const keySecret = 'test_secret_MeridianDemoSecret88';
    
    const encoder = new TextEncoder();
    const keyData = encoder.encode(keySecret);
    const messageData = encoder.encode(`${orderData.order_id}|${testPaymentId}`);
    const cryptoKey = await crypto.subtle.importKey('raw', keyData, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
    const signatureBuffer = await crypto.subtle.sign('HMAC', cryptoKey, messageData);
    const signatureArray = Array.from(new Uint8Array(signatureBuffer));
    const testSignature = signatureArray.map(b => b.toString(16).padStart(2, '0')).join('');

    // 3. Verify payment on server
    await fetch('http://127.0.0.1:8000/api/campaigns/CAMP_OPP_CASE_SCREEN_BUNDLE/checkout/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        razorpay_order_id: orderData.order_id,
        razorpay_payment_id: testPaymentId,
        razorpay_signature: testSignature,
        customer_id: 'CUST_1001',
        product: 'Nova Essential Protection Kit (Phone Case + 9H Glass)',
        amount_inr: 1000.0
      })
    });
  });

  // Reload checkout page or click Pay to show Success State View
  const payBtn = page.locator('button:has-text("Pay")').first();
  await payBtn.click();
  await page.waitForTimeout(1000);

  const testPayModalBtn = page.locator('button:has-text("Complete Test Card Payment")');
  if (await testPayModalBtn.isVisible()) {
    await testPayModalBtn.click();
    await page.waitForTimeout(2500);
  }

  // Take Payment Success Screenshot
  await page.screenshot({ path: path.join(artifactDir, 'razorpay_checkout_success.png') });
  console.log('Captured razorpay_checkout_success.png');

  // 4. Navigate to Campaigns Page
  console.log('4. Navigating to Campaigns page...');
  await page.goto('http://localhost:3000/campaigns', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(artifactDir, 'campaigns_predicted_vs_actual_updated.png') });
  console.log('Captured campaigns_predicted_vs_actual_updated.png');

  // 5. Navigate to Activity Page
  console.log('5. Navigating to Activity page...');
  await page.goto('http://localhost:3000/activity', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(artifactDir, 'activity_full_audit_chain.png') });
  console.log('Captured activity_full_audit_chain.png');

  await browser.close();
  console.log('All 4 Razorpay verification screenshots successfully captured!');
}

captureRazorpayVerification().catch(err => {
  console.error('Browser capture error:', err);
  process.exit(1);
});
