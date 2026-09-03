import os
import json
from typing import Dict, Any
from agents.audit_logger import audit_logger

class CampaignAgent:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

    def generate_campaign(self, opportunity_data: Dict[str, Any], strategy_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates structured campaign specification: target audience, title, offer, message, timing, budget, discount_pct.
        """
        opp_id = opportunity_data.get("id")
        opp_type = opportunity_data.get("type", "")
        title = opportunity_data.get("title", "")
        affected_count = opportunity_data.get("affected_customer_count", 0)
        strategy = strategy_data.get("strategy", "")

        # Compute specific campaign parameters
        if opp_type == "earbud_case_cross_sell":
            c_title = "Nova Pods Companion Case Discount"
            target_aud = f"Earbud buyers (n={affected_count}) within 7 days of purchase"
            offer = "15% off any Nova Premium Phone Case"
            discount_pct = 15.0
            budget_inr = min(35000.0, affected_count * 50.0)
            message = "Complete your audio setup! Get 15% off any precision-fit Nova Phone Case using code AUDIO15."
            timing = "Triggered automatically 48 hours after Earbud delivery"

        elif opp_type == "bundle_cross_sell":
            c_title = "Essential Protection Kit Bundle (Case + Screen Glass)"
            target_aud = f"Multi-item shoppers (n={affected_count}) interested in phone protection"
            offer = "Save 20% when bundling Phone Case + Tempered Glass"
            discount_pct = 20.0
            budget_inr = 25000.0
            message = "Protect your phone completely! Add 9H Tempered Glass to your Phone Case order and save 20% instantly."
            timing = "In-cart recommendation and checkout add-on trigger"

        elif opp_type == "win_back_cohort":
            c_title = "Welcome Back to Nova: Exclusive INR 300 Voucher"
            target_aud = f"Lapsed active customers (n={affected_count}) inactive for >60 days"
            offer = "INR 300 flat discount on orders over INR 1,499"
            discount_pct = 20.0
            budget_inr = 45000.0
            message = "We miss you at Nova! Enjoy ₹300 off your next order with voucher WELCOME300."
            timing = "Distributed via WhatsApp & Email sequence over 14 days"

        elif opp_type == "high_value_lapsed_winback":
            c_title = "VIP Concierge Re-engagement & Complimentary Accessory"
            target_aud = f"High-Value VIP Lapsed buyers (n={affected_count}) with AOV > INR 2,500"
            offer = "22% VIP discount + Free Fast Charger with next order"
            discount_pct = 22.0
            budget_inr = 48000.0
            message = "As a VIP Nova member, enjoy an exclusive 22% discount plus a complimentary GaN 65W Fast Charger on your next order."
            timing = "Personalized WhatsApp concierge message"

        elif opp_type == "declining_product_mitigation":
            c_title = "Nova Pods Lite Inventory Clearance & Loyalty Perk"
            target_aud = f"Recent gadget shoppers (n={affected_count})"
            offer = "25% discount on Nova Pods Lite"
            discount_pct = 25.0
            budget_inr = 20000.0
            message = "Special flash deal! Grab the Nova Pods Lite at 25% off while stocks last."
            timing = "48-hour flash promotion on store homepage"

        elif opp_type == "emerging_product_promotion":
            c_title = "Nova Fit Pulse 2 Launch Boost & VIP Access"
            target_aud = f"Smartwatch enthusiasts and repeat buyers (n={affected_count})"
            offer = "10% early-adopter bonus cashback"
            discount_pct = 10.0
            budget_inr = 30000.0
            message = "Trending now! The Nova Fit Pulse 2 is flying off shelves. Order today and get 10% instant cashback."
            timing = "Push notification & email blast"

        else:
            c_title = f"Campaign for {title}"
            target_aud = f"Target audience (n={affected_count})"
            offer = "10% off"
            discount_pct = 10.0
            budget_inr = 15000.0
            message = "Check out our special offer on Nova products."
            timing = "Immediate broadcast"

        campaign_package = {
            "campaign_id": f"CAMP_{opp_id}",
            "opportunity_id": opp_id,
            "title": c_title,
            "strategy": strategy,
            "target_audience": target_aud,
            "offer": offer,
            "discount_pct": discount_pct,
            "budget_inr": budget_inr,
            "message": message,
            "timing": timing
        }

        audit_logger.log_action(
            agent="CampaignAgent",
            action="generate_campaign",
            input_summary=f"Created campaign for {opp_id}",
            output_summary=f"Campaign '{c_title}' (Budget: ₹{budget_inr:,.2f}, Discount: {discount_pct}%)"
        )

        return campaign_package
