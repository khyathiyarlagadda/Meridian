import os
import json
import sys

# Ensure Python path includes data and backend directories
sys.path.append(r"C:\Dev\Meridian\data")
sys.path.append(r"C:\Dev\Meridian\backend")

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def seed_demo_data():
    print("================================================================================")
    print("MERIDIAN DEMO SEED DATA GENERATOR")
    print("================================================================================")
    print("1. Regenerating synthetic dataset for NOVA Electronics & Lifestyle...")
    import generate_nova_data

    print("\n2. Executing deterministic analytics engine pipeline...")
    from analytics import load_data, run_rfm_analysis, run_product_velocity_trends, generate_opportunities
    
    products, customers, transactions, order_items = load_data()
    opps = generate_opportunities(products, customers, transactions, order_items)
    rfm_df = run_rfm_analysis(customers, transactions)
    trends_df = run_product_velocity_trends(products, transactions, order_items)

    print(f" -> Generated {len(opps)} prioritized commercial opportunities.")
    print(f" -> Analyzed {len(rfm_df):,} customer RFM profiles.")
    print(f" -> Tracked sales velocity for {len(trends_df)} SKUs.")

    print("\n3. Resetting Audit Log & Stored Campaigns to baseline seed state...")
    audit_file = r"C:\Dev\Meridian\data\audit_log.json"
    campaigns_file = r"C:\Dev\Meridian\data\campaigns.json"

    initial_audit = [
        {
            "id": 1,
            "timestamp": "2026-08-31T23:11:11.843654",
            "agent": "OpportunityAgent",
            "action": "analyze_opportunity",
            "input_summary": "Analyzed OPP_EARBUD_CROSSSELL (Automated Earbud to Phone Case Cross-Sell Campaign)",
            "output_summary": "High cross-sell velocity detected: Earbud purchasers exhibit a 36.4% conversion to Phone Cases within 7 days.",
            "approver": None
        },
        {
            "id": 2,
            "timestamp": "2026-08-31T23:11:11.844331",
            "agent": "StrategyAgent",
            "action": "propose_strategy",
            "input_summary": "Evaluated earbud_case_cross_sell",
            "output_summary": "Proposed strategy: cross-sell",
            "approver": None
        },
        {
            "id": 3,
            "timestamp": "2026-08-31T23:11:11.844728",
            "agent": "CampaignAgent",
            "action": "generate_campaign",
            "input_summary": "Created campaign for OPP_EARBUD_CROSSSELL",
            "output_summary": "Campaign 'Nova Pods Companion Case Discount' (Budget: ₹24,050.00, Discount: 15.0%)",
            "approver": None
        },
        {
            "id": 4,
            "timestamp": "2026-08-31T23:11:11.845116",
            "agent": "SupervisorAgent",
            "action": "evaluate_campaign_risk",
            "input_summary": "Evaluated CAMP_OPP_EARBUD_CROSSSELL (Budget: ₹24,050.00, Discount: 15.0%)",
            "output_summary": "PENDING_MERCHANT_APPROVAL (Medium Risk)",
            "approver": None
        }
    ]

    initial_campaigns = [
        {
            "id": "CAMP_OPP_EARBUD_CROSSSELL",
            "opportunity_id": "OPP_EARBUD_CROSSSELL",
            "title": "Nova Pods Companion Case Discount",
            "strategy": "cross-sell",
            "target_audience": "Earbud buyers (n=481) within 7 days of purchase",
            "offer": "15% off any Nova Premium Phone Case",
            "discount_pct": 15.0,
            "budget_inr": 24050.0,
            "message": "Complete your audio setup! Get 15% off any precision-fit Nova Phone Case using code AUDIO15.",
            "timing": "Triggered automatically 48 hours after Earbud delivery",
            "status": "LAUNCHED",
            "risk_tier": "medium",
            "roi_pct": 250.5,
            "incremental_revenue_inr": 84292.0
        },
        {
            "id": "CAMP_OPP_CASE_SCREEN_BUNDLE",
            "opportunity_id": "OPP_CASE_SCREEN_BUNDLE",
            "title": "Essential Protection Kit Bundle (Case + Screen Glass)",
            "strategy": "bundle",
            "target_audience": "Multi-item shoppers (n=2,463) interested in phone protection",
            "offer": "Save 20% when bundling Phone Case + Tempered Glass",
            "discount_pct": 20.0,
            "budget_inr": 25000.0,
            "message": "Protect your phone completely! Add 9H Tempered Glass to your Phone Case order and save 20% instantly.",
            "timing": "In-cart recommendation and checkout add-on trigger",
            "status": "PENDING_MERCHANT_APPROVAL",
            "risk_tier": "medium",
            "roi_pct": 320.0,
            "incremental_revenue_inr": 105000.0
        }
    ]

    os.makedirs(os.path.dirname(audit_file), exist_ok=True)
    with open(audit_file, "w", encoding="utf-8") as f:
        json.dump(initial_audit, f, indent=2)

    with open(campaigns_file, "w", encoding="utf-8") as f:
        json.dump(initial_campaigns, f, indent=2)

    print("\nSUCCESS: Clean NOVA seed dataset generated & pre-computed successfully!")
    print("================================================================================")

if __name__ == "__main__":
    seed_demo_data()
