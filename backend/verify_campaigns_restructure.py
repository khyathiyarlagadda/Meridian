from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        # 1. Screenshot Active/Completed campaign list
        print("Navigating to http://localhost:3000/campaigns...")
        page.goto("http://localhost:3000/campaigns", wait_until="networkidle")
        page.wait_for_timeout(2000)

        img_list = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\campaigns_active_completed_list.png"
        page.screenshot(path=img_list, full_page=False)
        print(f"Captured Active/Completed List Screenshot: {img_list}")

        # 2. Click into completed campaign (Nova Pods Companion Case Discount)
        print("Clicking into completed campaign...")
        page.click("h3:has-text('Nova Pods Companion Case Discount')")
        page.wait_for_timeout(2000)

        # Screenshot Expected/Actual table and summary sentence
        img_detail = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\campaign_completed_detail_results.png"
        page.screenshot(path=img_detail, full_page=False)
        print(f"Captured Completed Detail Results Screenshot: {img_detail}")

        browser.close()

if __name__ == "__main__":
    run()
