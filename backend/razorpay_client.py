import os
import json
import time
import uuid
from typing import Dict, Any

RAZORPAY_TEST_KEY_ID = os.getenv("RAZORPAY_TEST_KEY_ID", "rzp_test_MeridianDemoKey99")
RAZORPAY_TEST_KEY_SECRET = os.getenv("RAZORPAY_TEST_KEY_SECRET", "test_secret_MeridianDemoSecret88")

class RazorpayTestClient:
    """
    Razorpay Test-Mode Integration Client for Meridian E-Commerce Analytics.
    Strictly operates in Razorpay Test/Sandbox mode using test keys starting with 'rzp_test_'.
    """
    def __init__(self, key_id: str = RAZORPAY_TEST_KEY_ID, key_secret: str = RAZORPAY_TEST_KEY_SECRET):
        assert key_id.startswith("rzp_test_"), f"SECURITY ALERT: Key ID '{key_id}' must start with 'rzp_test_' for test mode!"
        self.key_id = key_id
        self.key_secret = key_secret
        self.environment = "RAZORPAY_SANDBOX_TEST_MODE"

    def create_test_campaign_order(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a test-mode Razorpay Order object representing the campaign offer.
        Calculates amount in paise (1 INR = 100 paise).
        """
        camp_id = campaign_data.get("campaign_id", campaign_data.get("id", "CAMP_001"))
        title = campaign_data.get("title", "Campaign Offer")
        budget_inr = float(campaign_data.get("budget_inr", 25000.0))
        discount_pct = float(campaign_data.get("discount_pct", 15.0))

        # Sample price calculation (e.g. INR 699 base item with discount in paise)
        base_item_price_inr = 699.0
        final_price_inr = base_item_price_inr * (1.0 - (discount_pct / 100.0))
        amount_paise = int(round(final_price_inr * 100.0))

        unique_suffix = uuid.uuid4().hex[:8]
        order_id = f"order_rzp_test_{unique_suffix}"

        response = {
            "id": order_id,
            "entity": "order",
            "amount": amount_paise,
            "amount_paid": 0,
            "amount_due": amount_paise,
            "currency": "INR",
            "receipt": f"receipt_{camp_id}",
            "status": "created",
            "attempts": 0,
            "notes": {
                "campaign_id": camp_id,
                "campaign_title": title,
                "discount_pct": f"{discount_pct}%",
                "allocated_budget_inr": f"INR {budget_inr:,.2f}",
                "merchant_id": "NOVA_ELECTRONICS_INDIA",
                "key_id_prefix": self.key_id[:8],
                "environment_mode": self.environment
            },
            "created_at": int(time.time()),
            "razorpay_test_mode_verification": {
                "is_test_mode": True,
                "api_key_prefix": "rzp_test_",
                "key_id_used": self.key_id,
                "sandbox_indicator": "https://api.razorpay.com/v1/orders [TEST SANDBOX]"
            }
        }

        return response

razorpay_test_client = RazorpayTestClient()

if __name__ == "__main__":
    test_campaign = {
        "campaign_id": "CAMP_OPP_EARBUD_CROSSSELL",
        "title": "Nova Pods Companion Case Discount",
        "budget_inr": 24050.0,
        "discount_pct": 15.0
    }
    result = razorpay_test_client.create_test_campaign_order(test_campaign)
    print(json.dumps(result, indent=2))
