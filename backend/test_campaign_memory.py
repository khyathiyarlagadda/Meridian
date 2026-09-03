import json
from agents.opportunity_agent import OpportunityAgent
from agents.strategy_agent import StrategyAgent
from agents.campaign_agent import CampaignAgent

opp = {
    "id": "OPP_CASE_SCREEN_BUNDLE",
    "type": "bundle_cross_sell",
    "title": "Promote Phone Case & Screen Protector Add-On Bundle",
    "affected_customer_count": 2463,
    "estimated_revenue_potential": {"expected": 859587.0}
}

opp_analysis = OpportunityAgent().analyze_opportunity(opp)
strategy_prop = StrategyAgent().propose_strategy(opp_analysis, opp["type"])

print("================================================================================")
print("GENERATED CAMPAIGN PROPOSAL STRATEGY OUTPUT (WITH AI MEMORY CITATION):")
print("================================================================================")
print(json.dumps(strategy_prop, indent=2))
print("================================================================================")
