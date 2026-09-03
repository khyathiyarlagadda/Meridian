import json
import sys
from analytics import load_data, generate_opportunities
from simulation import run_campaign_simulation
from experiment import run_controlled_experiment

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("================================================================================")
    print("MERIDIAN PHASE 5: PREDICTIVE SIMULATION & CONTROLLED A/B EXPERIMENT RUNNER")
    print("================================================================================")

    # Load Phase 2/3 opportunity
    products, customers, transactions, order_items = load_data()
    opps = generate_opportunities(products, customers, transactions, order_items)
    target_opp = next((o for o in opps if o["id"] == "OPP_EARBUD_CROSSSELL"), opps[0])

    # 1. RUN PREDICTIVE SIMULATION
    print("--------------------------------------------------------------------------------")
    print("PART 1: PREDICTIVE CAMPAIGN SIMULATION (BOOTSTRAP RESAMPLING)")
    print("--------------------------------------------------------------------------------")
    sim_result = run_campaign_simulation(target_opp)
    print(json.dumps(sim_result, indent=2))
    print()

    print("ONE-LINE METHOD EXPLANATION:")
    print(f"Method: {sim_result['methodology']}")
    print()

    # 2. RUN CONTROLLED A/B EXPERIMENT (500 Control vs 500 AI-Targeted)
    print("--------------------------------------------------------------------------------")
    print("PART 2: CONTROLLED A/B EXPERIMENT (500 CONTROL VS 500 AI-TARGETED)")
    print("--------------------------------------------------------------------------------")
    exp_result = run_controlled_experiment(opportunity_type=target_opp["type"], sample_size_per_group=500)
    print(json.dumps(exp_result, indent=2))
    print()

    print("SUMMARY MEASURED PERFORMANCE:")
    print(f" - Control Group (500): Conversion = {exp_result['control_group']['conversion_rate_pct']}%, AOV = INR {exp_result['control_group']['measured_aov_inr']:,.2f}")
    print(f" - AI-Targeted Group (500): Conversion = {exp_result['ai_targeted_group']['conversion_rate_pct']}%, AOV = INR {exp_result['ai_targeted_group']['measured_aov_inr']:,.2f}")
    print(f" - Relative Lift: {exp_result['measured_experiment_lift']['relative_conversion_lift']}x, Incremental Rev: INR {exp_result['measured_experiment_lift']['incremental_revenue_inr']:,.2f}")
    print("================================================================================")

if __name__ == "__main__":
    main()
