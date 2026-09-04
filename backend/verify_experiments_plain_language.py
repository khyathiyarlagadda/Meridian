from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1200})

        print("Navigating to http://localhost:3000/experiments...")
        page.goto("http://localhost:3000/experiments", wait_until="networkidle")
        page.wait_for_timeout(3000)

        # Screenshot Top Section (Try Two Offers & Offer Options)
        img_hub = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\experiments_try_two_offers_hub.png"
        page.screenshot(path=img_hub, full_page=False)
        print(f"Captured Try Two Offers Hub Screenshot: {img_hub}")

        # Scroll to "Which one made more money?" table
        page.evaluate("window.scrollTo(0, 450)")
        page.wait_for_timeout(1000)

        img_table = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\experiments_which_one_made_more_money_table.png"
        page.screenshot(path=img_table, full_page=False)
        print(f"Captured Which One Made More Money Table Screenshot: {img_table}")

        browser.close()

if __name__ == "__main__":
    run()
