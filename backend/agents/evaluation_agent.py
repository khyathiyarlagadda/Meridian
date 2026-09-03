from typing import Dict, Any
from agents.audit_logger import audit_logger

class EvaluationAgent:
    def __init__(self):
        pass

    def evaluate_campaign(self, campaign_data: Dict[str, Any], post_campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compares baseline vs post-campaign metrics and computes ROI and incremental revenue.
        """
        camp_id = campaign_data.get("campaign_id", "")
        title = campaign_data.get("title", "")
        budget = float(campaign_data.get("budget_inr", 0.0))

        baseline_revenue = float(post_campaign_data.get("baseline_revenue_inr", 0.0))
        post_revenue = float(post_campaign_data.get("post_campaign_revenue_inr", 0.0))
        campaign_cost = float(post_campaign_data.get("actual_campaign_cost_inr", budget))

        incremental_revenue = max(0.0, post_revenue - baseline_revenue)
        net_profit = incremental_revenue - campaign_cost
        roi_pct = (net_profit / campaign_cost * 100.0) if campaign_cost > 0 else 0.0

        eval_result = {
            "campaign_id": camp_id,
            "campaign_title": title,
            "baseline_revenue_inr": round(baseline_revenue, 2),
            "post_campaign_revenue_inr": round(post_revenue, 2),
            "incremental_revenue_inr": round(incremental_revenue, 2),
            "actual_campaign_cost_inr": round(campaign_cost, 2),
            "net_profit_inr": round(net_profit, 2),
            "roi_pct": round(roi_pct, 2),
            "performance_summary": f"Campaign '{title}' generated INR {incremental_revenue:,.2f} in incremental revenue against a cost of INR {campaign_cost:,.2f}, delivering an ROI of {roi_pct:.1f}%."
        }

        audit_logger.log_action(
            agent="EvaluationAgent",
            action="evaluate_campaign",
            input_summary=f"Evaluated performance for {camp_id}",
            output_summary=f"Incremental Rev: ₹{incremental_revenue:,.2f}, ROI: {roi_pct:.1f}%"
        )

        return eval_result
