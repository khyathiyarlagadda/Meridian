from typing import Dict, Any, List
from agents.audit_logger import audit_logger
from services.merchant_settings import merchant_settings_manager

class SupervisorAgent:
    def __init__(self):
        self.existing_campaign_ids: List[str] = []

    def evaluate_campaign_risk(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministic rules-based supervisor evaluating campaign policy compliance.
        Enforces dynamic budget limits, discount caps, duplicate detection, and risk-tier classification.
        Reads operational guardrail thresholds directly from merchant settings storage.
        NOT an LLM call -- strictly plain Python conditionals.
        """
        # Fetch current dynamic guardrails set by merchant
        settings = merchant_settings_manager.get_settings()
        max_budget = float(settings.get("max_campaign_budget", 50000.0))
        max_discount = float(settings.get("max_discount_percent", 25.0))
        auto_approve_drafts = bool(settings.get("auto_approve_draft_campaigns", False))

        camp_id = campaign_data.get("campaign_id", campaign_data.get("id", ""))
        title = campaign_data.get("title", "")
        budget = float(campaign_data.get("budget_inr", 0.0))
        discount = float(campaign_data.get("discount_pct", 0.0))
        action_type = campaign_data.get("action_type", "launch_campaign")

        violations = []

        # 1. High-Risk Action Guardrail (No code path for high-risk operations like refunds/payment config)
        if action_type in ["process_refund", "payment_config_change", "delete_database"]:
            audit_logger.log_action(
                agent="SupervisorAgent",
                action="evaluate_campaign_risk",
                input_summary=f"Evaluated high-risk action: {action_type}",
                output_summary="REJECTED: High-risk action has no code execution path"
            )
            return {
                "campaign_id": camp_id,
                "status": "REJECTED",
                "risk_tier": "high",
                "auto_approved": False,
                "requires_merchant_approval": False,
                "reason": f"High-risk action '{action_type}' is prohibited and has no execution path."
            }

        # 2. Dynamic Budget Limit Guardrail
        if budget > max_budget:
            violations.append(f"Budget ₹{budget:,.2f} exceeds policy maximum of ₹{max_budget:,.2f}")

        # 3. Dynamic Discount Limit Guardrail
        if discount > max_discount:
            violations.append(f"Discount {discount}% exceeds policy maximum of {max_discount}%")

        # 4. Duplicate Campaign Detection Guardrail (Allow re-evaluating existing campaigns)
        if camp_id in self.existing_campaign_ids and campaign_data.get("action_type") == "create_new":
            violations.append(f"Duplicate campaign detected: ID '{camp_id}' already exists")

        # Rejection handling if policy violations exist
        if violations:
            reason = "Policy violation(s): " + "; ".join(violations)
            audit_logger.log_action(
                agent="SupervisorAgent",
                action="evaluate_campaign_risk",
                input_summary=f"Evaluated {camp_id} ({title}) [Limit: ₹{max_budget:,.2f}, {max_discount}%]",
                output_summary=f"REJECTED: {reason}"
            )
            return {
                "campaign_id": camp_id,
                "status": "REJECTED",
                "risk_tier": "high",
                "auto_approved": False,
                "requires_merchant_approval": False,
                "violations": violations,
                "reason": reason
            }

        # Track campaign ID for duplicate checking
        if camp_id:
            self.existing_campaign_ids.append(camp_id)

        # 5. Risk-Tier Classification (Low vs Medium Risk)
        # Low risk: Budget <= ₹10,000 and Discount <= 10% -> Auto-execute if enabled or low risk
        if budget <= 10000.0 and discount <= 10.0 and auto_approve_drafts:
            risk_tier = "low"
            status = "AUTO_EXECUTED"
            auto_approved = True
            requires_approval = False
            audit_msg = "AUTO_EXECUTED (Low Risk)"
        else:
            risk_tier = "medium"
            status = "PENDING_MERCHANT_APPROVAL"
            auto_approved = False
            requires_approval = True
            audit_msg = "PENDING_MERCHANT_APPROVAL (Medium Risk)"

        audit_logger.log_action(
            agent="SupervisorAgent",
            action="evaluate_campaign_risk",
            input_summary=f"Evaluated {camp_id} (Budget: ₹{budget:,.2f}, Discount: {discount}%)",
            output_summary=audit_msg
        )

        return {
            "campaign_id": camp_id,
            "status": status,
            "risk_tier": risk_tier,
            "auto_approved": auto_approved,
            "requires_merchant_approval": requires_approval,
            "approved_by": "SYSTEM_AUTO" if auto_approved else None,
            "policy_check": "PASSED"
        }

supervisor_agent = SupervisorAgent()
