import json
from ai_memory import compute_real_dataset_aggregations, initialize_or_load_memory

agg = compute_real_dataset_aggregations()
memories = initialize_or_load_memory()

print("================================================================================")
print("REAL DATASET AGGREGATION QUERY RESULT (WEEKEND VS WEEKDAY):")
print("================================================================================")
print(json.dumps(agg, indent=2))
print("================================================================================")
print("INITIALIZED MERIDIAN AI MEMORY ENTRIES:")
print("================================================================================")
print(json.dumps(memories, indent=2))
print("================================================================================")
