import urllib.request
import json

def test_guardrails():
    print("================================================================================")
    print("MERIDIAN VERIFICATION 1: DYNAMIC GUARDRAILS BACKEND REJECTION TEST")
    print("================================================================================")

    # 1. Update guardrails to lower max_campaign_budget to ₹5,000.00
    update_payload = {
        "max_discount_percent": 15.0,
        "max_campaign_budget": 5000.0,
        "max_campaigns_per_day": 5,
        "auto_approve_analysis": True,
        "auto_approve_draft_campaigns": False,
        "require_approval_to_launch": True
    }

    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/settings/guardrails",
        data=json.dumps(update_payload).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="PUT"
    )

    with urllib.request.urlopen(req) as resp:
        updated_settings = json.loads(resp.read().decode('utf-8'))

    print("1. UPDATED BACKEND GUARDRAILS SETTINGS (PUT /api/settings/guardrails):")
    print(json.dumps(updated_settings, indent=2))
    print()

    # 2. Evaluate campaign exceeding ₹5,000.00 (Budget ₹24,050.00)
    eval_payload = {
        "id": "CAMP_OPP_EARBUD_CROSSSELL",
        "opportunity_id": "OPP_EARBUD_CROSSSELL",
        "title": "Nova Pods Companion Case Discount",
        "strategy": "cross-sell",
        "target_audience": "Earbud buyers (n=481)",
        "offer": "15% off Phone Case",
        "discount_pct": 15.0,
        "budget_inr": 24050.0,
        "message": "Complete your audio setup!",
        "timing": "48 hours after delivery"
    }

    req_eval = urllib.request.Request(
        "http://127.0.0.1:8000/api/campaigns/evaluate",
        data=json.dumps(eval_payload).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req_eval) as resp_eval:
        eval_result = json.loads(resp_eval.read().decode('utf-8'))

    print("--------------------------------------------------------------------------------")
    print("2. ACTUAL SUPERVISOR AGENT REJECTION RESPONSE:")
    print("--------------------------------------------------------------------------------")
    print(json.dumps(eval_result["supervisor_eval"], indent=2))
    print("================================================================================")

if __name__ == "__main__":
    test_guardrails()
