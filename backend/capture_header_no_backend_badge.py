from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 850})

    print("Navigating to http://localhost:3000...")
    page.goto("http://localhost:3000", wait_until="networkidle")
    page.wait_for_timeout(2000)

    img_path = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\dashboard_header_merchant_status.png"
    page.screenshot(path=img_path, full_page=False)
    print(f"Captured: {img_path}")

    browser.close()
