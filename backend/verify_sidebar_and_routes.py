from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 850})

        print("1. Testing main route http://localhost:3000...")
        page.goto("http://localhost:3000", wait_until="networkidle")
        page.wait_for_timeout(1500)

        # Screenshot sidebar showing exactly 8 items
        img_path = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\sidebar_8_items_restructured.png"
        page.screenshot(path=img_path, full_page=False)
        print(f"Captured Sidebar Screenshot: {img_path}")

        # Test all routes for non-404 status
        routes = [
            "/",
            "/opportunities",
            "/customers",
            "/products",
            "/campaigns",
            "/experiments",
            "/activity",
            "/ai-activity",
            "/transactions",
            "/settings"
        ]

        print("\n2. Testing all routes for 200 OK / non-404 status:")
        for r in routes:
            url = f"http://localhost:3000{r}"
            response = page.goto(url, wait_until="domcontentloaded")
            status = response.status
            print(f"Route '{r}' -> Status {status} OK")
            assert status == 200, f"Route {r} failed with status {status}"

        print("\nALL 10 ROUTES VERIFIED CLEANLY WITH ZERO 404 ERRORS!")
        browser.close()

if __name__ == "__main__":
    verify()
