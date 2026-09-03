import json
import sys
from analytics import load_data, generate_opportunities
from agents.opportunity_agent import OpportunityAgent
from agents.strategy_agent import StrategyAgent
from agents.campaign_agent import CampaignAgent
from agents.evaluation_agent import EvaluationAgent
from agents.supervisor_agent import supervisor_agent
from agents.audit_logger import audit_logger

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("================================================================================")
    print("MERIDIAN MULTI-AGENT WORKFLOW RUNNER")
    print("================================================================================")
    
    # 1. Load opportunities
    products, customers, transactions, order_items = load_data()
    opportunities = generate_opportunities(products, customers, transactions, order_items)
    
    # Pick a real opportunity: Earbud -> Phone Case Cross-Sell
    target_opp = next((o for o in opportunities if o["id"] == "OPP_EARBUD_CROSSSELL"), opportunities[0])
    
    print(f"SELECTED OPPORTUNITY: {target_opp['id']} - {target_opp['title']}")
    print("RAW OPPORTUNITY INPUT:")
    print(json.dumps(target_opp, indent=2))
    print()

    # STAGE 1: OPPORTUNITY AGENT
    print("--------------------------------------------------------------------------------")
    print("STAGE 1: OPPORTUNITY AGENT OUTPUT")
    print("--------------------------------------------------------------------------------")
    opp_agent = OpportunityAgent()
    opp_analysis = opp_agent.analyze_opportunity(target_opp)
    print(json.dumps(opp_analysis, indent=2))
    print()

    # STAGE 2: STRATEGY AGENT
    print("--------------------------------------------------------------------------------")
    print("STAGE 2: STRATEGY AGENT OUTPUT")
    print("--------------------------------------------------------------------------------")
    strat_agent = StrategyAgent()
    strat_recommendation = strat_agent.propose_strategy(opp_analysis, target_opp["type"])
    print(json.dumps(strat_recommendation, indent=2))
    print()

    # STAGE 3: CAMPAIGN AGENT
    print("--------------------------------------------------------------------------------")
    print("STAGE 3: CAMPAIGN AGENT OUTPUT")
    print("--------------------------------------------------------------------------------")
    camp_agent = CampaignAgent()
    campaign_package = camp_agent.generate_campaign(target_opp, strat_recommendation)
    print(json.dumps(campaign_package, indent=2))
    print()

    # STAGE 4: SUPERVISOR AGENT (DETERMINISTIC RULES CHECK)
    print("--------------------------------------------------------------------------------")
    print("STAGE 4: SUPERVISOR AGENT OUTPUT (DETERMINISTIC POLICY CHECK)")
    print("--------------------------------------------------------------------------------")
    supervisor_result = supervisor_agent.evaluate_campaign_risk(campaign_package)
    print(json.dumps(supervisor_result, indent=2))
    print()

    # STAGE 5: EVALUATION AGENT (POST-CAMPAIGN SIMULATION)
    print("--------------------------------------------------------------------------------")
    print("STAGE 5: EVALUATION AGENT OUTPUT")
    print("--------------------------------------------------------------------------------")
    eval_agent = EvaluationAgent()
    mock_post_campaign = {
        "baseline_revenue_inr": 134208.0,
        "post_campaign_revenue_inr": 218500.0,
        "actual_campaign_cost_inr": campaign_package["budget_inr"]
    }
    eval_result = eval_agent.evaluate_campaign(campaign_package, mock_post_campaign)
    print(json.dumps(eval_result, indent=2))
    print("================================================================================")

if __name__ == "__main__":
    main()
