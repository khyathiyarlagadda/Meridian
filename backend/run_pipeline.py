import json
import sys
from analytics import load_data, run_rfm_analysis, run_market_basket_analysis, run_product_velocity_trends, generate_opportunities

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("================================================================================")
    print("MERIDIAN ANALYTICS PIPELINE: PATTERN REDISCOVERY RUN")
    print("================================================================================")
    
    products, customers, transactions, order_items = load_data()
    
    print(f"Loaded {len(products)} products, {len(customers)} customers, {len(transactions)} transactions, {len(order_items)} order items.")
    print()

    opportunities = generate_opportunities(products, customers, transactions, order_items)
    
    print("--------------------------------------------------------------------------------")
    print("SURFACED COMMERCIAL OPPORTUNITIES:")
    print("--------------------------------------------------------------------------------")
    print(json.dumps(opportunities, indent=2))
    print()

    print("================================================================================")
    print("INJECTED PATTERNS REDISCOVERY VERIFICATION SUMMARY")
    print("================================================================================")
    found_map = {
        "Pattern 1 (Earbud -> Phone Case Cross-Sell)": "OPP_EARBUD_CROSSSELL" in [o['id'] for o in opportunities],
        "Pattern 2 (Phone Case + Screen Protector Bundle)": "OPP_CASE_SCREEN_BUNDLE" in [o['id'] for o in opportunities],
        "Pattern 3 (Win-Back Cohort ~180)": "OPP_WINBACK_COHORT" in [o['id'] for o in opportunities],
        "Pattern 4 (Declining Product PROD_EAR_01)": "OPP_DECLINING_PRODUCT" in [o['id'] for o in opportunities],
        "Pattern 5 (Emerging Product PROD_WATCH_01)": "OPP_EMERGING_PRODUCT" in [o['id'] for o in opportunities],
        "Pattern 6 (High-Value-Lapsed Segment ~85)": "OPP_HIGH_VALUE_LAPSED" in [o['id'] for o in opportunities],
    }

    for pattern, found in found_map.items():
        status_str = "REDISCOVERED [FOUND]" if found else "MISSED [NOT FOUND]"
        print(f" - {pattern}: {status_str}")
    print("================================================================================")

if __name__ == "__main__":
    main()
