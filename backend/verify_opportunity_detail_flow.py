import json
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1400})

        print("Navigating to http://localhost:3000/opportunities/OPP_CASE_SCREEN_BUNDLE...")
        page.goto("http://localhost:3000/opportunities/OPP_CASE_SCREEN_BUNDLE", wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Screenshot the full 5-step flow
        img_path = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\opportunity_5step_flow_full.png"
        page.screenshot(path=img_path, full_page=True)
        print(f"Captured 5-Step Flow Screenshot: {img_path}")

        # Click Approve & Launch Campaign button
        print("Clicking Approve & Launch Campaign button...")
        page.click("button:has-text('Approve & Launch')")
        page.wait_for_timeout(4000)

        # Screenshot after approval
        img_path_approved = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\opportunity_5step_flow_approved.png"
        page.screenshot(path=img_path_approved, full_page=False)
        print(f"Captured Approved State Screenshot: {img_path_approved}")

        browser.close()

if __name__ == "__main__":
    run()
