from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        page.goto("http://localhost:3000/campaigns", wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Scroll down to Completed Campaigns
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)

        img_comp = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\campaigns_completed_section.png"
        page.screenshot(path=img_comp, full_page=False)
        print(f"Captured Completed Campaigns Section Screenshot: {img_comp}")

        browser.close()

if __name__ == "__main__":
    run()
