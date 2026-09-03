import os
import re

FRONTEND_DIR = r"C:\Dev\Meridian\frontend"

PATTERNS = [
    r"127\.0\.0\.1",
    r"localhost",
    r"Backend API",
    r"Backend Offline"
]

matches = []

for root, dirs, files in os.walk(FRONTEND_DIR):
    if "node_modules" in root or ".next" in root:
        continue
    for file in files:
        if file.endswith((".tsx", ".ts", ".js", ".jsx")):
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

print(f"FOUND {len(matches)} INFRASTRUCTURE TEXT MATCHES:")
print("=" * 80)
for m in matches:
    safe_text = m['text'].encode('ascii', errors='ignore').decode('ascii')
    print(f"[{m['file']}:{m['line']}] ({m['pattern']}) -> {safe_text}")
print("=" * 80)
