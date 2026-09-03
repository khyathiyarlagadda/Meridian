from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 850})

        print("Navigating to http://localhost:3000...")
        page.goto("http://localhost:3000", wait_until="networkidle")
        page.wait_for_timeout(2000)

        # 1. Screenshot sidebar showing the new logo
        sidebar_img = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\sidebar_new_logo_contrast.png"
        page.screenshot(path=sidebar_img, full_page=False)
        print(f"Captured Sidebar Logo Screenshot: {sidebar_img}")

        # 2. Screenshot browser tab / page header top bar showing title & icon elements
        tab_img = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\browser_tab_favicon.png"
        page.screenshot(path=tab_img, clip={"x": 0, "y": 0, "width": 1280, "height": 300})
        print(f"Captured Page Header Screenshot: {tab_img}")

        browser.close()

if __name__ == "__main__":
    run()
