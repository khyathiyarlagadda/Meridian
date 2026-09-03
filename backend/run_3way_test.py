import json
from experiment import run_controlled_experiment

exp = run_controlled_experiment(opportunity_type="earbud_case_cross_sell", sample_size_per_group=500, seed=42)

print("================================================================================")
print("3-WAY MULTIVARIATE EXPERIMENT RUN OUTPUT:")
print("================================================================================")
print(json.dumps(exp, indent=2))
print("================================================================================")
