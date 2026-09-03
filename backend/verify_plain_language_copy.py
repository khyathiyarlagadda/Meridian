import os
import re
from playwright.sync_api import sync_playwright

frontend_dir = r"C:\Dev\Meridian\frontend"

# Terms to search for in user-facing JSX/TSX content
OLD_TERMS = [
    "Customer Segmentation",
    "Behavioral Analytics",
    "Revenue Attribution",
    "Agent Orchestration",
    "Policy Enforcement",
    "Campaign Optimization",
    "Predictive Intelligence"
]

def audit_frontend_code():
    print("--- 1. AUDITING FRONTEND CODEBASE FOR OLD TECHNICAL TERMS ---")
    found_leaks = []
    
    for root, _, files in os.walk(frontend_dir):
        if "node_modules" in root or ".next" in root:
            continue
        for file in files:
            if file.endswith(".tsx") or file.endswith(".jsx"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    for term in OLD_TERMS:
                        if term in content:
                            found_leaks.append((file, term))

    if not found_leaks:
        print("[SUCCESS] ZERO user-facing technical terms found across the frontend!")
    else:
        print(f"Found {len(found_leaks)} occurrences of technical terms:")
        for f, t in found_leaks:
            print(f"  - File {f}: '{t}'")

def capture_screenshots():
    print("\n--- 2. CAPTURING CUSTOMERS & PRODUCTS PAGES SCREENSHOTS ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        # Screenshot Customers Page
        print("Navigating to http://localhost:3000/customers...")
        page.goto("http://localhost:3000/customers", wait_until="networkidle")
        page.wait_for_timeout(2000)
        cust_img = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\customers_page_simplified.png"
        page.screenshot(path=cust_img, full_page=False)
        print(f"Captured Customers Page Screenshot: {cust_img}")

        # Screenshot Products Page
        print("Navigating to http://localhost:3000/products...")
        page.goto("http://localhost:3000/products", wait_until="networkidle")
        page.wait_for_timeout(2000)
        prod_img = r"C:\Users\User\.gemini\antigravity\brain\449d913b-aff4-429b-87b7-df20ea995eaa\products_page_simplified.png"
        page.screenshot(path=prod_img, full_page=False)
        print(f"Captured Products Page Screenshot: {prod_img}")

        browser.close()

if __name__ == "__main__":
    audit_frontend_code()
    capture_screenshots()
