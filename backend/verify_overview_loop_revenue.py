from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1200})

        print("Navigating to Overview Page http://localhost:3000/...")
        page.goto("http://localhost:3000/", wait_until="networkidle")
        page.wait_for_timeout(3000)

        # Screenshot Top Section (Header + Loop Diagram + Stat Numbers)
        img_loop = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\overview_page_mental_model_loop.png"
        page.screenshot(path=img_loop, full_page=False)
        print(f"Captured Overview Mental Model Loop Screenshot: {img_loop}")

        # Scroll to Where Revenue Came From section
        page.evaluate("window.scrollTo(0, 450)")
        page.wait_for_timeout(1000)

        img_rev = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\overview_page_where_revenue_came_from.png"
        page.screenshot(path=img_rev, full_page=False)
        print(f"Captured Where Revenue Came From Screenshot: {img_rev}")

        browser.close()

if __name__ == "__main__":
    run()
