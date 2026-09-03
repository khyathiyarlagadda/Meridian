import os
import re

FRONTEND_DIR = r"C:\Dev\Meridian\frontend"

PATTERNS = [
    r"Phase\s*\d+",
    r"TODO",
    r"lorem",
    r"placeholder",
    r"avatar",
    r"weather",
    r"crypto",
    r"inventory",
    r"employee",
    r"social-media",
    r"Design System"
]

matches = []

for root, dirs, files in os.walk(FRONTEND_DIR):
    if "node_modules" in root or ".next" in root:
        continue
    for file in files:
        if file.endswith((".tsx", ".ts", ".js", ".jsx", ".json", ".css")):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for idx, line in enumerate(lines, 1):
                        for pat in PATTERNS:
                            if re.search(pat, line, re.IGNORECASE):
                                matches.append({
                                    "file": os.path.relpath(filepath, FRONTEND_DIR),
                                    "line": idx,
                                    "pattern": pat,
                                    "text": line.strip()
                                })
            except Exception as e:
                pass

print(f"FOUND {len(matches)} DEV-LABEL / UNWANTED PATTERN MATCHES:")
print("=" * 80)
for m in matches:
    print(f"[{m['file']}:{m['line']}] ({m['pattern']}) -> {m['text']}")
print("=" * 80)
