import os
import json
from typing import Dict, Any, List
from agents.audit_logger import audit_logger
from services.ai_memory import initialize_or_load_memory, record_memory_usage

ALLOWED_STRATEGIES = [
    "cross-sell",
    "bundle",
    "personalized offer",
    "win-back campaign",
    "product promotion",
    "loyalty incentive"
]

class StrategyAgent:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

    def recommend_strategy(self, opportunity_analysis: Dict[str, Any]) -> Dict[str, Any]:
        opp_type = opportunity_analysis.get("opportunity_type") or opportunity_analysis.get("type") or "bundle_cross_sell"
        return self.propose_strategy(opportunity_analysis, opp_type)

    def propose_strategy(self, opportunity_analysis: Dict[str, Any], opp_type: str) -> Dict[str, Any]:
        """
        Proposes one of the 6 allowed strategic tactics and incorporates Meridian AI Memory reasoning.
        """
        type_strategy_map = {
            "earbud_case_cross_sell": "cross-sell",
            "bundle_cross_sell": "bundle",
            "win_back_cohort": "win-back campaign",
            "high_value_lapsed_winback": "personalized offer",
            "declining_product_mitigation": "loyalty incentive",
            "emerging_product_promotion": "product promotion"
        }

        selected_strategy = type_strategy_map.get(opp_type, "cross-sell")
        assert selected_strategy in ALLOWED_STRATEGIES, f"Strategy {selected_strategy} must be one of {ALLOWED_STRATEGIES}"

        # Fetch active AI Memory entries
        memories = initialize_or_load_memory()
        referenced_memories: List[Dict[str, Any]] = []
        memory_citations: List[str] = []

        # Check performance pattern memory
        weekend_mem = next((m for m in memories if m["key"] == "pattern_weekend_conversion_peak"), None)
        if weekend_mem and selected_strategy in ["cross-sell", "bundle", "product promotion"]:
            referenced_memories.append(weekend_mem)
            memory_citations.append(f"Based on past performance pattern [{weekend_mem['key']}], weekend timing (Saturday-Sunday) is strongly recommended for this campaign because weekend conversion ({weekend_mem['supporting_data'].get('weekend', {}).get('conversion_rate_pct', 4.86)}%) outperforms weekdays ({weekend_mem['supporting_data'].get('weekday', {}).get('conversion_rate_pct', 3.14)}%).")
            record_memory_usage("pattern_weekend_conversion_peak")

        # Check merchant preference memory
        pref_mem = next((m for m in memories if m["key"] == "pref_merchant_discount_cap"), None)
        if pref_mem:
            referenced_memories.append(pref_mem)
            memory_citations.append(f"Adhering to learned merchant preference [{pref_mem['key']}] capping campaign discount percentages to protect gross profit margins.")
            record_memory_usage("pref_merchant_discount_cap")

        citation_text = " " + " ".join(memory_citations) if memory_citations else ""
        rationale = f"Selected strategic tactic '{selected_strategy}' as the optimal commercial mechanism to maximize conversion for {opp_type} opportunities.{citation_text}"

        strategy_output = {
            "opportunity_id": opportunity_analysis.get("opportunity_id"),
            "strategy": selected_strategy,
            "allowed_strategies": ALLOWED_STRATEGIES,
            "rationale": rationale,
            "referenced_memories": [m["key"] for m in referenced_memories],
            "memory_citations": memory_citations
        }

        audit_logger.log_action(
            agent="StrategyAgent",
            action="propose_strategy",
            input_summary=f"Evaluated {opp_type}",
            output_summary=f"Proposed strategy: {selected_strategy} (Referenced Memories: {[m['key'] for m in referenced_memories]})"
        )

        return strategy_output
