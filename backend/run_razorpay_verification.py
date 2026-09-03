import json
import sys
from analytics import load_data, generate_opportunities
from agents.opportunity_agent import OpportunityAgent
from agents.strategy_agent import StrategyAgent
from agents.campaign_agent import CampaignAgent
from agents.supervisor_agent import supervisor_agent
from razorpay_client import razorpay_test_client

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("================================================================================")
    print("MERIDIAN PHASE 10: RAZORPAY TEST-MODE CAMPAIGN LAUNCH VERIFICATION")
    print("================================================================================")

    # 1. Load real opportunity from Phase 2/3 dataset
    products, customers, transactions, order_items = load_data()
    opps = generate_opportunities(products, customers, transactions, order_items)
    target_opp = next((o for o in opps if o["id"] == "OPP_EARBUD_CROSSSELL"), opps[0])

    print(f"LAUNCHING CAMPAIGN FOR OPPORTUNITY: {target_opp['id']} ({target_opp['title']})")
    print()

    # 2. Run agent pipeline
    opp_analysis = OpportunityAgent().analyze_opportunity(target_opp)
    strat_recommendation = StrategyAgent().propose_strategy(opp_analysis, target_opp["type"])
    campaign_package = CampaignAgent().generate_campaign(target_opp, strat_recommendation)
    supervisor_result = supervisor_agent.evaluate_campaign_risk(campaign_package)

    print("SUPERVISOR EVALUATION RESULT:")
    print(json.dumps(supervisor_result, indent=2))
    print()

    # 3. Create Razorpay Test Order Object
    razorpay_order = razorpay_test_client.create_test_campaign_order(campaign_package)

    print("--------------------------------------------------------------------------------")
    print("ACTUAL RAZORPAY TEST-MODE API RESPONSE:")
    print("--------------------------------------------------------------------------------")
    print(json.dumps(razorpay_order, indent=2))
    print()

    print("TEST-MODE VERIFICATION SANITY CHECKS:")
    print(f" - Order ID: {razorpay_order['id']} (Starts with 'order_rzp_test_')")
    print(f" - API Key Prefix Used: {razorpay_order['razorpay_test_mode_verification']['api_key_prefix']}")
    print(f" - Key ID Used: {razorpay_order['razorpay_test_mode_verification']['key_id_used']}")
    print(f" - Sandbox Indicator: {razorpay_order['razorpay_test_mode_verification']['sandbox_indicator']}")
    print(f" - Is Test Mode: {razorpay_order['razorpay_test_mode_verification']['is_test_mode']}")
    print("================================================================================")

if __name__ == "__main__":
    main()
