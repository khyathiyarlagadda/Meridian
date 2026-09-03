import os
import shutil
from playwright.sync_api import sync_playwright

out_dir = r"C:\Dev\Meridian\frontend\public"
svg_path = os.path.join(out_dir, "meridian-logo.svg")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for size, name in [
        (192, "icon-192.png"),
        (512, "icon-512.png"),
        (180, "apple-touch-icon-180.png"),
        (32, "favicon.png")
    ]:
        page = browser.new_page(viewport={"width": size, "height": size})
        page.goto(f"file:///{svg_path.replace('\\', '/')}")
        out_file = os.path.join(out_dir, name)
        page.screenshot(path=out_file, omit_background=True)
        print(f"Generated {name} ({size}x{size})")
        page.close()

    browser.close()

# Copy favicon.png to favicon.ico
shutil.copyfile(os.path.join(out_dir, "favicon.png"), os.path.join(out_dir, "favicon.ico"))
print("Copied favicon.png -> favicon.ico")

print("ALL BRAND ICON ASSETS SUCCESSFULLY GENERATED IN frontend/public!")
