import urllib.request
import json

def run_verification():
    print("================================================================================")
    print("MERIDIAN VERIFICATION 1: PREDICTED VS ACTUAL CAMPAIGN PERFORMANCE TEST")
    print("================================================================================")

    # 1. Approve & Launch campaign CAMP_OPP_CASE_SCREEN_BUNDLE
    approve_payload = {
        "approver": "Merchant Admin",
        "notes": "Approved for full production launch after simulation review"
    }

    req_approve = urllib.request.Request(
        "http://127.0.0.1:8000/api/campaigns/CAMP_OPP_CASE_SCREEN_BUNDLE/approve",
        data=json.dumps(approve_payload).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req_approve) as resp:
        approve_resp = json.loads(resp.read().decode('utf-8'))

    print("1. CAMPAIGN APPROVAL & LAUNCH API RESPONSE:")
    print(json.dumps(approve_resp, indent=2))
    print()

    # 2. Fetch campaign record directly from database / GET /api/campaigns
    req_camps = urllib.request.Request("http://127.0.0.1:8000/api/campaigns")
    with urllib.request.urlopen(req_camps) as resp_camps:
        data = json.loads(resp_camps.read().decode('utf-8'))

    target_camp = next((c for c in data["campaigns"] if c["id"] == "CAMP_OPP_CASE_SCREEN_BUNDLE"), None)

    print("--------------------------------------------------------------------------------")
    print("2. ACTUAL STORED CAMPAIGN PERFORMANCE RECORD IN DATABASE (data/campaigns.json):")
    print("--------------------------------------------------------------------------------")
    print(json.dumps(target_camp, indent=2))
    print("================================================================================")

if __name__ == "__main__":
    run_verification()
