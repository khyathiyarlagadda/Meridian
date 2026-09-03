import json
import sys
from assistant import assistant
from analytics import load_data, run_product_velocity_trends

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("================================================================================")
    print("MERIDIAN PHASE 11: AI ASSISTANT FUNCTION-CALLING VERIFICATION")
    print("================================================================================")

    # 1. Verification Query 1: Sales Drop
    q1 = "why did sales drop this week"
    res1 = assistant.process_query(q1)

    print(f"QUERY 1: '{q1}'")
    print(f"EXECUTED TOOL CALLS: {res1['tool_calls_executed']}")
    print(f"ASSISTANT REPLY:\n{res1['reply']}")
    print()

    # Compare with ground-truth backend numbers
    products, customers, transactions, order_items = load_data()
    trends_df = run_product_velocity_trends(products, transactions, order_items)
    declining = trends_df[trends_df['status'] == 'declining'].to_dict(orient="records")[0]

    print("REAL BACKEND NUMBERS FOR DECLINING SKU:")
    print(f" - Product ID: {declining['product_id']} ({declining['product_name']})")
    print(f" - Weekly Unit History: W-3={declining['units_w3']}, W-2={declining['units_w2']} ({declining['wow_change_w2']}%), W-1={declining['units_w1']} ({declining['wow_change_w1']}%)")
    print()

    # 2. Verification Query 2: Create Campaign
    q2 = "create a campaign for earbud cross sell"
    res2 = assistant.process_query(q2)

    print("--------------------------------------------------------------------------------")
    print(f"QUERY 2: '{q2}'")
    print(f"EXECUTED TOOL CALLS: {res2['tool_calls_executed']}")
    print(f"ASSISTANT REPLY:\n{res2['reply']}")
    print("================================================================================")

if __name__ == "__main__":
    main()
