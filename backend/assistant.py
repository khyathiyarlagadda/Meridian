import json
import os
import time
from typing import Dict, Any, List

from analytics import load_data, run_product_velocity_trends, generate_opportunities, run_rfm_analysis
from agents.campaign_agent import CampaignAgent
from agents.strategy_agent import StrategyAgent
from agents.opportunity_agent import OpportunityAgent
from agents.supervisor_agent import supervisor_agent
from agents.audit_logger import audit_logger
from merchant_settings import merchant_settings_manager

CAMPAIGNS_FILE = r"C:\Dev\Meridian\data\campaigns.json"

def save_campaign_to_store(campaign: Dict[str, Any]):
    """
    Persists a created campaign object into campaigns.json store.
    """
    campaigns = []
    if os.path.exists(CAMPAIGNS_FILE):
        try:
            with open(CAMPAIGNS_FILE, "r", encoding="utf-8") as f:
                campaigns = json.load(f)
        except Exception:
            pass
    
    # Check if campaign with same ID or title exists
    existing_idx = next((i for i, c in enumerate(campaigns) if c.get("id") == campaign.get("id")), None)
    if existing_idx is not None:
        campaigns[existing_idx] = campaign
    else:
        campaigns.append(campaign)

    os.makedirs(os.path.dirname(CAMPAIGNS_FILE), exist_ok=True)
    with open(CAMPAIGNS_FILE, "w", encoding="utf-8") as f:
        json.dump(campaigns, f, indent=2)

class MeridianAssistant:
    """
    Function-calling AI Assistant for Meridian E-Commerce Intelligence.
    Routes merchant commands through real tool calls to read store analytics,
    create persisted campaign drafts, and inspect guardrail rules.
    """
    def __init__(self):
        pass

    def _get_data(self):
        return load_data()

    def tool_get_biggest_growth_opportunity(self) -> Dict[str, Any]:
        products, customers, transactions, order_items = self._get_data()
        opps = generate_opportunities(products, customers, transactions, order_items)
        top = opps[0] if opps else None
        return {
            "tool_name": "get_biggest_growth_opportunity",
            "top_opportunity": top,
            "total_opportunities": len(opps)
        }

    def tool_create_campaign_draft(self, opportunity_id: str = None) -> Dict[str, Any]:
        products, customers, transactions, order_items = self._get_data()
        opps = generate_opportunities(products, customers, transactions, order_items)
        
        if opportunity_id:
            target_opp = next((o for o in opps if o["id"] == opportunity_id or opportunity_id.lower() in o["id"].lower()), opps[0])
        else:
            target_opp = opps[0]  # Default to biggest opportunity

        # Execute agent pipeline chain
        opp_analysis = OpportunityAgent().analyze_opportunity(target_opp)
        strat = StrategyAgent().propose_strategy(opp_analysis, target_opp["type"])
        campaign = CampaignAgent().generate_campaign(target_opp, strat)
        
        # Enforce PENDING_MERCHANT_APPROVAL status and unique ID
        ts_id = int(time.time())
        campaign["id"] = f"CAMP_ASSISTANT_{target_opp['id']}_{ts_id}"
        campaign["status"] = "PENDING_MERCHANT_APPROVAL"
        
        # Risk evaluation
        supervisor_eval = supervisor_agent.evaluate_campaign_risk(campaign)
        campaign["risk_tier"] = supervisor_eval.get("risk_tier", "medium")

        # Save campaign draft to real database/store
        save_campaign_to_store(campaign)

        audit_logger.log_action(
            agent="Assistant",
            action="create_campaign_draft",
            input_summary=f"Assistant created campaign draft for opportunity '{target_opp['title']}'",
            output_summary=f"Draft Saved to Store: '{campaign['title']}' (ID: {campaign['id']}, Status: PENDING_MERCHANT_APPROVAL)"
        )

        return {
            "tool_name": "create_campaign_draft",
            "campaign_draft": campaign,
            "supervisor_eval": supervisor_eval,
            "opportunity_title": target_opp["title"],
            "approval_notice": "STATUS: PENDING_MERCHANT_APPROVAL — Draft campaign recorded in campaigns database. Requires explicit merchant approval before launch."
        }

    def tool_recommend_promotions(self) -> Dict[str, Any]:
        products, customers, transactions, order_items = self._get_data()
        trends_df = run_product_velocity_trends(products, transactions, order_items)
        opps = generate_opportunities(products, customers, transactions, order_items)

        trends_records = trends_df.to_dict(orient="records")
        emerging = [t for t in trends_records if t["status"] == "emerging"]
        
        top_emerging = emerging[0] if emerging else None
        top_opp = opps[0] if opps else None

        return {
            "tool_name": "recommend_promotions",
            "top_emerging_sku": top_emerging,
            "top_opportunity": top_opp
        }

    def tool_get_guardrail_settings(self) -> Dict[str, Any]:
        settings = merchant_settings_manager.get_settings()
        return {
            "tool_name": "get_guardrail_settings",
            "settings": settings
        }

    def process_query(self, query: str) -> Dict[str, Any]:
        query_lower = query.lower()
        tool_calls_executed = []

        # 1. Action: Create Campaign / Draft Campaign
        if any(w in query_lower for w in ["create a campaign", "create campaign", "draft campaign", "build campaign", "make a campaign"]):
            draft_res = self.tool_create_campaign_draft()
            tool_calls_executed.append(draft_res["tool_name"])
            
            camp = draft_res["campaign_draft"]
            sup = draft_res["supervisor_eval"]
            
            reply = (
                f"I have created a new draft campaign: '{camp['title']}' (ID: {camp['id']}) for opportunity '{draft_res['opportunity_title']}'.\n\n"
                f"- Target Audience: {camp['target_audience']}\n"
                f"- Proposed Offer: {camp['offer']} (Discount: {camp['discount_pct']}%, Budget: INR {camp['budget_inr']:,.2f})\n"
                f"- Policy Status: {sup['status']} (Risk Tier: {sup['risk_tier']})\n\n"
                f"[SAFETY NOTICE]: Per safety rules, this campaign status is PENDING_MERCHANT_APPROVAL. It has been recorded in your campaigns database and requires your explicit approval on the Campaigns page before launch (it will never auto-launch)."
            )

        # 2. Query: Biggest Growth Opportunity
        elif any(w in query_lower for w in ["biggest growth opportunity", "biggest opportunity", "top opportunity", "growth opportunity"]):
            opp_res = self.tool_get_biggest_growth_opportunity()
            tool_calls_executed.append(opp_res["tool_name"])
            
            top = opp_res["top_opportunity"]
            if top:
                reply = (
                    f"Your biggest growth opportunity right now is '{top['title']}' (ID: {top['id']}).\n\n"
                    f"- Target Audience Size: {top['affected_customer_count']:,} qualified buyers\n"
                    f"- Expected Revenue Potential: INR {top['estimated_revenue_potential']['expected']:,.2f}\n"
                    f"- Priority Score: {top['priority_score']:,.2f}\n\n"
                    f"You can ask me to 'Create a campaign for this opportunity' whenever you are ready to draft it."
                )
            else:
                reply = "No active high-yield growth opportunities detected at this time."

        # 3. Query: What should I promote today?
        elif any(w in query_lower for w in ["what should i promote", "promote today", "promotion recommendation", "what to promote"]):
            promo_res = self.tool_recommend_promotions()
            tool_calls_executed.append(promo_res["tool_name"])
            
            em = promo_res["top_emerging_sku"]
            opp = promo_res["top_opportunity"]
            
            recs = []
            if em:
                recs.append(f"1. SKU Demand Surge: '{em['product_name']}' ({em['category']}) - Weekly sales velocity increased by +{em['wow_change_w1']}% WoW.")
            if opp:
                recs.append(f"2. Commercial Bundle Opportunity: '{opp['title']}' - Targeting {opp['affected_customer_count']:,} buyers with INR {opp['estimated_revenue_potential']['expected']:,.2f} revenue potential.")

            reply = "Based on real-time transaction velocity and opportunity analysis, here is what you should promote today:\n\n" + "\n\n".join(recs)

        # 4. Query: Guardrail / Settings Inspection
        elif any(w in query_lower for w in ["guardrail", "settings", "policy", "limits", "safety rules"]):
            guard_res = self.tool_get_guardrail_settings()
            tool_calls_executed.append(guard_res["tool_name"])
            
            s = guard_res["settings"]
            reply = (
                f"Here are your active merchant guardrail settings:\n\n"
                f"- Max Discount Percent: {s['max_discount_percent']}%\n"
                f"- Max Campaign Budget: INR {s['max_campaign_budget']:,.2f} per campaign\n"
                f"- Daily Campaign Limit: {s['max_campaigns_per_day']} campaigns/day\n"
                f"- Launch Policy: ALWAYS REQUIRE MERCHANT APPROVAL (Human-in-the-Loop Locked)"
            )

        # 5. Query: Product Velocity / Sales Drop
        elif any(w in query_lower for w in ["drop", "decline", "sales", "velocity", "why did"]):
            products, customers, transactions, order_items = self._get_data()
            trends_df = run_product_velocity_trends(products, transactions, order_items)
            trends_records = trends_df.to_dict(orient="records")
            tool_calls_executed.append("get_product_trends")

            declining_skus = [t for t in trends_records if t["status"] == "declining"]
            if declining_skus:
                top_dec = declining_skus[0]
                reply = (
                    f"Sales dropped primarily due to a weekly sales velocity decline in SKU '{top_dec['product_name']}' ({top_dec['product_id']}). "
                    f"Unit sales decreased from {top_dec['units_w3']} units (W-3) to {top_dec['units_w1']} units in W-1 ({top_dec['wow_change_w1']}% WoW). "
                    f"Category: {top_dec['category']}, Price: INR {top_dec['price_inr']}."
                )
            else:
                reply = "Product velocity data shows overall stable SKU sales across categories."

        # Catch-All Fallback Overview Query
        else:
            products, customers, transactions, order_items = self._get_data()
            rfm_df = run_rfm_analysis(customers, transactions)
            segment_counts = rfm_df['rfm_segment'].value_counts().to_dict()
            tool_calls_executed.append("get_customer_segments")

            reply = (
                f"Meridian Analytics Engine analyzed {len(rfm_df):,} customers across RFM cohorts: {json.dumps(segment_counts)}.\n\n"
                f"Try asking:\n"
                f"• 'Find my biggest growth opportunity'\n"
                f"• 'Create a campaign for this opportunity'\n"
                f"• 'What should I promote today?'"
            )

        return {
            "query": query,
            "reply": reply,
            "tool_calls_executed": tool_calls_executed
        }

assistant = MeridianAssistant()
