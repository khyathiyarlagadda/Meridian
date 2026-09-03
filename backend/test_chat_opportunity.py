import urllib.request
import json

payload = {"query": "find my biggest growth opportunity"}
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/assistant",
    data=json.dumps(payload).encode('utf-8'),
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print(json.dumps(data, indent=2))
