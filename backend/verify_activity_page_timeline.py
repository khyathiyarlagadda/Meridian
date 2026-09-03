from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1200})

        print("Navigating to http://localhost:3000/ai-activity...")
        page.goto("http://localhost:3000/ai-activity", wait_until="networkidle")
        page.wait_for_timeout(2000)

        # 1. Screenshot plain-language timeline view
        img_timeline = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\activity_plain_language_timeline.png"
        page.screenshot(path=img_timeline, full_page=False)
        print(f"Captured Plain Timeline Screenshot: {img_timeline}")

        # 2. Click 'View technical details' on the first entry
        print("Clicking 'View technical details' on first entry...")
        page.click("button:has-text('View technical details')")
        page.wait_for_timeout(1000)

        # Screenshot expanded technical details view
        img_expanded = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\activity_technical_details_expanded.png"
        page.screenshot(path=img_expanded, full_page=False)
        print(f"Captured Expanded Details Screenshot: {img_expanded}")

        browser.close()

if __name__ == "__main__":
    run()
