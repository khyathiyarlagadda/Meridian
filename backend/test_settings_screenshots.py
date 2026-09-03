from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 850})

        # 1. Screenshot with chat closed
        print("Navigating to http://localhost:3000/settings...")
        page.goto("http://localhost:3000/settings", wait_until="networkidle")
        page.wait_for_timeout(1500)

        img1_path = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\settings_merchant_friendly_chat_closed.png"
        page.screenshot(path=img1_path, full_page=False)
        print(f"Captured: {img1_path}")

        # 2. Screenshot with chat open
        print("Opening Meridian Assistant Chat Drawer...")
        page.click("button:has-text('Meridian Assistant')")
        page.wait_for_timeout(1000)

        img2_path = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\settings_merchant_friendly_chat_open.png"
        page.screenshot(path=img2_path, full_page=False)
        print(f"Captured: {img2_path}")

        browser.close()

if __name__ == "__main__":
    run()
