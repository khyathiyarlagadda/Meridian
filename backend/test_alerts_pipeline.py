from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 850})

        print("Navigating to http://localhost:3000...")
        page.goto("http://localhost:3000", wait_until="networkidle")
        page.wait_for_timeout(1500)

        print("Opening Opportunity Alerts Drawer...")
        page.click("button:has-text('Alerts')")
        page.wait_for_timeout(1000)

        print("Triggering Re-Run Detection Pipeline...")
        page.click("button:has-text('Re-Run Detection Pipeline')")
        page.wait_for_timeout(4000)

        img_path = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\opportunity_alerts_rerun_panel.png"
        page.screenshot(path=img_path, full_page=False)
        print(f"Captured: {img_path}")

        browser.close()

if __name__ == "__main__":
    run()
