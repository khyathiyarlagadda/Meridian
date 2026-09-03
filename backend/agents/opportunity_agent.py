import os
import json
from typing import Dict, Any
from agents.audit_logger import audit_logger

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


class OpportunityAgent:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.api_key and HAS_ANTHROPIC:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None

    def analyze_opportunity(self, opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Translates raw opportunity metrics into natural language description
        with a 'Why?' explanation citing real evidence numbers strictly.
        """
        evidence = opportunity_data.get("supporting_evidence", {})
        title = opportunity_data.get("title", "")
        opp_type = opportunity_data.get("type", "")
        affected = opportunity_data.get("affected_customer_count", 0)
        rev = opportunity_data.get("estimated_revenue_potential", {})

        if self.client:
            prompt = f"""
You are the Opportunity Agent for Meridian E-Commerce Analytics.
Translate the following opportunity metric data into a concise natural language summary with a 'Why?' explanation.
CRITICAL RULE: Cite ONLY the exact empirical evidence numbers provided. Do NOT extrapolate or hallucinate numbers.

Opportunity Data:
{json.dumps(opportunity_data, indent=2)}
            """
            try:
                message = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                natural_desc = message.content[0].text
            except Exception as e:
                natural_desc = self._fallback_analysis(opportunity_data)
        else:
            natural_desc = self._fallback_analysis(opportunity_data)

        output = {
            "opportunity_id": opportunity_data.get("id"),
            "natural_language_summary": natural_desc["summary"],
            "why_explanation": natural_desc["why_explanation"],
            "evidence_cited": evidence
        }

        audit_logger.log_action(
            agent="OpportunityAgent",
            action="analyze_opportunity",
            input_summary=f"Analyzed {opportunity_data.get('id')} ({title})",
            output_summary=natural_desc["summary"]
        )

        return output

    def _fallback_analysis(self, opp: Dict[str, Any]) -> Dict[str, str]:
        evidence = opp.get("supporting_evidence", {})
        opp_type = opp.get("type", "")
        affected = opp.get("affected_customer_count", 0)

        if opp_type == "earbud_case_cross_sell":
            summary = f"High cross-sell velocity detected: Earbud purchasers exhibit a {evidence.get('earbud_7day_case_purchase_rate', 0)}% conversion to Phone Cases within 7 days."
            why = f"Data shows {evidence.get('earbud_buyers_count', 0)} Earbud buyers purchased Phone Cases within 7 days at a {evidence.get('earbud_7day_case_purchase_rate', 0)}% rate compared to the baseline rate of {evidence.get('baseline_case_purchase_rate', 0)}%, generating a relative cross-sell lift of {evidence.get('cross_sell_lift', 0)}x."
        
        elif opp_type == "bundle_cross_sell":
            summary = f"Strong bundling synergy identified between Phone Cases and Screen Protectors across {affected} multi-item orders."
            why = f"Out of {evidence.get('multi_item_order_count', 0)} multi-item orders, Phone Cases and Screen Protectors appeared together in {evidence.get('case_screen_copurchase_count', 0)} orders (co-purchase rate of {evidence.get('co_purchase_rate_pct', 0)}%), achieving a market-basket Lift of {evidence.get('lift', 0)}."
        
        elif opp_type == "win_back_cohort":
            summary = f"Substantial win-back cohort identified comprising {affected} previously active customers."
            why = f"Exactly {evidence.get('lapsed_customers_count', 0)} customers with >= {evidence.get('min_past_orders_threshold', 3)} past orders have been inactive for > {evidence.get('days_inactive_threshold', 60)} days, representing INR {evidence.get('historical_cohort_revenue_inr', 0):,.2f} in historical revenue."
        
        elif opp_type == "declining_product_mitigation":
            summary = f"Sales velocity decline flagged for SKU '{evidence.get('product_name', '')}'."
            why = f"Weekly unit sales for '{evidence.get('product_name', '')}' dropped from {evidence.get('weekly_units_history', [0,0,0])[0]} units (W-3) to {evidence.get('weekly_units_history', [0,0,0])[1]} units (W-2, {evidence.get('wow_change_week2_pct', 0)}%) and {evidence.get('weekly_units_history', [0,0,0])[2]} units (W-1, {evidence.get('wow_change_week1_pct', 0)}%)."
        
        elif opp_type == "emerging_product_promotion":
            summary = f"Emerging high-growth SKU identified: '{evidence.get('product_name', '')}'."
            why = f"Weekly unit sales for '{evidence.get('product_name', '')}' surged from {evidence.get('weekly_units_history', [0,0,0])[0]} units (W-3) to {evidence.get('weekly_units_history', [0,0,0])[1]} units (W-2, +{evidence.get('wow_growth_week2_pct', 0)}%) and {evidence.get('weekly_units_history', [0,0,0])[2]} units (W-1, +{evidence.get('wow_growth_week1_pct', 0)}%)."
        
        elif opp_type == "high_value_lapsed_winback":
            summary = f"High-Value VIP Lapsed segment identified comprising {affected} top-tier buyers."
            why = f"Exactly {evidence.get('high_value_lapsed_count', 0)} VIP customers with >= {evidence.get('min_order_frequency', 4)} orders and AOV > INR {evidence.get('aov_threshold_inr', 2500)} are inactive for > 60 days, representing INR {evidence.get('total_historical_spend_inr', 0):,.2f} in past spend."
        
        else:
            summary = f"Commercial opportunity detected affecting {affected} customers."
            why = f"Supporting evidence metrics: {json.dumps(evidence)}"

        return {"summary": summary, "why_explanation": why}
