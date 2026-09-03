from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("http://localhost:3000/campaigns/CAMP_OPP_CASE_SCREEN_BUNDLE", wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.evaluate("document.querySelector('main').scrollTop = 450")
    page.wait_for_timeout(1000)
    page.screenshot(path=r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\campaign_detail_predicted_vs_actual_table.png")
    browser.close()
    print("DONE")
