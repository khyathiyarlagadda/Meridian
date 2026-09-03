import subprocess
import os
import sys

def run():
    # Install playwright in python venv if needed
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=False)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        # 1. Products page scroll
        print("Navigating to http://localhost:3000/products...")
        page.goto("http://localhost:3000/products", wait_until="networkidle")
        page.wait_for_timeout(1500)
        print("Scrolling main element down by 650px...")
        page.evaluate("document.querySelector('main').scrollTop = 650")
        page.wait_for_timeout(1000)
        img1_path = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\products_mid_scroll_sidebar_pinned.png"
        page.screenshot(path=img1_path)
        print(f"Captured: {img1_path}")

        # 2. AI Activity page scroll
        print("Navigating to http://localhost:3000/ai-activity...")
        page.goto("http://localhost:3000/ai-activity", wait_until="networkidle")
        page.wait_for_timeout(1500)
        print("Scrolling main element down by 500px...")
        page.evaluate("document.querySelector('main').scrollTop = 500")
        page.wait_for_timeout(1000)
        img2_path = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\ai_activity_mid_scroll_sidebar_pinned.png"
        page.screenshot(path=img2_path)
        print(f"Captured: {img2_path}")

        browser.close()

if __name__ == "__main__":
    run()
