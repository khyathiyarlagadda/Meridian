from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        page.goto("http://localhost:3000/ai-activity", wait_until="networkidle")
        page.wait_for_timeout(2000)

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)

        img_mem = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\activity_what_meridian_remembers.png"
        page.screenshot(path=img_mem, full_page=False)
        print(f"Captured AI Memory Screenshot: {img_mem}")

        browser.close()

if __name__ == "__main__":
    run()
