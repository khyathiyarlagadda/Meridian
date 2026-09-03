from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    print("Navigating to http://localhost:3000...")
    page.goto("http://localhost:3000", wait_until="networkidle")
    page.wait_for_timeout(1500)

    print("Opening Meridian Assistant Chat Drawer...")
    page.click("button:has-text('Meridian Assistant')")
    page.wait_for_timeout(1000)

    print("Typing prompt: 'find my biggest growth opportunity'...")
    page.fill("input[placeholder*='Ask about sales drops']", "find my biggest growth opportunity")
    page.click("button:has-text('Send')")
    page.wait_for_timeout(4500)

    img_path = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\assistant_chat_growth_opportunity.png"
    page.screenshot(path=img_path)
    print(f"Captured: {img_path}")

    browser.close()
