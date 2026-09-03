from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1100})

        print("Navigating to http://localhost:3000/opportunities/OPP_CASE_SCREEN_BUNDLE...")
        page.goto("http://localhost:3000/opportunities/OPP_CASE_SCREEN_BUNDLE", wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Scroll to Step 5 (Take Action & Limits Check)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)

        print("Clicking 'Approve & Launch Campaign'...")
        page.click("button:has-text('Approve & Launch Campaign')")

        # Capture MID-WAY screenshot (step 4/5)
        time.sleep(0.5)
        img_mid = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\opportunity_approval_progress_midway.png"
        page.screenshot(path=img_mid, full_page=False)
        print(f"Captured Mid-Way Progress Screenshot: {img_mid}")

        # Wait for complete state (step 6: all checkmarks completed & completion banner visible)
        time.sleep(3.2)
        img_complete = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\opportunity_approval_progress_complete.png"
        page.screenshot(path=img_complete, full_page=False)
        print(f"Captured Complete Progress Screenshot: {img_complete}")

        browser.close()

if __name__ == "__main__":
    run()
