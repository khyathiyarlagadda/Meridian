import os
from PIL import Image, ImageDraw

out_dir = r"C:\Dev\Meridian\frontend\public"
os.makedirs(out_dir, exist_ok=True)

def create_logo_image(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer light cream backing rectangle
    margin = int(size * 0.05)
    radius = int(size * 0.24)
    bg_color = (253, 251, 247, 255) # Cream background
    border_color = (229, 221, 208, 255)

    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=bg_color,
        outline=border_color,
        width=int(max(1, size * 0.03))
    )

    # Stylized M path in dark chocolate to apricot gradient
    # We draw geometric M arches
    stroke_w = int(max(2, size * 0.09))

    # Left leg
    x1 = int(size * 0.30)
    y1 = int(size * 0.30)
    y2 = int(size * 0.72)
    draw.line([x1, y1, x1, y2], fill=(42, 24, 16, 255), width=stroke_w)

    # Diagonal left
    x_mid = int(size * 0.50)
    y_mid = int(size * 0.55)
    draw.line([x1, y1, x_mid, y_mid], fill=(140, 74, 39, 255), width=stroke_w)

    # Diagonal right
    x2 = int(size * 0.70)
    draw.line([x_mid, y_mid, x2, y1], fill=(226, 142, 77, 255), width=stroke_w)

    # Right leg
    draw.line([x2, y1, x2, y2], fill=(226, 142, 77, 255), width=stroke_w)

    # Star accent top center
    star_r = int(size * 0.06)
    draw.ellipse([x_mid - star_r, int(size * 0.16) - star_r, x_mid + star_r, int(size * 0.16) + star_r], fill=(226, 142, 77, 255))

    return img

# Generate icons
icon_192 = create_logo_image(192)
icon_192.save(os.path.join(out_dir, "icon-192.png"))
print("Created icon-192.png")

icon_512 = create_logo_image(512)
icon_512.save(os.path.join(out_dir, "icon-512.png"))
print("Created icon-512.png")

apple_180 = create_logo_image(180)
apple_180.save(os.path.join(out_dir, "apple-touch-icon-180.png"))
print("Created apple-touch-icon-180.png")

favicon_32 = create_logo_image(32)
favicon_32.save(os.path.join(out_dir, "favicon.ico"), format="ICO", sizes=[(32, 32)])
print("Created favicon.ico")
