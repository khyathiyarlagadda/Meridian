import os
import sys
import traceback
import urllib.request
import json

def check_keys_and_test():
    print("================================================================================")
    print("MERIDIAN ASSISTANT ENVIRONMENT & DIAGNOSTIC AUDIT")
    print("================================================================================")

    # Check root .env and backend/.env
    root_env = r"C:\Dev\Meridian\.env"
    backend_env = r"C:\Dev\Meridian\backend\.env"

    for path in [root_env, backend_env]:
        if os.path.exists(path):
            print(f"[FOUND] .env file at {path}:")
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines:
                line_str = line.strip()
                if "=" in line_str and not line_str.startswith("#"):
                    key = line_str.split("=")[0].strip()
                    val = line_str.split("=")[1].strip()
                    is_present = len(val) > 0
                    prefix = val[:6] + "..." if len(val) > 6 else ("SET" if is_present else "EMPTY")
                    print(f"   - Key '{key}': {'PRESENT (Prefix: ' + prefix + ')' if is_present else 'EMPTY'}")
        else:
            print(f"[NOT FOUND] .env file at {path}")

    print()
    print("2. CHECKING BACKEND ASSISTANT DIRECT ENDPOINT (POST http://127.0.0.1:8000/api/assistant):")
    
    test_payload = {"query": "why did sales drop this week"}
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/assistant",
        data=json.dumps(test_payload).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("[SUCCESS] Direct HTTP Endpoint Response:")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print("[ERROR] Direct HTTP Endpoint Failed:")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        if hasattr(e, "read"):
            try:
                err_body = e.read().decode('utf-8')
                print(f"Response Body: {err_body}")
            except Exception:
                pass
        traceback.print_exc()

    print("================================================================================")

if __name__ == "__main__":
    check_keys_and_test()
