import json
from assistant import assistant
from main import load_stored_campaigns

print("================================================================================")
print("TEST 1: 'Find my biggest growth opportunity'")
print("================================================================================")
res1 = assistant.process_query("Find my biggest growth opportunity")
print("TOOL CALLS EXECUTED:", res1["tool_calls_executed"])
print("ASSISTANT REPLY:\n", res1["reply"])

print("\n================================================================================")
print("TEST 2: 'Create a campaign for this opportunity'")
print("================================================================================")
res2 = assistant.process_query("Create a campaign for this opportunity")
print("TOOL CALLS EXECUTED:", res2["tool_calls_executed"])
print("ASSISTANT REPLY:\n", res2["reply"])

print("\n================================================================================")
print("DATABASE / CAMPAIGN LIST CONFIRMATION (GET /api/campaigns / campaigns.json):")
print("================================================================================")
stored = load_stored_campaigns()
newest = stored[-1]
print(f"Total Campaigns Stored: {len(stored)}")
print("Newest Stored Campaign Record:")
print(json.dumps(newest, indent=2))
print("================================================================================")

print("\n================================================================================")
print("TEST 3: 'What should I promote today?'")
print("================================================================================")
res3 = assistant.process_query("What should I promote today?")
print("TOOL CALLS EXECUTED:", res3["tool_calls_executed"])
print("ASSISTANT REPLY:\n", res3["reply"])
print("================================================================================")
